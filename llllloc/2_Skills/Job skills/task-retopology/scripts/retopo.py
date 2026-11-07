"""Retopologize a dense AI mesh with Instant Meshes, bake its texture, export GLB.

Run (cloud):  python3 -I retopo.py <model.glb> <out_dir> [--quads 5000 12000] [--tex 2048]
Needs:        python3 -m pip install bpy pynanoinstantmeshes numpy pillow
Writes:       <out_dir>/<name>_IM<N>k.glb per target, <name>_retopo_sheet.jpg, report.json
"""
import argparse, json, math, os, sys, time
import numpy as np
import bpy, bmesh
import pynanoinstantmeshes as nim
from mathutils.bvhtree import BVHTree
from mathutils import Vector

ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("out")
ap.add_argument("--quads", type=int, nargs="+", default=[5000, 12000])
ap.add_argument("--tex", type=int, default=2048)
ap.add_argument("--crease", type=float, default=0.0, help="degrees; 0 = smooth character, 30-45 = hard-surface")
a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)
name = os.path.splitext(os.path.basename(a.src))[0]

# 1 load, flatten transforms, weld UV-seam splits (glTF splits vertices at seams)
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=a.src)
meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
bpy.ops.object.select_all(action="DESELECT")
for o in meshes: o.select_set(True)
bpy.context.view_layer.objects.active = meshes[0]
bpy.ops.object.parent_clear(type="CLEAR_KEEP_TRANSFORM")
if len(meshes) > 1: bpy.ops.object.join()
src = bpy.context.active_object; src.name = "SRC"
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
bpy.ops.object.mode_set(mode="EDIT"); bpy.ops.mesh.select_all(action="SELECT")
bpy.ops.mesh.remove_doubles(threshold=1e-6 * max(src.dimensions)); bpy.ops.mesh.quads_convert_to_tris()
bpy.ops.object.mode_set(mode="OBJECT")
V = np.array([v.co[:] for v in src.data.vertices], dtype=np.float32)
F = np.array([p.vertices[:] for p in src.data.polygons], dtype=np.uint32)
diag = (Vector(np.max(V, 0)) - Vector(np.min(V, 0))).length
deg = bpy.context.evaluated_depsgraph_get(); bvh_src = BVHTree.FromObject(src, deg)
report = {"source": a.src, "source_tris": int(len(F)), "results": []}

sc = bpy.context.scene
sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = 4
bk = sc.render.bake
bk.use_selected_to_active = True; bk.cage_extrusion = 0.015 * diag; bk.max_ray_distance = 0.05 * diag
bk.use_pass_direct = False; bk.use_pass_indirect = False; bk.margin = 8

for q in a.quads:
    # 2 Instant Meshes. Pure-quad output subdivides once, so ask for a quarter of the target.
    t = time.time()
    v2, f2 = nim.remesh(V, F, vertex_count=-1, face_count=max(q // 4, 50), creaseAngle=a.crease,
                        smooth_iter=2, deterministic=True)
    v2 = np.asarray(v2); f2 = np.asarray(f2); secs = round(time.time() - t, 1)
    me = bpy.data.meshes.new(f"IM_{q}")
    faces = [list(dict.fromkeys(r.tolist())) for r in f2]
    me.from_pydata(v2.tolist(), [], [f for f in faces if len(f) >= 3]); me.validate(); me.update()
    lo = bpy.data.objects.new(f"{name}_IM{q // 1000}k", me); sc.collection.objects.link(lo)
    for p in me.polygons: p.use_smooth = True
    # 3 measure: quads, irregular vertices, distance to the source (% of the model's diagonal)
    bm = bmesh.new(); bm.from_mesh(me)
    nq = sum(1 for f in bm.faces if len(f.verts) == 4)
    inner = [v for v in bm.verts if not v.is_boundary]
    irr = sum(1 for v in inner if len(v.link_edges) != 4)
    holes = sum(1 for e in bm.edges if e.is_boundary); bm.free()
    deg = bpy.context.evaluated_depsgraph_get(); bvh_lo = BVHTree.FromObject(lo, deg)
    d = [bvh_src.find_nearest(v.co)[3] for v in me.vertices]
    step = max(1, len(V) // 40000); d += [bvh_lo.find_nearest(Vector(V[i]))[3] for i in range(0, len(V), step)]
    d = sorted(x for x in d if x is not None)
    # 4 UV + bake base color from SRC
    bpy.ops.object.select_all(action="DESELECT"); lo.select_set(True); bpy.context.view_layer.objects.active = lo
    bpy.ops.object.mode_set(mode="EDIT"); bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.smart_project(angle_limit=math.radians(66), island_margin=0.003); bpy.ops.object.mode_set(mode="OBJECT")
    img = bpy.data.images.new(lo.name + "_basecolor", a.tex, a.tex)
    mat = bpy.data.materials.new(lo.name + "_mat"); mat.use_nodes = True; nt = mat.node_tree
    tex = nt.nodes.new("ShaderNodeTexImage"); tex.image = img; nt.nodes.active = tex
    nt.links.new(tex.outputs["Color"], nt.nodes["Principled BSDF"].inputs["Base Color"])
    me.materials.append(mat)
    has_tex = any(n.type == "TEX_IMAGE" for m in src.data.materials if m and m.use_nodes for n in m.node_tree.nodes)
    if has_tex:
        src.select_set(True); bpy.context.view_layer.objects.active = lo
        bpy.ops.object.bake(type="DIFFUSE", pass_filter={"COLOR"})
        img.pack()
    # 5 export this mesh alone
    bpy.ops.object.select_all(action="DESELECT"); lo.select_set(True)
    out = os.path.join(a.out, lo.name + ".glb")
    bpy.ops.export_scene.gltf(filepath=out, use_selection=True, export_format="GLB")
    report["results"].append(dict(file=out, quads_target=q, faces=len(me.polygons), quad_pct=round(100 * nq / len(me.polygons), 1),
        irregular_vert_pct=round(100 * irr / max(len(inner), 1), 1), open_edges=holes, remesh_sec=secs, texture_baked=has_tex,
        dist_mean_pct=round(100 * sum(d) / len(d) / diag, 3), dist_p99_pct=round(100 * d[int(.99 * len(d))] / diag, 3),
        dist_max_pct=round(100 * d[-1] / diag, 3)))
    lo.hide_render = True

json.dump(report, open(os.path.join(a.out, "report.json"), "w"), indent=1)
print("REPORT", json.dumps(report))

# 6 contact sheet: source, then each result shaded + wireframe, front view
try:
    from PIL import Image, ImageDraw
except ImportError:
    sys.exit(0)
sc.cycles.samples = 16; sc.render.resolution_x = 600; sc.render.resolution_y = 800
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (0.9, 0.9, 0.92, 1); sc.view_settings.view_transform = "Standard"
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); sc.collection.objects.link(cam); sc.camera = cam
cam.data.type = "ORTHO"; cam.data.ortho_scale = 1.15 * max(src.dimensions.x, src.dimensions.z)
c = src.location + Vector(np.mean([np.min(V, 0), np.max(V, 0)], 0))
cam.location = c + Vector((0, 2 * diag, 0)); cam.rotation_euler = (math.radians(90), 0, math.radians(180))
sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN")); sun.data.energy = 3
sun.rotation_euler = (math.radians(50), 0, math.radians(150)); sc.collection.objects.link(sun)
dark = bpy.data.materials.new("dark"); dark.use_nodes = True
dark.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.02, 0.02, 0.05, 1)
shots = [("source", [src], f"AI model, {len(F):,} tris")]
for r in report["results"]:
    lo = bpy.data.objects[os.path.splitext(os.path.basename(r["file"]))[0]]
    wf = lo.copy(); wf.data = lo.data.copy(); sc.collection.objects.link(wf)
    wf.data.materials.clear(); wf.data.materials.append(dark)
    m = wf.modifiers.new("wf", "WIREFRAME"); m.thickness = 0.0018 * diag; m.use_replace = True
    shots.append((lo.name, [lo, wf], f"{r['faces']:,} quads, baked"))
allm = [o for o in sc.objects if o.type == "MESH"]
tiles = []
for key, show, label in shots:
    for o in allm: o.hide_render = o not in show
    p = os.path.join(a.out, f"_shot_{key}.png"); sc.render.filepath = p; bpy.ops.render.render(write_still=True)
    tiles.append((p, label))
W, H = 600, 800
sheet = Image.new("RGB", (W * len(tiles), H + 50), "white"); dr = ImageDraw.Draw(sheet)
for i, (p, label) in enumerate(tiles):
    sheet.paste(Image.open(p).convert("RGB"), (i * W, 50)); dr.text((i * W + 16, 12), label, fill="black", font_size=30)
    os.remove(p)
sheet.save(os.path.join(a.out, f"{name}_retopo_sheet.jpg"), quality=88)

"""render.py preview t1 t2 ... | frames START END [WORKERS] | missing   (v2, shutter motion blur)"""
import sys, os, time
import numpy as np
from PIL import Image
ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, os.environ.get('FRAMES_DIR', 'frames2')); PRE = os.path.join(ROOT, 'stills2')
os.makedirs(OUT, exist_ok=True); os.makedirs(PRE, exist_ok=True)
FILM = os.environ.get('FILM', 'film')     # the film module: draw_scene(c, t), post_np(x, t), shot_of(t)
SAMPLES = 4; SHUTTER = 0.5     # 180 degree shutter

def render_t(t, samples=SAMPLES):
    import skia, importlib; f = importlib.import_module(FILM)
    a, b, _ = f.shot_of(t)
    acc = None
    for k in range(samples):
        ts = t + (k / samples - 0.5 + 0.5 / samples) * SHUTTER / f.FPS if samples > 1 else t
        ts = min(max(ts, a), b - 1e-4)                  # never blur across a cut
        s = skia.Surface.MakeRaster(skia.ImageInfo.Make(f.W, f.H, skia.kRGBA_F16_ColorType, skia.kPremul_AlphaType))
        f.draw_scene(s.getCanvas(), ts)                 # half-float canvas: no 8-bit steps while drawing
        arr = s.makeImageSnapshot().toarray(colorType=skia.kRGBA_F16_ColorType)[..., :3].astype(np.float32)
        acc = arr if acc is None else acc + arr
    return f.post_np(acc / samples, t)               # vignette, moving grain, dither -> uint8

def work(args):
    lo, hi, step = args
    import importlib; f = importlib.import_module(FILM)
    n = 0
    for fr in range(lo, hi, step):
        p = os.path.join(OUT, 'f_%04d.png' % fr)
        if os.path.exists(p): continue
        Image.fromarray(render_t(fr / f.FPS)).save(p + '.tmp.png', compress_level=1); os.replace(p + '.tmp.png', p); n += 1
    return n

if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'preview':
        for ts in sys.argv[2:]:
            t0 = time.time(); a = render_t(float(ts), 1)
            Image.fromarray(a).save(os.path.join(PRE, 'p_%06.2f.jpg' % float(ts)), quality=90)
            print(ts, '%.2fs' % (time.time() - t0), flush=True)
    elif cmd == 'frames':
        lo, hi = int(sys.argv[2]), int(sys.argv[3]); k = int(sys.argv[4]) if len(sys.argv) > 4 else 2
        from multiprocessing import Pool
        t0 = time.time()
        with Pool(k) as pool: n = sum(pool.map(work, [(lo + i, hi, k) for i in range(k)]))
        print('rendered', n, 'in %.1fs' % (time.time() - t0))
    elif cmd == 'missing':
        import importlib; f = importlib.import_module(FILM)
        N = int(round(f.DUR * f.FPS))
        miss = [x for x in range(N) if not os.path.exists(os.path.join(OUT, 'f_%04d.png' % x))]
        print(len(miss), 'missing of', N, (miss[:5], miss[-5:]) if miss else '')

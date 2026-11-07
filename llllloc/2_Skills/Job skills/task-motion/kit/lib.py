"""a client Part 1 animation engine: shared helpers.
Pure functions of time. No randomness at draw time (seeded at load)."""
import math, re, os
import numpy as np
import skia
from svgelements import Path as SvgPath, Move, Line, CubicBezier, QuadraticBezier, Arc, Close

W, H, FPS = 1920, 1080, 30
ROOT = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(ROOT, 'assets')
SAMP = skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kLinear)

# ---------------------------------------------------------------- math / easing
def clamp(x, a=0.0, b=1.0): return a if x < a else (b if x > b else x)
def lerp(a, b, t): return a + (b - a) * t
def remap(t, a, b): return clamp((t - a) / (b - a)) if b != a else (1.0 if t >= b else 0.0)
def smooth(t): t = clamp(t); return t * t * (3 - 2 * t)
def smoother(t): t = clamp(t); return t * t * t * (t * (6 * t - 15) + 10)
def eout(t, p=3): t = clamp(t); return 1 - (1 - t) ** p
def ein(t, p=2): t = clamp(t); return t ** p
def eio(t, p=3):
    t = clamp(t)
    return 0.5 * (2 * t) ** p if t < 0.5 else 1 - 0.5 * (2 - 2 * t) ** p
def eback(t, s=1.4):
    t = clamp(t) - 1
    return t * t * ((s + 1) * t + s) + 1
def pulse(t, a, peak, b):
    """0 before a, rises to 1 at peak, falls to 0 at b (smooth)."""
    if t <= a or t >= b: return 0.0
    if t < peak: return smooth((t - a) / (peak - a))
    return smooth((b - t) / (b - peak))
def hexc(h, a=1.0):
    h = h.lstrip('#'); r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return skia.Color4f(r / 255, g / 255, b / 255, a)
def hexi(h, a=1.0):
    h = h.lstrip('#'); r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return skia.ColorSetARGB(int(clamp(a) * 255), r, g, b)
def mixhex(h1, h2, t):
    a = [int(h1.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)]
    b = [int(h2.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)]
    return '#%02x%02x%02x' % tuple(int(round(lerp(x, y, clamp(t)))) for x, y in zip(a, b))

def hash01(i, salt=0):
    x = math.sin(i * 127.1 + salt * 311.7) * 43758.5453
    return x - math.floor(x)
def noise1(t, seed=0):
    """cheap smooth 1D value noise in [-1,1]"""
    i = math.floor(t); f = t - i; u = f * f * (3 - 2 * f)
    return lerp(hash01(i, seed) * 2 - 1, hash01(i + 1, seed) * 2 - 1, u)

# ---------------------------------------------------------------- images
_img_cache = {}
def img(name):
    if name not in _img_cache:
        p = name if os.path.isabs(name) else os.path.join(A, name)
        _img_cache[name] = skia.Image.MakeFromEncoded(skia.Data.MakeFromFileName(p))
    return _img_cache[name]

def paint(alpha=1.0, blend=None, color=None, aa=True, **kw):
    p = skia.Paint(AntiAlias=aa)
    if color is not None:
        p.setColor4f(color if isinstance(color, skia.Color4f) else hexc(color))
    p.setAlphaf(clamp(alpha) * (p.getAlphaf() if color is not None else 1.0))
    if blend: p.setBlendMode(blend)
    for k, v in kw.items(): getattr(p, 'set' + k)(v)
    return p

def draw_img(c, im, x, y, w=None, h=None, alpha=1.0, blend=None, src=None):
    if alpha <= 0.002: return
    w = im.width() if w is None else w; h = im.height() if h is None else h
    s = src or skia.Rect.MakeWH(im.width(), im.height())
    c.drawImageRect(im, s, skia.Rect.MakeXYWH(x, y, w, h), SAMP, paint(alpha, blend))

def draw_img_c(c, im, cx, cy, scale=1.0, alpha=1.0, blend=None, rot=0.0, sx=1.0, sy=1.0):
    """draw image centred at (cx,cy) with uniform scale (image px -> screen px)"""
    if alpha <= 0.002 or scale <= 0: return
    c.save(); c.translate(cx, cy)
    if rot: c.rotate(rot)
    c.scale(scale * sx, scale * sy)
    c.drawImage(im, -im.width() / 2, -im.height() / 2, SAMP, paint(alpha, blend))
    c.restore()

def surface_image(w, h, fn):
    s = skia.Surface(int(w), int(h)); cc = s.getCanvas(); cc.clear(skia.ColorTRANSPARENT)
    fn(cc); return s.makeImageSnapshot()

def blurred(im, sigma):
    """return a blurred copy (padded) of an image"""
    pad = int(sigma * 3)
    def f(cc):
        p = skia.Paint(ImageFilter=skia.ImageFilters.Blur(sigma, sigma))
        cc.drawImage(im, pad, pad, SAMP, p)
    return surface_image(im.width() + 2 * pad, im.height() + 2 * pad, f)

def tinted(im, hexcol, alpha=1.0):
    def f(cc):
        p = skia.Paint(ColorFilter=skia.ColorFilters.Blend(hexi(hexcol, alpha), skia.BlendMode.kSrcIn))
        cc.drawImage(im, 0, 0, SAMP, p)
    return surface_image(im.width(), im.height(), f)

# ---------------------------------------------------------------- svg paths
def d_to_path(d):
    sp = SvgPath(d)
    p = skia.Path()
    for seg in sp:
        if isinstance(seg, Move): p.moveTo(seg.end.x, seg.end.y)
        elif isinstance(seg, Close): p.close()
        elif isinstance(seg, Line): p.lineTo(seg.end.x, seg.end.y)
        elif isinstance(seg, CubicBezier): p.cubicTo(seg.control1.x, seg.control1.y, seg.control2.x, seg.control2.y, seg.end.x, seg.end.y)
        elif isinstance(seg, QuadraticBezier): p.quadTo(seg.control.x, seg.control.y, seg.end.x, seg.end.y)
        elif isinstance(seg, Arc):
            for cb in seg.as_cubic_curves():
                p.cubicTo(cb.control1.x, cb.control1.y, cb.control2.x, cb.control2.y, cb.end.x, cb.end.y)
    return p

def subpaths(d):
    return [str(s) for s in SvgPath(d).as_subpaths()]

class Glyphs:
    """A text line outlined by Figma: whole path + letter groups (left->right)."""
    def __init__(self, d):
        self.path = d_to_path(d)
        b = self.path.computeTightBounds()
        self.x0, self.y0, self.w, self.h = b.left(), b.top(), b.width(), b.height()
        subs = []
        for sd in subpaths(d):
            pp = d_to_path(sd); bb = pp.computeTightBounds()
            if bb.width() <= 0 and bb.height() <= 0: continue
            subs.append((bb, pp))
        subs.sort(key=lambda s: s[0].left())
        groups = []
        for bb, pp in subs:
            placed = False
            for g in groups:
                gb = g['b']
                # counters / dots overlap an existing glyph horizontally
                ov = min(gb.right(), bb.right()) - max(gb.left(), bb.left())
                if ov > 0.5 * min(bb.width(), gb.width()):
                    g['p'].addPath(pp); g['b'] = skia.Rect.MakeLTRB(min(gb.left(), bb.left()), min(gb.top(), bb.top()), max(gb.right(), bb.right()), max(gb.bottom(), bb.bottom()))
                    placed = True; break
            if not placed: groups.append({'p': pp, 'b': bb})
        self.letters = groups

def load_text_holder():
    s = open(os.path.join(A, 'text_holder.svg')).read()
    out = {}
    for m in re.finditer(r'<path id="([^"]+)" d="([^"]+)"', s):
        out[m.group(1)] = Glyphs(m.group(2))
    for k in ('d8', 'd9'):
        s2 = open(os.path.join(A, k + '.svg')).read()
        m = re.search(r'<path id="%s" d="([^"]+)"' % k, s2)
        out[k] = Glyphs(m.group(1))
    return out

def draw_glyphs(c, g, x, y, scale=1.0, alpha=1.0, color='#FFFFFF', blend=None, letters=None, path=None):
    """draw text path so its tight bbox top-left sits at (x,y)."""
    if alpha <= 0.002: return
    c.save(); c.translate(x, y); c.scale(scale, scale); c.translate(-g.x0, -g.y0)
    c.drawPath(path if path is not None else g.path, paint(alpha, blend, color))
    c.restore()

def glow_path(c, path, color, sigma, alpha, blend=skia.BlendMode.kPlus):
    if alpha <= 0.002: return
    p = paint(alpha, blend, color)
    p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, sigma))
    c.drawPath(path, p)

def load_icons():
    icons = {}
    for f in sorted(os.listdir(os.path.join(A, 'icons'))):
        s = open(os.path.join(A, 'icons', f)).read()
        i = s.find('<g id="ICON'); t = s[i:]
        ds = re.findall(r'<path[^>]* d="([^"]+)"', t)
        p = skia.Path()
        for d in ds: p.addPath(d_to_path(d))
        icons[f[:-4]] = p
    return icons

def icon_sprite(path, size=160, stroke=1.6, color='#FCEEFF', glow=True, glow_amt=1.0):
    """48-unit icon path -> sprite image with the art-direction glow baked in."""
    k = size / 48.0; pad = int(size * 0.45); S = size + 2 * pad
    def f(cc):
        cc.translate(pad, pad); cc.scale(k, k)
        if glow:
            for colr, sig, a in (('#9B3BFF', 5.0, 0.80), ('#E27BFF', 1.7, 0.95)):
                pp = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=stroke * 1.4,
                                StrokeCap=skia.Paint.kRound_Cap, StrokeJoin=skia.Paint.kRound_Join)
                pp.setColor4f(hexc(colr, a * glow_amt))
                pp.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, sig))
                cc.drawPath(path, pp)
        pp = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=stroke,
                        StrokeCap=skia.Paint.kRound_Cap, StrokeJoin=skia.Paint.kRound_Join)
        pp.setColor4f(hexc(color)); cc.drawPath(path, pp)
    return surface_image(S, S, f)

# ---------------------------------------------------------------- orb
ORB_CX, ORB_CY, ORB_R = 2029.0, 1299.0, 900.0   # ring centre / radius inside the plate png
def draw_orb(c, cx, cy, R, rot=0.0, alpha=1.0, extra=0.0, gain=1.0):
    """ORB v9 REST plate, LIGHTEN blend. extra (0..1) fades in two rotated copies = full rim.
    gain > 1 adds a PLUS copy for flares."""
    plate = img('orb_raw1.png')
    s = R / ORB_R
    def one(rr, a, blend):
        if a <= 0.003: return
        c.save(); c.translate(cx, cy); c.rotate(rr); c.scale(s, s); c.translate(-ORB_CX, -ORB_CY)
        c.drawImage(plate, 0, 0, SAMP, paint(a, blend)); c.restore()
    one(rot, alpha, skia.BlendMode.kLighten)
    if extra > 0:
        one(rot - 56.6 * extra, alpha * extra, skia.BlendMode.kLighten)
        one(rot + 59.5 * extra, alpha * extra, skia.BlendMode.kLighten)
    if gain > 1.0:
        one(rot, alpha * clamp(gain - 1.0), skia.BlendMode.kPlus)

# ---------------------------------------------------------------- shapes
def radial(c, cx, cy, r, colors, stops=None, alpha=1.0, blend=None, sx=1.0, sy=1.0):
    if alpha <= 0.002 or r <= 0: return
    cols = [hexi(h, a * alpha) for h, a in colors]
    sh = skia.GradientShader.MakeRadial(skia.Point(0, 0), r, cols, stops)
    p = skia.Paint(AntiAlias=True, Shader=sh)
    if blend: p.setBlendMode(blend)
    c.save(); c.translate(cx, cy); c.scale(sx, sy)
    c.drawCircle(0, 0, r, p); c.restore()

def ring(c, cx, cy, r, width, color, alpha, blur=0.0, blend=None):
    if alpha <= 0.002 or r <= 0: return
    p = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=width)
    p.setColor4f(hexc(color, clamp(alpha)))
    if blur > 0: p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
    if blend: p.setBlendMode(blend)
    c.drawCircle(cx, cy, r, p)

def dot(c, x, y, r, color, alpha, blur=0.0, blend=None):
    if alpha <= 0.002 or r <= 0: return
    p = skia.Paint(AntiAlias=True); p.setColor4f(hexc(color, clamp(alpha)))
    if blur > 0: p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
    if blend: p.setBlendMode(blend)
    c.drawCircle(x, y, r, p)

def line(c, x1, y1, x2, y2, width, colors, stops=None, alpha=1.0, blur=0.0, blend=None, cap=True):
    if alpha <= 0.002: return
    cols = [hexi(h, a * alpha) for h, a in colors]
    sh = skia.GradientShader.MakeLinear([skia.Point(x1, y1), skia.Point(x2, y2)], cols, stops)
    p = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=width, Shader=sh)
    if cap: p.setStrokeCap(skia.Paint.kRound_Cap)
    if blur > 0: p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
    if blend: p.setBlendMode(blend)
    c.drawLine(x1, y1, x2, y2, p)

# ---------------------------------------------------------------- 3D
def fib_sphere(n, seed=0):
    pts = []
    g = math.pi * (3 - math.sqrt(5))
    for i in range(n):
        y = 1 - (i + 0.5) / n * 2
        r = math.sqrt(1 - y * y); th = g * i + seed
        pts.append((math.cos(th) * r, y, math.sin(th) * r))
    return np.array(pts)

def rot_yx(P, yaw, pitch):
    cy, sy = math.cos(yaw), math.sin(yaw); cp, sp = math.cos(pitch), math.sin(pitch)
    x = P[:, 0] * cy + P[:, 2] * sy; z = -P[:, 0] * sy + P[:, 2] * cy; y = P[:, 1]
    y2 = y * cp - z * sp; z2 = y * sp + z * cp
    return np.stack([x, y2, z2], 1)

# ---------------------------------------------------------------- frame post
def to_rgb(surface):
    a = surface.makeImageSnapshot().toarray(colorType=skia.ColorType.kRGBA_8888_ColorType)
    return a[..., :3]

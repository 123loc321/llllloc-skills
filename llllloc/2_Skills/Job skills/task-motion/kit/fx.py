"""fx.py - living-light helpers for llllloc:task-motion (from a client Part 1, 28 Sep 2026).
inner_flow: soft light drifting inside a card. rim_comet: a light running along a stroke.
living_background: drifting wide lights on the ground. All pure functions of t."""
import math, skia
from lib import radial, hexi
KB = skia.BlendMode

def inner_flow(c, rect, rad, t, alpha, seed=0.0):
    """drifting light inside a glass card: two soft blobs on slow Lissajous paths, clipped to the card"""
    if alpha <= 0.003: return
    x, y, w, h = rect
    c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), rad, rad), skia.ClipOp.kIntersect, True)
    for col, a, sp, ph in (('#A04BFF', 0.20, 0.45, 0.0), ('#4F6BFF', 0.16, 0.33, 2.2), ('#F07BFF', 0.10, 0.57, 4.0)):
        bx = x + w * (0.5 + 0.45 * math.sin(sp * t + ph + seed)); by = y + h * (0.55 + 0.45 * math.sin(sp * 1.37 * t + ph * 1.7 + seed))
        radial(c, bx, by, 0.75 * max(w, h), [(col, a * alpha), (col, 0)], blend=KB.kPlus, sx=1.0, sy=0.7)
    c.restore()

def rim_comet(c, rect, rad, phase, alpha, tail=0.22, col='#F4D8FF', glow='#C06BFF'):
    """a light running along the card stroke: bright head, fading tail, blurred halo"""
    if alpha <= 0.003: return
    x, y, w, h = rect
    pth = skia.Path(); pth.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x + 0.5, y + 0.5, w - 1, h - 1), rad, rad))
    pm = skia.PathMeasure(pth, True); L = pm.getLength()
    head = (phase % 1.0) * L; seg = tail * L
    t0 = (head - seg) % L
    sps = []
    for q0, q1 in (((t0, head),) if t0 <= head else ((t0, L - 0.01), (0.0, head))):
        sp = skia.Path(); pm.getSegment(q0, q1, sp, True); sps.append(sp)
    pa = pm.getPosTan(t0)[0]; pb = pm.getPosTan(head)[0]
    if (pb.x() - pa.x()) ** 2 + (pb.y() - pa.y()) ** 2 < 4: return
    pos = [i / 8 for i in range(9)]
    for wdt, blur, cc, am in ((10, 6, glow, 0.4), (2.2, 0, col, 0.95)):
        sh = skia.GradientShader.MakeLinear([pa, pb], [hexi(cc, am * alpha * q ** 2.2) for q in pos], pos)
        p = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=wdt, Shader=sh, BlendMode=KB.kPlus)
        if blur: p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
        for sp in sps: c.drawPath(sp, p)
    pt = pm.getPosTan(head)[0] if hasattr(pm, 'getPosTan') else None
    if pt is not None:
        radial(c, pt.x(), pt.y(), 38, [('#FFFFFF', 0.55 * alpha), (glow, 0.25 * alpha), (glow, 0)], [0, 0.3, 1], blend=KB.kPlus)


def living_background(c, t, W, H, lights, alpha=1.0):
    """drifting wide lights: lights = [(hex, strength, x_amp, x_speed, x_phase, y, y_amp, y_speed, radius, sx, sy), ...]
    speeds 0.2 to 0.6 rad/s. Additive. The move must be visible within 2 s, never busy."""
    for col, a, xa, xs, xp, y, ya, ys, rad, sx, sy in lights:
        radial(c, W / 2 + xa * math.sin(t * xs + xp), y + ya * math.sin(t * ys + xp * 0.7), rad,
               [(col, a), (col, 0.0)], alpha=alpha, blend=KB.kPlus, sx=sx, sy=sy)

"""fields.py - living gradients as float math (no PNG plates, no 8-bit steps).
Method (Stripe-style, 28 Sep 2026 research): a few soft color sources whose coordinates are warped by slow
sine flows that move against each other. Computed at 1/4 resolution in float32 (the fields have no detail
finer than that), upscaled with bicubic in float, handed to skia as a half-float image. No banding anywhere.
"""
import math, numpy as np, cv2, skia
from PIL import Image

W, H = 1920, 1080
DS = 4                                         # field resolution divider
w4, h4 = W // DS, H // DS
_yy, _xx = np.mgrid[0:h4, 0:w4].astype(np.float32)
YY = (_yy + 0.5) * DS; XX = (_xx + 0.5) * DS  # full-res pixel coordinates of each field sample

def hexf(h):
    h = h.lstrip('#'); return np.array([int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)], np.float32)

def to_image(rgb, alpha=None, size=(W, H)):
    """float RGB (h, w, 3) -> skia half-float image at `size` (bicubic in float)"""
    if rgb.shape[1] != size[0] or rgb.shape[0] != size[1]:
        rgb = cv2.resize(rgb, size, interpolation=cv2.INTER_CUBIC)
        if alpha is not None: alpha = cv2.resize(alpha, size, interpolation=cv2.INTER_CUBIC)
    a = np.ones(rgb.shape[:2], np.float32) if alpha is None else np.clip(alpha, 0, 1)
    rgba = np.dstack([np.clip(rgb, 0, None) * a[..., None], a]).astype(np.float16)   # premultiplied
    return skia.Image.fromarray(rgba, colorType=skia.kRGBA_F16_ColorType, alphaType=skia.kPremul_AlphaType)

# ---------------------------------------------------------------- horizon ground (replaces bg_horizon.png)
def _horizon_lut():
    """color along the glow, fitted once from his plate: center strip, heavy smoothing (the plate had blocks)"""
    bg = np.asarray(Image.open('assets/bg_horizon.png').convert('RGB')).astype(np.float32) / 255.0
    col = bg[:, 880:1040].mean(1)                                           # (1080, 3)
    col = cv2.GaussianBlur(np.ascontiguousarray(col[:, None, :]), (1, 0), sigmaX=0.3, sigmaY=18)[:, 0, :]
    ext = np.linspace(0, 1, 260)[:, None]                                   # extend below the frame
    top = hexf('#E6CCFF')
    tail = col[-1] * (1 - ext) + top * ext
    return np.concatenate([col, tail], 0)                                   # index = effective y (px)
HLUT = _horizon_lut()

def horizon(t, lift=0.0):
    """dark sky, curved glowing horizon. The curve breathes, color lobes travel along it."""
    u = (XX - W / 2) / (W / 2)
    curve = (118 + 22 * math.sin(t * 0.55)) * u ** 2                        # sides sit higher, the bow breathes
    wave = 16 * np.sin(u * 2.6 + t * 0.7) + 10 * np.sin(u * 5.1 - t * 0.9 + 1.3)   # the horizon line ripples slowly
    ye = np.clip(YY + curve + wave + lift, 0, len(HLUT) - 1.001)
    i0 = ye.astype(np.int32); f = (ye - i0)[..., None]
    base = HLUT[i0] * (1 - f) + HLUT[i0 + 1] * f
    glow = np.clip((ye - 520) / 560, 0, 1) ** 1.6                          # where the ground light lives
    # two color lobes run along the horizon in opposite directions (magenta, blue), plus a drifting sky light
    m1 = np.exp(-(((XX - (W / 2 + 620 * math.sin(t * 0.33))) / 520) ** 2))
    m2 = np.exp(-(((XX - (W / 2 - 660 * math.sin(t * 0.27 + 1.0))) / 560) ** 2))
    sky = np.exp(-(((XX - (W / 2 + 700 * math.sin(t * 0.19 + 2))) / 700) ** 2 + ((YY - 260 - 80 * math.sin(t * 0.4)) / 330) ** 2))
    out = base * (1 + 0.55 * glow[..., None] * (m1[..., None] * (hexf('#FF5CD6') - 0.45) + m2[..., None] * (hexf('#4F7BFF') - 0.45)))
    out += sky[..., None] * hexf('#2A1470') * 0.35
    return out

# ---------------------------------------------------------------- charcoal ground (replaces bg_charcoal.png)
def charcoal(t):
    base = hexf('#131116')
    corner = np.exp(-(((XX - 0) / 900) ** 2 + ((YY - 0) / 600) ** 2)) * 0.5
    fl = np.exp(-(((XX - (1000 + 380 * math.sin(t * 0.3))) / 700) ** 2 + ((YY - 1120) / 300) ** 2))
    fl2 = np.exp(-(((XX - (900 - 420 * math.sin(t * 0.24 + 1.4))) / 620) ** 2 + ((YY - 1100) / 260) ** 2))
    drift = np.exp(-(((XX - (W / 2 + 520 * math.sin(t * 0.21))) / 800) ** 2 + ((YY - (500 + 200 * math.sin(t * 0.17 + 1))) / 500) ** 2))
    out = np.broadcast_to(base, XX.shape + (3,)).copy()
    out += corner[..., None] * (hexf('#1D1823') - base)
    out += fl[..., None] * hexf('#2A1A56') * 0.9 + fl2[..., None] * hexf('#3A1760') * 0.6
    out += drift[..., None] * hexf('#1E1238') * 0.5
    return out

# ---------------------------------------------------------------- flowing mesh fill (buttons, card glass)
def mesh(t, w, h, colors, speed=1.0, seed=0.0, res=4):
    """a Stripe-like flowing gradient for a w x h box. colors: list of hex. Returns float RGB at (h//res, w//res)."""
    hw, hh = max(8, int(w // res)), max(8, int(h // res))
    y, x = np.mgrid[0:hh, 0:hw].astype(np.float32)
    x = x / hw; y = y / hh
    tt = t * speed
    # domain warp: coordinates bent by sines that move against each other
    xw = x + 0.18 * np.sin(y * 3.1 + tt * 0.9 + seed) + 0.08 * np.sin(y * 7.3 - tt * 1.3)
    yw = y + 0.18 * np.sin(x * 2.7 - tt * 0.7 + seed * 1.7) + 0.08 * np.sin(x * 6.1 + tt * 1.1)
    acc = np.zeros((hh, hw, 3), np.float32); wsum = np.zeros((hh, hw), np.float32)
    n = len(colors)
    for i, cc in enumerate(colors):
        ang = tt * (0.35 + 0.11 * i) + i * 2 * math.pi / n + seed
        cx = 0.5 + 0.42 * math.cos(ang); cy = 0.5 + 0.38 * math.sin(ang * 1.3 + i)
        wgt = np.exp(-(((xw - cx) / 0.42) ** 2 + ((yw - cy) / 0.55) ** 2) * 2.2)
        acc += wgt[..., None] * hexf(cc); wsum += wgt
    return acc / (wsum[..., None] + 1e-4)

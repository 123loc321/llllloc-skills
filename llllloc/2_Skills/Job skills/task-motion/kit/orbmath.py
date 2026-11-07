"""a client orb as pure math (resolution-free). Colors were matched once to ORB v9 REST;
the shape is smooth curves only: radial curves x low-order angular waves. No texture, no raster."""
import numpy as np, math
from scipy.signal import savgol_filter
from scipy.interpolate import CubicSpline
P = np.load('orb_polar.npy').astype(np.float64)      # used ONCE to fit the curves below
NA, NR = P.shape[:2]; RMAX = 1.45; K = 4
th = (np.arange(NA) + 0.5) / NA * 2 * np.pi
r_s = (np.arange(NR) + 0.5) / NR * RMAX
# 1) find the hard edge on every angle (largest drop in brightness near r = 1), smooth it around the circle
L = P.mean(2); band = (r_s > 0.95) & (r_s < 1.07); bi = np.where(band)[0]
edge = np.array([r_s[bi[np.argmin(np.diff(L[a, bi]))]] + 0.5 * RMAX / NR for a in range(NA)])
ef = np.fft.rfft(edge); ef[3:] = 0; edge = np.fft.irfft(ef, NA)          # keep only a smooth offset/oval
# 2) resample every angle so the edge sits exactly at u = 1
U = np.linspace(0, RMAX, NR)
Pn = np.stack([np.stack([np.interp(U * edge[a], r_s, P[a, :, ch]) for ch in range(3)], 1) for a in range(NA)])
def fit(mask_lo, mask_hi, win):
    sel = (U >= mask_lo) & (U <= mask_hi); us = U[sel]; out = []
    for k in range(K + 1):
        for fn in ((np.cos,) if k == 0 else (np.cos, np.sin)):
            w = fn(k * th)[:, None, None]
            c = (Pn[:, sel] * w).sum(0) / (NA if k == 0 else NA / 2)
            c = savgol_filter(c, win, 3, axis=0, mode='nearest')
            out.append((k, fn.__name__, CubicSpline(us, c, axis=0, extrapolate=True)))
    return out
# 3) two separate fields: the body inside the edge and the glow outside it. The edge between them stays a hard step.
IN = fit(0.0, 0.996, 21); OUT = fit(1.004, RMAX, 21)
R_FINE = np.linspace(0, RMAX, 8192)
TAB_IN = [(k, nm, cs(R_FINE)) for k, nm, cs in IN]
TAB_OUT = [(k, nm, cs(R_FINE)) for k, nm, cs in OUT]
RIM = np.where(R_FINE < 1, np.exp(-((1 - R_FINE) / 0.014) ** 2), 0.0)[:, None]      # thin hot line just inside the edge: pulses stay sharp
GLOW = np.where(R_FINE >= 1, 1.0, 0.0)[:, None]
FADE = np.clip((RMAX - R_FINE) / 0.06, 0, 1)[:, None]

def render(R, rot=0.0, rim=1.0, glow=1.0, full=0.0, form=1.0, spark=0.0, form_start=-90.0, ss=1, flow=None):
    """-> float RGB (S x S), orb centre at S/2. rot in degrees (clockwise, like skia)."""
    S = int(math.ceil(2 * RMAX * R)) | 1
    n = S * ss
    ax = (np.arange(n) + 0.5) / ss - S / 2
    X, Y = np.meshgrid(ax, ax)
    rr = np.hypot(X, Y) / R
    ang = np.arctan2(Y, X)
    idx = np.clip((rr / RMAX * (len(R_FINE) - 1)).astype(np.int32), 0, len(R_FINE) - 1)
    gain = (1 + (rim - 1) * RIM + (glow - 1) * GLOW) * FADE
    rrs = rr * R                                        # radius in pixels
    edge_s = np.clip(rrs - R + 0.5, 0, 1)[..., None]    # 1-pixel anti-aliased step: sharp at any size
    # flow: each light wave drifts at its own slow speed, so the colors inside the orb swirl (smooth, no noise)
    drift = {k: 0.0 for k in range(K + 1)}
    if flow is not None:
        for k, a, w, p in ((1, 18, 0.70, 0.3), (2, 38, 0.55, 1.9), (3, 50, 0.80, 4.1), (4, 55, 0.50, 2.7)):   # visible swirl (28 Sep: "not animated at all")
            drift[k] = math.radians(a * math.sin(w * flow + p) + 0.6 * a * math.sin(0.23 * w * flow + 2 * p))
    inside = (rrs < R + 1.0); outside = (rrs > R - 1.0)       # each field only where it is seen
    def eval_at(phase):
        res = np.zeros((n, n, 3))
        for tabs, m, wgt in ((TAB_IN, inside, 1 - edge_s), (TAB_OUT, outside, edge_s)):
            a = ang[m]; ii = idx[m]; acc = np.zeros((len(a), 3))
            for k, nm, tab in tabs:
                c = (tab * gain)[ii]
                if k == 0: acc += c
                else: acc += c * (np.cos if nm == 'cos' else np.sin)(k * (a - phase - drift[k]))[:, None]
            res[m] += acc * wgt[m]
        return res
    img = eval_at(math.radians(rot))
    if full > 0:
        img = np.maximum(img, full * np.maximum(eval_at(math.radians(rot + 56.6)), eval_at(math.radians(rot - 59.5))))
    if form < 1.0:
        d = (np.degrees(ang) - form_start) % 360.0; edge = form * 360.0
        drawn = np.clip((edge - d) / 10.0 + 0.5, 0, 1) * np.clip(d / 60.0, 0, 1) ** 1.5
        inner = np.clip((0.93 - rr) / 0.12, 0, 1)
        img = img * (inner * (0.25 + 0.6 * form) + (1 - inner) * drawn)[..., None]
        tip = np.exp(-((d - edge) / 5.0) ** 2) * spark
        ringp = np.exp(-((rr - 1.0) / 0.045) ** 2) * 1.8 + np.exp(-((rr - 1.02) / 0.12) ** 2) * 0.5
        img = img + (tip * ringp)[..., None] * np.array([1, 0.92, 1.0])
    img = np.where(img > 0.8, 0.8 + 0.2 * np.tanh((img - 0.8) / 0.2), img)   # soft shoulder: hot parts keep their shape
    img = np.clip(img, 0, 1)
    if ss > 1: img = img.reshape(S, ss, S, ss, 3).mean((1, 3))
    return img, S

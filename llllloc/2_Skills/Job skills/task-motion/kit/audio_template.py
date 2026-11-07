"""Sound design + music bed for a client Part 1, synthesized (no library samples, no paid generation).
Everything is placed on the VO word clock. Output: mix.wav (48 kHz stereo, -14 LUFS, -1 dBTP)."""
import numpy as np, soundfile as sf, pyloudnorm as pyln
from scipy import signal
import math, json

import pace, os
# Standalone: this part alone, mastered (mix2.wav). Chain mode (used by stitch.py): OFFSET = where this part
# starts in the whole film, TOTAL = whole film length, STEMS_OUT = folder for pre-master stems. No master, no tail fade.
OFFSET = float(os.environ.get('OFFSET', 0)); TOTAL = float(os.environ.get('TOTAL', pace.DUR)); STEMS_OUT = os.environ.get('STEMS_OUT')
SR = 48000; DUR = pace.DUR; N = int(round(SR * TOTAL))
rng = np.random.default_rng(3)
def T(t): return int(round((t + OFFSET) * SR))

sfx = np.zeros((N, 2)); mus = np.zeros((N, 2)); send = np.zeros((N, 2))

def place(bus, x, t, gain_db=0.0, pan=0.0, rev=0.0):
    """add mono or stereo clip x at time t (s). pan -1..1 (equal power)."""
    g = 10 ** (gain_db / 20)
    if x.ndim == 1:
        a = (pan + 1) * math.pi / 4
        x = np.stack([x * math.cos(a), x * math.sin(a)], 1) * math.sqrt(2)
    i0 = T(t)
    if i0 < 0: x = x[-i0:]; i0 = 0
    i1 = min(N, i0 + len(x))
    if i1 <= i0: return
    bus[i0:i1] += x[:i1 - i0] * g
    if rev > 0: send[i0:i1] += x[:i1 - i0] * g * rev

def env_ad(n, a, d, curve=4.0):
    e = np.ones(n); ia = max(1, int(a * SR)); e[:ia] = np.linspace(0, 1, ia) ** 2
    tt = np.arange(n - ia) / SR; e[ia:] = np.exp(-tt * curve / max(d, 1e-3))
    return e

def bandnoise_sweep(dur, f_start, f_end, bw=0.6, shape=None, seed=0):
    """noise shaped by a moving gaussian band (log freq), via STFT."""
    n = int(dur * SR); x = np.random.default_rng(seed).normal(0, 1, n + 2048)
    f, tt, Z = signal.stft(x, SR, nperseg=1024, noverlap=768)
    u = np.clip(tt / dur, 0, 1)
    fc = np.exp(np.log(f_start) + (np.log(f_end) - np.log(f_start)) * (u if shape is None else shape(u)))
    lf = np.log(np.maximum(f, 1.0))[:, None]
    M = np.exp(-0.5 * ((lf - np.log(fc)[None, :]) / bw) ** 2)
    _, y = signal.istft(Z * M, SR, nperseg=1024, noverlap=768)
    y = y[:n]; return y / (np.abs(y).max() + 1e-9)

def lp(x, fc, order=2):
    sos = signal.butter(order, fc, 'low', fs=SR, output='sos'); return signal.sosfilt(sos, x, axis=0)
def hp(x, fc, order=2):
    sos = signal.butter(order, fc, 'high', fs=SR, output='sos'); return signal.sosfilt(sos, x, axis=0)
def bp(x, f1, f2, order=2):
    sos = signal.butter(order, [f1, f2], 'band', fs=SR, output='sos'); return signal.sosfilt(sos, x, axis=0)

# ------------------------------------------------------------------ elements
def whoosh(dur, f0=300, f1=3000, peak=0.6, bw=0.55, seed=1):
    n = int(dur * SR); y = bandnoise_sweep(dur, f0, f1, bw, seed=seed)
    tt = np.linspace(0, 1, n)
    e = np.where(tt < peak, (tt / peak) ** 2.2, np.exp(-(tt - peak) / (1 - peak) * 4))
    return y * e

def sub_boom(dur=1.6, f0=62, f1=32, decay=0.9, drive=1.6):
    n = int(dur * SR); tt = np.arange(n) / SR
    f = f1 + (f0 - f1) * np.exp(-tt * 6); ph = 2 * np.pi * np.cumsum(f) / SR
    y = np.sin(ph) * np.exp(-tt / decay) * np.minimum(1, tt / 0.004)
    return np.tanh(y * drive) / np.tanh(drive)

def hit(size=1.0, bright=1.0, seed=2):
    b = sub_boom(1.8 * size, 70, 34, 0.55 * size)
    n = len(b); nz = np.random.default_rng(seed).normal(0, 1, n)
    body = lp(nz, 900 * bright) * np.exp(-np.arange(n) / SR / 0.09)
    click = hp(nz, 2500) * np.exp(-np.arange(n) / SR / 0.012)
    return 0.9 * b + 0.35 * body / (np.abs(body).max() + 1e-9) + 0.25 * bright * click / (np.abs(click).max() + 1e-9)

def tick(freq=3200, dur=0.05, noise=0.5, seed=0):
    n = int(dur * SR); tt = np.arange(n) / SR
    s = np.sin(2 * np.pi * freq * tt) * np.exp(-tt / 0.008)
    nz = hp(np.random.default_rng(seed).normal(0, 1, n), 3000) * np.exp(-tt / 0.003)
    y = s + noise * nz / (np.abs(nz).max() + 1e-9)
    return y / (np.abs(y).max() + 1e-9)

def glass(f=1800, dur=0.9, decay=0.35, seed=0):
    n = int(dur * SR); tt = np.arange(n) / SR
    y = np.zeros(n)
    for ratio, amp, dk in ((1, 1, 1), (2.76, 0.5, 0.6), (5.40, 0.25, 0.35), (8.93, 0.12, 0.2)):
        y += amp * np.sin(2 * np.pi * f * ratio * tt + ratio) * np.exp(-tt / (decay * dk))
    y *= np.minimum(1, tt / 0.002)
    return y / (np.abs(y).max() + 1e-9)

def sonar(f=1250, dur=0.7):
    n = int(dur * SR); tt = np.arange(n) / SR
    y = np.sin(2 * np.pi * f * tt) * np.exp(-tt / 0.12) * np.minimum(1, tt / 0.003)
    y += 0.35 * np.roll(y, int(0.11 * SR)) + 0.15 * np.roll(y, int(0.22 * SR))
    return y / (np.abs(y).max() + 1e-9)

def riser(dur=1.4, f0=180, f1=2400, tone=True, seed=4):
    n = int(dur * SR); tt = np.arange(n) / SR; u = tt / dur
    y = bandnoise_sweep(dur, f0 * 2, f1 * 2, 0.5, seed=seed) * 0.6
    if tone:
        f = f0 * (f1 / f0) ** (u ** 1.6); ph = 2 * np.pi * np.cumsum(f) / SR
        y += 0.35 * (np.sin(ph) + 0.5 * np.sin(ph * 1.5) + 0.3 * np.sin(ph * 2.01))
    return y * (u ** 2.4)

def reverse_swell(dur=0.5, seed=6):
    n = int(dur * SR); nz = np.random.default_rng(seed).normal(0, 1, n)
    y = bp(nz, 400, 6000) * np.exp(-np.arange(n) / SR / (dur * 0.35))
    return y[::-1] / (np.abs(y).max() + 1e-9)

def shimmer(dur=1.0, dens=60, lo=5000, hi=11000, seed=7):
    n = int(dur * SR); y = np.zeros(n); r = np.random.default_rng(seed)
    for _ in range(int(dens * dur)):
        f = r.uniform(lo, hi); L = int(r.uniform(0.02, 0.08) * SR); t0 = r.uniform(0, max(0.001, dur - L / SR - 0.001))
        tt = np.arange(L) / SR; g = np.sin(2 * np.pi * f * tt) * np.hanning(L)
        i = int(t0 * SR); y[i:i + L] += g * r.uniform(0.3, 1)
    return y / (np.abs(y).max() + 1e-9)

def thump(f=52, dur=0.45):
    n = int(dur * SR); tt = np.arange(n) / SR
    fr = f * (1 + 0.8 * np.exp(-tt * 30)); ph = 2 * np.pi * np.cumsum(fr) / SR
    y = np.sin(ph) * np.exp(-tt / 0.11) * np.minimum(1, tt / 0.003)
    y += 0.25 * lp(np.random.default_rng(9).normal(0, 1, n), 300) * np.exp(-tt / 0.03)
    return np.tanh(1.5 * y)

def swish(dur=0.28, seed=11):
    return whoosh(dur, 1200, 5000, 0.35, 0.5, seed)

# ------------------------------------------------------------------ music bed (synth pad + pulse)
def saw_stack(freqs, dur, detune=0.006, seed=0):
    n = int(dur * SR); tt = np.arange(n) / SR; r = np.random.default_rng(seed); y = np.zeros(n)
    for f in freqs:
        for d in (-detune, 0, detune):
            ph = r.uniform(0, 1)
            y += 2 * ((tt * f * (1 + d) + ph) % 1.0) - 1
    return y / (len(freqs) * 3)

def midi(m): return 440 * 2 ** ((m - 69) / 12)

def pad(chord, dur, att=1.2, rel=1.2, cutoff=1400, seed=0):
    y = saw_stack([midi(m) for m in chord], dur + rel, seed=seed)
    y = lp(y, cutoff, 2)
    n = len(y); tt = np.arange(n) / SR
    e = np.minimum(1, tt / att) * np.clip((dur + rel - tt) / rel, 0, 1)
    return y * e

def pluck(f, dur=0.35):
    n = int(dur * SR); tt = np.arange(n) / SR
    y = (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(4 * np.pi * f * tt)) * np.exp(-tt / 0.09) * np.minimum(1, tt / 0.002)
    return y


# ------------------------------------------------------------------ SFX v2 (film clock)
# S1 clock
def ang(t):
    u = min(max((t - 0.08) / 1.22, 0), 1); return 900.0 * (u ** 2.6)
k_prev = 0
for i in range(int(1.30 * SR / 64)):
    t = i * 64 / SR; k = int(ang(t) // 30)
    if k > k_prev:
        place(sfx, tick(2600 + 70 * k, 0.05, 0.6, seed=k), t, -21 + 0.25 * min(k, 20), pan=0.25 * math.sin(k)); k_prev = k
place(sfx, tick(1900, 0.08, 0.3), 0.08, -14)
place(sfx, whoosh(0.55, 300, 3000, 0.95, 0.5, seed=60), 0.80, -17, rev=0.2)       # hand spins up into a disc
place(sfx, reverse_swell(0.36, seed=61), 1.14, -13)
place(sfx, hit(0.8, 0.3, seed=3), 1.47, -10, rev=0.3)
place(sfx, glass(1320, 1.2, 0.3), 1.50, -22, rev=0.5)
# S2 vortex
r = np.random.default_rng(31); t = 1.55
while t < 4.30:
    dens = 12 + 30 * min(1, (t - 1.55) / 1.0) * (0.45 if 2.9 < t < 3.7 else 1.0)
    place(sfx, glass(r.uniform(1400, 4200), 0.25, 0.06, seed=int(t * 1000)), t, -28 + r.uniform(-3, 3), pan=r.uniform(-0.9, 0.9), rev=0.35)
    t += r.exponential(1 / dens)
place(sfx, whoosh(0.7, 500, 6000, 0.45, 0.55, seed=62), 1.62, -19, pan=-0.3, rev=0.2)
place(sfx, whoosh(0.9, 5000, 400, 0.15, 0.6, seed=63), 2.80, -22, pan=0.3)          # time slows
place(sfx, sonar(1180, 0.9), 3.77, -19, rev=0.5); place(sfx, thump(48, 0.4), 3.77, -15)
place(sfx, reverse_swell(0.62, seed=64), 4.34, -11, pan=0.35)
place(sfx, riser(0.55, 300, 2600, True, seed=65), 4.42, -16, pan=0.3)
place(sfx, hit(1.1, 0.25, seed=5), 4.97, -10, pan=0.2, rev=0.35)
place(sfx, glass(880, 2.0, 0.8), 4.99, -24, pan=0.3, rev=0.5)
# S3 sphere
for tt_ in (5.06, 5.18, 6.21, 6.57):
    place(sfx, tick(4400, 0.03, 0.7, seed=int(tt_ * 100)), tt_, -24, pan=-0.35)
for tt_, f0 in ((6.77, 1200), (7.64, 1500), (8.43, 1800)):
    place(sfx, swish(0.3, seed=int(tt_ * 10)), tt_ - 0.02, -16, pan=-0.35)
    place(sfx, glass(f0, 0.8, 0.25), tt_ + 0.2, -20, pan=-0.35, rev=0.3)
    place(sfx, whoosh(0.5, 600, 2400, 0.3, 0.5, seed=int(tt_ * 7)), tt_ - 0.05, -22, pan=0.4)    # sphere spin kick
for wave in (7.60, 8.39):
    for j in range(22):
        place(sfx, tick(3000 + 60 * j, 0.03, 0.4, seed=200 + j), wave + j * 0.011, -30, pan=0.1 + 0.03 * j)
r = np.random.default_rng(33)
for j in range(9):
    place(sfx, sonar(r.uniform(1100, 1700), 0.6), 8.62 + j * 0.15 + r.uniform(0, 0.07), -25, pan=r.uniform(0.1, 0.7), rev=0.4)
place(sfx, riser(1.2, 150, 2200, True, seed=34), 9.0, -17, rev=0.2)
# S4 770
tt_ = 10.21
while tt_ < 10.92:
    u = (tt_ - 10.21) / 0.71
    place(sfx, tick(5200, 0.02, 0.9, seed=int(tt_ * 997)), tt_, -27, pan=0.05); tt_ += 0.018 + 0.07 * u ** 2
for lt in (10.72, 10.82, 10.92): place(sfx, tick(2200, 0.06, 0.3), lt, -19)
place(sfx, hit(1.0, 0.4, seed=6), 10.94, -11, rev=0.3); place(sfx, whoosh(0.6, 3000, 600, 0.1, 0.6, seed=66), 10.95, -21)
place(sfx, tick(6000, 0.05, 1.0), 11.25, -17); place(sfx, thump(60, 0.35), 11.25, -15)
place(sfx, shimmer(0.7, 50, 6000, 12000, seed=35), 12.27, -24, rev=0.5)
place(sfx, reverse_swell(0.45, seed=36), 13.52, -12)
place(sfx, whoosh(0.9, 3000, 300, 0.12, 0.7, seed=37), 13.92, -12, rev=0.3)
place(sfx, hit(0.6, 1.0, seed=7), 14.40, -11, rev=0.3)
# S5 fly-through
r = np.random.default_rng(38); t = 14.5
while t < 16.6:
    place(sfx, tick(r.uniform(2500, 7000), 0.03, 0.6, seed=int(t * 911)), t, -31 + r.uniform(-3, 3), pan=r.uniform(-1, 1), rev=0.2); t += r.exponential(1 / 18)
for tt_, pn in ((14.55, -0.7), (14.85, 0.7), (15.25, -0.4)):
    place(sfx, whoosh(0.5, 900, 4000, 0.45, 0.5, seed=int(tt_ * 13)), tt_, -21, pan=pn)
place(sfx, whoosh(1.1, 2000, 9000, 0.5, 0.4, seed=39), 15.10, -21, pan=-0.6)
for j in range(5):
    place(sfx, bp(np.random.default_rng(70 + j).normal(0, 1, int(0.05 * SR)), 1500, 7000), 16.12 + j * 0.07, -27, pan=0.3 * (-1) ** j)
# S6 converge + orb forms + act
place(sfx, whoosh(1.2, 250, 2500, 0.75, 0.6, seed=40), 16.60, -14, pan=-0.2, rev=0.3)
place(sfx, riser(0.95, 160, 2400, True, seed=41), 18.18, -19, rev=0.25)
place(sfx, shimmer(0.9, 60, 3000, 9000, seed=67), 18.20, -27, rev=0.4)
place(sfx, sub_boom(2.0, 66, 30, 0.8), 19.10, -10, rev=0.3)
place(sfx, shimmer(1.4, 40, 4000, 10000, seed=42), 19.43, -21, rev=0.6); place(sfx, glass(587.3, 2.4, 0.9), 19.43, -21, rev=0.6)
# S7 heartbeat + name
place(sfx, thump(50, 0.5), 20.26, -8); place(sfx, thump(48, 0.5), 20.52, -11)
place(sfx, whoosh(0.7, 500, 6000, 0.8, 0.5, seed=43), 20.60, -16, rev=0.3)
place(sfx, glass(660, 3.0, 1.2), 20.94, -18, rev=0.6); place(sfx, glass(990, 3.0, 1.0), 21.00, -21, pan=0.2, rev=0.6)
place(sfx, shimmer(0.5, 70, 7000, 13000, seed=44), 21.42, -25, rev=0.4)
# S8 senses + UI
place(sfx, whoosh(0.55, 300, 3500, 0.55, 0.6, seed=46), 21.90, -15, pan=-0.5, rev=0.3)   # orb swings to the edge
place(sfx, swish(0.3, seed=47), 22.22, -16, pan=0.45); place(sfx, glass(2400, 0.5, 0.15), 22.50, -20, pan=0.45)   # card lands on "senses"
place(sfx, sonar(900, 0.8), 22.55, -26, rev=0.4)
for n_ in range(18): place(sfx, tick(6400, 0.025, 0.3, seed=300 + n_), 22.92 + n_ * 0.36, -32, pan=0.3)
for tt_ in (23.93, 25.75):
    place(sfx, swish(0.26, seed=int(tt_ * 10)), tt_, -17, pan=0.45); place(sfx, glass(2100, 0.5, 0.14), tt_ + 0.14, -21, pan=0.45)
nn = int(0.7 * SR); tt2 = np.arange(nn) / SR; ff = 700 + 900 * (tt2 / 0.7) ** 1.3
place(sfx, np.sin(2 * np.pi * np.cumsum(ff) / SR) * np.hanning(nn) * 0.6, 24.36, -30, pan=0.45)   # chart draws itself
place(sfx, whoosh(0.6, 1500, 5000, 0.5, 0.35, seed=50), 25.05, -24, pan=0.45)
place(sfx, shimmer(0.6, 40, 6000, 12000, seed=68), 26.75, -27, pan=0.45)
place(sfx, glass(1760, 0.5, 0.14), 28.14, -22, pan=0.45)
place(sfx, whoosh(0.5, 2000, 6000, 0.6, 0.4, seed=51), 27.62, -27, pan=0.6)
place(sfx, tick(3600, 0.04, 0.7), 28.27, -16, pan=0.4)
place(sfx, thump(62, 0.3), 28.27, -17)                                              # the press
place(sfx, shimmer(0.8, 90, 5000, 12500, seed=77), 28.29, -23, pan=0.45, rev=0.45)   # gradient floods the button
place(sfx, glass(1318.5, 1.2, 0.35), 28.29, -19, pan=0.35, rev=0.4); place(sfx, glass(1760.0, 1.4, 0.45), 28.39, -19, pan=0.35, rev=0.4)
place(sfx, whoosh(0.3, 5000, 1500, 0.3, 0.5, seed=52), 28.98, -18)
place(sfx, hit(1.2, 0.8, seed=9), 29.22, -7, rev=0.4); place(sfx, whoosh(0.45, 300, 6000, 0.25, 0.7, seed=53), 29.20, -10, rev=0.3)

# ------------------------------------------------------------------ music bed v2
place(mus, pad([50, 57, 62, 65, 69], 5.0, att=0.8, rel=0.8, cutoff=900, seed=1), 0.0, -24)
place(mus, pad([46, 53, 58, 62, 65], 5.3, att=0.4, rel=0.9, cutoff=1100, seed=2), 4.98, -24)
place(mus, pad([48, 55, 60, 64, 67], 4.2, att=0.4, rel=0.8, cutoff=1300, seed=3), 10.25, -24)
place(mus, pad([50, 57, 62, 65, 72], 4.8, att=0.3, rel=0.4, cutoff=1500, seed=4), 14.40, -26)
bpm = 120; step = 60 / bpm / 2; notes = [62, 65, 69, 72]; k = 0; t = 14.40
while t < 19.10:
    m = notes[k % 4] + (12 if t > 18.2 else 0)
    place(mus, pluck(midi(m), 0.3), t, -35 + 6 * min(1, (t - 14.4) / 4.7), pan=0.4 * math.sin(k * 1.3)); t += step; k += 1
place(mus, pad([46, 53, 58, 62, 69], 1.2, att=0.6, rel=0.8, cutoff=900, seed=5), 19.30, -30)
place(mus, pad([53, 57, 60, 64, 69], 5.6, att=0.25, rel=1.0, cutoff=1800, seed=6), 20.94, -25)
k = 0; t = 22.30
while t < 29.1:
    m = [65, 69, 72, 76, 74, 69][k % 6]
    place(mus, pluck(midi(m), 0.3), t, -36, pan=0.5 * math.sin(k * 0.9)); t += step; k += 1
place(mus, pad([50, 57, 62, 65, 69], 0.6, att=0.02, rel=0.4, cutoff=2400, seed=7), 29.22, -22)
# ------------------------------------------------------------------ reverb send (synthetic stereo IR)
L = int(2.2 * SR); tt = np.arange(L) / SR
ir = np.stack([np.random.default_rng(90).normal(0, 1, L), np.random.default_rng(91).normal(0, 1, L)], 1) * np.exp(-tt / 0.55)[:, None]
ir = lp(ir, 6000); ir /= np.sqrt((ir ** 2).sum(0))
wet = np.stack([signal.fftconvolve(send[:, i], ir[:, i])[:N] for i in range(2)], 1)

# ------------------------------------------------------------------ VO + ducking + master
vo, sr0 = sf.read('vo.wav'); assert sr0 == SR
src = vo[:int(pace.VO_END_OLD * SR)].copy(); fade = int(0.03 * SR); src[-fade:] *= np.linspace(1, 0, fade)[:, None]
vo = np.zeros((N, 2)); pts = [0.0] + [c for c, d in pace.cuts()] + [pace.VO_END_OLD]
for i in range(len(pts) - 1):
    s0, s1 = int(pts[i] * SR), int(pts[i + 1] * SR); o = int(round((pts[i] + pace.shift(pts[i] + 1e-6) + OFFSET) * SR))
    seg = src[s0:s1].copy(); f2 = min(96, len(seg) // 2)
    seg[:f2] *= np.linspace(0, 1, f2)[:, None]; seg[-f2:] *= np.linspace(1, 0, f2)[:, None]
    vo[o:o + len(seg)] += seg[:max(0, N - o)]
# ducking envelope from VO level (smoothed)
lvl = np.sqrt(signal.lfilter([1], [1, -0.999], (vo ** 2).mean(1)) * 0.001)
duck_db = np.clip((20 * np.log10(lvl + 1e-6) + 45) / 15, 0, 1) * -7.0
duck = 10 ** (lp(duck_db, 6, 1) / 20)
music_bus = mus * duck[:, None] * 10 ** (13 / 20)
fx_bus = sfx * (10 ** (lp(duck_db * 0.8, 6, 1) / 20))[:, None]
mix = vo * 1.0 + fx_bus + music_bus + wet * 0.35
if STEMS_OUT:
    os.makedirs(STEMS_OUT, exist_ok=True)
    for nm, x in (('vo', vo), ('sfx', fx_bus + wet * 0.35), ('music', music_bus)):
        sf.write(os.path.join(STEMS_OUT, nm + '.wav'), x.astype(np.float32), SR, subtype='FLOAT')
    print('stems ->', STEMS_OUT); raise SystemExit
# gentle glue + loudness to -14 LUFS, true-peak safety
meter = pyln.Meter(SR)
lufs = meter.integrated_loudness(mix)
mix *= 10 ** ((-14.0 - lufs) / 20)
pk = np.abs(mix).max()
if pk > 10 ** (-2.0 / 20):
    # soft-knee limiter on the peaks only
    th = 10 ** (-2.5 / 20)
    mix = np.where(np.abs(mix) > th, np.sign(mix) * (th + (1 - th) * np.tanh((np.abs(mix) - th) / (1 - th))), mix)
    mix *= 10 ** ((-14.0 - meter.integrated_loudness(mix)) / 20)
mix = np.clip(mix, -0.84, 0.84)
tail = int(0.05 * SR); mix[-tail:] *= np.linspace(1, 0, tail)[:, None]
sf.write('mix2.wav', mix, SR, subtype='PCM_24')
sf.write('stem2_sfx.wav', fx_bus + wet * 0.35, SR, subtype='PCM_24')
sf.write('stem2_music.wav', music_bus, SR, subtype='PCM_24')
sf.write('stem2_vo.wav', vo, SR, subtype='PCM_24')
print('LUFS', round(meter.integrated_loudness(mix), 2), 'peak dBFS', round(20 * np.log10(np.abs(mix).max()), 2))

"""VO pacing v2: silence added between phrases. The voice is never time-stretched.
old = original VO clock, new = film clock."""
import json, numpy as np
GAPS = [(0.76, 1.14, 0.35),   # "Every minute," | "QuickCommerce"
        (3.78, 4.36, 0.35),   # "can watch." | "By 2030,"
        (4.92, 5.36, 0.15),   # "By 2030," | "thousands of stores,"
        (6.40, 6.74, 0.15),   # "stores," | "products,"
        (7.04, 7.26, 0.15),   # "products," | "and signals"
        (12.34, 13.10, 0.25), # "a day." | "The challenge"
        (20.02, 20.58, 0.35), # "That's a client." | "It senses,"
        (21.30, 21.52, 0.90), # "senses," | "diagnoses,"
        (22.06, 22.38, 0.90), # "diagnoses," | "and recommends"
        (24.02, 24.08, 0.50)] # "the next move" | "in real time."
VO_END_OLD = 25.52; TAIL = 0.25
_cut = None
def cuts():
    """quietest 10 ms point inside each gap (computed once from vo.wav)"""
    global _cut
    if _cut is None:
        import soundfile as sf
        x, sr = sf.read('vo.wav'); m = x.mean(1)
        out = []
        for a, b, d in GAPS:
            best, bt = 9, (a + b) / 2
            for t in np.arange(a, b - 0.01, 0.005):
                s = m[int(t * sr):int((t + 0.01) * sr)]; e = np.sqrt((s ** 2).mean())
                if e < best: best, bt = e, t + 0.005
            out.append((bt, d))
        _cut = out
    return _cut
def shift(old):
    return sum(d for c, d in cuts() if old >= c)
def new(old): return old + shift(old)
DUR = VO_END_OLD + sum(g[2] for g in GAPS) + TAIL + 0.08
def words():
    w = json.load(open('words.json'))
    return [(new(a), new(b) if b > a else new(a), t.strip()) for a, b, t in w if a < 25.5]
if __name__ == '__main__':
    print('cuts', [(round(c, 3), d) for c, d in cuts()]); print('DUR', DUR, 'frames', int(round(DUR * 30)))
    for a, b, t in words(): print(f'{a:6.2f} {b:6.2f} {t}')

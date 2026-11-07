"""sync.py - text-to-voice check. Every on-screen text event must become readable
(50% opacity) between 3 frames BEFORE and 1 frame AFTER the onset of its word.
Window from ITU-R BT.1359: sound ahead of picture is noticed at 45 ms, sound behind at 125 ms.
Onset: the whisper word start, unless that start sits in silence (whisper stretches a word back
over a pause), then the first 10 ms window above -40 dBFS after it.
Usage: python3 sync.py   (exits 1 when any event is outside the window)"""
import sys, numpy as np, soundfile as sf
import pace

FPS = 30; SR = 48000; THR_DB = -40.0; WIN = 0.010

# (event, word as whisper wrote it, occurrence, time the text reaches 50% opacity, film clock)
EVENTS = [
    ('a client first letter', 'a client.', 0, 20.91),        # letters: tk = a client - 0.14 + 0.045k, 50% at tk + 0.125
    ('chip "Senses"', 'senses,', 0, 22.49),                # ca = smooth(22.40 -> 22.58)
    ('chip "Diagnoses"', 'diagnoses,', 0, 24.18),          # morph 24.06 -> 24.30, text 50% at mid
    ('chip "Recommends"', 'recommends', 0, 26.00),         # morph 25.88 -> 26.12
    ('chip "Real time"', 'real', 0, 28.18),                # morph 28.12 -> 28.24
]

def paced_vo():
    vo, sr = sf.read('vo.wav'); assert sr == SR
    N = int(pace.DUR * SR); out = np.zeros(N)
    src = vo[:int(pace.VO_END_OLD * SR)].mean(1)
    pts = [0.0] + [c for c, d in pace.cuts()] + [pace.VO_END_OLD]
    for a, b in zip(pts[:-1], pts[1:]):
        o = int(round(pace.new(a) * SR)); seg = src[int(a * SR):int(b * SR)]
        out[o:o + len(seg)] += seg[:max(0, N - o)]
    return out

def onset(db, t_word):
    """whisper start if it sits in sound; if it sits in silence, walk forward to the first loud window"""
    k = int(round(t_word / WIN))
    while k < len(db) - 1 and db[k] <= THR_DB: k += 1
    return k * WIN

if __name__ == '__main__':
    x = paced_vo(); w = int(WIN * SR); n = len(x) // w
    db = 20 * np.log10(np.sqrt((x[:n * w].reshape(n, w) ** 2).mean(1)) + 1e-9)
    words = pace.words(); bad = 0
    print('%-26s %-12s %8s %8s %8s  %s' % ('event', 'word', 'whisper', 'onset', 'lands', 'offset (frames)'))
    for ev, word, occ, lands in EVENTS:
        hits = [s for s, e, wd in words if wd == word]
        ws = hits[occ]; on = onset(db, ws)
        off = (on - lands) * FPS                      # positive = text ready before the voice
        ok = -1.0 <= off <= 3.0
        bad += not ok
        print('%-26s %-12s %8.2f %8.2f %8.2f  %+5.1f %s' % (ev, word, ws, on, lands, off, 'OK' if ok else 'FAIL'))
    print('ALL OK' if not bad else '%d FAIL' % bad)
    sys.exit(1 if bad else 0)

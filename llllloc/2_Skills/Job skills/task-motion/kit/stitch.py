"""stitch.py - join finished parts into one film WITHOUT rendering any part again.

Picture: each part keeps a MEZZ file (near-lossless H.264, rendered in CHAIN mode: no fade to black at
its end). The transition INTO a part lives in that part's own first second, so the joins are already
designed. stitch.py decodes the MEZZ files in order and encodes the whole film once.

Sound: sound is cheap, so it is rebuilt, not glued. Each part's audio script runs again in chain mode
(env OFFSET = where the part starts, TOTAL = film length, STEMS_OUT = folder). All parts write into one
long timeline, so reverb tails and music releases ring across the joins. Then one master pass:
-14 LUFS, soft-knee limiter, true peak under -1 dBTP.

Usage:  python3 stitch.py stitch.json
stitch.json:
{ "fps": 30, "out": "FILM.mp4", "crf": 16,
  "parts": [ {"name": "P1", "dir": "P1", "mezz": "P1/P1_MEZZ.mp4", "audio": "audio2.py", "frames": 897},
             {"name": "P2", "dir": "P2", "mezz": "P2/P2_MEZZ.mp4", "audio": "audio.py",  "frames": 900} ] }
"""
import sys, os, json, subprocess, tempfile
import numpy as np, soundfile as sf, pyloudnorm as pyln

SR = 48000

def probe_frames(path):
    out = subprocess.run(['ffprobe', '-v', 'error', '-count_frames', '-select_streams', 'v:0', '-show_entries',
                          'stream=nb_read_frames', '-of', 'csv=p=0', path], capture_output=True, text=True).stdout
    return int(out.strip())

def master(mix):
    meter = pyln.Meter(SR)
    mix = mix * 10 ** ((-14.0 - meter.integrated_loudness(mix)) / 20)
    th = 10 ** (-2.5 / 20)
    if np.abs(mix).max() > 10 ** (-2.0 / 20):
        mix = np.where(np.abs(mix) > th, np.sign(mix) * (th + (1 - th) * np.tanh((np.abs(mix) - th) / (1 - th))), mix)
        mix = mix * 10 ** ((-14.0 - meter.integrated_loudness(mix)) / 20)
    mix = np.clip(mix, -0.84, 0.84)
    tail = int(0.05 * SR); mix[-tail:] *= np.linspace(1, 0, tail)[:, None]
    return mix, meter.integrated_loudness(mix)

def main(cfg_path):
    cfg = json.load(open(cfg_path)); base = os.path.dirname(os.path.abspath(cfg_path)); fps = cfg.get('fps', 30)
    parts = cfg['parts']
    # 1) frame counts: from the file, checked against the config
    for p in parts:
        n = probe_frames(os.path.join(base, p['mezz']))
        if p.get('frames') and n != p['frames']:
            sys.exit('%s: MEZZ has %d frames, config says %d' % (p['name'], n, p['frames']))
        p['frames'] = n
    starts = np.cumsum([0] + [p['frames'] for p in parts])[:-1]
    total_frames = int(sum(p['frames'] for p in parts)); total = total_frames / fps
    print('parts:', [(p['name'], p['frames'], round(s / fps, 3)) for p, s in zip(parts, starts)], 'total', round(total, 3), 's')
    # 2) sound: every part rebuilds its stems on the whole-film timeline
    tmp = tempfile.mkdtemp(prefix='stitch_')
    bus = np.zeros((int(round(total * SR)), 2))
    for p, s in zip(parts, starts):
        so = os.path.join(tmp, p['name'])
        env = dict(os.environ, OFFSET=str(s / fps), TOTAL=str(total), STEMS_OUT=so)
        subprocess.run([sys.executable, p['audio']], cwd=os.path.join(base, p['dir']), env=env, check=True)
        for nm in ('vo', 'sfx', 'music'):
            x, sr = sf.read(os.path.join(so, nm + '.wav')); assert sr == SR
            n = min(len(x), len(bus)); bus[:n] += x[:n]
    mix, lufs = master(bus)
    wav = os.path.join(tmp, 'mix.wav'); sf.write(wav, mix, SR, subtype='PCM_24')
    print('audio LUFS %.1f  peak %.2f dBFS' % (lufs, 20 * np.log10(np.abs(mix).max())))
    # 3) picture: decode the MEZZ files in order, encode once
    ins = [];
    for p in parts: ins += ['-i', os.path.join(base, p['mezz'])]
    n = len(parts); fc = ''.join('[%d:v]' % i for i in range(n)) + 'concat=n=%d:v=1:a=0[v]' % n
    out = os.path.join(base, cfg['out'])
    cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y'] + ins + ['-i', wav, '-filter_complex', fc,
           '-map', '[v]', '-map', '%d:a' % n, '-r', str(fps), '-c:v', 'libx264', '-profile:v', 'high', '-pix_fmt', 'yuv420p',
           '-crf', str(cfg.get('crf', 14)), '-preset', 'slow', '-x264-params', 'aq-mode=3:aq-strength=0.8:psy-rd=1.0,0:deblock=-1,-1', '-g', str(fps * 2),
           '-c:a', 'aac', '-b:a', '320k', '-ar', '48000', '-movflags', '+faststart', '-shortest', out]
    subprocess.run(cmd, check=True)
    got = probe_frames(out)
    print('film:', out, got, 'frames', 'OK' if got == total_frames else 'FRAME COUNT MISMATCH (expected %d)' % total_frames)

if __name__ == '__main__':
    main(sys.argv[1])

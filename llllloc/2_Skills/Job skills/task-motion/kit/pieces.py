"""pieces.py - OLD: for the cloud device link only. Not used on the Mac, files are written in place (29 Oct 2026).
It cut a file into 16 MB pieces with 8 bytes RAWPIECE in front, then printed the join command and the md5.
Usage: python3 pieces.py <file> <outdir> [prefix]"""
import sys, os, hashlib
src, outdir = sys.argv[1], sys.argv[2]; pre = sys.argv[3] if len(sys.argv) > 3 else 'PIECE'
d = open(src, 'rb').read(); n = 16 * 1024 * 1024; os.makedirs(outdir, exist_ok=True); names = []
for i, s in enumerate(range(0, len(d), n)):
    nm = '%s.raw_%d' % (pre, i); open(os.path.join(outdir, nm), 'wb').write(b'RAWPIECE' + d[s:s + n]); names.append(nm)
print('md5', hashlib.md5(d).hexdigest(), 'bytes', len(d), 'pieces', len(names))
print('join on the drive:  (' + '; '.join('tail -c +9 _DELETE/%s' % x for x in names) + ') > "%s" && md5sum "%s"' % (os.path.basename(src), os.path.basename(src)))

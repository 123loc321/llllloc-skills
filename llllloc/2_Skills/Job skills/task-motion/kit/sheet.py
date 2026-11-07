import sys, glob
from PIL import Image, ImageDraw
fs = sys.argv[2:] if len(sys.argv) > 2 else sorted(glob.glob('stills/*.jpg'))
out = sys.argv[1]
cols = 3; tw, th = 640, 360
rows = (len(fs) + cols - 1) // cols
S = Image.new('RGB', (cols * tw, rows * (th + 4)), (30, 30, 30))
for i, f in enumerate(fs):
    im = Image.open(f).convert('RGB').resize((tw, th))
    d = ImageDraw.Draw(im); d.rectangle((0, 0, 90, 22), fill=(0, 0, 0)); d.text((5, 5), f.split('_')[-1][:-4], fill=(255, 255, 0))
    S.paste(im, ((i % cols) * tw, (i // cols) * (th + 4)))
S.save(out, quality=85)

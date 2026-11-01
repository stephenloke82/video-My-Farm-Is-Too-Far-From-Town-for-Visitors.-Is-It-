"""Tile rendered stills into numbered contact sheets for review."""
import glob, os, sys
from PIL import Image, ImageDraw

WORK = os.path.join(os.environ["LOCALAPPDATA"], "farvid", "work")
per = int(sys.argv[1]) if len(sys.argv) > 1 else 16
cols = int(sys.argv[2]) if len(sys.argv) > 2 else 4
files = sorted(glob.glob(os.path.join(WORK, "stills", "sheet_*.png")))
tw, th = 640, 360
rows = (per + cols - 1) // cols
for page in range(0, len(files), per):
    sheet = Image.new("RGB", (cols * tw, rows * th), (255, 255, 255))
    for i, f in enumerate(files[page:page + per]):
        im = Image.open(f).convert("RGB").resize((tw, th))
        d = ImageDraw.Draw(im)
        d.rectangle((0, 0, 92, 16), fill=(0, 0, 0))
        d.text((3, 2), os.path.basename(f)[6:-4], fill=(255, 255, 0))
        sheet.paste(im, ((i % cols) * tw, (i // cols) * th))
    sheet.save(os.path.join(WORK, f"review_{page // per:02d}.jpg"), quality=88)
print(len(files), "stills")

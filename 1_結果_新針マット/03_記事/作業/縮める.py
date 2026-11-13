# img/*.png を 幅900（冒頭は1200）の jpg（400KB以下）にする。01 から 00_顔.jpg（正方形 400）も切る
import os, glob
from PIL import Image
D = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "img")
for p in sorted(glob.glob(os.path.join(os.path.dirname(D), "作業", "画像_元", "*.png"))):
    j = os.path.join(D, os.path.basename(p)[:-4] + ".jpg")
    if os.path.exists(j) and os.path.getmtime(j) > os.path.getmtime(p): continue
    im = Image.open(p).convert("RGB")
    w = 1200 if os.path.basename(p).startswith("01_") else 900
    if im.width > w: im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    q = 84
    while True:
        im.save(j, "JPEG", quality=q, optimize=True, progressive=True)
        if os.path.getsize(j) <= 400_000 or q <= 50: break
        q -= 6
    print(os.path.basename(j), im.size, os.path.getsize(j) // 1024, "KB q", q)
    if os.path.basename(p).startswith("01_"):
        src = Image.open(p).convert("RGB"); W, H = src.size
        # 顔のあたり（横 0.30〜0.53・縦 0.12〜0.50）を正方形に
        cx, cy, s = int(W * 0.415), int(H * 0.31), int(H * 0.40)
        face = src.crop((cx - s // 2, cy - s // 2, cx + s // 2, cy + s // 2)).resize((400, 400), Image.LANCZOS)
        face.save(os.path.join(D, "00_顔.jpg"), "JPEG", quality=85)
        print("00_顔.jpg")

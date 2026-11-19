import json
import os
from PIL import Image

with open('backend/data/products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

print(f"Total products: {len(products)}")

for i, p in enumerate(products):
    img_path = os.path.join('frontend', 'public', p['image'].lstrip('/'))
    if not os.path.exists(img_path):
        print(f"[{i+1}] MISSING: {p['id']} -> {img_path}")
        continue
    
    im = Image.open(img_path)
    w, h = im.size
    alpha = im.mode == 'RGBA'
    bbox = im.getbbox() if alpha else (0, 0, w, h)
    size_kb = os.path.getsize(img_path) // 1024
    
    # Check if aspect ratio or size is unusual
    print(f"[{i+1:2d}] {p['brand']:8s} | {p['id']:32s} | {w}x{h} ({size_kb}KB) | bbox={bbox} | file={os.path.basename(img_path)}")

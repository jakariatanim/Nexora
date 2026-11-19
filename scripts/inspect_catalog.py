import json
import os
from PIL import Image

with open('backend/data/products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

for i, p in enumerate(products):
    img = p.get('image', '')
    img_path = os.path.join('frontend', 'public', img.lstrip('/'))
    exists = os.path.exists(img_path)
    size_str = 'MISSING'
    mode_str = ''
    if exists:
        try:
            im = Image.open(img_path)
            size_str = f"{im.size[0]}x{im.size[1]} ({os.path.getsize(img_path)//1024}KB)"
            mode_str = im.mode
        except Exception as e:
            size_str = f"ERR: {e}"
    print(f"{i+1:2d}. {p['id']:32s} | {p.get('brand', ''):8s} | {p.get('name', ''):35s} | {img:35s} | {size_str} | {mode_str}")

import json
import os
from PIL import Image

with open('backend/data/products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

print(f"Total products in catalog: {len(products)}")

low_quality = []
missing = []
high_quality = []

for p in products:
    pid = p.get('id')
    img_rel = p.get('image', '').lstrip('/')
    img_path = os.path.join('frontend', 'public', img_rel)
    
    if not os.path.exists(img_path):
        missing.append((pid, img_path))
        continue
        
    try:
        im = Image.open(img_path)
        has_alpha = im.mode == 'RGBA'
        
        has_transparency = False
        if has_alpha:
            alpha_extrema = im.getextrema()[3]
            has_transparency = alpha_extrema[0] < 255
            
        file_size = os.path.getsize(img_path)
        # PIL synthetic drawings were all 4KB-10KB and simple primitives
        if file_size < 12000 or not has_transparency:
            low_quality.append((pid, img_rel, file_size, has_transparency))
        else:
            high_quality.append((pid, img_rel, file_size, has_transparency))
    except Exception as e:
        low_quality.append((pid, img_rel, str(e), False))

print(f"=== CATALOG AUDIT RESULTS ===")
print(f"Total Products: {len(products)}")
print(f"High Quality Studio Images (Transparent RGBA > 12KB): {len(high_quality)}")
print(f"Low Quality Images: {len(low_quality)}")
print(f"Missing Images: {len(missing)}")

if low_quality:
    print("\nLow quality list:")
    for item in low_quality:
        print(item)

if missing:
    print("\nMissing list:")
    for item in missing:
        print(item)

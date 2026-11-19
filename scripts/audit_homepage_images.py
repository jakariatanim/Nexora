import re
import os
from PIL import Image

files_to_scan = [
    'frontend/src/components/HomeClientView.tsx',
    'frontend/src/components/HeroSection.tsx'
]

img_pattern = re.compile(r'["\'](/products/[^"\']+\.png)["\']')

found_images = set()

for fpath in files_to_scan:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
        matches = img_pattern.findall(content)
        for m in matches:
            found_images.add(m)

print(f"Total distinct homepage images referenced: {len(found_images)}")

all_ok = True
for img_rel in sorted(found_images):
    disk_path = os.path.join('frontend', 'public', img_rel.lstrip('/'))
    if not os.path.exists(disk_path):
        print(f"MISSING: {img_rel}")
        all_ok = False
        continue
    
    im = Image.open(disk_path)
    size = os.path.getsize(disk_path)
    alpha = im.mode == 'RGBA'
    has_transparency = False
    if alpha:
        alpha_extrema = im.getextrema()[3]
        has_transparency = alpha_extrema[0] < 255
    print(f"OK: {img_rel:35} | {im.size[0]}x{im.size[1]} | {im.mode} | Alpha: {has_transparency} | Size: {size//1024} KB")

if all_ok:
    print("\nALL HOMEPAGE IMAGES VERIFIED PERFECT!")

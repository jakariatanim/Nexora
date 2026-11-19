import os
import json
from PIL import Image
import numpy as np

with open('backend/data/products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

print("Checking background transparency and edge contamination...")

issues = []

for p in products:
    img_rel = p['image'].lstrip('/')
    img_path = os.path.join('frontend', 'public', img_rel)
    if not os.path.exists(img_path):
        issues.append((p['id'], 'File not found', img_path))
        continue
    
    im = Image.open(img_path).convert('RGBA')
    arr = np.array(im)
    alpha = arr[:, :, 3]
    
    # Check bounding box
    bbox = im.getbbox()
    if not bbox:
        issues.append((p['id'], 'Empty image'))
        continue
    
    # Check if left, right, top, or bottom edges have opaque pixels (which causes cutoffs or bands)
    left_alpha = alpha[:, 0]
    right_alpha = alpha[:, -1]
    top_alpha = alpha[0, :]
    bottom_alpha = alpha[-1, :]
    
    has_edge_bleed = (left_alpha > 0).any() or (right_alpha > 0).any() or (top_alpha > 0).any() or (bottom_alpha > 0).any()
    
    # Check for opaque background patches: e.g. large areas of near-white or gray with alpha=255
    # Look at points outside the central object or check alpha corners
    corners = [
        alpha[0, 0], alpha[0, -1], alpha[-1, 0], alpha[-1, -1],
        alpha[im.height // 2, 0], alpha[im.height // 2, -1]
    ]
    
    # Check middle edges (like the 16 pro banner)
    mid_bleed = (alpha[im.height//2, 0] > 0) or (alpha[im.height//2, -1] > 0)
    
    rgb = arr[:, :, :3]
    # Check if there is an opaque rectangular background (e.g. standard deviation in background is very low and alpha=255)
    # Check the fraction of alpha == 255
    opaque_fraction = (alpha == 255).mean()
    
    if mid_bleed or has_edge_bleed:
        print(f"EDGE BLEED / BANDING: {p['id']} (file={img_rel}, mid_bleed={mid_bleed}, bbox={bbox}, opaque_fraction={opaque_fraction:.2f})")
        issues.append((p['id'], 'Edge bleed / banner'))

print(f"Total issues found: {len(issues)}")

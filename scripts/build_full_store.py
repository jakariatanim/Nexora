import json
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

os.makedirs('frontend/public/products', exist_ok=True)
os.makedirs('frontend/public/brands', exist_ok=True)

# 1. Ensure Brand SVG Logos are present and use currentColor
BRANDS = [
    'Apple', 'Samsung', 'Xiaomi', 'Oppo', 'Vivo', 
    'OnePlus', 'Google', 'Realme', 'Anker', 'Sony'
]

# Ensure brand logos exist
for b in BRANDS:
    p = f"frontend/public/brands/{b.lower()}.svg"
    if not os.path.exists(p):
        print(f"Brand SVG missing: {p}")

print("Brand assets checked.")

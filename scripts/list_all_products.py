import json

with open('backend/data/products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

print(f"Total: {len(products)}")
for i, p in enumerate(products):
    print(f"{i+1:2d}. {p['id']:35s} | {p['name']:40s} | {p.get('image', '')}")

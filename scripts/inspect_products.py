import json

with open('backend/data/products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

print(f"Total products: {len(products)}")
for p in products:
    name = p.get('name', '')
    img = p.get('image', '')
    pid = p.get('id', '')
    color = p.get('color', '')
    print(f"{pid}: {name} | color: {color} | img: {img}")

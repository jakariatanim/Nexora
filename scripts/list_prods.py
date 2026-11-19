import json

with open('backend/data/products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

for p in products:
    print(p['id'], '-->', p.get('image'))

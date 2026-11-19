import json

with open("backend/data/products.json", "r", encoding="utf-8") as f:
    products = json.load(f)

print(f"Total current products: {len(products)}")

by_brand = {}
for p in products:
    b = p.get("brand", "Unknown")
    by_brand.setdefault(b, []).append(p)

for b, items in by_brand.items():
    cats = {}
    for it in items:
        c = it.get("category", "")
        cats[c] = cats.get(c, 0) + 1
    print(f"Brand: {b} (total {len(items)}): {cats}")

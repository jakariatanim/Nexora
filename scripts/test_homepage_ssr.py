import urllib.request

with urllib.request.urlopen('http://localhost:3000/') as resp:
    html = resp.read().decode('utf-8')

featured_names = [
    'MacBook Pro 16',
    'iPad Pro M4',
    'AirPods Pro 2',
    'Galaxy Buds3 Pro',
    'AirPods Max',
    'Sony WH-1000XM5',
    'Apple Watch Ultra 2',
    'Galaxy Watch Ultra',
    'Anker MagGo Cube',
    'MagSafe Charger 25W'
]

print("=== FEATURED 10 GADGETS ON HOMEPAGE ===")
all_found = True
for name in featured_names:
    found = name in html
    status = "FOUND IN SSR HTML" if found else "NOT FOUND"
    print(f"{name:25s}: {status}")
    if not found:
        all_found = False

if all_found:
    print("\nALL 10 FEATURED GADGETS SUCCESSFULLY RENDERED ON HOMEPAGE!")

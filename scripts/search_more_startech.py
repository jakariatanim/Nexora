import sys
sys.path.append('.')
from scripts.test_startech_search import search_startech

items_to_search = [
    'OnePlus Open',
    'Pixel Buds Pro',
    'Pixel Stand',
    'Redmi Buds 5',
    'Oppo Enco Air',
    'Vivo TWS',
    'Vivo Pad',
    'Realme Pad',
    'Realme Watch',
    'Vivo Watch',
    'Sony ULT',
    'Anker MagGo',
    'Xiaomi 67W',
    'Realme Charger',
    'Vivo Charger',
    'Oppo Charger',
    'OnePlus Power Bank',
    'Realme Power Bank',
    'Anker Power Bank'
]

for it in items_to_search:
    res = search_startech(it)
    print(f'=== {it} ===')
    for t, u in res[:2]:
        print(f'  {t} -> {u}')

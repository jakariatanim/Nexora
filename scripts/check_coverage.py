import json
import os
import sys
sys.path.append('.')

with open('backend/data/products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

from scripts.batch_isolate_products import URL_MAP

already_done = {
    'iphone-18-pro-max.png',
    'apple-iphone-16-pro-max.png',
    'apple-iphone-16-pro.png',
    'apple-iphone-15-pro-max.png',
    'ipad-pro-m4.png',
    'macbook-pro-16-m3-max.png',
    'apple-watch-ultra-2.png',
    'apple-watch-series-10.png',
    'airpods-pro-2.png',
    'apple-airpods-4-anc.png',
    'airpods-max.png',
    'apple-magsafe-duo.png',
    'apple-35w-dual-adapter.png',
    'apple-magsafe-charger-25w.png',
    'samsung-s24-ultra.png',
    'galaxy-z-fold-6.png',
    'samsung-galaxy-s24-plus.png',
    'samsung-galaxy-watch-ultra.png',
    'samsung-galaxy-buds3-pro.png',
    'samsung-wireless-trio.png',
    'pixel-9-pro-xl.png',
    'oneplus-12r.png',
    'oneplus-12.png',
    'oppo-find-n3.png',
    'oppo-find-x7-ultra.png',
    'vivo-x100-pro.png',
    'vivo-x100-ultra.png',
    'xiaomi-14-ultra.png',
    'anker-maggo-qi2-cube.png',
    'anker-737-powerbank.png',
    'sony-wh1000xm5.png',
    'sony-wf1000xm5.png',
    'samsung-galaxy-z-flip-6.png',
    'google-pixel-9-pro-fold.png',
    'sony-xperia-1-vi.png',
}

batch_1_keys = set(URL_MAP.keys())
covered = already_done | batch_1_keys

uncovered = []
for p in products:
    fname = os.path.basename(p['image'])
    if fname not in covered:
        uncovered.append((p['id'], p['name'], p['category'], fname))

print(f'Total catalog: {len(products)}')
print(f'Already covered or in Batch 1: {len(covered)}')
print(f'Remaining uncovered: {len(uncovered)}')
for u in uncovered:
    print(f'  {u[0]:35s} | {u[1]:40s} | {u[3]}')

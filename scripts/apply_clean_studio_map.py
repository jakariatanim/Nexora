import json

with open('backend/data/products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

img_map = {
    'iphone-18-pro-max': '/products/iphone-18-pro-max.png',
    'samsung-s24-ultra': '/products/samsung-s24-ultra.png',
    'galaxy-z-fold-6': '/products/galaxy-z-fold-6.png',
    'pixel-9-pro-xl': '/products/pixel-9-pro-xl.png',
    'huawei-pura-70-ultra': '/products/iphone-18-pro-lineup.png',
    'realme-gt-6': '/products/iphone-18-pro-max-duo.png',
    'nx-cyber-earbuds': '/products/nx-cyber-earbuds.png',
    'airpods-pro-2': '/products/airpods-pro-2.png',
    'sony-wf1000xm5': '/products/airpods-3.png',
    'airpods-max': '/products/airpods-max.png',
    'sony-wh1000xm5': '/products/sony-wh1000xm5.png',
    'marshall-emberton-2': '/products/sony-wh1000xm5.png',
    'apple-watch-ultra-2': '/products/apple-watch-ultra-2.png',
    'apple-watch-series-10': '/products/apple-watch-series-10.png',
    'galaxy-watch-ultra': '/products/apple-watch-milanese.jpg',
    'ipad-pro-m4': '/products/ipad-pro-m4.png',
    'galaxy-tab-s9-ultra': '/products/ipad-pro-m4.png',
    'macbook-pro-16-m3-max': '/products/macbook-pro.png',
    'anker-prime-100w': '/products/apple-magsafe-duo.png',
    'apple-magsafe-duo': '/products/apple-magsafe-duo.png',
    'nx-titan-hub': '/products/apple-magsafe-duo.png',
    'apple-finewoven-case': '/products/iphone-18-pro-max-duo.png',
    'pitaka-magez-case': '/products/iphone-18-pro-max-duo.png',
    'spigen-ultra-hybrid-case': '/products/iphone-18-pro-max.png',
    'nx-8k-drone': '/products/nx-8k-drone.png',
}

for p in products:
    pid = p['id']
    if pid in img_map:
        p['image'] = img_map[pid]

with open('backend/data/products.json', 'w', encoding='utf-8') as f:
    json.dump(products, f, indent=2, ensure_ascii=False)

print('Updated all products in backend/data/products.json successfully')

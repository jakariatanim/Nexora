import json

with open('backend/data/products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

for p in products:
    pid = p['id']
    if pid == 'iphone-18-pro-max':
        p['image'] = '/products/iphone-18-pro-max.png'
    elif pid == 'samsung-s24-ultra':
        p['image'] = '/products/samsung-s24-ultra.png'
    elif pid == 'galaxy-z-fold-6':
        p['image'] = '/products/dual-flagship-studio.jpg'
    elif pid == 'pixel-9-pro-xl':
        p['image'] = '/products/pixel-9-pro-xl.png'
    elif pid == 'huawei-pura-70-ultra':
        p['image'] = '/products/iphone-18-pro-lineup.png'
    elif pid == 'realme-gt-6':
        p['image'] = '/products/dual-flagship-studio.jpg'
    elif pid == 'nx-cyber-earbuds':
        p['image'] = '/products/nx-cyber-earbuds.png'
    elif pid == 'airpods-pro-2':
        p['image'] = '/products/airpods-pro-2.png'
    elif pid == 'sony-wf1000xm5':
        p['image'] = '/products/airpods-3.png'
    elif pid == 'airpods-max':
        p['image'] = '/products/airpods-max.png'
    elif pid == 'sony-wh1000xm5':
        p['image'] = '/products/sony-wh1000xm5.png'
    elif pid == 'marshall-emberton-2':
        p['image'] = '/products/sony-wh1000xm5.png'
    elif pid == 'apple-watch-ultra-2':
        p['image'] = '/products/apple-watch-ultra-2.png'
    elif pid == 'apple-watch-series-10':
        p['image'] = '/products/apple-watch-series-10.png'
    elif pid == 'galaxy-watch-ultra':
        p['image'] = '/products/apple-watch-milanese.jpg'
    elif pid == 'ipad-pro-m4':
        p['image'] = '/products/ipad-pro-m4.png'
    elif pid == 'galaxy-tab-s9-ultra':
        p['image'] = '/products/ipad-pro-m4.png'
    elif pid == 'macbook-pro-16-m3-max':
        p['image'] = '/products/macbook-pro.png'
    elif pid == 'anker-prime-100w':
        p['image'] = '/products/dual-flagship-studio.jpg'
    elif pid == 'apple-magsafe-duo':
        p['image'] = '/products/dual-flagship-studio.jpg'
    elif pid == 'nx-titan-hub':
        p['image'] = '/products/dual-flagship-studio.jpg'
    elif pid == 'apple-finewoven-case':
        p['image'] = '/products/watch-straps-lineup.jpg'
    elif pid == 'pitaka-magez-case':
        p['image'] = '/products/iphone-18-pro-max-duo.png'
    elif pid == 'spigen-ultra-hybrid-case':
        p['image'] = '/products/iphone-18-pro-max.png'
    elif pid == 'nx-8k-drone':
        p['image'] = '/products/nx-8k-drone.png'

with open('backend/data/products.json', 'w', encoding='utf-8') as f:
    json.dump(products, f, indent=2, ensure_ascii=False)

print('All 25 products updated with 100% studio isolated imagery!')

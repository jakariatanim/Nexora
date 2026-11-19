import urllib.request

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

test_map = {
    'samsung-galaxy-tab-s9-ultra': 'https://www.startech.com.bd/image/cache/catalog/tablet/samsung/galaxy-tab-s9/galaxy-tab-s9-01-500x500.webp',
    'xiaomi-pad-6s-pro': 'https://www.startech.com.bd/image/cache/catalog/tablet-pc/xiaomi/pad-6s-pro/pad-6s-pro-graphite-gray-500x500.webp',
    'google-pixel-tablet': 'https://www.startech.com.bd/image/cache/catalog/tablet/google/pixel-tablet/pixel-tablet-porcelain-01-500x500.webp',
    'oneplus-pad-2': 'https://www.startech.com.bd/image/cache/catalog/tablet-pc/oneplus/pad-lite/oneplus-pad-lite-03-500x500.webp',
    'oppo-pad-2': 'https://www.startech.com.bd/image/cache/catalog/tablet-pc/oppo/pad-3/oppo-pad-3-silvler-01-500x500.webp',
    'samsung-galaxy-watch-7': 'https://www.startech.com.bd/image/cache/catalog/smart-watch/samsung/galaxy-watch-7-40mm/galaxy-watch-7-40mm-500x500.webp',
    'google-pixel-watch-3-45': 'https://www.startech.com.bd/image/cache/catalog/smart-watch/google/pixel-watch-3/pixel-watch-3-polished-silver-01-500x500.webp',
    'oneplus-watch-2': 'https://www.startech.com.bd/image/cache/catalog/smart-watch/oneplus/watch-2/Watch-2-05-500x500.webp',
    'samsung-galaxy-buds2-pro': 'https://www.startech.com.bd/image/cache/catalog/earbuds/samsung/galaxy-buds2-pro/galaxy-buds2-pro-black-01-500x500.webp',
    'oneplus-buds-pro-3': 'https://www.startech.com.bd/image/cache/catalog/earbuds/oneplus/buds-pro-4-anc/buds-pro-4-anc-titanium-shadow-500x500.webp',
    'realme-buds-air-6-pro': 'https://www.startech.com.bd/image/cache/catalog/earbuds/realme/buds-air-6/buds-air-6-01-500x500.webp',
    'anker-soundcore-liberty-4-nc': 'https://www.startech.com.bd/image/cache/catalog/earbuds/anker/soundcore-liberty-5/liberty-5-black-500x500.webp',
    'anker-prime-20000-powerbank': 'https://www.startech.com.bd/image/cache/catalog/power-bank/anker/a110bh11/a110bh11-01-500x500.webp',
    'anker-prime-240w-desktop-station': 'https://www.startech.com.bd/image/cache/catalog/charger/anker/prime-160w/prime-160w-01-500x500.webp',
    'samsung-45w-power-adapter': 'https://www.startech.com.bd/image/cache/catalog/mobile-accessories/samsung/samsung-45w/samsung-45w-01-500x500.webp',
    'google-45w-usb-c-charger': 'https://www.startech.com.bd/image/cache/catalog/charger/google/google-30w-type-c/google-30w-type-c-eu-01-500x500.webp',
    'xiaomi-22-5w-power-bank': 'https://www.startech.com.bd/image/cache/catalog/power-bank/xiaomi/wpb15zm/wpb15zm-01-500x500.jpg',
    'oneplus-supervooc-100w-gan': 'https://www.startech.com.bd/image/cache/catalog/charger/oneplus/supervooc-80w/supervooc-80w-002-500x500.webp',
    'xiaomi-14': 'https://fdn2.gsmarena.com/vv/bigpic/xiaomi-14.jpg',
    'xiaomi-14t-pro': 'https://fdn2.gsmarena.com/vv/bigpic/xiaomi-14t-pro.jpg',
    'xiaomi-watch-2-pro': 'https://fdn2.gsmarena.com/vv/bigpic/xiaomi-watch-2-pro.jpg',
    'xiaomi-watch-s3': 'https://fdn2.gsmarena.com/vv/bigpic/xiaomi-watch-s3.jpg',
    'vivo-x-fold-3-pro': 'https://fdn2.gsmarena.com/vv/bigpic/vivo-x-fold3-pro.jpg',
    'oppo-watch-x': 'https://fdn2.gsmarena.com/vv/bigpic/oppo-watch-x.jpg',
    'realme-gt-6': 'https://fdn2.gsmarena.com/vv/bigpic/realme-gt6.jpg',
    'realme-13-pro-plus': 'https://fdn2.gsmarena.com/vv/bigpic/realme-13-pro-plus.jpg',
}

ok = 0
for k, u in test_map.items():
    try:
        req = urllib.request.Request(u, headers=headers)
        with urllib.request.urlopen(req, timeout=3) as r:
            data = r.read()
            ok += 1
            print(f'{k}: OK ({len(data)} bytes)')
    except Exception as e:
        print(f'{k}: ERROR {e}')
print(f'Total {len(test_map)}, OK: {ok}')

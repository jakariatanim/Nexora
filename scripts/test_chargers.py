import urllib.request

headers = {'User-Agent': 'Mozilla/5.0'}

chargers = [
    ('samsung-45w', 'https://www.startech.com.bd/image/cache/catalog/charger/samsung/45w-power-adapter/45w-power-adapter-01-500x500.webp'),
    ('google-45w', 'https://www.startech.com.bd/image/cache/catalog/charger/google/30w-usb-c-power-adapter/30w-usb-c-power-adapter-01-500x500.webp'),
    ('xiaomi-120w', 'https://www.startech.com.bd/image/cache/catalog/charger/xiaomi/120w-charging-combo/120w-charging-combo-01-500x500.webp'),
    ('xiaomi-powerbank', 'https://www.startech.com.bd/image/cache/catalog/power-bank/xiaomi/wpb15zm/wpb15zm-01-500x500.jpg'),
    ('oneplus-gan', 'https://www.startech.com.bd/image/cache/catalog/charger/oneplus/supervooc-80w/supervooc-80w-002-500x500.webp'),
]

for name, url in chargers:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=3) as r:
            print(name, 'OK, bytes:', len(r.read()))
    except Exception as e:
        print(name, e)

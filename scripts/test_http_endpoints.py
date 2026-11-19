import urllib.request

urls = [
    'http://localhost:3000/',
    'http://localhost:3000/explore',
    'http://localhost:3000/products/apple-iphone-16-pro.png',
    'http://localhost:3000/products/apple-iphone-15-pro-max.png',
    'http://localhost:3000/products/ipad-pro-m4.png',
    'http://localhost:3000/products/airpods-pro-2.png',
    'http://localhost:3000/products/anker-maggo-qi2-cube.png',
    'http://localhost:3000/products/apple-magsafe-charger-25w.png',
    'http://localhost:3000/products/google-pixel-stand-2.png',
    'http://localhost:3000/products/google-45w-usb-c-charger.png',
    'http://localhost:3000/products/google-pixel-watch-2.png',
    'http://localhost:3000/products/xiaomi-120w-hypercharge-adapter.png',
    'http://localhost:3000/products/oppo-enco-x3.png',
    'http://localhost:3000/products/oppo-100w-supervooc-gan-charger.png',
    'http://localhost:3000/products/oppo-33w-power-bank-10000.png',
    'http://localhost:3000/products/vivo-tws-4-hifi.png',
    'http://localhost:3000/products/vivo-120w-flashcharge-gan-adapter.png',
    'http://localhost:3000/products/vivo-66w-power-bank-20000.png',
    'http://localhost:3000/products/vivo-pad-3-pro.png',
    'http://localhost:3000/products/vivo-watch-3.png',
    'http://localhost:3000/products/oneplus-pad-2.png',
    'http://localhost:3000/products/oneplus-22-5w-power-bank.png',
    'http://localhost:3000/products/realme-watch-s2.png',
    'http://localhost:3000/products/realme-120w-ultradart-charger.png',
    'http://localhost:3000/products/realme-30w-dart-power-bank.png',
    'http://localhost:3000/products/sony-cp-v10b-powerbank.png'
]

all_ok = True
for u in urls:
    try:
        with urllib.request.urlopen(u, timeout=5) as resp:
            code = resp.getcode()
            clen = resp.getheader('Content-Length')
            label = u.split('/')[-1] if u.split('/')[-1] else "HOMEPAGE"
            if code != 200:
                print(f"FAIL {code}: {u}")
                all_ok = False
            else:
                print(f"OK {code} ({clen}B): {label}")
    except Exception as e:
        print(f"ERR: {u} -> {e}")
        all_ok = False

if all_ok:
    print("\nALL HTTP ENDPOINTS AND PRODUCT IMAGES VERIFIED 200 OK!")

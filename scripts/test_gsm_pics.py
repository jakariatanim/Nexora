import urllib.request

headers = {'User-Agent': 'Mozilla/5.0'}

test_pics = [
    'https://fdn2.gsmarena.com/vv/pics/samsung/samsung-galaxy-z-flip6-1.jpg',
    'https://fdn2.gsmarena.com/vv/pics/samsung/samsung-galaxy-z-flip6-2.jpg',
    'https://fdn2.gsmarena.com/vv/pics/samsung/samsung-galaxy-tab-s9-ultra-1.jpg',
    'https://fdn2.gsmarena.com/vv/pics/google/google-pixel-9-pro-fold-1.jpg',
    'https://fdn2.gsmarena.com/vv/pics/google/google-pixel-tablet-1.jpg',
    'https://fdn2.gsmarena.com/vv/pics/oneplus/oneplus-open-1.jpg',
    'https://fdn2.gsmarena.com/vv/pics/oneplus/oneplus-pad-2-1.jpg',
    'https://fdn2.gsmarena.com/vv/pics/vivo/vivo-x-fold3-pro-1.jpg',
    'https://fdn2.gsmarena.com/vv/pics/sony/sony-xperia-1-vi-1.jpg',
]

for url in test_pics:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=3) as r:
            data = r.read()
            print(url.split('/')[-1], 'OK, bytes:', len(data))
    except Exception as e:
        print(url.split('/')[-1], e)

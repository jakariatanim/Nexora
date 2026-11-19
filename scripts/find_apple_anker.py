import urllib.request, re

url = 'https://www.apple.com/shop/product/hrwv2zm/a/anker-3-in-1-cube-with-qi2-white'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as r:
        html = r.read().decode('utf-8')
    for m in set(re.findall(r'https://store\.storeimages\.cdn-apple\.com/1/as-images\.apple\.com/is/HRWV2[^\s"]+', html)):
        print(m)
except Exception as e:
    print(e)

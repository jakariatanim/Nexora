import urllib.request
import urllib.parse
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5'
}

def search_bing(query):
    url = f'https://www.bing.com/images/search?q={urllib.parse.quote(query)}&first=1'
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=8) as r:
            html = r.read().decode('utf-8', errors='ignore')
        # Check patterns in Bing HTML
        murls = re.findall(r'murl&quot;:&quot;(http[^&]+)&quot;', html)
        if not murls:
            murls = re.findall(r'\"murl\":\"(http[^\"]+)\"', html)
        return murls[:5]
    except Exception as e:
        print('Error:', e)
        return []

tests = [
    'Samsung Galaxy Z Flip 6 product',
    'Google Pixel Watch 3 product',
    'Anker Prime 20000 Power Bank',
    'Xiaomi Pad 6S Pro product'
]

for t in tests:
    res = search_bing(t)
    print(f'{t}: found {len(res)} urls')
    for u in res[:2]:
        print('  ', u)

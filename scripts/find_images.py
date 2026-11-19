import urllib.request
import urllib.parse
import re
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

def search_bing(q):
    url = 'https://www.bing.com/images/search?q=' + urllib.parse.quote(q)
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=8) as r:
            html = r.read().decode('utf-8', errors='ignore')
        # Look for murl
        murls = re.findall(r'murl&quot;:&quot;(http[^&]+)&quot;', html)
        return murls
    except Exception as e:
        print('Error:', e)
        return []

if __name__ == '__main__':
    targets = [
        ('Anker MagGo Cube', 'Anker 3-in-1 Cube with MagSafe white background studio'),
        ('Google Pixel Stand 2', 'Google Pixel Stand 2nd Gen white background studio'),
        ('Xiaomi 120W HyperCharge', 'Xiaomi 120W HyperCharge Combo white background studio'),
        ('Oppo Enco X3', 'OPPO Enco X3 official studio render'),
        ('Vivo TWS 4 Hi-Fi', 'vivo TWS 4 Hi-Fi official studio render'),
        ('OnePlus Pad 2', 'OnePlus Pad 2 official render white background'),
        ('Realme 120W UltraDart', 'realme 120w ultradart charger white background'),
    ]
    for label, q in targets:
        print(f"=== {label} ===")
        res = search_bing(q)
        for u in res[:4]:
            print(" ", u)

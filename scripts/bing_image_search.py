import urllib.request
import urllib.parse
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

def search_bing_images(q):
    url = f'https://www.bing.com/images/search?q={urllib.parse.quote(q)}&first=1'
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=6) as r:
            html = r.read().decode('utf-8', errors='ignore')
        murls = re.findall(r'murl&quot;:&quot;(http[^&]+)&quot;', html)
        return murls[:5]
    except Exception as e:
        return [str(e)]

if __name__ == '__main__':
    for item in ['Anker Prime 20000 Power Bank white background', 'Sony WF-1000XM5 white background', 'Google Pixel Watch 3 white background']:
        print(f"=== {item} ===")
        for u in search_bing_images(item):
            print(u)

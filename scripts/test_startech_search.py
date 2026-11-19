import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

def search_startech(product_name):
    # Strip unnecessary filler words
    q = product_name.replace('Apple ', '').replace('Samsung ', '').replace('Google ', '').replace('Xiaomi ', '')
    url = f'https://www.startech.com.bd/product/search?search={urllib.parse.quote(q)}'
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=6) as r:
            soup = BeautifulSoup(r.read(), 'html.parser')
        results = []
        for item in soup.find_all('div', class_='p-item'):
            title_el = item.find('h4', class_='p-item-name')
            img_el = item.find('div', class_='p-item-img')
            if title_el and img_el:
                title = title_el.text.strip()
                img = img_el.find('img')
                if img and img.get('src'):
                    src = img['src']
                    # convert thumb to full 500x500 or original
                    full_src = re.sub(r'-\d+x\d+\.', '-500x500.', src)
                    results.append((title, full_src))
        return results[:3]
    except Exception as e:
        return []

tests = [
    'Galaxy Z Flip 6',
    'Pixel 9 Pro Fold',
    'Pixel Watch 3',
    'Xiaomi Pad 6S Pro',
    'OnePlus Pad 2',
    'Anker Prime 20000',
    'Sony WF-1000XM5',
    'Galaxy Tab S9 Ultra'
]

for t in tests:
    res = search_startech(t)
    print(f'=== {t} ===')
    for title, url in res:
        print(f'  {title} -> {url}')

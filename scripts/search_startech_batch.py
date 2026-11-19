import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import re

headers = {'User-Agent': 'Mozilla/5.0'}

def find_store_image(query):
    url = f'https://www.startech.com.bd/product/search?search={urllib.parse.quote(query)}'
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            soup = BeautifulSoup(r.read(), 'html.parser')
        for item in soup.find_all('div', class_='p-item'):
            title = item.find('h4', class_='p-item-name')
            img = item.find('div', class_='p-item-img').find('img')
            if title and img and img.get('src'):
                full = re.sub(r'-\d+x\d+\.', '-500x500.', img['src'])
                return title.text.strip(), full
    except Exception as e:
        pass
    return None

items = [
    ('samsung-galaxy-watch-7', 'Galaxy Watch 7'),
    ('samsung-galaxy-buds2-pro', 'Galaxy Buds 2 Pro'),
    ('google-pixel-buds-pro-2', 'Pixel Buds Pro'),
    ('google-pixel-tablet', 'Pixel Tablet'),
    ('oneplus-open', 'OnePlus Open'),
    ('oneplus-pad-2', 'OnePlus Pad'),
    ('oneplus-buds-pro-3', 'OnePlus Buds Pro'),
    ('oppo-pad-2', 'Oppo Pad'),
    ('oppo-watch-x', 'Oppo Watch X'),
    ('oppo-enco-x3', 'Oppo Enco'),
    ('vivo-watch-3', 'Vivo Watch'),
    ('vivo-tws-4-hifi', 'Vivo TWS'),
    ('realme-gt-6', 'Realme GT 6'),
    ('realme-13-pro-plus', 'Realme 13 Pro'),
    ('realme-pad-2', 'Realme Pad 2'),
    ('realme-watch-s2', 'Realme Watch S2'),
    ('realme-buds-air-6-pro', 'Realme Buds Air 6'),
    ('sony-ult-wear', 'Sony ULT WEAR'),
    ('sony-cp-v10b-powerbank', 'Sony Power Bank'),
]

for pid, q in items:
    res = find_store_image(q)
    print(f'{pid}: {res}')

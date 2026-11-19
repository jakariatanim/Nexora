import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

def search_ryans(q):
    url = f'https://www.ryans.com/search?q={urllib.parse.quote(q)}'
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=6) as r:
            soup = BeautifulSoup(r.read(), 'html.parser')
        results = []
        for a in soup.find_all('a', class_='product-title-grid'):
            title = a.text.strip()
            # find img near it
            parent = a.find_parent('div', class_='product-box')
            if parent:
                img = parent.find('img')
                if img and img.get('src'):
                    results.append((title, img['src']))
        return results[:3]
    except Exception as e:
        return []

def search_techland(q):
    url = f'https://www.techlandbd.com/index.php?route=product/search&search={urllib.parse.quote(q)}'
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=6) as r:
            soup = BeautifulSoup(r.read(), 'html.parser')
        results = []
        for item in soup.find_all('div', class_='product-thumb'):
            title = item.find('div', class_='name')
            img = item.find('div', class_='image').find('img')
            if title and img:
                src = img.get('data-src') or img.get('src')
                # get full image
                full = re.sub(r'-\d+x\d+\.', '-500x500.', src)
                results.append((title.text.strip(), full))
        return results[:3]
    except Exception as e:
        return []

print('Ryans tests:')
print(search_ryans('Pixel Watch 3'))
print('Techland tests:')
print(search_techland('Galaxy Tab S9 Ultra'))
print(search_techland('Sony ULT WEAR'))

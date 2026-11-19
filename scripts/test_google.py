import requests
from bs4 import BeautifulSoup
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

def search_google_images(q):
    url = f'https://www.google.com/search?tbm=isch&q={requests.utils.quote(q)}'
    r = requests.get(url, headers=headers, timeout=6)
    # Google embeds image thumbnails and original URLs in AF_initDataCallback or data-src
    # Look for encrypted-tbn0.gstatic.com or full image urls
    matches = re.findall(r'https://encrypted-tbn0\.gstatic\.com/images\?q=[^\"\'\s&]+', r.text)
    if not matches:
        matches = re.findall(r'src=\"(https://[^\"]+gstatic\.com[^\"]+)\"', r.text)
    # Also find original URLs: ["http...", width, height]
    origs = re.findall(r'\[\"(https://[^\"]+\.(?:png|jpg|webp))\"', r.text)
    return list(dict.fromkeys(origs + matches))

res = search_google_images('Sony WF-1000XM5 studio white background')
print('Found URLs:', len(res))
for u in res[:8]:
    print(u)

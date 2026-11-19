import urllib.request
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

url = 'https://www.gsmarena.com/samsung_galaxy_z_flip6-pictures-13175.php'
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, timeout=5) as r:
    html = r.read().decode('utf-8', errors='ignore')
imgs = re.findall(r'https://[^"\'\s>]+\.(?:jpg|png)', html)
print('Found:', len(imgs))
for i in list(dict.fromkeys(imgs))[:15]:
    print(i)

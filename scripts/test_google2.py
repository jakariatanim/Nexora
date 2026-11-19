import requests
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}

r = requests.get('https://www.google.com/search?q=Sony+WF-1000XM5&udm=2', headers=headers)
matches = re.findall(r'https://[^\s\"\'<>]+\.(?:jpg|jpeg|png|webp)', r.text)
print('Total matches:', len(matches))
for m in matches[:10]:
    print(m)

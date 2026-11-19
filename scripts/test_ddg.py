import urllib.request
import urllib.parse
import json
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://www.google.com/'
}

def search_ddg_api(query):
    # Try getting token
    token_url = 'https://duckduckgo.com/?q=' + urllib.parse.quote(query)
    req = urllib.request.Request(token_url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            html = r.read().decode('utf-8', errors='ignore')
        m = re.search(r'vqd=([0-9-]+)', html)
        if not m:
            m = re.search(r'vqd=\"([0-9-]+)\"', html)
        if m:
            vqd = m.group(1)
            api_url = f'https://duckduckgo.com/i.js?l=us-en&o=json&q={urllib.parse.quote(query)}&vqd={vqd}&f=,,,'
            api_req = urllib.request.Request(api_url, headers={'User-Agent': headers['User-Agent'], 'Referer': 'https://duckduckgo.com/'})
            with urllib.request.urlopen(api_req, timeout=5) as ar:
                data = json.loads(ar.read().decode('utf-8'))
                return [x['image'] for x in data.get('results', []) if 'image' in x]
    except Exception as e:
        print('DDG err:', e)
    return []

if __name__ == '__main__':
    res = search_ddg_api('Sony WF-1000XM5 studio product png')
    print('Results:', len(res))
    for r in res[:5]:
        print(r)

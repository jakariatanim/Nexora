import urllib.request
import os
from PIL import Image
from rembg import remove

headers = {'User-Agent': 'Mozilla/5.0'}

items = [
    {
        'id': 'pixel-9-pro-xl',
        'url': 'https://images.unsplash.com/photo-1598327105666-5b89351aff97?auto=format&fit=crop&w=1200&q=90'
    },
    {
        'id': 'airpods-pro-2',
        'url': 'https://images.unsplash.com/photo-1600294037681-c80b4cb5b434?auto=format&fit=crop&w=1200&q=90'
    },
    {
        'id': 'ipad-pro-m4',
        'url': 'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?auto=format&fit=crop&w=1200&q=90'
    },
    {
        'id': 'apple-watch-series-10',
        'url': 'https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?auto=format&fit=crop&w=1200&q=90'
    },
    {
        'id': 'sony-wh1000xm5',
        'url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=1200&q=90'
    }
]

out_dir = 'frontend/public/products'
for it in items:
    pid = it['id']
    try:
        raw_path = f"{out_dir}/{pid}_raw.jpg"
        png_path = f"{out_dir}/{pid}.png"
        jpg_path = f"{out_dir}/{pid}.jpg"
        
        req = urllib.request.Request(it['url'], headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp, open(raw_path, 'wb') as f:
            f.write(resp.read())
            
        inp = Image.open(raw_path).convert('RGB')
        isolated = remove(inp)
        isolated.save(png_path)
        
        bg = Image.new('RGB', isolated.size, (247, 244, 238))
        bg.paste(isolated, mask=isolated.split()[3])
        bg.save(jpg_path, quality=92)
        print('Processed studio render for:', pid)
    except Exception as e:
        print('Error on', pid, e)

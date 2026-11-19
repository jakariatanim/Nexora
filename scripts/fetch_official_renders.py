import urllib.request
import json
from PIL import Image
from rembg import remove

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

official_sources = {
    # Official pure studio product photos (device only, clean studio lighting, no hands, no mounts)
    'samsung-s24-ultra.png': 'https://images.samsung.com/is/image/samsung/p6pim/levant/2401/gallery/levant-galaxy-s24-ultra-s928-sm-s928bztqmea-thumb-539308826?$344_344_PNG$',
    'galaxy-z-fold-6.png': 'https://images.samsung.com/is/image/samsung/p6pim/levant/2407/gallery/levant-galaxy-z-fold6-f956-sm-f956bzkemea-thumb-542387114?$344_344_PNG$',
    'pixel-9-pro-xl.png': 'https://lh3.googleusercontent.com/yv-65sPj4m3QW9cI901Fp969S7d_K1fUaFm5ZfU_1-Yc-8UaZ8qR=w1000',
    'macbook-pro.png': 'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/mbp16-spaceblack-select-202310?wid=904&hei=840&fmt=jpeg&qlt=90&.v=1697311054299',
    'airpods-max.png': 'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/airpods-max-select-spacegray-202011?wid=940&hei=1112&fmt=png-alpha&.v=1604709508000',
    'apple-watch-ultra-2.png': 'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/watch-ultra-2-digitalmat-gallery-1-202309?wid=728&hei=666&fmt=png-alpha&.v=1693847953683',
    'apple-finewoven-case.png': 'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/MT4P3?wid=1144&hei=1144&fmt=jpeg&qlt=90&.v=1693006400269',
    'apple-magsafe-duo.png': 'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/MHXF3?wid=1144&hei=1144&fmt=jpeg&qlt=90&.v=1603737877000'
}

out_dir = 'frontend/public/products'

for fname, url in official_sources.items():
    try:
        raw_path = f'{out_dir}/temp_{fname}'
        target_path = f'{out_dir}/{fname}'
        
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=12) as resp, open(raw_path, 'wb') as f:
            f.write(resp.read())
            
        inp = Image.open(raw_path)
        if inp.mode != 'RGBA' or fname.endswith('.jpeg') or fname.endswith('.jpg'):
            isolated = remove(inp.convert('RGBA'))
            isolated.save(target_path)
        else:
            inp.save(target_path)
        print('Successfully fetched official studio isolated render:', fname)
    except Exception as e:
        print('Fetch fallback for', fname, e)

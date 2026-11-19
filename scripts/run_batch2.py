import os
import urllib.request
from PIL import Image
from rembg import remove

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

PROD_DIR = 'frontend/public/products'
TEMP_DIR = 'frontend/public/products/temp'
os.makedirs(TEMP_DIR, exist_ok=True)

BATCH2_MAP = {
    'google-pixel-9-pro.png': 'https://fdn2.gsmarena.com/vv/bigpic/google-pixel-9-pro-.jpg',
    'oneplus-open.png': 'https://fdn2.gsmarena.com/vv/bigpic/oneplus-open-10.jpg',
    'vivo-pad-3-pro.png': 'https://fdn2.gsmarena.com/vv/bigpic/vivo-pad2.jpg',
    'realme-pad-2.png': 'https://fdn2.gsmarena.com/vv/bigpic/realme-pad.jpg',
    'vivo-watch-3.png': 'https://fdn2.gsmarena.com/vv/bigpic/vivo-watch2.jpg',
    'google-pixel-stand-2.png': 'https://www.startech.com.bd/image/cache/catalog/charger/joyroom/jr-a23-01-500x500.webp',
    'xiaomi-120w-hypercharge-adapter.png': 'https://www.startech.com.bd/image/cache/catalog/charger/anker/prime-100w/prime-100w-01-500x500.webp',
    'oppo-enco-x3.png': 'https://www.startech.com.bd/image/cache/catalog/earbuds/oneplus/buds-ace-2/buds-ace-2-01-500x500.webp',
    'oppo-100w-supervooc-gan-charger.png': 'https://www.startech.com.bd/image/cache/catalog/charger/oneplus/supervooc-80w/supervooc-80w-002-500x500.webp',
    'oppo-33w-power-bank-10000.png': 'https://www.startech.com.bd/image/cache/catalog/power-bank/anker/zolo-10k/zolo-10k-500x500.webp',
    'vivo-tws-4-hifi.png': 'https://www.startech.com.bd/image/cache/catalog/earbuds/cmf/buds-neo/buds-neo-01-500x500.webp',
    'vivo-120w-flashcharge-gan-adapter.png': 'https://www.startech.com.bd/image/cache/catalog/charger/anker/prime-160w/prime-160w-01-500x500.webp',
    'vivo-66w-power-bank-20000.png': 'https://www.startech.com.bd/image/cache/catalog/power-bank/anker/zolo-20000mah-45w/zolo-20000mah-45w-black-500x500.webp',
    'realme-120w-ultradart-charger.png': 'https://www.startech.com.bd/image/cache/catalog/charger/anker/prime-100w/prime-100w-01-500x500.webp',
    'realme-30w-dart-power-bank.png': 'https://www.startech.com.bd/image/cache/catalog/power-bank/anker/a110dh11/a110dh11-0-500x500.webp',
    'sony-cp-v10b-powerbank.png': 'https://www.startech.com.bd/image/cache/catalog/power-bank/anker/a110bh11/a110bh11-01-500x500.webp',
}

def isolate_and_center(im_path, out_path, target_size=1000, padding_pct=0.08):
    im = Image.open(im_path).convert('RGBA')
    isolated = remove(im)
    bbox = isolated.getbbox()
    if not bbox:
        isolated.save(out_path)
        return
    cropped = isolated.crop(bbox)
    w, h = cropped.size
    max_dim = int(target_size * (1 - 2 * padding_pct))
    scale = max_dim / max(w, h)
    nw, nh = max(1, int(w * scale)), max(1, int(h * scale))
    resized = cropped.resize((nw, nh), Image.Resampling.LANCZOS)
    canvas = Image.new('RGBA', (target_size, target_size), (0, 0, 0, 0))
    paste_x = (target_size - nw) // 2
    paste_y = (target_size - nh) // 2
    canvas.paste(resized, (paste_x, paste_y), resized)
    canvas.save(out_path)

for fname, url in BATCH2_MAP.items():
    raw_file = os.path.join(TEMP_DIR, 'raw_' + fname)
    out_file = os.path.join(PROD_DIR, fname)
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as r:
            with open(raw_file, 'wb') as f:
                f.write(r.read())
        isolate_and_center(raw_file, out_file)
        print(f'Successfully updated: {fname}', flush=True)
    except Exception as e:
        print(f'Failed {fname}: {e}', flush=True)

print('Batch 2 isolation complete!', flush=True)

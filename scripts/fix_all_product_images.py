import os
import urllib.request
from PIL import Image
import numpy as np
from rembg import remove

PROD_DIR = 'frontend/public/products'
SCRIPTS_DIR = 'scripts'

def download_file(url, out_path, headers=None):
    if os.path.exists(out_path) and os.path.getsize(out_path) > 1000:
        return
    h = headers or {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    req = urllib.request.Request(url, headers=h)
    with urllib.request.urlopen(req, timeout=15) as r:
        with open(out_path, 'wb') as f:
            f.write(r.read())
    print(f"Downloaded: {out_path}")

def isolate_crop_center(src_img_or_path, out_path, need_rembg=True, target_size=1000, padding_pct=0.08, crop_box=None):
    if isinstance(src_img_or_path, str):
        im = Image.open(src_img_or_path).convert('RGBA')
    else:
        im = src_img_or_path.convert('RGBA')
        
    if crop_box:
        im = im.crop(crop_box)
        
    if need_rembg:
        im = remove(im)
        
    bbox = im.getbbox()
    if not bbox:
        print(f"WARNING: empty bbox for {out_path}")
        im.save(out_path)
        return
        
    cropped = im.crop(bbox)
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
    print(f"Processed & saved: {os.path.basename(out_path)} ({nw}x{nh} in {target_size}x{target_size})")

def main():
    print("Starting comprehensive image upgrades...")
    
    # 1. Apple iPhone 16 Pro (remove gray banner)
    print("\n--- iPhone 16 Pro ---")
    isolate_crop_center(
        os.path.join(PROD_DIR, 'apple-iphone-16-pro.png'),
        os.path.join(PROD_DIR, 'apple-iphone-16-pro.png'),
        need_rembg=True
    )
    
    # 2. Apple iPhone 15 Pro Max (remove gray banner)
    print("\n--- iPhone 15 Pro Max ---")
    isolate_crop_center(
        os.path.join(PROD_DIR, 'apple-iphone-15-pro-max.png'),
        os.path.join(PROD_DIR, 'apple-iphone-15-pro-max.png'),
        need_rembg=True
    )
    
    # 3. Apple iPad Pro 13-inch M4 (fix edge clipping, add 8% floating padding)
    print("\n--- iPad Pro M4 ---")
    isolate_crop_center(
        os.path.join(PROD_DIR, 'ipad-pro-m4.png'),
        os.path.join(PROD_DIR, 'ipad-pro-m4.png'),
        need_rembg=False
    )
    
    # 4. Apple AirPods Pro 2 (scale & center to 1000x1000)
    print("\n--- AirPods Pro 2 ---")
    isolate_crop_center(
        os.path.join(PROD_DIR, 'airpods-pro-2.png'),
        os.path.join(PROD_DIR, 'airpods-pro-2.png'),
        need_rembg=True
    )
    
    # 5. Apple MagSafe Charger 25W (clean bottom border artifact & center)
    print("\n--- Apple MagSafe Charger 25W ---")
    # Clean bottom 10px if needed
    im_magsafe = Image.open(os.path.join(PROD_DIR, 'apple-magsafe-charger-25w.png')).convert('RGBA')
    # Crop slightly above the bottom line artifact
    w_m, h_m = im_magsafe.size
    im_magsafe = im_magsafe.crop((0, 0, w_m, h_m - 8))
    isolate_crop_center(
        im_magsafe,
        os.path.join(PROD_DIR, 'apple-magsafe-charger-25w.png'),
        need_rembg=True
    )
    # Also update apple-magsafe-charger.png for hero section
    im_magsafe.save(os.path.join(PROD_DIR, 'apple-magsafe-charger.png'))
    
    # 6. Anker MagGo Qi2 Cube (Official Apple Store 2000x2000 master)
    print("\n--- Anker MagGo Qi2 Cube ---")
    if os.path.exists('scripts/hrwv2_av1.jpg'):
        isolate_crop_center(
            'scripts/hrwv2_av1.jpg',
            os.path.join(PROD_DIR, 'anker-maggo-qi2-cube.png'),
            need_rembg=True
        )
        # Duplicate to anker-maggo-cube.png used in HeroSection and HomeClientView
        im_cube = Image.open(os.path.join(PROD_DIR, 'anker-maggo-qi2-cube.png'))
        im_cube.save(os.path.join(PROD_DIR, 'anker-maggo-cube.png'))
    
    # 7. Anker Prime 240W Desktop Station (Metal Stand 4-Port GaN)
    print("\n--- Anker Prime 240W ---")
    if os.path.exists('scripts/test_anker_240w.jpg'):
        isolate_crop_center(
            'scripts/test_anker_240w.jpg',
            os.path.join(PROD_DIR, 'anker-prime-240w-desktop-station.png'),
            need_rembg=True
        )
        
    # 8. Google Pixel Stand 2 (Official Google Store Render)
    print("\n--- Google Pixel Stand 2 ---")
    if os.path.exists('scripts/test_pixel_stand.png'):
        isolate_crop_center(
            'scripts/test_pixel_stand.png',
            os.path.join(PROD_DIR, 'google-pixel-stand-2.png'),
            need_rembg=True
        )
        
    # 9. Google 45W USB-C Charger (Official Google Store Rounded Profile)
    print("\n--- Google 45W USB-C Charger ---")
    if os.path.exists('scripts/test_google_45w.png'):
        isolate_crop_center(
            'scripts/test_google_45w.png',
            os.path.join(PROD_DIR, 'google-45w-usb-c-charger.png'),
            need_rembg=True
        )
        
    # 10. Google Pixel Watch 2 (Official Google Store Duo Render)
    print("\n--- Google Pixel Watch 2 ---")
    if os.path.exists('scripts/test_pw2_1.png'):
        isolate_crop_center(
            'scripts/test_pw2_1.png',
            os.path.join(PROD_DIR, 'google-pixel-watch-2.png'),
            need_rembg=False
        )
        
    # 11. Xiaomi 120W HyperCharge Combo (Official mi.com 1600x1600 Render)
    print("\n--- Xiaomi 120W HyperCharge ---")
    if os.path.exists('scripts/test_xiaomi_120w.png'):
        isolate_crop_center(
            'scripts/test_xiaomi_120w.png',
            os.path.join(PROD_DIR, 'xiaomi-120w-hypercharge-adapter.png'),
            need_rembg=False
        )
        
    # 12. Oppo Enco X3 (Official oppo.com Render)
    print("\n--- Oppo Enco X3 ---")
    if os.path.exists('scripts/test_oppo_enco.png'):
        isolate_crop_center(
            'scripts/test_oppo_enco.png',
            os.path.join(PROD_DIR, 'oppo-enco-x3.png'),
            need_rembg=False
        )
        
    # 13. Oppo 100W SuperVOOC GaN Adapter (Official oppo.com Render)
    print("\n--- Oppo 100W SuperVOOC ---")
    if os.path.exists('scripts/test_oppo_100w.png'):
        isolate_crop_center(
            'scripts/test_oppo_100w.png',
            os.path.join(PROD_DIR, 'oppo-100w-supervooc-gan-charger.png'),
            need_rembg=False
        )
        
    # 14. Oppo 33W Power Bank 10000 (Official Oppo Pocket Charge)
    print("\n--- Oppo 33W Power Bank ---")
    if os.path.exists('scripts/test_oppo_pb.jpg'):
        im_opb = Image.open('scripts/test_oppo_pb.jpg')
        # Crop the top white/tan power bank
        w_op, h_op = im_opb.size
        crop_top = im_opb.crop((int(w_op*0.05), int(h_op*0.1), int(w_op*0.65), int(h_op*0.6)))
        isolate_crop_center(
            crop_top,
            os.path.join(PROD_DIR, 'oppo-33w-power-bank-10000.png'),
            need_rembg=True
        )
        
    # 15. Vivo TWS 4 Hi-Fi (Official vivo.com 750x750 Render)
    print("\n--- Vivo TWS 4 Hi-Fi ---")
    if os.path.exists('scripts/test_vivo_tws4.webp'):
        isolate_crop_center(
            'scripts/test_vivo_tws4.webp',
            os.path.join(PROD_DIR, 'vivo-tws-4-hifi.png'),
            need_rembg=False
        )
        
    # 16. Vivo 120W FlashCharge Adapter (Official vivo.com Render)
    print("\n--- Vivo 120W FlashCharge ---")
    if os.path.exists('scripts/test_vivo_120w.webp'):
        im_v120 = Image.open('scripts/test_vivo_120w.webp')
        # Crop adapter on left
        w_v, h_v = im_v120.size
        adapter_crop = im_v120.crop((int(w_v*0.15), int(h_v*0.3), int(w_v*0.55), int(h_v*0.9)))
        isolate_crop_center(
            adapter_crop,
            os.path.join(PROD_DIR, 'vivo-120w-flashcharge-gan-adapter.png'),
            need_rembg=True
        )
        
    # 17. Vivo FlashCharge Power Bank (Official vivo studio render)
    print("\n--- Vivo 66W Power Bank ---")
    if os.path.exists('scripts/test_vivo_pb.png'):
        im_vpb = Image.open('scripts/test_vivo_pb.png')
        w_vp, h_vp = im_vpb.size
        # Crop the white vivo flashcharge power bank on the right
        pb_crop = im_vpb.crop((int(w_vp*0.38), int(h_vp*0.3), int(w_vp*0.98), int(h_vp*0.98)))
        isolate_crop_center(
            pb_crop,
            os.path.join(PROD_DIR, 'vivo-66w-power-bank-20000.png'),
            need_rembg=True
        )
        
    # 18. Vivo Pad 3 Pro (Official vivo.com Render)
    print("\n--- Vivo Pad 3 Pro ---")
    if os.path.exists('scripts/test_vivo_pad3.png'):
        isolate_crop_center(
            'scripts/test_vivo_pad3.png',
            os.path.join(PROD_DIR, 'vivo-pad-3-pro.png'),
            need_rembg=True
        )
        
    # 19. Vivo Watch 3 (Official vivo.com 750x750 Render)
    print("\n--- Vivo Watch 3 ---")
    if os.path.exists('scripts/test_vivo_w3.webp'):
        isolate_crop_center(
            'scripts/test_vivo_w3.webp',
            os.path.join(PROD_DIR, 'vivo-watch-3.png'),
            need_rembg=False
        )
        
    # 20. OnePlus Pad 2 (Official oneplus.com 960x960 Render)
    print("\n--- OnePlus Pad 2 ---")
    if os.path.exists('scripts/oneplus_pad2_net.png'):
        isolate_crop_center(
            'scripts/oneplus_pad2_net.png',
            os.path.join(PROD_DIR, 'oneplus-pad-2.png'),
            need_rembg=False
        )
        
    # 21. OnePlus 22.5W Power Bank (Official OnePlus 1+ Power Bank)
    print("\n--- OnePlus Power Bank ---")
    if os.path.exists('scripts/test_oneplus_pb.jpg'):
        isolate_crop_center(
            'scripts/test_oneplus_pb.jpg',
            os.path.join(PROD_DIR, 'oneplus-22-5w-power-bank.png'),
            need_rembg=True
        )
        
    # 22. Realme Watch S2 (Official realme.com 2280x900 Render)
    print("\n--- Realme Watch S2 ---")
    if os.path.exists('scripts/test_realme_w_s2.jpg'):
        im_rs2 = Image.open('scripts/test_realme_w_s2.jpg')
        # Center crop the watch
        w_r, h_r = im_rs2.size
        watch_crop = im_rs2.crop((int(w_r*0.25), 0, int(w_r*0.75), h_r))
        isolate_crop_center(
            watch_crop,
            os.path.join(PROD_DIR, 'realme-watch-s2.png'),
            need_rembg=True
        )
        
    # 23. Realme 120W UltraDart Charger (Official realme SuperDart)
    print("\n--- Realme UltraDart Charger ---")
    download_file(
        'https://www.startech.com.bd/image/cache/catalog/adapter/realme/65w-superdart/65w-superdart-01-500x500.webp',
        'scripts/test_realme_charger.webp'
    )
    if os.path.exists('scripts/test_realme_charger.webp'):
        isolate_crop_center(
            'scripts/test_realme_charger.webp',
            os.path.join(PROD_DIR, 'realme-120w-ultradart-charger.png'),
            need_rembg=True
        )
        
    # 24. Realme 30W Dart Power Bank (Official realme Dart Charge Power Bank)
    print("\n--- Realme Dart Power Bank ---")
    if os.path.exists('scripts/test_realme_pb.jpg'):
        isolate_crop_center(
            'scripts/test_realme_pb.jpg',
            os.path.join(PROD_DIR, 'realme-30w-dart-power-bank.png'),
            need_rembg=True
        )
        
    # 25. Sony CP-V10B Power Bank (Official Sony 1500x1500 Master)
    print("\n--- Sony CP-V10B Power Bank ---")
    if os.path.exists('scripts/test_sony_pb.jpg'):
        isolate_crop_center(
            'scripts/test_sony_pb.jpg',
            os.path.join(PROD_DIR, 'sony-cp-v10b-powerbank.png'),
            need_rembg=True
        )

    print("\nAll 25 product images upgraded successfully!")

if __name__ == '__main__':
    main()

import json
import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

os.makedirs('frontend/public/products', exist_ok=True)
os.makedirs('frontend/public/brands', exist_ok=True)
os.makedirs('backend/data', exist_ok=True)

# Helper to create sleek studio hardware renders
def create_studio_canvas(size=(1000, 1000)):
    return Image.new('RGBA', size, (0, 0, 0, 0))

# 1. Multi-Brand Wireless Chargers Render Generator
def draw_apple_magsafe_puck():
    im = create_studio_canvas()
    d = ImageDraw.Draw(im)
    # Cable
    d.arc([150, 400, 600, 850], start=45, end=210, fill=(210, 212, 215, 255), width=24)
    # Outer ring
    d.ellipse([280, 280, 720, 720], fill=(235, 237, 240, 255), outline=(190, 193, 198, 255), width=12)
    # Inner MagSafe white puck
    d.ellipse([340, 340, 660, 660], fill=(255, 255, 255, 255), outline=(220, 222, 226, 255), width=4)
    # Subtle inner Qi2 ring
    d.ellipse([430, 430, 570, 570], outline=(225, 227, 232, 255), width=6)
    im.save('frontend/public/products/apple-magsafe-charger.png')

def draw_samsung_wireless_trio():
    im = create_studio_canvas()
    d = ImageDraw.Draw(im)
    # Slate base
    d.rounded_rectangle([120, 350, 880, 650], radius=48, fill=(24, 27, 33, 255), outline=(55, 60, 70, 255), width=6)
    # Phone pad area (left)
    d.rounded_rectangle([160, 380, 460, 620], radius=24, outline=(45, 50, 62, 255), width=4)
    d.ellipse([290, 480, 330, 520], outline=(0, 113, 227, 180), width=3)
    # Watch magnetic recess (middle)
    d.ellipse([510, 450, 610, 550], fill=(16, 18, 22, 255), outline=(0, 113, 227, 220), width=4)
    # Buds pad area (right)
    d.rounded_rectangle([660, 410, 840, 590], radius=24, outline=(45, 50, 62, 255), width=4)
    # LED Indicators
    for x in [310, 560, 750]:
        d.ellipse([x-4, 625, x+4, 633], fill=(0, 230, 150, 255))
    im.save('frontend/public/products/samsung-wireless-trio.png')

def draw_wireless_stand(brand_color=(0, 113, 227), brand_name="SAMSUNG", filename="samsung-wireless-stand.png"):
    im = create_studio_canvas()
    d = ImageDraw.Draw(im)
    # Base pedestal
    d.ellipse([240, 680, 760, 860], fill=(30, 33, 40, 255), outline=(60, 65, 75, 255), width=6)
    # Upright angled charging backplate
    d.polygon([(340, 220), (660, 220), (710, 720), (290, 720)], fill=(20, 23, 28, 255), outline=(50, 55, 65, 255))
    # Charging coil indicator ring
    d.ellipse([410, 360, 590, 540], outline=brand_color, width=8)
    d.ellipse([465, 415, 535, 485], fill=brand_color)
    # Rest lip
    d.rounded_rectangle([330, 700, 670, 740], radius=12, fill=(40, 44, 52, 255), outline=(70, 75, 85, 255), width=3)
    # Brand LED
    d.ellipse([490, 790, 510, 810], fill=brand_color)
    im.save(f'frontend/public/products/{filename}')

def draw_anker_maggo_cube():
    im = create_studio_canvas()
    d = ImageDraw.Draw(im)
    # Folded cube base
    d.rounded_rectangle([280, 420, 720, 780], radius=40, fill=(35, 38, 44, 255), outline=(70, 75, 85, 255), width=6)
    # Pop-up MagSafe Qi2 arm (tilted)
    d.polygon([(310, 430), (690, 430), (660, 210), (340, 210)], fill=(45, 49, 56, 255), outline=(90, 95, 105, 255))
    # Magnetic ring on face
    d.ellipse([410, 240, 590, 400], outline=(0, 165, 232, 255), width=8)
    d.line([(500, 285), (500, 355)], fill=(0, 165, 232, 255), width=6)
    # Anker Cyan LED line
    d.line([400, 740, 600, 740], fill=(0, 165, 232, 255), width=4)
    im.save('frontend/public/products/anker-maggo-cube.png')

def draw_anker_prime_powerbank():
    im = create_studio_canvas()
    d = ImageDraw.Draw(im)
    # Power bank pillar
    d.rounded_rectangle([340, 180, 660, 820], radius=44, fill=(28, 30, 36, 255), outline=(60, 64, 74, 255), width=6)
    # OLED smart display
    d.rounded_rectangle([380, 240, 620, 440], radius=20, fill=(10, 12, 16, 255), outline=(40, 44, 52, 255), width=3)
    # Display telemetry graphics
    d.ellipse([450, 270, 550, 370], outline=(0, 165, 232, 255), width=6)
    # Anker metallic ports top
    d.rounded_rectangle([420, 155, 480, 180], radius=6, fill=(15, 17, 20, 255))
    d.rounded_rectangle([520, 155, 580, 180], radius=6, fill=(15, 17, 20, 255))
    im.save('frontend/public/products/anker-prime-powerbank.png')

# 2. Earbuds Case & Buds Generator
def draw_earbuds(brand_color, accent_color, filename):
    im = create_studio_canvas()
    d = ImageDraw.Draw(im)
    # Pebble charging case
    d.ellipse([260, 380, 740, 740], fill=(245, 246, 248, 255), outline=(210, 214, 220, 255), width=8)
    d.line([265, 540, 735, 540], fill=(200, 204, 210, 255), width=4)
    # Earbuds stems sticking out slightly or placed beside
    d.rounded_rectangle([200, 240, 260, 440], radius=24, fill=(255, 255, 255, 255), outline=(215, 218, 224, 255), width=4)
    d.ellipse([180, 210, 280, 310], fill=(255, 255, 255, 255), outline=(215, 218, 224, 255), width=4)
    d.rounded_rectangle([740, 240, 800, 440], radius=24, fill=(255, 255, 255, 255), outline=(215, 218, 224, 255), width=4)
    d.ellipse([720, 210, 820, 310], fill=(255, 255, 255, 255), outline=(215, 218, 224, 255), width=4)
    # Accent badge / status LED
    d.ellipse([490, 570, 510, 590], fill=brand_color)
    im.save(f'frontend/public/products/{filename}')

# 3. Smartwatch Generator
def draw_smartwatch(case_color, strap_color, screen_color, filename, circular=True):
    im = create_studio_canvas()
    d = ImageDraw.Draw(im)
    # Straps top & bottom
    d.rounded_rectangle([400, 100, 600, 360], radius=24, fill=strap_color)
    d.rounded_rectangle([400, 640, 600, 900], radius=24, fill=strap_color)
    # Watch Case
    if circular:
        d.ellipse([310, 310, 690, 690], fill=case_color, outline=(120, 125, 135, 255), width=8)
        # Crown
        d.rounded_rectangle([685, 460, 715, 540], radius=8, fill=case_color)
        # AMOLED Screen
        d.ellipse([345, 345, 655, 655], fill=screen_color)
        # UI Accent Rings
        d.ellipse([380, 380, 620, 620], outline=(0, 230, 150, 160), width=6)
        d.ellipse([410, 410, 590, 590], outline=(0, 113, 227, 180), width=6)
    else:
        d.rounded_rectangle([320, 310, 680, 690], radius=72, fill=case_color, outline=(120, 125, 135, 255), width=8)
        d.rounded_rectangle([675, 440, 710, 520], radius=8, fill=case_color)
        d.rounded_rectangle([350, 340, 650, 660], radius=50, fill=screen_color)
        d.ellipse([420, 420, 580, 580], outline=(246, 171, 29, 200), width=8)
    im.save(f'frontend/public/products/{filename}')

# 4. Smartphone Render Generator (Clean Studio Lineup)
def draw_smartphone(body_color, camera_style, camera_accent, filename):
    im = create_studio_canvas()
    d = ImageDraw.Draw(im)
    # Phone Body (Graceful curved rectangle)
    d.rounded_rectangle([290, 140, 710, 860], radius=68, fill=body_color, outline=(140, 145, 155, 255), width=7)
    
    # Camera Island Style
    if camera_style == 'circle': # Leica / Zeiss circular matrix
        d.ellipse([370, 200, 630, 460], fill=(22, 24, 28, 255), outline=camera_accent, width=6)
        # 4 lens elements
        for cx, cy in [(440, 270), (560, 270), (440, 390), (560, 390)]:
            d.ellipse([cx-32, cy-32, cx+32, cy+32], fill=(10, 12, 16, 255), outline=(60, 65, 75, 255), width=4)
            d.ellipse([cx-12, cy-12, cx+12, cy+12], fill=(28, 38, 55, 255))
    elif camera_style == 'squircle': # Hasselblad / OnePlus matrix
        d.rounded_rectangle([340, 200, 560, 440], radius=48, fill=(22, 24, 28, 255), outline=camera_accent, width=6)
        for cx, cy in [(400, 260), (500, 260), (400, 370)]:
            d.ellipse([cx-28, cy-28, cx+28, cy+28], fill=(10, 12, 16, 255), outline=(60, 65, 75, 255), width=3)
    elif camera_style == 'visor': # Pixel style camera visor bar
        d.rounded_rectangle([292, 240, 708, 380], radius=28, fill=(25, 27, 32, 255), outline=(70, 75, 85, 255), width=5)
        d.rounded_rectangle([340, 270, 540, 350], radius=32, fill=(10, 12, 16, 255))
        d.ellipse([580, 290, 640, 330], fill=(10, 12, 16, 255))
    else: # Vertical multi-camera pill
        d.rounded_rectangle([330, 190, 450, 480], radius=40, fill=(20, 22, 26, 255), outline=camera_accent, width=4)
        for cy in [245, 335, 425]:
            d.ellipse([390-28, cy-28, 390+28, cy+28], fill=(10, 12, 16, 255), outline=(55, 60, 70, 255), width=3)

    im.save(f'frontend/public/products/{filename}')

# 5. Tablet Generator
def draw_tablet(body_color, filename):
    im = create_studio_canvas()
    d = ImageDraw.Draw(im)
    # Tablet slate
    d.rounded_rectangle([190, 200, 810, 800], radius=42, fill=body_color, outline=(140, 145, 155, 255), width=6)
    # Camera corner
    d.rounded_rectangle([230, 240, 310, 340], radius=20, fill=(22, 24, 28, 255), outline=(60, 65, 75, 255), width=3)
    d.ellipse([270-16, 270-16, 270+16, 270+16], fill=(10, 12, 16, 255))
    im.save(f'frontend/public/products/{filename}')

print("Running image render generation...")
# Multi-Brand Wireless Chargers
draw_apple_magsafe_puck()
draw_samsung_wireless_trio()
draw_wireless_stand((0, 113, 227), "SAMSUNG", "samsung-wireless-stand.png")
draw_wireless_stand((255, 105, 0), "XIAOMI", "xiaomi-wireless-stand.png")
draw_wireless_stand((235, 0, 41), "ONEPLUS", "oneplus-airvooc-50w.png")
draw_wireless_stand((33, 148, 77), "OPPO", "oppo-airvooc-50w.png")
draw_wireless_stand((65, 90, 250), "VIVO", "vivo-flashcharge-50w.png")
draw_wireless_stand((66, 133, 244), "GOOGLE", "google-pixel-stand.png")
draw_wireless_stand((255, 201, 21), "REALME", "realme-magdart-50w.png")
draw_anker_maggo_cube()
draw_anker_prime_powerbank()

# Earbuds
draw_earbuds((0, 113, 227), (200, 200, 200), "samsung-galaxy-buds3-pro.png")
draw_earbuds((255, 105, 0), (200, 200, 200), "xiaomi-buds-5.png")
draw_earbuds((235, 0, 41), (200, 200, 200), "oneplus-buds-pro-3.png")
draw_earbuds((33, 148, 77), (200, 200, 200), "oppo-enco-x3.png")
draw_earbuds((65, 90, 250), (200, 200, 200), "vivo-tws-4-hifi.png")
draw_earbuds((66, 133, 244), (200, 200, 200), "google-pixel-buds-pro-2.png")
draw_earbuds((255, 201, 21), (200, 200, 200), "realme-buds-air-6-pro.png")
draw_earbuds((0, 165, 232), (200, 200, 200), "anker-soundcore-liberty-4-nc.png")
draw_earbuds((20, 20, 20), (200, 200, 200), "sony-wf1000xm5.png")

# Smartwatches
draw_smartwatch((215, 218, 224), (245, 130, 32), (15, 18, 22), "samsung-galaxy-watch-ultra.png", circular=False)
draw_smartwatch((40, 42, 48), (55, 58, 65), (12, 14, 18), "google-pixel-watch-3.png", circular=True)
draw_smartwatch((200, 205, 212), (30, 35, 42), (12, 14, 18), "oneplus-watch-2.png", circular=True)
draw_smartwatch((45, 48, 54), (255, 105, 0), (12, 14, 18), "xiaomi-watch-2-pro.png", circular=True)
draw_smartwatch((210, 215, 220), (33, 148, 77), (12, 14, 18), "oppo-watch-x.png", circular=True)
draw_smartwatch((35, 38, 44), (65, 90, 250), (12, 14, 18), "vivo-watch-3.png", circular=True)
draw_smartwatch((205, 210, 215), (255, 201, 21), (12, 14, 18), "realme-watch-s2.png", circular=True)

# Smartphones
draw_smartphone((28, 30, 34), 'circle', (255, 75, 40), "xiaomi-14-ultra.png")
draw_smartphone((240, 242, 245), 'squircle', (255, 105, 0), "xiaomi-14.png")
draw_smartphone((32, 65, 55), 'circle', (235, 0, 41), "oneplus-12.png")
draw_smartphone((30, 32, 36), 'circle', (235, 0, 41), "oneplus-open.png")
draw_smartphone((210, 195, 175), 'circle', (190, 150, 100), "oppo-find-x7-ultra.png")
draw_smartphone((215, 218, 228), 'vertical', (33, 148, 77), "oppo-reno-12-pro.png")
draw_smartphone((38, 40, 45), 'circle', (65, 90, 250), "vivo-x100-ultra.png")
draw_smartphone((225, 230, 238), 'vertical', (65, 90, 250), "vivo-v30-pro.png")
draw_smartphone((205, 215, 225), 'visor', (255, 201, 21), "realme-gt-6.png")
draw_smartphone((35, 38, 42), 'visor', (66, 133, 244), "google-pixel-9-fold.png")

# Tablets
draw_tablet((220, 222, 226), "oneplus-pad-2.png")
draw_tablet((200, 202, 206), "xiaomi-pad-6s-pro.png")
draw_tablet((30, 32, 36), "samsung-galaxy-tab-s9-ultra.png")
draw_tablet((225, 228, 232), "google-pixel-tablet.png")

print("All studio hardware images generated successfully!")

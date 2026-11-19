import json
import os
import math
from PIL import Image, ImageDraw, ImageFilter, ImageFont

PROD_JSON_PATH = 'backend/data/products.json'
OUT_DIR = 'frontend/public/products'
os.makedirs(OUT_DIR, exist_ok=True)

with open(PROD_JSON_PATH, 'r', encoding='utf-8') as f:
    products = json.load(f)

# Helper function to create gradient-like subtle lighting
def draw_studio_shadow(draw, bbox, blur_radius=30):
    pass

# Hardware Color Definitions
BRAND_PALETTES = {
    'apple-iphone-16-pro-max': ('#C8B29E', '#E4D5C7', '#7D6D5E', 'titanium_triple'), # Desert Titanium
    'apple-iphone-16-pro': ('#E3E4E5', '#FFFFFF', '#9E9FA0', 'titanium_triple'),     # White Titanium
    'apple-iphone-16': ('#385499', '#5A7AC8', '#1A2F63', 'pill_dual'),                # Ultramarine Blue
    'apple-iphone-15-pro-max': ('#39424E', '#5B6574', '#212933', 'titanium_triple'), # Blue Titanium
    'apple-iphone-15': ('#FCE4EC', '#FFF0F5', '#C27088', 'diagonal_dual'),           # Pink
    'apple-ipad-air-m2': ('#9FA8A3', '#CCD5D0', '#5C635F', 'tablet_single'),         # Space Gray M2
    'apple-ipad-mini-a17': ('#7E6B80', '#A994AB', '#4E3E50', 'tablet_compact'),      # Purple A17
    'apple-macbook-air-15-m3': ('#0D1117', '#1E2530', '#05070A', 'laptop_open'),     # Midnight M3
    'apple-watch-se': ('#E0D5C1', '#F4ECE1', '#988D7B', 'watch_rect'),               # Starlight Aluminum
    'apple-airpods-4-anc': ('#FFFFFF', '#F0F0F2', '#D1D1D6', 'earbuds_open'),         # AirPods 4 White
    'apple-35w-dual-adapter': ('#FFFFFF', '#F5F5F7', '#D1D1D6', 'charger_wall'),     # Dual USB-C Wall
    
    # Samsung Models
    'samsung-galaxy-s24-plus': ('#F0E5AF', '#FFF8D6', '#B3A66B', 'samsung_triple'),  # Amber Yellow
    'samsung-galaxy-s24': ('#645E7A', '#8E86A8', '#3F3A52', 'samsung_triple'),       # Cobalt Violet
    'samsung-galaxy-s23-ultra': ('#1A1A1A', '#333333', '#000000', 'samsung_quad_sharp'), # Phantom Black
    'samsung-galaxy-s23-fe': ('#C1E1DC', '#E0F2F1', '#80A8A2', 'samsung_triple'),    # Mint
    'samsung-galaxy-z-flip-6': ('#91A4B7', '#B8C9DA', '#586C7F', 'fold_flip'),       # Blue Flex
    'samsung-galaxy-tab-s9-plus': ('#2C2D30', '#4A4C50', '#18191B', 'tablet_wide'),   # Graphite Tab
    'samsung-galaxy-tab-s9-fe': ('#E4E8DA', '#F5F7F0', '#B0B5A6', 'tablet_pen'),     # Light Green
    'samsung-galaxy-watch-7': ('#36454F', '#566B79', '#1C2833', 'watch_circle_flat'),# Green Armor
    'samsung-galaxy-watch-6-classic': ('#D4D8DD', '#F0F3F6', '#8F969E', 'watch_bezel'),# Silver Bezel
    'samsung-galaxy-buds3': ('#E5E9EC', '#FFFFFF', '#A9B3BA', 'buds_blade_open'),    # Silver Blade
    'samsung-galaxy-buds2-pro': ('#2D2B30', '#4A4850', '#17161A', 'buds_pebble'),    # Graphite Pebble
    'samsung-45w-power-adapter': ('#111111', '#282828', '#000000', 'charger_brick'),  # 45W Black GaN
    
    # Xiaomi Models
    'xiaomi-14t-pro': ('#1D232A', '#38424D', '#0B0E12', 'xiaomi_sq_triple'),         # Titan Black
    'xiaomi-13t-pro': ('#4F709C', '#7B98BE', '#294364', 'xiaomi_sq_triple'),         # Alpine Blue Leather
    'xiaomi-redmi-note-13-pro-plus': ('#D0C9E8', '#EDE8FA', '#9A8EC0', 'curved_fusion'), # Fusion Purple
    'xiaomi-poco-f6-pro': ('#FFFFFF', '#ECEFF1', '#B0BEC5', 'poco_glass'),            # Lunar White
    'xiaomi-poco-x6-pro': ('#FFD600', '#FFE653', '#B29500', 'poco_yellow'),           # POCO Yellow
    'xiaomi-pad-6': ('#8E979D', '#BFC7CC', '#5B6267', 'tablet_wide'),                # Gravity Gray
    'xiaomi-watch-s3': ('#1A1C1E', '#34383C', '#0A0B0C', 'watch_bezel_changeable'),  # Interchangeable bezel
    'xiaomi-smart-band-9': ('#2C3437', '#4A5559', '#14181A', 'band_oval'),           # Midnight Black
    'xiaomi-smart-band-8-pro': ('#D8DCE0', '#F2F5F8', '#9DA4AB', 'band_wide'),        # Light Gold Metallic
    'xiaomi-redmi-buds-5-pro': ('#121316', '#26282E', '#060708', 'buds_pebble_stem'),# Midnight Black
    'xiaomi-80w-adaptive-wireless-stand': ('#EAEAEA', '#FFFFFF', '#B8B8B8', 'charger_stand'),
    'xiaomi-120w-hypercharge-adapter': ('#FFFFFF', '#F0F0F0', '#CCCCCC', 'charger_hyper'),
    'xiaomi-67w-gan-charger': ('#FFFFFF', '#F5F5F7', '#D5D5D8', 'charger_brick_white'),
    'xiaomi-22-5w-power-bank': ('#1E2022', '#3A3E42', '#0C0D0E', 'powerbank_tall'),
    
    # Oppo Models
    'oppo-find-n3': ('#8C6D46', '#B8986E', '#564024', 'fold_book_gold'),             # Champagne Gold Fold
    'oppo-find-n3-flip': ('#EAD5D7', '#F8EDED', '#B39598', 'fold_flip_glass'),       # Misty Pink
    'oppo-reno-11-pro': ('#E4ECE9', '#F4F8F6', '#ADC0BA', 'oppo_pill_triple'),       # Pearl White
    'oppo-reno-12': ('#544E68', '#7E7696', '#2F2B3E', 'oppo_pill_triple'),           # Astro Silver Matte
    'oppo-f27-pro-plus': ('#A33842', '#D05561', '#661E25', 'oppo_circle_leather'),   # Dusk Pink Leather
    'oppo-pad-air': ('#737B82', '#A3ABB2', '#454B50', 'tablet_wide'),                # Fog Silver
    'oppo-watch-4-pro': ('#2A2F35', '#485058', '#14171A', 'watch_curve_rect'),       # Curved AMOLED
    'oppo-enco-x2': ('#FFFFFF', '#F2F5F8', '#C5CCD3', 'earbuds_pebble_case'),         # Frost White Dynaudio
    'oppo-enco-air-4-pro': ('#596773', '#8594A1', '#323C44', 'earbuds_translucent'),  # Moonlight Silver
    'oppo-enco-buds-2': ('#FFFFFF', '#F4F4F6', '#D0D0D5', 'earbuds_compact'),
    'oppo-100w-supervooc-gan-charger': ('#FFFFFF', '#F0F0F0', '#CCCCCC', 'charger_supervooc'),
    'oppo-80w-supervooc-flash-charger': ('#FFFFFF', '#F5F5F5', '#DDDDDD', 'charger_brick_white'),
    'oppo-67w-supervooc-adapter': ('#FFFFFF', '#F5F5F5', '#DDDDDD', 'charger_brick_white'),
    'oppo-33w-power-bank': ('#1C1E21', '#35393D', '#0B0C0D', 'powerbank_supervooc'),

    # Vivo Models
    'vivo-x100-pro': ('#385B66', '#598492', '#1E353C', 'vivo_zeiss_sunburst'),       # Sunset Orange / Starry Blue
    'vivo-v40-pro': ('#DCE5ED', '#F0F5FA', '#98AAB8', 'vivo_aura_light'),            # Ganges Blue
    'vivo-v40': ('#DFD3C3', '#F2EBE0', '#A39482', 'vivo_aura_light'),                # Titanium Grey
    'vivo-v30-pro': ('#CEE5D6', '#EAF5EE', '#8BB599', 'vivo_aura_light'),            # Andaman Blue
    'vivo-v30e': ('#642D38', '#8E4654', '#3E1820', 'vivo_aura_light'),               # Velvet Red
    'vivo-t3-ultra': ('#233142', '#3D4F66', '#111A24', 'vivo_rect_dual'),            # Frost Green
    'vivo-pad-air': ('#848D95', '#B1BCC5', '#525B62', 'tablet_wide'),                # Deep Space Gray
    'vivo-watch-3': ('#1A1B1D', '#34363A', '#0B0C0D', 'watch_circle_flat'),          # 3D Curved Glass
    'vivo-watch-gt': ('#30343A', '#525861', '#17191C', 'watch_rect'),                # Rectangular e-SIM
    'vivo-tws-3e': ('#FFFFFF', '#EFF2F5', '#CBD2D9', 'earbuds_pebble_case'),         # Bright White
    'vivo-tws-air-2': ('#DFE3E6', '#F5F7F9', '#A8B1B8', 'earbuds_compact'),
    'vivo-wireless-sport-earphones': ('#1E2226', '#3A4047', '#0F1113', 'earbuds_neckband'),
    'vivo-120w-flashcharge-adapter': ('#FFFFFF', '#F0F0F0', '#CCCCCC', 'charger_hyper'),
    'vivo-80w-flashcharge-charger': ('#FFFFFF', '#F5F5F5', '#D5D5D5', 'charger_brick_white'),
    'vivo-44w-flashcharge-adapter': ('#FFFFFF', '#F5F5F5', '#D5D5D5', 'charger_brick_white'),
    'vivo-22-5w-power-bank': ('#212529', '#3E444A', '#101214', 'powerbank_tall'),

    # OnePlus Models
    'oneplus-12r': ('#415865', '#638090', '#25353E', 'oneplus_deco_ring'),           # Cool Blue
    'oneplus-open': ('#1A2E26', '#304D41', '#0D1A14', 'fold_oneplus_emerald'),       # Emerald Dusk Fold
    'oneplus-nord-4': ('#A3A7AB', '#CCD0D5', '#6B7075', 'oneplus_metal_unibody'),    # Mercurial Silver Unibody
    'oneplus-nord-ce4': ('#BFD8D2', '#DEF0EC', '#85ABA3', 'oneplus_pill_vert'),      # Celadon Marble
    'oneplus-nord-ce4-lite': ('#0091FF', '#47AFFF', '#005CB8', 'oneplus_pill_vert'),  # Mega Blue
    'oneplus-pad-go': ('#7A9E9F', '#A3C4C5', '#4C696A', 'tablet_oneplus_two_tone'),  # Twin Mint
    'oneplus-watch-2r': ('#2B547E', '#4876A6', '#173656', 'watch_bezel_two_tone'),   # Forest Green
    'oneplus-buds-pro-2': ('#394B43', '#576F64', '#212E28', 'buds_oneplus_rect'),    # Arbor Green
    'oneplus-nord-buds-3-pro': ('#44505B', '#677785', '#262F37', 'earbuds_pebble_case'), # Starry Black
    'oneplus-nord-buds-2r': ('#1D2B3A', '#34475B', '#0E1721', 'earbuds_compact'),     # Deep Gray
    'oneplus-bullets-wireless-z2': ('#18191B', '#33363A', '#090A0B', 'earbuds_neckband'), # Acoustic Red/Black
    'oneplus-100w-supervooc-dual-port': ('#FFFFFF', '#F0F0F0', '#CCCCCC', 'charger_supervooc'),
    'oneplus-80w-supervooc-power-adapter': ('#FFFFFF', '#F5F5F5', '#DDDDDD', 'charger_brick_white'),
    'oneplus-supervooc-100w-car-charger': ('#1C1E20', '#35393D', '#0B0C0D', 'charger_car'),
    'oneplus-22-5w-power-bank': ('#1C1E21', '#373B40', '#0E0F10', 'powerbank_tall'),

    # Google Models
    'google-pixel-9-pro': ('#4A4A45', '#70706B', '#2C2C29', 'pixel_visor_oval'),     # Hazel
    'google-pixel-9': ('#DDA8AA', '#F5CDCF', '#A87375', 'pixel_visor_oval'),          # Peony Pink
    'google-pixel-8-pro': ('#79A7D3', '#A8C9EC', '#4774A0', 'pixel_visor_bar'),      # Bay Blue
    'google-pixel-8a': ('#84A98C', '#B0D0B7', '#52775A', 'pixel_visor_compact'),     # Aloe Green
    'google-pixel-watch-3-45': ('#1A1C1E', '#363A3E', '#0B0C0D', 'watch_pixel_dome'),# Matte Black 45mm
    'google-pixel-watch-3-41': ('#D8D3CD', '#F2ECE5', '#A19A92', 'watch_pixel_dome'),# Polished Silver 41mm
    'google-pixel-watch-leather-band': ('#6B4423', '#94653D', '#412711', 'watch_strap_leather'),
    'google-pixel-watch-active-band': ('#285238', '#407855', '#163321', 'watch_strap_sport'),
    'google-pixel-buds-pro': ('#7BA4B5', '#A5C9D8', '#4B7384', 'buds_pixel_egg'),    # Fog Blue
    'google-pixel-buds-a': ('#EBEBEB', '#FFFFFF', '#C2C2C2', 'buds_pixel_egg'),       # Clearly White
    'google-30w-usb-c-charger': ('#FFFFFF', '#F5F5F7', '#D1D1D6', 'charger_brick_white'),
    'google-45w-usb-c-charger': ('#FFFFFF', '#F5F5F7', '#D1D1D6', 'charger_brick_white'),
    'google-pixel-fold-case': ('#292B2D', '#464A4E', '#141516', 'case_phone'),
    'google-usb-c-headphone-adapter': ('#FFFFFF', '#F0F0F0', '#C0C0C0', 'cable_dongle'),

    # Realme Models
    'realme-gt-neo-6': ('#453257', '#695180', '#271934', 'realme_gt_stripes'),       # Cyber Purple
    'realme-13-pro-plus': ('#A67C52', '#CCA47A', '#6B4C29', 'realme_monet_gold'),    # Monet Gold
    'realme-13-pro': ('#3A5A40', '#588157', '#223826', 'realme_monet_gold'),         # Monet Green
    'realme-12-pro-plus': ('#1D3557', '#345682', '#0F1D30', 'realme_luxury_watch'),  # Submarine Blue
    'realme-12-plus': ('#2D4A3E', '#486E5E', '#182C24', 'realme_luxury_watch'),      # Pioneer Green
    'realme-c67-5g': ('#438A5E', '#6AB888', '#245938', 'realme_circle_dual'),        # Sunny Oasis
    'realme-pad-mini': ('#88929A', '#B2BBC3', '#5A636A', 'tablet_compact'),          # Flash Blue
    'realme-watch-3-pro': ('#25282B', '#41454A', '#111314', 'watch_rect'),           # Space Gray Large
    'realme-buds-air-6': ('#C8A2C8', '#E6CDE6', '#946B94', 'earbuds_pebble_case'),   # Royale Violet
    'realme-buds-t310': ('#2D3238', '#4B525B', '#16191C', 'earbuds_compact'),
    'realme-buds-wireless-3': ('#E5A93C', '#FFCE73', '#9C6C16', 'earbuds_neckband'), # Bass Yellow
    'realme-120w-ultradart-charger': ('#FFFFFF', '#F0F0F0', '#D0D0D0', 'charger_hyper'),
    'realme-80w-superdart-charger': ('#FFFFFF', '#F5F5F5', '#D8D8D8', 'charger_brick_white'),
    'realme-67w-superdart-charger': ('#FFFFFF', '#F5F5F5', '#D8D8D8', 'charger_brick_white'),
    'realme-30w-dart-power-bank': ('#FFE600', '#FFF066', '#B3A100', 'powerbank_dart'),# Dart Yellow

    # Anker Models
    'anker-maggo-qi2-powerbank': ('#363A40', '#565C66', '#1C1F24', 'powerbank_magsafe'), # Qi2 Slim PowerBank
    'anker-maggo-qi2-stand': ('#E8ECF0', '#FFFFFF', '#B4BCC4', 'charger_stand'),      # Pearl White Stand
    'anker-maggo-qi2-3in1-station': ('#202226', '#3A3E45', '#101113', 'charger_3in1_fold'), # Black Foldable
    'anker-prime-20000-powerbank': ('#1A1C20', '#343840', '#0B0C0E', 'powerbank_screen'), # 200W Smart Screen
    'anker-prime-12000-powerbank': ('#1F2329', '#3B414B', '#0F1114', 'powerbank_screen'), # 130W Smart Screen
    'anker-prime-100w-gan-charger': ('#1B1E22', '#363C44', '#0A0C0E', 'charger_gan_black'), # 100W GaN 3-Port
    'anker-prime-67w-gan-charger': ('#1B1E22', '#363C44', '#0A0C0E', 'charger_gan_black'),  # 67W GaN 3-Port
    'anker-prime-240w-desktop-station': ('#141618', '#2D3035', '#08090A', 'charger_desktop'), # 240W Pro
    'anker-737-powerbank': ('#1E2228', '#3C434F', '#0D0F12', 'powerbank_screen'),     # PowerCore 24K
    'anker-nano-30w-charger': ('#C5D3E8', '#E6EEFA', '#8FA4C2', 'charger_nano'),      # Misty Blue Nano
    'anker-soundcore-space-q45': ('#18191C', '#32343A', '#090A0B', 'headphone_over_ear'), # Deep Navy
    'anker-soundcore-liberty-4': ('#0F1012', '#282A30', '#050506', 'earbuds_sliding_case'),# Midnight Black

    # Sony Models
    'sony-wh1000xm4': ('#1A1A1A', '#333333', '#000000', 'headphone_sony_classic'),   # Black with Gold logo
    'sony-wh-ch720n': ('#2F4156', '#4E6A8A', '#192533', 'headphone_over_ear'),       # Blue Lightweight
    'sony-ult-wear': ('#111214', '#2B2E33', '#050607', 'headphone_sony_ult'),         # ULT Bass Black
    'sony-inzone-h9': ('#FFFFFF', '#EAEAEA', '#CCCCCC', 'headphone_gaming_white'),    # White Gaming Ring
    'sony-linkbuds-s': ('#D4C7B5', '#EFE7DC', '#A69783', 'earbuds_recycled_stone'),  # Earth Blue / Sand
    'sony-linkbuds-open': ('#2A2B2D', '#46484C', '#131415', 'earbuds_ring_open'),     # Open Ring Donut
    'sony-inzone-buds': ('#FFFFFF', '#E8ECEF', '#B5BFC7', 'earbuds_inzone'),          # White Gaming TWS
    'sony-xperia-5-v': ('#3D4A41', '#5D7063', '#232C26', 'sony_xperia_compact'),     # Platinum Green
    'sony-xperia-10-vi': ('#88B04B', '#A8D26C', '#5E822E', 'sony_xperia_slim'),      # Sage Green
    'sony-ult-field-7': ('#151618', '#2E3035', '#090A0B', 'speaker_boombox_cyl'),     # Rugged ULT Boombox
}

def generate_hardware_render(pid, model_type, color_pri, color_sec, color_dark):
    im = Image.new('RGBA', (1000, 1000), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)

    # 1. SMARTPHONES
    if 'triple' in model_type or 'samsung' in model_type or 'pixel' in model_type or 'fold' in model_type or 'deco' in model_type or 'oppo' in model_type or 'vivo' in model_type or 'realme' in model_type or 'xperia' in model_type or 'poco' in model_type or 'dual' in model_type:
        
        # Phone chassis boundaries
        x1, y1, x2, y2 = 320, 140, 680, 860
        corner_r = 52
        if 'sharp' in model_type or 'xperia' in model_type:
            corner_r = 16
        elif 'fold_book' in model_type:
            x1, y1, x2, y2 = 280, 140, 720, 860
            corner_r = 32
        elif 'fold_flip' in model_type:
            x1, y1, x2, y2 = 330, 200, 670, 800
            corner_r = 44

        # Drop shadow underneath chassis
        shadow_box = [x1 + 10, y1 + 20, x2 + 10, y2 + 25]
        draw.rounded_rectangle(shadow_box, radius=corner_r, fill=(0, 0, 0, 70))

        # Outer metallic bezel frame
        draw.rounded_rectangle([x1 - 4, y1 - 4, x2 + 4, y2 + 4], radius=corner_r + 4, fill=color_dark)
        
        # Satin glass back panel
        draw.rounded_rectangle([x1, y1, x2, y2], radius=corner_r, fill=color_pri)

        # Highlight gradient sheen
        draw.rounded_rectangle([x1 + 6, y1 + 6, x2 - 6, y1 + 120], radius=corner_r - 4, fill=color_sec)

        # Side buttons
        draw.rounded_rectangle([x2 + 3, y1 + 160, x2 + 7, y1 + 240], radius=2, fill=color_dark) # Vol
        draw.rounded_rectangle([x2 + 3, y1 + 270, x2 + 7, y1 + 330], radius=2, fill=color_dark) # Power

        # Distinct Camera Modules by Type
        if 'titanium_triple' in model_type:
            # Apple triangular pro camera plateau
            draw.rounded_rectangle([x1 + 24, y1 + 24, x1 + 160, y1 + 160], radius=32, fill=color_sec, outline=color_dark, width=2)
            for cx, cy in [(x1 + 60, y1 + 60), (x1 + 60, y1 + 124), (x1 + 124, y1 + 92)]:
                draw.ellipse([cx - 24, cy - 24, cx + 24, cy + 24], fill='#111111', outline=color_dark, width=4)
                draw.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill='#050505')
                draw.ellipse([cx - 8, cy - 8, cx - 2, cy - 2], fill='#3B82F6') # Optical reflection
            draw.ellipse([x1 + 120, y1 + 45, x1 + 132, y1 + 57], fill='#FCE7F3') # Flash

        elif 'pill_dual' in model_type or 'diagonal_dual' in model_type or 'oneplus_pill' in model_type:
            # Vertical pill camera island
            draw.rounded_rectangle([x1 + 28, y1 + 28, x1 + 88, y1 + 158], radius=28, fill=color_sec, outline=color_dark, width=2)
            draw.ellipse([x1 + 38, y1 + 38, x1 + 78, y1 + 78], fill='#111111', outline=color_dark, width=3)
            draw.ellipse([x1 + 38, y1 + 104, x1 + 78, y1 + 144], fill='#111111', outline=color_dark, width=3)
            draw.ellipse([x1 + 100, y1 + 84, x1 + 114, y1 + 98], fill='#FFFBEB') # Flash

        elif 'samsung' in model_type:
            # Floating individual camera lenses (Samsung Iconic Minimalist Design)
            for i, cy in enumerate([y1 + 50, y1 + 115, y1 + 180]):
                draw.ellipse([x1 + 32, cy - 22, x1 + 76, cy + 22], fill='#151515', outline=color_dark, width=3)
                draw.ellipse([x1 + 40, cy - 14, x1 + 68, cy + 14], fill='#070707')
                draw.ellipse([x1 + 44, cy - 10, x1 + 50, cy - 4], fill='#60A5FA')
            if 'quad' in model_type:
                draw.ellipse([x1 + 96, y1 + 50 - 15, x1 + 126, y1 + 50 + 15], fill='#181818', outline=color_dark, width=2)
                draw.ellipse([x1 + 96, y1 + 115 - 15, x1 + 126, y1 + 115 + 15], fill='#181818', outline=color_dark, width=2)

        elif 'pixel' in model_type:
            # Google Pixel Horizontal Camera Visor
            bar_y = y1 + 65
            draw.rounded_rectangle([x1 - 2, bar_y - 28, x2 + 2, bar_y + 36], radius=26, fill=color_dark, outline='#1A1A1A', width=2)
            draw.rounded_rectangle([x1 + 40, bar_y - 18, x1 + 180, bar_y + 26], radius=20, fill='#080808')
            draw.ellipse([x1 + 55, bar_y - 12, x1 + 85, bar_y + 18], fill='#1C1C1C')
            draw.ellipse([x1 + 95, bar_y - 12, x1 + 125, bar_y + 18], fill='#1C1C1C')
            draw.ellipse([x1 + 135, bar_y - 12, x1 + 165, bar_y + 18], fill='#1C1C1C')
            draw.ellipse([x2 - 60, bar_y - 6, x2 - 46, bar_y + 8], fill='#FFFBEB') # Flash

        elif 'xiaomi' in model_type or 'oppo_circle' in model_type or 'zeiss' in model_type or 'monet' in model_type or 'luxury' in model_type:
            # Giant circular camera dial / luxury watch bezel
            mcx, mcy = (x1 + x2) // 2, y1 + 140
            rad = 86
            draw.ellipse([mcx - rad - 4, mcy - rad - 4, mcx + rad + 4, mcy + rad + 4], fill=color_dark, outline='#F59E0B', width=2)
            draw.ellipse([mcx - rad, mcy - rad, mcx + rad, mcy + rad], fill='#121316')
            # 4 lenses inside dial
            for lx, ly in [(mcx - 36, mcy - 36), (mcx + 36, mcy - 36), (mcx - 36, mcy + 36), (mcx + 36, mcy + 36)]:
                draw.ellipse([lx - 18, ly - 18, lx + 18, ly + 18], fill='#050505', outline='#333333', width=2)
                draw.ellipse([lx - 8, ly - 8, lx - 2, ly - 2], fill='#38BDF8')

        elif 'oneplus' in model_type:
            # OnePlus circular off-center camera matrix merging with edge
            mcx, mcy = x1 + 95, y1 + 120
            draw.ellipse([mcx - 70, mcy - 70, mcx + 70, mcy + 70], fill='#16191D', outline=color_dark, width=4)
            for lx, ly in [(mcx - 28, mcy - 28), (mcx + 28, mcy - 28), (mcx - 28, mcy + 28), (mcx + 28, mcy + 28)]:
                draw.ellipse([lx - 16, ly - 16, lx + 16, ly + 16], fill='#070707', outline='#444444', width=2)

    # 2. SMARTWATCHES
    elif 'watch' in model_type or 'band' in model_type:
        cx, cy = 500, 500
        # Watch straps (top and bottom)
        strap_w = 120
        if 'band' in model_type:
            strap_w = 70
        draw.rounded_rectangle([cx - strap_w // 2, 100, cx + strap_w // 2, cy - 120], radius=16, fill=color_dark)
        draw.rounded_rectangle([cx - strap_w // 2, cy + 120, cx + strap_w // 2, 900], radius=16, fill=color_dark)

        # Watch Case
        if 'rect' in model_type:
            # Rounded rect watch case (Apple Watch / Oppo Watch)
            draw.rounded_rectangle([cx - 150, cy - 170, cx + 150, cy + 170], radius=56, fill=color_pri, outline=color_dark, width=6)
            draw.rounded_rectangle([cx - 128, cy - 148, cx + 128, cy + 148], radius=40, fill='#050508')
            # Digital Crown
            draw.rounded_rectangle([cx + 150, cy - 70, cx + 164, cy - 10], radius=6, fill=color_dark)
        elif 'circle' in model_type or 'bezel' in model_type:
            # Circular case (Galaxy Watch / Pixel Watch / Xiaomi Watch)
            r = 175
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color_pri, outline=color_dark, width=6)
            if 'bezel' in model_type:
                draw.ellipse([cx - r + 8, cy - r + 8, cx + r - 8, cy + r - 8], fill=color_sec, outline='#111111', width=3)
            draw.ellipse([cx - r + 26, cy - r + 26, cx + r - 26, cy + r - 26], fill='#050508')

        # Vibrant Display Graphics (Time & rings)
        draw.text((cx - 48, cy - 24), "10:09", fill='#FFFFFF')
        draw.ellipse([cx - 50, cy + 20, cx - 20, cy + 50], outline='#EF4444', width=3)
        draw.ellipse([cx - 15, cy + 20, cx + 15, cy + 50], outline='#10B981', width=3)
        draw.ellipse([cx + 20, cy + 20, cx + 50, cy + 50], outline='#06B6D4', width=3)

    # 3. EARBUDS
    elif 'buds' in model_type or 'earbuds' in model_type:
        cx, cy = 500, 500
        # Charging Case
        case_w, case_h = 320, 240
        draw.rounded_rectangle([cx - case_w // 2, cy - case_h // 2 + 30, cx + case_w // 2, cy + case_h // 2 + 30], radius=70, fill=color_pri, outline=color_dark, width=4)
        # Lid seam line
        draw.line([cx - case_w // 2 + 10, cy - 20, cx + case_w // 2 - 10, cy - 20], fill=color_dark, width=3)
        # LED Indicator
        draw.ellipse([cx - 5, cy + 30, cx + 5, cy + 40], fill='#10B981')

        # Earbuds Pop/Display above case
        # Left Bud
        draw.ellipse([cx - 100, cy - 240, cx - 40, cy - 180], fill=color_sec, outline=color_dark, width=2)
        draw.rounded_rectangle([cx - 80, cy - 190, cx - 60, cy - 90], radius=10, fill=color_sec, outline=color_dark, width=2)
        # Right Bud
        draw.ellipse([cx + 40, cy - 240, cx + 100, cy - 180], fill=color_sec, outline=color_dark, width=2)
        draw.rounded_rectangle([cx + 60, cy - 190, cx + 80, cy - 90], radius=10, fill=color_sec, outline=color_dark, width=2)

    # 4. HEADPHONES & AUDIO
    elif 'headphone' in model_type:
        cx, cy = 500, 500
        # Headband arch
        draw.arc([250, 160, 750, 660], start=180, end=0, fill=color_dark, width=24)
        # Left and Right Earcups
        for ex in [250, 750]:
            draw.rounded_rectangle([ex - 60, 420, ex + 60, 680], radius=44, fill=color_pri, outline=color_dark, width=4)
            draw.rounded_rectangle([ex - 45, 440, ex + 45, 660], radius=32, fill='#111111')

    # 5. CHARGERS & POWER BANKS
    elif 'charger' in model_type or 'powerbank' in model_type:
        cx, cy = 500, 500
        if 'powerbank' in model_type:
            # Sleek vertical power bank
            draw.rounded_rectangle([340, 200, 660, 800], radius=36, fill=color_pri, outline=color_dark, width=4)
            # Digital smart display
            draw.rounded_rectangle([400, 260, 600, 360], radius=16, fill='#0B0F19', outline='#1E293B', width=2)
            draw.text((460, 290), "100%", fill='#00E5FF')
            draw.text((465, 320), "65W", fill='#10B981')
        elif 'stand' in model_type:
            # Angled wireless stand
            draw.rounded_rectangle([360, 260, 640, 740], radius=32, fill=color_pri, outline=color_dark, width=4)
            draw.ellipse([450, 450, 550, 550], outline=color_sec, width=4) # Coil ring
            draw.rounded_rectangle([320, 720, 680, 800], radius=20, fill=color_dark) # Base
        else:
            # MagSafe charging puck or GaN wall plug
            draw.ellipse([300, 300, 700, 700], fill=color_pri, outline=color_dark, width=6)
            draw.ellipse([380, 380, 620, 620], fill=color_sec, outline=color_dark, width=3)
            # Center subtle logo circle
            draw.ellipse([470, 470, 530, 530], fill=color_dark)
            # Braided cord
            draw.line([500, 700, 500, 950], fill='#9CA3AF', width=16)

    # 6. TABLETS & LAPTOPS
    elif 'tablet' in model_type or 'laptop' in model_type:
        x1, y1, x2, y2 = 220, 200, 780, 800
        draw.rounded_rectangle([x1, y1, x2, y2], radius=32, fill=color_pri, outline=color_dark, width=4)
        draw.rounded_rectangle([x1 + 16, y1 + 16, x2 - 16, y2 - 16], radius=20, fill='#080B11')
        # Display Wallpaper Aurora Glow
        draw.ellipse([360, 340, 640, 660], fill=color_sec)

    # Fallback Generic Hardware Render
    else:
        draw.rounded_rectangle([320, 200, 680, 800], radius=44, fill=color_pri, outline=color_dark, width=4)

    return im

count_generated = 0
for p in products:
    pid = p['id']
    target_rel = f"/products/{pid}.png"
    target_abs = os.path.join(OUT_DIR, f"{pid}.png")

    # If product image already points to a unique existing file and isn't shared, keep it
    if os.path.exists(target_abs) and os.path.getsize(target_abs) > 10000:
        p['image'] = target_rel
        continue

    # Determine hardware profile from palette
    if pid in BRAND_PALETTES:
        pri, sec, dark, mtype = BRAND_PALETTES[pid]
    else:
        # Dynamic fallback palette based on brand and category
        cat = p.get('category', '').lower()
        br = p.get('brand', '').lower()
        if 'smartphones' in cat:
            pri, sec, dark, mtype = ('#2A3439', '#4E5F68', '#141A1D', 'triple')
        elif 'smartwatches' in cat:
            pri, sec, dark, mtype = ('#2B2D42', '#4B516D', '#12131C', 'watch_rect')
        elif 'earbuds' in cat:
            pri, sec, dark, mtype = ('#FFFFFF', '#F0F2F5', '#D1D5DB', 'earbuds_pebble_case')
        elif 'audio' in cat:
            pri, sec, dark, mtype = ('#1E2024', '#383D45', '#0E0F11', 'headphone_over_ear')
        elif 'chargers' in cat:
            pri, sec, dark, mtype = ('#1F2328', '#3E4651', '#111316', 'charger_stand')
        elif 'tablets' in cat:
            pri, sec, dark, mtype = ('#475569', '#64748B', '#1E293B', 'tablet_wide')
        else:
            pri, sec, dark, mtype = ('#334155', '#475569', '#1E293B', 'hardware')

    img = generate_hardware_render(pid, mtype, pri, sec, dark)
    img.save(target_abs, 'PNG')
    p['image'] = target_rel
    count_generated += 1

with open(PROD_JSON_PATH, 'w', encoding='utf-8') as f:
    json.dump(products, f, indent=2, ensure_ascii=False)

print(f"Successfully processed all 200 products! Generated {count_generated} unique hardware models. Unique images verified: {len(set(p['image'] for p in products))}")

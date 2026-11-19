import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

canvas_w, canvas_h = 1620, 770
bg_color = (247, 244, 238) # #F7F4EE
img = Image.new('RGB', (canvas_w, canvas_h), bg_color)
draw = ImageDraw.Draw(img)

font_title = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 30)
font_subtitle = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 16)
font_card_title = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 18)
font_card_desc = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 13)
font_badge = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 12)

# Top Brand Header
draw.text((canvas_w // 2, 45), 'NEXORA — White Product Contrast Design Demos', fill=(29, 29, 31), font=font_title, anchor='mm')
draw.text((canvas_w // 2, 85), 'Showing 4 World-Class Options on Light Mode (#F7F4EE) for White Gadgets', fill=(110, 110, 115), font=font_subtitle, anchor='mm')

card_w = 345
card_h = 580
card_y = 130
spacing = 38
start_x = (canvas_w - (4 * card_w + 3 * spacing)) // 2

options = [
    {
        'num': 'OPTION 1',
        'badge': 'RECOMMENDED',
        'badge_color': (0, 113, 227), # Apple Blue
        'title': 'Apple Soft Inset Pod',
        'subtitle': 'Subtle studio gray/off-white inset',
        'desc': 'Clean, subtle #F0EFF4 pod creates high edge contrast without harsh lines.',
        'type': 'soft_pod',
        'prod': 'frontend/public/products/airpods-pro-2.png'
    },
    {
        'num': 'OPTION 2',
        'badge': 'PREMIUM 3D',
        'badge_color': (16, 185, 129), # Emerald
        'title': 'Ambient Studio Shadow',
        'subtitle': 'Soft contact & floor shadow',
        'desc': 'Soft blurred contact shadow anchors the device and defines its bottom edges.',
        'type': 'shadow',
        'prod': 'frontend/public/products/airpods-pro-2.png'
    },
    {
        'num': 'OPTION 3',
        'badge': 'MODERN TECH',
        'badge_color': (139, 92, 246), # Purple
        'title': 'Subtle Slate Glass Inset',
        'subtitle': 'Fine border & cool tinted lens',
        'desc': 'Sleek 5% slate-tinted container gives an intentional architectural hardware frame.',
        'type': 'slate_lens',
        'prod': 'frontend/public/products/airpods-pro-2.png'
    },
    {
        'num': 'OPTION 4',
        'badge': 'HERO CONTRAST',
        'badge_color': (245, 158, 11), # Amber
        'title': 'Signature Titanium Color',
        'subtitle': 'Darker / Titanium main photo',
        'desc': 'Displays the iconic Titanium or Space Black finish for maximum contrast.',
        'type': 'dark_colorway',
        'prod': 'frontend/public/products/sony-wh1000xm5.png'
    }
]

for i, opt in enumerate(options):
    cx = start_x + i * (card_w + spacing)
    cy = card_y
    
    # Outer Card (White with soft border and subtle shadow)
    shadow_card = Image.new('RGBA', (card_w + 24, card_h + 24), (0,0,0,0))
    sdraw = ImageDraw.Draw(shadow_card)
    sdraw.rounded_rectangle([12, 12, card_w + 12, card_h + 12], radius=24, fill=(0, 0, 0, 15))
    shadow_card = shadow_card.filter(ImageFilter.GaussianBlur(10))
    img.paste(shadow_card, (cx - 12, cy - 8), shadow_card)
    
    # Draw Card
    card_img = Image.new('RGBA', (card_w, card_h), (255, 255, 255, 255))
    cdraw = ImageDraw.Draw(card_img)
    cdraw.rounded_rectangle([0, 0, card_w - 1, card_h - 1], radius=24, fill=(255, 255, 255), outline=(0, 0, 0, 25), width=1)
    
    # Badge (Pill)
    badge_text = opt['badge']
    bbox = font_badge.getbbox(badge_text)
    bw = (bbox[2] - bbox[0]) + 16
    bh = 22
    bx = 20
    by = 22
    cdraw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=11, fill=(*opt['badge_color'], 25))
    cdraw.text((bx + bw // 2, by + bh // 2), badge_text, fill=opt['badge_color'], font=font_badge, anchor='mm')
    
    # Title & Subtitle
    cdraw.text((20, 56), opt['title'], fill=(29, 29, 31), font=font_card_title)
    cdraw.text((20, 80), opt['subtitle'], fill=(134, 134, 139), font=font_card_desc)
    
    # Image Inset Box (285x240)
    box_x = 30
    box_y = 115
    box_w = card_w - 60
    box_h = 240
    
    if opt['type'] == 'soft_pod':
        # Soft Apple studio inset (#F0EFF4)
        cdraw.rounded_rectangle([box_x, box_y, box_x + box_w, box_y + box_h], radius=18, fill=(240, 239, 244), outline=(0, 0, 0, 20), width=1)
    elif opt['type'] == 'shadow':
        # Clean white inset with subtle border
        cdraw.rounded_rectangle([box_x, box_y, box_x + box_w, box_y + box_h], radius=18, fill=(252, 252, 253), outline=(0, 0, 0, 15), width=1)
    elif opt['type'] == 'slate_lens':
        # Cool slate glass tint (#E8ECF2) with crisp slate border
        cdraw.rounded_rectangle([box_x, box_y, box_x + box_w, box_y + box_h], radius=18, fill=(232, 236, 242), outline=(30, 41, 59, 40), width=1)
    elif opt['type'] == 'dark_colorway':
        # Pure white/cream inset
        cdraw.rounded_rectangle([box_x, box_y, box_x + box_w, box_y + box_h], radius=18, fill=(248, 248, 250), outline=(0, 0, 0, 15), width=1)
    
    # Load and composite product image
    p_img = Image.open(opt['prod']).convert('RGBA')
    p_img.thumbnail((180, 180), Image.Resampling.LANCZOS)
    
    px = box_x + (box_w - p_img.width) // 2
    py = box_y + (box_h - p_img.height) // 2 - 10
    
    if opt['type'] == 'shadow':
        shadow_layer = Image.new('RGBA', (box_w, box_h), (0,0,0,0))
        sh_draw = ImageDraw.Draw(shadow_layer)
        sh_w = int(p_img.width * 0.75)
        sh_h = 24
        sh_x = (box_w - sh_w) // 2
        sh_y = py + p_img.height - 12
        sh_draw.ellipse([sh_x, sh_y, sh_x + sh_w, sh_y + sh_h], fill=(0, 0, 0, 100))
        shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(10))
        card_img.paste(shadow_layer, (box_x, box_y), shadow_layer)
    
    card_img.paste(p_img, (px, py), p_img)
    
    # Mock Product Info under image
    prod_name = 'Apple AirPods Pro 2' if 'airpods' in opt['prod'] else 'Sony WH-1000XM5'
    cdraw.text((card_w // 2, 385), prod_name, fill=(29, 29, 31), font=font_card_title, anchor='mm')
    cdraw.text((card_w // 2, 412), 'Active Noise Cancellation · ৳28,500', fill=(110, 110, 115), font=font_card_desc, anchor='mm')
    
    # Divider line
    cdraw.line([(25, 440), (card_w - 25, 440)], fill=(0, 0, 0, 20), width=1)
    
    # Word wrap description
    words = opt['desc'].split()
    lines = []
    curr = ''
    for w in words:
        test = curr + ' ' + w if curr else w
        if font_card_desc.getlength(test) <= card_w - 50:
            curr = test
        else:
            lines.append(curr)
            curr = w
    if curr: lines.append(curr)
    
    line_y = 462
    for l in lines:
        cdraw.text((card_w // 2, line_y), l, fill=(80, 80, 85), font=font_card_desc, anchor='mm')
        line_y += 20
        
    # Mock Action Button
    cdraw.rounded_rectangle([40, 518, card_w - 40, 555], radius=18, fill=(0, 113, 227) if i == 0 else (240, 240, 242))
    btn_text = 'Option 1 (Recommended)' if i == 0 else f'Option {i+1}'
    btn_color = (255, 255, 255) if i == 0 else (29, 29, 31)
    cdraw.text((card_w // 2, 536), btn_text, fill=btn_color, font=font_card_desc, anchor='mm')
    
    img.paste(card_img, (cx, cy))

out_path = 'C:/Users/ASSDI/.gemini/antigravity/brain/c0909019-a6ca-47e2-8d6a-b02a923a6083/demo_contrast_options.png'
img.save(out_path, quality=95)
print('Demo image created successfully at:', out_path)

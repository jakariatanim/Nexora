import os
from PIL import Image, ImageDraw

public_dir = r"d:\Anti Gravity Project\Website\Nexora\frontend\public"
brand_icon_path = os.path.join(public_dir, "brand", "nexora_icon_white_transparent.png")

if not os.path.exists(brand_icon_path):
    brand_icon_path = os.path.join(public_dir, "brand", "nexora_icon_transparent.png")

logo = Image.open(brand_icon_path).convert("RGBA")

def create_pwa_icon(size, output_path, padding_percent=0.22, bg_color=(11, 19, 43, 255)):
    # Create canvas
    canvas = Image.new("RGBA", (size, size), bg_color)
    
    # Calculate inner size
    inner_size = int(size * (1 - padding_percent * 2))
    resized_logo = logo.copy()
    resized_logo.thumbnail((inner_size, inner_size), Image.Resampling.LANCZOS)
    
    # Center position
    pos_x = (size - resized_logo.width) // 2
    pos_y = (size - resized_logo.height) // 2
    
    canvas.paste(resized_logo, (pos_x, pos_y), resized_logo)
    canvas.save(output_path, "PNG")
    print(f"Generated {output_path} ({size}x{size})")

# 1. 192x192
create_pwa_icon(192, os.path.join(public_dir, "icon-192.png"))

# 2. 512x512
create_pwa_icon(512, os.path.join(public_dir, "icon-512.png"))

# 3. Maskable 512x512 (with slightly larger padding to be safe-zone compliant)
create_pwa_icon(512, os.path.join(public_dir, "icon-maskable-512.png"), padding_percent=0.28)

# 4. Apple Touch Icon 180x180
create_pwa_icon(180, os.path.join(public_dir, "apple-touch-icon.png"), padding_percent=0.20)

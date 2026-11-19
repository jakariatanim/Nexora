import os
import re

brands_dir = r"d:\Anti Gravity Project\Website\Nexora\frontend\public\brands"

# Let's check each svg
viewbox_updates = {
    "samsung.svg": "-0.5 9.7 25.0 4.7",
    "sony.svg": "-0.5 9.4 25.0 5.2",
    "oppo.svg": "-0.5 8.6 25.0 6.7",
    "vivo.svg": "-0.5 8.3 25.0 7.3",
}

for fname, vb in viewbox_updates.items():
    fpath = os.path.join(brands_dir, fname)
    if os.path.exists(fpath):
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Replace viewBox
        new_content = re.sub(r'viewBox="[^"]*"', f'viewBox="{vb}"', content)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Updated {fname} with viewBox: {vb}")

# Check realme and anker
for check_f in ["realme.svg", "anker.svg", "google.svg"]:
    fpath = os.path.join(brands_dir, check_f)
    if os.path.exists(fpath):
        with open(fpath, "r", encoding="utf-8") as f:
            c = f.read()
        vb = re.search(r'viewBox="([^"]*)"', c)
        print(f"{check_f} viewBox:", vb.group(1) if vb else "None")

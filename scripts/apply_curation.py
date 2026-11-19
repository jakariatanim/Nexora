import json

with open("backend/data/products.json.bak", "r", encoding="utf-8") as f:
    all_products = json.load(f)

# The curated list of exact product IDs
CURATED_IDS = [
    # --- Apple ---
    "iphone-18-pro-max",
    "apple-iphone-16-pro-max",
    "apple-iphone-16-pro",
    "apple-iphone-15-pro-max",
    "ipad-pro-m4",
    "macbook-pro-16-m3-max",
    "apple-watch-ultra-2",
    "apple-watch-series-10",
    "airpods-pro-2",
    "apple-airpods-4-anc",
    "airpods-max",
    "apple-magsafe-duo",
    "apple-35w-dual-adapter",

    # --- Samsung ---
    "samsung-s24-ultra",
    "galaxy-z-fold-6",
    "samsung-galaxy-z-flip-6",
    "samsung-galaxy-s24-plus",
    "samsung-galaxy-tab-s9-ultra",
    "samsung-galaxy-watch-ultra",
    "samsung-galaxy-watch-7",
    "samsung-galaxy-buds3-pro",
    "samsung-galaxy-buds2-pro",
    "samsung-wireless-trio",
    "samsung-45w-power-adapter",

    # --- Xiaomi ---
    "xiaomi-14-ultra",
    "xiaomi-14",
    "xiaomi-14t-pro",
    "xiaomi-pad-6s-pro",
    "xiaomi-watch-2-pro",
    "xiaomi-watch-s3",
    "xiaomi-buds-5",
    "xiaomi-120w-hypercharge-adapter",
    "xiaomi-22-5w-power-bank",

    # --- Google ---
    "pixel-9-pro-xl",
    "google-pixel-9-pro",
    "google-pixel-9-pro-fold",
    "google-pixel-tablet",
    "google-pixel-watch-3-45",
    "google-pixel-watch-2",
    "google-pixel-buds-pro-2",
    "google-pixel-stand-2",
    "google-45w-usb-c-charger",

    # --- OnePlus ---
    "oneplus-12",
    "oneplus-open",
    "oneplus-12r",
    "oneplus-pad-2",
    "oneplus-watch-2",
    "oneplus-buds-pro-3",
    "oneplus-supervooc-100w-gan",
    "oneplus-22-5w-power-bank",

    # --- Oppo ---
    "oppo-find-x7-ultra",
    "oppo-find-n3",
    "oppo-pad-2",
    "oppo-watch-x",
    "oppo-enco-x3",
    "oppo-100w-supervooc-gan-charger",
    "oppo-33w-power-bank-10000",

    # --- Vivo ---
    "vivo-x100-ultra",
    "vivo-x-fold-3-pro",
    "vivo-pad-3-pro",
    "vivo-watch-3",
    "vivo-tws-4-hifi",
    "vivo-120w-flashcharge-gan-adapter",
    "vivo-66w-power-bank-20000",

    # --- Realme ---
    "realme-gt-6",
    "realme-13-pro-plus",
    "realme-pad-2",
    "realme-watch-s2",
    "realme-buds-air-6-pro",
    "realme-120w-ultradart-charger",
    "realme-30w-dart-power-bank",

    # --- Anker ---
    "anker-maggo-qi2-cube",
    "anker-maggo-qi2-powerbank",
    "anker-prime-20000-powerbank",
    "anker-prime-240w-desktop-station",
    "anker-737-powerbank",
    "anker-soundcore-liberty-4-nc",

    # --- Sony ---
    "sony-xperia-1-vi",
    "sony-wh1000xm5",
    "sony-wh-ult900n",
    "sony-wf1000xm5",
    "sony-cp-v10b-powerbank"
]

prod_dict = {p["id"]: p for p in all_products}

curated_list = []
missing_ids = []

for pid in CURATED_IDS:
    if pid in prod_dict:
        p = prod_dict[pid]
        # Ensure category is NOT Cases & Accessories
        if p.get("category") == "Cases & Accessories":
            continue
        curated_list.append(p)
    else:
        missing_ids.append(pid)

print(f"Total curated: {len(curated_list)}")
if missing_ids:
    print(f"Missing IDs: {missing_ids}")

# Verify brand and category counts
brand_counts = {}
cat_counts = {}
for p in curated_list:
    b = p.get("brand", "Unknown")
    c = p.get("category", "Unknown")
    brand_counts[b] = brand_counts.get(b, 0) + 1
    cat_counts[c] = cat_counts.get(c, 0) + 1

print("\nBrand breakdown:")
for b, c in brand_counts.items():
    print(f"  {b}: {c}")

print("\nCategory breakdown:")
for cat, count in cat_counts.items():
    print(f"  {cat}: {count}")

with open("backend/data/products.json", "w", encoding="utf-8") as f:
    json.dump(curated_list, f, indent=2, ensure_ascii=False)

print("\nSuccessfully updated backend/data/products.json!")

import json
import shutil

# Make backup first
shutil.copyfile("backend/data/products.json", "backend/data/products.json.bak")

with open("backend/data/products.json", "r", encoding="utf-8") as f:
    products = json.load(f)

# The user explicitly asked:
# 1. Drop "Cases & Accessories" category completely!
# 2. Curate 2-3 top flagship smartphones per brand (or 3-4 for top brands Apple, Samsung, Google, Xiaomi; 2 for others).
# 3. Earbuds: top 1-2 per brand.
# 4. Chargers & Power: top GaN fast chargers + power banks (Anker, Apple, Samsung, Xiaomi, Google, OnePlus, Sony, Realme).
# 5. Audio, Smartwatches, Tablets & Laptops: keep only top flagship devices.
# Total curated catalog: ~50-60 top-tier gadgets.

CURATED_PRODUCT_IDS = {
    # Apple (Flagships across categories)
    "iphone-18-pro-max",
    "apple-iphone-16-pro-max",
    "apple-iphone-16-pro",
    "apple-iphone-15-pro-max",
    "ipad-pro-m4",
    "macbook-pro-16",
    "apple-watch-ultra-2",
    "apple-watch-series-10",
    "airpods-pro-2",
    "apple-airpods-4",
    "airpods-max",
    "apple-magsafe-duo",
    "apple-35w-dual-gan",
    "apple-magsafe-battery-pack",

    # Samsung (Flagships)
    "samsung-s24-ultra",
    "galaxy-z-fold-6",
    "galaxy-z-flip-6",
    "samsung-galaxy-s24-plus",
    "galaxy-tab-s9-ultra",
    "galaxy-watch-ultra",
    "samsung-galaxy-watch-7",
    "galaxy-buds-3-pro",
    "samsung-galaxy-buds-fe",
    "samsung-45w-trio",
    "samsung-wireless-powerbank-10k",

    # Xiaomi (Flagships)
    "xiaomi-14-ultra",
    "xiaomi-14-pro",
    "xiaomi-mix-fold-3",
    "xiaomi-pad-6-max",
    "xiaomi-watch-s3",
    "xiaomi-buds-5-pro",
    "xiaomi-120w-hypercharge",
    "xiaomi-50w-wireless-powerbank",

    # Google (Flagships)
    "google-pixel-9-pro-xl",
    "google-pixel-9-pro",
    "google-pixel-9-pro-fold",
    "pixel-watch-3",
    "pixel-buds-pro-2",
    "google-45w-usbc-gan",
    "google-pixel-stand-2",

    # OnePlus (Flagships)
    "oneplus-12",
    "oneplus-open",
    "oneplus-12r",
    "oneplus-watch-2",
    "oneplus-buds-pro-3",
    "oneplus-supervooc-100w",
    "oneplus-80w-powerbank",

    # Oppo (Flagships)
    "oppo-find-x7-ultra",
    "oppo-find-n3",
    "oppo-enco-x3-pro",
    "oppo-supervooc-80w",
    "oppo-33w-powerbank",

    # Vivo (Flagships)
    "vivo-x100-ultra",
    "vivo-x-fold-3-pro",
    "vivo-tws-4-hifi",
    "vivo-flashcharge-120w",
    "vivo-44w-wireless-powerbank",

    # Realme (Flagships)
    "realme-gt-6",
    "realme-gt5-pro",
    "realme-buds-air-6-pro",
    "realme-150w-ultradart-gan",
    "realme-10000mah-powerbank",

    # Anker (Charging & Audio Specialists)
    "anker-prime-240w",
    "anker-maggo-qi2-cube",
    "anker-737-powerbank",
    "anker-maggo-10k-qi2-powerbank",
    "anker-prime-20k-200w-powerbank",
    "anker-100w-gan-wall",
    "anker-soundcore-liberty-4-pro",
    "anker-soundcore-space-one-pro",

    # Sony (Audio, Headphones & Xperia Flagship)
    "sony-wh-1000xm5",
    "sony-wh-ult900n",
    "sony-wf-1000xm5",
    "sony-xperia-1-vi",
    "sony-cp-v10a-powerbank"
}

# Match products from existing list
curated = []
seen_ids = set()

# First, any product in our curated set that exists in products.json
prod_by_id = {p["id"]: p for p in products}

for pid in CURATED_PRODUCT_IDS:
    if pid in prod_by_id:
        p = prod_by_id[pid]
        # Never include Cases & Accessories
        if p.get("category") == "Cases & Accessories":
            continue
        curated.append(p)
        seen_ids.add(pid)

# If any ID had slight slug mismatch, let's search by name
for p in products:
    pid = p["id"]
    if pid in seen_ids:
        continue
    if p.get("category") == "Cases & Accessories":
        continue
    # Check if it matches any curated keywords
    name_lower = p["name"].lower()
    cat = p.get("category", "")
    brand = p.get("brand", "")
    
    # If we need to fill top items
    if brand in ["Apple", "Samsung", "Google", "Xiaomi", "OnePlus", "Oppo", "Vivo", "Realme", "Anker", "Sony"]:
        # Check if it's a power bank
        if "power bank" in name_lower or "powerbank" in name_lower or "battery" in name_lower:
            p["category"] = "Chargers & Power"
            curated.append(p)
            seen_ids.add(pid)

print(f"Curated {len(curated)} premium flagship products.")

# Verify category counts
cat_counts = {}
for p in curated:
    c = p.get("category", "Unknown")
    cat_counts[c] = cat_counts.get(c, 0) + 1

print("Curated category distribution:", cat_counts)

# Save back to backend/data/products.json
with open("backend/data/products.json", "w", encoding="utf-8") as f:
    json.dump(curated, f, indent=2, ensure_ascii=False)

print("Saved curated catalog to backend/data/products.json successfully.")

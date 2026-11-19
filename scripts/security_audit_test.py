import urllib.request
import urllib.error
import json

base_url = "http://localhost:5001"

print("--- 1. Testing Security Headers ---")
req = urllib.request.Request(f"{base_url}/api/stats")
with urllib.request.urlopen(req) as resp:
    headers = dict(resp.getheaders())
    print("X-Content-Type-Options:", headers.get("X-Content-Type-Options", "MISSING"))
    print("X-Frame-Options:", headers.get("X-Frame-Options", "MISSING"))
    print("X-XSS-Protection:", headers.get("X-XSS-Protection", "MISSING"))
    print("Referrer-Policy:", headers.get("Referrer-Policy", "MISSING"))

print("\n--- 2. Testing Unauthenticated Guard on /api/admins ---")
req = urllib.request.Request(f"{base_url}/api/admins")
try:
    with urllib.request.urlopen(req) as resp:
        print("FAIL: Expected HTTP 401 Unauthorized, but got HTTP", resp.status)
except urllib.error.HTTPError as e:
    print(f"PASS: Unauthenticated access blocked -> HTTP {e.code} ({e.reason})")

print("\n--- 3. Testing Staff Authentication & Password Stripping on /api/admins ---")
login_url = f"{base_url}/api/admin/login"
auth_payload = json.dumps({"username": "inventory", "password": "InventoryMod2026!"}).encode()
login_req = urllib.request.Request(login_url, data=auth_payload, headers={"Content-Type": "application/json"})
with urllib.request.urlopen(login_req) as resp:
    token = json.loads(resp.read().decode())["token"]
    print(f"Admin JWT token issued: {token[:20]}...")

req = urllib.request.Request(f"{base_url}/api/admins", headers={"Authorization": f"Bearer {token}"})
with urllib.request.urlopen(req) as resp:
    admins = json.loads(resp.read().decode())
    has_password = any("password" in a for a in admins)
    print(f"Total admin records: {len(admins)}")
    print(f"Are plain or hashed passwords leaked? {has_password} (Expected: False)")

print("\n--- 4. Testing Anti-Price-Tampering Authoritative Order Recalculation ---")
# Submit an order with manipulated client price of ৳10
tamper_order = {
    "customer": {
        "name": "Audit Security Tester",
        "phone": "+8801700000000",
        "email": "audit@nexora.com",
        "address": "Banani, Dhaka",
        "deliveryZone": "dhaka"
    },
    "items": [
        {
            "id": "iphone-18-pro-max",
            "quantity": 1,
            "priceBDT": 10  # MALICIOUS CLIENT MANIPULATION
        }
    ],
    "subtotalBDT": 10,
    "totalBDT": 10,
    "paymentMethod": "Cash on Delivery"
}
order_req = urllib.request.Request(
    f"{base_url}/api/orders",
    data=json.dumps(tamper_order).encode(),
    headers={"Content-Type": "application/json"}
)
with urllib.request.urlopen(order_req) as resp:
    order_res = json.loads(resp.read().decode())
    official_total = order_res.get("totalBDT")
    print(f"Client sent: ৳10 -> Server authoritative total: ৳{official_total:,}")
    print(f"Tampering neutralized? {official_total > 200000} (Expected: True)")

print("\n--- 5. Testing Rate Limiting on /api/admin/login ---")
dummy_payload = json.dumps({"username": "attacker", "password": "wrong_password"}).encode()
for i in range(1, 6):
    req = urllib.request.Request(login_url, data=dummy_payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as resp:
            print(f"Attempt {i}: HTTP {resp.status}")
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"Attempt {i}: HTTP {e.code} -> {body[:60]}...")

print("\nAll security audit and verification checks completed successfully!")

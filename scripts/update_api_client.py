# -*- coding: utf-8 -*-
with open("frontend/src/lib/api.ts", "r", encoding="utf-8") as f:
    code = f.read()

# Add getAuthHeaders right after API_BASE
old_header = "const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5001/api';"
new_header = """const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5001/api';

function getAuthHeaders(extra: Record<string, string> = {}): HeadersInit {
  const token = typeof window !== 'undefined' ? localStorage.getItem('nexora_admin_token') : null;
  return {
    'Content-Type': 'application/json',
    ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
    ...extra,
  };
}"""

code = code.replace(old_header, new_header, 1)

# In createProduct
code = code.replace(
    "headers: { 'Content-Type': 'application/json' },\n      body: JSON.stringify(product),",
    "headers: getAuthHeaders(),\n      body: JSON.stringify(product),",
    1
)

# In updateProduct
code = code.replace(
    "headers: { 'Content-Type': 'application/json' },\n      body: JSON.stringify(updates),",
    "headers: getAuthHeaders(),\n      body: JSON.stringify(updates),",
    1
)

# In deleteProduct
code = code.replace(
    "fetch(`${API_BASE}/products/${id}`, { method: 'DELETE' });",
    "fetch(`${API_BASE}/products/${id}`, { method: 'DELETE', headers: getAuthHeaders() });",
    1
)

# In uploadImage
old_upload = """    const res = await fetch(`${API_BASE}/upload`, {
      method: 'POST',
      body: formData,
    });"""
new_upload = """    const token = typeof window !== 'undefined' ? localStorage.getItem('nexora_admin_token') : null;
    const res = await fetch(`${API_BASE}/upload`, {
      method: 'POST',
      headers: token ? { 'Authorization': `Bearer ${token}` } : {},
      body: formData,
    });"""
code = code.replace(old_upload, new_upload, 1)

# In fetchOrders
code = code.replace(
    "fetch(`${API_BASE}/orders`, { cache: 'no-store' });",
    "fetch(`${API_BASE}/orders`, { cache: 'no-store', headers: getAuthHeaders() });",
    1
)

# In updateOrderStatus
code = code.replace(
    "headers: { 'Content-Type': 'application/json' },\n      body: JSON.stringify({ status }),",
    "headers: getAuthHeaders(),\n      body: JSON.stringify({ status }),",
    1
)

# In deleteReview
code = code.replace(
    "fetch(`${API_BASE}/reviews/${id}`, { method: 'DELETE' });",
    "fetch(`${API_BASE}/reviews/${id}`, { method: 'DELETE', headers: getAuthHeaders() });",
    1
)

# In updateFounder
code = code.replace(
    "headers: { 'Content-Type': 'application/json' },\n      body: JSON.stringify(data),",
    "headers: getAuthHeaders(),\n      body: JSON.stringify(data),",
    1
)

# In fetchAdminMembers
code = code.replace(
    "fetch(`${API_BASE}/admins`, { cache: 'no-store' });",
    "fetch(`${API_BASE}/admins`, { cache: 'no-store', headers: getAuthHeaders() });",
    1
)

# In createAdminMember
code = code.replace(
    "headers: { 'Content-Type': 'application/json' },\n      body: JSON.stringify(member),",
    "headers: getAuthHeaders(),\n      body: JSON.stringify(member),",
    1
)

# In updateAdminMember
code = code.replace(
    "headers: { 'Content-Type': 'application/json' },\n      body: JSON.stringify(updates),",
    "headers: getAuthHeaders(),\n      body: JSON.stringify(updates),",
    1
)

# In deleteAdminMember
code = code.replace(
    "fetch(`${API_BASE}/admins/${id}`, { method: 'DELETE' });",
    "fetch(`${API_BASE}/admins/${id}`, { method: 'DELETE', headers: getAuthHeaders() });",
    1
)

# In fetchClaims
code = code.replace(
    "fetch(`${API_BASE}/claims`, { cache: 'no-store' });",
    "fetch(`${API_BASE}/claims`, { cache: 'no-store', headers: getAuthHeaders() });",
    1
)

# In updateClaimStatus
code = code.replace(
    "headers: { 'Content-Type': 'application/json' },\n      body: JSON.stringify({ status }),",
    "headers: getAuthHeaders(),\n      body: JSON.stringify({ status }),",
    1
)

# In fetchDetailedAnalytics
code = code.replace(
    "fetch(`${API_BASE}/admin/analytics`, { cache: 'no-store' });",
    "fetch(`${API_BASE}/admin/analytics`, { cache: 'no-store', headers: getAuthHeaders() });",
    1
)

# In fetchCoupons
code = code.replace(
    "fetch(`${API_BASE}/coupons`, { cache: 'no-store' });",
    "fetch(`${API_BASE}/coupons`, { cache: 'no-store', headers: getAuthHeaders() });",
    1
)

# In createCoupon
code = code.replace(
    "headers: { 'Content-Type': 'application/json' },\n      body: JSON.stringify(coupon),",
    "headers: getAuthHeaders(),\n      body: JSON.stringify(coupon),",
    1
)

# In updateCoupon
code = code.replace(
    "headers: { 'Content-Type': 'application/json' },\n      body: JSON.stringify(updates),",
    "headers: getAuthHeaders(),\n      body: JSON.stringify(updates),",
    1
)

# In deleteCoupon
code = code.replace(
    "fetch(`${API_BASE}/coupons/${id}`, {\n      method: 'DELETE',\n    });",
    "fetch(`${API_BASE}/coupons/${id}`, {\n      method: 'DELETE',\n      headers: getAuthHeaders(),\n    });",
    1
)

with open("frontend/src/lib/api.ts", "w", encoding="utf-8") as f:
    f.write(code)

print("Updated frontend/src/lib/api.ts with auth token headers")

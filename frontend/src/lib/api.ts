import { Product, Order, Review, Founder, AdminMember, User, Coupon, Claim, Category } from './types';
import defaultProducts from '../data/products.json';
import defaultCategories from '../data/categories.json';
import defaultReviews from '../data/reviews.json';
import defaultFounder from '../data/founder.json';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5001/api';

function getAuthHeaders(extra: Record<string, string> = {}): HeadersInit {
  const token = typeof window !== 'undefined' ? localStorage.getItem('nexora_admin_token') : null;
  return {
    'Content-Type': 'application/json',
    ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
    ...extra,
  };
}

export async function fetchProducts(): Promise<Product[]> {
  try {
    const res = await fetch(`${API_BASE}/products`, { cache: 'no-store' });
    if (!res.ok) throw new Error('Failed to fetch products');
    const data = await res.json();
    return Array.isArray(data) && data.length > 0 ? data : (defaultProducts as unknown as Product[]);
  } catch (err) {
    return defaultProducts as unknown as Product[];
  }
}

export async function fetchProductById(id: string): Promise<Product | null> {
  const products = await fetchProducts();
  return products.find(p => p.id === id) || null;
}

export async function createProduct(product: Partial<Product>): Promise<Product | null> {
  try {
    const res = await fetch(`${API_BASE}/products`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(product),
    });
    if (!res.ok) return null;
    return await res.json();
  } catch (err) {
    console.error('Error creating product:', err);
    return null;
  }
}

export async function updateProduct(id: string, updates: Partial<Product>): Promise<Product | null> {
  try {
    const res = await fetch(`${API_BASE}/products/${id}`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(updates),
    });
    if (!res.ok) return null;
    return await res.json();
  } catch (err) {
    console.error('Error updating product:', err);
    return null;
  }
}

export async function deleteProduct(id: string): Promise<boolean> {
  try {
    const res = await fetch(`${API_BASE}/products/${id}`, { method: 'DELETE', headers: getAuthHeaders() });
    return res.ok;
  } catch (err) {
    console.error('Error deleting product:', err);
    return false;
  }
}

export async function uploadImage(file: File): Promise<string | null> {
  try {
    const formData = new FormData();
    formData.append('image', file);
    const token = typeof window !== 'undefined' ? localStorage.getItem('nexora_admin_token') : null;
    const res = await fetch(`${API_BASE}/upload`, {
      method: 'POST',
      headers: token ? { 'Authorization': `Bearer ${token}` } : {},
      body: formData,
    });
    const data = await res.json();
    return data.url || null;
  } catch (err) {
    console.error('Error uploading image:', err);
    return null;
  }
}

export async function fetchOrders(): Promise<Order[]> {
  try {
    const res = await fetch(`${API_BASE}/orders`, { cache: 'no-store', headers: getAuthHeaders() });
    if (!res.ok) throw new Error('Failed to fetch orders');
    return await res.json();
  } catch (err) {
    console.warn('API fetchOrders fallback:', err);
    return [];
  }
}

export async function createOrder(orderData: Partial<Order>): Promise<(Order & { error?: string }) | null> {
  try {
    const res = await fetch(`${API_BASE}/orders`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(orderData),
    });
    const data = await res.json();
    if (!res.ok) {
      return { error: data.error || 'Failed to place order' } as any;
    }
    return data;
  } catch (err) {
    console.error('Error creating order:', err);
    return { error: 'Network communication failure' } as any;
  }
}

export async function updateOrderStatus(orderId: string, status: string): Promise<Order | null> {
  try {
    const res = await fetch(`${API_BASE}/orders/${orderId}/status`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify({ status }),
    });
    return await res.json();
  } catch (err) {
    console.error('Error updating order status:', err);
    return null;
  }
}

export async function trackOrder(query: string): Promise<Order | null> {
  try {
    const res = await fetch(`${API_BASE}/orders/track/${encodeURIComponent(query)}`, { cache: 'no-store' });
    if (!res.ok) return null;
    return await res.json();
  } catch (err) {
    console.error('Error tracking order:', err);
    return null;
  }
}

export async function fetchReviews(): Promise<Review[]> {
  try {
    const res = await fetch(`${API_BASE}/reviews`, { cache: 'no-store' });
    if (!res.ok) throw new Error('Failed to fetch reviews');
    const data = await res.json();
    return Array.isArray(data) && data.length > 0 ? data : (defaultReviews as unknown as Review[]);
  } catch (err) {
    return defaultReviews as unknown as Review[];
  }
}

export async function submitReview(review: Partial<Review>): Promise<Review | null> {
  try {
    const res = await fetch(`${API_BASE}/reviews`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(review),
    });
    const data = await res.json();
    if (!res.ok || !data || !data.id) {
      if (typeof window !== 'undefined' && data && data.error) {
        alert(data.error);
      }
      return null;
    }
    return data;
  } catch (err) {
    console.error('Error submitting review:', err);
    return null;
  }
}

export async function deleteReview(id: string): Promise<boolean> {
  try {
    const res = await fetch(`${API_BASE}/reviews/${id}`, { method: 'DELETE', headers: getAuthHeaders() });
    return res.ok;
  } catch (err) {
    console.error('Error deleting review:', err);
    return false;
  }
}

export async function fetchFounder(): Promise<Founder | null> {
  try {
    const res = await fetch(`${API_BASE}/founder`, { cache: 'no-store' });
    if (!res.ok) throw new Error('Failed to fetch founder');
    return await res.json();
  } catch (err) {
    return defaultFounder as unknown as Founder;
  }
}

export async function updateFounder(data: Partial<Founder>): Promise<Founder | null> {
  try {
    const res = await fetch(`${API_BASE}/founder`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(data),
    });
    return await res.json();
  } catch (err) {
    console.error('Error updating founder:', err);
    return null;
  }
}

export async function fetchAdminMembers(): Promise<AdminMember[]> {
  try {
    const res = await fetch(`${API_BASE}/admins`, { cache: 'no-store', headers: getAuthHeaders() });
    if (!res.ok) throw new Error('Failed to fetch admin members');
    return await res.json();
  } catch (err) {
    console.warn('API fetchAdminMembers fallback:', err);
    return [];
  }
}

export async function createAdminMember(member: Partial<AdminMember>): Promise<AdminMember | null> {
  try {
    const res = await fetch(`${API_BASE}/admins`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(member),
    });
    return await res.json();
  } catch (err) {
    console.error('Error creating admin member:', err);
    return null;
  }
}

export async function updateAdminMember(id: string, updates: Partial<AdminMember>): Promise<AdminMember | null> {
  try {
    const res = await fetch(`${API_BASE}/admins/${id}`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(updates),
    });
    return await res.json();
  } catch (err) {
    console.error('Error updating admin member:', err);
    return null;
  }
}

export async function deleteAdminMember(id: string): Promise<boolean> {
  try {
    const res = await fetch(`${API_BASE}/admins/${id}`, { method: 'DELETE', headers: getAuthHeaders() });
    return res.ok;
  } catch (err) {
    console.error('Error deleting admin member:', err);
    return false;
  }
}

// ============================================================================
// Customer Authentication & Account Hub API
// ============================================================================
export async function loginCustomer(credential: string, password: string): Promise<{ success: boolean; user?: User; error?: string }> {
  try {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ credential, password }),
    });
    const data = await res.json();
    if (!res.ok) {
      return { success: false, error: data.error || 'Invalid credentials' };
    }
    return { success: true, user: data.user };
  } catch (err) {
    return { success: false, error: 'Connection to authentication service failed.' };
  }
}

export async function registerCustomer(payload: { name: string; email?: string; phone?: string; password: string }): Promise<{ success: boolean; user?: User; error?: string }> {
  try {
    const res = await fetch(`${API_BASE}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    if (!res.ok) {
      return { success: false, error: data.error || 'Registration failed' };
    }
    return { success: true, user: data.user };
  } catch (err) {
    return { success: false, error: 'Connection to authentication service failed.' };
  }
}

export async function socialCustomerSignIn(provider: 'google' | 'apple', email: string, name: string): Promise<{ success: boolean; user?: User; error?: string }> {
  try {
    const res = await fetch(`${API_BASE}/auth/social`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ provider, email, name }),
    });
    const data = await res.json();
    if (!res.ok) {
      return { success: false, error: data.error || 'Social authentication failed' };
    }
    return { success: true, user: data.user };
  } catch (err) {
    return { success: false, error: 'Social authentication service unavailable.' };
  }
}

export async function fetchUserOrders(phone?: string, email?: string): Promise<Order[]> {
  try {
    const params = new URLSearchParams();
    if (phone) params.set('phone', phone);
    if (email) params.set('email', email);
    const res = await fetch(`${API_BASE}/auth/orders?${params.toString()}`, { cache: 'no-store' });
    if (!res.ok) return [];
    const data = await res.json();
    return data.orders || [];
  } catch (err) {
    console.error('Error fetching user orders:', err);
    return [];
  }
}

// Coupons & Promo Codes
export async function validateCoupon(code: string, subtotal: number): Promise<{ success: boolean; coupon?: Coupon; error?: string }> {
  try {
    const res = await fetch(`${API_BASE}/coupons/validate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code, subtotal }),
    });
    const data = await res.json();
    if (!res.ok) {
      return { success: false, error: data.error || 'Invalid coupon code' };
    }
    return { success: true, coupon: data };
  } catch (err) {
    return { success: false, error: 'Coupon verification service unreachable' };
  }
}

// Warranty & Return Claims
export async function fetchClaims(): Promise<Claim[]> {
  try {
    const res = await fetch(`${API_BASE}/claims`, { cache: 'no-store', headers: getAuthHeaders() });
    if (!res.ok) return [];
    return await res.json();
  } catch (err) {
    console.error('Error fetching claims:', err);
    return [];
  }
}

export async function submitClaim(payload: Partial<Claim>): Promise<{ success: boolean; claim?: Claim; error?: string }> {
  try {
    const res = await fetch(`${API_BASE}/claims`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    if (!res.ok) {
      return { success: false, error: data.error || 'Failed to submit warranty ticket' };
    }
    return { success: true, claim: data.claim };
  } catch (err) {
    return { success: false, error: 'Connection to warranty claim server failed' };
  }
}

export async function updateClaimStatus(id: string, status: string): Promise<boolean> {
  try {
    const res = await fetch(`${API_BASE}/claims/${id}`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify({ status }),
    });
    return res.ok;
  } catch (err) {
    return false;
  }
}

// Store Analytics
export async function fetchDetailedAnalytics(): Promise<any> {
  try {
    const res = await fetch(`${API_BASE}/admin/analytics`, { cache: 'no-store', headers: getAuthHeaders() });
    if (!res.ok) return null;
    return await res.json();
  } catch (err) {
    console.error('Error fetching detailed analytics:', err);
    return null;
  }
}

// Coupons Management
export async function fetchCoupons(): Promise<Coupon[]> {
  try {
    const res = await fetch(`${API_BASE}/coupons`, { cache: 'no-store', headers: getAuthHeaders() });
    if (!res.ok) return [];
    return await res.json();
  } catch (err) {
    console.error('Error fetching coupons:', err);
    return [];
  }
}

export async function createCoupon(coupon: Partial<Coupon>): Promise<Coupon | null> {
  try {
    const res = await fetch(`${API_BASE}/coupons`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(coupon),
    });
    const data = await res.json();
    return (data && (data.coupon || (data.code ? data : null))) || null;
  } catch (err) {
    console.error('Error creating coupon:', err);
    return null;
  }
}

export async function updateCoupon(id: string, updates: Partial<Coupon>): Promise<Coupon | null> {
  try {
    const res = await fetch(`${API_BASE}/coupons/${id}`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(updates),
    });
    const data = await res.json();
    return (data && (data.coupon || (data.code ? data : null))) || null;
  } catch (err) {
    console.error('Error updating coupon:', err);
    return null;
  }
}

export async function deleteCoupon(id: string): Promise<boolean> {
  try {
    const res = await fetch(`${API_BASE}/coupons/${id}`, {
      method: 'DELETE',
      headers: getAuthHeaders(),
    });
    return res.ok;
  } catch (err) {
    console.error('Error deleting coupon:', err);
    return false;
  }
}

// Category Catalog Management
export async function fetchCategories(): Promise<Category[]> {
  try {
    const res = await fetch(`${API_BASE}/categories`, { cache: 'no-store' });
    if (!res.ok) return defaultCategories as unknown as Category[];
    const data = await res.json();
    return Array.isArray(data) && data.length > 0 ? data : (defaultCategories as unknown as Category[]);
  } catch (err) {
    return defaultCategories as unknown as Category[];
  }
}

export async function createCategory(cat: Partial<Category>): Promise<Category | null> {
  try {
    const res = await fetch(`${API_BASE}/categories`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(cat),
    });
    if (!res.ok) return null;
    return await res.json();
  } catch (err) {
    console.error('Error creating category:', err);
    return null;
  }
}

export async function deleteCategory(id: string): Promise<boolean> {
  try {
    const res = await fetch(`${API_BASE}/categories/${id}`, {
      method: 'DELETE',
      headers: getAuthHeaders(),
    });
    return res.ok;
  } catch (err) {
    console.error('Error deleting category:', err);
    return false;
  }
}

// Staff Invitation Activation
export async function activateAdminInvite(payload: {
  email?: string;
  username: string;
  password: string;
  role?: string;
  name?: string;
}): Promise<{ success: boolean; user?: any; error?: string }> {
  try {
    const res = await fetch(`${API_BASE}/admin/activate-invite`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    return { success: res.ok && data.success, user: data.user, error: data.error };
  } catch (err) {
    return { success: false, error: 'Network failure during account activation.' };
  }
}

// Admin Security & Password
export async function changeAdminPassword(payload: {
  id?: string;
  username?: string;
  currentPassword?: string;
  newPassword: string;
}): Promise<{ success: boolean; error?: string }> {
  try {
    const res = await fetch(`${API_BASE}/admin/change-password`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    return { success: res.ok && data.success, error: data.error };
  } catch (err) {
    return { success: false, error: 'Network failure communicating with admin auth service.' };
  }
}

export async function resetAdminPassword(payload: {
  username?: string;
  email?: string;
}): Promise<{ success: boolean; tempPassword?: string; error?: string }> {
  try {
    const res = await fetch(`${API_BASE}/admin/reset-password`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    return {
      success: res.ok && data.success,
      tempPassword: data.tempPassword,
      error: data.error,
    };
  } catch (err) {
    return { success: false, error: 'Network failure resetting password.' };
  }
}


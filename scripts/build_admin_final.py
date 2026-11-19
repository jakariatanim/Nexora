# -*- coding: utf-8 -*-
import os

script_path = "scripts/build_admin_final.py"

# We will read scripts/build_admin_overhaul.py and modify it with all features
with open("scripts/build_admin_overhaul.py", "r", encoding="utf-8") as f:
    text = f.read()

# Extract code between code = ''' and '''
start_str = "code = '''"
end_str = "\n'''\n"
s_idx = text.find(start_str) + len(start_str)
e_idx = text.rfind(end_str)
base_code = text[s_idx:e_idx]
base_code = base_code.replace(r"\'", "'")

# 1. Update imports
old_import = "import React, { useState, useEffect } from 'react';"
new_import = "import React, { useState, useEffect, useMemo } from 'react';"
base_code = base_code.replace(old_import, new_import, 1)

old_types = "import { Product, Order, Founder, Category, AdminMember, Review } from '../../lib/types';"
new_types = "import { Product, Order, Founder, Category, AdminMember, Review, Coupon, Claim } from '../../lib/types';"
base_code = base_code.replace(old_types, new_types, 1)

old_api = """import {
  fetchProducts,
  createProduct,
  updateProduct,
  deleteProduct,
  uploadImage,
  fetchOrders,
  updateOrderStatus,
  fetchFounder,
  updateFounder,
  fetchAdminMembers,
  createAdminMember,
  updateAdminMember,
  deleteAdminMember,
  fetchReviews,
  deleteReview
} from '../../lib/api';"""

new_api = """import {
  fetchProducts,
  createProduct,
  updateProduct,
  deleteProduct,
  uploadImage,
  fetchOrders,
  updateOrderStatus,
  fetchFounder,
  updateFounder,
  fetchAdminMembers,
  createAdminMember,
  updateAdminMember,
  deleteAdminMember,
  fetchReviews,
  deleteReview,
  fetchCoupons,
  createCoupon,
  updateCoupon,
  deleteCoupon,
  changeAdminPassword,
  resetAdminPassword,
  fetchClaims,
  updateClaimStatus
} from '../../lib/api';"""
base_code = base_code.replace(old_api, new_api, 1)

old_lucide = """  Sparkles,
  UserPlus,
  UserCheck
} from 'lucide-react';"""

new_lucide = """  Sparkles,
  UserPlus,
  UserCheck,
  Tag,
  Percent,
  Calendar,
  Clock,
  AlertCircle,
  Bell,
  Truck,
  FileText,
  CheckCircle2,
  RotateCcw,
  AlertTriangle,
  ArrowRight,
  ShieldAlert
} from 'lucide-react';"""
base_code = base_code.replace(old_lucide, new_lucide, 1)

# 2. Update activeTab type and data states
old_tab_state = """  // Active Navigation Tab
  const [activeTab, setActiveTab] = useState<'overview' | 'products' | 'categories' | 'orders' | 'founder' | 'staff' | 'reviews'>('products');

  // Toggle Controls
  const [showMetrics, setShowMetrics] = useState(true);
  const [showFilters, setShowFilters] = useState(true);

  // Data States
  const [products, setProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<Category[]>(INITIAL_CATEGORIES);
  const [orders, setOrders] = useState<Order[]>([]);
  const [founder, setFounder] = useState<Founder | null>(null);
  const [adminMembers, setAdminMembers] = useState<AdminMember[]>([]);
  const [reviews, setReviews] = useState<Review[]>([]);
  const [loading, setLoading] = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);"""

new_tab_state = """  // Active Navigation Tab (Includes Products, Orders, Staff, Categories, RMA Claims, Notifications, Coupons, Reviews, Founder)
  const [activeTab, setActiveTab] = useState<'overview' | 'products' | 'categories' | 'orders' | 'claims' | 'notifications' | 'founder' | 'staff' | 'reviews' | 'coupons'>('products');

  // Toggle Controls
  const [showMetrics, setShowMetrics] = useState(true);
  const [showFilters, setShowFilters] = useState(true);

  // Data States
  const [products, setProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<Category[]>(INITIAL_CATEGORIES);
  const [orders, setOrders] = useState<Order[]>([]);
  const [claims, setClaims] = useState<Claim[]>([]);
  const [founder, setFounder] = useState<Founder | null>(null);
  const [adminMembers, setAdminMembers] = useState<AdminMember[]>([]);
  const [reviews, setReviews] = useState<Review[]>([]);
  const [coupons, setCoupons] = useState<Coupon[]>([]);
  const [loading, setLoading] = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);

  // Coupon State & Modal
  const [isCouponModalOpen, setIsCouponModalOpen] = useState(false);
  const [couponForm, setCouponForm] = useState<{
    code: string;
    type: 'percent' | 'flat' | 'freeship';
    value: number;
    minSpend: number;
    durationDays: number;
    description: string;
    active: boolean;
  }>({
    code: '',
    type: 'percent',
    value: 10,
    minSpend: 0,
    durationDays: 30,
    description: '',
    active: true,
  });

  // Password Reset Modal State
  const [isResetPasswordModalOpen, setIsResetPasswordModalOpen] = useState(false);
  const [resetModalMessage, setResetModalMessage] = useState('');
  const [resetModalSuccess, setResetModalSuccess] = useState(false);
  const [resetLoading, setResetLoading] = useState(false);

  // RMA Claims Filter & Detail
  const [claimSearchQuery, setClaimSearchQuery] = useState('');
  const [selectedClaimStatusFilter, setSelectedClaimStatusFilter] = useState('All');
  const [selectedClaimDetail, setSelectedClaimDetail] = useState<Claim | null>(null);

  // Notifications Filter & Read State
  const [notificationCategoryFilter, setNotificationCategoryFilter] = useState<'all' | 'orders' | 'claims' | 'courier' | 'coupons' | 'reviews' | 'security'>('all');
  const [readNotificationIds, setReadNotificationIds] = useState<string[]>([]);"""

base_code = base_code.replace(old_tab_state, new_tab_state, 1)

# 3. Add showCurrentPassword state
old_pass_state = """  const [profileSuccessMsg, setProfileSuccessMsg] = useState('');"""

new_pass_state = """  const [profileSuccessMsg, setProfileSuccessMsg] = useState('');
  const [profileCurrentPassword, setProfileCurrentPassword] = useState('');
  const [showCurrentPassword, setShowCurrentPassword] = useState(false);"""
base_code = base_code.replace(old_pass_state, new_pass_state, 1)

# 4. Update loadDashboardData to include coupons & claims
old_load = """      const [prods, ords, fndr, admins, revs] = await Promise.all([
        fetchProducts(),
        fetchOrders(),
        fetchFounder(),
        fetchAdminMembers(),
        fetchReviews()
      ]);
      setProducts(prods || []);
      setOrders(ords || []);
      setFounder(fndr);
      setAdminMembers(admins || []);
      setReviews(revs || []);
      if (fndr) setFounderForm(fndr);"""

new_load = """      const [prods, ords, fndr, admins, revs, coupList, claimList] = await Promise.all([
        fetchProducts(),
        fetchOrders(),
        fetchFounder(),
        fetchAdminMembers(),
        fetchReviews(),
        fetchCoupons(),
        fetchClaims()
      ]);
      setProducts(prods || []);
      setOrders(ords || []);
      setFounder(fndr);
      setAdminMembers(admins || []);
      setReviews(revs || []);
      setCoupons(coupList || []);
      setClaims(claimList || []);
      if (fndr) setFounderForm(fndr);"""
base_code = base_code.replace(old_load, new_load, 1)

# 5. Update handleSaveProfile to use changeAdminPassword and add password reset, coupon, RMA, notification handlers
old_save_profile = """    if (isChangingPassword) {
      if (!profileCurrentPassword.trim()) {
        alert('Current password is required to authorize changing your password.');
        return;
      }
      const actualPassword = activeUser.password || (activeUser.username === 'admin' ? 'admin123' : 'NexoraSuperAdmin2026!');
      if (profileCurrentPassword.trim() !== actualPassword) {
        alert('Current password does not match. Please enter your valid current password to update security credentials.');
        return;
      }
      if (profileForm.password !== profileForm.confirmPassword) {
        alert('New passwords do not match. Please verify.');
        return;
      }
      if (profileForm.password.length < 6) {
        alert('New password must be at least 6 characters long.');
        return;
      }
    }"""

new_save_profile = """    if (isChangingPassword) {
      if (!profileCurrentPassword.trim()) {
        alert('Current password is required to authorize changing your password.');
        return;
      }
      if (profileForm.password !== profileForm.confirmPassword) {
        alert('New passwords do not match. Please verify.');
        return;
      }
      if (profileForm.password.length < 6) {
        alert('New password must be at least 6 characters long.');
        return;
      }

      // Authorize password change through backend security
      const passResult = await changeAdminPassword({
        id: activeUser.id,
        username: activeUser.username,
        currentPassword: profileCurrentPassword.trim(),
        newPassword: profileForm.password.trim()
      });

      if (!passResult.success) {
        alert(passResult.error || 'Current password is incorrect. (Hint: Default initial password is AdminOps2026!)');
        return;
      }
    }"""
base_code = base_code.replace(old_save_profile, new_save_profile, 1)

# 6. Add Emergency Reset, Coupon Handlers, RMA Handlers, and Notifications Stream after handleSaveProfile
old_delete_staff = """  // Delete Staff Member
  const handleDeleteStaff = async (id: string) => {"""

new_handlers = """  // Emergency Admin Password Reset
  const handlePerformPasswordReset = async () => {
    setResetLoading(true);
    setResetModalMessage('');
    try {
      const activeUser = adminMembers.find(m => m.username === currentUser?.username || m.email === currentUser?.email) || adminMembers[0];
      const targetUser = activeUser?.username || profileForm.username || 'admin';
      const targetEmail = activeUser?.email || profileForm.email || 'support@nexora.com';
      
      const res = await resetAdminPassword({ username: targetUser, email: targetEmail });
      if (res.success && res.tempPassword) {
        setResetModalSuccess(true);
        setResetModalMessage(`✓ Password has been reset to: ${res.tempPassword}`);
        setProfileCurrentPassword(res.tempPassword);
        setInviteToast(`✓ Admin password reset to: ${res.tempPassword}`);
        setTimeout(() => setInviteToast(''), 6000);
      } else {
        setResetModalSuccess(false);
        setResetModalMessage(res.error || 'Failed to reset password. Please check backend connection.');
      }
    } catch {
      setResetModalSuccess(false);
      setResetModalMessage('Error connecting to authentication service.');
    } finally {
      setResetLoading(false);
    }
  };

  // Coupon Management Handlers
  const handleOpenNewCoupon = () => {
    setCouponForm({
      code: '',
      type: 'percent',
      value: 10,
      minSpend: 0,
      durationDays: 30,
      description: '',
      active: true,
    });
    setIsCouponModalOpen(true);
  };

  const handleSaveCoupon = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!couponForm.code.trim()) {
      alert('Please enter a coupon code.');
      return;
    }
    const cleanCode = couponForm.code.trim().toUpperCase().replace(/[^A-Z0-9_-]/g, '');
    const expiry = new Date();
    expiry.setDate(expiry.getDate() + (Number(couponForm.durationDays) || 30));

    const payload: Partial<Coupon> = {
      code: cleanCode,
      type: couponForm.type,
      value: Number(couponForm.value) || 0,
      discountBDT: couponForm.type === 'flat' ? Number(couponForm.value) : 0,
      minSpend: Number(couponForm.minSpend) || 0,
      expiryDate: expiry.toISOString(),
      description: couponForm.description.trim() || `${couponForm.type === 'percent' ? couponForm.value + '%' : '৳' + couponForm.value} Promotional Voucher`,
      active: couponForm.active,
      usageCount: 0
    };

    const created = await createCoupon(payload);
    if (created) {
      setCoupons(prev => [created, ...prev.filter(c => c.id !== created.id)]);
      setIsCouponModalOpen(false);
      setInviteToast(`✓ Promo coupon "${cleanCode}" created successfully!`);
      setTimeout(() => setInviteToast(''), 4000);
    } else {
      alert('Failed to save coupon. Please ensure the coupon code is unique.');
    }
  };

  const handleDeleteCoupon = async (id: string, code: string) => {
    if (!confirm(`Are you sure you want to delete coupon "${code}"? Customers will no longer be able to apply it.`)) {
      return;
    }
    const ok = await deleteCoupon(id);
    if (ok) {
      setCoupons(prev => prev.filter(c => c.id !== id));
      setInviteToast(`✓ Coupon "${code}" deleted.`);
      setTimeout(() => setInviteToast(''), 3500);
    } else {
      alert('Failed to delete coupon.');
    }
  };

  const handleToggleCouponActive = async (coupon: Coupon) => {
    if (!coupon.id) return;
    const newActive = !coupon.active;
    const updated = await updateCoupon(coupon.id, { active: newActive });
    if (updated) {
      setCoupons(prev => prev.map(c => c.id === coupon.id ? updated : c));
      setInviteToast(`✓ Coupon "${coupon.code}" ${newActive ? 'activated' : 'paused'}.`);
      setTimeout(() => setInviteToast(''), 3000);
    }
  };

  // RMA Claims Status Updater
  const handleClaimStatusChange = async (claimId: string, newStatus: string) => {
    const ok = await updateClaimStatus(claimId, newStatus);
    if (ok) {
      setClaims(prev => prev.map(c => c.id === claimId ? { ...c, status: newStatus as any, updatedAt: new Date().toISOString() } : c));
      setInviteToast(`✓ RMA Claim ${claimId} updated to: ${newStatus}`);
      setTimeout(() => setInviteToast(''), 3500);
    } else {
      alert('Failed to update RMA claim status.');
    }
  };

  // Dynamic Notification Stream (Consolidates Orders, Claims, Reviews, Courier, Coupons, Security)
  const allNotifications = useMemo(() => {
    const list: {
      id: string;
      title: string;
      message: string;
      category: 'orders' | 'claims' | 'courier' | 'coupons' | 'reviews' | 'security';
      timestamp: string;
      dateObj: Date;
      linkTab?: 'orders' | 'claims' | 'reviews' | 'coupons';
      severity: 'info' | 'success' | 'warning' | 'alert';
    }[] = [];

    // 1. RMA Claims
    claims.forEach(c => {
      const d = c.createdAt ? new Date(c.createdAt) : new Date();
      if (c.status === 'Under Review') {
        list.push({
          id: `notif-claim-${c.id}`,
          title: `New RMA Claim: ${c.id}`,
          message: `${c.customerName} filed a return/warranty claim for Order #${c.orderId} (${c.issueType}). Issue: "${c.description}".`,
          category: 'claims',
          timestamp: c.createdAt || new Date().toISOString(),
          dateObj: d,
          linkTab: 'claims',
          severity: 'alert'
        });
      } else if (c.status === 'Approved for Pickup') {
        list.push({
          id: `notif-claim-${c.id}-pickup`,
          title: `RMA Claim Approved: ${c.id}`,
          message: `Claim #${c.id} approved for courier reverse-pickup from ${c.customerName} (${c.customerPhone}).`,
          category: 'courier',
          timestamp: c.updatedAt || c.createdAt || new Date().toISOString(),
          dateObj: d,
          linkTab: 'claims',
          severity: 'warning'
        });
      } else if (c.status === 'Replacement Dispatched') {
        list.push({
          id: `notif-claim-${c.id}-dispatch`,
          title: `Replacement Dispatched: ${c.id}`,
          message: `Fresh replacement hardware dispatched to customer ${c.customerName} for claim #${c.id}.`,
          category: 'courier',
          timestamp: c.updatedAt || c.createdAt || new Date().toISOString(),
          dateObj: d,
          linkTab: 'claims',
          severity: 'info'
        });
      } else if (c.status === 'Resolved') {
        list.push({
          id: `notif-claim-${c.id}-resolved`,
          title: `RMA Claim Resolved: ${c.id}`,
          message: `Warranty ticket #${c.id} has been fully inspected, resolved and closed.`,
          category: 'claims',
          timestamp: c.updatedAt || c.createdAt || new Date().toISOString(),
          dateObj: d,
          linkTab: 'claims',
          severity: 'success'
        });
      }
    });

    // 2. Orders
    orders.forEach(o => {
      const d = o.createdAt ? new Date(o.createdAt) : new Date();
      if (o.status === 'Pending') {
        list.push({
          id: `notif-order-${o.id}-pending`,
          title: `New Order Placed: #${o.id}`,
          message: `${o.customer.name} placed order #${o.id} for ৳${o.totalBDT.toLocaleString()} (${o.paymentMethod}). Pending dispatch.`,
          category: 'orders',
          timestamp: o.createdAt || new Date().toISOString(),
          dateObj: d,
          linkTab: 'orders',
          severity: 'warning'
        });
      } else if (o.status === 'Shipped') {
        list.push({
          id: `notif-order-${o.id}-ship`,
          title: `Courier In-Transit: #${o.id}`,
          message: `Order #${o.id} handed to courier partner for delivery to ${o.customer.address}.`,
          category: 'courier',
          timestamp: o.updatedAt || o.createdAt || new Date().toISOString(),
          dateObj: d,
          linkTab: 'orders',
          severity: 'info'
        });
      } else if (o.status === 'Delivered') {
        list.push({
          id: `notif-order-${o.id}-del`,
          title: `Order Delivered: #${o.id}`,
          message: `Shipment #${o.id} successfully delivered to ${o.customer.name}.`,
          category: 'orders',
          timestamp: o.updatedAt || o.createdAt || new Date().toISOString(),
          dateObj: d,
          linkTab: 'orders',
          severity: 'success'
        });
      }
    });

    // 3. Reviews
    reviews.forEach(r => {
      list.push({
        id: `notif-rev-${r.id}`,
        title: `Customer Feedback (${r.rating}★): ${r.productName}`,
        message: `${r.author} reviewed: "${r.comment.slice(0, 100)}..."`,
        category: 'reviews',
        timestamp: r.date || new Date().toISOString(),
        dateObj: new Date(r.date || Date.now()),
        linkTab: 'reviews',
        severity: 'info'
      });
    });

    // 4. Coupons
    coupons.forEach(c => {
      if (c.usageCount && c.usageCount > 0) {
        list.push({
          id: `notif-coup-${c.code}`,
          title: `Coupon Redeemed: ${c.code}`,
          message: `Voucher ${c.code} (${c.type === 'percent' ? c.value + '%' : '৳' + c.value} off) has been redeemed ${c.usageCount} time(s).`,
          category: 'coupons',
          timestamp: c.createdAt || new Date().toISOString(),
          dateObj: new Date(c.createdAt || Date.now()),
          linkTab: 'coupons',
          severity: 'info'
        });
      }
    });

    // 5. Security & System
    list.push({
      id: 'notif-sec-system',
      title: 'Security Governance & Active Infrastructure',
      message: 'NEXORA high-performance silicon store backend operational. Root admin session authorized.',
      category: 'security',
      timestamp: new Date().toISOString(),
      dateObj: new Date(),
      severity: 'info'
    });

    return list.sort((a, b) => b.dateObj.getTime() - a.dateObj.getTime());
  }, [claims, orders, reviews, coupons]);

  const unreadCount = allNotifications.filter(n => !readNotificationIds.includes(n.id)).length;

  const handleMarkAllNotificationsRead = () => {
    setReadNotificationIds(allNotifications.map(n => n.id));
    setInviteToast('✓ All notifications marked as read.');
    setTimeout(() => setInviteToast(''), 3000);
  };

  const handleToggleNotificationRead = (id: string) => {
    setReadNotificationIds(prev => 
      prev.includes(id) ? prev.filter(x => x !== id) : [...prev, id]
    );
  };

  // Delete Staff Member
  const handleDeleteStaff = async (id: string) => {"""
base_code = base_code.replace(old_delete_staff, new_handlers, 1)

# 7. Update Left Dock to include Claims, Notifications, and Coupons
old_dock_orders = """          {/* 5. Customer Orders */}
          <button
            onClick={() => setActiveTab('orders')}
            className={`relative group w-12 h-12 rounded-2xl flex items-center justify-center transition-all ${
              activeTab === 'orders'
                ? 'bg-[#0071E3] text-white shadow-lg shadow-blue-500/30 ring-2 ring-white/20'
                : 'text-white/60 hover:text-white hover:bg-white/10'
            }`}
            aria-label="Customer Orders"
          >
            <ShoppingBag className="w-5 h-5 transition-transform group-hover:scale-110" />
            <div className="absolute left-[84px] px-3 py-1.5 rounded-xl bg-[#1D1D1F] text-white text-xs font-semibold whitespace-nowrap shadow-2xl pointer-events-none opacity-0 group-hover:opacity-100 transition-opacity duration-200 z-50 border border-white/15">
              Customer Orders ({orders.length})
            </div>
          </button>"""

new_dock_middle = """          {/* 5. Customer Orders */}
          <button
            onClick={() => setActiveTab('orders')}
            className={`relative group w-12 h-12 rounded-2xl flex items-center justify-center transition-all ${
              activeTab === 'orders'
                ? 'bg-[#0071E3] text-white shadow-lg shadow-blue-500/30 ring-2 ring-white/20'
                : 'text-white/60 hover:text-white hover:bg-white/10'
            }`}
            aria-label="Customer Orders"
          >
            <ShoppingBag className="w-5 h-5 transition-transform group-hover:scale-110" />
            <div className="absolute left-[84px] px-3 py-1.5 rounded-xl bg-[#1D1D1F] text-white text-xs font-semibold whitespace-nowrap shadow-2xl pointer-events-none opacity-0 group-hover:opacity-100 transition-opacity duration-200 z-50 border border-white/15">
              Customer Orders ({orders.length})
            </div>
          </button>

          {/* 6. RMA & Warranty Claims (New Dedicated Tab) */}
          <button
            onClick={() => setActiveTab('claims')}
            className={`relative group w-12 h-12 rounded-2xl flex items-center justify-center transition-all ${
              activeTab === 'claims'
                ? 'bg-[#0071E3] text-white shadow-lg shadow-blue-500/30 ring-2 ring-white/20'
                : 'text-white/60 hover:text-white hover:bg-white/10'
            }`}
            aria-label="RMA & Warranty Claims"
          >
            <RotateCcw className="w-5 h-5 transition-transform group-hover:scale-110" />
            {claims.filter(c => c.status === 'Under Review').length > 0 && (
              <span className="absolute top-2 right-2 w-2.5 h-2.5 rounded-full bg-amber-400 ring-2 ring-[#0B132B]" />
            )}
            <div className="absolute left-[84px] px-3 py-1.5 rounded-xl bg-[#1D1D1F] text-white text-xs font-semibold whitespace-nowrap shadow-2xl pointer-events-none opacity-0 group-hover:opacity-100 transition-opacity duration-200 z-50 border border-white/15">
              RMA &amp; Warranty Claims ({claims.length})
            </div>
          </button>

          {/* 7. Notifications Center (New Dedicated Tab) */}
          <button
            onClick={() => setActiveTab('notifications')}
            className={`relative group w-12 h-12 rounded-2xl flex items-center justify-center transition-all ${
              activeTab === 'notifications'
                ? 'bg-[#0071E3] text-white shadow-lg shadow-blue-500/30 ring-2 ring-white/20'
                : 'text-white/60 hover:text-white hover:bg-white/10'
            }`}
            aria-label="Notifications Center"
          >
            <Bell className="w-5 h-5 transition-transform group-hover:scale-110" />
            {unreadCount > 0 && (
              <span className="absolute -top-1 -right-1 px-1.5 py-0.5 min-w-[18px] text-[10px] font-bold font-mono rounded-full bg-red-500 text-white flex items-center justify-center ring-2 ring-[#0B132B] shadow-md animate-pulse">
                {unreadCount > 99 ? '99+' : unreadCount}
              </span>
            )}
            <div className="absolute left-[84px] px-3 py-1.5 rounded-xl bg-[#1D1D1F] text-white text-xs font-semibold whitespace-nowrap shadow-2xl pointer-events-none opacity-0 group-hover:opacity-100 transition-opacity duration-200 z-50 border border-white/15">
              Notifications &amp; Activity ({unreadCount} unread)
            </div>
          </button>"""
base_code = base_code.replace(old_dock_orders, new_dock_middle, 1)

old_dock_founder = """          {/* 7. Founder's Vision */}
          <button
            onClick={() => setActiveTab('founder')}
            className={`relative group w-12 h-12 rounded-2xl flex items-center justify-center transition-all ${
              activeTab === 'founder'
                ? 'bg-[#0071E3] text-white shadow-lg shadow-blue-500/30 ring-2 ring-white/20'
                : 'text-white/60 hover:text-white hover:bg-white/10'
            }`}
            aria-label="Founder's Vision"
          >
            <Compass className="w-5 h-5 transition-transform group-hover:scale-110" />
            <div className="absolute left-[84px] px-3 py-1.5 rounded-xl bg-[#1D1D1F] text-white text-xs font-semibold whitespace-nowrap shadow-2xl pointer-events-none opacity-0 group-hover:opacity-100 transition-opacity duration-200 z-50 border border-white/15">
              Founder's Vision
            </div>
          </button>"""

new_dock_founder = """          {/* 9. Promotional Coupons & Discounts */}
          <button
            onClick={() => setActiveTab('coupons')}
            className={`relative group w-12 h-12 rounded-2xl flex items-center justify-center transition-all ${
              activeTab === 'coupons'
                ? 'bg-[#0071E3] text-white shadow-lg shadow-blue-500/30 ring-2 ring-white/20'
                : 'text-white/60 hover:text-white hover:bg-white/10'
            }`}
            aria-label="Promo Coupons"
          >
            <Tag className="w-5 h-5 transition-transform group-hover:scale-110" />
            <div className="absolute left-[84px] px-3 py-1.5 rounded-xl bg-[#1D1D1F] text-white text-xs font-semibold whitespace-nowrap shadow-2xl pointer-events-none opacity-0 group-hover:opacity-100 transition-opacity duration-200 z-50 border border-white/15">
              Promo Coupons &amp; Discounts ({coupons.length})
            </div>
          </button>

          {/* 10. Founder's Vision */}
          <button
            onClick={() => setActiveTab('founder')}
            className={`relative group w-12 h-12 rounded-2xl flex items-center justify-center transition-all ${
              activeTab === 'founder'
                ? 'bg-[#0071E3] text-white shadow-lg shadow-blue-500/30 ring-2 ring-white/20'
                : 'text-white/60 hover:text-white hover:bg-white/10'
            }`}
            aria-label="Founder's Vision"
          >
            <Compass className="w-5 h-5 transition-transform group-hover:scale-110" />
            <div className="absolute left-[84px] px-3 py-1.5 rounded-xl bg-[#1D1D1F] text-white text-xs font-semibold whitespace-nowrap shadow-2xl pointer-events-none opacity-0 group-hover:opacity-100 transition-opacity duration-200 z-50 border border-white/15">
              Founder's Vision
            </div>
          </button>"""
base_code = base_code.replace(old_dock_founder, new_dock_founder, 1)

# 8. Update Header Titles and Header Action Buttons
old_header_title = """              {activeTab === 'orders' && 'Live Customer Orders & Fulfillment'}
              {activeTab === 'reviews' && 'Customer Experience & Feedback'}
              {activeTab === 'founder' && "Founder's Vision Profile"}"""

new_header_title = """              {activeTab === 'orders' && 'Live Customer Orders & Fulfillment'}
              {activeTab === 'claims' && 'RMA & Warranty Claims Governance'}
              {activeTab === 'notifications' && 'Notifications & Activity Center'}
              {activeTab === 'reviews' && 'Customer Experience & Feedback'}
              {activeTab === 'founder' && "Founder's Vision Profile"}
              {activeTab === 'coupons' && 'Promo Coupons & Discount Architecture'}"""
base_code = base_code.replace(old_header_title, new_header_title, 1)

old_header_badge_end = """              <div className="text-left hidden sm:block pr-1">
                <div className="text-xs font-bold text-[#1D1D1F] dark:text-white leading-tight">
                  {currentUser?.name || 'Jakaria Tanim'}
                </div>
                <div className="text-[10px] text-amber-600 dark:text-amber-400 font-mono font-semibold">
                  {currentUser?.role || 'Super Administrator'}
                </div>
              </div>
            </div>"""

new_header_badge_end = """              <div className="text-left hidden sm:block pr-1">
                <div className="text-xs font-bold text-[#1D1D1F] dark:text-white leading-tight">
                  {currentUser?.name || 'Jakaria Tanim'}
                </div>
                <div className="text-[10px] text-amber-600 dark:text-amber-400 font-mono font-semibold">
                  {currentUser?.role || 'Super Administrator'}
                </div>
              </div>
            </div>

            {/* Quick Notification Bell in Header */}
            <button
              onClick={() => setActiveTab('notifications')}
              className={`relative p-2.5 rounded-full border transition-all ${
                activeTab === 'notifications'
                  ? 'bg-[#0071E3] text-white border-[#0071E3] shadow-md shadow-blue-500/20'
                  : 'bg-slate-100 dark:bg-white/10 border-black/10 dark:border-white/15 text-[#1D1D1F] dark:text-white hover:bg-slate-200'
              }`}
              title="Open Notifications Center"
            >
              <Bell className="w-4 h-4" />
              {unreadCount > 0 && (
                <span className="absolute -top-1 -right-1 px-1.5 py-0.2 min-w-[18px] text-[10px] font-bold font-mono rounded-full bg-red-500 text-white flex items-center justify-center ring-2 ring-white dark:ring-[#0D152A] shadow-sm">
                  {unreadCount > 99 ? '99+' : unreadCount}
                </span>
              )}
            </button>"""
base_code = base_code.replace(old_header_badge_end, new_header_badge_end, 1)

old_header_reviews = """            {activeTab === 'reviews' && (
              <a
                href="/reviews"
                target="_blank"
                rel="noreferrer"
                className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full bg-[#0071E3] hover:bg-[#0077ED] text-white text-sm font-bold shadow-md transition-all active:scale-95"
              >
                <ExternalLink className="w-4 h-4" />
                <span>Public Reviews Page ↗</span>
              </a>
            )}"""

new_header_reviews = """            {activeTab === 'reviews' && (
              <a
                href="/reviews"
                target="_blank"
                rel="noreferrer"
                className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full bg-[#0071E3] hover:bg-[#0077ED] text-white text-sm font-bold shadow-md transition-all active:scale-95"
              >
                <ExternalLink className="w-4 h-4" />
                <span>Public Reviews Page ↗</span>
              </a>
            )}

            {activeTab === 'coupons' && (
              <button
                onClick={handleOpenNewCoupon}
                className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full bg-[#0071E3] hover:bg-[#0077ED] text-white text-sm font-bold shadow-md transition-all active:scale-95"
              >
                <Plus className="w-4 h-4" />
                <span>Create Promo Coupon</span>
              </button>
            )}

            {activeTab === 'claims' && (
              <a
                href="/warranty-claim"
                target="_blank"
                rel="noreferrer"
                className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full bg-[#0071E3] hover:bg-[#0077ED] text-white text-sm font-bold shadow-md transition-all active:scale-95"
              >
                <ExternalLink className="w-4 h-4" />
                <span>Public RMA Claim Page ↗</span>
              </a>
            )}

            {activeTab === 'notifications' && (
              <button
                onClick={handleMarkAllNotificationsRead}
                className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full bg-emerald-600 hover:bg-emerald-700 text-white text-sm font-bold shadow-md transition-all active:scale-95"
              >
                <CheckCircle2 className="w-4 h-4" />
                <span>Mark All Read</span>
              </button>
            )}"""
base_code = base_code.replace(old_header_reviews, new_header_reviews, 1)

# 9. Add Tab 8 (Coupons), Tab 9 (RMA Claims), Tab 10 (Notifications) after Tab 7 (Founder)
tab_8_9_10 = """          {/* =======================================================
              TAB 8: PROMOTIONAL COUPONS & DISCOUNT ARCHITECTURE
              ======================================================= */}
          {activeTab === 'coupons' && (
            <div className="space-y-6">
              {/* Header Banner */}
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-6 rounded-2xl bg-white dark:bg-[#151D30] border border-black/[0.08] dark:border-white/10 shadow-sm">
                <div>
                  <div className="flex items-center gap-2">
                    <div className="p-2 rounded-xl bg-blue-500/10 text-[#0071E3]">
                      <Tag className="w-5 h-5" />
                    </div>
                    <h3 className="text-xl font-bold text-[#1D1D1F] dark:text-white">Promo Coupons &amp; Discount Governance</h3>
                  </div>
                  <p className="text-sm text-[#6E6E73] dark:text-[#A1A1A6] mt-1">
                    Create promotional vouchers, configure percentage (%) or flat amount (৳) discounts, set validity days, and track redemption activity.
                  </p>
                </div>
                <button
                  onClick={handleOpenNewCoupon}
                  className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full bg-[#0071E3] hover:bg-[#0077ED] text-white text-sm font-bold shadow-md transition-all active:scale-95 self-start sm:self-auto"
                >
                  <Plus className="w-4 h-4" />
                  <span>Create Promo Coupon</span>
                </button>
              </div>

              {/* Quick Metrics */}
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div className="p-5 rounded-2xl bg-white dark:bg-[#151D30] border border-black/[0.08] dark:border-white/10 shadow-sm">
                  <span className="text-xs font-mono uppercase tracking-wider text-[#86868B]">Active Coupons</span>
                  <div className="text-3xl font-extrabold text-[#1D1D1F] dark:text-white mt-1">
                    {coupons.filter(c => c.active !== false).length} <span className="text-sm font-normal text-[#86868B]">/ {coupons.length} total</span>
                  </div>
                </div>
                <div className="p-5 rounded-2xl bg-white dark:bg-[#151D30] border border-black/[0.08] dark:border-white/10 shadow-sm">
                  <span className="text-xs font-mono uppercase tracking-wider text-[#86868B]">Customer Redemptions</span>
                  <div className="text-3xl font-extrabold text-emerald-600 dark:text-emerald-400 mt-1">
                    {coupons.reduce((sum, c) => sum + (c.usageCount || 0), 0)} <span className="text-sm font-normal text-[#86868B]">times used</span>
                  </div>
                </div>
                <div className="p-5 rounded-2xl bg-white dark:bg-[#151D30] border border-black/[0.08] dark:border-white/10 shadow-sm">
                  <span className="text-xs font-mono uppercase tracking-wider text-[#86868B]">Checkout Validation</span>
                  <div className="text-3xl font-extrabold text-[#0071E3] mt-1">
                    Live <span className="text-sm font-normal text-[#86868B]">(JSON Database)</span>
                  </div>
                </div>
              </div>

              {/* Coupons Table */}
              <div className="rounded-2xl bg-white dark:bg-[#151D30] border border-black/[0.08] dark:border-white/10 shadow-sm overflow-hidden">
                <div className="overflow-x-auto">
                  <table className="w-full text-left">
                    <thead className="bg-[#F5F5F7] dark:bg-white/5 text-[#86868B] dark:text-slate-400 uppercase font-mono text-xs font-bold tracking-wider border-b border-black/[0.06] dark:border-white/10">
                      <tr>
                        <th className="px-6 py-4">Coupon Code</th>
                        <th className="px-6 py-4">Discount Value</th>
                        <th className="px-6 py-4">Min. Order Spend</th>
                        <th className="px-6 py-4">Validity / Expiry</th>
                        <th className="px-6 py-4">Usage</th>
                        <th className="px-6 py-4">Status</th>
                        <th className="px-6 py-4 text-right">Actions</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-black/[0.06] dark:divide-white/10 text-sm">
                      {coupons.length === 0 ? (
                        <tr>
                          <td colSpan={7} className="px-6 py-12 text-center text-[#86868B]">
                            No coupons currently found. Click &quot;Create Promo Coupon&quot; to add your first discount voucher.
                          </td>
                        </tr>
                      ) : (
                        coupons.map((coup) => {
                          const isExpired = coup.expiryDate ? new Date(coup.expiryDate).getTime() < Date.now() : false;
                          const daysLeft = coup.expiryDate
                            ? Math.ceil((new Date(coup.expiryDate).getTime() - Date.now()) / (1000 * 60 * 60 * 24))
                            : null;
                          return (
                            <tr key={coup.id || coup.code} className="hover:bg-black/[0.02] dark:hover:bg-white/5 transition-colors">
                              <td className="px-6 py-4">
                                <div className="flex items-center gap-2">
                                  <span className="px-3 py-1.5 rounded-lg bg-blue-500/10 text-[#0071E3] font-mono font-bold tracking-wider text-sm border border-blue-500/20">
                                    {coup.code}
                                  </span>
                                  <button
                                    onClick={() => {
                                      navigator.clipboard.writeText(coup.code);
                                      setInviteToast(`✓ Code "${coup.code}" copied to clipboard!`);
                                      setTimeout(() => setInviteToast(''), 3000);
                                    }}
                                    className="p-1 rounded text-gray-400 hover:text-[#0071E3] transition-colors"
                                    title="Copy coupon code"
                                  >
                                    <Copy className="w-3.5 h-3.5" />
                                  </button>
                                </div>
                                <div className="text-xs text-[#86868B] mt-1 max-w-xs truncate">
                                  {coup.description || 'Promotional voucher'}
                                </div>
                              </td>

                              <td className="px-6 py-4">
                                <span className="inline-flex items-center gap-1 font-bold text-emerald-600 dark:text-emerald-400 font-mono">
                                  {coup.type === 'percent' && (
                                    <>
                                      <Percent className="w-3.5 h-3.5" />
                                      <span>{coup.value || 0}% OFF</span>
                                    </>
                                  )}
                                  {coup.type === 'flat' && (
                                    <>
                                      <span>৳{(coup.value || coup.discountBDT || 0).toLocaleString()} OFF</span>
                                    </>
                                  )}
                                  {coup.type === 'freeship' && (
                                    <span>Free Shipping</span>
                                  )}
                                </span>
                              </td>

                              <td className="px-6 py-4 font-mono text-xs">
                                {coup.minSpend && coup.minSpend > 0 ? (
                                  <span className="font-semibold text-[#1D1D1F] dark:text-white">
                                    ৳{coup.minSpend.toLocaleString()}
                                  </span>
                                ) : (
                                  <span className="text-gray-400">No minimum</span>
                                )}
                              </td>

                              <td className="px-6 py-4 font-mono text-xs">
                                {isExpired ? (
                                  <span className="px-2 py-0.5 rounded-full bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-400 font-bold">
                                    Expired
                                  </span>
                                ) : daysLeft !== null ? (
                                  <div className="space-y-0.5">
                                    <span className="px-2 py-0.5 rounded-full bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 font-bold">
                                      {daysLeft} days left
                                    </span>
                                    <div className="text-[10px] text-[#86868B]">
                                      Exp: {new Date(coup.expiryDate!).toLocaleDateString('en-GB')}
                                    </div>
                                  </div>
                                ) : (
                                  <span className="text-gray-400">Permanent</span>
                                )}
                              </td>

                              <td className="px-6 py-4 font-mono text-xs text-[#1D1D1F] dark:text-white">
                                <span className="font-bold">{coup.usageCount || 0}</span> orders
                              </td>

                              <td className="px-6 py-4">
                                <button
                                  onClick={() => handleToggleCouponActive(coup)}
                                  className={`px-3 py-1 rounded-full text-xs font-bold transition-all ${
                                    coup.active !== false && !isExpired
                                      ? 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-400 hover:bg-emerald-200'
                                      : 'bg-gray-100 dark:bg-white/10 text-gray-500 hover:bg-gray-200'
                                  }`}
                                  title="Toggle coupon active / paused"
                                >
                                  {coup.active !== false && !isExpired ? 'Active' : 'Paused'}
                                </button>
                              </td>

                              <td className="px-6 py-4 text-right">
                                <button
                                  onClick={() => coup.id && handleDeleteCoupon(coup.id, coup.code)}
                                  className="p-2 rounded-xl text-red-500 hover:text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors"
                                  title="Delete & revoke coupon"
                                >
                                  <Trash2 className="w-4 h-4" />
                                </button>
                              </td>
                            </tr>
                          );
                        })
                      )}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}

          {/* =======================================================
              TAB 9: RMA & WARRANTY CLAIMS GOVERNANCE (NEW)
              ======================================================= */}
          {activeTab === 'claims' && (
            <div className="space-y-6">
              {/* Header Banner */}
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-6 rounded-2xl bg-white dark:bg-[#151D30] border border-black/[0.08] dark:border-white/10 shadow-sm">
                <div>
                  <div className="flex items-center gap-2">
                    <div className="p-2 rounded-xl bg-amber-500/10 text-amber-600 dark:text-amber-400">
                      <RotateCcw className="w-5 h-5" />
                    </div>
                    <h3 className="text-xl font-bold text-[#1D1D1F] dark:text-white">RMA Return &amp; Warranty Claims Governance</h3>
                  </div>
                  <p className="text-sm text-[#6E6E73] dark:text-[#A1A1A6] mt-1">
                    Manage incoming hardware replacement tickets, authorize courier pick-ups, track testing results, and close resolved warranty claims.
                  </p>
                </div>
                <div className="flex items-center gap-2 self-start sm:self-auto">
                  <a
                    href="/warranty-claim"
                    target="_blank"
                    rel="noreferrer"
                    className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full bg-[#0071E3] hover:bg-[#0077ED] text-white text-xs font-bold shadow-md transition-all"
                  >
                    <ExternalLink className="w-3.5 h-3.5" />
                    <span>Public RMA Claim Page ↗</span>
                  </a>
                </div>
              </div>

              {/* Claims Metric Cards */}
              <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
                <div className="p-5 rounded-2xl bg-white dark:bg-[#151D30] border border-black/[0.08] dark:border-white/10 shadow-sm">
                  <span className="text-xs font-mono uppercase tracking-wider text-[#86868B]">Total RMA Tickets</span>
                  <div className="text-3xl font-extrabold text-[#1D1D1F] dark:text-white mt-1">
                    {claims.length}
                  </div>
                </div>

                <div className="p-5 rounded-2xl bg-white dark:bg-[#151D30] border border-amber-200 dark:border-amber-700/30 bg-amber-50/30 dark:bg-amber-950/20 shadow-sm">
                  <span className="text-xs font-mono uppercase tracking-wider text-amber-700 dark:text-amber-400 flex items-center gap-1">
                    <AlertTriangle className="w-3.5 h-3.5" />
                    <span>Under Review</span>
                  </span>
                  <div className="text-3xl font-extrabold text-amber-600 dark:text-amber-400 mt-1">
                    {claims.filter(c => c.status === 'Under Review').length}
                  </div>
                </div>

                <div className="p-5 rounded-2xl bg-white dark:bg-[#151D30] border border-blue-200 dark:border-blue-700/30 bg-blue-50/30 dark:bg-blue-950/20 shadow-sm">
                  <span className="text-xs font-mono uppercase tracking-wider text-blue-700 dark:text-blue-300 flex items-center gap-1">
                    <Truck className="w-3.5 h-3.5" />
                    <span>Courier Pickup / Transit</span>
                  </span>
                  <div className="text-3xl font-extrabold text-[#0071E3] mt-1">
                    {claims.filter(c => c.status === 'Approved for Pickup' || c.status === 'Replacement Dispatched').length}
                  </div>
                </div>

                <div className="p-5 rounded-2xl bg-white dark:bg-[#151D30] border border-emerald-200 dark:border-emerald-700/30 bg-emerald-50/30 dark:bg-emerald-950/20 shadow-sm">
                  <span className="text-xs font-mono uppercase tracking-wider text-emerald-700 dark:text-emerald-400 flex items-center gap-1">
                    <CheckCircle className="w-3.5 h-3.5" />
                    <span>Resolved &amp; Closed</span>
                  </span>
                  <div className="text-3xl font-extrabold text-emerald-600 dark:text-emerald-400 mt-1">
                    {claims.filter(c => c.status === 'Resolved').length}
                  </div>
                </div>
              </div>

              {/* Filter & Search Bar */}
              <div className="p-4 rounded-2xl bg-white dark:bg-[#151D30] border border-black/[0.08] dark:border-white/10 shadow-sm flex flex-col sm:flex-row items-center justify-between gap-3">
                <div className="flex items-center gap-2 w-full sm:w-auto">
                  <Search className="w-4 h-4 text-gray-400" />
                  <input
                    type="text"
                    placeholder="Search by RMA ID, Order ID, Customer name, or phone..."
                    value={claimSearchQuery}
                    onChange={(e) => setClaimSearchQuery(e.target.value)}
                    className="w-full sm:w-80 px-3 py-1.5 rounded-xl bg-[#F5F5F7] dark:bg-white/5 border border-black/10 dark:border-white/10 text-xs text-[#1D1D1F] dark:text-white focus:outline-none focus:border-[#0071E3]"
                  />
                </div>

                <div className="flex items-center gap-1.5 overflow-x-auto w-full sm:w-auto pb-1 sm:pb-0">
                  {['All', 'Under Review', 'Approved for Pickup', 'Replacement Dispatched', 'Resolved'].map((st) => (
                    <button
                      key={st}
                      onClick={() => setSelectedClaimStatusFilter(st)}
                      className={`px-3 py-1 rounded-lg text-xs font-bold whitespace-nowrap transition-all ${
                        selectedClaimStatusFilter === st
                          ? 'bg-[#0071E3] text-white shadow-sm'
                          : 'bg-[#F5F5F7] dark:bg-white/5 text-[#6E6E73] dark:text-[#A1A1A6] hover:bg-black/5 dark:hover:bg-white/15'
                      }`}
                    >
                      {st}
                    </button>
                  ))}
                </div>
              </div>

              {/* Claims Table */}
              <div className="rounded-2xl bg-white dark:bg-[#151D30] border border-black/[0.08] dark:border-white/10 shadow-sm overflow-hidden">
                <div className="overflow-x-auto">
                  <table className="w-full text-left">
                    <thead className="bg-[#F5F5F7] dark:bg-white/5 text-[#86868B] dark:text-slate-400 uppercase font-mono text-xs font-bold tracking-wider border-b border-black/[0.06] dark:border-white/10">
                      <tr>
                        <th className="px-6 py-4">RMA &amp; Order ID</th>
                        <th className="px-6 py-4">Customer Details</th>
                        <th className="px-6 py-4">Issue Category &amp; Description</th>
                        <th className="px-6 py-4">Filed Date</th>
                        <th className="px-6 py-4">Claim Status</th>
                        <th className="px-6 py-4 text-right">Actions</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-black/[0.06] dark:divide-white/10 text-sm">
                      {claims
                        .filter(c => {
                          const matchesStatus = selectedClaimStatusFilter === 'All' || c.status === selectedClaimStatusFilter;
                          const q = claimSearchQuery.toLowerCase().trim();
                          const matchesQuery = !q || 
                            (c.id && c.id.toLowerCase().includes(q)) || 
                            (c.orderId && c.orderId.toLowerCase().includes(q)) || 
                            (c.customerName && c.customerName.toLowerCase().includes(q)) || 
                            (c.customerPhone && c.customerPhone.toLowerCase().includes(q)) || 
                            (c.issueType && c.issueType.toLowerCase().includes(q));
                          return matchesStatus && matchesQuery;
                        })
                        .map((c) => {
                          return (
                            <tr key={c.id} className="hover:bg-black/[0.02] dark:hover:bg-white/5 transition-colors">
                              <td className="px-6 py-4">
                                <div className="font-mono font-bold text-sm text-[#0071E3] flex items-center gap-1.5">
                                  <span>{c.id}</span>
                                </div>
                                <div className="text-xs font-mono text-[#86868B] mt-0.5">
                                  Order: <strong className="text-[#1D1D1F] dark:text-white">#{c.orderId}</strong>
                                </div>
                              </td>

                              <td className="px-6 py-4">
                                <div className="font-semibold text-sm text-[#1D1D1F] dark:text-white">
                                  {c.customerName || 'Valued Customer'}
                                </div>
                                <div className="text-xs font-mono text-[#86868B] mt-0.5 flex items-center gap-2">
                                  <span>{c.customerPhone}</span>
                                  {c.customerPhone && (
                                    <a
                                      href={`https://wa.me/${c.customerPhone.replace(/[^0-9]/g, '')}`}
                                      target="_blank"
                                      rel="noreferrer"
                                      className="text-emerald-600 hover:underline text-[10px] font-bold"
                                      title="Message customer on WhatsApp"
                                    >
                                      WhatsApp
                                    </a>
                                  )}
                                </div>
                              </td>

                              <td className="px-6 py-4 max-w-sm">
                                <span className="inline-block px-2 py-0.5 rounded-md bg-amber-100 dark:bg-amber-900/30 text-amber-800 dark:text-amber-300 font-semibold text-xs mb-1">
                                  {c.issueType}
                                </span>
                                <p className="text-xs text-[#6E6E73] dark:text-[#A1A1A6] line-clamp-2 leading-relaxed">
                                  {c.description}
                                </p>
                              </td>

                              <td className="px-6 py-4 text-xs font-mono text-[#86868B]">
                                {c.createdAt ? new Date(c.createdAt).toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' }) : 'Recent'}
                              </td>

                              <td className="px-6 py-4">
                                <select
                                  value={c.status}
                                  onChange={(e) => handleClaimStatusChange(c.id, e.target.value)}
                                  className={`px-3 py-1.5 rounded-xl border text-xs font-bold font-mono focus:outline-none transition-colors ${
                                    c.status === 'Under Review'
                                      ? 'border-amber-300 bg-amber-50 text-amber-800 dark:bg-amber-950/40 dark:text-amber-300'
                                      : c.status === 'Approved for Pickup'
                                      ? 'border-blue-300 bg-blue-50 text-blue-800 dark:bg-blue-950/40 dark:text-blue-300'
                                      : c.status === 'Replacement Dispatched'
                                      ? 'border-purple-300 bg-purple-50 text-purple-800 dark:bg-purple-950/40 dark:text-purple-300'
                                      : 'border-emerald-300 bg-emerald-50 text-emerald-800 dark:bg-emerald-950/40 dark:text-emerald-300'
                                  }`}
                                >
                                  <option value="Under Review" className="text-black">Under Review</option>
                                  <option value="Approved for Pickup" className="text-black">Approved for Pickup</option>
                                  <option value="Replacement Dispatched" className="text-black">Replacement Dispatched</option>
                                  <option value="Resolved" className="text-black">Resolved</option>
                                </select>
                              </td>

                              <td className="px-6 py-4 text-right">
                                <button
                                  onClick={() => setSelectedClaimDetail(c)}
                                  className="px-3 py-1.5 rounded-xl bg-slate-100 dark:bg-white/10 hover:bg-[#0071E3] hover:text-white text-xs font-semibold transition-all"
                                >
                                  View Details
                                </button>
                              </td>
                            </tr>
                          );
                        })}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}

          {/* =======================================================
              TAB 10: NOTIFICATIONS & ACTIVITY CENTER (NEW)
              ======================================================= */}
          {activeTab === 'notifications' && (
            <div className="space-y-6">
              {/* Header Banner */}
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-6 rounded-2xl bg-white dark:bg-[#151D30] border border-black/[0.08] dark:border-white/10 shadow-sm">
                <div>
                  <div className="flex items-center gap-2">
                    <div className="p-2 rounded-xl bg-red-500/10 text-red-500">
                      <Bell className="w-5 h-5" />
                    </div>
                    <h3 className="text-xl font-bold text-[#1D1D1F] dark:text-white">Admin Notifications &amp; System Activity Center</h3>
                  </div>
                  <p className="text-sm text-[#6E6E73] dark:text-[#A1A1A6] mt-1">
                    Unified notifications for incoming customer orders, RMA warranty claims, courier fulfillment, reviews, and security events.
                  </p>
                </div>
                <div className="flex items-center gap-2 self-start sm:self-auto">
                  <button
                    onClick={handleMarkAllNotificationsRead}
                    className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold shadow-md transition-all active:scale-95"
                  >
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    <span>Mark All Read</span>
                  </button>
                  <button
                    onClick={handleRefresh}
                    className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-slate-100 dark:bg-white/10 hover:bg-slate-200 text-xs font-semibold text-[#1D1D1F] dark:text-white transition-all"
                  >
                    <RefreshCw className={`w-3.5 h-3.5 ${isRefreshing ? 'animate-spin text-[#0071E3]' : ''}`} />
                    <span>Refresh</span>
                  </button>
                </div>
              </div>

              {/* Category Filter Tabs */}
              <div className="flex items-center gap-2 overflow-x-auto pb-1 scrollbar-none">
                {[
                  { id: 'all', label: 'All Notifications', count: allNotifications.length, icon: Bell },
                  { id: 'orders', label: 'Orders', count: allNotifications.filter(n => n.category === 'orders').length, icon: ShoppingBag },
                  { id: 'claims', label: 'RMA & Warranty', count: allNotifications.filter(n => n.category === 'claims').length, icon: RotateCcw },
                  { id: 'courier', label: 'Courier & Logistics', count: allNotifications.filter(n => n.category === 'courier').length, icon: Truck },
                  { id: 'reviews', label: 'Customer Reviews', count: allNotifications.filter(n => n.category === 'reviews').length, icon: Star },
                  { id: 'coupons', label: 'Promo Coupons', count: allNotifications.filter(n => n.category === 'coupons').length, icon: Tag },
                  { id: 'security', label: 'Security & Staff', count: allNotifications.filter(n => n.category === 'security').length, icon: ShieldCheck },
                ].map((tab) => {
                  const Icon = tab.icon;
                  const isActive = notificationCategoryFilter === tab.id;
                  return (
                    <button
                      key={tab.id}
                      onClick={() => setNotificationCategoryFilter(tab.id as any)}
                      className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold whitespace-nowrap transition-all ${
                        isActive
                          ? 'bg-[#0071E3] text-white shadow-md shadow-blue-500/20'
                          : 'bg-white dark:bg-[#151D30] text-[#6E6E73] dark:text-[#A1A1A6] hover:bg-black/5 dark:hover:bg-white/10 border border-black/[0.06] dark:border-white/10'
                      }`}
                    >
                      <Icon className="w-3.5 h-3.5" />
                      <span>{tab.label}</span>
                      <span className={`px-1.5 py-0.2 rounded-full text-[10px] font-mono ${
                        isActive ? 'bg-white/20 text-white' : 'bg-black/5 dark:bg-white/10 text-[#86868B]'
                      }`}>
                        {tab.count}
                      </span>
                    </button>
                  );
                })}
              </div>

              {/* Notification Cards Stream */}
              <div className="space-y-3">
                {allNotifications
                  .filter(n => notificationCategoryFilter === 'all' || n.category === notificationCategoryFilter)
                  .length === 0 ? (
                  <div className="p-12 text-center rounded-2xl bg-white dark:bg-[#151D30] border border-black/[0.08] dark:border-white/10 text-[#86868B]">
                    <Bell className="w-8 h-8 mx-auto mb-2 opacity-40" />
                    <p className="text-sm font-semibold">No notifications found in this category.</p>
                  </div>
                ) : (
                  allNotifications
                    .filter(n => notificationCategoryFilter === 'all' || n.category === notificationCategoryFilter)
                    .map((item) => {
                      const isUnread = !readNotificationIds.includes(item.id);
                      return (
                        <div
                          key={item.id}
                          className={`p-4 sm:p-5 rounded-2xl border transition-all flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 ${
                            isUnread
                              ? 'bg-white dark:bg-[#151D30] border-[#0071E3]/40 shadow-sm ring-1 ring-[#0071E3]/20'
                              : 'bg-white/60 dark:bg-[#151D30]/60 border-black/[0.06] dark:border-white/10 opacity-80'
                          }`}
                        >
                          <div className="flex items-start gap-3.5 flex-1">
                            {/* Icon badge */}
                            <div className={`w-10 h-10 rounded-2xl flex items-center justify-center flex-shrink-0 mt-0.5 ${
                              item.category === 'claims'
                                ? 'bg-amber-500/10 text-amber-600 dark:text-amber-400'
                                : item.category === 'orders'
                                ? 'bg-blue-500/10 text-[#0071E3]'
                                : item.category === 'courier'
                                ? 'bg-purple-500/10 text-purple-600 dark:text-purple-400'
                                : item.category === 'reviews'
                                ? 'bg-yellow-500/10 text-yellow-600'
                                : item.category === 'coupons'
                                ? 'bg-emerald-500/10 text-emerald-600'
                                : 'bg-cyan-500/10 text-cyan-600'
                            }`}>
                              {item.category === 'claims' && <RotateCcw className="w-5 h-5" />}
                              {item.category === 'orders' && <ShoppingBag className="w-5 h-5" />}
                              {item.category === 'courier' && <Truck className="w-5 h-5" />}
                              {item.category === 'reviews' && <Star className="w-5 h-5" />}
                              {item.category === 'coupons' && <Tag className="w-5 h-5" />}
                              {item.category === 'security' && <ShieldCheck className="w-5 h-5" />}
                            </div>

                            <div className="space-y-1">
                              <div className="flex items-center gap-2 flex-wrap">
                                <span className="text-sm font-bold text-[#1D1D1F] dark:text-white">
                                  {item.title}
                                </span>
                                <span className={`px-2 py-0.5 rounded-full text-[10px] font-mono font-bold uppercase tracking-wider ${
                                  item.category === 'claims'
                                    ? 'bg-amber-100 dark:bg-amber-900/30 text-amber-700 dark:text-amber-300'
                                    : item.category === 'orders'
                                    ? 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300'
                                    : item.category === 'courier'
                                    ? 'bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300'
                                    : item.category === 'reviews'
                                    ? 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-800 dark:text-yellow-300'
                                    : item.category === 'coupons'
                                    ? 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300'
                                    : 'bg-cyan-100 dark:bg-cyan-900/30 text-cyan-700 dark:text-cyan-300'
                                }`}>
                                  {item.category}
                                </span>
                                {isUnread && (
                                  <span className="w-2 h-2 rounded-full bg-[#0071E3] animate-pulse" title="Unread notification" />
                                )}
                              </div>

                              <p className="text-xs text-[#6E6E73] dark:text-[#A1A1A6] leading-relaxed">
                                {item.message}
                              </p>

                              <div className="text-[11px] font-mono text-[#86868B] pt-0.5">
                                {new Date(item.timestamp).toLocaleString('en-GB', {
                                  day: 'numeric',
                                  month: 'short',
                                  year: 'numeric',
                                  hour: '2-digit',
                                  minute: '2-digit'
                                })}
                              </div>
                            </div>
                          </div>

                          {/* Quick Actions */}
                          <div className="flex items-center gap-2 self-end sm:self-center">
                            {item.linkTab && (
                              <button
                                onClick={() => {
                                  handleToggleNotificationRead(item.id);
                                  setActiveTab(item.linkTab as any);
                                }}
                                className="px-3 py-1.5 rounded-xl bg-[#0071E3]/10 hover:bg-[#0077ED] text-[#0071E3] hover:text-white text-xs font-bold transition-all flex items-center gap-1"
                              >
                                <span>Inspect</span>
                                <ArrowRight className="w-3.5 h-3.5" />
                              </button>
                            )}
                            <button
                              onClick={() => handleToggleNotificationRead(item.id)}
                              className={`p-1.5 rounded-xl text-xs font-semibold transition-colors ${
                                isUnread 
                                  ? 'text-gray-400 hover:text-emerald-600 hover:bg-emerald-50 dark:hover:bg-emerald-950/30' 
                                  : 'text-emerald-600 bg-emerald-50 dark:bg-emerald-950/30'
                              }`}
                              title={isUnread ? 'Mark as read' : 'Mark as unread'}
                            >
                              <CheckCircle2 className="w-4 h-4" />
                            </button>
                          </div>
                        </div>
                      );
                    })
                )}
              </div>
            </div>
          )}"""

old_founder_tab_end = """                <button
                  type="submit"
                  className="px-8 py-3 rounded-full bg-[#0071E3] hover:bg-[#0077ED] text-white font-bold text-sm tracking-wide shadow-md transition-all active:scale-95"
                >
                  Save Vision Profile
                </button>
              </form>
            </div>
          )}"""

base_code = base_code.replace(old_founder_tab_end, old_founder_tab_end + "\n\n" + tab_8_9_10, 1)

# 10. Update Edit Profile Modal for Password changes and Emergency Reset
old_edit_modal_pwd = """                <div>
                  <div className="flex items-center justify-between mb-1">
                    <label className="text-xs font-bold text-[#1D1D1F] dark:text-white">
                      Current Password {profileForm.password ? <span className="text-red-500 font-bold">* (Required)</span> : <span className="text-gray-400 font-normal">(Optional unless changing password)</span>}
                    </label>
                    <button
                      type="button"
                      onClick={() => alert(`Password recovery link has been dispatched to: ${profileForm.email}`)}
                      className="text-[11px] text-[#0071E3] hover:underline font-semibold"
                    >
                      Forgot Password?
                    </button>
                  </div>
                  <input
                    type="password"
                    value={profileCurrentPassword}
                    onChange={(e) => setProfileCurrentPassword(e.target.value)}
                    placeholder={profileForm.password ? "Enter your current password to verify" : "Only needed if changing password"}
                    className="w-full px-4 py-2.5 rounded-xl bg-white dark:bg-black/20 border border-black/10 dark:border-white/10 text-sm font-mono text-[#1D1D1F] dark:text-white focus:outline-none focus:border-[#0071E3]"
                  />
                </div>"""

new_edit_modal_pwd = """                <div>
                  <div className="flex items-center justify-between mb-1">
                    <label className="text-xs font-bold text-[#1D1D1F] dark:text-white flex items-center gap-1.5 flex-wrap">
                      <span>Current Password</span>
                      {profileForm.password ? (
                        <span className="text-red-500 font-bold">* (Required)</span>
                      ) : (
                        <span className="text-gray-400 font-normal">(Optional unless changing password)</span>
                      )}
                      <span className="text-[10px] text-amber-700 dark:text-amber-400 font-mono font-semibold bg-amber-100 dark:bg-amber-900/30 px-1.5 py-0.5 rounded">
                        Default: AdminOps2026!
                      </span>
                    </label>
                    <div className="flex items-center gap-2">
                      <button
                        type="button"
                        onClick={() => setShowCurrentPassword(!showCurrentPassword)}
                        className="text-[11px] text-[#0071E3] font-medium"
                      >
                        {showCurrentPassword ? 'Hide' : 'Show'}
                      </button>
                      <button
                        type="button"
                        onClick={() => {
                          setResetModalMessage('');
                          setIsResetPasswordModalOpen(true);
                        }}
                        className="text-[11px] text-[#0071E3] hover:underline font-semibold"
                      >
                        Forgot Password?
                      </button>
                    </div>
                  </div>
                  <input
                    type={showCurrentPassword ? 'text' : 'password'}
                    value={profileCurrentPassword}
                    onChange={(e) => setProfileCurrentPassword(e.target.value)}
                    placeholder={profileForm.password ? "Enter your current password (e.g. AdminOps2026!)" : "Only needed if changing password"}
                    className="w-full px-4 py-2.5 rounded-xl bg-white dark:bg-black/20 border border-black/10 dark:border-white/10 text-sm font-mono text-[#1D1D1F] dark:text-white focus:outline-none focus:border-[#0071E3]"
                  />
                </div>"""
base_code = base_code.replace(old_edit_modal_pwd, new_edit_modal_pwd, 1)

# 11. Add Modals: Coupon Modal, Reset Password Modal, RMA Claim Detail Modal before </div>\n  );\n}
all_modals = """      {/* =========================================================
          COUPON CREATION & GOVERNANCE MODAL
          ========================================================= */}
      {isCouponModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-fade-in">
          <div className="relative w-full max-w-xl bg-white dark:bg-[#141A2E] rounded-3xl border border-black/10 dark:border-white/15 shadow-2xl p-6 sm:p-8 max-h-[90vh] overflow-y-auto space-y-6">
            
            <div className="flex items-center justify-between pb-3 border-b border-black/[0.08] dark:border-white/10">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-2xl bg-blue-500/10 text-[#0071E3] flex items-center justify-center">
                  <Tag className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-xl font-extrabold text-[#1D1D1F] dark:text-white">Create Promo Coupon</h3>
                  <p className="text-xs text-[#86868B] mt-0.5">
                    Configure discount percentage or flat amount, minimum spend, and validity duration.
                  </p>
                </div>
              </div>
              <button
                onClick={() => setIsCouponModalOpen(false)}
                className="p-1.5 rounded-full bg-[#F5F5F7] dark:bg-white/10 text-[#86868B] hover:text-[#1D1D1F]"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleSaveCoupon} className="space-y-4">
              
              <div>
                <label className="block text-xs font-bold text-[#1D1D1F] dark:text-white mb-1 uppercase tracking-wider">
                  Coupon Code *
                </label>
                <input
                  type="text"
                  required
                  value={couponForm.code}
                  onChange={(e) => setCouponForm({ ...couponForm, code: e.target.value.toUpperCase().replace(/[^A-Z0-9_-]/g, '') })}
                  placeholder="e.g. NEXORA20, EID500, FREESHIP"
                  className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] dark:bg-white/5 border border-black/10 dark:border-white/10 text-sm font-mono font-bold text-[#1D1D1F] dark:text-white focus:outline-none focus:border-[#0071E3] tracking-widest uppercase"
                />
                <span className="text-[11px] text-[#86868B] mt-1 block">
                  Customers will enter this code at checkout. Capital letters and numbers only.
                </span>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-bold text-[#1D1D1F] dark:text-white mb-1 uppercase tracking-wider">
                    Discount Type *
                  </label>
                  <select
                    value={couponForm.type}
                    onChange={(e) => setCouponForm({ ...couponForm, type: e.target.value as any })}
                    className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] dark:bg-white/5 border border-black/10 dark:border-white/10 text-sm font-bold text-[#1D1D1F] dark:text-white focus:outline-none focus:border-[#0071E3]"
                  >
                    <option value="percent" className="text-black">Percentage Discount (%)</option>
                    <option value="flat" className="text-black">Flat Amount Discount (৳)</option>
                    <option value="freeship" className="text-black">Free Shipping Waiver</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-bold text-[#1D1D1F] dark:text-white mb-1 uppercase tracking-wider">
                    {couponForm.type === 'percent' ? 'Discount Percentage (%) *' : couponForm.type === 'flat' ? 'Discount Amount (৳) *' : 'Shipping Waiver'}
                  </label>
                  <input
                    type="number"
                    required={couponForm.type !== 'freeship'}
                    disabled={couponForm.type === 'freeship'}
                    value={couponForm.type === 'freeship' ? 0 : couponForm.value}
                    onChange={(e) => setCouponForm({ ...couponForm, value: Number(e.target.value) })}
                    placeholder={couponForm.type === 'percent' ? '10 (means 10%)' : '500 (means ৳500)'}
                    className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] dark:bg-white/5 border border-black/10 dark:border-white/10 text-sm font-mono font-bold text-[#1D1D1F] dark:text-white focus:outline-none focus:border-[#0071E3] disabled:opacity-50"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-[#1D1D1F] dark:text-white mb-1 uppercase tracking-wider">
                  Validity Duration (Days) *
                </label>
                <div className="flex flex-wrap items-center gap-2 mb-2">
                  {[7, 15, 30, 60, 90, 180, 365].map((d) => (
                    <button
                      key={d}
                      type="button"
                      onClick={() => setCouponForm({ ...couponForm, durationDays: d })}
                      className={`px-3 py-1 rounded-lg text-xs font-bold transition-all ${
                        couponForm.durationDays === d
                          ? 'bg-[#0071E3] text-white shadow-sm'
                          : 'bg-[#F5F5F7] dark:bg-white/10 text-[#6E6E73] dark:text-[#A1A1A6] hover:bg-black/5 dark:hover:bg-white/15'
                      }`}
                    >
                      {d} Days
                    </button>
                  ))}
                </div>
                <div className="flex items-center gap-3">
                  <input
                    type="number"
                    min="1"
                    max="1000"
                    required
                    value={couponForm.durationDays}
                    onChange={(e) => setCouponForm({ ...couponForm, durationDays: Number(e.target.value) })}
                    className="w-28 px-4 py-2 rounded-xl bg-[#F5F5F7] dark:bg-white/5 border border-black/10 dark:border-white/10 text-sm font-mono font-bold text-[#1D1D1F] dark:text-white focus:outline-none focus:border-[#0071E3]"
                  />
                  <div className="text-xs text-[#86868B] font-mono">
                    Calculated expiry: <strong className="text-[#1D1D1F] dark:text-white">
                      {new Date(Date.now() + (couponForm.durationDays || 30) * 86400000).toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' })}
                    </strong>
                  </div>
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-[#1D1D1F] dark:text-white mb-1 uppercase tracking-wider">
                  Minimum Order Spend (৳)
                </label>
                <input
                  type="number"
                  min="0"
                  value={couponForm.minSpend}
                  onChange={(e) => setCouponForm({ ...couponForm, minSpend: Number(e.target.value) })}
                  placeholder="0 (means no minimum spend required)"
                  className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] dark:bg-white/5 border border-black/10 dark:border-white/10 text-sm font-mono text-[#1D1D1F] dark:text-white focus:outline-none focus:border-[#0071E3]"
                />
                <span className="text-[11px] text-[#86868B] mt-1 block">
                  Customer cart must be at least this amount to apply this coupon. Enter 0 for no threshold.
                </span>
              </div>

              <div>
                <label className="block text-xs font-bold text-[#1D1D1F] dark:text-white mb-1 uppercase tracking-wider">
                  Coupon Description / Campaign Note
                </label>
                <input
                  type="text"
                  value={couponForm.description}
                  onChange={(e) => setCouponForm({ ...couponForm, description: e.target.value })}
                  placeholder="e.g. 10% Flagship Hardware Launch Promotion"
                  className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] dark:bg-white/5 border border-black/10 dark:border-white/10 text-sm text-[#1D1D1F] dark:text-white focus:outline-none focus:border-[#0071E3]"
                />
              </div>

              <div className="flex items-center gap-2 pt-1">
                <input
                  type="checkbox"
                  id="coupon-active-check"
                  checked={couponForm.active}
                  onChange={(e) => setCouponForm({ ...couponForm, active: e.target.checked })}
                  className="w-4 h-4 rounded text-[#0071E3] focus:ring-0"
                />
                <label htmlFor="coupon-active-check" className="text-xs font-bold text-[#1D1D1F] dark:text-white cursor-pointer select-none">
                  Activate coupon immediately for customer checkout
                </label>
              </div>

              <div className="pt-4 border-t border-black/[0.08] dark:border-white/10 flex items-center justify-end gap-3">
                <button
                  type="button"
                  onClick={() => setIsCouponModalOpen(false)}
                  className="px-5 py-2.5 rounded-full border border-black/15 dark:border-white/20 text-sm font-semibold hover:bg-black/5 dark:hover:bg-white/5 transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-7 py-2.5 rounded-full bg-[#0071E3] hover:bg-[#0077ED] text-white font-bold text-sm tracking-wide shadow-md transition-all active:scale-95 flex items-center gap-1.5"
                >
                  <Check className="w-4 h-4" />
                  <span>Generate &amp; Deploy Coupon</span>
                </button>
              </div>

            </form>
          </div>
        </div>
      )}

      {/* =========================================================
          EMERGENCY ADMIN PASSWORD RESET MODAL
          ========================================================= */}
      {isResetPasswordModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-fade-in">
          <div className="relative w-full max-w-md bg-white dark:bg-[#141A2E] rounded-3xl border border-black/10 dark:border-white/15 shadow-2xl p-6 sm:p-7 space-y-5">
            
            <div className="flex items-center justify-between pb-3 border-b border-black/[0.08] dark:border-white/10">
              <div className="flex items-center gap-2.5">
                <div className="w-9 h-9 rounded-xl bg-amber-500/10 text-amber-600 flex items-center justify-center">
                  <Key className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-lg font-extrabold text-[#1D1D1F] dark:text-white">Reset Admin Password</h3>
                  <p className="text-[11px] text-[#86868B]">Official Nexora Security Recovery</p>
                </div>
              </div>
              <button
                onClick={() => setIsResetPasswordModalOpen(false)}
                className="p-1.5 rounded-full bg-[#F5F5F7] dark:bg-white/10 text-[#86868B] hover:text-[#1D1D1F]"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-3 text-xs text-[#1D1D1F] dark:text-slate-300">
              <p className="leading-relaxed">
                Forgot your current password or having difficulty authenticating? You can securely reset this administrator account credentials to the factory-preset temporary password:
              </p>

              <div className="p-3.5 rounded-2xl bg-slate-100 dark:bg-white/5 border border-black/10 dark:border-white/10 space-y-1 font-mono">
                <div>Account: <strong className="text-[#0071E3]">{profileForm.username || 'admin'}</strong></div>
                <div>Notification Email: <strong className="text-[#1D1D1F] dark:text-white">{profileForm.email || 'support@nexora.com'}</strong></div>
                <div>Default Reset Credential: <strong className="text-emerald-600 dark:text-emerald-400 font-bold">Nexora2026!</strong></div>
              </div>

              {resetModalMessage && (
                <div className={`p-3 rounded-xl text-xs font-semibold ${resetModalSuccess ? 'bg-emerald-50 text-emerald-800 border border-emerald-200' : 'bg-red-50 text-red-800 border border-red-200'}`}>
                  {resetModalMessage}
                </div>
              )}
            </div>

            <div className="pt-2 flex flex-col gap-2">
              <button
                type="button"
                disabled={resetLoading}
                onClick={handlePerformPasswordReset}
                className="w-full py-3 rounded-full bg-[#0071E3] hover:bg-[#0077ED] text-white font-bold text-xs tracking-wide shadow-md transition-all active:scale-95 flex items-center justify-center gap-2 disabled:opacity-50"
              >
                <RefreshCw className={`w-3.5 h-3.5 ${resetLoading ? 'animate-spin' : ''}`} />
                <span>{resetLoading ? 'Authorizing Reset...' : 'Authorize Instant Password Reset'}</span>
              </button>

              {resetModalSuccess && (
                <button
                  type="button"
                  onClick={() => setIsResetPasswordModalOpen(false)}
                  className="w-full py-2.5 rounded-full bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs tracking-wide transition-all"
                >
                  Apply &amp; Return to Profile Settings
                </button>
              )}
            </div>

          </div>
        </div>
      )}

      {/* =========================================================
          RMA CLAIM DETAILS & RESOLUTION MODAL
          ========================================================= */}
      {selectedClaimDetail && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-fade-in">
          <div className="relative w-full max-w-lg bg-white dark:bg-[#141A2E] rounded-3xl border border-black/10 dark:border-white/15 shadow-2xl p-6 sm:p-7 space-y-5 max-h-[90vh] overflow-y-auto">
            
            <div className="flex items-center justify-between pb-3 border-b border-black/[0.08] dark:border-white/10">
              <div className="flex items-center gap-2.5">
                <div className="w-10 h-10 rounded-2xl bg-amber-500/10 text-amber-600 dark:text-amber-400 flex items-center justify-center">
                  <RotateCcw className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-lg font-extrabold text-[#1D1D1F] dark:text-white">RMA Claim Details</h3>
                  <p className="text-xs font-mono text-[#86868B]">{selectedClaimDetail.id} • Order #{selectedClaimDetail.orderId}</p>
                </div>
              </div>
              <button
                onClick={() => setSelectedClaimDetail(null)}
                className="p-1.5 rounded-full bg-[#F5F5F7] dark:bg-white/10 text-[#86868B] hover:text-[#1D1D1F]"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-4 text-xs">
              <div className="p-4 rounded-2xl bg-slate-50 dark:bg-white/5 border border-black/[0.06] dark:border-white/10 space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-[#86868B]">Customer Name:</span>
                  <span className="font-bold text-[#1D1D1F] dark:text-white text-sm">{selectedClaimDetail.customerName}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-[#86868B]">Phone Number:</span>
                  <div className="flex items-center gap-2">
                    <span className="font-mono font-bold text-[#1D1D1F] dark:text-white">{selectedClaimDetail.customerPhone}</span>
                    {selectedClaimDetail.customerPhone && (
                      <a
                        href={`https://wa.me/${selectedClaimDetail.customerPhone.replace(/[^0-9]/g, '')}`}
                        target="_blank"
                        rel="noreferrer"
                        className="px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-600 font-bold hover:bg-emerald-500 hover:text-white transition-colors"
                      >
                        WhatsApp
                      </a>
                    )}
                  </div>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-[#86868B]">Date Submitted:</span>
                  <span className="font-mono text-[#1D1D1F] dark:text-white">
                    {selectedClaimDetail.createdAt ? new Date(selectedClaimDetail.createdAt).toLocaleString('en-GB') : 'N/A'}
                  </span>
                </div>
              </div>

              <div>
                <label className="block text-[#86868B] font-bold uppercase tracking-wider text-[11px] mb-1">
                  Hardware Issue Category
                </label>
                <div className="p-3 rounded-xl bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-700/30 font-semibold text-amber-900 dark:text-amber-300">
                  {selectedClaimDetail.issueType}
                </div>
              </div>

              <div>
                <label className="block text-[#86868B] font-bold uppercase tracking-wider text-[11px] mb-1">
                  Customer Problem Description
                </label>
                <div className="p-3.5 rounded-xl bg-[#F5F5F7] dark:bg-black/30 border border-black/10 dark:border-white/10 text-[#1D1D1F] dark:text-slate-200 font-mono text-xs leading-relaxed whitespace-pre-wrap">
                  {selectedClaimDetail.description}
                </div>
              </div>

              <div>
                <label className="block text-[#86868B] font-bold uppercase tracking-wider text-[11px] mb-1.5">
                  Update Claim Status
                </label>
                <div className="grid grid-cols-2 gap-2">
                  {(['Under Review', 'Approved for Pickup', 'Replacement Dispatched', 'Resolved'] as const).map((st) => (
                    <button
                      key={st}
                      type="button"
                      onClick={() => {
                        handleClaimStatusChange(selectedClaimDetail.id, st);
                        setSelectedClaimDetail(prev => prev ? { ...prev, status: st } : null);
                      }}
                      className={`px-3 py-2 rounded-xl text-xs font-bold transition-all border ${
                        selectedClaimDetail.status === st
                          ? 'bg-[#0071E3] text-white border-[#0071E3] shadow-md'
                          : 'bg-white dark:bg-white/5 text-[#6E6E73] dark:text-[#A1A1A6] border-black/10 dark:border-white/10 hover:bg-black/5 dark:hover:bg-white/10'
                      }`}
                    >
                      {st}
                    </button>
                  ))}
                </div>
              </div>
            </div>

            <div className="pt-3 border-t border-black/[0.08] dark:border-white/10 flex justify-end">
              <button
                type="button"
                onClick={() => setSelectedClaimDetail(null)}
                className="px-6 py-2.5 rounded-full bg-[#1D1D1F] hover:bg-[#333336] text-white text-xs font-bold tracking-wide"
              >
                Close Ticket
              </button>
            </div>

          </div>
        </div>
      )}
"""

end_of_file = "\n    </div>\n  );\n}"
end_pos = base_code.rfind(end_of_file)
if end_pos != -1:
    base_code = base_code[:end_pos] + "\n" + all_modals + end_of_file
else:
    print("Could not find end_of_file token")

# Write directly to frontend/src/app/myadminerapanel/page.tsx
target_file = "frontend/src/app/myadminerapanel/page.tsx"
with open(target_file, "w", encoding="utf-8") as f:
    f.write(base_code)

print("Successfully written final enhanced admin panel to:", target_file)

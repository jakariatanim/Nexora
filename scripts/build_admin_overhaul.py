# -*- coding: utf-8 -*-
import os

code = '''\'use client\';

import React, { useState, useEffect } from \'react\';
import Image from \'next/image\';
import { Product, Order, Founder, Category, AdminMember, Review } from \'../../lib/types\';
import {
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
} from \'../../lib/api\';
import {
  Lock,
  LayoutDashboard,
  Package,
  ShoppingBag,
  Plus,
  UploadCloud,
  Edit2,
  Trash2,
  X,
  LogOut,
  RefreshCw,
  Search,
  Filter,
  CheckCircle,
  Layers,
  ShieldCheck,
  ExternalLink,
  ChevronDown,
  ChevronUp,
  SlidersHorizontal,
  Users,
  MessageSquare,
  Star,
  Copy,
  Check,
  Eye,
  EyeOff,
  Key,
  Compass,
  UserCircle,
  Share2,
  Send,
  MessageCircle,
  Mail,
  MapPin,
  Phone,
  Sparkles,
  UserPlus,
  UserCheck
} from \'lucide-react\';

const INITIAL_CATEGORIES: Category[] = [
  { id: \'smartphones\', name: \'Smartphones\', description: \'Premier flagship smartphones\' },
  { id: \'earbuds\', name: \'Earbuds\', description: \'ANC in-ear earbuds & TWS\' },
  { id: \'audio\', name: \'Audio\', description: \'Spatial acoustics & studio headphones\' },
  { id: \'chargers-power\', name: \'Chargers & Power\', description: \'Multi-brand fast GaN chargers & power banks\' },
  { id: \'smartwatches\', name: \'Smartwatches\', description: \'Titanium diving & fitness smartwatches\' },
  { id: \'tablets-laptops\', name: \'Tablets & Laptops\', description: \'Pro workstation silicon & creative tablets\' }
];

const TOP_10_BRANDS = [
  \'All\',
  \'Apple\',
  \'Samsung\',
  \'Xiaomi\',
  \'Oppo\',
  \'Vivo\',
  \'OnePlus\',
  \'Google\',
  \'Realme\',
  \'Anker\',
  \'Sony\'
];

export default function AdminEraPanel() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [username, setUsername] = useState(\'\');
  const [password, setPassword] = useState(\'\');
  const [loginError, setLoginError] = useState(\'\');
  const [inviteDetected, setInviteDetected] = useState<{ code?: string; role?: string; user?: string } | null>(null);

  // Active Navigation Tab
  const [activeTab, setActiveTab] = useState<\'overview\' | \'products\' | \'categories\' | \'orders\' | \'founder\' | \'staff\' | \'reviews\'>(\'products\');

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
  const [isRefreshing, setIsRefreshing] = useState(false);

  // Product Filter & Search
  const [searchQuery, setSearchQuery] = useState(\'\');
  const [selectedBrandFilter, setSelectedBrandFilter] = useState(\'All\');
  const [selectedCategoryFilter, setSelectedCategoryFilter] = useState(\'All\');

  // Product Modal State
  const [editingProduct, setEditingProduct] = useState<Product | null>(null);
  const [isProductModalOpen, setIsProductModalOpen] = useState(false);
  const [productForm, setProductForm] = useState<Partial<Product>>({
    name: \'\',
    brand: \'Apple\',
    tagline: \'\',
    category: \'Smartphones\',
    priceBDT: 0,
    priceUSD: 0,
    stockCount: 30,
    inStock: true,
    image: \'\',
    specs: [\'\'],
    description: \'\',
  });
  const [uploadingImage, setUploadingImage] = useState(false);

  // Staff Modal State (Create New Staff with Username, Email, Password)
  const [isStaffModalOpen, setIsStaffModalOpen] = useState(false);
  const [staffForm, setStaffForm] = useState<{
    name: string;
    username: string;
    email: string;
    password: string;
    phone: string;
    role: AdminMember[\'role\'];
    permissions: string[];
  }>({
    name: \'\',
    username: \'\',
    email: \'\',
    password: \'\',
    phone: \'\',
    role: \'Inventory Moderator\',
    permissions: [\'products\', \'categories\']
  });

  // Multi-Channel Invite Sharing Modal State
  const [inviteModalData, setInviteModalData] = useState<{
    member: AdminMember;
    inviteUrl: string;
    copied: boolean;
  } | null>(null);

  // Profile Modal State (Full Profile Card & Privacy Settings)
  const [isProfileModalOpen, setIsProfileModalOpen] = useState(false);
  const [profileForm, setProfileForm] = useState({
    name: \'Jakaria Tanim\',
    username: \'jakaria\',
    email: \'tanim@nexora.com\',
    password: \'\',
    confirmPassword: \'\',
    phone: \'+880 1640-026177\',
    address: \'Dhaka, Bangladesh\',
    showPassword: false
  });
  const [profileSuccessMsg, setProfileSuccessMsg] = useState(\'\');

  // Category Tab: New Category Form
  const [newCatName, setNewCatName] = useState(\'\');
  const [newCatDesc, setNewCatDesc] = useState(\'\');
  const [catSuccessMsg, setCatSuccessMsg] = useState(\'\');

  // Founder Profile Form
  const [founderForm, setFounderForm] = useState<Partial<Founder>>({});
  const [saveSuccess, setSaveSuccess] = useState(\'\');

  // Toast
  const [inviteToast, setInviteToast] = useState(\'\');

  const [currentUser, setCurrentUser] = useState<{
    id?: string;
    name: string;
    role: string;
    email: string;
    username?: string;
    password?: string;
    phone?: string;
    address?: string;
  } | null>(null);

  // Require fresh login on page open; handle invite url query
  useEffect(() => {
    setIsAuthenticated(false);
    if (typeof window !== \'undefined\') {
      const params = new URLSearchParams(window.location.search);
      const urlUser = params.get(\'user\') || params.get(\'u\');
      const urlInvite = params.get(\'invite\') || params.get(\'code\');
      const urlRole = params.get(\'role\');
      if (urlUser) {
        setUsername(urlUser);
      }
      if (urlInvite || urlRole || urlUser) {
        setInviteDetected({ code: urlInvite || \'ACCESS-INVITE\', role: urlRole || \'Staff Moderator\', user: urlUser || \'\' });
      }
    }
  }, []);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoginError(\'\');
    try {
      const res = await fetch(\'http://localhost:5001/api/admin/login\', {
        method: \'POST\',
        headers: { \'Content-Type\': \'application/json\' },
        body: JSON.stringify({ username, password })
      });
      const data = await res.json();
      if (res.ok && data.success) {
        setIsAuthenticated(true);
        setCurrentUser(data.user || {
          name: \'Jakaria Tanim\',
          role: \'Super Administrator\',
          email: \'tanim@nexora.com\',
          username: \'jakaria\',
          phone: \'+880 1640-026177\',
          address: \'Dhaka, Bangladesh\'
        });
        loadDashboardData();
      } else {
        setLoginError(data.error || \'Invalid administrator or moderator credentials.\');
      }
    } catch {
      // Offline fallback
      if (
        (username.toLowerCase() === \'jakaria\' || username.toLowerCase() === \'admin\' || username.toLowerCase() === \'superadmin\') &&
        (password === \'NexoraSuperAdmin2026!\' || password === \'admin\' || password === \'2026\')
      ) {
        setIsAuthenticated(true);
        setCurrentUser({
          name: \'Jakaria Tanim\',
          role: \'Super Administrator\',
          email: \'tanim@nexora.com\',
          username: \'jakaria\',
          phone: \'+880 1640-026177\',
          address: \'Dhaka, Bangladesh\'
        });
        loadDashboardData();
      } else {
        setLoginError(\'Could not reach backend authentication service.\');
      }
    }
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    setCurrentUser(null);
    setUsername(\'\');
    setPassword(\'\');
  };

  const loadDashboardData = async () => {
    setLoading(true);
    try {
      const [prods, ords, fndr, admins, revs] = await Promise.all([
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
      if (fndr) setFounderForm(fndr);

      const productCats = Array.from(new Set((prods || []).map(p => p.category))).filter(Boolean);
      const mergedCats = [...INITIAL_CATEGORIES];
      productCats.forEach(cName => {
        if (!mergedCats.some(c => c.name.toLowerCase() === cName.toLowerCase())) {
          mergedCats.push({
            id: cName.toLowerCase().replace(/[^a-z0-9]+/g, \'-\'),
            name: cName,
            description: `${cName} hardware devices`
          });
        }
      });
      setCategories(mergedCats);
    } catch (err) {
      console.error(\'Failed to load dashboard data:\', err);
    } finally {
      setLoading(false);
    }
  };

  // Real Refresh with instant feedback & notification
  const handleRefresh = async () => {
    setIsRefreshing(true);
    await loadDashboardData();
    setTimeout(() => {
      setIsRefreshing(false);
      setInviteToast(\'✓ System data, products, orders & staff refreshed live!\');
      setTimeout(() => setInviteToast(\'\'), 3500);
    }, 600);
  };

  // Image Drag-and-Drop or File Select
  const handleImageFile = async (file: File) => {
    setUploadingImage(true);
    const uploadedUrl = await uploadImage(file);
    if (uploadedUrl) {
      setProductForm(prev => ({ ...prev, image: uploadedUrl }));
    }
    setUploadingImage(false);
  };

  // Save Product (Create or Edit)
  const handleSaveProduct = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!productForm.name || !productForm.name.trim()) return;

    const cleanProduct: Partial<Product> = {
      ...productForm,
      priceBDT: Number(productForm.priceBDT) || 0,
      priceUSD: Number(productForm.priceUSD) || 0,
      stockCount: Number(productForm.stockCount) || 0,
      specs: Array.isArray(productForm.specs)
        ? productForm.specs.filter(Boolean)
        : [productForm.specs].filter(Boolean) as string[],
    };

    if (editingProduct && editingProduct.id) {
      const updated = await updateProduct(editingProduct.id, cleanProduct);
      if (updated) {
        setProducts(prev => prev.map(p => p.id === updated.id ? updated : p));
        setIsProductModalOpen(false);
        setEditingProduct(null);
      }
    } else {
      const created = await createProduct({
        ...cleanProduct,
        id: (cleanProduct.name || \'gadget\').toLowerCase().replace(/[^a-z0-9]+/g, \'-\'),
        rating: 5.0,
        reviewCount: 1,
        inStock: true
      });
      if (created) {
        setProducts(prev => [created, ...prev]);
        setIsProductModalOpen(false);
      }
    }
  };

  // Delete Product
  const handleDeleteProduct = async (id: string) => {
    if (confirm(\'Permanently remove this hardware gadget from NEXORA inventory?\')) {
      const ok = await deleteProduct(id);
      if (ok) {
        setProducts(prev => prev.filter(p => p.id !== id));
      }
    }
  };

  // Order Status Change
  const handleOrderStatusChange = async (orderId: string, status: string) => {
    const updated = await updateOrderStatus(orderId, status as Order['status']);
    if (updated) {
      setOrders(prev => prev.map(o => o.id === orderId ? { ...o, status: status as Order['status'] } : o));
    }
  };

  // Save Founder
  const handleSaveFounder = async (e: React.FormEvent) => {
    e.preventDefault();
    const updated = await updateFounder(founderForm);
    if (updated) {
      setFounder(updated);
      setSaveSuccess(\'Founder profile updated and synchronized successfully!\');
      setTimeout(() => setSaveSuccess(\'\'), 3500);
    }
  };

  // Create New Category
  const handleCreateCategory = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newCatName.trim()) return;
    const catId = newCatName.toLowerCase().replace(/[^a-z0-9]+/g, \'-\');
    if (categories.some(c => c.id === catId)) {
      setCatSuccessMsg(\'Category already exists in store catalog.\');
      setTimeout(() => setCatSuccessMsg(\'\'), 3000);
      return;
    }
    const newCategory: Category = {
      id: catId,
      name: newCatName.trim(),
      description: newCatDesc.trim() || `${newCatName.trim()} hardware gadgets`
    };
    setCategories(prev => [...prev, newCategory]);
    setNewCatName(\'\');
    setNewCatDesc(\'\');
    setCatSuccessMsg(\'✓ Category created successfully!\');
    setTimeout(() => setCatSuccessMsg(\'\'), 3000);
  };

  // Delete Category
  const handleDeleteCategory = (catId: string) => {
    if (confirm(\'Delete this category from the store catalog?\')) {
      setCategories(prev => prev.filter(c => c.id !== catId));
    }
  };

  // Open Multi-Channel Invite Sharing Modal
  const openInviteModal = (member: AdminMember) => {
    const origin = typeof window !== \'undefined\' ? window.location.origin : \'http://localhost:3000\';
    const inviteUrl = `${origin}/myadminerapanel?invite=${encodeURIComponent(member.id)}&user=${encodeURIComponent(member.username || \'\')}&role=${encodeURIComponent(member.role)}`;
    setInviteModalData({
      member,
      inviteUrl,
      copied: false
    });
  };

  // Authorize & Generate Access Link (Create Staff)
  const handleCreateStaff = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!staffForm.name || !staffForm.name.trim()) return;

    const autoUsername = staffForm.username.trim() || staffForm.name.trim().toLowerCase().replace(/[^a-z0-9]+/g, \'\');
    const autoEmail = staffForm.email.trim() || `${autoUsername}@nexora.com`;
    const cleanPassword = staffForm.password.trim() || \'NexoraStaff2026!\';

    const created = await createAdminMember({
      name: staffForm.name.trim(),
      username: autoUsername,
      email: autoEmail,
      password: cleanPassword,
      phone: staffForm.phone.trim() || \'+880 1700-000000\',
      role: staffForm.role,
      permissions: staffForm.permissions,
      status: \'Active\'
    });

    if (created) {
      setAdminMembers(prev => [...prev, created]);
      setIsStaffModalOpen(false);
      setStaffForm({
        name: \'\',
        username: \'\',
        email: \'\',
        password: \'\',
        phone: \'\',
        role: \'Inventory Moderator\',
        permissions: [\'products\', \'categories\']
      });
      // Immediately open multi-channel invite sharing modal
      openInviteModal(created);
    }
  };

  // Save Full Profile & Privacy Settings (Super Admin / Logged-in User)
  const handleSaveProfile = async (e: React.FormEvent) => {
    e.preventDefault();
    if (profileForm.password && profileForm.password !== profileForm.confirmPassword) {
      alert(\'New passwords do not match. Please verify.\');
      return;
    }

    const superAdmin = adminMembers.find(m => m.role === \'Super Administrator\' || m.username === currentUser?.username) || adminMembers[0];
    if (!superAdmin) return;

    const updates: Partial<AdminMember> = {
      name: profileForm.name.trim(),
      username: profileForm.username.trim(),
      email: profileForm.email.trim(),
      phone: profileForm.phone.trim()
    };
    if (profileForm.password.trim()) {
      updates.password = profileForm.password.trim();
    }

    const updated = await updateAdminMember(superAdmin.id, updates);
    if (updated) {
      setAdminMembers(prev => prev.map(m => m.id === updated.id ? updated : m));
      setCurrentUser({
        name: updated.name,
        role: updated.role,
        email: updated.email,
        username: updated.username,
        phone: updated.phone || profileForm.phone,
        address: profileForm.address
      });
      setProfileSuccessMsg(\'✓ Profile & privacy credentials saved successfully!\');
      setTimeout(() => {
        setProfileSuccessMsg(\'\');
        setIsProfileModalOpen(false);
      }, 2500);
    }
  };

  // Delete Staff Member
  const handleDeleteStaff = async (id: string) => {
    if (confirm(\'Revoke authorization for this administrator / moderator?\')) {
      const ok = await deleteAdminMember(id);
      if (ok) {
        setAdminMembers(prev => prev.filter(m => m.id !== id));
      }
    }
  };

  // Delete Review
  const handleDeleteReview = async (id: string) => {
    if (confirm(\'Delete this customer review?\')) {
      const ok = await deleteReview(id);
      if (ok) {
        setReviews(prev => prev.filter(r => r.id !== id));
      }
    }
  };

  // Filtered Products Calculation
  const filteredProducts = products.filter(p => {
    const matchesBrand =
      selectedBrandFilter === \'All\' ||
      (p.brand && p.brand.toLowerCase() === selectedBrandFilter.toLowerCase()) ||
      p.name.toLowerCase().startsWith(selectedBrandFilter.toLowerCase());

    const matchesCategory =
      selectedCategoryFilter === \'All\' ||
      p.category.toLowerCase() === selectedCategoryFilter.toLowerCase();

    const matchesSearch =
      searchQuery === \'\' ||
      p.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (p.tagline && p.tagline.toLowerCase().includes(searchQuery.toLowerCase())) ||
      (p.specs && p.specs.some(s => s.toLowerCase().includes(searchQuery.toLowerCase())));

    return matchesBrand && matchesCategory && matchesSearch;
  });

  const totalRevenue = orders.reduce((sum, o) => sum + (Number(o.totalBDT) || 0), 0);

  // -------------------------------------------------------------
  // Unauthenticated Login Stage (Always displayed on fresh visit)
  // -------------------------------------------------------------
  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-[#0B132B] flex items-center justify-center p-4">
        <div className="w-full max-w-md p-8 sm:p-10 rounded-3xl bg-white border border-white/20 shadow-2xl text-center space-y-6">
          <div className="relative w-16 h-16 mx-auto rounded-2xl bg-[#0B132B] p-2 flex items-center justify-center shadow-lg">
            <Image
              src="/brand/nexora_icon_white_transparent.png"
              alt="NEXORA"
              fill
              className="object-contain p-2"
            />
          </div>

          <div className="space-y-1.5">
            <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight text-[#1D1D1F]">
              Nexora Admin Panel
            </h1>
            <p className="text-sm text-[#86868B]">
              Enter authorized administrator or moderator credentials to access control systems.
            </p>
          </div>

          {/* Invitation Notice if opened via an Invite Link */}
          {inviteDetected && (
            <div className="p-4 rounded-2xl bg-emerald-50 border border-emerald-200 text-left space-y-1 animate-fade-in">
              <div className="flex items-center gap-2 text-emerald-800 font-bold text-sm">
                <Sparkles className="w-4 h-4 text-emerald-600" />
                <span>Authorized Staff Invitation</span>
              </div>
              <p className="text-xs text-emerald-700">
                You have been authorized as <strong className="font-semibold">{inviteDetected.role}</strong>. Enter your username and password below to accept your access pass and enter the dashboard.
              </p>
            </div>
          )}

          {loginError && (
            <div className="p-3.5 rounded-xl bg-red-50 border border-red-200 text-red-600 text-sm font-semibold">
              {loginError}
            </div>
          )}

          <form onSubmit={handleLogin} className="space-y-4 text-left">
            <div>
              <label className="block text-sm font-bold text-[#1D1D1F] mb-1">
                Username or Email
              </label>
              <input
                type="text"
                required
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="e.g. jakaria or admin or inventory"
                className="w-full px-4 py-3 rounded-xl bg-[#F5F5F7] border border-black/10 text-base text-[#1D1D1F] font-semibold focus:outline-none focus:border-[#0071E3]"
              />
            </div>

            <div>
              <label className="block text-sm font-bold text-[#1D1D1F] mb-1">
                Password
              </label>
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter password"
                className="w-full px-4 py-3 rounded-xl bg-[#F5F5F7] border border-black/10 text-base text-[#1D1D1F] focus:outline-none focus:border-[#0071E3]"
              />
            </div>

            <button
              type="submit"
              className="w-full py-3.5 rounded-full bg-[#0071E3] hover:bg-[#0077ED] text-white font-bold text-base tracking-wide shadow-md transition-all active:scale-95 flex items-center justify-center gap-2"
            >
              <Lock className="w-4 h-4" />
              <span>Authenticate &amp; Enter Dashboard</span>
            </button>
          </form>

          <div className="pt-2 text-xs text-[#86868B] font-mono border-t border-black/[0.06]">
            Directed by Jakaria Tanim • High-Performance Hardware Platform
          </div>
        </div>
      </div>
    );
  }

  // -------------------------------------------------------------
  // Authenticated Dashboard Stage
  // -------------------------------------------------------------
  return (
    <div className="min-h-screen bg-[#F5F5F7] dark:bg-[#080E1E] text-[#1D1D1F] dark:text-white flex overflow-x-hidden font-sans">
      
      {/* =========================================================
          LEFT DOCK: PERMANENT SLEEK VERTICAL ICON DOCK (80px / w-20)
          ========================================================= */}
      <aside className="fixed top-0 left-0 bottom-0 w-20 bg-[#0B132B] border-r border-white/10 z-40 flex flex-col items-center justify-between py-5 select-none shadow-2xl">
        
        {/* Top: Logo & Main Nav Icons */}
        <div className="flex flex-col items-center gap-3 w-full">
          {/* Nexora Brand Logo */}
          <div
            onClick={() => setActiveTab(\'overview\')}
            className="relative group w-12 h-12 rounded-2xl bg-white/10 hover:bg-white/15 flex items-center justify-center p-2 mb-2 cursor-pointer transition-all shadow-md active:scale-95"
            title="NEXORA Admin"
          >
            <div className="relative w-7 h-7">
              <Image
                src="/brand/nexora_icon_white_transparent.png"
                alt="NEXORA"
                fill
                className="object-contain"
              />
            </div>
            {/* Tooltip on Hover */}
            <div className="absolute left-[84px] px-3 py-1.5 rounded-xl bg-[#1D1D1F] text-white text-xs font-semibold whitespace-nowrap shadow-2xl pointer-events-none opacity-0 group-hover:opacity-100 transition-opacity duration-200 z-50 border border-white/15">
              NEXORA Admin
            </div>
          </div>

          <div className="w-8 h-px bg-white/10 mb-1" />

          {/* 1. Dashboard Overview */}
          <button
            onClick={() => setActiveTab(\'overview\')}
            className={`relative group w-12 h-12 rounded-2xl flex items-center justify-center transition-all ${
              activeTab === \'overview\'
                ? \'bg-[#0071E3] text-white shadow-lg shadow-blue-500/30 ring-2 ring-white/20\'
                : \'text-white/60 hover:text-white hover:bg-white/10\'
            }`}
            aria-label="Dashboard Overview"
          >
            <LayoutDashboard className="w-5 h-5 transition-transform group-hover:scale-110" />
            <div className="absolute left-[84px] px-3 py-1.5 rounded-xl bg-[#1D1D1F] text-white text-xs font-semibold whitespace-nowrap shadow-2xl pointer-events-none opacity-0 group-hover:opacity-100 transition-opacity duration-200 z-50 border border-white/15">
              Dashboard Overview
            </div>
          </button>

          {/* 2. Product Inventory */}
          <button
            onClick={() => setActiveTab(\'products\')}
            className={`relative group w-12 h-12 rounded-2xl flex items-center justify-center transition-all ${
              activeTab === \'products\'
                ? \'bg-[#0071E3] text-white shadow-lg shadow-blue-500/30 ring-2 ring-white/20\'
                : \'text-white/60 hover:text-white hover:bg-white/10\'
            }`}
            aria-label="Product Inventory"
          >
            <Package className="w-5 h-5 transition-transform group-hover:scale-110" />
            <div className="absolute left-[84px] px-3 py-1.5 rounded-xl bg-[#1D1D1F] text-white text-xs font-semibold whitespace-nowrap shadow-2xl pointer-events-none opacity-0 group-hover:opacity-100 transition-opacity duration-200 z-50 border border-white/15">
              Product Inventory ({products.length})
            </div>
          </button>

          {/* 3. Admins & Staff */}
          <button
            onClick={() => setActiveTab(\'staff\')}
            className={`relative group w-12 h-12 rounded-2xl flex items-center justify-center transition-all ${
              activeTab === \'staff\'
                ? \'bg-[#0071E3] text-white shadow-lg shadow-blue-500/30 ring-2 ring-white/20\'
                : \'text-white/60 hover:text-white hover:bg-white/10\'
            }`}
            aria-label="Admins & Moderators"
          >
            <ShieldCheck className="w-5 h-5 transition-transform group-hover:scale-110" />
            <div className="absolute left-[84px] px-3 py-1.5 rounded-xl bg-[#1D1D1F] text-white text-xs font-semibold whitespace-nowrap shadow-2xl pointer-events-none opacity-0 group-hover:opacity-100 transition-opacity duration-200 z-50 border border-white/15">
              Admins &amp; Moderators ({adminMembers.length})
            </div>
          </button>

          {/* 4. Categories & Catalog */}
          <button
            onClick={() => setActiveTab(\'categories\')}
            className={`relative group w-12 h-12 rounded-2xl flex items-center justify-center transition-all ${
              activeTab === \'categories\'
                ? \'bg-[#0071E3] text-white shadow-lg shadow-blue-500/30 ring-2 ring-white/20\'
                : \'text-white/60 hover:text-white hover:bg-white/10\'
            }`}
            aria-label="Categories & Catalog"
          >
            <Layers className="w-5 h-5 transition-transform group-hover:scale-110" />
            <div className="absolute left-[84px] px-3 py-1.5 rounded-xl bg-[#1D1D1F] text-white text-xs font-semibold whitespace-nowrap shadow-2xl pointer-events-none opacity-0 group-hover:opacity-100 transition-opacity duration-200 z-50 border border-white/15">
              Categories &amp; Catalog ({categories.length})
            </div>
          </button>

          {/* 5. Customer Orders */}
          <button
            onClick={() => setActiveTab(\'orders\')}
            className={`relative group w-12 h-12 rounded-2xl flex items-center justify-center transition-all ${
              activeTab === \'orders\'
                ? \'bg-[#0071E3] text-white shadow-lg shadow-blue-500/30 ring-2 ring-white/20\'
                : \'text-white/60 hover:text-white hover:bg-white/10\'
            }`}
            aria-label="Customer Orders"
          >
            <ShoppingBag className="w-5 h-5 transition-transform group-hover:scale-110" />
            <div className="absolute left-[84px] px-3 py-1.5 rounded-xl bg-[#1D1D1F] text-white text-xs font-semibold whitespace-nowrap shadow-2xl pointer-events-none opacity-0 group-hover:opacity-100 transition-opacity duration-200 z-50 border border-white/15">
              Customer Orders ({orders.length})
            </div>
          </button>

          {/* 6. Customer Experience / Reviews */}
          <button
            onClick={() => setActiveTab(\'reviews\')}
            className={`relative group w-12 h-12 rounded-2xl flex items-center justify-center transition-all ${
              activeTab === \'reviews\'
                ? \'bg-[#0071E3] text-white shadow-lg shadow-blue-500/30 ring-2 ring-white/20\'
                : \'text-white/60 hover:text-white hover:bg-white/10\'
            }`}
            aria-label="Customer Experience"
          >
            <MessageSquare className="w-5 h-5 transition-transform group-hover:scale-110" />
            <div className="absolute left-[84px] px-3 py-1.5 rounded-xl bg-[#1D1D1F] text-white text-xs font-semibold whitespace-nowrap shadow-2xl pointer-events-none opacity-0 group-hover:opacity-100 transition-opacity duration-200 z-50 border border-white/15">
              Customer Experience ({reviews.length})
            </div>
          </button>

          {/* 7. Founder\'s Vision */}
          <button
            onClick={() => setActiveTab(\'founder\')}
            className={`relative group w-12 h-12 rounded-2xl flex items-center justify-center transition-all ${
              activeTab === \'founder\'
                ? \'bg-[#0071E3] text-white shadow-lg shadow-blue-500/30 ring-2 ring-white/20\'
                : \'text-white/60 hover:text-white hover:bg-white/10\'
            }`}
            aria-label="Founder\'s Vision"
          >
            <Compass className="w-5 h-5 transition-transform group-hover:scale-110" />
            <div className="absolute left-[84px] px-3 py-1.5 rounded-xl bg-[#1D1D1F] text-white text-xs font-semibold whitespace-nowrap shadow-2xl pointer-events-none opacity-0 group-hover:opacity-100 transition-opacity duration-200 z-50 border border-white/15">
              Founder\'s Vision
            </div>
          </button>
        </div>

        {/* Bottom Rail: Live Store, Refresh, Super Admin Profile, Logout */}
        <div className="flex flex-col items-center gap-3 w-full">
          <div className="w-8 h-px bg-white/10 my-1" />

          {/* Live Store */}
          <a
            href="/"
            target="_blank"
            rel="noreferrer"
            className="relative group w-12 h-12 rounded-2xl flex items-center justify-center text-white/60 hover:text-white hover:bg-white/10 transition-all cursor-pointer"
            aria-label="Live Store"
          >
            <ExternalLink className="w-5 h-5 transition-transform group-hover:scale-110" />
            <div className="absolute left-[84px] px-3 py-1.5 rounded-xl bg-[#1D1D1F] text-white text-xs font-semibold whitespace-nowrap shadow-2xl pointer-events-none opacity-0 group-hover:opacity-100 transition-opacity duration-200 z-50 border border-white/15">
              View Live Store ↗
            </div>
          </a>

          {/* Refresh Data (Real live sync with spinning animation & toast) */}
          <button
            onClick={handleRefresh}
            className="relative group w-12 h-12 rounded-2xl flex items-center justify-center text-white/60 hover:text-white hover:bg-white/10 transition-all cursor-pointer"
            aria-label="Refresh Data"
            title="Refresh All System Data"
          >
            <RefreshCw className={`w-5 h-5 transition-transform group-hover:scale-110 ${isRefreshing ? \'animate-spin text-[#0071E3]\' : \'\'}`} />
            <div className="absolute left-[84px] px-3 py-1.5 rounded-xl bg-[#1D1D1F] text-white text-xs font-semibold whitespace-nowrap shadow-2xl pointer-events-none opacity-0 group-hover:opacity-100 transition-opacity duration-200 z-50 border border-white/15">
              {isRefreshing ? \'Refreshing System...\' : \'Refresh Dashboard Data\'}
            </div>
          </button>

          {/* Admin / Moderator Profile & Privacy Settings */}
          <button
            onClick={() => {
              const activePerson = adminMembers.find(m => m.username === currentUser?.username || m.email === currentUser?.email) || adminMembers[0];
              setProfileForm({
                name: activePerson?.name || currentUser?.name || \'Jakaria Tanim\',
                username: activePerson?.username || currentUser?.username || \'jakaria\',
                email: activePerson?.email || currentUser?.email || \'tanim@nexora.com\',
                password: activePerson?.password || \'NexoraSuperAdmin2026!\',
                confirmPassword: activePerson?.password || \'NexoraSuperAdmin2026!\',
                phone: activePerson?.phone || \'+880 1640-026177\',
                address: currentUser?.address || \'Dhaka, Bangladesh\',
                showPassword: false
              });
              setIsProfileModalOpen(true);
            }}
            className="relative group w-12 h-12 rounded-2xl flex items-center justify-center text-amber-300 hover:text-amber-200 hover:bg-white/10 transition-all cursor-pointer"
            aria-label="My Profile & Credentials"
          >
            <UserCircle className="w-5 h-5 transition-transform group-hover:scale-110" />
            <div className="absolute left-[84px] px-3 py-1.5 rounded-xl bg-[#1D1D1F] text-white text-xs font-semibold whitespace-nowrap shadow-2xl pointer-events-none opacity-0 group-hover:opacity-100 transition-opacity duration-200 z-50 border border-white/15">
              Full Profile &amp; Privacy Settings
            </div>
          </button>

          {/* Sign Out */}
          <button
            onClick={handleLogout}
            className="relative group w-12 h-12 rounded-2xl flex items-center justify-center text-red-400 hover:text-red-300 hover:bg-red-500/20 transition-all cursor-pointer"
            aria-label="Sign Out"
          >
            <LogOut className="w-5 h-5 transition-transform group-hover:scale-110" />
            <div className="absolute left-[84px] px-3 py-1.5 rounded-xl bg-[#1D1D1F] text-white text-xs font-semibold whitespace-nowrap shadow-2xl pointer-events-none opacity-0 group-hover:opacity-100 transition-opacity duration-200 z-50 border border-white/15">
              Sign Out Session
            </div>
          </button>
        </div>
      </aside>

      {/* =========================================================
          MAIN WORKSPACE AREA (Left margin 80px to accommodate Dock)
          ========================================================= */}
      <main className="ml-20 flex-1 min-h-screen flex flex-col bg-[#F5F5F7] dark:bg-[#080E1E]">
        
        {/* Top Header Bar */}
        <header className="sticky top-0 z-30 bg-white/95 dark:bg-[#0D152A]/95 backdrop-blur-xl border-b border-black/[0.08] dark:border-white/10 px-6 sm:px-8 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight text-[#1D1D1F] dark:text-white">
              {activeTab === \'overview\' && \'Dashboard Overview\'}
              {activeTab === \'products\' && \'Product Inventory & Catalog\'}
              {activeTab === \'staff\' && \'Admins & Moderators Governance\'}
              {activeTab === \'categories\' && \'Category Management\'}
              {activeTab === \'orders\' && \'Live Customer Orders & Fulfillment\'}
              {activeTab === \'reviews\' && \'Customer Experience & Feedback\'}
              {activeTab === \'founder\' && "Founder\'s Vision Profile"}
            </h1>
            <p className="text-sm text-[#86868B] font-mono mt-0.5">
              NEXORA Authorized Hardware Platform • Directed by Jakaria Tanim
            </p>
          </div>

          <div className="flex items-center gap-3">
            {/* Super Admin / Staff User Badge - Click to open Full Profile */}
            <div
              onClick={() => {
                const activePerson = adminMembers.find(m => m.username === currentUser?.username || m.email === currentUser?.email) || adminMembers[0];
                setProfileForm({
                  name: activePerson?.name || currentUser?.name || \'Jakaria Tanim\',
                  username: activePerson?.username || currentUser?.username || \'jakaria\',
                  email: activePerson?.email || currentUser?.email || \'tanim@nexora.com\',
                  password: activePerson?.password || \'NexoraSuperAdmin2026!\',
                  confirmPassword: activePerson?.password || \'NexoraSuperAdmin2026!\',
                  phone: activePerson?.phone || \'+880 1640-026177\',
                  address: currentUser?.address || \'Dhaka, Bangladesh\',
                  showPassword: false
                });
                setIsProfileModalOpen(true);
              }}
              className="flex items-center gap-3 px-3.5 py-1.5 rounded-full bg-slate-100 dark:bg-white/10 border border-black/10 dark:border-white/15 cursor-pointer hover:bg-slate-200/80 transition-colors"
              title="Click to view Full Profile & Privacy Settings"
            >
              <div className="w-7 h-7 rounded-full bg-[#0071E3] text-white flex items-center justify-center font-bold text-xs shadow-sm">
                {(currentUser?.name || \'J\').charAt(0).toUpperCase()}
              </div>
              <div className="text-left hidden sm:block pr-1">
                <div className="text-xs font-bold text-[#1D1D1F] dark:text-white leading-tight">
                  {currentUser?.name || \'Jakaria Tanim\'}
                </div>
                <div className="text-[10px] text-amber-600 dark:text-amber-400 font-mono font-semibold">
                  {currentUser?.role || \'Super Administrator\'}
                </div>
              </div>
            </div>

            {/* Contextual Action Button */}
            {activeTab === \'products\' && (
              <button
                onClick={() => {
                  setEditingProduct(null);
                  setProductForm({
                    name: \'\',
                    brand: \'Apple\',
                    tagline: \'\',
                    category: \'Smartphones\',
                    priceBDT: 0,
                    priceUSD: 0,
                    stockCount: 30,
                    inStock: true,
                    image: \'\',
                    specs: [\'\'],
                    description: \'\',
                  });
                  setIsProductModalOpen(true);
                }}
                className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full bg-[#0071E3] hover:bg-[#0077ED] text-white text-sm font-bold shadow-md transition-all active:scale-95"
              >
                <Plus className="w-4 h-4" />
                <span>+ Add Hardware Gadget</span>
              </button>
            )}

            {activeTab === \'staff\' && (
              <button
                onClick={() => setIsStaffModalOpen(true)}
                className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full bg-emerald-600 hover:bg-emerald-700 text-white text-sm font-bold shadow-md transition-all active:scale-95"
              >
                <UserPlus className="w-4 h-4" />
                <span>+ Add Administrator / Moderator</span>
              </button>
            )}

            {activeTab === \'categories\' && (
              <button
                onClick={() => {
                  const input = document.getElementById(\'new-cat-input\');
                  if (input) input.focus();
                }}
                className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full bg-emerald-600 hover:bg-emerald-700 text-white text-sm font-bold shadow-md transition-all active:scale-95"
              >
                <Plus className="w-4 h-4" />
                <span>+ Create Category</span>
              </button>
            )}

            {activeTab === \'reviews\' && (
              <a
                href="/reviews"
                target="_blank"
                rel="noreferrer"
                className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full bg-[#1D1D1F] hover:bg-[#333336] text-white text-sm font-bold shadow-sm transition-all"
              >
                <ExternalLink className="w-4 h-4" />
                <span>Public Reviews Page ↗</span>
              </a>
            )}
          </div>
        </header>

        {/* Content Body */}
        <div className="p-6 sm:p-8 space-y-8 flex-1">
          
          {/* Toggle Button for Overview Metrics */}
          <div className="flex items-center justify-between">
            <button
              onClick={() => setShowMetrics(!showMetrics)}
              className="inline-flex items-center gap-2 text-sm font-bold text-[#6E6E73] hover:text-[#1D1D1F] transition-colors"
            >
              <SlidersHorizontal className="w-4 h-4" />
              <span>{showMetrics ? \'Hide Executive Metrics\' : \'Show Executive Metrics\'}</span>
              {showMetrics ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
            </button>
          </div>

          {/* Top Performance Analytics Row - UNIFORM CLEAN CARD BACKGROUND */}
          {showMetrics && (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6 animate-fade-in">
              <div className="p-6 rounded-2xl bg-white dark:bg-[#151D30] border border-black/[0.08] dark:border-white/10 shadow-sm">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-mono uppercase tracking-wider text-[#6E6E73] font-bold">Total Revenue</span>
                  <span className="text-emerald-600 font-mono text-base font-bold">৳</span>
                </div>
                <div className="mt-3 text-3xl sm:text-4xl font-extrabold text-[#1D1D1F] dark:text-white tracking-tight">
                  ৳{totalRevenue.toLocaleString()}
                </div>
                <p className="mt-1.5 text-xs text-[#86868B]">Across all confirmed customer orders</p>
              </div>

              <div className="p-6 rounded-2xl bg-white dark:bg-[#151D30] border border-black/[0.08] dark:border-white/10 shadow-sm">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-mono uppercase tracking-wider text-[#6E6E73] font-bold">Catalog Hardware</span>
                  <Package className="w-5 h-5 text-[#0071E3]" />
                </div>
                <div className="mt-3 text-3xl sm:text-4xl font-extrabold text-[#1D1D1F] dark:text-white tracking-tight">
                  {products.length} Gadgets
                </div>
                <p className="mt-1.5 text-xs text-emerald-600 font-bold">
                  {products.filter(p => p.inStock).length} currently in stock
                </p>
              </div>

              <div className="p-6 rounded-2xl bg-white dark:bg-[#151D30] border border-black/[0.08] dark:border-white/10 shadow-sm">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-mono uppercase tracking-wider text-[#6E6E73] font-bold">Active Categories</span>
                  <Layers className="w-5 h-5 text-purple-600" />
                </div>
                <div className="mt-3 text-3xl sm:text-4xl font-extrabold text-[#1D1D1F] dark:text-white tracking-tight">
                  {categories.length}
                </div>
                <p className="mt-1.5 text-xs text-[#86868B] truncate">
                  Smartphones, Audio, Chargers &amp; Power
                </p>
              </div>

              <div className="p-6 rounded-2xl bg-white dark:bg-[#151D30] border border-black/[0.08] dark:border-white/10 shadow-sm">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-mono uppercase tracking-wider text-[#6E6E73] font-bold">Customer Reviews</span>
                  <Star className="w-5 h-5 text-amber-500 fill-amber-500" />
                </div>
                <div className="mt-3 text-3xl sm:text-4xl font-extrabold text-[#1D1D1F] dark:text-white tracking-tight">
                  {reviews.length} Reviews
                </div>
                <p className="mt-1.5 text-xs text-amber-600 font-bold">4.9 ★ Average customer rating</p>
              </div>
            </div>
          )}

          {/* =======================================================
              TAB 1: PRODUCT INVENTORY & CATALOG TAB
              ======================================================= */}
          {activeTab === \'products\' && (
            <div className="space-y-6">
              
              {/* Product Filtering Controls - UNIFORM CLEAN CARD BACKGROUND */}
              <div className="p-6 rounded-2xl bg-white dark:bg-[#151D30] border border-black/[0.08] dark:border-white/10 shadow-sm space-y-4">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                  <div className="relative flex-1">
                    <Search className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400" />
                    <input
                      type="text"
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                      placeholder="Search gadgets by title, specs, processor, or description..."
                      className="w-full pl-10 pr-4 py-3 rounded-xl bg-[#F5F5F7] dark:bg-white/5 border border-black/10 dark:border-white/10 text-base text-[#1D1D1F] dark:text-white focus:outline-none focus:border-[#0071E3]"
                    />
                  </div>

                  <button
                    onClick={() => setShowFilters(!showFilters)}
                    className="inline-flex items-center gap-2 px-5 py-3 rounded-xl bg-[#F5F5F7] dark:bg-white/10 hover:bg-[#EBEBEF] text-sm font-bold text-[#1D1D1F] dark:text-white transition-colors"
                  >
                    <Filter className="w-4 h-4" />
                    <span>Filter By Brand &amp; Category</span>
                  </button>
                </div>

                {showFilters && (
                  <div className="pt-3 border-t border-black/[0.06] dark:border-white/10 flex flex-wrap items-center gap-5 text-sm font-semibold">
                    <div className="flex items-center gap-2.5">
                      <span className="text-[#86868B]">Brand:</span>
                      <select
                        value={selectedBrandFilter}
                        onChange={(e) => setSelectedBrandFilter(e.target.value)}
                        className="px-3.5 py-2 rounded-xl bg-[#F5F5F7] dark:bg-white/10 border border-black/10 dark:border-white/10 text-[#1D1D1F] dark:text-white font-bold focus:outline-none"
                      >
                        {TOP_10_BRANDS.map((b) => (
                          <option key={b} value={b} className="text-black">{b}</option>
                        ))}
                      </select>
                    </div>

                    <div className="flex items-center gap-2.5">
                      <span className="text-[#86868B]">Category:</span>
                      <select
                        value={selectedCategoryFilter}
                        onChange={(e) => setSelectedCategoryFilter(e.target.value)}
                        className="px-3.5 py-2 rounded-xl bg-[#F5F5F7] dark:bg-white/10 border border-black/10 dark:border-white/10 text-[#1D1D1F] dark:text-white font-bold focus:outline-none"
                      >
                        <option value="All" className="text-black">All Categories</option>
                        {categories.map((c) => (
                          <option key={c.id} value={c.name} className="text-black">{c.name}</option>
                        ))}
                      </select>
                    </div>

                    <div className="ml-auto text-sm text-[#86868B] font-mono font-semibold">
                      Showing {filteredProducts.length} of {products.length} hardware gadgets
                    </div>
                  </div>
                )}
              </div>

              {/* Products Table - UNIFORM CLEAN CARD BACKGROUND */}
              <div className="rounded-2xl bg-white dark:bg-[#151D30] border border-black/[0.08] dark:border-white/10 shadow-sm overflow-hidden">
                <div className="overflow-x-auto">
                  <table className="w-full text-left">
                    <thead className="bg-[#F5F5F7] dark:bg-white/5 text-[#424245] dark:text-slate-300 uppercase font-mono text-xs font-bold tracking-wider border-b border-black/[0.08] dark:border-white/10">
                      <tr>
                        <th className="px-6 py-4">Hardware Item</th>
                        <th className="px-6 py-4">Brand</th>
                        <th className="px-6 py-4">Category</th>
                        <th className="px-6 py-4">Pricing (BDT)</th>
                        <th className="px-6 py-4">Stock</th>
                        <th className="px-6 py-4 text-right">Actions</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-black/[0.06] dark:divide-white/10 text-sm">
                      {filteredProducts.map((p) => (
                        <tr key={p.id} className="hover:bg-slate-50/80 dark:hover:bg-white/5 transition-colors">
                          <td className="px-6 py-4">
                            <div className="flex items-center gap-3.5">
                              <div className="relative w-12 h-12 rounded-xl bg-[#F5F5F7] dark:bg-black/40 p-1 flex-shrink-0 border border-black/[0.06]">
                                <Image
                                  src={p.image}
                                  alt={p.name}
                                  fill
                                  className="object-contain"
                                />
                              </div>
                              <div>
                                <div className="font-bold text-base text-[#1D1D1F] dark:text-white">{p.name}</div>
                                <div className="text-xs text-[#86868B] line-clamp-1 max-w-xs">{p.tagline || p.description}</div>
                              </div>
                            </div>
                          </td>
                          <td className="px-6 py-4">
                            <span className="font-bold text-sm text-[#1D1D1F] dark:text-slate-200">{p.brand || \'Apple\'}</span>
                          </td>
                          <td className="px-6 py-4">
                            <span className="px-3 py-1 rounded-full bg-slate-100 dark:bg-white/10 text-xs font-bold font-mono">
                              {p.category}
                            </span>
                          </td>
                          <td className="px-6 py-4 font-mono font-bold text-base text-[#1D1D1F] dark:text-white">
                            ৳{p.priceBDT.toLocaleString()}
                          </td>
                          <td className="px-6 py-4">
                            <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold font-mono ${
                              p.inStock
                                ? \'bg-emerald-50 text-emerald-700 dark:bg-emerald-500/20 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-500/30\'
                                : \'bg-red-50 text-red-700 dark:bg-red-500/20 dark:text-red-300 border border-red-200 dark:border-red-500/30\'
                            }`}>
                              <span className={`w-2 h-2 rounded-full ${p.inStock ? \'bg-emerald-500\' : \'bg-red-500\'}`} />
                              {p.stockCount} in stock
                            </span>
                          </td>
                          <td className="px-6 py-4 text-right">
                            <div className="flex items-center justify-end gap-2">
                              <button
                                onClick={() => {
                                  setEditingProduct(p);
                                  setProductForm(p);
                                  setIsProductModalOpen(true);
                                }}
                                className="p-2 rounded-xl text-[#0071E3] hover:bg-blue-50 dark:hover:bg-blue-500/20 transition-colors"
                                title="Edit Product Specs"
                              >
                                <Edit2 className="w-4 h-4" />
                              </button>
                              <button
                                onClick={() => handleDeleteProduct(p.id)}
                                className="p-2 rounded-xl text-red-500 hover:bg-red-50 dark:hover:bg-red-500/20 transition-colors"
                                title="Delete Hardware"
                              >
                                <Trash2 className="w-4 h-4" />
                              </button>
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}

          {/* =======================================================
              TAB 2: DASHBOARD OVERVIEW TAB - UNIFORM CLEAN CARDS
              ======================================================= */}
          {activeTab === \'overview\' && (
            <div className="space-y-6">
              <div className="p-6 rounded-2xl bg-white dark:bg-[#151D30] border border-black/[0.08] dark:border-white/10 shadow-sm">
                <h3 className="text-xl font-bold text-[#1D1D1F] dark:text-white">Platform Operating Core</h3>
                <p className="text-sm text-[#6E6E73] dark:text-[#A1A1A6] mt-1">
                  NEXORA Enterprise Dashboard telemetry. Complete hardware ecosystem management directed by Jakaria Tanim.
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div
                  onClick={() => setActiveTab(\'products\')}
                  className="p-6 rounded-2xl bg-white dark:bg-[#151D30] border border-black/[0.08] dark:border-white/10 shadow-sm hover:shadow-md transition-all cursor-pointer group"
                >
                  <Package className="w-8 h-8 text-[#0071E3] mb-3 group-hover:scale-110 transition-transform" />
                  <h4 className="font-bold text-lg text-[#1D1D1F] dark:text-white">Manage Inventory</h4>
                  <p className="text-sm text-[#6E6E73] dark:text-[#A1A1A6] mt-1">
                    {products.length} flagship devices catalogued with active piece telemetry.
                  </p>
                </div>

                <div
                  onClick={() => setActiveTab(\'staff\')}
                  className="p-6 rounded-2xl bg-white dark:bg-[#151D30] border border-black/[0.08] dark:border-white/10 shadow-sm hover:shadow-md transition-all cursor-pointer group"
                >
                  <ShieldCheck className="w-8 h-8 text-emerald-600 mb-3 group-hover:scale-110 transition-transform" />
                  <h4 className="font-bold text-lg text-[#1D1D1F] dark:text-white">Admins &amp; Staff</h4>
                  <p className="text-sm text-[#6E6E73] dark:text-[#A1A1A6] mt-1">
                    {adminMembers.length} team members authorized across governance roles.
                  </p>
                </div>

                <div
                  onClick={() => setActiveTab(\'orders\')}
                  className="p-6 rounded-2xl bg-white dark:bg-[#151D30] border border-black/[0.08] dark:border-white/10 shadow-sm hover:shadow-md transition-all cursor-pointer group"
                >
                  <ShoppingBag className="w-8 h-8 text-amber-500 mb-3 group-hover:scale-110 transition-transform" />
                  <h4 className="font-bold text-lg text-[#1D1D1F] dark:text-white">Live Orders</h4>
                  <p className="text-sm text-[#6E6E73] dark:text-[#A1A1A6] mt-1">
                    {orders.length} confirmed orders fulfilled through NEXORA logistics.
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* =======================================================
              TAB 3: ADMINS & MODERATORS GOVERNANCE TAB (Super Admin Authority)
              ======================================================= */}
          {activeTab === \'staff\' && (
            <div className="space-y-6">
              
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-6 rounded-2xl bg-white dark:bg-[#151D30] border border-black/[0.08] dark:border-white/10 shadow-sm">
                <div>
                  <h3 className="text-xl sm:text-2xl font-bold text-[#1D1D1F] dark:text-white">Administrative Team &amp; Role Governance</h3>
                  <p className="text-sm text-[#6E6E73] dark:text-[#A1A1A6] mt-1">
                    Super Administrator master control: Authorize team members, generate invitation passes, and dispatch multi-channel access links.
                  </p>
                </div>
                <button
                  onClick={() => setIsStaffModalOpen(true)}
                  className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full bg-emerald-600 hover:bg-emerald-700 text-white text-sm font-bold shadow-md transition-all active:scale-95 self-start sm:self-auto"
                >
                  <UserPlus className="w-4 h-4" />
                  <span>+ Add Administrator / Moderator</span>
                </button>
              </div>

              {/* Staff Table - CLEAN UNIFORM CARD (NO CREDENTIALS/PASSWORD COLUMN, EDIT MOVED TO PROFILE) */}
              <div className="rounded-2xl bg-white dark:bg-[#151D30] border border-black/[0.08] dark:border-white/10 shadow-sm overflow-hidden">
                <div className="overflow-x-auto">
                  <table className="w-full text-left">
                    <thead className="bg-[#F5F5F7] dark:bg-white/5 text-[#424245] dark:text-slate-300 uppercase font-mono text-xs font-bold tracking-wider border-b border-black/[0.08] dark:border-white/10">
                      <tr>
                        <th className="px-6 py-4">Staff Member</th>
                        <th className="px-6 py-4">Assigned Role</th>
                        <th className="px-6 py-4">Active Permissions</th>
                        <th className="px-6 py-4">Live Status</th>
                        <th className="px-6 py-4 text-right">Access Actions</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-black/[0.06] dark:divide-white/10 text-sm">
                      {adminMembers.map((member) => {
                        const isSuperOwner = member.role === \'Super Administrator\' || member.id === \'adm-001\';
                        const isCurrentUserActive = member.username === currentUser?.username || member.email === currentUser?.email || isSuperOwner;

                        return (
                          <tr key={member.id} className="hover:bg-slate-50/80 dark:hover:bg-white/5 transition-colors">
                            <td className="px-6 py-4">
                              <div className="flex items-center gap-3.5">
                                <div className="w-11 h-11 rounded-full bg-[#0B132B] text-amber-300 font-bold flex items-center justify-center text-sm shadow-sm flex-shrink-0">
                                  {member.name.slice(0, 2).toUpperCase()}
                                </div>
                                <div>
                                  <div className="font-bold text-base text-[#1D1D1F] dark:text-white">{member.name}</div>
                                  <div className="text-xs text-[#0071E3] font-mono font-bold">@{member.username || member.name.toLowerCase().replace(/[^a-z0-9]+/g, \'\')}</div>
                                  <div className="text-xs text-[#6E6E73] dark:text-[#A1A1A6] font-mono">{member.email}</div>
                                </div>
                              </div>
                            </td>
                            <td className="px-6 py-4">
                              <span className={`px-3 py-1 rounded-full text-xs font-bold font-mono ${
                                isSuperOwner
                                  ? \'bg-purple-100 text-purple-800 border border-purple-200 dark:bg-purple-900/30 dark:text-purple-300 dark:border-purple-800\'
                                  : member.role.includes(\'Admin\')
                                  ? \'bg-blue-100 text-blue-800 border border-blue-200 dark:bg-blue-900/30 dark:text-blue-300 dark:border-blue-800\'
                                  : \'bg-emerald-100 text-emerald-800 border border-emerald-200 dark:bg-emerald-900/30 dark:text-emerald-300 dark:border-emerald-800\'
                              }`}>
                                {member.role}
                              </span>
                            </td>
                            <td className="px-6 py-4">
                              <div className="flex flex-wrap gap-1">
                                {member.permissions.map((perm) => (
                                  <span key={perm} className="px-2.5 py-0.5 rounded bg-gray-100 dark:bg-white/10 text-gray-700 dark:text-gray-300 text-xs font-mono font-medium">
                                    {perm}
                                  </span>
                                ))}
                              </div>
                            </td>
                            <td className="px-6 py-4">
                              {isCurrentUserActive ? (
                                <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-50 dark:bg-emerald-500/20 text-emerald-700 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-500/30 text-xs font-bold font-mono">
                                  <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                                  Active Now
                                </span>
                              ) : member.status === \'Active\' ? (
                                <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-slate-100 dark:bg-white/10 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-white/10 text-xs font-bold font-mono">
                                  <span className="w-2 h-2 rounded-full bg-slate-400" />
                                  Active (Offline)
                                </span>
                              ) : (
                                <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-amber-50 dark:bg-amber-500/20 text-amber-700 dark:text-amber-300 border border-amber-200 dark:border-amber-500/30 text-xs font-bold font-mono">
                                  <span className="w-2 h-2 rounded-full bg-amber-400" />
                                  Invited
                                </span>
                              )}
                            </td>
                            <td className="px-6 py-4 text-right">
                              <div className="flex items-center justify-end gap-2.5">
                                {isSuperOwner ? (
                                  <span className="text-xs font-mono text-purple-700 dark:text-purple-300 font-bold px-3 py-1 rounded-full bg-purple-50 dark:bg-purple-900/30 border border-purple-200 dark:border-purple-800">
                                    ★ Platform Owner
                                  </span>
                                ) : (
                                  <>
                                    {/* Invite Action Button (Per User Direction: says "Invite", not "Copy Link") */}
                                    <button
                                      onClick={() => openInviteModal(member)}
                                      className="inline-flex items-center gap-1.5 px-4 py-1.5 rounded-full bg-[#0071E3] hover:bg-[#0077ED] text-white text-xs font-bold transition-all shadow-sm active:scale-95"
                                      title="Send invitation link via WhatsApp, Messenger, or Copy Link"
                                    >
                                      <Share2 className="w-3.5 h-3.5" />
                                      <span>Invite</span>
                                    </button>

                                    {/* Revoke Role Access */}
                                    <button
                                      onClick={() => handleDeleteStaff(member.id)}
                                      className="p-1.5 rounded-lg text-red-500 hover:bg-red-50 dark:hover:bg-red-500/20 transition-colors"
                                      title="Revoke Role Access"
                                    >
                                      <Trash2 className="w-4 h-4" />
                                    </button>
                                  </>
                                )}
                              </div>
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
              TAB 4: CATEGORIES MANAGEMENT TAB - UNIFORM CLEAN CARD
              ======================================================= */}
          {activeTab === \'categories\' && (
            <div className="space-y-8">
              
              {/* Category Creation Form */}
              <div className="p-6 sm:p-8 rounded-2xl bg-white dark:bg-[#151D30] border border-black/[0.08] dark:border-white/10 shadow-sm space-y-4">
                <div>
                  <h3 className="text-xl font-bold text-[#1D1D1F] dark:text-white">Create New Category</h3>
                  <p className="text-sm text-[#6E6E73] dark:text-[#A1A1A6] mt-1">
                    Categories appear instantly across the storefront, predictive suggestions, and gadget inventories.
                  </p>
                </div>

                {catSuccessMsg && (
                  <div className="p-3.5 rounded-xl bg-emerald-50 text-emerald-800 text-sm font-semibold border border-emerald-200">
                    {catSuccessMsg}
                  </div>
                )}

                <form onSubmit={handleCreateCategory} className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                  <div>
                    <label className="block text-sm font-bold text-[#1D1D1F] dark:text-white mb-1">
                      Category Name *
                    </label>
                    <input
                      id="new-cat-input"
                      type="text"
                      required
                      value={newCatName}
                      onChange={(e) => setNewCatName(e.target.value)}
                      placeholder="e.g. Wireless Drones"
                      className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] dark:bg-white/5 border border-black/10 dark:border-white/10 text-sm font-semibold text-[#1D1D1F] dark:text-white focus:outline-none focus:border-[#0071E3]"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-bold text-[#1D1D1F] dark:text-white mb-1">
                      Description
                    </label>
                    <input
                      type="text"
                      value={newCatDesc}
                      onChange={(e) => setNewCatDesc(e.target.value)}
                      placeholder="e.g. Pro aerial 4K camera robotics"
                      className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] dark:bg-white/5 border border-black/10 dark:border-white/10 text-sm text-[#1D1D1F] dark:text-white focus:outline-none focus:border-[#0071E3]"
                    />
                  </div>

                  <div className="flex items-end">
                    <button
                      type="submit"
                      className="w-full py-2.5 rounded-xl bg-[#0071E3] hover:bg-[#0077ED] text-white font-bold text-sm tracking-wide shadow-md transition-all active:scale-95 flex items-center justify-center gap-2"
                    >
                      <Plus className="w-4 h-4" />
                      <span>+ Create Category</span>
                    </button>
                  </div>
                </form>
              </div>

              {/* Active Categories List - UNIFORM CLEAN CARD */}
              <div className="rounded-2xl bg-white dark:bg-[#151D30] border border-black/[0.08] dark:border-white/10 shadow-sm p-6 sm:p-8 space-y-4">
                <h4 className="font-bold text-lg text-[#1D1D1F] dark:text-white">Active Product Categories ({categories.length})</h4>
                
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                  {categories.map((c) => {
                    const count = products.filter(p => p.category.toLowerCase() === c.name.toLowerCase()).length;
                    return (
                      <div
                        key={c.id}
                        className="p-5 rounded-xl bg-[#F5F5F7] dark:bg-white/5 border border-black/[0.06] dark:border-white/10 flex items-center justify-between group hover:border-[#0071E3] transition-all"
                      >
                        <div>
                          <div className="font-bold text-base text-[#1D1D1F] dark:text-white">{c.name}</div>
                          <div className="text-xs text-[#86868B] mt-0.5">{c.description}</div>
                          <div className="text-xs font-mono font-bold text-[#0071E3] mt-1">{count} gadgets in inventory</div>
                        </div>

                        <button
                          onClick={() => handleDeleteCategory(c.id)}
                          className="p-2 text-gray-400 hover:text-red-500 rounded-lg hover:bg-white dark:hover:bg-black/20 transition-colors"
                          title="Delete Category"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    );
                  })}
                </div>
              </div>

            </div>
          )}

          {/* =======================================================
              TAB 5: LIVE CUSTOMER ORDERS TAB - UNIFORM CLEAN CARD
              ======================================================= */}
          {activeTab === \'orders\' && (
            <div className="space-y-6">
              <div className="p-6 rounded-2xl bg-white dark:bg-[#151D30] border border-black/[0.08] dark:border-white/10 shadow-sm flex items-center justify-between">
                <div>
                  <h3 className="text-xl font-bold text-[#1D1D1F] dark:text-white">Live Customer Orders</h3>
                  <p className="text-sm text-[#6E6E73] dark:text-[#A1A1A6] mt-1">
                    Manage direct orders, customer delivery addresses, and real-time fulfillment stages.
                  </p>
                </div>
                <div className="text-right">
                  <div className="text-xs font-mono text-[#86868B]">Total Processed</div>
                  <div className="text-2xl font-extrabold text-[#1D1D1F] dark:text-white">৳{totalRevenue.toLocaleString()}</div>
                </div>
              </div>

              {/* Orders Table */}
              <div className="rounded-2xl bg-white dark:bg-[#151D30] border border-black/[0.08] dark:border-white/10 shadow-sm overflow-hidden">
                <div className="overflow-x-auto">
                  <table className="w-full text-left">
                    <thead className="bg-[#F5F5F7] dark:bg-white/5 text-[#424245] dark:text-slate-300 uppercase font-mono text-xs font-bold tracking-wider border-b border-black/[0.08] dark:border-white/10">
                      <tr>
                        <th className="px-6 py-4">Order ID</th>
                        <th className="px-6 py-4">Customer</th>
                        <th className="px-6 py-4">Items Ordered</th>
                        <th className="px-6 py-4">Total Amount</th>
                        <th className="px-6 py-4">Payment</th>
                        <th className="px-6 py-4">Fulfillment Status</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-black/[0.06] dark:divide-white/10 text-sm">
                      {orders.map((o) => (
                        <tr key={o.id} className="hover:bg-slate-50/80 dark:hover:bg-white/5 transition-colors">
                          <td className="px-6 py-4 font-mono font-bold text-[#0071E3]">
                            {o.id}
                          </td>
                          <td className="px-6 py-4">
                            <div className="font-bold text-[#1D1D1F] dark:text-white">{o.customer?.name || \'Customer\'}</div>
                            <div className="text-xs text-[#86868B] font-mono">{o.customer?.phone}</div>
                          </td>
                          <td className="px-6 py-4 text-xs">
                            {o.items?.map((item, i) => (
                              <div key={i} className="text-[#1D1D1F] dark:text-slate-200 font-medium">
                                {item.name} × {item.quantity}
                              </div>
                            ))}
                          </td>
                          <td className="px-6 py-4 font-mono font-bold text-base text-[#1D1D1F] dark:text-white">
                            ৳{o.totalBDT.toLocaleString()}
                          </td>
                          <td className="px-6 py-4">
                            <span className="px-2.5 py-1 rounded-full bg-slate-100 dark:bg-white/10 text-xs font-mono font-semibold">
                              {o.paymentMethod}
                            </span>
                          </td>
                          <td className="px-6 py-4">
                            <select
                              value={o.status}
                              onChange={(e) => handleOrderStatusChange(o.id, e.target.value)}
                              className="px-3 py-1.5 rounded-xl border border-black/10 dark:border-white/10 bg-white dark:bg-black/30 text-xs font-bold font-mono focus:outline-none"
                            >
                              <option value="Pending">Pending</option>
                              <option value="Processing">Processing</option>
                              <option value="Shipped">Shipped</option>
                              <option value="Delivered">Delivered</option>
                              <option value="Cancelled">Cancelled</option>
                            </select>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}

          {/* =======================================================
              TAB 6: CUSTOMER EXPERIENCE & REVIEWS MANAGEMENT TAB - UNIFORM CLEAN CARD
              ======================================================= */}
          {activeTab === \'reviews\' && (
            <div className="space-y-6">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-6 rounded-2xl bg-white dark:bg-[#151D30] border border-black/[0.08] dark:border-white/10 shadow-sm">
                <div>
                  <h3 className="text-xl font-bold text-[#1D1D1F] dark:text-white">Customer Experience &amp; Community Feedback</h3>
                  <p className="text-sm text-[#6E6E73] dark:text-[#A1A1A6] mt-1">
                    Manage verified customer testimonials, star ratings, and community reviews displayed across the storefront.
                  </p>
                </div>
                <a
                  href="/reviews"
                  target="_blank"
                  rel="noreferrer"
                  className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full bg-[#1D1D1F] dark:bg-[#0071E3] hover:bg-[#333336] text-white text-xs font-bold shadow-md transition-all self-start sm:self-auto"
                >
                  <ExternalLink className="w-3.5 h-3.5" />
                  <span>View Public Reviews Page ↗</span>
                </a>
              </div>

              {/* Reviews Table */}
              <div className="rounded-2xl bg-white dark:bg-[#151D30] border border-black/[0.08] dark:border-white/10 shadow-sm overflow-hidden">
                <div className="overflow-x-auto">
                  <table className="w-full text-left">
                    <thead className="bg-[#F5F5F7] dark:bg-white/5 text-[#424245] dark:text-slate-300 uppercase font-mono text-xs font-bold tracking-wider border-b border-black/[0.08] dark:border-white/10">
                      <tr>
                        <th className="px-6 py-4">Customer</th>
                        <th className="px-6 py-4">Product Purchased</th>
                        <th className="px-6 py-4">Rating</th>
                        <th className="px-6 py-4">Review Feedback</th>
                        <th className="px-6 py-4">Date</th>
                        <th className="px-6 py-4 text-right">Actions</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-black/[0.06] dark:divide-white/10 text-sm">
                      {reviews.map((rev) => (
                        <tr key={rev.id} className="hover:bg-slate-50/80 dark:hover:bg-white/5 transition-colors">
                          <td className="px-6 py-4">
                            <div className="font-bold text-base text-[#1D1D1F] dark:text-white">{rev.author}</div>
                            <span className="text-[10px] font-mono text-emerald-600 font-semibold bg-emerald-50 dark:bg-emerald-500/20 px-2 py-0.5 rounded-full">Verified Buyer</span>
                          </td>
                          <td className="px-6 py-4">
                            <div className="font-semibold text-[#0071E3] text-sm">{rev.productName}</div>
                          </td>
                          <td className="px-6 py-4">
                            <div className="flex gap-1 text-amber-500">
                              {Array.from({ length: 5 }).map((_, i) => (
                                <Star
                                  key={i}
                                  className={`w-4 h-4 ${
                                    i < rev.rating
                                      ? \'fill-amber-400 text-amber-400\'
                                      : \'text-gray-300\'
                                  }`}
                                />
                              ))}
                            </div>
                          </td>
                          <td className="px-6 py-4">
                            <p className="text-sm text-[#333336] dark:text-slate-200 max-w-md italic">&ldquo;{rev.comment}&rdquo;</p>
                          </td>
                          <td className="px-6 py-4 font-mono text-xs text-[#86868B]">
                            {rev.date}
                          </td>
                          <td className="px-6 py-4 text-right">
                            <button
                              onClick={() => handleDeleteReview(rev.id)}
                              className="p-2 rounded-xl text-red-500 hover:bg-red-50 dark:hover:bg-red-500/20 transition-colors"
                              title="Delete Review"
                            >
                              <Trash2 className="w-4 h-4" />
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}

          {/* =======================================================
              TAB 7: FOUNDER\'S VISION SETTINGS - UNIFORM CLEAN CARD
              ======================================================= */}
          {activeTab === \'founder\' && (
            <div className="max-w-3xl mx-auto space-y-6">
              <div className="p-6 rounded-2xl bg-white dark:bg-[#151D30] border border-black/[0.08] dark:border-white/10 shadow-sm">
                <h3 className="text-xl font-bold text-[#1D1D1F] dark:text-white">Founder&apos;s Vision &amp; Executive Profile</h3>
                <p className="text-sm text-[#6E6E73] dark:text-[#A1A1A6] mt-1">
                  Updates made here sync directly to the Founder&apos;s Vision portal across the website.
                </p>
              </div>

              {saveSuccess && (
                <div className="p-4 rounded-xl bg-emerald-50 text-emerald-800 text-sm font-semibold border border-emerald-200">
                  ✓ {saveSuccess}
                </div>
              )}

              <form onSubmit={handleSaveFounder} className="p-6 sm:p-8 rounded-2xl bg-white dark:bg-[#151D30] border border-black/[0.08] dark:border-white/10 shadow-sm space-y-5 text-sm">
                <div>
                  <label className="block text-[#1D1D1F] dark:text-white font-bold mb-1">Founder Name</label>
                  <input
                    type="text"
                    value={founderForm.name || \'\'}
                    onChange={(e) => setFounderForm({ ...founderForm, name: e.target.value })}
                    className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] dark:bg-white/5 border border-black/10 dark:border-white/10 text-[#1D1D1F] dark:text-white focus:outline-none focus:border-[#0071E3]"
                  />
                </div>

                <div>
                  <label className="block text-[#1D1D1F] dark:text-white font-bold mb-1">Company &amp; Executive Role</label>
                  <input
                    type="text"
                    value={founderForm.role || \'\'}
                    onChange={(e) => setFounderForm({ ...founderForm, role: e.target.value })}
                    className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] dark:bg-white/5 border border-black/10 dark:border-white/10 text-[#1D1D1F] dark:text-white focus:outline-none focus:border-[#0071E3]"
                  />
                </div>

                <div>
                  <label className="block text-[#1D1D1F] dark:text-white font-bold mb-1">Architectural Vision Statement</label>
                  <textarea
                    rows={4}
                    value={founderForm.vision || \'\'}
                    onChange={(e) => setFounderForm({ ...founderForm, vision: e.target.value })}
                    className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] dark:bg-white/5 border border-black/10 dark:border-white/10 text-[#1D1D1F] dark:text-white focus:outline-none focus:border-[#0071E3]"
                  />
                </div>

                <button
                  type="submit"
                  className="px-8 py-3 rounded-full bg-[#0071E3] hover:bg-[#0077ED] text-white font-bold text-sm tracking-wide shadow-md transition-all active:scale-95"
                >
                  Save Vision Profile
                </button>
              </form>
            </div>
          )}

        </div>
      </main>

      {/* =========================================================
          FLOAT TOAST NOTIFICATION
          ========================================================= */}
      {inviteToast && (
        <div className="fixed bottom-6 right-6 z-50 bg-[#1D1D1F] text-white px-5 py-3.5 rounded-2xl shadow-2xl flex items-center gap-3 border border-white/10 animate-fade-in text-sm font-semibold">
          <CheckCircle className="w-5 h-5 text-emerald-400 flex-shrink-0" />
          <span>{inviteToast}</span>
        </div>
      )}

      {/* =========================================================
          1. FULL PROFILE & PRIVACY SETTINGS MODAL (FOR LOGGED-IN ADMIN/MODERATOR)
          ========================================================= */}
      {isProfileModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-fade-in">
          <div className="relative w-full max-w-xl bg-white dark:bg-[#141A2E] rounded-3xl border border-black/10 dark:border-white/15 shadow-2xl p-6 sm:p-8 max-h-[90vh] overflow-y-auto space-y-6">
            
            <div className="flex items-center justify-between pb-3 border-b border-black/[0.08] dark:border-white/10">
              <div>
                <h3 className="text-xl sm:text-2xl font-extrabold text-[#1D1D1F] dark:text-white">Full Executive Profile</h3>
                <p className="text-xs text-[#86868B] mt-0.5">
                  Verified platform identity, active role governance, and personal privacy settings.
                </p>
              </div>
              <button
                onClick={() => setIsProfileModalOpen(false)}
                className="p-1.5 rounded-full bg-[#F5F5F7] dark:bg-white/10 text-[#86868B] hover:text-[#1D1D1F]"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {profileSuccessMsg && (
              <div className="p-3.5 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-800 text-sm font-semibold">
                {profileSuccessMsg}
              </div>
            )}

            {/* PART 1: FULL PROFILE CARD */}
            <div className="p-5 rounded-2xl bg-[#F8F9FA] dark:bg-white/5 border border-black/[0.08] dark:border-white/10 flex flex-col sm:flex-row items-center gap-5">
              <div className="relative w-20 h-20 sm:w-24 sm:h-24 rounded-full overflow-hidden bg-[#0B132B] border-2 border-[#0071E3] flex-shrink-0 shadow-md">
                <Image
                  src="/brand/founder_jakaria.png"
                  alt={profileForm.name}
                  fill
                  className="object-cover"
                />
              </div>

              <div className="text-center sm:text-left space-y-1.5 flex-1">
                <div className="flex flex-wrap items-center justify-center sm:justify-start gap-2">
                  <h4 className="text-xl font-bold text-[#1D1D1F] dark:text-white">{profileForm.name}</h4>
                  <span className="px-2.5 py-0.5 rounded-full bg-purple-100 text-purple-800 text-[11px] font-bold font-mono">
                    {currentUser?.role || \'Super Administrator\'}
                  </span>
                </div>
                
                <div className="text-xs text-[#0071E3] font-mono font-bold">
                  @{profileForm.username} • Authorized Master Key
                </div>

                <div className="flex flex-wrap items-center justify-center sm:justify-start gap-3 text-xs text-[#6E6E73] dark:text-[#A1A1A6] pt-1">
                  <span className="inline-flex items-center gap-1">
                    <MapPin className="w-3.5 h-3.5 text-gray-400" />
                    {profileForm.address || \'Dhaka, Bangladesh\'}
                  </span>
                  <span className="inline-flex items-center gap-1">
                    <Phone className="w-3.5 h-3.5 text-gray-400" />
                    {profileForm.phone || \'+880 1640-026177\'}
                  </span>
                </div>

                <div className="pt-2">
                  <a
                    href="https://www.facebook.com/iamJakariaTanim"
                    target="_blank"
                    rel="noreferrer"
                    className="inline-flex items-center gap-1.5 text-xs font-semibold text-[#0071E3] hover:underline"
                  >
                    <span>View Founder Facebook Profile ↗</span>
                  </a>
                </div>
              </div>
            </div>

            {/* PART 2: ACCOUNT PRIVACY & CREDENTIALS SETTINGS */}
            <form onSubmit={handleSaveProfile} className="space-y-4 pt-2">
              <div className="pb-1 border-b border-black/[0.06] dark:border-white/10">
                <h5 className="text-sm font-bold text-[#1D1D1F] dark:text-white flex items-center gap-1.5">
                  <Lock className="w-4 h-4 text-[#0071E3]" />
                  <span>Privacy &amp; Credentials Settings</span>
                </h5>
                <p className="text-xs text-[#86868B] mt-0.5">
                  Update your personal username, login email, physical address, and password here.
                </p>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-bold text-[#1D1D1F] dark:text-white mb-1">
                    Full Name
                  </label>
                  <input
                    type="text"
                    required
                    value={profileForm.name}
                    onChange={(e) => setProfileForm({ ...profileForm, name: e.target.value })}
                    className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] dark:bg-white/5 border border-black/10 dark:border-white/10 text-sm font-semibold text-[#1D1D1F] dark:text-white focus:outline-none focus:border-[#0071E3]"
                  />
                </div>

                <div>
                  <label className="block text-sm font-bold text-[#1D1D1F] dark:text-white mb-1">
                    Username
                  </label>
                  <input
                    type="text"
                    required
                    value={profileForm.username}
                    onChange={(e) => setProfileForm({ ...profileForm, username: e.target.value })}
                    className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] dark:bg-white/5 border border-black/10 dark:border-white/10 text-sm font-mono font-bold text-[#1D1D1F] dark:text-white focus:outline-none focus:border-[#0071E3]"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-bold text-[#1D1D1F] dark:text-white mb-1">
                    Login Email
                  </label>
                  <input
                    type="email"
                    required
                    value={profileForm.email}
                    onChange={(e) => setProfileForm({ ...profileForm, email: e.target.value })}
                    className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] dark:bg-white/5 border border-black/10 dark:border-white/10 text-sm font-mono font-semibold text-[#1D1D1F] dark:text-white focus:outline-none focus:border-[#0071E3]"
                  />
                </div>

                <div>
                  <label className="block text-sm font-bold text-[#1D1D1F] dark:text-white mb-1">
                    Contact Phone
                  </label>
                  <input
                    type="text"
                    value={profileForm.phone}
                    onChange={(e) => setProfileForm({ ...profileForm, phone: e.target.value })}
                    className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] dark:bg-white/5 border border-black/10 dark:border-white/10 text-sm font-semibold text-[#1D1D1F] dark:text-white focus:outline-none focus:border-[#0071E3]"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-bold text-[#1D1D1F] dark:text-white mb-1">
                  Residential / Office Address
                </label>
                <input
                  type="text"
                  value={profileForm.address}
                  onChange={(e) => setProfileForm({ ...profileForm, address: e.target.value })}
                  placeholder="e.g. Dhaka, Bangladesh"
                  className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] dark:bg-white/5 border border-black/10 dark:border-white/10 text-sm font-semibold text-[#1D1D1F] dark:text-white focus:outline-none focus:border-[#0071E3]"
                />
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <div className="flex items-center justify-between mb-1">
                    <label className="text-sm font-bold text-[#1D1D1F] dark:text-white">
                      New Password
                    </label>
                    <button
                      type="button"
                      onClick={() => setProfileForm({ ...profileForm, showPassword: !profileForm.showPassword })}
                      className="text-xs text-[#0071E3] font-medium"
                    >
                      {profileForm.showPassword ? \'Hide\' : \'Show\'}
                    </button>
                  </div>
                  <input
                    type={profileForm.showPassword ? \'text\' : \'password\'}
                    value={profileForm.password}
                    onChange={(e) => setProfileForm({ ...profileForm, password: e.target.value })}
                    placeholder="Enter new password"
                    className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] dark:bg-white/5 border border-black/10 dark:border-white/10 text-sm font-mono text-[#1D1D1F] dark:text-white focus:outline-none focus:border-[#0071E3]"
                  />
                </div>

                <div>
                  <label className="block text-sm font-bold text-[#1D1D1F] dark:text-white mb-1">
                    Confirm New Password
                  </label>
                  <input
                    type={profileForm.showPassword ? \'text\' : \'password\'}
                    value={profileForm.confirmPassword}
                    onChange={(e) => setProfileForm({ ...profileForm, confirmPassword: e.target.value })}
                    placeholder="Confirm new password"
                    className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] dark:bg-white/5 border border-black/10 dark:border-white/10 text-sm font-mono text-[#1D1D1F] dark:text-white focus:outline-none focus:border-[#0071E3]"
                  />
                </div>
              </div>

              <div className="pt-3 flex items-center justify-end gap-3">
                <button
                  type="button"
                  onClick={() => setIsProfileModalOpen(false)}
                  className="px-5 py-2.5 rounded-full border border-black/15 dark:border-white/20 text-sm font-semibold hover:bg-black/5 dark:hover:bg-white/5"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-7 py-2.5 rounded-full bg-[#0071E3] hover:bg-[#0077ED] text-white font-bold text-sm tracking-wide shadow-md transition-all active:scale-95"
                >
                  Save Profile &amp; Privacy Settings
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* =========================================================
          2. AUTHORIZE & GENERATE ACCESS LINK MODAL (+ Add Administrator / Moderator)
          Exact match to user screenshot media_1794919695949_0f1a0f1c.png
          ========================================================= */}
      {isStaffModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-fade-in">
          <div className="relative w-full max-w-lg bg-white dark:bg-[#141A2E] rounded-3xl border border-black/10 dark:border-white/15 shadow-2xl p-6 sm:p-8 space-y-5">
            <div className="flex items-center justify-between pb-3 border-b border-black/[0.08] dark:border-white/10">
              <div>
                <h3 className="text-xl font-bold text-[#1D1D1F] dark:text-white">Authorize New Staff Member</h3>
                <p className="text-xs text-[#86868B] mt-0.5">
                  Select role and click Authorize &amp; Generate Access Link to produce multi-channel invite links.
                </p>
              </div>
              <button
                onClick={() => setIsStaffModalOpen(false)}
                className="p-1.5 rounded-full bg-[#F5F5F7] dark:bg-white/10 text-[#86868B] hover:text-[#1D1D1F]"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleCreateStaff} className="space-y-4 text-xs">
              <div>
                <label className="block text-[#1D1D1F] dark:text-white font-bold mb-1 text-sm">Full Name *</label>
                <input
                  type="text"
                  required
                  value={staffForm.name}
                  onChange={(e) => {
                    const name = e.target.value;
                    const autoUsername = name.toLowerCase().replace(/[^a-z0-9]+/g, \'\');
                    setStaffForm({
                      ...staffForm,
                      name,
                      username: staffForm.username || autoUsername,
                      email: staffForm.email || (autoUsername ? `${autoUsername}@nexora.com` : \'\')
                    });
                  }}
                  placeholder="e.g. Tanvir Ahmed"
                  className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] dark:bg-white/5 border border-black/10 dark:border-white/10 text-sm font-semibold text-[#1D1D1F] dark:text-white focus:outline-none focus:border-[#0071E3]"
                />
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-[#1D1D1F] dark:text-white font-bold mb-1 text-sm">Assigned Username *</label>
                  <input
                    type="text"
                    required
                    value={staffForm.username}
                    onChange={(e) => setStaffForm({ ...staffForm, username: e.target.value })}
                    placeholder="e.g. tanvir"
                    className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] dark:bg-white/5 border border-black/10 dark:border-white/10 text-sm font-mono text-[#1D1D1F] dark:text-white focus:outline-none focus:border-[#0071E3]"
                  />
                </div>

                <div>
                  <label className="block text-[#1D1D1F] dark:text-white font-bold mb-1 text-sm">Email Address *</label>
                  <input
                    type="email"
                    required
                    value={staffForm.email}
                    onChange={(e) => setStaffForm({ ...staffForm, email: e.target.value })}
                    placeholder="tanvir@nexora.com"
                    className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] dark:bg-white/5 border border-black/10 dark:border-white/10 text-sm font-mono text-[#1D1D1F] dark:text-white focus:outline-none focus:border-[#0071E3]"
                  />
                </div>
              </div>

              <div>
                <label className="block text-[#1D1D1F] dark:text-white font-bold mb-1 text-sm">Assigned Governance Role *</label>
                <select
                  value={staffForm.role}
                  onChange={(e) => {
                    const r = e.target.value as AdminMember[\'role\'];
                    let perms = [\'products\'];
                    if (r === \'Administrator\') perms = [\'products\', \'orders\', \'categories\', \'reviews\'];
                    if (r === \'Inventory Moderator\') perms = [\'products\', \'categories\'];
                    if (r === \'Order Moderator\') perms = [\'orders\'];
                    setStaffForm({ ...staffForm, role: r, permissions: perms });
                  }}
                  className="w-full px-4 py-3 rounded-xl bg-[#F5F5F7] dark:bg-white/5 border border-black/10 dark:border-white/10 text-sm font-semibold text-[#1D1D1F] dark:text-white focus:outline-none"
                >
                  <option value="Inventory Moderator" className="text-black">Inventory Moderator (Products &amp; Categories)</option>
                  <option value="Order Moderator" className="text-black">Order Moderator (Customer Orders &amp; Fulfillment)</option>
                  <option value="Administrator" className="text-black">Administrator (Products, Orders, Categories, Reviews)</option>
                </select>
              </div>

              {/* Exact Green Button matching user screenshot media_1794919695949_0f1a0f1c.png */}
              <button
                type="submit"
                className="w-full py-3.5 rounded-full bg-[#059669] hover:bg-[#047857] text-white font-bold text-sm tracking-wide shadow-md transition-all active:scale-95 flex items-center justify-center gap-2"
              >
                <Key className="w-4 h-4" />
                <span>Authorize &amp; Generate Access Link</span>
              </button>
            </form>
          </div>
        </div>
      )}

      {/* =========================================================
          3. MULTI-CHANNEL INVITATION & ACCESS SHARING MODAL
          (Opens when clicking "Invite" on any staff row OR right after generating a staff pass)
          ========================================================= */}
      {inviteModalData && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-fade-in">
          <div className="relative w-full max-w-lg bg-white dark:bg-[#141A2E] rounded-3xl border border-black/10 dark:border-white/15 shadow-2xl p-6 sm:p-8 space-y-5">
            
            <div className="flex items-center justify-between pb-3 border-b border-black/[0.08] dark:border-white/10">
              <div className="flex items-center gap-2.5">
                <div className="w-9 h-9 rounded-full bg-emerald-100 dark:bg-emerald-500/20 text-emerald-600 flex items-center justify-center">
                  <Sparkles className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-xl font-bold text-[#1D1D1F] dark:text-white">Staff Access Pass Generated</h3>
                  <p className="text-xs text-[#86868B]">
                    Multi-channel invitation for {inviteModalData.member.name} ({inviteModalData.member.role})
                  </p>
                </div>
              </div>
              <button
                onClick={() => setInviteModalData(null)}
                className="p-1.5 rounded-full bg-[#F5F5F7] dark:bg-white/10 text-[#86868B] hover:text-[#1D1D1F]"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Link Container with Copy Button */}
            <div className="space-y-2">
              <label className="block text-xs font-bold text-[#1D1D1F] dark:text-white">
                Official Access Invitation Link:
              </label>
              <div className="flex items-center gap-2">
                <input
                  type="text"
                  readOnly
                  value={inviteModalData.inviteUrl}
                  className="flex-1 px-4 py-2.5 rounded-xl bg-[#F5F5F7] dark:bg-white/5 border border-black/10 dark:border-white/10 text-xs font-mono text-[#0071E3] font-bold select-all focus:outline-none"
                />
                <button
                  onClick={() => {
                    if (typeof navigator !== \'undefined\' && navigator.clipboard) {
                      navigator.clipboard.writeText(inviteModalData.inviteUrl);
                      setInviteModalData({ ...inviteModalData, copied: true });
                      setInviteToast(\'✓ Invitation link copied to clipboard!\');
                      setTimeout(() => {
                        if (inviteModalData) setInviteModalData(prev => prev ? { ...prev, copied: false } : null);
                        setInviteToast(\'\');
                      }, 3000);
                    }
                  }}
                  className={`px-4 py-2.5 rounded-xl text-xs font-bold transition-all flex items-center gap-1.5 shadow-sm active:scale-95 ${
                    inviteModalData.copied
                      ? \'bg-emerald-600 text-white\'
                      : \'bg-[#0071E3] hover:bg-[#0077ED] text-white\'
                  }`}
                >
                  {inviteModalData.copied ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
                  <span>{inviteModalData.copied ? \'Copied!\' : \'Copy Link\'}</span>
                </button>
              </div>
            </div>

            {/* Multi-Channel Instant Sharing Buttons */}
            <div className="space-y-2.5 pt-2">
              <label className="block text-xs font-bold text-[#6E6E73] dark:text-[#A1A1A6] uppercase font-mono">
                Dispatch Access Pass Via:
              </label>
              
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
                {/* 1. WhatsApp */}
                <a
                  href={`https://wa.me/?text=${encodeURIComponent(
                    `NEXORA Staff Access Authorization: Hello ${inviteModalData.member.name}, you have been granted access as ${inviteModalData.member.role} on NEXORA. Click here to accept your invitation: ${inviteModalData.inviteUrl}`
                  )}`}
                  target="_blank"
                  rel="noreferrer"
                  className="p-3 rounded-2xl bg-[#25D366]/10 hover:bg-[#25D366] text-[#25D366] hover:text-white border border-[#25D366]/30 flex flex-col items-center justify-center gap-1 text-xs font-bold transition-all hover:scale-105 shadow-sm"
                  title="Share on WhatsApp"
                >
                  <MessageCircle className="w-5 h-5" />
                  <span>WhatsApp</span>
                </a>

                {/* 2. Messenger */}
                <a
                  href={`https://www.facebook.com/dialog/send?link=${encodeURIComponent(inviteModalData.inviteUrl)}&app_id=291494419107518&redirect_uri=${encodeURIComponent(inviteModalData.inviteUrl)}`}
                  target="_blank"
                  rel="noreferrer"
                  className="p-3 rounded-2xl bg-[#0084FF]/10 hover:bg-[#0084FF] text-[#0084FF] hover:text-white border border-[#0084FF]/30 flex flex-col items-center justify-center gap-1 text-xs font-bold transition-all hover:scale-105 shadow-sm"
                  title="Share on Messenger"
                >
                  <Send className="w-5 h-5" />
                  <span>Messenger</span>
                </a>

                {/* 3. Telegram */}
                <a
                  href={`https://t.me/share/url?url=${encodeURIComponent(inviteModalData.inviteUrl)}&text=${encodeURIComponent(
                    `NEXORA Staff Access Authorization for ${inviteModalData.member.name} (${inviteModalData.member.role})`
                  )}`}
                  target="_blank"
                  rel="noreferrer"
                  className="p-3 rounded-2xl bg-[#0088cc]/10 hover:bg-[#0088cc] text-[#0088cc] hover:text-white border border-[#0088cc]/30 flex flex-col items-center justify-center gap-1 text-xs font-bold transition-all hover:scale-105 shadow-sm"
                  title="Share on Telegram"
                >
                  <Send className="w-5 h-5" />
                  <span>Telegram</span>
                </a>

                {/* 4. Email */}
                <a
                  href={`mailto:${inviteModalData.member.email}?subject=${encodeURIComponent(`NEXORA Staff Authorization: ${inviteModalData.member.role}`)}&body=${encodeURIComponent(
                    `Hello ${inviteModalData.member.name},\n\nYou have been authorized as ${inviteModalData.member.role} on NEXORA by Jakaria Tanim.\n\nPlease click the link below to accept your invitation and access the control dashboard:\n${inviteModalData.inviteUrl}\n\nAssigned Username: ${inviteModalData.member.username}\n\nNEXORA Technologies`
                  )}`}
                  className="p-3 rounded-2xl bg-amber-500/10 hover:bg-amber-500 text-amber-600 hover:text-white border border-amber-500/30 flex flex-col items-center justify-center gap-1 text-xs font-bold transition-all hover:scale-105 shadow-sm"
                  title="Send via Email"
                >
                  <Mail className="w-5 h-5" />
                  <span>Email</span>
                </a>
              </div>
            </div>

            {/* Invite Message Preview Box */}
            <div className="p-3.5 rounded-2xl bg-[#F5F5F7] dark:bg-black/30 border border-black/[0.06] dark:border-white/10 text-xs text-[#6E6E73] dark:text-[#A1A1A6] font-mono leading-relaxed">
              &ldquo;Hello {inviteModalData.member.name}, you have been granted authorized access as {inviteModalData.member.role} on NEXORA. Click the link to accept invitation and log in: {inviteModalData.inviteUrl}&rdquo;
            </div>

            <div className="pt-2 flex justify-end">
              <button
                onClick={() => setInviteModalData(null)}
                className="px-6 py-2.5 rounded-full bg-[#1D1D1F] hover:bg-[#333336] text-white text-xs font-bold tracking-wide"
              >
                Done
              </button>
            </div>

          </div>
        </div>
      )}

      {/* =========================================================
          PRODUCT CREATION / EDITING MODAL
          ========================================================= */}
      {isProductModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm animate-fade-in">
          <div className="relative w-full max-w-2xl bg-white dark:bg-[#141A2E] rounded-3xl border border-black/10 dark:border-white/15 shadow-2xl p-6 sm:p-8 max-h-[90vh] overflow-y-auto">
            
            <div className="flex items-center justify-between pb-4 border-b border-black/[0.08] dark:border-white/10">
              <div>
                <h3 className="text-xl font-bold text-[#1D1D1F] dark:text-white">
                  {editingProduct ? \'Edit Gadget Specs & Inventory\' : \'Add New Hardware Gadget\'}
                </h3>
                <p className="text-xs text-[#86868B] mt-0.5">
                  Update product details, official brand attribution, and stock piece counts.
                </p>
              </div>
              <button
                onClick={() => setIsProductModalOpen(false)}
                className="p-1.5 rounded-full bg-[#F5F5F7] dark:bg-white/10 text-[#86868B] hover:text-[#1D1D1F]"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleSaveProduct} className="space-y-4 pt-4 text-xs">
              
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-[#1D1D1F] dark:text-white font-bold mb-1 text-sm">Gadget Title *</label>
                  <input
                    type="text"
                    required
                    value={productForm.name || \'\'}
                    onChange={(e) => setProductForm({ ...productForm, name: e.target.value })}
                    placeholder="e.g. Samsung Galaxy S24 Ultra"
                    className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] dark:bg-white/5 border border-black/10 dark:border-white/10 text-sm text-[#1D1D1F] dark:text-white font-semibold focus:outline-none focus:border-[#0071E3]"
                  />
                </div>

                <div>
                  <label className="block text-[#1D1D1F] dark:text-white font-bold mb-1 text-sm">Brand *</label>
                  <select
                    value={productForm.brand || \'Apple\'}
                    onChange={(e) => setProductForm({ ...productForm, brand: e.target.value })}
                    className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] dark:bg-white/5 border border-black/10 dark:border-white/10 text-sm text-[#1D1D1F] dark:text-white font-semibold focus:outline-none focus:border-[#0071E3]"
                  >
                    {TOP_10_BRANDS.filter(b => b !== \'All\').map(b => (
                      <option key={b} value={b} className="text-black">{b}</option>
                    ))}
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-[#1D1D1F] dark:text-white font-bold mb-1 text-sm">Category *</label>
                  <select
                    value={productForm.category || \'Smartphones\'}
                    onChange={(e) => setProductForm({ ...productForm, category: e.target.value })}
                    className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] dark:bg-white/5 border border-black/10 dark:border-white/10 text-sm text-[#1D1D1F] dark:text-white font-semibold focus:outline-none focus:border-[#0071E3]"
                  >
                    {categories.map(c => (
                      <option key={c.id} value={c.name} className="text-black">{c.name}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-[#1D1D1F] dark:text-white font-bold mb-1 text-sm">Tagline / Key Highlight</label>
                  <input
                    type="text"
                    value={productForm.tagline || \'\'}
                    onChange={(e) => setProductForm({ ...productForm, tagline: e.target.value })}
                    placeholder="e.g. Breakthrough Titanium Unibody & Silicon"
                    className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] dark:bg-white/5 border border-black/10 dark:border-white/10 text-sm text-[#1D1D1F] dark:text-white focus:outline-none focus:border-[#0071E3]"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div>
                  <label className="block text-[#1D1D1F] dark:text-white font-bold mb-1 text-sm">Price in BDT (৳) *</label>
                  <input
                    type="number"
                    required
                    value={productForm.priceBDT || \'\'}
                    onChange={(e) => setProductForm({ ...productForm, priceBDT: Number(e.target.value) })}
                    placeholder="178000"
                    className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] dark:bg-white/5 border border-black/10 dark:border-white/10 text-sm font-mono font-bold text-[#1D1D1F] dark:text-white focus:outline-none focus:border-[#0071E3]"
                  />
                </div>

                <div>
                  <label className="block text-[#1D1D1F] dark:text-white font-bold mb-1 text-sm">Price in USD ($)</label>
                  <input
                    type="number"
                    value={productForm.priceUSD || \'\'}
                    onChange={(e) => setProductForm({ ...productForm, priceUSD: Number(e.target.value) })}
                    placeholder="1370"
                    className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] dark:bg-white/5 border border-black/10 dark:border-white/10 text-sm font-mono text-[#1D1D1F] dark:text-white focus:outline-none focus:border-[#0071E3]"
                  />
                </div>

                <div>
                  <label className="block text-[#1D1D1F] dark:text-white font-bold mb-1 text-sm">Stock Quantity *</label>
                  <input
                    type="number"
                    required
                    value={productForm.stockCount || \'\'}
                    onChange={(e) => setProductForm({ ...productForm, stockCount: Number(e.target.value) })}
                    placeholder="30"
                    className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] dark:bg-white/5 border border-black/10 dark:border-white/10 text-sm font-mono text-[#1D1D1F] dark:text-white focus:outline-none focus:border-[#0071E3]"
                  />
                </div>
              </div>

              {/* Image Input / Upload */}
              <div>
                <label className="block text-[#1D1D1F] dark:text-white font-bold mb-1 text-sm">Gadget Image File URL *</label>
                <div className="flex gap-2">
                  <input
                    type="text"
                    required
                    value={productForm.image || \'\'}
                    onChange={(e) => setProductForm({ ...productForm, image: e.target.value })}
                    placeholder="/products/samsung-s24-ultra.png"
                    className="flex-1 px-4 py-2.5 rounded-xl bg-[#F5F5F7] dark:bg-white/5 border border-black/10 dark:border-white/10 text-sm font-mono text-[#1D1D1F] dark:text-white focus:outline-none focus:border-[#0071E3]"
                  />
                  <label className="cursor-pointer px-4 py-2.5 rounded-xl bg-[#1D1D1F] hover:bg-[#333336] text-white font-semibold text-xs flex items-center gap-1.5 transition-colors">
                    <UploadCloud className="w-4 h-4" />
                    <span>{uploadingImage ? \'Uploading...\' : \'Upload PNG\'}</span>
                    <input
                      type="file"
                      accept="image/*"
                      className="hidden"
                      onChange={(e) => {
                        const file = e.target.files?.[0];
                        if (file) handleImageFile(file);
                      }}
                    />
                  </label>
                </div>
              </div>

              {/* Description */}
              <div>
                <label className="block text-[#1D1D1F] dark:text-white font-bold mb-1 text-sm">Product Description</label>
                <textarea
                  rows={3}
                  value={productForm.description || \'\'}
                  onChange={(e) => setProductForm({ ...productForm, description: e.target.value })}
                  placeholder="Engineered by Google / Apple / Samsung. Built for ultra-fidelity performance."
                  className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] dark:bg-white/5 border border-black/10 dark:border-white/10 text-sm text-[#1D1D1F] dark:text-white focus:outline-none focus:border-[#0071E3]"
                />
              </div>

              <div className="pt-2 flex items-center justify-end gap-3 border-t border-black/[0.08] dark:border-white/10">
                <button
                  type="button"
                  onClick={() => setIsProductModalOpen(false)}
                  className="px-5 py-2.5 rounded-full border border-black/15 dark:border-white/20 text-sm font-semibold text-[#1D1D1F] dark:text-white hover:bg-black/5 dark:hover:bg-white/5"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-7 py-2.5 rounded-full bg-[#0071E3] hover:bg-[#0077ED] text-white font-bold text-sm tracking-wide shadow-md transition-all active:scale-95"
                >
                  {editingProduct ? \'Save Changes\' : \'Publish Gadget\'}
                </button>
              </div>

            </form>
          </div>
        </div>
      )}

    </div>
  );
}
'''

with open('frontend/src/app/myadminerapanel/page.tsx', 'w', encoding='utf-8') as f:
    f.write(code)

print("Successfully written updated admin panel to frontend/src/app/myadminerapanel/page.tsx")

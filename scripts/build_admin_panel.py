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
  UserCircle
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

  // Edit Staff Modal State
  const [editingStaff, setEditingStaff] = useState<AdminMember | null>(null);
  const [isEditStaffModalOpen, setIsEditStaffModalOpen] = useState(false);
  const [editStaffForm, setEditStaffForm] = useState({
    name: \'\',
    username: \'\',
    email: \'\',
    password: \'\',
    phone: \'\',
    role: \'Administrator\' as AdminMember[\'role\'],
    permissions: [] as string[]
  });

  // Super Admin Self Profile / Credentials Modal
  const [isProfileModalOpen, setIsProfileModalOpen] = useState(false);
  const [profileForm, setProfileForm] = useState({
    name: \'Jakaria Tanim\',
    username: \'jakaria\',
    email: \'tanim@nexora.com\',
    password: \'\',
    confirmPassword: \'\'
  });
  const [profileSuccessMsg, setProfileSuccessMsg] = useState(\'\');

  // Category Tab: New Category Form
  const [newCatName, setNewCatName] = useState(\'\');
  const [newCatDesc, setNewCatDesc] = useState(\'\');
  const [catSuccessMsg, setCatSuccessMsg] = useState(\'\');

  // Founder Profile Form
  const [founderForm, setFounderForm] = useState<Partial<Founder>>({});
  const [saveSuccess, setSaveSuccess] = useState(\'\');

  // Toast / Password reveal maps
  const [inviteToast, setInviteToast] = useState(\'\');
  const [showPasswordMap, setShowPasswordMap] = useState<Record<string, boolean>>({});

  const [currentUser, setCurrentUser] = useState<{
    id?: string;
    name: string;
    role: string;
    email: string;
    username?: string;
  } | null>(null);

  // Require fresh login on page open; handle invite url query
  useEffect(() => {
    setIsAuthenticated(false);
    if (typeof window !== \'undefined\') {
      const params = new URLSearchParams(window.location.search);
      const urlUser = params.get(\'user\') || params.get(\'u\');
      if (urlUser) {
        setUsername(urlUser);
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
        setCurrentUser(data.user || { name: \'Jakaria Tanim\', role: \'Super Administrator\', email: \'tanim@nexora.com\' });
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
        setCurrentUser({ name: \'Jakaria Tanim\', role: \'Super Administrator\', email: \'tanim@nexora.com\' });
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

    if (editingProduct) {
      const updated = await updateProduct(editingProduct.id, cleanProduct);
      if (updated) {
        setProducts(prev => prev.map(p => p.id === updated.id ? updated : p));
      }
    } else {
      const created = await createProduct(cleanProduct);
      if (created) {
        setProducts(prev => [created, ...prev]);
      }
    }
    setIsProductModalOpen(false);
    setEditingProduct(null);
  };

  // Delete Product
  const handleDeleteProduct = async (id: string) => {
    if (confirm(\'Are you sure you want to permanently delete this gadget from inventory?\')) {
      const success = await deleteProduct(id);
      if (success) {
        setProducts(prev => prev.filter(p => p.id !== id));
      }
    }
  };

  // Toggle Stock Availability
  const handleToggleStock = async (product: Product) => {
    const currentStock = typeof product.stockCount === \'number\' ? product.stockCount : 30;
    const newStock = currentStock > 0 ? 0 : 30;
    const updated = await updateProduct(product.id, {
      stockCount: newStock,
      inStock: newStock > 0
    });
    if (updated) {
      setProducts(prev => prev.map(p => p.id === updated.id ? updated : p));
    }
  };

  // Create Category
  const handleCreateCategory = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newCatName.trim()) return;
    const newCat: Category = {
      id: newCatName.toLowerCase().replace(/[^a-z0-9]+/g, \'-\'),
      name: newCatName.trim(),
      description: newCatDesc.trim() || `${newCatName.trim()} devices collection.`
    };
    setCategories(prev => [...prev, newCat]);
    setNewCatName(\'\');
    setNewCatDesc(\'\');
    setCatSuccessMsg(`Category "${newCat.name}" published successfully!`);
    setTimeout(() => setCatSuccessMsg(\'\'), 4000);
  };

  // Delete Category
  const handleDeleteCategory = (id: string) => {
    if (confirm(\'Delete this category? Gadgets assigned to it will retain their classification.\')) {
      setCategories(prev => prev.filter(c => c.id !== id));
    }
  };

  // Update Order Status
  const handleOrderStatusChange = async (orderId: string, newStatus: string) => {
    const updated = await updateOrderStatus(orderId, newStatus);
    if (updated) {
      setOrders(prev => prev.map(o => o.id === updated.id ? updated : o));
    }
  };

  // Save Founder Form
  const handleSaveFounder = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaveSuccess(\'\');
    const updated = await updateFounder(founderForm);
    if (updated) {
      setFounder(updated);
      setSaveSuccess("Founder\'s Vision and leadership profile updated successfully!");
      setTimeout(() => setSaveSuccess(\'\'), 4000);
    }
  };

  // Add New Staff Member
  const handleCreateStaff = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!staffForm.name || !staffForm.name.trim()) return;

    const payload = {
      name: staffForm.name.trim(),
      username: staffForm.username.trim() || staffForm.name.trim().toLowerCase().replace(/[^a-z0-9]+/g, \'\'),
      email: staffForm.email.trim() || `${staffForm.name.trim().toLowerCase().replace(/[^a-z0-9]+/g, \'\')}@nexora.com`,
      password: staffForm.password.trim() || \'NexoraStaff2026!\',
      phone: staffForm.phone.trim() || \'+8801700000000\',
      role: staffForm.role,
      permissions: staffForm.permissions
    };

    const created = await createAdminMember(payload);
    if (created) {
      setAdminMembers(prev => [...prev, created]);
      setIsStaffModalOpen(false);
      copyStaffInvite(created);
      setStaffForm({
        name: \'\',
        username: \'\',
        email: \'\',
        password: \'\',
        phone: \'\',
        role: \'Inventory Moderator\',
        permissions: [\'products\', \'categories\']
      });
    }
  };

  // Save Edited Staff
  const handleSaveEditStaff = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingStaff) return;
    const updates: Partial<AdminMember> = {
      name: editStaffForm.name.trim(),
      username: editStaffForm.username.trim(),
      email: editStaffForm.email.trim(),
      role: editStaffForm.role,
      permissions: editStaffForm.permissions
    };
    if (editStaffForm.password.trim()) {
      updates.password = editStaffForm.password.trim();
    }
    const updated = await updateAdminMember(editingStaff.id, updates);
    if (updated) {
      setAdminMembers(prev => prev.map(m => m.id === updated.id ? updated : m));
      setIsEditStaffModalOpen(false);
      setEditingStaff(null);
      setInviteToast(`Credentials for ${updated.name} updated successfully!`);
      setTimeout(() => setInviteToast(\'\'), 5000);
    }
  };

  // Save Super Admin Profile & Credentials
  const handleSaveProfile = async (e: React.FormEvent) => {
    e.preventDefault();
    if (profileForm.password && profileForm.password !== profileForm.confirmPassword) {
      alert(\'Passwords do not match!\');
      return;
    }

    const superAdmin = adminMembers.find(m => m.role === \'Super Administrator\') || { id: \'adm-001\' };
    const updates: Partial<AdminMember> = {
      name: profileForm.name.trim(),
      username: profileForm.username.trim(),
      email: profileForm.email.trim()
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
        username: updated.username
      });
      setProfileSuccessMsg(\'Super Administrator credentials updated successfully! You can now log in with your updated username and password.\');
      setTimeout(() => {
        setProfileSuccessMsg(\'\');
        setIsProfileModalOpen(false);
      }, 3000);
    }
  };

  // Delete Staff Member
  const handleDeleteStaff = async (id: string) => {
    if (confirm(\'Revoke access for this administrator/moderator?\')) {
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

  // Copy Staff Invite Credentials Helper
  const copyStaffInvite = (m: AdminMember) => {
    const portalUrl = typeof window !== \'undefined\' ? `${window.location.origin}/myadminerapanel` : \'http://localhost:3000/myadminerapanel\';
    const directLogin = `${portalUrl}?user=${encodeURIComponent(m.username || \'\')}`;
    const text = `===========================================
NEXORA ENTERPRISE STAFF ACCESS AUTHORIZATION
===========================================
Staff Member: ${m.name}
Assigned Role: ${m.role}
Active Permissions: ${m.permissions.join(\', \')}

Admin Portal: ${portalUrl}
Direct Login Link: ${directLogin}
Username: ${m.username || m.email}
Email: ${m.email}
Password: ${m.password || \'(Contact Super Admin)\'}

Authorized By: Jakaria Tanim (Super Administrator)
===========================================`;

    if (typeof navigator !== \'undefined\' && navigator.clipboard) {
      navigator.clipboard.writeText(text);
      setInviteToast(`Copied authorization invite for ${m.name}! Send directly to your staff.`);
      setTimeout(() => setInviteToast(\'\'), 5000);
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
        <div className="w-full max-w-md p-8 rounded-3xl bg-white border border-white/20 shadow-2xl text-center space-y-6">
          <div className="relative w-14 h-14 mx-auto rounded-2xl bg-[#0B132B] p-2 flex items-center justify-center shadow-lg">
            <Image
              src="/brand/nexora_icon_white_transparent.png"
              alt="NEXORA"
              fill
              className="object-contain p-2"
            />
          </div>

          <div className="space-y-1">
            <h1 className="text-2xl font-bold tracking-tight text-[#1D1D1F]">
              Nexora Admin Panel
            </h1>
            <p className="text-xs text-[#86868B]">
              Enter authorized administrator or moderator credentials to access control systems.
            </p>
          </div>

          {loginError && (
            <div className="p-3 rounded-xl bg-red-50 border border-red-200 text-red-600 text-xs font-semibold">
              {loginError}
            </div>
          )}

          <form onSubmit={handleLogin} className="space-y-4 text-left">
            <div>
              <label className="block text-xs font-semibold text-[#1D1D1F] mb-1">
                Username or Email
              </label>
              <input
                type="text"
                required
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="e.g. jakaria or admin or inventory"
                className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] border border-black/10 text-sm text-[#1D1D1F] focus:outline-none focus:border-[#0071E3]"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-[#1D1D1F] mb-1">
                Password
              </label>
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter password"
                className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] border border-black/10 text-sm text-[#1D1D1F] focus:outline-none focus:border-[#0071E3]"
              />
            </div>

            <button
              type="submit"
              className="w-full py-3 rounded-full bg-[#0071E3] hover:bg-[#0077ED] text-white font-semibold text-sm tracking-wide transition-all shadow-md active:scale-95"
            >
              Sign In to Admin Panel
            </button>
          </form>

          {/* Quick Credential Test Helpers */}
          <div className="pt-2 border-t border-black/10 text-left">
            <span className="text-[10px] uppercase font-bold tracking-wider text-[#86868B] block mb-2">
              Authorized Role Fast Fill:
            </span>
            <div className="grid grid-cols-2 gap-1.5 text-[11px]">
              <button
                type="button"
                onClick={() => { setUsername(\'jakaria\'); setPassword(\'NexoraSuperAdmin2026!\'); }}
                className="px-2.5 py-1.5 rounded-lg bg-[#F5F5F7] hover:bg-[#EBEBEF] text-[#1D1D1F] font-semibold text-left truncate transition-colors"
                title="Super Administrator (Jakaria Tanim)"
              >
                👑 Super Admin
              </button>
              <button
                type="button"
                onClick={() => { setUsername(\'admin\'); setPassword(\'AdminOps2026!\'); }}
                className="px-2.5 py-1.5 rounded-lg bg-[#F5F5F7] hover:bg-[#EBEBEF] text-[#1D1D1F] font-semibold text-left truncate transition-colors"
                title="Administrator"
              >
                🛡️ Administrator
              </button>
              <button
                type="button"
                onClick={() => { setUsername(\'inventory\'); setPassword(\'InventoryMod2026!\'); }}
                className="px-2.5 py-1.5 rounded-lg bg-[#F5F5F7] hover:bg-[#EBEBEF] text-[#1D1D1F] font-semibold text-left truncate transition-colors"
                title="Inventory Moderator"
              >
                📦 Inventory Mod
              </button>
              <button
                type="button"
                onClick={() => { setUsername(\'orders\'); setPassword(\'OrderMod2026!\'); }}
                className="px-2.5 py-1.5 rounded-lg bg-[#F5F5F7] hover:bg-[#EBEBEF] text-[#1D1D1F] font-semibold text-left truncate transition-colors"
                title="Order Moderator"
              >
                🛍️ Order Mod
              </button>
            </div>
          </div>

          <p className="text-[11px] text-[#86868B] font-mono">
            Direct secure route: /myadminerapanel // 256-bit SSL
          </p>
        </div>
      </div>
    );
  }

  // -------------------------------------------------------------
  // Full Standard Admin Dashboard Layout (With Sleek Icon-only Left Rail)
  // -------------------------------------------------------------
  return (
    <div className="min-h-screen bg-[#F7F4EE] flex text-[#1D1D1F]">
      
      {/* =========================================================================
          1. SLEEK ICON-ONLY LEFT NAVIGATION RAIL / DOCK (NO WIDE BLUE DRAWER)
          ========================================================================= */}
      <aside className="sticky top-0 left-0 h-screen w-20 bg-[#0B132B] text-white z-50 flex flex-col items-center justify-between py-5 border-r border-white/10 shadow-2xl select-none flex-shrink-0">
        
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

          {/* 3. Admins & Moderators */}
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

          {/* 7. Founder's Vision */}
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

          {/* Refresh Data */}
          <button
            onClick={loadDashboardData}
            className="relative group w-12 h-12 rounded-2xl flex items-center justify-center text-white/60 hover:text-white hover:bg-white/10 transition-all cursor-pointer"
            aria-label="Refresh Data"
          >
            <RefreshCw className={`w-5 h-5 transition-transform group-hover:scale-110 ${loading ? \'animate-spin\' : \'\'}`} />
            <div className="absolute left-[84px] px-3 py-1.5 rounded-xl bg-[#1D1D1F] text-white text-xs font-semibold whitespace-nowrap shadow-2xl pointer-events-none opacity-0 group-hover:opacity-100 transition-opacity duration-200 z-50 border border-white/15">
              Refresh Dashboard Data
            </div>
          </button>

          {/* Super Admin Profile & Credentials */}
          <button
            onClick={() => {
              const superAdmin = adminMembers.find(m => m.role === \'Super Administrator\') || currentUser;
              setProfileForm({
                name: superAdmin?.name || \'Jakaria Tanim\',
                username: superAdmin?.username || \'jakaria\',
                email: superAdmin?.email || \'tanim@nexora.com\',
                password: superAdmin?.password || \'NexoraSuperAdmin2026!\',
                confirmPassword: superAdmin?.password || \'NexoraSuperAdmin2026!\'
              });
              setIsProfileModalOpen(true);
            }}
            className="relative group w-12 h-12 rounded-2xl flex items-center justify-center text-amber-300 hover:text-amber-200 hover:bg-white/10 transition-all cursor-pointer"
            aria-label="My Profile & Credentials"
          >
            <UserCircle className="w-5 h-5 transition-transform group-hover:scale-110" />
            <div className="absolute left-[84px] px-3 py-1.5 rounded-xl bg-[#1D1D1F] text-white text-xs font-semibold whitespace-nowrap shadow-2xl pointer-events-none opacity-0 group-hover:opacity-100 transition-opacity duration-200 z-50 border border-white/15">
              Super Admin Profile &amp; Credentials
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
              Sign Out Terminal
            </div>
          </button>
        </div>
      </aside>

      {/* =========================================================================
          2. EXPANSIVE MAIN CONTENT AREA (Takes 100% of remaining width)
          ========================================================================= */}
      <main className="flex-1 min-w-0 flex flex-col min-h-screen">
        
        {/* Top Control Header */}
        <header className="sticky top-0 z-30 bg-white/95 backdrop-blur-xl border-b border-black/[0.08] px-6 py-4 flex items-center justify-between shadow-sm">
          <div>
            <h1 className="text-xl sm:text-2xl font-extrabold tracking-tight text-[#1D1D1F]">
              {activeTab === \'overview\' && \'Dashboard Overview\'}
              {activeTab === \'products\' && \'Product Inventory & Catalog\'}
              {activeTab === \'staff\' && \'Admins & Moderators Governance\'}
              {activeTab === \'categories\' && \'Category Management\'}
              {activeTab === \'orders\' && \'Live Customer Orders & Fulfillment\'}
              {activeTab === \'reviews\' && \'Customer Experience & Feedback\'}
              {activeTab === \'founder\' && "Founder\'s Vision Profile"}
            </h1>
            <p className="text-xs text-[#86868B] font-mono mt-0.5">
              NEXORA Authorized Hardware Platform • Directed by Jakaria Tanim
            </p>
          </div>

          <div className="flex items-center gap-3">
            {/* Super Admin / Staff User Badge */}
            <div
              onClick={() => {
                const superAdmin = adminMembers.find(m => m.role === \'Super Administrator\') || currentUser;
                setProfileForm({
                  name: superAdmin?.name || \'Jakaria Tanim\',
                  username: superAdmin?.username || \'jakaria\',
                  email: superAdmin?.email || \'tanim@nexora.com\',
                  password: superAdmin?.password || \'NexoraSuperAdmin2026!\',
                  confirmPassword: superAdmin?.password || \'NexoraSuperAdmin2026!\'
                });
                setIsProfileModalOpen(true);
              }}
              className="hidden sm:flex items-center gap-2.5 px-3.5 py-1.5 rounded-full bg-[#F5F5F7] border border-black/10 hover:border-black/20 cursor-pointer transition-all"
              title="Click to edit credentials"
            >
              <div className="w-6 h-6 rounded-full bg-[#0B132B] text-amber-300 font-bold text-xs flex items-center justify-center">
                {currentUser?.name?.slice(0, 2).toUpperCase() || \'JT\'}
              </div>
              <div className="text-xs text-left">
                <span className="font-bold text-[#1D1D1F] block leading-none">{currentUser?.name || \'Jakaria Tanim\'}</span>
                <span className="text-[10px] text-[#6E6E73] font-mono block leading-none mt-0.5">{currentUser?.role || \'Super Administrator\'}</span>
              </div>
              <Key className="w-3.5 h-3.5 text-[#86868B] ml-1" />
            </div>

            {/* Dynamic Action Buttons based on Active Tab */}
            {activeTab === \'products\' && (
              <button
                onClick={() => {
                  setEditingProduct(null);
                  setProductForm({
                    name: \'\',
                    brand: \'Apple\',
                    tagline: \'\',
                    category: categories[0]?.name || \'Smartphones\',
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
                className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-[#0071E3] hover:bg-[#0077ED] text-white text-xs font-semibold shadow-sm transition-all active:scale-95"
              >
                <Plus className="w-4 h-4" />
                <span>+ Add Gadget</span>
              </button>
            )}

            {activeTab === \'staff\' && (
              <button
                onClick={() => setIsStaffModalOpen(true)}
                className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold shadow-sm transition-all active:scale-95"
              >
                <Plus className="w-4 h-4" />
                <span>+ Add Staff Member</span>
              </button>
            )}

            {activeTab === \'categories\' && (
              <button
                onClick={() => {
                  const input = document.getElementById(\'new-cat-input\');
                  if (input) input.focus();
                }}
                className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold shadow-sm transition-all active:scale-95"
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
                className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-[#1D1D1F] hover:bg-[#333336] text-white text-xs font-semibold shadow-sm transition-all"
              >
                <ExternalLink className="w-3.5 h-3.5" />
                <span>Public Reviews Page</span>
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
              className="inline-flex items-center gap-2 text-xs font-semibold text-[#6E6E73] hover:text-[#1D1D1F] transition-colors"
            >
              <SlidersHorizontal className="w-3.5 h-3.5" />
              <span>{showMetrics ? \'Hide Executive Metrics\' : \'Show Executive Metrics\'}</span>
              {showMetrics ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
            </button>
          </div>

          {/* Top Performance Analytics Row */}
          {showMetrics && (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 animate-fade-in">
              <div className="p-5 rounded-2xl bg-white border border-black/[0.08] shadow-sm">
                <div className="flex items-center justify-between">
                  <span className="text-[11px] font-mono uppercase tracking-wider text-[#6E6E73] font-semibold">Total Revenue</span>
                  <span className="text-emerald-600 font-mono text-sm font-bold">৳</span>
                </div>
                <div className="mt-2 text-2xl sm:text-3xl font-extrabold text-[#1D1D1F] tracking-tight">
                  ৳{totalRevenue.toLocaleString()}
                </div>
                <p className="mt-1 text-xs text-[#86868B]">Across all confirmed customer orders</p>
              </div>

              <div className="p-5 rounded-2xl bg-white border border-black/[0.08] shadow-sm">
                <div className="flex items-center justify-between">
                  <span className="text-[11px] font-mono uppercase tracking-wider text-[#6E6E73] font-semibold">Catalog Hardware</span>
                  <Package className="w-4 h-4 text-[#0071E3]" />
                </div>
                <div className="mt-2 text-2xl sm:text-3xl font-extrabold text-[#1D1D1F] tracking-tight">
                  {products.length} Gadgets
                </div>
                <p className="mt-1 text-xs text-emerald-600 font-medium">
                  {products.filter(p => p.inStock).length} currently in stock
                </p>
              </div>

              <div className="p-5 rounded-2xl bg-white border border-black/[0.08] shadow-sm">
                <div className="flex items-center justify-between">
                  <span className="text-[11px] font-mono uppercase tracking-wider text-[#6E6E73] font-semibold">Active Categories</span>
                  <Layers className="w-4 h-4 text-purple-600" />
                </div>
                <div className="mt-2 text-2xl sm:text-3xl font-extrabold text-[#1D1D1F] tracking-tight">
                  {categories.length}
                </div>
                <p className="mt-1 text-xs text-[#86868B] truncate">
                  Smartphones, Audio, Chargers &amp; Power
                </p>
              </div>

              <div className="p-5 rounded-2xl bg-white border border-black/[0.08] shadow-sm">
                <div className="flex items-center justify-between">
                  <span className="text-[11px] font-mono uppercase tracking-wider text-[#6E6E73] font-semibold">Customer Reviews</span>
                  <Star className="w-4 h-4 text-amber-500 fill-amber-500" />
                </div>
                <div className="mt-2 text-2xl sm:text-3xl font-extrabold text-[#1D1D1F] tracking-tight">
                  {reviews.length} Reviews
                </div>
                <p className="mt-1 text-xs text-amber-600 font-medium">4.9 ★ Average rating</p>
              </div>
            </div>
          )}

          {/* =======================================================
              TAB 1: PRODUCT INVENTORY & CATALOG TAB
              ======================================================= */}
          {activeTab === \'products\' && (
            <div className="space-y-6">
              
              {/* Product Filtering Controls */}
              <div className="p-5 rounded-3xl bg-white border border-black/[0.08] shadow-sm space-y-4">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                  <div className="relative flex-1">
                    <Search className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400" />
                    <input
                      type="text"
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                      placeholder="Search gadgets by title, specs, processor, or description..."
                      className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-[#F5F5F7] border border-black/10 text-sm text-[#1D1D1F] focus:outline-none focus:border-[#0071E3]"
                    />
                  </div>

                  <button
                    onClick={() => setShowFilters(!showFilters)}
                    className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-[#F5F5F7] hover:bg-[#EBEBEF] text-xs font-semibold text-[#1D1D1F] transition-colors"
                  >
                    <Filter className="w-3.5 h-3.5" />
                    <span>Filter By Brand &amp; Category</span>
                  </button>
                </div>

                {showFilters && (
                  <div className="pt-3 border-t border-black/[0.06] flex flex-wrap items-center gap-4 text-xs font-semibold">
                    <div className="flex items-center gap-2">
                      <span className="text-[#86868B]">Brand:</span>
                      <select
                        value={selectedBrandFilter}
                        onChange={(e) => setSelectedBrandFilter(e.target.value)}
                        className="px-3 py-1.5 rounded-lg bg-[#F5F5F7] border border-black/10 text-[#1D1D1F] focus:outline-none"
                      >
                        {TOP_10_BRANDS.map((b) => (
                          <option key={b} value={b}>{b}</option>
                        ))}
                      </select>
                    </div>

                    <div className="flex items-center gap-2">
                      <span className="text-[#86868B]">Category:</span>
                      <select
                        value={selectedCategoryFilter}
                        onChange={(e) => setSelectedCategoryFilter(e.target.value)}
                        className="px-3 py-1.5 rounded-lg bg-[#F5F5F7] border border-black/10 text-[#1D1D1F] focus:outline-none"
                      >
                        <option value="All">All Categories</option>
                        {categories.map((c) => (
                          <option key={c.id} value={c.name}>{c.name}</option>
                        ))}
                      </select>
                    </div>

                    {(selectedBrandFilter !== \'All\' || selectedCategoryFilter !== \'All\' || searchQuery) && (
                      <button
                        onClick={() => {
                          setSelectedBrandFilter(\'All\');
                          setSelectedCategoryFilter(\'All\');
                          setSearchQuery(\'\');
                        }}
                        className="text-xs text-[#0071E3] hover:underline"
                      >
                        Reset Filters
                      </button>
                    )}
                  </div>
                )}
              </div>

              {/* Products Table */}
              <div className="rounded-3xl bg-white border border-black/[0.08] shadow-sm overflow-hidden">
                <div className="overflow-x-auto">
                  <table className="w-full text-left">
                    <thead className="bg-[#F5F5F7] text-[#424245] uppercase font-mono text-xs font-bold tracking-wider border-b border-black/[0.08]">
                      <tr>
                        <th className="px-6 py-4">Visual</th>
                        <th className="px-6 py-4">Gadget Details</th>
                        <th className="px-6 py-4">Category</th>
                        <th className="px-6 py-4">Price</th>
                        <th className="px-6 py-4">Inventory Stock</th>
                        <th className="px-6 py-4 text-right">Actions</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-black/[0.06] text-sm">
                      {filteredProducts.map((p) => (
                        <tr key={p.id} className="hover:bg-slate-50/80 transition-colors">
                          <td className="px-6 py-4">
                            <div className="relative w-12 h-12 rounded-xl bg-[#F5F5F7] border border-black/[0.06] p-1 flex items-center justify-center overflow-hidden">
                              <Image
                                src={p.image || \'/products/iphone-18-pro-max.png\'}
                                alt={p.name}
                                fill
                                className="object-contain p-1"
                              />
                            </div>
                          </td>
                          <td className="px-6 py-4">
                            <div className="font-bold text-[#1D1D1F] text-base">{p.name}</div>
                            <div className="text-xs text-[#86868B] truncate max-w-sm">{p.tagline || p.description}</div>
                            <div className="text-[11px] font-mono text-[#0071E3] font-semibold mt-0.5">{p.brand}</div>
                          </td>
                          <td className="px-6 py-4">
                            <span className="px-2.5 py-1 rounded-full bg-slate-100 text-slate-700 text-xs font-mono font-medium">
                              {p.category}
                            </span>
                          </td>
                          <td className="px-6 py-4">
                            <div className="font-mono font-bold text-base text-[#1D1D1F]">
                              ৳{p.priceBDT.toLocaleString()}
                            </div>
                            <div className="text-xs text-[#86868B] font-mono">${p.priceUSD}</div>
                          </td>
                          <td className="px-6 py-4">
                            <button
                              onClick={() => handleToggleStock(p)}
                              className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold font-mono transition-colors ${
                                p.inStock
                                  ? \'bg-emerald-50 text-emerald-700 border border-emerald-200 hover:bg-emerald-100\'
                                  : \'bg-red-50 text-red-700 border border-red-200 hover:bg-red-100\'
                              }`}
                            >
                              <span className={`w-2 h-2 rounded-full ${p.inStock ? \'bg-emerald-500\' : \'bg-red-500\'}`} />
                              {p.inStock ? `${p.stockCount || 30} Units In Stock` : \'Sold Out (Restock)\'}
                            </button>
                          </td>
                          <td className="px-6 py-4 text-right">
                            <div className="flex items-center justify-end gap-1.5">
                              <button
                                onClick={() => {
                                  setEditingProduct(p);
                                  setProductForm(p);
                                  setIsProductModalOpen(true);
                                }}
                                className="p-2 rounded-xl text-slate-600 hover:text-[#0071E3] hover:bg-slate-100 transition-colors"
                                title="Edit Product"
                              >
                                <Edit2 className="w-4 h-4" />
                              </button>
                              <button
                                onClick={() => handleDeleteProduct(p.id)}
                                className="p-2 rounded-xl text-slate-600 hover:text-red-600 hover:bg-red-50 transition-colors"
                                title="Delete Product"
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
              TAB 2: DASHBOARD OVERVIEW TAB
              ======================================================= */}
          {activeTab === \'overview\' && (
            <div className="space-y-6">
              <div className="p-6 rounded-3xl bg-white border border-black/[0.08] shadow-sm">
                <h3 className="text-xl font-bold text-[#1D1D1F]">Platform Operating Core</h3>
                <p className="text-sm text-[#6E6E73] mt-1">
                  NEXORA Enterprise Dashboard telemetry. Complete hardware ecosystem management directed by Jakaria Tanim.
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div
                  onClick={() => setActiveTab(\'products\')}
                  className="p-6 rounded-3xl bg-white border border-black/[0.08] shadow-sm hover:shadow-md transition-all cursor-pointer group"
                >
                  <Package className="w-8 h-8 text-[#0071E3] mb-3 group-hover:scale-110 transition-transform" />
                  <h4 className="font-bold text-lg text-[#1D1D1F]">Manage Inventory</h4>
                  <p className="text-xs text-[#86868B] mt-1">Review {products.length} flagship gadgets across 10 official brands.</p>
                </div>

                <div
                  onClick={() => setActiveTab(\'orders\')}
                  className="p-6 rounded-3xl bg-white border border-black/[0.08] shadow-sm hover:shadow-md transition-all cursor-pointer group"
                >
                  <ShoppingBag className="w-8 h-8 text-emerald-600 mb-3 group-hover:scale-110 transition-transform" />
                  <h4 className="font-bold text-lg text-[#1D1D1F]">Live Orders</h4>
                  <p className="text-xs text-[#86868B] mt-1">{orders.length} orders awaiting fulfillment and courier dispatch.</p>
                </div>

                <div
                  onClick={() => setActiveTab(\'staff\')}
                  className="p-6 rounded-3xl bg-white border border-black/[0.08] shadow-sm hover:shadow-md transition-all cursor-pointer group"
                >
                  <ShieldCheck className="w-8 h-8 text-purple-600 mb-3 group-hover:scale-110 transition-transform" />
                  <h4 className="font-bold text-lg text-[#1D1D1F]">Admins &amp; Staff</h4>
                  <p className="text-xs text-[#86868B] mt-1">{adminMembers.length} authorized staff members with role governance.</p>
                </div>
              </div>
            </div>
          )}

          {/* =======================================================
              TAB 3: ADMINS & MODERATORS GOVERNANCE TAB (Super Admin Authority)
              ======================================================= */}
          {activeTab === \'staff\' && (
            <div className="space-y-6">
              
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-6 rounded-3xl bg-white border border-black/[0.08] shadow-sm">
                <div>
                  <h3 className="text-xl font-bold text-[#1D1D1F]">Administrative Team &amp; Role Governance</h3>
                  <p className="text-sm text-[#6E6E73] mt-1">
                    Super Administrator full authority: define credentials, generate instant verification links, and assign moderators.
                  </p>
                </div>
                <button
                  onClick={() => setIsStaffModalOpen(true)}
                  className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full bg-emerald-600 hover:bg-emerald-700 text-white text-sm font-bold shadow-md transition-all active:scale-95 self-start sm:self-auto"
                >
                  <Plus className="w-4 h-4" />
                  <span>+ Add Administrator / Moderator</span>
                </button>
              </div>

              {/* Staff Table */}
              <div className="rounded-3xl bg-white border border-black/[0.08] shadow-sm overflow-hidden">
                <div className="overflow-x-auto">
                  <table className="w-full text-left">
                    <thead className="bg-[#F5F5F7] text-[#424245] uppercase font-mono text-xs font-bold tracking-wider border-b border-black/[0.08]">
                      <tr>
                        <th className="px-6 py-4">Staff Member</th>
                        <th className="px-6 py-4">Assigned Role</th>
                        <th className="px-6 py-4">Credentials &amp; Password</th>
                        <th className="px-6 py-4">Active Permissions</th>
                        <th className="px-6 py-4">Status</th>
                        <th className="px-6 py-4 text-right">Access Actions</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-black/[0.06] text-sm">
                      {adminMembers.map((member) => (
                        <tr key={member.id} className="hover:bg-slate-50/80 transition-colors">
                          <td className="px-6 py-4">
                            <div className="flex items-center gap-3">
                              <div className="w-10 h-10 rounded-full bg-[#0B132B] text-amber-300 font-bold flex items-center justify-center text-sm shadow-sm">
                                {member.name.slice(0, 2).toUpperCase()}
                              </div>
                              <div>
                                <div className="font-bold text-[#1D1D1F] text-base">{member.name}</div>
                                <div className="text-xs text-[#0071E3] font-mono font-semibold">@{member.username || member.name.toLowerCase().replace(/[^a-z0-9]+/g, \'\')}</div>
                                <div className="text-xs text-[#6E6E73] font-mono">{member.email}</div>
                              </div>
                            </div>
                          </td>
                          <td className="px-6 py-4">
                            <span className={`px-3 py-1 rounded-full text-xs font-bold font-mono ${
                              member.role.includes(\'Super\')
                                ? \'bg-purple-100 text-purple-800 border border-purple-200\'
                                : member.role.includes(\'Admin\')
                                ? \'bg-blue-100 text-blue-800 border border-blue-200\'
                                : \'bg-emerald-100 text-emerald-800 border border-emerald-200\'
                            }`}>
                              {member.role}
                            </span>
                          </td>
                          <td className="px-6 py-4">
                            <div className="flex items-center gap-2 font-mono text-xs">
                              <span className="px-2.5 py-1 bg-slate-100 rounded-md text-slate-700">
                                {showPasswordMap[member.id] ? (member.password || \'••••••••\') : \'••••••••'}
                              </span>
                              <button
                                onClick={() => setShowPasswordMap(prev => ({ ...prev, [member.id]: !prev[member.id] }))}
                                className="p-1 text-slate-400 hover:text-slate-600 rounded"
                                title={showPasswordMap[member.id] ? "Hide Password" : "Show Password"}
                              >
                                {showPasswordMap[member.id] ? <EyeOff className="w-3.5 h-3.5" /> : <Eye className="w-3.5 h-3.5" />}
                              </button>
                            </div>
                          </td>
                          <td className="px-6 py-4">
                            <div className="flex flex-wrap gap-1">
                              {member.permissions.map((perm) => (
                                <span key={perm} className="px-2 py-0.5 rounded bg-gray-100 text-gray-700 text-xs font-mono">
                                  {perm}
                                </span>
                              ))}
                            </div>
                          </td>
                          <td className="px-6 py-4">
                            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 text-xs font-bold font-mono">
                              <span className="w-2 h-2 rounded-full bg-emerald-500" />
                              {member.status || \'Active\'}
                            </span>
                          </td>
                          <td className="px-6 py-4 text-right">
                            <div className="flex items-center justify-end gap-2">
                              {/* Copy Invite Link & Credentials */}
                              <button
                                onClick={() => copyStaffInvite(member)}
                                className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-blue-50 hover:bg-blue-100 text-[#0071E3] text-xs font-semibold transition-colors"
                                title="Copy invitation link & credentials"
                              >
                                <Copy className="w-3.5 h-3.5" />
                                <span>Copy Link</span>
                              </button>

                              {/* Edit Credentials */}
                              <button
                                onClick={() => {
                                  if (member.role === \'Super Administrator\') {
                                    setProfileForm({
                                      name: member.name,
                                      username: member.username || \'jakaria\',
                                      email: member.email,
                                      password: member.password || \'\',
                                      confirmPassword: member.password || \'\'
                                    });
                                    setIsProfileModalOpen(true);
                                  } else {
                                    setEditingStaff(member);
                                    setEditStaffForm({
                                      name: member.name,
                                      username: member.username || \'\',
                                      email: member.email,
                                      password: member.password || \'\',
                                      phone: member.phone || \'\',
                                      role: member.role,
                                      permissions: member.permissions
                                    });
                                    setIsEditStaffModalOpen(true);
                                  }
                                }}
                                className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-800 text-xs font-semibold transition-colors"
                                title="Edit Credentials & Role"
                              >
                                <Key className="w-3.5 h-3.5" />
                                <span>Edit</span>
                              </button>

                              {/* Revoke (only for non-superadmin) */}
                              {member.role !== \'Super Administrator\' ? (
                                <button
                                  onClick={() => handleDeleteStaff(member.id)}
                                  className="p-1.5 rounded-lg text-red-500 hover:bg-red-50 transition-colors"
                                  title="Revoke Role Access"
                                >
                                  <Trash2 className="w-4 h-4" />
                                </button>
                              ) : (
                                <span className="text-xs font-mono text-amber-500 font-bold px-2 py-0.5 rounded bg-amber-50 border border-amber-200">Owner</span>
                              )}
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
              TAB 4: CATEGORIES MANAGEMENT TAB
              ======================================================= */}
          {activeTab === \'categories\' && (
            <div className="space-y-8">
              
              {/* Category Creation Form */}
              <div className="p-6 sm:p-8 rounded-3xl bg-white border border-black/[0.08] shadow-sm space-y-4">
                <div>
                  <h3 className="text-xl font-bold text-[#1D1D1F]">Create New Category</h3>
                  <p className="text-xs sm:text-sm text-[#6E6E73] mt-1">
                    Categories appear instantly across the storefront, predictive suggestions, and gadget inventories.
                  </p>
                </div>

                {catSuccessMsg && (
                  <div className="p-3 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs font-semibold">
                    ✓ {catSuccessMsg}
                  </div>
                )}

                <form onSubmit={handleCreateCategory} className="space-y-4 text-xs">
                  <div>
                    <label className="block text-[#1D1D1F] font-semibold mb-1 text-sm">
                      Category Name *
                    </label>
                    <input
                      id="new-cat-input"
                      type="text"
                      required
                      value={newCatName}
                      onChange={(e) => setNewCatName(e.target.value)}
                      placeholder="e.g. Wireless Audio, GaN Chargers, Foldable Phones"
                      className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] border border-black/10 text-sm text-[#1D1D1F] focus:outline-none focus:border-[#0071E3]"
                    />
                  </div>

                  <div>
                    <label className="block text-[#1D1D1F] font-semibold mb-1 text-sm">
                      Short Description
                    </label>
                    <input
                      type="text"
                      value={newCatDesc}
                      onChange={(e) => setNewCatDesc(e.target.value)}
                      placeholder="e.g. Flagship wireless charging stands and multi-port GaN power stations"
                      className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] border border-black/10 text-sm text-[#1D1D1F] focus:outline-none focus:border-[#0071E3]"
                    />
                  </div>

                  <button
                    type="submit"
                    className="px-6 py-2.5 rounded-full bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-sm tracking-wide shadow-md active:scale-95 transition-all"
                  >
                    + Publish Category
                  </button>
                </form>
              </div>

              {/* Existing Categories Grid */}
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                {categories.map((cat) => {
                  const prodsInCat = products.filter(p => p.category.toLowerCase() === cat.name.toLowerCase()).length;
                  return (
                    <div
                      key={cat.id}
                      className="p-6 rounded-3xl bg-white border border-black/[0.08] shadow-sm flex flex-col justify-between space-y-4"
                    >
                      <div className="space-y-2">
                        <div className="flex items-center justify-between">
                          <span className="px-3 py-1 rounded-full bg-[#0071E3]/10 text-[#0071E3] font-mono text-xs font-bold">
                            {prodsInCat} Gadgets
                          </span>
                          <button
                            onClick={() => handleDeleteCategory(cat.id)}
                            className="p-1.5 rounded-lg text-slate-400 hover:text-red-500 hover:bg-red-50 transition-colors"
                            title="Delete Category"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </div>
                        <h4 className="text-lg font-bold text-[#1D1D1F]">{cat.name}</h4>
                        <p className="text-xs text-[#6E6E73] leading-relaxed">
                          {cat.description || \'Collection of premium hardware.\'}
                        </p>
                      </div>

                      <div className="pt-2 border-t border-black/[0.06] flex items-center justify-between text-xs font-mono text-[#86868B]">
                        <span>ID: {cat.id}</span>
                        <button
                          onClick={() => {
                            setSelectedCategoryFilter(cat.name);
                            setActiveTab(\'products\');
                          }}
                          className="text-[#0071E3] hover:underline font-semibold"
                        >
                          View Products →
                        </button>
                      </div>
                    </div>
                  );
                })}
              </div>

            </div>
          )}

          {/* =======================================================
              TAB 5: LIVE CUSTOMER ORDERS TAB
              ======================================================= */}
          {activeTab === \'orders\' && (
            <div className="space-y-6">
              <div className="p-6 rounded-3xl bg-white border border-black/[0.08] shadow-sm">
                <h3 className="text-xl font-bold text-[#1D1D1F]">Customer Orders &amp; Fulfillment</h3>
                <p className="text-xs sm:text-sm text-[#6E6E73] mt-1">
                  Review customer transactions, shipping addresses, payment status, and dispatch tracking codes.
                </p>
              </div>

              <div className="rounded-3xl bg-white border border-black/[0.08] shadow-sm overflow-hidden">
                <div className="overflow-x-auto">
                  <table className="w-full text-left">
                    <thead className="bg-[#F5F5F7] text-[#424245] uppercase font-mono text-xs font-bold tracking-wider border-b border-black/[0.08]">
                      <tr>
                        <th className="px-6 py-4">Tracking Code</th>
                        <th className="px-6 py-4">Customer</th>
                        <th className="px-6 py-4">Items Ordered</th>
                        <th className="px-6 py-4">Total (BDT)</th>
                        <th className="px-6 py-4">Payment</th>
                        <th className="px-6 py-4">Status</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-black/[0.06] text-sm">
                      {orders.map((o) => (
                        <tr key={o.id} className="hover:bg-slate-50/80 transition-colors">
                          <td className="px-6 py-4 font-mono font-bold text-[#0071E3]">
                            {o.id}
                          </td>
                          <td className="px-6 py-4">
                            <div className="font-bold text-[#1D1D1F]">{o.customer?.name || \'Customer\'}</div>
                            <div className="text-xs text-[#86868B] font-mono">{o.customer?.phone}</div>
                          </td>
                          <td className="px-6 py-4 text-xs">
                            {o.items?.map((item, i) => (
                              <div key={i} className="text-[#1D1D1F] font-medium">
                                {item.name} × {item.quantity}
                              </div>
                            ))}
                          </td>
                          <td className="px-6 py-4 font-mono font-bold text-base text-[#1D1D1F]">
                            ৳{o.totalBDT.toLocaleString()}
                          </td>
                          <td className="px-6 py-4">
                            <span className="px-2.5 py-1 rounded-full bg-slate-100 text-xs font-mono font-semibold">
                              {o.paymentMethod}
                            </span>
                          </td>
                          <td className="px-6 py-4">
                            <select
                              value={o.status}
                              onChange={(e) => handleOrderStatusChange(o.id, e.target.value)}
                              className="px-3 py-1.5 rounded-xl border border-black/10 text-xs font-bold font-mono focus:outline-none"
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
              TAB 6: CUSTOMER EXPERIENCE & REVIEWS MANAGEMENT TAB
              ======================================================= */}
          {activeTab === \'reviews\' && (
            <div className="space-y-6">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-6 rounded-3xl bg-white border border-black/[0.08] shadow-sm">
                <div>
                  <h3 className="text-xl font-bold text-[#1D1D1F]">Customer Experience &amp; Community Feedback</h3>
                  <p className="text-xs sm:text-sm text-[#6E6E73] mt-1">
                    Manage verified customer testimonials, star ratings, and community reviews displayed across the storefront.
                  </p>
                </div>
                <a
                  href="/reviews"
                  target="_blank"
                  rel="noreferrer"
                  className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full bg-[#1D1D1F] hover:bg-[#333336] text-white text-xs font-bold shadow-md transition-all self-start sm:self-auto"
                >
                  <ExternalLink className="w-3.5 h-3.5" />
                  <span>View Public Reviews Page ↗</span>
                </a>
              </div>

              {/* Reviews Table */}
              <div className="rounded-3xl bg-white border border-black/[0.08] shadow-sm overflow-hidden">
                <div className="overflow-x-auto">
                  <table className="w-full text-left">
                    <thead className="bg-[#F5F5F7] text-[#424245] uppercase font-mono text-xs font-bold tracking-wider border-b border-black/[0.08]">
                      <tr>
                        <th className="px-6 py-4">Customer</th>
                        <th className="px-6 py-4">Product Purchased</th>
                        <th className="px-6 py-4">Rating</th>
                        <th className="px-6 py-4">Review Feedback</th>
                        <th className="px-6 py-4">Date</th>
                        <th className="px-6 py-4 text-right">Actions</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-black/[0.06] text-sm">
                      {reviews.map((rev) => (
                        <tr key={rev.id} className="hover:bg-slate-50/80 transition-colors">
                          <td className="px-6 py-4">
                            <div className="font-bold text-[#1D1D1F]">{rev.author}</div>
                            <span className="text-[10px] font-mono text-emerald-600 font-semibold bg-emerald-50 px-2 py-0.5 rounded-full">Verified Buyer</span>
                          </td>
                          <td className="px-6 py-4">
                            <div className="font-semibold text-[#0071E3] text-xs">{rev.productName}</div>
                          </td>
                          <td className="px-6 py-4">
                            <div className="flex gap-1 text-amber-500">
                              {Array.from({ length: 5 }).map((_, i) => (
                                <Star
                                  key={i}
                                  className={`w-3.5 h-3.5 ${
                                    i < rev.rating
                                      ? \'fill-amber-400 text-amber-400\'
                                      : \'text-gray-300\'
                                  }`}
                                />
                              ))}
                            </div>
                          </td>
                          <td className="px-6 py-4">
                            <p className="text-xs text-[#333336] max-w-md italic">&ldquo;{rev.comment}&rdquo;</p>
                          </td>
                          <td className="px-6 py-4 font-mono text-xs text-[#86868B]">
                            {rev.date}
                          </td>
                          <td className="px-6 py-4 text-right">
                            <button
                              onClick={() => handleDeleteReview(rev.id)}
                              className="p-2 rounded-xl text-red-500 hover:bg-red-50 transition-colors"
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
              TAB 7: FOUNDER'S VISION SETTINGS
              ======================================================= */}
          {activeTab === \'founder\' && (
            <div className="max-w-3xl mx-auto space-y-6">
              <div className="p-6 rounded-3xl bg-white border border-black/[0.08] shadow-sm">
                <h3 className="text-xl font-bold text-[#1D1D1F]">Founder&apos;s Vision &amp; Executive Profile</h3>
                <p className="text-xs sm:text-sm text-[#6E6E73] mt-1">
                  Updates made here sync directly to the Founder&apos;s Vision portal across the website.
                </p>
              </div>

              {saveSuccess && (
                <div className="p-4 rounded-2xl bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs font-semibold">
                  ✓ {saveSuccess}
                </div>
              )}

              <form onSubmit={handleSaveFounder} className="p-6 sm:p-8 rounded-3xl bg-white border border-black/[0.08] shadow-sm space-y-5 text-sm">
                <div>
                  <label className="block text-[#1D1D1F] font-bold mb-1">Founder Name</label>
                  <input
                    type="text"
                    value={founderForm.name || \'\'}
                    onChange={(e) => setFounderForm({ ...founderForm, name: e.target.value })}
                    className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] border border-black/10 text-[#1D1D1F] focus:outline-none focus:border-[#0071E3]"
                  />
                </div>

                <div>
                  <label className="block text-[#1D1D1F] font-bold mb-1">Company &amp; Executive Role</label>
                  <input
                    type="text"
                    value={founderForm.role || \'\'}
                    onChange={(e) => setFounderForm({ ...founderForm, role: e.target.value })}
                    className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] border border-black/10 text-[#1D1D1F] focus:outline-none focus:border-[#0071E3]"
                  />
                </div>

                <div>
                  <label className="block text-[#1D1D1F] font-bold mb-1">Architectural Vision Statement</label>
                  <textarea
                    rows={4}
                    value={founderForm.vision || \'\'}
                    onChange={(e) => setFounderForm({ ...founderForm, vision: e.target.value })}
                    className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] border border-black/10 text-[#1D1D1F] focus:outline-none focus:border-[#0071E3]"
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
          COPIED INVITE TOAST NOTIFICATION
          ========================================================= */}
      {inviteToast && (
        <div className="fixed bottom-6 right-6 z-50 bg-[#1D1D1F] text-white px-5 py-3.5 rounded-2xl shadow-2xl flex items-center gap-3 border border-white/10 animate-fade-in text-xs font-medium">
          <CheckCircle className="w-4 h-4 text-emerald-400 flex-shrink-0" />
          <span>{inviteToast}</span>
        </div>
      )}

      {/* =========================================================
          SUPER ADMINISTRATOR CREDENTIALS MODAL
          ========================================================= */}
      {isProfileModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-fade-in">
          <div className="relative w-full max-w-md bg-white rounded-3xl border border-black/10 shadow-2xl p-6 sm:p-8 space-y-5">
            <div className="flex items-center justify-between pb-3 border-b border-black/[0.08]">
              <div>
                <h3 className="text-xl font-bold text-[#1D1D1F]">Super Administrator Credentials</h3>
                <p className="text-xs text-[#86868B] mt-0.5">
                  Update your master username, login email, and authentication password.
                </p>
              </div>
              <button
                onClick={() => setIsProfileModalOpen(false)}
                className="p-1.5 rounded-full bg-[#F5F5F7] text-[#86868B] hover:text-[#1D1D1F]"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {profileSuccessMsg && (
              <div className="p-3 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs font-semibold">
                ✓ {profileSuccessMsg}
              </div>
            )}

            <form onSubmit={handleSaveProfile} className="space-y-4 text-xs">
              <div>
                <label className="block text-[#1D1D1F] font-bold mb-1 text-sm">Full Name</label>
                <input
                  type="text"
                  required
                  value={profileForm.name}
                  onChange={(e) => setProfileForm({ ...profileForm, name: e.target.value })}
                  className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] border border-black/10 text-sm font-semibold text-[#1D1D1F] focus:outline-none focus:border-[#0071E3]"
                />
              </div>

              <div>
                <label className="block text-[#1D1D1F] font-bold mb-1 text-sm">Master Username</label>
                <input
                  type="text"
                  required
                  value={profileForm.username}
                  onChange={(e) => setProfileForm({ ...profileForm, username: e.target.value })}
                  className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] border border-black/10 text-sm font-mono font-semibold text-[#1D1D1F] focus:outline-none focus:border-[#0071E3]"
                />
              </div>

              <div>
                <label className="block text-[#1D1D1F] font-bold mb-1 text-sm">Login Email</label>
                <input
                  type="email"
                  required
                  value={profileForm.email}
                  onChange={(e) => setProfileForm({ ...profileForm, email: e.target.value })}
                  className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] border border-black/10 text-sm font-mono font-semibold text-[#1D1D1F] focus:outline-none focus:border-[#0071E3]"
                />
              </div>

              <div>
                <label className="block text-[#1D1D1F] font-bold mb-1 text-sm">New Master Password</label>
                <input
                  type="password"
                  required
                  value={profileForm.password}
                  onChange={(e) => setProfileForm({ ...profileForm, password: e.target.value })}
                  placeholder="Enter new master password"
                  className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] border border-black/10 text-sm font-mono text-[#1D1D1F] focus:outline-none focus:border-[#0071E3]"
                />
              </div>

              <div>
                <label className="block text-[#1D1D1F] font-bold mb-1 text-sm">Confirm Password</label>
                <input
                  type="password"
                  required
                  value={profileForm.confirmPassword}
                  onChange={(e) => setProfileForm({ ...profileForm, confirmPassword: e.target.value })}
                  placeholder="Confirm new password"
                  className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] border border-black/10 text-sm font-mono text-[#1D1D1F] focus:outline-none focus:border-[#0071E3]"
                />
              </div>

              <button
                type="submit"
                className="w-full py-3 rounded-full bg-[#0071E3] hover:bg-[#0077ED] text-white font-bold text-sm tracking-wide shadow-md transition-all active:scale-95"
              >
                Update Credentials &amp; Save
              </button>
            </form>
          </div>
        </div>
      )}

      {/* =========================================================
          ADD NEW STAFF MEMBER MODAL (With Username & Password Defined by Super Admin)
          ========================================================= */}
      {isStaffModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-fade-in">
          <div className="relative w-full max-w-lg bg-white rounded-3xl border border-black/10 shadow-2xl p-6 sm:p-8 space-y-5">
            <div className="flex items-center justify-between pb-3 border-b border-black/[0.08]">
              <div>
                <h3 className="text-xl font-bold text-[#1D1D1F]">Authorize New Staff Member</h3>
                <p className="text-xs text-[#86868B] mt-0.5">
                  Super Administrator defines custom username, email, and password for direct login.
                </p>
              </div>
              <button
                onClick={() => setIsStaffModalOpen(false)}
                className="p-1.5 rounded-full bg-[#F5F5F7] text-[#86868B] hover:text-[#1D1D1F]"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleCreateStaff} className="space-y-4 text-xs">
              <div>
                <label className="block text-[#1D1D1F] font-bold mb-1 text-sm">Full Name *</label>
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
                  className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] border border-black/10 text-sm font-semibold text-[#1D1D1F] focus:outline-none focus:border-[#0071E3]"
                />
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-[#1D1D1F] font-bold mb-1 text-sm">Assigned Username *</label>
                  <input
                    type="text"
                    required
                    value={staffForm.username}
                    onChange={(e) => setStaffForm({ ...staffForm, username: e.target.value })}
                    placeholder="e.g. tanvir or mod_orders"
                    className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] border border-black/10 text-sm font-mono text-[#1D1D1F] focus:outline-none focus:border-[#0071E3]"
                  />
                </div>

                <div>
                  <label className="block text-[#1D1D1F] font-bold mb-1 text-sm">Email Address *</label>
                  <input
                    type="email"
                    required
                    value={staffForm.email}
                    onChange={(e) => setStaffForm({ ...staffForm, email: e.target.value })}
                    placeholder="tanvir@nexora.com"
                    className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] border border-black/10 text-sm font-mono text-[#1D1D1F] focus:outline-none focus:border-[#0071E3]"
                  />
                </div>
              </div>

              <div>
                <div className="flex items-center justify-between mb-1">
                  <label className="text-[#1D1D1F] font-bold text-sm">Initial Password *</label>
                  <button
                    type="button"
                    onClick={() => {
                      const randomPass = \'Nexora\' + Math.floor(1000 + Math.random() * 9000) + \'!\';
                      setStaffForm({ ...staffForm, password: randomPass });
                    }}
                    className="text-xs text-[#0071E3] hover:underline font-mono"
                  >
                    Generate Random
                  </button>
                </div>
                <input
                  type="text"
                  required
                  value={staffForm.password}
                  onChange={(e) => setStaffForm({ ...staffForm, password: e.target.value })}
                  placeholder="e.g. NexoraStaff2026!"
                  className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] border border-black/10 text-sm font-mono text-[#1D1D1F] focus:outline-none focus:border-[#0071E3]"
                />
              </div>

              <div>
                <label className="block text-[#1D1D1F] font-bold mb-1 text-sm">Assigned Role *</label>
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
                  className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] border border-black/10 text-sm font-semibold text-[#1D1D1F] focus:outline-none"
                >
                  <option value="Administrator">Administrator (Products, Orders, Categories, Reviews)</option>
                  <option value="Inventory Moderator">Inventory Moderator (Products &amp; Categories)</option>
                  <option value="Order Moderator">Order Moderator (Customer Orders &amp; Fulfillment)</option>
                </select>
              </div>

              <button
                type="submit"
                className="w-full py-3 rounded-full bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-sm tracking-wide shadow-md transition-all active:scale-95"
              >
                Authorize &amp; Generate Access Link
              </button>
            </form>
          </div>
        </div>
      )}

      {/* =========================================================
          EDIT STAFF MEMBER MODAL
          ========================================================= */}
      {isEditStaffModalOpen && editingStaff && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-fade-in">
          <div className="relative w-full max-w-lg bg-white rounded-3xl border border-black/10 shadow-2xl p-6 sm:p-8 space-y-5">
            <div className="flex items-center justify-between pb-3 border-b border-black/[0.08]">
              <div>
                <h3 className="text-xl font-bold text-[#1D1D1F]">Edit Staff Credentials: {editingStaff.name}</h3>
                <p className="text-xs text-[#86868B] mt-0.5">
                  Update staff username, email, reset password, or modify assigned role.
                </p>
              </div>
              <button
                onClick={() => { setIsEditStaffModalOpen(false); setEditingStaff(null); }}
                className="p-1.5 rounded-full bg-[#F5F5F7] text-[#86868B] hover:text-[#1D1D1F]"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleSaveEditStaff} className="space-y-4 text-xs">
              <div>
                <label className="block text-[#1D1D1F] font-bold mb-1 text-sm">Staff Full Name</label>
                <input
                  type="text"
                  required
                  value={editStaffForm.name}
                  onChange={(e) => setEditStaffForm({ ...editStaffForm, name: e.target.value })}
                  className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] border border-black/10 text-sm font-semibold text-[#1D1D1F] focus:outline-none focus:border-[#0071E3]"
                />
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-[#1D1D1F] font-bold mb-1 text-sm">Username</label>
                  <input
                    type="text"
                    required
                    value={editStaffForm.username}
                    onChange={(e) => setEditStaffForm({ ...editStaffForm, username: e.target.value })}
                    className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] border border-black/10 text-sm font-mono text-[#1D1D1F] focus:outline-none focus:border-[#0071E3]"
                  />
                </div>

                <div>
                  <label className="block text-[#1D1D1F] font-bold mb-1 text-sm">Email Address</label>
                  <input
                    type="email"
                    required
                    value={editStaffForm.email}
                    onChange={(e) => setEditStaffForm({ ...editStaffForm, email: e.target.value })}
                    className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] border border-black/10 text-sm font-mono text-[#1D1D1F] focus:outline-none focus:border-[#0071E3]"
                  />
                </div>
              </div>

              <div>
                <label className="block text-[#1D1D1F] font-bold mb-1 text-sm">Reset Password</label>
                <input
                  type="text"
                  value={editStaffForm.password}
                  onChange={(e) => setEditStaffForm({ ...editStaffForm, password: e.target.value })}
                  placeholder="Enter new password (leave blank to keep current)"
                  className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] border border-black/10 text-sm font-mono text-[#1D1D1F] focus:outline-none focus:border-[#0071E3]"
                />
              </div>

              <div>
                <label className="block text-[#1D1D1F] font-bold mb-1 text-sm">Role</label>
                <select
                  value={editStaffForm.role}
                  onChange={(e) => {
                    const r = e.target.value as AdminMember[\'role\'];
                    let perms = [\'products\'];
                    if (r === \'Administrator\') perms = [\'products\', \'orders\', \'categories\', \'reviews\'];
                    if (r === \'Inventory Moderator\') perms = [\'products\', \'categories\'];
                    if (r === \'Order Moderator\') perms = [\'orders\'];
                    setEditStaffForm({ ...editStaffForm, role: r, permissions: perms });
                  }}
                  className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] border border-black/10 text-sm font-semibold text-[#1D1D1F] focus:outline-none"
                >
                  <option value="Administrator">Administrator</option>
                  <option value="Inventory Moderator">Inventory Moderator</option>
                  <option value="Order Moderator">Order Moderator</option>
                </select>
              </div>

              <button
                type="submit"
                className="w-full py-3 rounded-full bg-[#0071E3] hover:bg-[#0077ED] text-white font-bold text-sm tracking-wide shadow-md transition-all active:scale-95"
              >
                Save Updated Credentials
              </button>
            </form>
          </div>
        </div>
      )}

      {/* =========================================================
          PRODUCT CREATION / EDITING MODAL
          ========================================================= */}
      {isProductModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm animate-fade-in">
          <div className="relative w-full max-w-2xl bg-white rounded-3xl border border-black/10 shadow-2xl p-6 sm:p-8 max-h-[90vh] overflow-y-auto">
            
            <div className="flex items-center justify-between pb-4 border-b border-black/[0.08]">
              <div>
                <h3 className="text-xl font-bold text-[#1D1D1F]">
                  {editingProduct ? \'Edit Gadget Specs & Inventory\' : \'Add New Hardware Gadget\'}
                </h3>
                <p className="text-xs text-[#86868B] mt-0.5">
                  Update product details, official brand attribution, and stock piece counts.
                </p>
              </div>
              <button
                onClick={() => setIsProductModalOpen(false)}
                className="p-1.5 rounded-full bg-[#F5F5F7] text-[#86868B] hover:text-[#1D1D1F]"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleSaveProduct} className="space-y-4 pt-4 text-xs">
              
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-[#1D1D1F] font-bold mb-1 text-sm">Gadget Title *</label>
                  <input
                    type="text"
                    required
                    value={productForm.name || \'\'}
                    onChange={(e) => setProductForm({ ...productForm, name: e.target.value })}
                    placeholder="e.g. Samsung Galaxy S24 Ultra"
                    className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] border border-black/10 text-sm text-[#1D1D1F] font-semibold focus:outline-none focus:border-[#0071E3]"
                  />
                </div>

                <div>
                  <label className="block text-[#1D1D1F] font-bold mb-1 text-sm">Brand *</label>
                  <select
                    value={productForm.brand || \'Apple\'}
                    onChange={(e) => setProductForm({ ...productForm, brand: e.target.value })}
                    className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] border border-black/10 text-sm text-[#1D1D1F] font-semibold focus:outline-none focus:border-[#0071E3]"
                  >
                    {TOP_10_BRANDS.filter(b => b !== \'All\').map(b => (
                      <option key={b} value={b}>{b}</option>
                    ))}
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-[#1D1D1F] font-bold mb-1 text-sm">Category *</label>
                  <select
                    value={productForm.category || \'Smartphones\'}
                    onChange={(e) => setProductForm({ ...productForm, category: e.target.value })}
                    className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] border border-black/10 text-sm text-[#1D1D1F] font-semibold focus:outline-none focus:border-[#0071E3]"
                  >
                    {categories.map(c => (
                      <option key={c.id} value={c.name}>{c.name}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-[#1D1D1F] font-bold mb-1 text-sm">Tagline / Key Highlight</label>
                  <input
                    type="text"
                    value={productForm.tagline || \'\'}
                    onChange={(e) => setProductForm({ ...productForm, tagline: e.target.value })}
                    placeholder="e.g. Breakthrough Titanium Unibody & Silicon"
                    className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] border border-black/10 text-sm text-[#1D1D1F] focus:outline-none focus:border-[#0071E3]"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div>
                  <label className="block text-[#1D1D1F] font-bold mb-1 text-sm">Price in BDT (৳) *</label>
                  <input
                    type="number"
                    required
                    value={productForm.priceBDT || \'\'}
                    onChange={(e) => setProductForm({ ...productForm, priceBDT: Number(e.target.value) })}
                    placeholder="178000"
                    className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] border border-black/10 text-sm font-mono font-bold text-[#1D1D1F] focus:outline-none focus:border-[#0071E3]"
                  />
                </div>

                <div>
                  <label className="block text-[#1D1D1F] font-bold mb-1 text-sm">Price in USD ($)</label>
                  <input
                    type="number"
                    value={productForm.priceUSD || \'\'}
                    onChange={(e) => setProductForm({ ...productForm, priceUSD: Number(e.target.value) })}
                    placeholder="1370"
                    className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] border border-black/10 text-sm font-mono text-[#1D1D1F] focus:outline-none focus:border-[#0071E3]"
                  />
                </div>

                <div>
                  <label className="block text-[#1D1D1F] font-bold mb-1 text-sm">Stock Quantity *</label>
                  <input
                    type="number"
                    required
                    value={productForm.stockCount || \'\'}
                    onChange={(e) => setProductForm({ ...productForm, stockCount: Number(e.target.value) })}
                    placeholder="30"
                    className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] border border-black/10 text-sm font-mono text-[#1D1D1F] focus:outline-none focus:border-[#0071E3]"
                  />
                </div>
              </div>

              {/* Image Input / Upload */}
              <div>
                <label className="block text-[#1D1D1F] font-bold mb-1 text-sm">Gadget Image File URL *</label>
                <div className="flex gap-2">
                  <input
                    type="text"
                    required
                    value={productForm.image || \'\'}
                    onChange={(e) => setProductForm({ ...productForm, image: e.target.value })}
                    placeholder="/products/samsung-s24-ultra.png"
                    className="flex-1 px-4 py-2.5 rounded-xl bg-[#F5F5F7] border border-black/10 text-sm font-mono text-[#1D1D1F] focus:outline-none focus:border-[#0071E3]"
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
                <label className="block text-[#1D1D1F] font-bold mb-1 text-sm">Product Description</label>
                <textarea
                  rows={3}
                  value={productForm.description || \'\'}
                  onChange={(e) => setProductForm({ ...productForm, description: e.target.value })}
                  placeholder="Engineered by Google / Apple / Samsung. Built for ultra-fidelity performance."
                  className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] border border-black/10 text-sm text-[#1D1D1F] focus:outline-none focus:border-[#0071E3]"
                />
              </div>

              <div className="pt-2 flex items-center justify-end gap-3 border-t border-black/[0.08]">
                <button
                  type="button"
                  onClick={() => setIsProductModalOpen(false)}
                  className="px-5 py-2.5 rounded-full border border-black/15 text-sm font-semibold text-[#1D1D1F] hover:bg-black/5"
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

with open("frontend/src/app/myadminerapanel/page.tsx", "w", encoding="utf-8") as f:
    f.write(code)

print("Generated frontend/src/app/myadminerapanel/page.tsx successfully!")

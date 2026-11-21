'use client';

import React, { useState, useEffect, useRef } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { usePathname, useRouter } from 'next/navigation';
import { useCart } from '../lib/cartContext';
import { useSettings } from '../lib/settingsContext';
import { Product } from '../lib/types';
import { fetchProducts } from '../lib/api';
import { ShoppingBag, User, Sun, Moon, Search, X, ArrowRight, Heart } from 'lucide-react';

export const Navbar: React.FC = () => {
  const pathname = usePathname();
  const router = useRouter();
  const { totalCount, setIsCartOpen, setIsAuthModalOpen, user, wishlist, setIsWishlistOpen } = useCart();
  const { theme, toggleTheme } = useSettings();

  // Search Modal State
  const [isSearchOpen, setIsSearchOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [products, setProducts] = useState<Product[]>([]);
  const [isScrolled, setIsScrolled] = useState(false);
  const searchInputRef = useRef<HTMLInputElement>(null);
  const navContainerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetchProducts().then(data => setProducts(data || []));
  }, []);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };
    handleScroll();
    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  useEffect(() => {
    if (isSearchOpen) {
      setTimeout(() => searchInputRef.current?.focus(), 50);
      const handleKeyDown = (e: KeyboardEvent) => {
        if (e.key === 'Escape') setIsSearchOpen(false);
      };
      const handleClickOutside = (e: MouseEvent) => {
        if (navContainerRef.current && !navContainerRef.current.contains(e.target as Node)) {
          setIsSearchOpen(false);
        }
      };
      window.addEventListener('keydown', handleKeyDown);
      document.addEventListener('mousedown', handleClickOutside);
      return () => {
        window.removeEventListener('keydown', handleKeyDown);
        document.removeEventListener('mousedown', handleClickOutside);
      };
    } else {
      setSearchQuery('');
    }
  }, [isSearchOpen]);

  // Don't render public floating navbar on Admin panel or App Simulator
  if (pathname?.startsWith('/myadminerapanel') || pathname?.startsWith('/app-demo')) {
    return null;
  }

  // Predictive matching suggestions (Starts immediately on open or from 1 character)
  const matchingSuggestions = searchQuery.trim() === ''
    ? products.slice(0, 10)
    : products.filter(p => {
        const q = searchQuery.toLowerCase().trim();
        return (
          p.name.toLowerCase().includes(q) ||
          (p.brand && p.brand.toLowerCase().includes(q))
        );
      });

  const handleSelectProduct = (productId: string) => {
    setIsSearchOpen(false);
    router.push(`/product/${productId}`);
  };

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;
    setIsSearchOpen(false);
    router.push(`/explore?q=${encodeURIComponent(searchQuery.trim())}`);
  };

  return (
    <header className="fixed top-0 left-0 right-0 z-50 flex flex-col items-center px-3 sm:px-4 py-3 sm:py-4 pointer-events-none">
      <div ref={navContainerRef} className="pointer-events-auto relative w-full max-w-5xl flex flex-col items-center">
        {/* Floating Dark Navy Capsule over Canvas with Dynamic Scroll Opacity (100% at top, 70-75% on scroll) */}
        <nav className={`flex items-center justify-between w-full px-4 sm:px-6 py-2 sm:py-2.5 rounded-full border border-white/15 dark:border-white/20 transition-all duration-300 ${
          isScrolled
            ? 'bg-[#0B132B]/75 dark:bg-[#070B18]/75 backdrop-blur-md sm:backdrop-blur-xl shadow-[0_8px_32px_rgba(11,19,43,0.30)]'
            : 'bg-[#0B132B] dark:bg-[#070B18] shadow-[0_8px_32px_rgba(11,19,43,0.45)]'
        }`}>
          
          {/* Solo Logo (Pure White Aperture Icon on Dark Navy Capsule) */}
          <Link href="/" className="flex items-center group py-0.5 flex-shrink-0" aria-label="NEXORA Home">
            <div className="relative w-7 h-7 sm:w-8 sm:h-8 flex-shrink-0 transition-transform duration-500 group-hover:scale-105">
              <Image
                src="/brand/nexora_icon_white_transparent.png"
                alt="NEXORA"
                fill
                priority
                className="object-contain"
              />
            </div>
          </Link>

          {/* Inline Search Input or Navigation Links */}
          {isSearchOpen ? (
            <form onSubmit={handleSearchSubmit} className="flex-1 flex items-center mx-3 sm:mx-6 animate-fade-in">
              <Search className="w-4 h-4 text-white/70 mr-2.5 flex-shrink-0" />
              <input
                ref={searchInputRef}
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search gadgets (e.g. iPhone, AirPods, MacBook)..."
                className="w-full bg-transparent text-sm sm:text-base font-medium text-white placeholder-white/50 focus:outline-none"
              />
              {searchQuery && (
                <button
                  type="button"
                  onClick={() => setSearchQuery('')}
                  className="p-1 text-white/70 hover:text-white mr-1"
                >
                  <X className="w-4 h-4" />
                </button>
              )}
            </form>
          ) : (
            /* Navigation Links in Pure White (English) */
            <div className="hidden md:flex items-center gap-5 lg:gap-7 text-xs lg:text-sm font-medium tracking-tight text-white">
              <Link
                href="/explore"
                className="text-white/90 hover:text-[#38BDF8] transition-colors"
              >
                Gadgets
              </Link>
              <Link
                href="/founder"
                className="text-white/90 hover:text-[#38BDF8] transition-colors"
              >
                Founder&apos;s Vision
              </Link>
              <Link
                href="/track-order"
                className="text-white/90 hover:text-[#38BDF8] transition-colors"
              >
                Track Order
              </Link>
              <Link
                href="/terms"
                className="text-white/80 hover:text-[#38BDF8] transition-colors"
              >
                Terms & Conditions
              </Link>
              <Link
                href="/privacy"
                className="text-white/80 hover:text-[#38BDF8] transition-colors"
              >
                Privacy Policy
              </Link>
            </div>
          )}

          {/* Action Controls */}
          <div className="flex items-center gap-2 sm:gap-2.5 flex-shrink-0">
            {/* Search Icon Trigger / Close Toggle */}
            <button
              onClick={() => setIsSearchOpen(!isSearchOpen)}
              title={isSearchOpen ? 'Close search' : 'Search products...'}
              aria-label="Search Catalog"
              className={`p-1.5 rounded-full transition-all active:scale-95 border border-white/10 ${
                isSearchOpen ? 'bg-white/25 text-white' : 'bg-white/10 hover:bg-white/20 text-white'
              }`}
            >
              {isSearchOpen ? <X className="w-4 h-4 text-white" /> : <Search className="w-4 h-4 text-white" />}
            </button>

            {/* Theme Toggle (Default Light -> Dark) */}
            <button
              onClick={toggleTheme}
              title={theme === 'light' ? 'Switch to Dark Mode' : 'Switch to Light Mode'}
              aria-label="Toggle Theme"
              className="p-1.5 rounded-full bg-white/10 hover:bg-white/20 text-white transition-all active:scale-95 border border-white/10"
            >
              {theme === 'light' ? (
                <Moon className="w-4 h-4 text-amber-300" />
              ) : (
                <Sun className="w-4 h-4 text-amber-400" />
              )}
            </button>

            {/* Wishlist Button */}
            <button
              onClick={() => setIsWishlistOpen(true)}
              title="Saved Hardware (Wishlist)"
              aria-label="Wishlist"
              className="relative p-1.5 rounded-full bg-white/10 hover:bg-white/20 text-white transition-all active:scale-95 border border-white/10"
            >
              <Heart className={`w-4 h-4 ${wishlist.length > 0 ? 'fill-rose-400 text-rose-400' : 'text-white'}`} />
              {wishlist.length > 0 && (
                <span className="absolute -top-1 -right-1 flex items-center justify-center min-w-[16px] h-4 px-1 rounded-full bg-rose-500 text-white text-[9px] font-bold">
                  {wishlist.length}
                </span>
              )}
            </button>

            {/* User Sign In / Account in Pure White with Active Indicator */}
            <button
              onClick={() => setIsAuthModalOpen(true)}
              className="flex items-center gap-1.5 px-2.5 sm:px-3 py-1.5 rounded-full text-xs sm:text-sm font-medium text-white hover:bg-white/10 hover:text-[#38BDF8] transition-colors"
              title={user ? `Signed in as ${user.name}` : 'Sign in to NEXORA'}
            >
              <div className="relative flex items-center justify-center">
                <User className="w-4 h-4 text-white" />
                {user && (
                  <span className="absolute -top-0.5 -right-0.5 w-2 h-2 rounded-full bg-emerald-400 ring-2 ring-[#0B132B]" />
                )}
              </div>
              <span className="hidden sm:inline">
                {user ? user.name.split(' ')[0] : 'Sign In'}
              </span>
            </button>

            {/* Cart Bag Button (Only Bag Icon on Mobile, Bag + Label on Desktop) */}
            <button
              onClick={() => setIsCartOpen(true)}
              title="Shopping Bag"
              aria-label="Shopping Bag"
              className="relative flex items-center justify-center p-2 sm:px-3.5 sm:py-1.5 rounded-full bg-white hover:bg-slate-100 dark:bg-[#0071E3] dark:hover:bg-[#0077ED] text-[#0B132B] dark:text-white transition-all shadow-md active:scale-95"
            >
              <ShoppingBag className="w-4 h-4 stroke-[2.2] text-[#0B132B] dark:text-white" />
              <span className="hidden sm:inline text-xs sm:text-sm font-bold ml-1.5 text-[#0B132B] dark:text-white">Bag</span>
              {totalCount > 0 && (
                <span className="absolute -top-1 -right-1 sm:static sm:ml-1.5 flex items-center justify-center min-w-[18px] sm:min-w-[22px] h-[18px] sm:h-[22px] px-1 sm:px-1.5 rounded-full bg-[#0071E3] text-white dark:bg-white dark:text-[#0071E3] text-[10px] sm:text-xs font-bold leading-none shadow-sm">
                  {totalCount}
                </span>
              )}
            </button>
          </div>
        </nav>

        {/* Attached Dropdown Suggestions beneath Navbar (No background blur, page fully visible!) */}
        {isSearchOpen && (
          <div className="absolute top-full mt-2 w-full max-w-2xl bg-white dark:bg-[#121624] rounded-2xl border border-black/10 dark:border-white/15 shadow-[0_12px_40px_rgba(0,0,0,0.2)] overflow-hidden animate-fade-in z-50">
            {/* Suggestions Container: STRICTLY PRODUCT TITLES ONLY LINE-BY-LINE */}
            <div className="max-h-80 sm:max-h-96 overflow-y-auto divide-y divide-black/[0.05] dark:divide-white/10">
              <div className="px-5 py-2.5 bg-[#F5F5F7] dark:bg-[#1A1F30] text-xs font-semibold tracking-wider uppercase text-[#86868B] flex items-center justify-between">
                <span>
                  {searchQuery.trim().length > 0
                    ? `Matching Products (${matchingSuggestions.length})`
                    : 'Popular Catalog Suggestions'}
                </span>
                <span className="text-[11px] font-normal lowercase text-[#86868B]">Click title to open</span>
              </div>
              {matchingSuggestions.length > 0 ? (
                matchingSuggestions.map((product) => (
                  <button
                    key={product.id}
                    onClick={() => handleSelectProduct(product.id)}
                    className="w-full text-left px-5 py-3 hover:bg-[#F5F5F7] dark:hover:bg-white/5 transition-colors flex items-center justify-between group"
                  >
                    {/* Strictly Product Title ONLY */}
                    <span className="text-sm sm:text-base font-medium text-[#1D1D1F] dark:text-slate-100 group-hover:text-[#0071E3] dark:group-hover:text-[#2997FF] transition-colors truncate">
                      {product.name}
                    </span>
                    <ArrowRight className="w-4 h-4 text-[#86868B] group-hover:text-[#0071E3] dark:group-hover:text-[#2997FF] group-hover:translate-x-1 transition-all flex-shrink-0 ml-3" />
                  </button>
                ))
              ) : (
                <div className="p-6 text-center text-sm text-[#86868B]">
                  No product found matching &quot;{searchQuery}&quot;.
                </div>
              )}
            </div>

            {/* Search Footer Tip */}
            <div className="px-5 py-2.5 bg-[#F5F5F7]/80 dark:bg-[#161B2B] text-xs text-[#86868B] flex items-center justify-between border-t border-black/[0.05] dark:border-white/10">
              <span>Press <kbd className="px-1.5 py-0.5 rounded bg-black/10 dark:bg-white/15 font-mono text-[11px]">Enter</kbd> to search catalog</span>
              <button
                type="button"
                onClick={handleSearchSubmit}
                className="text-[#0071E3] dark:text-[#2997FF] font-medium hover:underline"
              >
                Search in Catalog →
              </button>
            </div>
          </div>
        )}
      </div>
    </header>
  );
};

'use client';

import React, { useState, useEffect, useRef, Suspense } from 'react';
import { useSearchParams } from 'next/navigation';
import Link from 'next/link';
import { Product } from '../../lib/types';
import { fetchProducts } from '../../lib/api';
import { ProductCard } from '../../components/ProductCard';
import { Search, Sparkles, ArrowRight, X, Filter } from 'lucide-react';

const TOP_10_BRANDS = [
  'All Brands',
  'Apple',
  'Samsung',
  'Xiaomi',
  'Oppo',
  'Vivo',
  'OnePlus',
  'Google',
  'Realme',
  'Anker',
  'Sony'
];

const CATEGORIES = [
  'All Categories',
  'Smartphones',
  'Earbuds',
  'Audio',
  'Chargers & Power',
  'Smartwatches',
  'Tablets & Laptops',
  'Cases & Accessories'
];

function ExploreContent() {
  const searchParams = useSearchParams();
  const initialCategory = searchParams.get('category') || 'All Categories';
  const initialBrand = searchParams.get('brand') || 'All Brands';
  const initialQuery = searchParams.get('q') || '';

  const [products, setProducts] = useState<Product[]>([]);
  const [activeCategory, setActiveCategory] = useState<string>(initialCategory);
  const [activeBrand, setActiveBrand] = useState<string>(initialBrand);
  const [searchQuery, setSearchQuery] = useState<string>(initialQuery);
  const [loading, setLoading] = useState(true);
  const [isSearchFocused, setIsSearchFocused] = useState(false);
  const searchContainerRef = useRef<HTMLDivElement>(null);
  const searchInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    fetchProducts().then(data => {
      setProducts(data || []);
      setLoading(false);
    });
  }, []);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (searchContainerRef.current && !searchContainerRef.current.contains(event.target as Node)) {
        setIsSearchFocused(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  useEffect(() => {
    const cat = searchParams.get('category');
    if (cat) setActiveCategory(cat);
    const br = searchParams.get('brand');
    if (br) setActiveBrand(br);
    const q = searchParams.get('q');
    if (q) setSearchQuery(q);
  }, [searchParams]);

  // Predictive real-time suggestions: STRICTLY PRODUCT TITLES ONLY, LINE-BY-LINE
  const suggestions = searchQuery.trim() === ''
    ? products.slice(0, 10)
    : products.filter(p => {
        const q = searchQuery.toLowerCase().trim();
        return (
          p.name.toLowerCase().includes(q) ||
          (p.brand && p.brand.toLowerCase().includes(q))
        );
      });

  const filtered = products.filter(p => {
    const matchesCategory =
      activeCategory === 'All Categories' ||
      activeCategory === 'All' ||
      p.category.toLowerCase().includes(activeCategory.toLowerCase());

    const matchesBrand =
      activeBrand === 'All Brands' ||
      activeBrand === 'All' ||
      (p.brand && p.brand.toLowerCase() === activeBrand.toLowerCase());

    const matchesSearch =
      searchQuery === '' ||
      p.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (p.brand && p.brand.toLowerCase().includes(searchQuery.toLowerCase())) ||
      p.tagline.toLowerCase().includes(searchQuery.toLowerCase()) ||
      p.category.toLowerCase().includes(searchQuery.toLowerCase());

    return matchesCategory && matchesBrand && matchesSearch;
  });

  return (
    <div className="min-h-screen bg-[#F7F4EE] dark:bg-[#0B0B0F] pt-28 sm:pt-32 pb-24 px-4 sm:px-6">
      <div className="max-w-7xl mx-auto space-y-8 sm:space-y-10">
        
        {/* Header Stage */}
        <div className="text-center max-w-3xl mx-auto space-y-3">
          <div className="inline-flex items-center gap-1.5 px-3.5 py-1 rounded-full bg-white dark:bg-[#14141B] border border-black/[0.08] dark:border-white/10 text-xs font-mono uppercase tracking-widest text-[#0071E3] font-semibold">
            <Sparkles className="w-3.5 h-3.5 text-[#0071E3]" />
            <span>Official Authorized Catalog</span>
          </div>
          <h1 className="text-3xl sm:text-4xl md:text-5xl font-semibold text-[#1D1D1F] dark:text-white tracking-tight">
            Top 10 Global Brands Archive
          </h1>
          <p className="text-sm sm:text-base text-[#424245] dark:text-[#A1A1A6] max-w-2xl mx-auto leading-relaxed">
            Authentic flagship hardware from Apple, Samsung, Xiaomi, Oppo, Vivo, OnePlus, Google, Realme, Anker, and Sony—complete with genuine manufacturer warranties.
          </p>

          {/* Predictive Search Bar Stage */}
          <div ref={searchContainerRef} className="pt-3 max-w-xl mx-auto relative text-left">
            <div className="relative flex items-center">
              <button
                type="button"
                onClick={() => {
                  setIsSearchFocused(true);
                  searchInputRef.current?.focus();
                }}
                className="absolute left-3.5 p-1 text-[#86868B] hover:text-[#0071E3] transition-colors"
                aria-label="Search"
              >
                <Search className="w-4 h-4" />
              </button>
              <input
                ref={searchInputRef}
                type="text"
                value={searchQuery}
                onFocus={() => setIsSearchFocused(true)}
                onClick={() => setIsSearchFocused(true)}
                onChange={(e) => {
                  setSearchQuery(e.target.value);
                  setIsSearchFocused(true);
                }}
                placeholder="Type any letter or product name..."
                className="w-full pl-11 pr-10 py-3.5 rounded-2xl bg-white dark:bg-[#14141B] border border-black/10 dark:border-white/15 focus:border-[#0071E3] focus:ring-2 focus:ring-[#0071E3]/20 focus:outline-none text-base text-[#1D1D1F] dark:text-white placeholder-[#86868B] shadow-sm transition-all"
              />
              {searchQuery && (
                <button
                  onClick={() => setSearchQuery('')}
                  className="absolute right-4 text-[#86868B] hover:text-[#1D1D1F] dark:hover:text-white p-1"
                  aria-label="Clear Search"
                >
                  <X className="w-4 h-4" />
                </button>
              )}
            </div>

            {/* Line-by-Line Floating Predictive Suggestions Dropdown: TITLES ONLY */}
            {isSearchFocused && (
              <div className="absolute top-full left-0 right-0 mt-2 z-40 bg-white dark:bg-[#161622] rounded-2xl border border-black/10 dark:border-white/15 shadow-2xl overflow-hidden divide-y divide-black/[0.06] dark:divide-white/10 animate-fade-in max-h-80 sm:max-h-96 overflow-y-auto">
                <div className="px-4 py-2 bg-[#F5F5F7] dark:bg-[#1E1E2D] flex items-center justify-between text-[11px] font-mono font-semibold uppercase tracking-wider text-[#86868B] sticky top-0 z-10">
                  <span>
                    {searchQuery.trim().length > 0
                      ? `Instant Matches (${suggestions.length})`
                      : 'Popular Catalog Suggestions'}
                  </span>
                  <span>Click product to open</span>
                </div>
                {suggestions.length > 0 ? (
                  suggestions.map((p) => (
                    <Link
                      key={p.id}
                      href={`/product/${p.id}`}
                      onClick={() => setIsSearchFocused(false)}
                      className="block px-4 py-3 hover:bg-[#F5F5F7] dark:hover:bg-white/5 transition-colors group cursor-pointer"
                    >
                      <div className="flex items-center justify-between">
                        {/* ONLY THE PRODUCT TITLE - NO THUMBNAIL, NO PRICE, NO CATEGORY */}
                        <span className="font-medium text-sm sm:text-base text-[#1D1D1F] dark:text-slate-100 group-hover:text-[#0071E3] transition-colors truncate">
                          {p.name}
                        </span>
                        <ArrowRight className="w-4 h-4 text-[#86868B] group-hover:text-[#0071E3] group-hover:translate-x-1 transition-all flex-shrink-0 ml-3" />
                      </div>
                    </Link>
                  ))
                ) : (
                  <div className="p-4 text-center text-xs text-[#86868B]">
                    No hardware found matching &quot;{searchQuery}&quot;.
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Brand Filter Pills - Horizontally scrollable on mobile, wrapped on tablet/desktop */}
          <div className="space-y-2 pt-4">
            <div className="flex items-center justify-center gap-1.5 text-xs font-semibold text-[#86868B]">
              <Filter className="w-3.5 h-3.5" />
              <span>Select Brand:</span>
            </div>
            <div className="flex overflow-x-auto no-scrollbar sm:flex-wrap items-center justify-start sm:justify-center gap-1.5 sm:gap-2 px-1 py-1 max-w-full touch-pan-x">
              {TOP_10_BRANDS.map((brand) => (
                <button
                  key={brand}
                  onClick={() => setActiveBrand(brand)}
                  className={`flex-shrink-0 px-3.5 py-1.5 rounded-full text-xs font-semibold tracking-wide transition-all min-h-[34px] flex items-center justify-center ${
                    activeBrand.toLowerCase() === brand.toLowerCase()
                      ? 'bg-[#0071E3] text-white shadow-sm'
                      : 'bg-white dark:bg-[#14141B] border border-black/10 dark:border-white/10 text-[#555558] dark:text-[#A1A1A6] hover:text-[#1D1D1F] dark:hover:text-white'
                  }`}
                >
                  {brand}
                </button>
              ))}
            </div>
          </div>

          {/* Category Filter Pills - Horizontally scrollable on mobile, wrapped on tablet/desktop */}
          <div className="flex overflow-x-auto no-scrollbar sm:flex-wrap items-center justify-start sm:justify-center gap-1.5 sm:gap-2 px-1 py-1 max-w-full touch-pan-x pt-1">
            {CATEGORIES.map((cat) => (
              <button
                key={cat}
                onClick={() => setActiveCategory(cat)}
                className={`flex-shrink-0 px-3.5 py-1.5 rounded-full text-xs font-medium tracking-wide transition-all min-h-[34px] flex items-center justify-center ${
                  activeCategory.toLowerCase() === cat.toLowerCase()
                    ? 'bg-[#1D1D1F] dark:bg-white text-white dark:text-[#1D1D1F] shadow-sm font-semibold'
                    : 'bg-white/60 dark:bg-[#14141B]/60 border border-black/[0.06] dark:border-white/10 text-[#6E6E73] dark:text-[#A1A1A6] hover:text-[#1D1D1F] dark:hover:text-white'
                }`}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>

        {/* Results Counter & Reset */}
        <div className="flex items-center justify-between text-xs text-[#86868B] px-1 border-b border-black/[0.06] dark:border-white/10 pb-3">
          <span>Showing <strong>{filtered.length}</strong> authenticated products</span>
          {(activeBrand !== 'All Brands' || activeCategory !== 'All Categories' || searchQuery) && (
            <button
              onClick={() => {
                setActiveBrand('All Brands');
                setActiveCategory('All Categories');
                setSearchQuery('');
              }}
              className="text-[#0071E3] dark:text-[#2997FF] hover:underline font-medium"
            >
              Reset All Filters
            </button>
          )}
        </div>

        {/* Products Grid or Loading / Empty */}
        {loading ? (
          <div className="py-24 text-center">
            <div className="w-8 h-8 border-2 border-[#0071E3] border-t-transparent rounded-full animate-spin mx-auto mb-3" />
            <p className="text-xs font-mono text-[#86868B]">Loading curated hardware archive...</p>
          </div>
        ) : filtered.length === 0 ? (
          <div className="py-20 text-center bg-white dark:bg-[#14141B] rounded-3xl border border-black/[0.06] dark:border-white/10 p-12 space-y-4">
            <h3 className="text-xl font-bold text-[#1D1D1F] dark:text-white">No products found</h3>
            <p className="text-sm text-[#86868B] max-w-sm mx-auto">
              We couldn&apos;t find any gadget matching &quot;{searchQuery}&quot; for brand &quot;{activeBrand}&quot; in &quot;{activeCategory}&quot;.
            </p>
            <button
              onClick={() => {
                setActiveBrand('All Brands');
                setActiveCategory('All Categories');
                setSearchQuery('');
              }}
              className="px-6 py-2.5 rounded-full bg-[#0071E3] text-white text-xs font-semibold shadow-sm hover:bg-[#0077ED] transition-colors"
            >
              Reset Filters
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-2 md:grid-cols-2 lg:grid-cols-3 gap-3 sm:gap-6">
            {filtered.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
        )}

      </div>
    </div>
  );
}

export default function ExplorePage() {
  return (
    <Suspense fallback={<div className="min-h-screen pt-32 text-center text-xs font-mono">Loading NEXORA Archive...</div>}>
      <ExploreContent />
    </Suspense>
  );
}

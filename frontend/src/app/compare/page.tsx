'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { fetchProducts } from '../../lib/api';
import { Product } from '../../lib/types';
import { useCart } from '../../lib/cartContext';
import { 
  ArrowLeft, 
  ShoppingBag, 
  Check, 
  Layers, 
  SlidersHorizontal, 
  Cpu, 
  Battery, 
  Camera, 
  ShieldCheck,
  Sparkles,
  Plus
} from 'lucide-react';

const DEFAULT_COMPARE_PRODUCTS: Product[] = [
  {
    id: 'iphone-18-pro-max',
    name: 'Apple iPhone 18 Pro Max',
    brand: 'Apple',
    tagline: 'Titanium Unibody. Breakthrough A20 Pro Silicon.',
    category: 'Smartphones',
    priceBDT: 215000,
    priceUSD: 1599,
    inStock: true,
    stockCount: 35,
    rating: 5,
    reviewCount: 164,
    image: '/products/iphone-18-pro-max.png',
    specs: [
      'A20 Pro Neural Bionic Silicon Architecture',
      'Grade 5 Natural Titanium Frame with Micro-Arc Finish',
      '48MP Fusion Periscope Lens with 10x Optical Reach',
      '6.9-Inch Super Retina XDR 144Hz ProMotion Display'
    ],
    description: 'The ultimate flagship from Apple featuring next-generation A20 Pro neural processing.'
  },
  {
    id: 'apple-iphone-16-pro-max',
    name: 'Apple iPhone 16 Pro Max',
    brand: 'Apple',
    tagline: 'Built for Apple Intelligence. Grade 5 Titanium.',
    category: 'Smartphones',
    priceBDT: 195000,
    priceUSD: 1499,
    inStock: true,
    stockCount: 41,
    rating: 4.95,
    reviewCount: 230,
    image: '/products/apple-iphone-16-pro-max.png',
    specs: [
      'A18 Pro Chip with 6-Core GPU and Hardware Ray Tracing',
      '48MP Fusion Camera & 5x Telephoto Optical Zoom',
      '6.9-Inch Super Retina XDR OLED with Always-On Display',
      'Dedicated Touch-Sensitive Camera Control Button'
    ],
    description: 'Engineered with aerospace-grade titanium, introducing Camera Control.'
  },
  {
    id: 'samsung-s24-ultra',
    name: 'Samsung Galaxy S24 Ultra',
    brand: 'Samsung',
    tagline: 'Galaxy AI is Here. Titanium Armor Enclosure.',
    category: 'Smartphones',
    priceBDT: 185000,
    priceUSD: 1399,
    inStock: true,
    stockCount: 25,
    rating: 4.9,
    reviewCount: 140,
    image: '/products/samsung-galaxy-s24-ultra.png',
    specs: [
      'Snapdragon 8 Gen 3 for Galaxy Silicon',
      '200MP Quad Telephoto Camera with AI Nightography',
      '6.8-Inch Dynamic AMOLED 2X Flat Display with Corning Armor',
      'Embedded S-Pen Stylus with Bluetooth Remote Control'
    ],
    description: 'The definitive Android flagship with Galaxy AI capabilities.'
  }
];

export default function ComparePage() {
  const { addToCart, setIsCartOpen } = useCart();
  const [allProducts, setAllProducts] = useState<Product[]>(DEFAULT_COMPARE_PRODUCTS);
  const [selectedIds, setSelectedIds] = useState<string[]>(['iphone-18-pro-max', 'apple-iphone-16-pro-max']);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchProducts().then((data) => {
      if (data && data.length > 0) {
        setAllProducts(data);
        if (selectedIds.length === 0) {
          setSelectedIds([data[0].id, data[1]?.id || data[0].id]);
        }
      }
      setLoading(false);
    });
  }, []);

  const selectedProducts = selectedIds
    .map((id) => allProducts.find((p) => p.id === id))
    .filter(Boolean) as Product[];

  const handleSelectProduct = (index: number, newId: string) => {
    setSelectedIds((prev) => {
      const next = [...prev];
      next[index] = newId;
      return next;
    });
  };

  const handleAddSlot = () => {
    if (selectedIds.length < 3 && allProducts.length > selectedIds.length) {
      const remaining = allProducts.find((p) => !selectedIds.includes(p.id));
      if (remaining) {
        setSelectedIds([...selectedIds, remaining.id]);
      }
    }
  };

  const handleRemoveSlot = (index: number) => {
    if (selectedIds.length > 2) {
      setSelectedIds(selectedIds.filter((_, i) => i !== index));
    }
  };

  return (
    <div className="min-h-screen bg-[#F7F4EE] dark:bg-[#080E1E] pt-28 sm:pt-36 pb-20 sm:pb-24 px-4 sm:px-6 transition-colors">
      <div className="max-w-6xl mx-auto space-y-8">
        
        {/* Navigation Breadcrumb */}
        <div>
          <Link
            href="/explore"
            className="inline-flex items-center gap-2 text-xs font-semibold px-4 py-2 rounded-full bg-white dark:bg-[#121624] border border-black/10 dark:border-white/15 text-[#0071E3] hover:bg-[#0077ED] hover:text-white transition-all shadow-sm"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Hardware Archive</span>
          </Link>
        </div>

        {/* Header */}
        <div className="text-center space-y-2">
          <div className="inline-flex items-center gap-1.5 px-3 py-0.5 rounded-full bg-[#0071E3]/10 text-[#0071E3] dark:text-[#38BDF8] text-xs font-mono font-bold uppercase tracking-wider">
            <SlidersHorizontal className="w-3.5 h-3.5" />
            <span>Side-by-Side Flagship Matrix</span>
          </div>
          <h1 className="text-3xl sm:text-5xl font-semibold tracking-tight text-[#1D1D1F] dark:text-white">
            Compare Flagship Architecture
          </h1>
          <p className="text-xs sm:text-base text-[#6E6E73] dark:text-[#A1A1A6] max-w-xl mx-auto">
            Evaluate silicon power, imaging architecture, battery endurance, and pricing across genuine global flagships.
          </p>
        </div>

        {/* Comparison Matrix Table */}
        {loading ? (
          <div className="py-20 text-center font-mono text-xs text-[#86868B] animate-pulse">
            Loading telemetry comparison matrices...
          </div>
        ) : (
          <div className="rounded-3xl bg-white dark:bg-[#121624] border border-black/[0.08] dark:border-white/10 shadow-lg overflow-x-auto">
            <div className="min-w-[680px] p-6 sm:p-8 space-y-6">
              
              {/* Slot Selectors & Visual Pedestal */}
              <div className="grid grid-cols-12 gap-4 pb-6 border-b border-black/[0.06] dark:border-white/10 items-end">
                <div className="col-span-3 text-left">
                  <span className="text-xs font-mono uppercase tracking-widest text-[#86868B] block font-medium">
                    Selected Models
                  </span>
                  <p className="text-xs text-[#6E6E73] dark:text-[#A1A1A6] mt-1">
                    Choose up to 3 hardware units to benchmark simultaneously.
                  </p>
                  {selectedIds.length < 3 && (
                    <button
                      onClick={handleAddSlot}
                      className="mt-3 inline-flex items-center gap-1 px-3 py-1.5 rounded-full bg-[#0071E3]/10 text-[#0071E3] dark:text-[#38BDF8] text-xs font-semibold hover:bg-[#0071E3] hover:text-white transition-all"
                    >
                      <Plus className="w-3.5 h-3.5" />
                      <span>Add Comparison Slot</span>
                    </button>
                  )}
                </div>

                {selectedProducts.map((p, idx) => (
                  <div key={p.id + idx} className={`${selectedProducts.length === 2 ? 'col-span-4' : 'col-span-3'} space-y-3 text-center`}>
                    {/* Model Dropdown Picker */}
                    <div className="relative">
                      <select
                        value={p.id}
                        onChange={(e) => handleSelectProduct(idx, e.target.value)}
                        className="w-full text-xs font-semibold px-3 py-1.5 rounded-xl bg-[#F5F5F7] dark:bg-white/5 border border-black/10 dark:border-white/10 text-[#1D1D1F] dark:text-white focus:outline-none focus:border-[#0071E3]"
                      >
                        {allProducts.map((item) => (
                          <option key={item.id} value={item.id} className="dark:bg-[#121624]">
                            {item.name}
                          </option>
                        ))}
                      </select>
                    </div>

                    {/* Image Pedestal */}
                    <Link
                      href={`/product/${p.id}`}
                      className="relative w-full h-36 sm:h-44 rounded-2xl bg-[#E8EBF0] dark:bg-[#1A2035] p-3 flex items-center justify-center border border-black/[0.04] dark:border-white/10 block group"
                    >
                      <Image
                        src={p.image}
                        alt={p.name}
                        fill
                        className="object-contain p-2 group-hover:scale-105 transition-transform duration-500"
                      />
                    </Link>

                    <div>
                      <span className="text-[10px] font-mono uppercase tracking-wider text-[#0071E3] font-bold block">
                        {p.brand}
                      </span>
                      <h4 className="text-sm font-bold text-[#1D1D1F] dark:text-white truncate">{p.name}</h4>
                      <p className="text-base font-mono font-extrabold text-[#1D1D1F] dark:text-white mt-1">
                        ৳ {p.priceBDT.toLocaleString()}
                      </p>
                    </div>

                    <button
                      onClick={() => {
                        addToCart(p, 1, true);
                        setIsCartOpen(true);
                      }}
                      className="w-full py-2 rounded-full bg-[#0071E3] hover:bg-[#0077ED] text-white text-xs font-semibold shadow-sm transition-all flex items-center justify-center gap-1.5"
                    >
                      <ShoppingBag className="w-3.5 h-3.5" />
                      <span>Add to Bag</span>
                    </button>

                    {selectedProducts.length > 2 && (
                      <button
                        onClick={() => handleRemoveSlot(idx)}
                        className="text-[10px] text-red-500 hover:underline"
                      >
                        Remove Column
                      </button>
                    )}
                  </div>
                ))}
              </div>

              {/* Specification Comparison Rows */}
              <div className="space-y-4 text-xs">
                
                {/* Row: Official Warranty */}
                <div className="grid grid-cols-12 gap-4 py-2 border-b border-black/[0.04] dark:border-white/10 items-center">
                  <div className="col-span-3 text-left font-mono uppercase tracking-wider text-[#86868B] font-semibold">
                    Warranty &amp; Coverage
                  </div>
                  {selectedProducts.map((p, idx) => (
                    <div key={idx} className={`${selectedProducts.length === 2 ? 'col-span-4' : 'col-span-3'} text-center font-medium`}>
                      1-Year Official Manufacturer Warranty + 7-Day Replacement
                    </div>
                  ))}
                </div>

                {/* Row: Silicon Architecture / Key Specs */}
                <div className="grid grid-cols-12 gap-4 py-3 border-b border-black/[0.04] dark:border-white/10 items-start">
                  <div className="col-span-3 text-left font-mono uppercase tracking-wider text-[#86868B] font-semibold">
                    Technical Architecture
                  </div>
                  {selectedProducts.map((p, idx) => (
                    <div key={idx} className={`${selectedProducts.length === 2 ? 'col-span-4' : 'col-span-3'} space-y-1.5 text-center`}>
                      {p.specs?.map((spec, i) => (
                        <div key={i} className="p-1.5 rounded-lg bg-[#F5F5F7] dark:bg-white/5 text-[11px] font-medium text-[#1D1D1F] dark:text-slate-200">
                          {spec}
                        </div>
                      ))}
                    </div>
                  ))}
                </div>

                {/* Row: Stock Status */}
                <div className="grid grid-cols-12 gap-4 py-2 border-b border-black/[0.04] dark:border-white/10 items-center">
                  <div className="col-span-3 text-left font-mono uppercase tracking-wider text-[#86868B] font-semibold">
                    Stock Dispatch Readiness
                  </div>
                  {selectedProducts.map((p, idx) => (
                    <div key={idx} className={`${selectedProducts.length === 2 ? 'col-span-4' : 'col-span-3'} text-center`}>
                      <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-mono font-semibold ${
                        p.inStock ? 'bg-emerald-50 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-300' : 'bg-red-50 text-red-700'
                      }`}>
                        {p.inStock ? 'In Stock — Ready for Dispatch' : 'Backorder'}
                      </span>
                    </div>
                  ))}
                </div>

                {/* Row: Customer Rating */}
                <div className="grid grid-cols-12 gap-4 py-2 items-center">
                  <div className="col-span-3 text-left font-mono uppercase tracking-wider text-[#86868B] font-semibold">
                    Verified Customer Rating
                  </div>
                  {selectedProducts.map((p, idx) => (
                    <div key={idx} className={`${selectedProducts.length === 2 ? 'col-span-4' : 'col-span-3'} text-center font-bold text-amber-500 font-mono`}>
                      ★ {p.rating || 5.0} / 5.0 ({p.reviewCount || 100}+ reviews)
                    </div>
                  ))}
                </div>

              </div>

            </div>
          </div>
        )}

      </div>
    </div>
  );
}

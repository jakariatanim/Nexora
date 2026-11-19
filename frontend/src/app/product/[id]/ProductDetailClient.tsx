'use client';

import React, { useState, useEffect } from 'react';
import Image from 'next/image';
import Link from 'next/link';
import { Product, Review } from '../../../lib/types';
import { useCart } from '../../../lib/cartContext';
import { fetchReviews, submitReview } from '../../../lib/api';
import {
  ShoppingBag,
  Star,
  ShieldCheck,
  Truck,
  RefreshCw,
  ArrowLeft,
  CheckCircle2,
  MessageSquarePlus,
  User,
  LogIn,
  LogOut,
  Send,
  Sparkles,
  Heart,
  CreditCard,
  MessageCircle,
  HelpCircle,
  X,
  Layers,
  ChevronRight
} from 'lucide-react';
import { useRouter } from 'next/navigation';

export const ProductDetailClient: React.FC<{ product: Product }> = ({ product }) => {
  const { addToCart, setIsAuthModalOpen, user, logout, toggleWishlist, isInWishlist } = useCart();
  const [quantity, setQuantity] = useState(1);
  const [added, setAdded] = useState(false);
  const router = useRouter();

  // Multi-variant Selection
  const isPhone = product.category.toLowerCase().includes('phone') || product.name.toLowerCase().includes('iphone');
  const isAudio = product.category.toLowerCase().includes('audio') || product.category.toLowerCase().includes('earbud');
  const isWatch = product.category.toLowerCase().includes('watch');
  
  interface ColorFinish {
    name: string;
    hex: string;
    image?: string;
    filter?: string;
  }

  const availableColors: ColorFinish[] = isPhone
    ? [
        { name: 'Natural Titanium', hex: '#C5B9AC', filter: 'none' },
        { name: 'Space Black', hex: '#1E1F21', filter: 'brightness(0.7) contrast(1.2) grayscale(0.5)' },
        { name: 'Desert Titanium', hex: '#D19E75', filter: 'sepia(0.55) hue-rotate(-22deg) saturate(1.4) brightness(0.96)' },
        { name: 'White Titanium', hex: '#E5E7EB', filter: 'brightness(1.18) saturate(0.2) contrast(1.05)' }
      ]
    : isAudio
    ? [
        { name: 'Pure White', hex: '#F8FAFC', filter: 'none' },
        { name: 'Midnight Black', hex: '#111827', image: '/products/airpods-pro-black.png', filter: 'brightness(0.65) contrast(1.2)' },
        { name: 'Platinum Silver', hex: '#CBD5E1', filter: 'brightness(1.1) saturate(0.2)' }
      ]
    : isWatch
    ? [
        { name: 'Orange Ocean (Ultra)', hex: '#EA580C', image: product.image.includes('apple-watch') ? '/products/apple-watch-ultra-2.png' : product.image, filter: 'none' },
        { name: 'Matte Black', hex: '#18181B', image: product.image.includes('apple-watch') ? '/products/apple-watch-milanese.jpg' : product.image, filter: 'grayscale(0.95) brightness(0.6) contrast(1.3)' },
        { name: 'Natural Titanium', hex: '#C5B9AC', filter: 'sepia(0.3) saturate(0.8) brightness(1.02)' },
        { name: 'Silver Milanese', hex: '#E2E8F0', image: product.image.includes('apple-watch') ? '/products/apple-watch-milanese.jpg' : product.image, filter: 'grayscale(0.4) brightness(1.15) contrast(1.05)' }
      ]
    : [
        { name: 'Space Gray', hex: '#4B5563', filter: 'brightness(0.8) contrast(1.1)' },
        { name: 'Silver', hex: '#E2E8F0', filter: 'brightness(1.15) saturate(0.25)' },
        { name: 'Matte Black', hex: '#18181B', filter: 'brightness(0.55) contrast(1.25) grayscale(0.8)' }
      ];

  const availableStorage = isPhone
    ? [
        { label: '128GB', markup: -10000 },
        { label: '256GB', markup: 0, tag: 'Standard' },
        { label: '512GB', markup: 20000 },
        { label: '1TB', markup: 45000 }
      ]
    : null;

  const [selectedColor, setSelectedColor] = useState(availableColors[0].name);
  const [selectedStorage, setSelectedStorage] = useState(availableStorage ? '256GB' : 'Standard');
  const [activeImageIndex, setActiveImageIndex] = useState(0);
  const [isEmiModalOpen, setIsEmiModalOpen] = useState(false);

  // EMI Financing Configuration with Realistic Retail Markups:
  // 3 Months: 0% Extra (Promotional Introductory)
  // 6 Months: +3% Financing Surcharge
  // 12 Months: +6% Financing Surcharge (Standard Tenure)
  // 24 Months: +12% Financing Surcharge (Extended Tenure)
  const EMI_PLANS = [
    { months: 3, label: '3 Months Plan', markupPct: 0, tag: '0% Surcharge' },
    { months: 6, label: '6 Months Plan', markupPct: 3, tag: '+3% Bank Financing' },
    { months: 12, label: '12 Months Plan (Recommended)', markupPct: 6, tag: '+6% Bank Financing' },
    { months: 24, label: '24 Months Extended Plan', markupPct: 12, tag: '+12% Extended Financing' },
  ];

  const [selectedEmiMonths, setSelectedEmiMonths] = useState<number | null>(null);
  const [modalSelectedEmi, setModalSelectedEmi] = useState<number>(12);

  // Active color finish details & dynamic visual styling
  const currentColorObj = availableColors.find(c => c.name === selectedColor) || availableColors[0];
  const activeImageSrc = currentColorObj.image || product.image;
  const activeFilter = currentColorObj.filter || 'none';

  // Dynamic calculated price based on variant and active EMI plan
  const currentMarkup = availableStorage?.find(s => s.label === selectedStorage)?.markup || 0;
  const baseHardwarePrice = Math.max(0, product.priceBDT + currentMarkup);

  const activeEmiPlan = selectedEmiMonths ? EMI_PLANS.find(p => p.months === selectedEmiMonths) : null;
  const emiSurcharge = activeEmiPlan ? Math.round((baseHardwarePrice * activeEmiPlan.markupPct) / 100) : 0;
  const currentPrice = baseHardwarePrice + emiSurcharge;

  // Reviews & Feedback State
  const [reviews, setReviews] = useState<Review[]>([]);
  const [loadingReviews, setLoadingReviews] = useState(true);
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [feedbackName, setFeedbackName] = useState(user ? user.name : '');
  const [rating, setRating] = useState(5);
  const [hoverRating, setHoverRating] = useState(0);
  const [comment, setComment] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [submitSuccess, setSubmitSuccess] = useState(false);

  // Sync user name when user logs in
  useEffect(() => {
    if (user && !feedbackName) {
      setFeedbackName(user.name);
    }
  }, [user, feedbackName]);

  // Load reviews for this product
  useEffect(() => {
    fetchReviews().then((allReviews) => {
      const matched = allReviews.filter(
        (r) =>
          r.productId === product.id ||
          r.productName?.toLowerCase().includes(product.name.toLowerCase()) ||
          product.name.toLowerCase().includes(r.productName?.toLowerCase() || '')
      );
      // Fallback: if no specific review found, show general verified reviews
      if (matched.length > 0) {
        setReviews(matched);
      } else {
        setReviews(allReviews.slice(0, 3));
      }
      setLoadingReviews(false);
    });
  }, [product.id, product.name]);

  const handleAddToCart = () => {
    addToCart(product, quantity, true, {
      color: selectedColor,
      storage: selectedStorage,
      priceBDT: currentPrice,
    });
    setAdded(true);
    setTimeout(() => setAdded(false), 2500);
  };

  const handleBuyNow = () => {
    addToCart(product, quantity, false, {
      color: selectedColor,
      storage: selectedStorage,
      priceBDT: currentPrice,
    });
    router.push('/checkout');
  };

  const handleReviewSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!comment.trim()) return;
    setSubmitting(true);

    const payload: Partial<Review> = {
      productId: product.id,
      productName: product.name,
      author: feedbackName.trim() || (user ? user.name : 'Verified Customer'),
      rating: rating,
      comment: comment.trim(),
    };

    const created = await submitReview(payload);
    if (created && created.id) {
      setReviews([created, ...reviews]);
      setComment('');
      setSubmitSuccess(true);
      setTimeout(() => {
        setSubmitSuccess(false);
        setIsFormOpen(false);
      }, 3000);
    }
    setSubmitting(false);
  };

  const ratingDescriptions: Record<number, string> = {
    1: '1 Star — Poor Performance',
    2: '2 Stars — Below Expectations',
    3: '3 Stars — Average Quality',
    4: '4 Stars — Very Good & Reliable',
    5: '5 Stars — Exceptional Masterpiece',
  };

  return (
    <div className="min-h-screen bg-[#F7F4EE] pt-32 pb-24 px-4 sm:px-6">
      <div className="max-w-6xl mx-auto space-y-16">
        
        {/* Back Link */}
        <Link
          href="/explore"
          className="inline-flex items-center gap-2 text-sm font-medium text-[#6E6E73] hover:text-[#0071E3] transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Hardware Archive</span>
        </Link>

        {/* ================= 1. PRIMARY PRODUCT SHOWCASE ================= */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 sm:gap-8 lg:gap-12 items-start">
          
          {/* Product Visual Stage */}
          <div className="lg:col-span-7 rounded-3xl p-4 sm:p-8 md:p-12 lg:p-14 bg-[#E8EBF0] dark:bg-[#141824] border border-black/[0.06] dark:border-white/10 shadow-[0_4px_30px_rgba(0,0,0,0.04)] flex items-center justify-center relative overflow-hidden group transition-colors">
            {/* Floating Wishlist Heart */}
            <button
              type="button"
              onClick={() => toggleWishlist(product)}
              className={`absolute top-4 right-4 z-20 p-3 rounded-full transition-all shadow-md active:scale-90 ${
                isInWishlist(product.id)
                  ? 'bg-rose-500 text-white shadow-rose-500/30'
                  : 'bg-white/80 dark:bg-black/60 backdrop-blur-sm text-slate-600 hover:text-rose-500 hover:bg-white'
              }`}
              title={isInWishlist(product.id) ? 'Remove from Wishlist' : 'Add to Wishlist'}
              aria-label="Wishlist"
            >
              <Heart className={`w-5 h-5 ${isInWishlist(product.id) ? 'fill-current text-white' : ''}`} />
            </button>

            {/* Active Angle & Finish Badge */}
            <div className="absolute top-4 left-4 z-20 flex items-center gap-1.5 px-3 py-1 rounded-full bg-white/80 dark:bg-black/60 backdrop-blur-md border border-black/10 dark:border-white/10 shadow-xs text-[11px] font-semibold text-[#1D1D1F] dark:text-white">
              <span className="w-2 h-2 rounded-full bg-[#0071E3] animate-pulse" />
              <span>
                {activeImageIndex === 0 ? 'Studio Front View' : activeImageIndex === 1 ? 'Perspective 3D Angle' : '2.0x Macro Detail Profile'}
              </span>
            </div>

            <div className="relative w-full h-64 sm:h-80 md:h-[400px] lg:h-[440px] flex items-center justify-center overflow-hidden">
              <Image
                src={activeImageSrc}
                alt={`${product.name} - ${selectedColor}`}
                fill
                priority
                style={{ filter: activeFilter }}
                className={`object-contain transform transition-all duration-700 ease-out drop-shadow-2xl ${
                  activeImageIndex === 1
                    ? 'scale-110 -rotate-6 translate-x-3 translate-y-1'
                    : activeImageIndex === 2
                    ? 'scale-[1.65] translate-x-8 -translate-y-6'
                    : 'scale-100 rotate-0 translate-x-0 translate-y-0 group-hover:scale-105'
                }`}
              />
            </div>

            {/* Multi-angle Preview Bar */}
            <div className="absolute bottom-4 left-1/2 -translate-x-1/2 z-20 flex items-center gap-2 px-3 py-1.5 rounded-full bg-white/85 dark:bg-black/70 backdrop-blur-md border border-black/10 dark:border-white/10 shadow-md">
              {[
                { id: 0, label: 'Studio Front' },
                { id: 1, label: 'Perspective' },
                { id: 2, label: 'Detail Profile' },
              ].map((angle) => (
                <button
                  key={angle.id}
                  type="button"
                  onClick={() => setActiveImageIndex(angle.id)}
                  className={`px-3 py-1 rounded-full text-[11px] font-semibold transition-all ${
                    activeImageIndex === angle.id
                      ? 'bg-[#0071E3] text-white shadow-sm scale-105'
                      : 'text-[#86868B] hover:text-[#1D1D1F] dark:hover:text-white'
                  }`}
                >
                  {angle.label}
                </button>
              ))}
            </div>
          </div>

          {/* Product Details & Actions */}
          <div className="lg:col-span-5 space-y-6 text-left">
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-mono tracking-widest text-[#0071E3] uppercase font-bold">
                  {product.category}
                </span>
                <span className="px-3 py-1 rounded-full text-xs font-semibold tracking-wide bg-emerald-50 text-emerald-800 border border-emerald-200">
                  {product.inStock ? 'In Stock — Ready to Dispatch' : 'Backorder'}
                </span>
              </div>
              <h1 className="text-fluid-title font-semibold text-[#1D1D1F] tracking-tight">
                {product.name}
              </h1>
              <p className="text-sm sm:text-base text-[#6E6E73] mt-1">{product.tagline}</p>
            </div>

            {/* Rating Summary Link */}
            <div className="flex items-center gap-2 text-sm text-amber-500">
              <div className="flex gap-1">
                {[1, 2, 3, 4, 5].map((i) => (
                  <Star key={i} className="w-4 h-4 fill-amber-500" />
                ))}
              </div>
              <span className="font-bold text-[#1D1D1F] ml-1">{product.rating}</span>
              <a
                href="#reviews-section"
                className="text-[#0071E3] text-sm hover:underline ml-1"
              >
                ({reviews.length} verified reviews)
              </a>
            </div>

            {/* Pricing Box & 0% EMI Banner */}
            <div className="p-5 rounded-2xl bg-white border border-black/[0.06] shadow-sm space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-mono uppercase tracking-wider text-[#86868B] block">
                  {activeEmiPlan ? 'Total Payable (With Selected EMI)' : 'Official Guaranteed Price'}
                </span>
                <span className="px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
                  NBR VAT Included
                </span>
              </div>

              <div className="flex items-baseline gap-3">
                <span className="text-3xl sm:text-4xl font-extrabold text-[#1D1D1F] font-mono flex items-baseline">
                  <span className="text-xl sm:text-2xl font-semibold text-gray-500 mr-2">৳</span>
                  <span>{currentPrice.toLocaleString()}</span>
                </span>
                <span className="text-sm font-mono text-[#6E6E73]">
                  (~${Math.round(currentPrice / 134)} USD)
                </span>
              </div>

              {/* Active EMI Plan Callout or Teaser */}
              {activeEmiPlan ? (
                <div className="p-3 rounded-xl bg-[#0071E3]/5 border border-[#0071E3]/20 space-y-1.5 text-xs text-left">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-[#0071E3] flex items-center gap-1.5">
                      <CreditCard className="w-4 h-4" />
                      <span>{activeEmiPlan.label} Active</span>
                    </span>
                    <button
                      type="button"
                      onClick={() => setSelectedEmiMonths(null)}
                      className="text-[11px] text-red-500 hover:underline font-semibold"
                    >
                      Remove EMI
                    </button>
                  </div>
                  <div className="flex items-center justify-between text-slate-700">
                    <span>Monthly Installment:</span>
                    <span className="font-mono font-bold text-[#1D1D1F] text-sm">
                      ৳{Math.round(currentPrice / activeEmiPlan.months).toLocaleString()}/month
                    </span>
                  </div>
                  <div className="text-[11px] text-gray-500 pt-1 border-t border-[#0071E3]/10 flex items-center justify-between">
                    <span>Base ৳{baseHardwarePrice.toLocaleString()} + {activeEmiPlan.markupPct}% Bank Markup (৳{emiSurcharge.toLocaleString()})</span>
                    <button
                      type="button"
                      onClick={() => setIsEmiModalOpen(true)}
                      className="text-[#0071E3] hover:underline font-semibold"
                    >
                      Change Plan &rarr;
                    </button>
                  </div>
                </div>
              ) : (
                baseHardwarePrice >= 20000 && (
                  <div className="pt-2 border-t border-black/[0.06] flex items-center justify-between text-xs">
                    <div className="flex items-center gap-1.5 text-slate-700">
                      <CreditCard className="w-3.5 h-3.5 text-[#0071E3]" />
                      <span>Flexible EMI from <strong>৳{Math.round(baseHardwarePrice / 12).toLocaleString()}</strong>/mo (3–24 Mos)</span>
                    </div>
                    <button
                      type="button"
                      onClick={() => setIsEmiModalOpen(true)}
                      className="text-[#0071E3] hover:underline font-semibold flex items-center gap-0.5"
                    >
                      <span>Choose Plan</span>
                      <ChevronRight className="w-3 h-3" />
                    </button>
                  </div>
                )
              )}
            </div>

            {/* Variant Selectors (Color & Storage) */}
            <div className="p-5 rounded-2xl bg-white border border-black/[0.06] shadow-sm space-y-4">
              {/* Color Swatch Selector */}
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-semibold text-[#1D1D1F]">
                    Color Finish: <span className="text-[#0071E3] font-bold">{selectedColor}</span>
                  </span>
                </div>
                <div className="flex items-center gap-2.5">
                  {availableColors.map((c) => (
                    <button
                      key={c.name}
                      type="button"
                      onClick={() => setSelectedColor(c.name)}
                      className={`group relative p-1 rounded-full transition-all ${
                        selectedColor === c.name ? 'ring-2 ring-[#0071E3] scale-110' : 'hover:scale-105'
                      }`}
                      title={c.name}
                    >
                      <span
                        className="w-6 h-6 rounded-full block border border-black/10 shadow-xs"
                        style={{ backgroundColor: c.hex }}
                      />
                    </button>
                  ))}
                </div>
              </div>

              {/* Storage Capacity Selector */}
              {availableStorage && (
                <div className="pt-3 border-t border-black/[0.06]">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs font-semibold text-[#1D1D1F]">
                      Storage Capacity: <span className="text-[#0071E3] font-bold">{selectedStorage}</span>
                    </span>
                  </div>
                  <div className="grid grid-cols-4 gap-2">
                    {availableStorage.map((st) => (
                      <button
                        key={st.label}
                        type="button"
                        onClick={() => setSelectedStorage(st.label)}
                        className={`py-2 px-1 rounded-xl border text-center transition-all ${
                          selectedStorage === st.label
                            ? 'border-[#0071E3] bg-[#0071E3]/5 text-[#0071E3] font-bold shadow-xs'
                            : 'border-black/10 text-slate-700 hover:border-black/30'
                        }`}
                      >
                        <div className="text-xs">{st.label}</div>
                        {st.markup !== 0 && (
                          <div className="text-[10px] text-gray-500 font-mono">
                            {st.markup > 0 ? `+৳${(st.markup / 1000).toFixed(0)}k` : `-৳${(Math.abs(st.markup) / 1000).toFixed(0)}k`}
                          </div>
                        )}
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Description */}
            <p className="text-base text-[#424245] font-normal leading-relaxed">
              {product.description}
            </p>

            {/* Key Specs Pills */}
            <div className="space-y-2.5">
              <span className="text-xs font-mono uppercase tracking-widest text-[#1D1D1F] font-bold">
                Technical Specifications
              </span>
              <div className="grid grid-cols-1 gap-2 pt-1">
                {product.specs.map((spec, i) => (
                  <div
                    key={i}
                    className="flex items-center gap-3 p-3 rounded-xl bg-white border border-black/[0.05] text-sm text-[#1D1D1F] font-medium"
                  >
                    <CheckCircle2 className="w-4 h-4 text-[#0071E3] flex-shrink-0" />
                    <span>{spec}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Quantity Stepper & Buy Buttons */}
            <div className="space-y-3 pt-4 border-t border-black/[0.06]">
              <div className="flex items-center gap-3">
                <div className="flex items-center border border-black/15 rounded-full px-4 py-2 bg-white">
                  <button
                    onClick={() => setQuantity(Math.max(1, quantity - 1))}
                    className="w-6 h-6 flex items-center justify-center text-slate-500 hover:text-black font-bold text-base"
                  >
                    -
                  </button>
                  <span className="w-8 text-center text-sm font-mono text-[#1D1D1F] font-bold">
                    {quantity}
                  </span>
                  <button
                    onClick={() => setQuantity(quantity + 1)}
                    className="w-6 h-6 flex items-center justify-center text-slate-500 hover:text-black font-bold text-base"
                  >
                    +
                  </button>
                </div>

                <button
                  onClick={handleAddToCart}
                  className="flex-1 py-3.5 rounded-full border border-black/15 hover:bg-black/5 text-[#1D1D1F] font-semibold text-sm tracking-wider uppercase transition-all flex items-center justify-center gap-2 shadow-sm"
                >
                  <ShoppingBag className="w-4 h-4" />
                  <span>{added ? 'Added to Bag' : 'Add to Bag'}</span>
                </button>

                {/* Wishlist Button */}
                <button
                  type="button"
                  onClick={() => toggleWishlist(product)}
                  className={`p-3.5 rounded-full border transition-all flex items-center justify-center shadow-xs active:scale-95 ${
                    isInWishlist(product.id)
                      ? 'bg-rose-500 border-rose-500 text-white shadow-rose-500/25'
                      : 'border-black/15 bg-white hover:bg-rose-50 text-slate-600 hover:text-rose-500 hover:border-rose-300'
                  }`}
                  title={isInWishlist(product.id) ? 'Remove from Wishlist' : 'Add to Wishlist'}
                  aria-label="Toggle Wishlist"
                >
                  <Heart className={`w-4 h-4 ${isInWishlist(product.id) ? 'fill-current' : ''}`} />
                </button>
              </div>

              <button
                onClick={handleBuyNow}
                className="w-full py-4 rounded-full bg-[#0071E3] hover:bg-[#0077ED] text-white font-medium text-base tracking-wide transition-all shadow-md hover:shadow-lg"
              >
                Buy Now with 1-Click
              </button>
            </div>

            {/* Trust Guarantees - Responsive compact cards */}
            <div className="grid grid-cols-3 gap-1.5 sm:gap-2 pt-4 border-t border-black/[0.06] text-center text-[10px] sm:text-xs text-[#555558]">
              <div className="p-2 sm:p-3 rounded-xl sm:rounded-2xl bg-white border border-black/[0.05]">
                <ShieldCheck className="w-4 h-4 sm:w-5 sm:h-5 text-[#0071E3] mx-auto mb-1 sm:mb-1.5" />
                <span className="font-medium leading-tight block">1-Year Warranty</span>
              </div>
              <div className="p-2 sm:p-3 rounded-xl sm:rounded-2xl bg-white border border-black/[0.05]">
                <Truck className="w-4 h-4 sm:w-5 sm:h-5 text-[#0071E3] mx-auto mb-1 sm:mb-1.5" />
                <span className="font-medium leading-tight block">Express Dispatch</span>
              </div>
              <div className="p-2 sm:p-3 rounded-xl sm:rounded-2xl bg-white border border-black/[0.05]">
                <RefreshCw className="w-4 h-4 sm:w-5 sm:h-5 text-[#0071E3] mx-auto mb-1 sm:mb-1.5" />
                <span className="font-medium leading-tight block">7-Day Return</span>
              </div>
            </div>
          </div>
        </div>

        {/* ================= 2. MEMBER SIGN-IN & APP PORTAL ================= */}
        <div className="rounded-3xl p-6 sm:p-8 bg-white border border-black/[0.06] shadow-sm flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="flex items-center gap-4 text-left">
            <div className="w-12 h-12 rounded-2xl bg-[#0B132B] flex items-center justify-center text-white flex-shrink-0 shadow-sm">
              <User className="w-6 h-6 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-xs font-mono uppercase tracking-widest text-[#0071E3] font-bold">
                  NEXORA Ecosystem Profile
                </span>
                {user && (
                  <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase bg-emerald-100 text-emerald-800">
                    Active Member
                  </span>
                )}
              </div>
              <h3 className="text-xl font-semibold text-[#1D1D1F] mt-0.5">
                {user ? `Welcome back, ${user.name}` : 'Sign in to Your NEXORA Account'}
              </h3>
              <p className="text-sm text-[#6E6E73] mt-1 max-w-xl">
                {user
                  ? `Signed in as ${user.email}. Your warranty and hardware orders are synced.`
                  : 'Sign in to register hardware warranty, track express deliveries, and publish verified customer reviews.'}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            {user ? (
              <button
                onClick={logout}
                className="px-5 py-2.5 rounded-full border border-red-200 text-red-600 hover:bg-red-50 text-xs font-semibold tracking-wide transition-colors flex items-center gap-1.5"
              >
                <LogOut className="w-3.5 h-3.5" />
                <span>Sign Out</span>
              </button>
            ) : (
              <button
                onClick={() => setIsAuthModalOpen(true)}
                className="px-6 py-3 rounded-full bg-[#0B132B] hover:bg-[#152347] text-white text-xs font-semibold tracking-wide transition-all shadow-sm flex items-center gap-2"
              >
                <LogIn className="w-4 h-4" />
                <span>Sign In / Create Account</span>
              </button>
            )}
          </div>
        </div>

        {/* ================= 3. REVIEWS & FEEDBACK SYSTEM ================= */}
        <section id="reviews-section" className="space-y-8 scroll-mt-36">
          <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4 pb-6 border-b border-black/[0.08]">
            <div>
              <span className="text-xs font-mono uppercase tracking-widest text-[#0071E3] font-bold block mb-1">
                Verified Customer Feedback
              </span>
              <h2 className="text-3xl sm:text-4xl font-semibold text-[#1D1D1F] tracking-tight">
                Ratings &amp; Reviews for {product.name}
              </h2>
              <p className="text-sm text-[#6E6E73] mt-1">
                Real feedback from verified purchasers across Bangladesh and international clients.
              </p>
            </div>

            <button
              onClick={() => setIsFormOpen(!isFormOpen)}
              className="inline-flex items-center gap-2 px-6 py-3 rounded-full bg-[#0071E3] hover:bg-[#0077ED] text-white text-sm font-semibold tracking-wide transition-all shadow-sm self-start sm:self-auto"
            >
              <MessageSquarePlus className="w-4 h-4" />
              <span>{isFormOpen ? 'Cancel Feedback' : 'Send Feedback / Rate'}</span>
            </button>
          </div>

          {/* Interactive Feedback & Rating Form Card */}
          {isFormOpen && (
            <div className="rounded-3xl p-8 bg-white border border-[#0071E3]/30 shadow-lg text-left transition-all animate-fade-in space-y-6">
              <div className="flex items-center gap-2 text-xs font-mono uppercase tracking-widest text-[#0071E3] font-bold">
                <Sparkles className="w-4 h-4 text-[#0071E3]" />
                <span>Submit Your Feedback &amp; Device Rating</span>
              </div>

              {submitSuccess ? (
                <div className="p-6 rounded-2xl bg-emerald-50 border border-emerald-200 text-center space-y-2">
                  <CheckCircle2 className="w-8 h-8 text-emerald-600 mx-auto" />
                  <h4 className="text-lg font-bold text-emerald-900">Thank you for your feedback!</h4>
                  <p className="text-sm text-emerald-700">
                    Your rating and review for {product.name} have been registered and published live.
                  </p>
                </div>
              ) : (
                <form onSubmit={handleReviewSubmit} className="space-y-6">
                  {/* Star Rating Picker */}
                  <div>
                    <label className="block text-sm font-semibold text-[#1D1D1F] mb-2">
                      Your Rating (Click to Select)
                    </label>
                    <div className="flex items-center gap-2">
                      <div className="flex gap-1.5">
                        {[1, 2, 3, 4, 5].map((star) => (
                          <button
                            key={star}
                            type="button"
                            onMouseEnter={() => setHoverRating(star)}
                            onMouseLeave={() => setHoverRating(0)}
                            onClick={() => setRating(star)}
                            className="p-1 focus:outline-none transition-transform hover:scale-125"
                          >
                            <Star
                              className={`w-7 h-7 transition-colors ${
                                (hoverRating || rating) >= star
                                  ? 'fill-amber-400 text-amber-400'
                                  : 'text-gray-300'
                              }`}
                            />
                          </button>
                        ))}
                      </div>
                      <span className="text-sm font-semibold text-[#1D1D1F] ml-3">
                        {ratingDescriptions[hoverRating || rating]}
                      </span>
                    </div>
                  </div>

                  {/* Name Input */}
                  <div>
                    <label className="block text-sm font-semibold text-[#1D1D1F] mb-1.5">
                      Your Name
                    </label>
                    <input
                      type="text"
                      required
                      value={feedbackName}
                      onChange={(e) => setFeedbackName(e.target.value)}
                      placeholder="e.g. Tanvir Ahmed"
                      className="w-full max-w-md px-4 py-3 rounded-xl bg-[#F5F5F7] border border-black/10 focus:border-[#0071E3] focus:bg-white text-sm text-[#1D1D1F] focus:outline-none transition-all"
                    />
                  </div>

                  {/* Feedback Text Area */}
                  <div>
                    <label className="block text-sm font-semibold text-[#1D1D1F] mb-1.5">
                      Feedback &amp; Experience Details
                    </label>
                    <textarea
                      required
                      rows={4}
                      value={comment}
                      onChange={(e) => setComment(e.target.value)}
                      placeholder="Describe the build quality, performance, battery endurance, delivery experience, or suggestions..."
                      className="w-full px-4 py-3 rounded-xl bg-[#F5F5F7] border border-black/10 focus:border-[#0071E3] focus:bg-white text-sm text-[#1D1D1F] focus:outline-none transition-all"
                    />
                  </div>

                  {/* Submit Button */}
                  <div className="flex items-center gap-3">
                    <button
                      type="submit"
                      disabled={submitting}
                      className="px-8 py-3.5 rounded-full bg-[#1D1D1F] hover:bg-[#333336] text-white text-sm font-semibold tracking-wide transition-all shadow-md flex items-center gap-2"
                    >
                      <Send className="w-4 h-4" />
                      <span>{submitting ? 'Submitting...' : 'Post Verified Feedback'}</span>
                    </button>
                    <button
                      type="button"
                      onClick={() => setIsFormOpen(false)}
                      className="px-5 py-3.5 rounded-full text-sm font-medium text-[#6E6E73] hover:text-[#1D1D1F]"
                    >
                      Cancel
                    </button>
                  </div>
                </form>
              )}
            </div>
          )}

          {/* Reviews List */}
          {loadingReviews ? (
            <div className="py-12 text-center text-sm font-mono text-[#86868B]">
              Loading verified feedback...
            </div>
          ) : reviews.length === 0 ? (
            <div className="p-12 text-center rounded-3xl bg-white border border-black/[0.06] space-y-2">
              <Star className="w-8 h-8 text-amber-400 mx-auto" />
              <h3 className="text-lg font-semibold text-[#1D1D1F]">Be the First to Rate this Gadget</h3>
              <p className="text-sm text-[#6E6E73]">
                Share your impressions with the NEXORA community.
              </p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {reviews.map((rev) => (
                <div
                  key={rev.id}
                  className="rounded-3xl p-6 bg-white border border-black/[0.06] shadow-[0_2px_16px_rgba(0,0,0,0.03)] flex flex-col justify-between text-left space-y-4"
                >
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <div className="flex gap-1 text-amber-500">
                        {Array.from({ length: rev.rating }).map((_, i) => (
                          <Star key={i} className="w-4 h-4 fill-amber-500" />
                        ))}
                      </div>
                      <span className="text-xs font-mono text-[#86868B]">{rev.date}</span>
                    </div>
                    <p className="text-base text-[#1D1D1F] font-normal leading-relaxed">
                      &ldquo;{rev.comment}&rdquo;
                    </p>
                  </div>

                  <div className="pt-4 border-t border-black/[0.06] flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <CheckCircle2 className="w-4 h-4 text-emerald-600 flex-shrink-0" />
                      <span className="text-sm font-semibold text-[#1D1D1F]">{rev.author}</span>
                    </div>
                    <span className="text-xs font-mono text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-full border border-emerald-200">
                      Verified Buyer
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>

      {/* 0% EMI Bank Installment Modal */}
      {isEmiModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-fade-in">
          <div className="bg-white rounded-3xl max-w-lg w-full p-6 sm:p-8 shadow-2xl border border-black/10 relative text-left">
            <button
              onClick={() => setIsEmiModalOpen(false)}
              className="absolute top-5 right-5 p-2 rounded-full hover:bg-gray-100 text-gray-500 hover:text-black transition-colors"
            >
              <X className="w-5 h-5" />
            </button>

            <div className="flex items-center gap-2.5 text-[#0071E3] mb-1">
              <CreditCard className="w-5 h-5" />
              <span className="text-xs font-mono uppercase tracking-widest font-bold">Official Bank Financing</span>
            </div>

            <h3 className="text-xl font-bold text-[#1D1D1F]">
              Select Bank EMI Financing Plan
            </h3>
            <p className="text-xs text-slate-500 mt-1">
              Select your preferred tenure. Longer installment tenures apply standard bank financing charges, while shorter tenures offer maximum savings.
            </p>

            <div className="mt-5 space-y-2.5">
              {EMI_PLANS.map((plan) => {
                const planMarkup = Math.round((baseHardwarePrice * plan.markupPct) / 100);
                const planTotal = baseHardwarePrice + planMarkup;
                const planMonthly = Math.round(planTotal / plan.months);
                const isSelected = modalSelectedEmi === plan.months;

                return (
                  <button
                    key={plan.months}
                    type="button"
                    onClick={() => setModalSelectedEmi(plan.months)}
                    className={`w-full p-4 rounded-2xl border flex items-center justify-between text-left transition-all ${
                      isSelected
                        ? 'border-[#0071E3] bg-[#0071E3]/5 ring-2 ring-[#0071E3]/30 shadow-xs'
                        : 'border-black/10 hover:border-black/25 bg-white'
                    }`}
                  >
                    <div className="flex items-center gap-3">
                      <div className={`w-5 h-5 rounded-full flex items-center justify-center border transition-colors ${
                        isSelected ? 'border-[#0071E3] bg-[#0071E3] text-white' : 'border-gray-300 bg-white'
                      }`}>
                        {isSelected && <div className="w-2 h-2 rounded-full bg-white" />}
                      </div>
                      <div>
                        <div className="font-bold text-xs text-[#1D1D1F] flex items-center gap-2">
                          <span>{plan.label}</span>
                          <span className={`px-2 py-0.5 rounded-full text-[10px] font-semibold ${
                            plan.markupPct === 0 
                              ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' 
                              : 'bg-amber-50 text-amber-800 border border-amber-200'
                          }`}>
                            {plan.markupPct === 0 ? '0% Extra' : `+${plan.markupPct}% Bank Markup (+৳${planMarkup.toLocaleString()})`}
                          </span>
                        </div>
                        <div className="text-[11px] text-gray-500 mt-0.5">
                          Total payable: <strong className="text-[#1D1D1F]">৳{planTotal.toLocaleString()}</strong> across {plan.months} monthly installments
                        </div>
                      </div>
                    </div>

                    <div className="text-right flex-shrink-0 ml-3">
                      <div className="text-sm sm:text-base font-mono font-extrabold text-[#0071E3]">
                        ৳{planMonthly.toLocaleString()}<span className="text-[11px] text-gray-500 font-normal">/mo</span>
                      </div>
                    </div>
                  </button>
                );
              })}
            </div>

            <div className="mt-6 pt-4 border-t border-black/10 flex flex-col sm:flex-row items-center justify-between gap-3">
              <button
                type="button"
                onClick={() => {
                  setSelectedEmiMonths(null);
                  setIsEmiModalOpen(false);
                }}
                className="w-full sm:w-auto px-4 py-2.5 rounded-full text-xs font-semibold text-gray-600 hover:text-black hover:bg-gray-100 transition-colors"
              >
                Standard One-Time Payment (0% Extra)
              </button>

              <button
                type="button"
                onClick={() => {
                  setSelectedEmiMonths(modalSelectedEmi);
                  setIsEmiModalOpen(false);
                }}
                className="w-full sm:w-auto px-6 py-2.5 rounded-full bg-[#0071E3] hover:bg-[#0077ED] text-white text-xs font-semibold transition-all shadow-md active:scale-95 flex items-center justify-center gap-1.5"
              >
                <span>Apply {modalSelectedEmi} Months EMI Plan</span>
              </button>
            </div>
          </div>
        </div>
      )}

      </div>
    </div>
  );
};

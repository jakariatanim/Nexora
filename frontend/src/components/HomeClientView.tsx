'use client';

import React, { useState, useRef, useEffect } from 'react';
import Image from 'next/image';
import { motion } from 'framer-motion';
import { HeroSection } from './HeroSection';
import { FounderSection } from './FounderSection';
import { ReviewsSection } from './ReviewsSection';
import { AppInstallBanner } from './AppInstallBanner';
import { Product, Review } from '../lib/types';
import { useCart } from '../lib/cartContext';
import Link from 'next/link';
import { ChevronLeft, ChevronRight, Grid, MoveHorizontal, Sparkles, Scale, Heart } from 'lucide-react';

interface HomeClientViewProps {
  products: Product[];
  reviews: Review[];
}

const TOP_10_BRANDS = [
  { name: 'Apple', logo: '/brands/apple.svg', isWide: false },
  { name: 'Samsung', logo: '/brands/samsung.svg', isWide: true },
  { name: 'Xiaomi', logo: '/brands/xiaomi.svg', isWide: false },
  { name: 'Oppo', logo: '/brands/oppo.svg', isWide: true },
  { name: 'Vivo', logo: '/brands/vivo.svg', isWide: true },
  { name: 'OnePlus', logo: '/brands/oneplus.svg', isWide: false },
  { name: 'Google', logo: '/brands/google.svg', isWide: false },
  { name: 'Realme', logo: '/brands/realme.svg', isWide: true },
  { name: 'Anker', logo: '/brands/anker.svg', isWide: true },
  { name: 'Sony', logo: '/brands/sony.svg', isWide: true },
];

const FEATURED_10_IDS = [
  'macbook-pro-16-m3-max',
  'ipad-pro-m4',
  'airpods-pro-2',
  'samsung-galaxy-buds3-pro',
  'airpods-max',
  'sony-wh1000xm5',
  'apple-watch-ultra-2',
  'samsung-galaxy-watch-ultra',
  'anker-maggo-qi2-cube',
  'apple-magsafe-charger-25w'
];

const SHORT_TITLES: Record<string, string> = {
  'macbook-pro-16-m3-max': 'MacBook Pro 16"',
  'ipad-pro-m4': 'iPad Pro M4',
  'airpods-pro-2': 'AirPods Pro 2',
  'samsung-galaxy-buds3-pro': 'Galaxy Buds3 Pro',
  'airpods-max': 'AirPods Max',
  'sony-wh1000xm5': 'Sony WH-1000XM5',
  'apple-watch-ultra-2': 'Apple Watch Ultra 2',
  'samsung-galaxy-watch-ultra': 'Galaxy Watch Ultra',
  'anker-maggo-qi2-cube': 'Anker MagGo Cube',
  'apple-magsafe-charger-25w': 'MagSafe Charger 25W',
};

// 3D Tilt & Glass-Glare Animated Featured Card (Supports both Slider and 2-Column Grid)
const FeaturedCard: React.FC<{
  product: Product;
  index: number;
  addedId: string | null;
  onAddToCart: (p: Product) => void;
  onBuy: (p: Product) => void;
  cleanTitle: string;
  isSlider?: boolean;
}> = ({ product, index, addedId, onAddToCart, onBuy, cleanTitle, isSlider }) => {
  const { toggleWishlist, isInWishlist } = useCart();
  const cardRef = useRef<HTMLDivElement>(null);
  const [rotateX, setRotateX] = useState(0);
  const [rotateY, setRotateY] = useState(0);
  const [glare, setGlare] = useState({ x: 50, y: 50, opacity: 0 });

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!cardRef.current) return;
    const rect = cardRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const centerX = rect.width / 2;
    const centerY = rect.height / 2;

    const rotX = -((y - centerY) / centerY) * 5.5;
    const rotY = ((x - centerX) / centerX) * 5.5;

    setRotateX(rotX);
    setRotateY(rotY);
    setGlare({
      x: (x / rect.width) * 100,
      y: (y / rect.height) * 100,
      opacity: 0.16,
    });
  };

  const handleMouseLeave = () => {
    setRotateX(0);
    setRotateY(0);
    setGlare(prev => ({ ...prev, opacity: 0 }));
  };

  return (
    <motion.div
      ref={cardRef}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      initial={{ opacity: 0, y: 25 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-20px' }}
      transition={{
        duration: 0.45,
        delay: (index % 2) * 0.08,
        ease: [0.16, 1, 0.3, 1],
      }}
      animate={{
        rotateX,
        rotateY,
        transformPerspective: 1000,
      }}
      style={{ transformStyle: 'preserve-3d' }}
      className={`rounded-2xl sm:rounded-3xl border border-black/[0.08] dark:border-white/10 shadow-[0_4px_20px_rgba(0,0,0,0.03)] hover:shadow-[0_20px_40px_rgba(0,0,0,0.10)] bg-white dark:bg-[#141824] p-3 sm:p-5 md:p-6 flex flex-col items-center justify-between text-center relative overflow-hidden group transition-shadow duration-300 ${
        isSlider
          ? 'w-[82vw] sm:w-[380px] md:w-[calc(50%-12px)] max-w-[480px] flex-shrink-0 snap-start'
          : 'w-full'
      }`}
    >
      {/* Interactive Cursor-Tracked Light Glare */}
      <div
        className="pointer-events-none absolute inset-0 z-20 rounded-2xl sm:rounded-3xl transition-opacity duration-300"
        style={{
          background: `radial-gradient(circle at ${glare.x}% ${glare.y}%, rgba(255,255,255,0.35) 0%, transparent 60%)`,
          opacity: glare.opacity,
        }}
      />

      {/* Floating Wishlist Heart Button */}
      <button
        type="button"
        onClick={(e) => {
          e.preventDefault();
          e.stopPropagation();
          toggleWishlist(product);
        }}
        className={`absolute top-2.5 right-2.5 sm:top-3.5 sm:right-3.5 z-30 p-1.5 sm:p-2 rounded-full transition-all shadow-xs active:scale-90 ${
          isInWishlist(product.id)
            ? 'bg-rose-500 text-white shadow-rose-500/30'
            : 'bg-black/5 hover:bg-black/10 dark:bg-white/10 dark:hover:bg-white/20 text-slate-500 hover:text-rose-500'
        }`}
        title={isInWishlist(product.id) ? 'Remove from Wishlist' : 'Save to Wishlist'}
        aria-label="Save to Wishlist"
      >
        <Heart className={`w-3.5 h-3.5 sm:w-4 sm:h-4 ${isInWishlist(product.id) ? 'fill-current text-white' : ''}`} />
      </button>

      {/* Top: Brand kicker, Clean Short Title, Tagline */}
      <div className="space-y-1 z-10 flex flex-col items-center w-full">
        <span className="text-[9px] sm:text-[11px] font-bold tracking-widest uppercase text-[#86868B] dark:text-white/60">
          {product.brand || 'Flagship'}
        </span>

        <Link href={`/product/${product.id}`} className="group/title transition-colors">
          <h3 className="text-xs sm:text-lg md:text-xl font-bold tracking-tight text-[#1D1D1F] dark:text-white group-hover/title:text-[#0071E3] dark:group-hover/title:text-[#38BDF8] transition-colors line-clamp-1">
            {cleanTitle}
          </h3>
        </Link>

        <p className="hidden sm:block text-xs sm:text-sm text-[#6E6E73] dark:text-[#A1A1A6] max-w-sm line-clamp-1">
          {product.tagline || product.description}
        </p>
      </div>

      {/* Center: Pedestal Frame Product Image (Compact 16:9 with 3D Pop) */}
      <Link
        href={`/product/${product.id}`}
        className="relative my-2 sm:my-3 h-28 sm:h-40 md:h-44 w-full flex items-center justify-center rounded-xl sm:rounded-2xl bg-[#E8EBF0] dark:bg-[#181D2B] border border-black/[0.06] dark:border-white/10 p-2 sm:p-3 cursor-pointer group-hover:scale-105 transition-all duration-500"
      >
        <div className="relative w-full h-full">
          <Image
            src={product.image}
            alt={product.name}
            fill
            className="object-contain drop-shadow-[0_10px_20px_rgba(0,0,0,0.12)]"
            sizes="(max-width: 768px) 240px, 440px"
          />
        </div>
      </Link>

      {/* Price tag with refined Taka typography */}
      <div className="mb-2 z-10">
        <span className="text-xs sm:text-base font-bold text-[#1D1D1F] dark:text-white font-mono">
          <span className="text-[10px] sm:text-xs font-normal text-gray-500 dark:text-gray-400 mr-1">৳</span>
          <span>{product.priceBDT.toLocaleString()}</span>
        </span>
      </div>

      {/* Bottom: Dual Buttons - First "Add to Cart" (Silent), Then "Buy" (Opens Cart) */}
      <div className="flex flex-col sm:flex-row items-center justify-center gap-1.5 sm:gap-2.5 pt-1 z-10 w-full max-w-xs">
        <button
          onClick={() => onAddToCart(product)}
          className="w-full sm:flex-1 min-h-[34px] sm:min-h-[38px] py-1.5 sm:py-2 px-2 sm:px-3 rounded-full border border-black/15 dark:border-white/20 bg-black/[0.03] hover:bg-black/[0.07] dark:bg-white/[0.06] dark:hover:bg-white/[0.12] text-[#1D1D1F] dark:text-white text-[10px] sm:text-xs font-semibold tracking-wide transition-all shadow-sm active:scale-95 touch-manipulation"
        >
          {addedId === product.id ? 'Added ✓' : 'Add to Cart'}
        </button>
        <button
          onClick={() => onBuy(product)}
          className="w-full sm:flex-1 min-h-[34px] sm:min-h-[38px] py-1.5 sm:py-2 px-2 sm:px-3 rounded-full bg-[#0071E3] hover:bg-[#0077ED] text-white text-[10px] sm:text-xs font-semibold tracking-wide transition-all shadow-sm active:scale-95 touch-manipulation"
        >
          Buy
        </button>
      </div>
    </motion.div>
  );
};

export const HomeClientView: React.FC<HomeClientViewProps> = ({ products, reviews }) => {
  const { addToCart, setIsCartOpen } = useCart();
  const [addedId, setAddedId] = useState<string | null>(null);
  const [activeProducts, setActiveProducts] = useState<Product[]>(products || []);

  useEffect(() => {
    if (!products || products.length === 0) {
      import('../lib/api').then(({ fetchProducts }) => {
        fetchProducts().then(res => {
          if (res && res.length > 0) setActiveProducts(res);
        });
      });
    } else {
      setActiveProducts(products);
    }
  }, [products]);
  
  // Slider vs Grid view mode
  const [viewMode, setViewMode] = useState<'slider' | 'grid'>('slider');
  const [activeSlideIndex, setActiveSlideIndex] = useState(0);
  const sliderRef = useRef<HTMLDivElement>(null);

  const handleAddToCartSilent = (product: Product) => {
    addToCart(product, 1, false);
    setAddedId(product.id);
    setTimeout(() => {
      setAddedId(prev => (prev === product.id ? null : prev));
    }, 1600);
  };

  const handleBuy = (product: Product) => {
    addToCart(product, 1);
    setIsCartOpen(true);
  };

  let featuredProducts = FEATURED_10_IDS
    .map(id => activeProducts.find(p => p.id === id))
    .filter((p): p is Product => !!p);

  if (featuredProducts.length < 6 && activeProducts.length > 0) {
    featuredProducts = activeProducts.slice(0, 10);
  }

  const getCleanTitle = (product: Product) => {
    if (SHORT_TITLES[product.id]) return SHORT_TITLES[product.id];
    if (product.brand) {
      const regex = new RegExp(`^${product.brand}\\s*`, 'i');
      return product.name.replace(regex, '').trim();
    }
    return product.name;
  };

  // Slider navigation
  const slideLeft = () => {
    if (!sliderRef.current) return;
    const cardWidth = sliderRef.current.clientWidth > 640 ? 400 : 310;
    sliderRef.current.scrollBy({ left: -cardWidth, behavior: 'smooth' });
  };

  const slideRight = () => {
    if (!sliderRef.current) return;
    const cardWidth = sliderRef.current.clientWidth > 640 ? 400 : 310;
    sliderRef.current.scrollBy({ left: cardWidth, behavior: 'smooth' });
  };

  const handleScroll = () => {
    if (!sliderRef.current) return;
    const scrollLeft = sliderRef.current.scrollLeft;
    const cardWidth = sliderRef.current.clientWidth > 640 ? 400 : 310;
    const newIndex = Math.round(scrollLeft / cardWidth);
    setActiveSlideIndex(Math.min(featuredProducts.length - 1, Math.max(0, newIndex)));
  };

  const scrollToSlide = (idx: number) => {
    if (!sliderRef.current) return;
    const cardWidth = sliderRef.current.clientWidth > 640 ? 400 : 310;
    sliderRef.current.scrollTo({ left: idx * cardWidth, behavior: 'smooth' });
  };

  return (
    <div className="space-y-16 sm:space-y-20 pb-12">
      {/* 1. Living Mosaic Hero & Apple Billboards */}
      <HeroSection />

      {/* 2. Official Brand Collaborations Showcase (10 Brands) */}
      <motion.section
        initial={{ opacity: 0, y: 25 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, margin: '-40px' }}
        transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
        className="max-w-6xl mx-auto px-4 sm:px-6"
      >
        <div className="rounded-3xl bg-white dark:bg-[#14141B] border border-black/[0.08] dark:border-white/10 shadow-sm p-6 sm:p-8 space-y-6 text-center">
          <h2 className="text-xl sm:text-2xl md:text-3xl font-bold text-[#1D1D1F] dark:text-white tracking-tight">
            Official Brand Collaborations
          </h2>

          {/* 10 Brand Logos: 5 on Top, 5 on Bottom on Mobile (grid-cols-5) */}
          <div className="grid grid-cols-5 sm:grid-cols-5 lg:grid-cols-10 gap-2 sm:gap-3">
            {TOP_10_BRANDS.map((brand, idx) => (
              <motion.div
                key={brand.name}
                initial={{ opacity: 0, scale: 0.95 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: true }}
                transition={{ duration: 0.4, delay: idx * 0.04 }}
              >
                <Link
                  href={`/explore?brand=${encodeURIComponent(brand.name)}`}
                  className="h-12 sm:h-16 rounded-xl sm:rounded-2xl border border-black/[0.06] dark:border-white/10 hover:border-[#0071E3] dark:hover:border-[#0071E3] bg-[#FBFBFD] dark:bg-white/5 hover:bg-[#0071E3]/5 dark:hover:bg-[#0071E3]/15 transition-all flex items-center justify-center p-1.5 sm:p-3 group shadow-sm hover:scale-105"
                  title={`Explore all ${brand.name} gadgets`}
                >
                  <div className={`relative flex items-center justify-center transition-transform group-hover:scale-105 ${
                    brand.isWide ? 'w-12 sm:w-20 md:w-24 h-5 sm:h-8 md:h-9' : 'w-5 sm:w-8 md:w-9 h-5 sm:h-8 md:h-9'
                  }`}>
                    <Image
                      src={brand.logo}
                      alt={brand.name}
                      fill
                      className={`object-contain ${(brand.name === 'Apple' || brand.name === 'Sony') ? 'dark:invert' : ''}`}
                    />
                  </div>
                </Link>
              </motion.div>
            ))}
          </div>
        </div>
      </motion.section>

      {/* 3. Featured Gadgets - Apple 2-Column Grid (2 Products per row on Mobile & Desktop) */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6">
        <div className="space-y-6 sm:space-y-8">
          
          <div className="text-center max-w-2xl mx-auto space-y-1">
            <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-[#0071E3]/10 text-[#0071E3] dark:text-[#38BDF8] text-[11px] font-semibold">
              <Sparkles className="w-3 h-3" />
              <span>Curated Highlights</span>
            </div>
            <h2 className="text-2xl sm:text-4xl md:text-5xl font-semibold text-[#1D1D1F] dark:text-white tracking-tight">
              Featured Gadgets
            </h2>
          </div>

          {/* 2-Column Side-by-Side Grid (2 Products per row on both Mobile & Desktop) */}
          <div className="grid grid-cols-2 md:grid-cols-2 gap-3 sm:gap-6">
            {featuredProducts.map((product, index) => (
              <FeaturedCard
                key={product.id}
                product={product}
                index={index}
                addedId={addedId}
                onAddToCart={handleAddToCartSilent}
                onBuy={handleBuy}
                cleanTitle={getCleanTitle(product)}
                isSlider={false}
              />
            ))}
          </div>

          {/* Action Links: Compare Flagships Above Explore All Products */}
          <div className="flex flex-col items-center justify-center gap-3 pt-3 sm:pt-4">
            {/* Compare Flagships Side-by-Side Button */}
            <Link
              href="/compare"
              className="inline-flex items-center gap-2 px-6 py-2.5 rounded-full bg-white dark:bg-[#152238] border border-black/10 dark:border-white/10 hover:border-[#0071E3] dark:hover:border-[#38BDF8] text-[#1D1D1F] dark:text-white hover:text-[#0071E3] dark:hover:text-[#38BDF8] font-medium text-xs sm:text-sm tracking-wide transition-all shadow-xs hover:shadow-md group"
            >
              <Scale className="w-4 h-4 text-[#0071E3] dark:text-[#38BDF8] group-hover:rotate-12 transition-transform" />
              <span>Compare Flagships Side-by-Side</span>
              <span className="text-xs group-hover:translate-x-0.5 transition-transform">&rarr;</span>
            </Link>

            {/* Centered Explore All Link */}
            <Link
              href="/explore"
              className="inline-flex items-center justify-center px-8 py-3.5 rounded-full bg-[#1D1D1F] hover:bg-[#0071E3] dark:bg-[#0071E3] dark:hover:bg-[#0077ED] text-white font-medium text-xs sm:text-sm tracking-wide transition-all shadow-sm hover:shadow-lg hover:scale-105 active:scale-95"
            >
              <span>Explore All Products in Stock →</span>
            </Link>
          </div>
        </div>
      </section>

      {/* 4. Customer Verified Reviews */}
      <ReviewsSection initialReviews={reviews} />

      {/* 5. Founder's Vision */}
      <FounderSection />

      {/* 6. Official App Install Banner */}
      <AppInstallBanner />
    </div>
  );
};

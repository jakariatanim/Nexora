'use client';

import React, { useState, useRef } from 'react';
import Image from 'next/image';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { Product } from '../lib/types';
import { useCart } from '../lib/cartContext';
import { Star, Check, Heart } from 'lucide-react';

export const ProductCard: React.FC<{ product: Product }> = ({ product }) => {
  const { addToCart, setIsCartOpen, toggleWishlist, isInWishlist } = useCart();
  const [justAdded, setJustAdded] = useState(false);
  const cardRef = useRef<HTMLDivElement>(null);

  // 3D Tilt & Interactive Dynamic Glare State
  const [rotateX, setRotateX] = useState(0);
  const [rotateY, setRotateY] = useState(0);
  const [glare, setGlare] = useState({ x: 50, y: 50, opacity: 0 });

  const stock = typeof product.stockCount === 'number' ? product.stockCount : (product.inStock ? 25 : 0);
  const isAvailable = product.inStock && stock > 0;

  // Clean title without repeating brand prefix
  const cleanTitle = product.brand 
    ? product.name.replace(new RegExp(`^${product.brand}\\s*`, 'i'), '').trim() || product.name
    : product.name;

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!cardRef.current) return;
    const rect = cardRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const centerX = rect.width / 2;
    const centerY = rect.height / 2;

    // Refined Apple-like 3D tilt: max 6 degrees for smooth luxury feel
    const rotX = -((y - centerY) / centerY) * 6;
    const rotY = ((x - centerX) / centerX) * 6;

    setRotateX(rotX);
    setRotateY(rotY);
    setGlare({
      x: (x / rect.width) * 100,
      y: (y / rect.height) * 100,
      opacity: 0.15,
    });
  };

  const handleMouseLeave = () => {
    setRotateX(0);
    setRotateY(0);
    setGlare((prev) => ({ ...prev, opacity: 0 }));
  };

  const handleSilentAdd = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (!isAvailable) return;
    addToCart(product, 1, false);
    setJustAdded(true);
    setTimeout(() => setJustAdded(false), 2000);
  };

  const handleBuy = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (!isAvailable) return;
    addToCart(product, 1, true);
    setIsCartOpen(true);
  };

  return (
    <motion.div
      ref={cardRef}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      initial={{ opacity: 0, y: 24 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-30px' }}
      animate={{
        rotateX,
        rotateY,
        transformPerspective: 1000,
      }}
      transition={{
        rotateX: { type: 'spring', stiffness: 350, damping: 25, mass: 0.5 },
        rotateY: { type: 'spring', stiffness: 350, damping: 25, mass: 0.5 },
        opacity: { duration: 0.45, ease: [0.16, 1, 0.3, 1] },
        y: { duration: 0.45, ease: [0.16, 1, 0.3, 1] },
      }}
      style={{ transformStyle: 'preserve-3d' }}
      className="@container cq-card group relative rounded-2xl sm:rounded-3xl p-3 sm:p-6 md:p-7 bg-white dark:bg-[#14141B] border border-black/[0.08] dark:border-white/10 shadow-[0_4px_20px_rgba(0,0,0,0.03)] hover:shadow-[0_20px_40px_rgba(0,0,0,0.10)] transition-shadow duration-300 flex flex-col justify-between overflow-hidden"
    >
      {/* Interactive Cursor-Tracked Glass Reflection Glare */}
      <div
        className="pointer-events-none absolute inset-0 z-20 rounded-2xl sm:rounded-3xl transition-opacity duration-300"
        style={{
          background: `radial-gradient(circle at ${glare.x}% ${glare.y}%, rgba(255,255,255,0.35) 0%, transparent 60%)`,
          opacity: glare.opacity,
        }}
      />

      {/* Wishlist Floating Heart Button */}
      <button
        type="button"
        onClick={(e) => {
          e.preventDefault();
          e.stopPropagation();
          toggleWishlist(product);
        }}
        className={`absolute top-4 right-4 z-30 p-2 rounded-full transition-all shadow-sm active:scale-90 ${
          isInWishlist(product.id)
            ? 'bg-rose-500 text-white'
            : 'bg-white/80 dark:bg-black/60 backdrop-blur-sm text-slate-500 hover:text-rose-500 hover:bg-white dark:hover:bg-black/80'
        }`}
        title={isInWishlist(product.id) ? 'Remove from Wishlist' : 'Save to Wishlist'}
        aria-label="Wishlist"
      >
        <Heart className={`w-3.5 h-3.5 ${isInWishlist(product.id) ? 'fill-current text-white' : ''}`} />
      </button>

      {/* 1. TOP: Product Image Pedestal (Clickable to detail page) */}
      <Link
        href={`/product/${product.id}`}
        className="relative w-full h-32 sm:h-56 @md:h-60 mb-2 sm:mb-3 flex items-center justify-center rounded-xl sm:rounded-2xl bg-[#E8EBF0] dark:bg-[#181D2B] border border-black/[0.06] dark:border-white/10 p-2 sm:p-4 cursor-pointer overflow-hidden group/img transition-colors"
      >
        <div className="relative w-full h-full transform transition-transform duration-500 group-hover/img:scale-105">
          <Image
            src={product.image}
            alt={product.name}
            fill
            className="object-contain drop-shadow-[0_10px_22px_rgba(0,0,0,0.10)]"
            sizes="(max-width: 768px) 200px, 400px"
          />
        </div>
      </Link>

      {/* 2. ROW 1: Rating (Left) & Real Stock Badge (Right) */}
      <div className="flex items-center justify-between text-[10px] sm:text-xs w-full px-0.5 pt-0.5 pb-1 sm:pb-2">
        <div className="flex items-center gap-1 sm:gap-1.5 text-amber-500 font-semibold">
          <Star className="w-3 h-3 sm:w-3.5 sm:h-3.5 fill-amber-500" />
          <span className="text-[#1D1D1F] dark:text-white font-mono">{product.rating || '5.0'}</span>
          <span className="hidden sm:inline text-[#86868B] font-normal">({product.reviewCount || 120})</span>
        </div>

        <div>
          {isAvailable ? (
            <span className={`px-1.5 sm:px-2 py-0.5 rounded-full text-[9px] sm:text-[10px] font-mono font-semibold ${
              stock <= 5 
                ? 'bg-amber-100 text-amber-800 dark:bg-amber-900/40 dark:text-amber-300' 
                : 'bg-emerald-50 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-300'
            }`}>
              {stock <= 5 ? `Only ${stock} Left` : `${stock} In Stock`}
            </span>
          ) : (
            <span className="px-1.5 sm:px-2 py-0.5 rounded-full text-[9px] sm:text-[10px] font-mono font-semibold bg-red-100 text-red-700 dark:bg-red-950/40 dark:text-red-300">
              Out of Stock
            </span>
          )}
        </div>
      </div>

      {/* 3. CENTER COLUMN: Brand, Short Title, Tagline, Price */}
      <div className="text-center space-y-1 w-full py-0.5 sm:py-1">
        {/* Brand Kicker */}
        <span className="text-[9px] sm:text-[11px] font-mono uppercase tracking-widest text-[#0071E3] dark:text-[#38BDF8] font-bold block">
          {product.brand || 'Flagship'}
        </span>

        {/* Short Title (No duplicate brand) */}
        <Link href={`/product/${product.id}`} className="block">
          <h3 className="text-xs sm:text-lg font-bold text-[#1D1D1F] dark:text-white hover:text-[#0071E3] dark:hover:text-[#38BDF8] transition-colors line-clamp-1 tracking-tight">
            {cleanTitle}
          </h3>
        </Link>

        {/* Subtitle / Tagline */}
        <p className="hidden sm:block text-xs sm:text-sm text-[#6E6E73] dark:text-[#A1A1A6] line-clamp-1">
          {product.tagline || product.description}
        </p>

        {/* Price */}
        <div className="pt-1 sm:pt-2">
          <span className="text-sm sm:text-2xl font-bold text-[#1D1D1F] dark:text-white font-mono tracking-tight flex items-baseline justify-center">
            <span className="text-xs sm:text-base font-normal text-gray-500 dark:text-gray-400 mr-1">৳</span>
            <span>{product.priceBDT.toLocaleString()}</span>
          </span>
        </div>
      </div>

      {/* 4. ROW 6: Centered Dual Action Buttons ("Add to Cart" + "Buy") */}
      <div className="cq-stack flex flex-col sm:flex-row items-center justify-center gap-1.5 sm:gap-2.5 pt-2 sm:pt-4 w-full">
        {/* Add to Cart (Silent) */}
        <button
          onClick={handleSilentAdd}
          disabled={!isAvailable}
          className={`cq-btn w-full sm:flex-1 min-h-[34px] sm:min-h-[40px] py-1.5 sm:py-2.5 px-2 rounded-full text-[10px] sm:text-xs font-semibold tracking-wide transition-all active:scale-95 flex items-center justify-center gap-1 touch-manipulation ${
            isAvailable
              ? 'border border-black/15 dark:border-white/20 bg-black/[0.03] hover:bg-black/[0.08] dark:bg-white/[0.06] dark:hover:bg-white/[0.12] text-[#1D1D1F] dark:text-white'
              : 'border border-black/5 dark:border-white/5 bg-black/5 dark:bg-white/5 text-black/30 dark:text-white/30 cursor-not-allowed'
          }`}
          title="Add to cart silently"
        >
          {justAdded ? (
            <>
              <Check className="w-3 h-3 sm:w-3.5 sm:h-3.5 text-emerald-600 dark:text-emerald-400" />
              <span className="text-emerald-600 dark:text-emerald-400">Added ✓</span>
            </>
          ) : (
            <span>Add to Cart</span>
          )}
        </button>

        {/* Buy (Opens Cart Drawer) */}
        <button
          onClick={handleBuy}
          disabled={!isAvailable}
          className={`cq-btn w-full sm:flex-1 min-h-[34px] sm:min-h-[40px] py-1.5 sm:py-2.5 px-3 rounded-full text-[10px] sm:text-xs font-semibold tracking-wide transition-all shadow-sm active:scale-95 flex items-center justify-center gap-1 touch-manipulation ${
            isAvailable
              ? 'bg-[#0071E3] hover:bg-[#0077ED] text-white'
              : 'bg-black/10 dark:bg-white/10 text-black/30 dark:text-white/30 cursor-not-allowed'
          }`}
          title="Buy now and proceed to checkout"
        >
          <span>{isAvailable ? 'Buy' : 'Sold Out'}</span>
        </button>
      </div>

    </motion.div>
  );
};

'use client';

import React from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { useCart } from '../lib/cartContext';
import { X, Heart, ShoppingBag, Trash2, ArrowRight } from 'lucide-react';

export const WishlistDrawer: React.FC = () => {
  const { wishlist, isWishlistOpen, setIsWishlistOpen, toggleWishlist, addToCart } = useCart();

  if (!isWishlistOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex justify-end animate-fadeIn">
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black/50 backdrop-blur-sm transition-opacity"
        onClick={() => setIsWishlistOpen(false)}
      />

      {/* Drawer */}
      <div className="relative w-full max-w-md h-full bg-white dark:bg-[#121624] border-l border-black/10 dark:border-white/10 p-6 flex flex-col z-10 shadow-2xl text-[#1D1D1F] dark:text-white">
        
        {/* Header */}
        <div className="flex items-center justify-between pb-5 border-b border-black/[0.08] dark:border-white/10">
          <div className="flex items-center gap-2">
            <div className="p-2 rounded-xl bg-rose-50 dark:bg-rose-950/40 text-rose-600 dark:text-rose-400">
              <Heart className="w-5 h-5 fill-rose-500 text-rose-500" />
            </div>
            <div>
              <h2 className="text-base font-bold tracking-tight">Saved Hardware</h2>
              <p className="text-xs text-[#86868B]">{wishlist.length} items in your wishlist</p>
            </div>
          </div>
          <button
            onClick={() => setIsWishlistOpen(false)}
            className="p-2 rounded-full text-slate-400 hover:text-[#1D1D1F] dark:hover:text-white hover:bg-black/5 dark:hover:bg-white/10 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Wishlist Items List */}
        <div className="flex-1 overflow-y-auto py-6 space-y-4">
          {wishlist.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-72 text-center p-6 space-y-3">
              <div className="w-16 h-16 rounded-full bg-rose-50 dark:bg-rose-950/30 flex items-center justify-center text-rose-400">
                <Heart className="w-8 h-8 opacity-60" />
              </div>
              <p className="text-base font-semibold text-[#1D1D1F] dark:text-white">Your Wishlist is Empty</p>
              <p className="text-xs text-[#6E6E73] dark:text-[#A1A1A6] max-w-xs leading-relaxed">
                Save bespoke smartphones, foldables, and acoustics by tapping the heart icon on any product card.
              </p>
              <Link
                href="/explore"
                onClick={() => setIsWishlistOpen(false)}
                className="mt-2 px-5 py-2.5 rounded-full text-xs font-semibold bg-[#0071E3] text-white hover:bg-[#0077ED] transition-colors shadow-sm"
              >
                Explore Hardware Archive
              </Link>
            </div>
          ) : (
            wishlist.map((product) => (
              <div
                key={product.id}
                className="p-4 rounded-2xl bg-[#F5F5F7] dark:bg-white/5 border border-black/[0.05] dark:border-white/10 flex items-center gap-4 group hover:border-[#0071E3]/30 transition-all"
              >
                {/* Product Thumbnail */}
                <Link
                  href={`/product/${product.id}`}
                  onClick={() => setIsWishlistOpen(false)}
                  className="relative w-16 h-16 rounded-xl bg-white dark:bg-[#1A2035] flex-shrink-0 border border-black/[0.06] dark:border-white/10 p-1 flex items-center justify-center cursor-pointer"
                >
                  <Image
                    src={product.image}
                    alt={product.name}
                    fill
                    className="object-contain p-1"
                  />
                </Link>

                {/* Details */}
                <div className="flex-1 min-w-0">
                  <span className="text-[10px] font-mono uppercase tracking-wider text-[#0071E3] font-bold block">
                    {product.brand || 'Flagship'}
                  </span>
                  <Link
                    href={`/product/${product.id}`}
                    onClick={() => setIsWishlistOpen(false)}
                    className="text-xs sm:text-sm font-semibold truncate block hover:text-[#0071E3] transition-colors"
                  >
                    {product.name}
                  </Link>
                  <p className="text-xs font-mono font-bold text-[#1D1D1F] dark:text-white mt-1">
                    ৳ {product.priceBDT.toLocaleString()}
                  </p>
                </div>

                {/* Actions */}
                <div className="flex flex-col gap-2 items-end">
                  <button
                    onClick={() => {
                      addToCart(product, 1, true);
                      setIsWishlistOpen(false);
                    }}
                    className="p-2 rounded-xl bg-[#0071E3] hover:bg-[#0077ED] text-white shadow-sm transition-all"
                    title="Add to Bag"
                  >
                    <ShoppingBag className="w-4 h-4" />
                  </button>
                  <button
                    onClick={() => toggleWishlist(product)}
                    className="p-2 rounded-xl text-slate-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-950/40 transition-colors"
                    title="Remove from Wishlist"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            ))
          )}
        </div>

        {/* Footer */}
        {wishlist.length > 0 && (
          <div className="pt-4 pb-[max(env(safe-area-inset-bottom),1rem)] border-t border-black/[0.08] dark:border-white/10 space-y-3">
            <button
              onClick={() => {
                wishlist.forEach((p) => addToCart(p, 1, false));
                setIsWishlistOpen(false);
              }}
              className="w-full flex items-center justify-center gap-2 py-3.5 rounded-full bg-[#0071E3] hover:bg-[#0077ED] text-white font-medium text-xs sm:text-sm tracking-wide transition-all shadow-sm"
            >
              <span>Move All to Bag</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

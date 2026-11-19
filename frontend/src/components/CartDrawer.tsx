'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { useCart } from '../lib/cartContext';
import { validateCoupon } from '../lib/api';
import { X, Trash2, ArrowRight, ShoppingBag, Tag, Check, AlertCircle } from 'lucide-react';

export const CartDrawer: React.FC = () => {
  const { 
    cart, 
    isCartOpen, 
    setIsCartOpen, 
    removeFromCart, 
    updateQuantity, 
    totalBDT,
    appliedCoupon,
    setAppliedCoupon,
    discountBDT
  } = useCart();

  const [couponCode, setCouponCode] = useState('');
  const [couponLoading, setCouponLoading] = useState(false);
  const [couponError, setCouponError] = useState('');
  const [couponSuccess, setCouponSuccess] = useState('');

  if (!isCartOpen) return null;

  const rawSubtotal = cart.reduce((sum, item) => sum + item.product.priceBDT * item.quantity, 0);

  const handleApplyCoupon = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!couponCode.trim()) return;
    setCouponLoading(true);
    setCouponError('');
    setCouponSuccess('');

    const res = await validateCoupon(couponCode.trim(), rawSubtotal);
    if (res.success && res.coupon) {
      setAppliedCoupon(res.coupon);
      setCouponSuccess(res.coupon.description);
      setCouponCode('');
    } else {
      setCouponError(res.error || 'Invalid coupon code');
    }
    setCouponLoading(false);
  };

  const handleRemoveCoupon = () => {
    setAppliedCoupon(null);
    setCouponSuccess('');
    setCouponError('');
  };

  return (
    <div className="fixed inset-0 z-50 flex justify-end">
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black/40 backdrop-blur-sm transition-opacity"
        onClick={() => setIsCartOpen(false)}
      />

      {/* Drawer */}
      <div className="relative w-full max-w-md h-full bg-white dark:bg-obsidian-900 border-l border-black/10 dark:border-slate-800 p-6 flex flex-col z-10 shadow-2xl">
        {/* Header */}
        <div className="flex items-center justify-between pb-5 border-b border-black/[0.08] dark:border-slate-800">
          <div className="flex items-center gap-2">
            <ShoppingBag className="w-5 h-5 text-[#0071E3]" />
            <h2 className="text-base font-semibold tracking-tight text-[#1D1D1F] dark:text-white">Your Cart</h2>
          </div>
          <button
            onClick={() => setIsCartOpen(false)}
            className="p-1 rounded-full text-slate-400 hover:text-[#1D1D1F] hover:bg-black/5 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Cart Item List */}
        <div className="flex-1 overflow-y-auto py-6 space-y-4">
          {cart.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-64 text-center">
              <ShoppingBag className="w-10 h-10 text-slate-300 mb-2" />
              <p className="text-slate-500 text-sm">Your bag is empty.</p>
              <Link
                href="/explore"
                onClick={() => setIsCartOpen(false)}
                className="mt-4 px-4 py-2 rounded-full text-xs font-semibold text-[#0071E3] border border-[#0071E3]/30 hover:bg-[#0071E3]/5 transition-colors"
              >
                Continue Shopping
              </Link>
            </div>
          ) : (
            cart.map(item => (
              <div
                key={`${item.product.id}-${item.selectedColor || 'def'}-${item.selectedStorage || 'def'}`}
                className="flex items-center gap-4 p-3.5 rounded-2xl bg-[#F5F5F7] dark:bg-obsidian-850 border border-black/[0.05]"
              >
                <div className="relative w-16 h-16 rounded-xl overflow-hidden bg-[#E8EBF0] dark:bg-[#181D2B] flex-shrink-0 border border-black/[0.06] dark:border-white/10 p-1">
                  <Image
                    src={item.product.image}
                    alt={item.product.name}
                    fill
                    className="object-contain"
                  />
                </div>
                <div className="flex-1 min-w-0">
                  <h4 className="text-sm font-semibold text-[#1D1D1F] truncate">{item.product.name}</h4>
                  {(item.selectedColor || item.selectedStorage) && (
                    <div className="flex items-center gap-1.5 mt-0.5">
                      {item.selectedColor && (
                        <span className="text-[10px] px-1.5 py-0.5 rounded-md bg-white border border-black/5 font-medium text-slate-600">
                          {item.selectedColor}
                        </span>
                      )}
                      {item.selectedStorage && (
                        <span className="text-[10px] px-1.5 py-0.5 rounded-md bg-white border border-black/5 font-medium text-slate-600">
                          {item.selectedStorage}
                        </span>
                      )}
                    </div>
                  )}
                  <p className="text-xs text-[#0071E3] font-mono mt-0.5 font-bold flex items-baseline">
                    <span className="text-[10px] font-normal mr-1">৳</span>
                    <span>{item.product.priceBDT.toLocaleString()}</span>
                  </p>
                  <div className="flex items-center gap-3 mt-2">
                    <button
                      onClick={() => updateQuantity(item.product.id, item.quantity - 1, item.selectedColor, item.selectedStorage)}
                      className="w-6 h-6 flex items-center justify-center rounded-md bg-white border border-black/10 text-slate-700 hover:bg-slate-100 text-xs font-bold"
                    >
                      -
                    </button>
                    <span className="text-xs text-[#1D1D1F] font-mono font-medium">{item.quantity}</span>
                    <button
                      onClick={() => updateQuantity(item.product.id, item.quantity + 1, item.selectedColor, item.selectedStorage)}
                      className="w-6 h-6 flex items-center justify-center rounded-md bg-white border border-black/10 text-slate-700 hover:bg-slate-100 text-xs font-bold"
                    >
                      +
                    </button>
                  </div>
                </div>
                <button
                  onClick={() => removeFromCart(item.product.id, item.selectedColor, item.selectedStorage)}
                  className="p-2 text-slate-400 hover:text-red-500 transition-colors"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            ))
          )}
        </div>

        {/* Footer Summary & Checkout */}
        {cart.length > 0 && (
          <div className="pt-3 sm:pt-4 pb-[max(env(safe-area-inset-bottom),1.25rem)] border-t border-black/[0.08] dark:border-white/10 space-y-3">
            
            {/* Promo Code Input Bar */}
            {appliedCoupon ? (
              <div className="p-2.5 rounded-xl bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800 flex items-center justify-between text-xs">
                <div className="flex items-center gap-1.5 text-emerald-800 dark:text-emerald-300 font-medium">
                  <Check className="w-3.5 h-3.5" />
                  <span>Promo <strong>{appliedCoupon.code}</strong> applied (-৳{appliedCoupon.discountBDT.toLocaleString()})</span>
                </div>
                <button
                  type="button"
                  onClick={handleRemoveCoupon}
                  className="text-red-500 hover:text-red-700 text-[10px] font-bold uppercase underline"
                >
                  Remove
                </button>
              </div>
            ) : (
              <form onSubmit={handleApplyCoupon} className="flex gap-2">
                <div className="relative flex-1">
                  <Tag className="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-slate-400" />
                  <input
                    type="text"
                    value={couponCode}
                    onChange={(e) => setCouponCode(e.target.value)}
                    placeholder="Coupon (e.g. NEXORA10)"
                    className="w-full pl-9 pr-3 py-1.5 rounded-xl bg-[#F5F5F7] dark:bg-white/5 border border-black/10 dark:border-white/10 text-xs text-[#1D1D1F] dark:text-white uppercase placeholder-normal focus:outline-none focus:border-[#0071E3]"
                  />
                </div>
                <button
                  type="submit"
                  disabled={couponLoading || !couponCode.trim()}
                  className="px-4 py-1.5 rounded-xl bg-[#0B132B] dark:bg-white/10 text-white text-xs font-semibold hover:bg-black transition-all disabled:opacity-40"
                >
                  {couponLoading ? '...' : 'Apply'}
                </button>
              </form>
            )}

            {couponError && (
              <p className="text-[10px] text-red-500 text-left">{couponError}</p>
            )}

            {/* Calculations Breakdown */}
            <div className="space-y-1.5 text-xs">
              <div className="flex items-center justify-between text-slate-500">
                <span>Subtotal</span>
                <span className="font-mono">৳ {rawSubtotal.toLocaleString()}</span>
              </div>
              {appliedCoupon && (
                <div className="flex items-center justify-between text-emerald-600 dark:text-emerald-400 font-semibold">
                  <span>Coupon Savings</span>
                  <span className="font-mono">- ৳ {discountBDT.toLocaleString()}</span>
                </div>
              )}
              <div className="flex items-center justify-between text-sm font-bold pt-1.5 border-t border-black/[0.04] dark:border-white/10">
                <span className="text-[#1D1D1F] dark:text-white">Estimated Total:</span>
                <span className="text-lg font-bold text-[#0071E3] font-mono flex items-baseline">
                  <span className="text-sm font-normal mr-1">৳</span>
                  <span>{totalBDT.toLocaleString()}</span>
                </span>
              </div>
            </div>

            <p className="text-[10px] text-slate-400">
              * Supports bKash, Nagad, Cash on Delivery, Bank &amp; Cards.
            </p>
            
            <Link
              href="/checkout"
              onClick={() => setIsCartOpen(false)}
              className="w-full flex items-center justify-center gap-2 py-3 rounded-full bg-[#0071E3] hover:bg-[#0077ED] text-white font-medium text-sm tracking-wide transition-all shadow-sm"
            >
              <span>Check Out</span>
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        )}
      </div>
    </div>
  );
};

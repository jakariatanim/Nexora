'use client';

import React, { useState, useEffect, Suspense } from 'react';
import { useSearchParams } from 'next/navigation';
import Link from 'next/link';
import { trackOrder } from '../../lib/api';
import { Order } from '../../lib/types';
import { Search, AlertCircle, ShieldCheck } from 'lucide-react';

function TrackOrderContent() {
  const searchParams = useSearchParams();
  const initialCode = searchParams.get('code') || '';

  const [query, setQuery] = useState(initialCode);
  const [order, setOrder] = useState<Order | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (initialCode) {
      handleSearch(initialCode);
    }
  }, [initialCode]);

  const handleSearch = async (searchCode: string) => {
    if (!searchCode.trim()) return;
    setLoading(true);
    setError('');
    const result = await trackOrder(searchCode.trim());
    if (result) {
      setOrder(result);
    } else {
      setError('No order found matching that tracking code or phone number.');
      setOrder(null);
    }
    setLoading(false);
  };

  const steps = ['Pending', 'Processing', 'Shipped', 'Delivered'];
  const getStepIndex = (status: string) => {
    const idx = steps.indexOf(status);
    return idx === -1 ? 0 : idx;
  };

  return (
    <div className="max-w-4xl mx-auto px-4 pt-28 sm:pt-36 pb-20 sm:pb-24 bg-[#F7F4EE]">
      {/* Header */}
      <div className="text-center max-w-xl mx-auto mb-8 sm:mb-10 space-y-2">
        <span className="text-xs font-mono tracking-widest text-[#0071E3] uppercase font-semibold">
          Live Telemetry
        </span>
        <h1 className="text-3xl sm:text-4xl font-semibold text-[#1D1D1F] tracking-tight">
          Track Your Order
        </h1>
        <p className="text-xs text-[#6E6E73]">
          Enter your Order Tracking Code (e.g. NX-2026-5802) or the phone number used during checkout.
        </p>
      </div>

      {/* Search Input Bar */}
      <div className="max-w-lg mx-auto mb-10 sm:mb-12">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSearch(query);
          }}
          className="flex items-center gap-2 p-1.5 sm:p-2 rounded-full bg-white border border-black/10 shadow-sm"
        >
          <Search className="w-4 h-4 text-slate-400 ml-3 flex-shrink-0" />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Order Code or Phone (e.g. NX-2026-5802)"
            className="flex-1 bg-transparent px-2 py-2 text-base sm:text-sm text-[#1D1D1F] placeholder-slate-400 focus:outline-none min-w-0"
          />
          <button
            type="submit"
            disabled={loading}
            className="px-5 sm:px-6 py-2.5 rounded-full bg-[#0071E3] hover:bg-[#0077ED] text-white font-medium text-xs tracking-wide transition-all shadow-sm flex-shrink-0 min-h-[38px]"
          >
            {loading ? 'Locating...' : 'Track'}
          </button>
        </form>

        {error && (
          <div className="flex items-center justify-center gap-2 text-xs text-red-600 mt-4">
            <AlertCircle className="w-4 h-4" />
            <span>{error}</span>
          </div>
        )}
      </div>

      {/* Order Status Display */}
      {order && (
        <div className="p-5 sm:p-10 rounded-2xl sm:rounded-3xl bg-white border border-black/[0.08] shadow-md space-y-6 sm:space-y-8 animate-fadeIn text-left">
          
          <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-6 border-b border-black/[0.06] gap-4">
            <div>
              <span className="text-[11px] font-mono text-[#86868B]">Order Reference</span>
              <h3 className="text-xl font-bold font-mono text-[#0071E3]">{order.id}</h3>
            </div>
            <div className="text-left sm:text-right">
              <span className="text-[11px] font-mono text-[#86868B] block">Current Status</span>
              <span className="px-4 py-1 rounded-full text-xs font-medium tracking-wide bg-[#0071E3]/10 text-[#0071E3] border border-[#0071E3]/20 inline-block mt-1">
                {order.status}
              </span>
            </div>
          </div>

          {/* Stepper Progress */}
          <div className="py-4">
            <div className="relative flex items-center justify-between">
              <div className="absolute left-0 top-1/2 -translate-y-1/2 w-full h-1 bg-slate-100 -z-0" />
              <div
                className="absolute left-0 top-1/2 -translate-y-1/2 h-1 bg-[#0071E3] transition-all duration-700 -z-0"
                style={{
                  width: `${(getStepIndex(order.status) / (steps.length - 1)) * 100}%`,
                }}
              />

              {steps.map((step, index) => {
                const isPassed = index <= getStepIndex(order.status);
                return (
                  <div key={step} className="flex flex-col items-center gap-1.5 z-10">
                    <div
                      className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold transition-all ${
                        isPassed
                          ? 'bg-[#0071E3] text-white shadow-sm'
                          : 'bg-[#F5F5F7] text-slate-400 border border-slate-200'
                      }`}
                    >
                      {index + 1}
                    </div>
                    <span
                      className={`text-[9px] sm:text-[11px] uppercase tracking-wider text-center ${
                        isPassed ? 'text-[#1D1D1F] font-semibold' : 'text-[#86868B]'
                      }`}
                    >
                      {step}
                    </span>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Details Breakdown */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-6 border-t border-black/[0.06] text-xs">
            <div className="space-y-1.5">
              <span className="font-mono text-[#86868B] uppercase tracking-widest block font-medium">
                Customer &amp; Dispatch
              </span>
              <p className="text-[#1D1D1F] font-semibold">{order.customer.name}</p>
              <p className="text-[#6E6E73]">{order.customer.phone}</p>
              <p className="text-[#6E6E73]">{order.customer.address}</p>
            </div>

            <div className="space-y-1.5">
              <span className="font-mono text-[#86868B] uppercase tracking-widest block font-medium">
                Payment Info
              </span>
              <p className="text-[#1D1D1F] font-semibold">Method: {order.paymentMethod}</p>
              <p className="font-mono text-[#6E6E73]">TrxID: {order.transactionId}</p>
              <p className="font-mono text-[#0071E3] font-bold text-sm flex items-baseline">
                <span className="mr-1">Total:</span>
                <span className="text-xs font-normal text-[#0071E3]/70 mr-1">৳</span>
                <span>{order.totalBDT.toLocaleString()}</span>
              </p>
            </div>
          </div>

          {/* Items List */}
          <div className="pt-4 border-t border-black/[0.06]">
            <span className="font-mono text-[#86868B] uppercase tracking-widest block text-xs mb-3 font-medium">
              Allocated Hardware
            </span>
            <div className="space-y-2">
              {order.items.map((item, idx) => (
                <div key={idx} className="flex justify-between items-center text-xs text-[#424245]">
                  <span>{item.name} (x{item.quantity})</span>
                  <span className="font-mono text-[#1D1D1F] font-semibold flex items-baseline">
                    <span className="text-[10px] font-normal text-gray-500 mr-1">৳</span>
                    <span>{(item.priceBDT * item.quantity).toLocaleString()}</span>
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* 7-Day Replacement & Warranty RMA Claim Box */}
          <div className="pt-4 border-t border-black/[0.06] flex flex-col sm:flex-row items-center justify-between gap-3 bg-blue-50/50 p-4 rounded-2xl border border-blue-100">
            <div>
              <span className="text-xs font-semibold text-[#1D1D1F] flex items-center gap-1.5">
                <ShieldCheck className="w-4 h-4 text-[#0071E3]" />
                <span>7-Day Replacement Guarantee &bull; Official RMA Support</span>
              </span>
              <p className="text-[11px] text-[#6E6E73] mt-0.5">
                Experiencing technical hardware issues? Submit an official replacement ticket.
              </p>
            </div>
            <Link
              href={`/warranty-claim?orderId=${encodeURIComponent(order.id)}`}
              className="px-4 py-2 rounded-full bg-[#0071E3] hover:bg-[#0077ED] text-white text-xs font-semibold tracking-wide flex-shrink-0 transition-colors shadow-xs"
            >
              Apply for RMA Claim &rarr;
            </Link>
          </div>
        </div>
      )}

      {/* Direct RMA Claim Portal Link */}
      <div className="text-center pt-8 text-xs text-[#6E6E73]">
        <span>Need to return or exchange a gadget? </span>
        <Link href="/warranty-claim" className="text-[#0071E3] font-semibold hover:underline">
          Visit 7-Day RMA Claim Portal &rarr;
        </Link>
      </div>
    </div>
  );
}

export default function TrackOrderPage() {
  return (
    <Suspense fallback={<div className="pt-36 text-center text-slate-400 font-mono text-sm">Loading telemetry...</div>}>
      <TrackOrderContent />
    </Suspense>
  );
}

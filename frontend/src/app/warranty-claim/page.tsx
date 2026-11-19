'use client';

import React, { useState, useEffect, Suspense } from 'react';
import Link from 'next/link';
import { useSearchParams } from 'next/navigation';
import { submitClaim } from '../../lib/api';
import { Claim } from '../../lib/types';
import { 
  ShieldCheck, 
  ArrowLeft, 
  CheckCircle2, 
  RefreshCw, 
  AlertTriangle, 
  Clock, 
  Phone, 
  FileText, 
  Truck,
  Sparkles,
  Search
} from 'lucide-react';

function WarrantyClaimContent() {
  const searchParams = useSearchParams();
  const [orderId, setOrderId] = useState('');
  const [customerName, setCustomerName] = useState('');
  const [customerPhone, setCustomerPhone] = useState('');
  const [issueType, setIssueType] = useState('Hardware Defect / Malfunction');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [submittedClaim, setSubmittedClaim] = useState<Claim | null>(null);

  useEffect(() => {
    const qOrderId = searchParams.get('orderId') || searchParams.get('id');
    if (qOrderId) {
      setOrderId(qOrderId);
    }
  }, [searchParams]);

  const issueOptions = [
    'Hardware Defect / Malfunction',
    'Display, Touch or Pixel Glitch',
    'Acoustic Sync / Bluetooth Disconnection',
    'Battery or Fast Charging Irregularity',
    'Package Transit Damage upon Delivery',
    'Other Technical Inspection Request',
  ];

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const res = await submitClaim({
        orderId: orderId.trim(),
        customerName: customerName.trim(),
        customerPhone: customerPhone.trim(),
        issueType,
        description: description.trim(),
      });

      if (res.success && res.claim) {
        setSubmittedClaim(res.claim);
      } else {
        setError(res.error || 'Failed to submit warranty ticket. Please check your order reference.');
      }
    } catch (err) {
      setError('Connection to warranty server failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#F7F4EE] dark:bg-[#080E1E] pt-28 sm:pt-36 pb-20 sm:pb-24 px-4 sm:px-6 transition-colors">
      <div className="max-w-3xl mx-auto space-y-8">
        
        {/* Back Link */}
        <div>
          <Link
            href="/"
            className="inline-flex items-center gap-2 text-xs font-semibold px-4 py-2 rounded-full bg-white dark:bg-[#121624] border border-black/10 dark:border-white/15 text-[#0071E3] hover:bg-[#0071E3] hover:text-white transition-all shadow-sm"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Return to Store</span>
          </Link>
        </div>

        {/* Header Stage */}
        <div className="text-center space-y-2.5">
          <div className="inline-flex items-center gap-1.5 px-3.5 py-1 rounded-full bg-emerald-50 dark:bg-emerald-950/40 text-emerald-700 dark:text-emerald-400 border border-emerald-200 dark:border-emerald-800 text-xs font-mono font-semibold uppercase tracking-wider">
            <ShieldCheck className="w-4 h-4" />
            <span>7-Day Replacement &amp; 1-Year Hardware Warranty</span>
          </div>
          <h1 className="text-3xl sm:text-4xl font-semibold tracking-tight text-[#1D1D1F] dark:text-white">
            Warranty Claim &amp; Replacement Portal
          </h1>
          <p className="text-xs sm:text-sm text-[#6E6E73] dark:text-[#A1A1A6] max-w-xl mx-auto leading-relaxed">
            Every genuine gadget from NEXORA is protected by our guaranteed 7-day hassle-free replacement policy and official manufacturer hardware coverage.
          </p>
        </div>

        {/* Claim Submission Result */}
        {submittedClaim ? (
          <div className="p-8 sm:p-12 rounded-3xl bg-white dark:bg-[#121624] border border-black/[0.08] dark:border-white/10 shadow-xl space-y-6 text-center animate-fadeIn">
            <div className="w-16 h-16 rounded-full bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800 flex items-center justify-center mx-auto text-emerald-600 dark:text-emerald-400">
              <CheckCircle2 className="w-8 h-8" />
            </div>

            <div>
              <span className="text-xs font-mono tracking-widest text-[#0071E3] uppercase font-bold">
                Ticket Generated
              </span>
              <h2 className="text-2xl sm:text-3xl font-bold text-[#1D1D1F] dark:text-white mt-1">
                Replacement Ticket Registered
              </h2>
              <p className="text-xs sm:text-sm text-[#6E6E73] dark:text-[#A1A1A6] mt-2">
                Thank you, <strong className="text-[#1D1D1F] dark:text-white">{submittedClaim.customerName}</strong>. Our senior hardware engineers will review your telemetry report.
              </p>
            </div>

            {/* RMA Code Badge */}
            <div className="p-5 rounded-2xl bg-[#F5F5F7] dark:bg-white/5 border border-black/[0.06] dark:border-white/10 text-center max-w-md mx-auto space-y-1">
              <span className="text-xs font-mono uppercase tracking-wider text-[#86868B]">
                Your RMA Tracking Code
              </span>
              <div className="text-3xl font-mono font-extrabold text-[#0071E3] dark:text-[#38BDF8] tracking-widest">
                {submittedClaim.id}
              </div>
              <p className="text-[11px] text-[#6E6E73] dark:text-[#A1A1A6] pt-1">
                Status: <strong className="text-amber-600 dark:text-amber-400">{submittedClaim.status}</strong>
              </p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-left max-w-xl mx-auto pt-2">
              <div className="p-3.5 rounded-xl bg-[#F5F5F7] dark:bg-white/5 border border-black/[0.04] dark:border-white/10 text-xs">
                <Truck className="w-4 h-4 text-[#0071E3] mb-1.5" />
                <p className="font-semibold text-[#1D1D1F] dark:text-white">Free Doorstep Pickup</p>
                <p className="text-[11px] text-[#6E6E73] dark:text-[#A1A1A6]">Our courier will collect the gadget from your address in BD.</p>
              </div>

              <div className="p-3.5 rounded-xl bg-[#F5F5F7] dark:bg-white/5 border border-black/[0.04] dark:border-white/10 text-xs">
                <RefreshCw className="w-4 h-4 text-[#0071E3] mb-1.5" />
                <p className="font-semibold text-[#1D1D1F] dark:text-white">Sealed Replacement</p>
                <p className="text-[11px] text-[#6E6E73] dark:text-[#A1A1A6]">Brand new authentic unit dispatched immediately.</p>
              </div>

              <div className="p-3.5 rounded-xl bg-[#F5F5F7] dark:bg-white/5 border border-black/[0.04] dark:border-white/10 text-xs">
                <Clock className="w-4 h-4 text-[#0071E3] mb-1.5" />
                <p className="font-semibold text-[#1D1D1F] dark:text-white">24-Hour Resolution</p>
                <p className="text-[11px] text-[#6E6E73] dark:text-[#A1A1A6]">Fast diagnosis and concierge updates via WhatsApp.</p>
              </div>
            </div>

            <div className="pt-4 flex flex-col sm:flex-row items-center justify-center gap-3">
              <button
                onClick={() => setSubmittedClaim(null)}
                className="w-full sm:w-auto px-6 py-2.5 rounded-full border border-black/10 dark:border-white/15 text-xs font-semibold hover:bg-black/5 dark:hover:bg-white/10 transition-colors"
              >
                Submit Another Request
              </button>
              <Link
                href="/"
                className="w-full sm:w-auto px-8 py-2.5 rounded-full bg-[#0071E3] text-white text-xs font-semibold hover:bg-[#0077ED] transition-colors shadow-sm"
              >
                Return to Showroom
              </Link>
            </div>
          </div>
        ) : (
          /* Claim Form */
          <div className="p-6 sm:p-10 rounded-3xl bg-white dark:bg-[#121624] border border-black/[0.08] dark:border-white/10 shadow-lg space-y-6">
            
            {error && (
              <div className="p-3.5 rounded-2xl bg-red-50 dark:bg-red-950/40 border border-red-200 dark:border-red-800 text-red-600 dark:text-red-300 text-xs text-center font-medium">
                {error}
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-4 sm:space-y-5 text-left">
              
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {/* Order ID */}
                <div>
                  <label className="block text-xs font-medium text-[#1D1D1F] dark:text-slate-200 mb-1">
                    Order Tracking Reference *
                  </label>
                  <input
                    type="text"
                    required
                    value={orderId}
                    onChange={(e) => setOrderId(e.target.value)}
                    placeholder="e.g. NX-2026-8812"
                    className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] dark:bg-white/5 border border-black/10 dark:border-white/15 text-base sm:text-sm text-[#1D1D1F] dark:text-white uppercase font-mono placeholder-normal focus:outline-none focus:border-[#0071E3]"
                  />
                  <span className="text-[10px] text-[#86868B] mt-0.5 block">Found on your order confirmation or SMS receipt.</span>
                </div>

                {/* Customer Phone */}
                <div>
                  <label className="block text-xs font-medium text-[#1D1D1F] dark:text-slate-200 mb-1">
                    Registered Contact Phone *
                  </label>
                  <input
                    type="tel"
                    required
                    value={customerPhone}
                    onChange={(e) => setCustomerPhone(e.target.value)}
                    placeholder="017XXXXXXXX"
                    className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] dark:bg-white/5 border border-black/10 dark:border-white/15 text-base sm:text-sm text-[#1D1D1F] dark:text-white focus:outline-none focus:border-[#0071E3]"
                  />
                </div>
              </div>

              {/* Full Name */}
              <div>
                <label className="block text-xs font-medium text-[#1D1D1F] dark:text-slate-200 mb-1">
                  Customer Full Name *
                </label>
                <input
                  type="text"
                  required
                  value={customerName}
                  onChange={(e) => setCustomerName(e.target.value)}
                  placeholder="e.g. Tanvir Ahmed"
                  className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] dark:bg-white/5 border border-black/10 dark:border-white/15 text-base sm:text-sm text-[#1D1D1F] dark:text-white focus:outline-none focus:border-[#0071E3]"
                />
              </div>

              {/* Issue Type */}
              <div>
                <label className="block text-xs font-medium text-[#1D1D1F] dark:text-slate-200 mb-1">
                  Select Technical Issue Category *
                </label>
                <select
                  value={issueType}
                  onChange={(e) => setIssueType(e.target.value)}
                  className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] dark:bg-white/5 border border-black/10 dark:border-white/15 text-base sm:text-sm text-[#1D1D1F] dark:text-white focus:outline-none focus:border-[#0071E3]"
                >
                  {issueOptions.map((opt) => (
                    <option key={opt} value={opt} className="dark:bg-[#121624] text-[#1D1D1F] dark:text-white">
                      {opt}
                    </option>
                  ))}
                </select>
              </div>

              {/* Problem Description */}
              <div>
                <label className="block text-xs font-medium text-[#1D1D1F] dark:text-slate-200 mb-1">
                  Detailed Description of the Issue *
                </label>
                <textarea
                  rows={4}
                  required
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder="Please describe what occurred, whether the device powers on, and any error message displayed..."
                  className="w-full px-4 py-2.5 rounded-xl bg-[#F5F5F7] dark:bg-white/5 border border-black/10 dark:border-white/15 text-base sm:text-sm text-[#1D1D1F] dark:text-white focus:outline-none focus:border-[#0071E3]"
                />
              </div>

              {/* Policy Check */}
              <div className="p-4 rounded-2xl bg-[#F5F5F7] dark:bg-white/5 border border-black/[0.04] dark:border-white/10 text-xs text-[#6E6E73] dark:text-[#A1A1A6] flex items-start gap-2.5">
                <AlertTriangle className="w-4 h-4 text-amber-500 flex-shrink-0 mt-0.5" />
                <p className="leading-relaxed">
                  Under the 7-day policy, devices with manufacturer defects will be replaced with a brand new sealed unit. Physical water submergence beyond IP rating or accidental drops are serviced under standard warranty terms.
                </p>
              </div>

              {/* Submit CTA */}
              <button
                type="submit"
                disabled={loading}
                className="w-full py-3.5 rounded-full bg-[#0071E3] hover:bg-[#0077ED] text-white font-medium text-sm tracking-wide transition-all shadow-md active:scale-95 disabled:opacity-50"
              >
                {loading ? 'Registering Replacement Ticket...' : 'Submit Warranty Claim Ticket'}
              </button>
            </form>
          </div>
        )}

      </div>
    </div>
  );
}

export default function WarrantyClaimPage() {
  return (
    <Suspense fallback={<div className="min-h-screen bg-[#F7F4EE] pt-32 text-center text-slate-500 font-medium">Loading Warranty Claim Portal...</div>}>
      <WarrantyClaimContent />
    </Suspense>
  );
}

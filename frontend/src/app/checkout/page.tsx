'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { useCart } from '../../lib/cartContext';
import { createOrder, validateCoupon } from '../../lib/api';
import { 
  ShieldCheck, 
  ArrowRight, 
  CheckCircle2, 
  Truck, 
  CreditCard, 
  Smartphone, 
  UserCheck, 
  Printer, 
  Tag, 
  Check, 
  X, 
  FileText,
  MapPin,
  Building,
  Home
} from 'lucide-react';

export default function CheckoutPage() {
  const { 
    cart, 
    totalBDT, 
    clearCart, 
    user, 
    setIsAuthModalOpen, 
    appliedCoupon, 
    setAppliedCoupon, 
    discountBDT 
  } = useCart();
  
  const [name, setName] = useState(user?.name || '');
  const [phone, setPhone] = useState(user?.phone || '');
  const [email, setEmail] = useState(user?.email || '');
  const [address, setAddress] = useState('');
  const [addressType, setAddressType] = useState<'Home' | 'Office'>('Home');
  const [deliveryZone, setDeliveryZone] = useState<'dhaka' | 'greater_dhaka' | 'outside_dhaka'>('dhaka');
  const [paymentMethod, setPaymentMethod] = useState<'bKash' | 'Nagad' | 'Cash on Delivery' | 'Bank Transfer' | 'Credit/Debit Card'>('bKash');
  const [transactionId, setTransactionId] = useState('');
  const [loading, setLoading] = useState(false);
  const [orderConfirmed, setOrderConfirmed] = useState<any | null>(null);
  const [showInvoice, setShowInvoice] = useState(false);

  // Checkout coupon state
  const [couponInput, setCouponInput] = useState('');
  const [couponLoading, setCouponLoading] = useState(false);
  const [couponMsg, setCouponMsg] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  // Sync logged-in customer info automatically
  useEffect(() => {
    if (user) {
      if (user.name && !name) setName(user.name);
      if (user.phone && !phone) setPhone(user.phone);
      if (user.email && !email) setEmail(user.email);
    }
  }, [user]);

  const rawSubtotal = cart.reduce((sum, item) => sum + item.product.priceBDT * item.quantity, 0);
  const baseDeliveryFee = deliveryZone === 'greater_dhaka' ? 100 : deliveryZone === 'outside_dhaka' ? 140 : 70;
  const deliveryFee = appliedCoupon?.type === 'freeship' ? 0 : baseDeliveryFee;
  const grandTotal = Math.max(0, rawSubtotal - discountBDT + (cart.length > 0 ? deliveryFee : 0));

  const handleApplyCoupon = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!couponInput.trim()) return;
    setCouponLoading(true);
    setCouponMsg(null);

    const res = await validateCoupon(couponInput.trim(), rawSubtotal);
    if (res.success && res.coupon) {
      setAppliedCoupon(res.coupon);
      setCouponMsg({ type: 'success', text: res.coupon.description });
      setCouponInput('');
    } else {
      setCouponMsg({ type: 'error', text: res.error || 'Invalid coupon code.' });
    }
    setCouponLoading(false);
  };

  const handlePlaceOrder = async (e: React.FormEvent) => {
    e.preventDefault();
    if (cart.length === 0) return;
    setLoading(true);

    const orderPayload = {
      customer: {
        name,
        phone,
        email,
        address: `[${addressType}] ${address}`,
        deliveryZone,
      },
      deliveryZone,
      couponCode: appliedCoupon?.code || '',
      items: cart.map(item => ({
        id: item.product.id,
        name: item.product.name,
        priceBDT: item.product.priceBDT,
        quantity: item.quantity,
        selectedColor: item.selectedColor || 'Default',
        selectedStorage: item.selectedStorage || 'Standard',
      })),
      totalBDT: grandTotal,
      paymentMethod,
      transactionId: paymentMethod === 'Cash on Delivery' ? 'COD-VERIFIED' : (transactionId || 'PENDING-VERIFY'),
      coupon: appliedCoupon?.code,
      discountBDT: discountBDT,
    };

    const result = await createOrder(orderPayload);
    if (result && result.id && result.customer) {
      setOrderConfirmed(result);
      clearCart();
    } else {
      alert((result as any)?.error || 'Order submission failed. Please verify your stock or details.');
    }
    setLoading(false);
  };

  if (orderConfirmed) {
    return (
      <div className="max-w-3xl mx-auto px-4 pt-36 pb-24 text-center bg-[#F7F4EE]">
        <div className="rounded-3xl p-10 bg-white border border-black/[0.08] shadow-xl space-y-6">
          <div className="w-16 h-16 rounded-full bg-emerald-50 border border-emerald-200 flex items-center justify-center mx-auto text-emerald-600">
            <CheckCircle2 className="w-8 h-8" />
          </div>

          <div>
            <span className="text-xs font-mono tracking-widest text-[#0071E3] uppercase font-semibold">
              Order Confirmed &bull; Hardware Allocated
            </span>
            <h1 className="text-3xl font-semibold text-[#1D1D1F] mt-1 tracking-tight">
              Welcome to the Next Era!
            </h1>
            <p className="text-sm text-[#6E6E73] mt-2">
              Thank you, <strong className="text-[#1D1D1F]">{orderConfirmed.customer.name}</strong>. Your hardware allocation is locked.
            </p>
          </div>

          {/* Tracking ID Badge */}
          <div className="p-4 rounded-2xl bg-[#F5F5F7] border border-black/[0.06] text-center max-w-sm mx-auto">
            <span className="text-xs text-[#86868B] block mb-1">Your Official Tracking Code</span>
            <div className="text-2xl font-mono font-bold text-[#0071E3] tracking-wider">
              {orderConfirmed.id}
            </div>
            <p className="text-[11px] text-[#86868B] mt-1">
              Save this code or click below to view live telemetry and progress.
            </p>
          </div>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-3 pt-4">
            <button
              type="button"
              onClick={() => setShowInvoice(true)}
              className="w-full sm:w-auto px-6 py-3 rounded-full bg-slate-900 text-white font-medium text-sm tracking-wide shadow-sm hover:bg-black flex items-center justify-center gap-2 transition-colors"
            >
              <Printer className="w-4 h-4 text-emerald-400" />
              <span>Print Official Cash Memo / Invoice</span>
            </button>
            <Link
              href={`/track-order?code=${orderConfirmed.id}`}
              className="w-full sm:w-auto px-6 py-3 rounded-full bg-[#0071E3] text-white font-medium text-sm tracking-wide shadow-sm hover:bg-[#0077ED] transition-colors"
            >
              Track Order Live
            </Link>
            <Link
              href="/"
              className="w-full sm:w-auto px-6 py-3 rounded-full border border-black/10 text-[#1D1D1F] font-medium text-sm hover:bg-black/[0.02] transition-colors"
            >
              Return to Showroom
            </Link>
          </div>
        </div>

        {/* Printable Official Invoice / Cash Memo Modal */}
        {showInvoice && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in duration-200">
            <div className="relative w-full max-w-2xl bg-white rounded-3xl shadow-2xl p-6 sm:p-8 text-left max-h-[90vh] overflow-y-auto">
              {/* Header Controls */}
              <div className="flex items-center justify-between pb-4 border-b border-gray-200 print:hidden">
                <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-gray-500">
                  <FileText className="w-4 h-4 text-[#0071E3]" />
                  <span>Official Cash Memo &bull; Tax Invoice</span>
                </div>
                <div className="flex items-center gap-2">
                  <button
                    type="button"
                    onClick={() => window.print()}
                    className="px-4 py-1.5 rounded-full bg-[#0071E3] hover:bg-[#0077ED] text-white text-xs font-medium flex items-center gap-1.5 shadow-sm"
                  >
                    <Printer className="w-3.5 h-3.5" />
                    <span>Print Memo</span>
                  </button>
                  <button
                    type="button"
                    onClick={() => setShowInvoice(false)}
                    className="w-8 h-8 rounded-full bg-gray-100 hover:bg-gray-200 flex items-center justify-center text-gray-600 transition-colors"
                  >
                    <X className="w-4 h-4" />
                  </button>
                </div>
              </div>

              {/* Printable Invoice Body */}
              <div id="printable-memo" className="pt-6 space-y-6 text-[#1D1D1F]">
                {/* Brand & Memo Meta */}
                <div className="flex items-start justify-between">
                  <div>
                    <h2 className="text-2xl font-bold tracking-tight text-[#0B132B]">NEXORA</h2>
                    <p className="text-[11px] text-[#6E6E73] uppercase tracking-wider font-medium">Step Into the Next Era</p>
                    <p className="text-xs text-gray-500 mt-1">Gulshan-2, Dhaka 1212, Bangladesh</p>
                    <p className="text-xs text-gray-500">Hotline: +880 1640-026177 &bull; support@nexora.com</p>
                  </div>
                  <div className="text-right">
                    <span className="inline-block px-3 py-1 rounded-full bg-emerald-50 text-emerald-700 text-xs font-mono font-bold border border-emerald-200">
                      PAID / CONFIRMED
                    </span>
                    <p className="text-xs font-mono text-gray-500 mt-2">Memo #{orderConfirmed.id}</p>
                    <p className="text-xs text-gray-500">Date: {new Date(orderConfirmed.createdAt || Date.now()).toLocaleDateString('en-GB')}</p>
                  </div>
                </div>

                {/* Customer & Shipping Details */}
                <div className="grid grid-cols-2 gap-4 p-4 rounded-2xl bg-gray-50 border border-gray-100 text-xs">
                  <div>
                    <span className="text-[10px] uppercase font-bold text-gray-400 tracking-wider block mb-1">Billed &amp; Shipped To:</span>
                    <p className="font-semibold text-gray-900">{orderConfirmed.customer.name}</p>
                    <p className="text-gray-600 font-mono">{orderConfirmed.customer.phone}</p>
                    {orderConfirmed.customer.email && <p className="text-gray-600">{orderConfirmed.customer.email}</p>}
                    <p className="text-gray-700 mt-1 whitespace-pre-wrap">{orderConfirmed.customer.address}</p>
                  </div>
                  <div className="text-right">
                    <span className="text-[10px] uppercase font-bold text-gray-400 tracking-wider block mb-1">Payment &amp; Logistics:</span>
                    <p className="font-medium text-gray-800">Method: <strong className="text-gray-900">{orderConfirmed.paymentMethod}</strong></p>
                    <p className="font-mono text-gray-600">TrxID: {orderConfirmed.transactionId}</p>
                    <p className="text-gray-600 mt-1">Status: <span className="text-blue-600 font-medium">Processing Allocation</span></p>
                    <p className="text-gray-500 text-[11px] mt-1">Logistics: Express Nationwide Dispatch</p>
                  </div>
                </div>

                {/* Line Items Table */}
                <div className="border border-gray-200 rounded-2xl overflow-hidden">
                  <table className="w-full text-xs">
                    <thead className="bg-gray-100/75 border-b border-gray-200 text-gray-600 font-semibold uppercase tracking-wider">
                      <tr>
                        <th className="py-2.5 px-4 text-left">Item Description</th>
                        <th className="py-2.5 px-3 text-center">Qty</th>
                        <th className="py-2.5 px-4 text-right">Unit Price</th>
                        <th className="py-2.5 px-4 text-right">Total</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-100">
                      {orderConfirmed.items.map((item: any, idx: number) => (
                        <tr key={idx} className="hover:bg-gray-50/50">
                          <td className="py-2.5 px-4 font-medium text-gray-900">{item.name}</td>
                          <td className="py-2.5 px-3 text-center font-mono text-gray-700">{item.quantity}</td>
                          <td className="py-2.5 px-4 text-right font-mono text-gray-700">৳{item.priceBDT.toLocaleString()}</td>
                          <td className="py-2.5 px-4 text-right font-mono font-bold text-gray-900">৳{(item.priceBDT * item.quantity).toLocaleString()}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>

                {/* Totals Summary */}
                <div className="flex justify-end text-xs">
                  <div className="w-64 space-y-2">
                    {orderConfirmed.discountBDT ? (
                      <div className="flex justify-between text-emerald-600 font-medium">
                        <span>Promo Code Discount ({orderConfirmed.coupon || 'Applied'})</span>
                        <span className="font-mono">-৳{Number(orderConfirmed.discountBDT).toLocaleString()}</span>
                      </div>
                    ) : null}
                    <div className="flex justify-between font-bold text-sm text-gray-900 pt-2 border-t border-gray-200">
                      <span>Total Amount Payable</span>
                      <span className="font-mono text-[#0071E3] text-base">৳{Number(orderConfirmed.totalBDT).toLocaleString()}</span>
                    </div>
                  </div>
                </div>

                {/* Official Guarantee Footer */}
                <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 text-[11px] text-gray-600 space-y-1">
                  <div className="font-semibold text-gray-800 flex items-center gap-1.5">
                    <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
                    <span>Official 1-Year Hardware Warranty &bull; 7-Day Replacement Guarantee</span>
                  </div>
                  <p className="text-gray-500">
                    This cash memo acts as proof of purchase for manufacturer service and RMA claims under NEXORA Technologies.
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    );
  }

  if (cart.length === 0) {
    return (
      <div className="max-w-2xl mx-auto px-4 pt-36 pb-24 text-center bg-[#F7F4EE]">
        <div className="rounded-3xl p-12 bg-white border border-black/[0.08] shadow-sm space-y-4">
          <Truck className="w-12 h-12 text-slate-400 mx-auto" />
          <h2 className="text-2xl font-semibold text-[#1D1D1F]">Your Bag is Empty</h2>
          <p className="text-sm text-[#6E6E73]">
            Select a bespoke gadget from our showroom before proceeding to checkout.
          </p>
          <Link
            href="/explore"
            className="inline-block mt-4 px-6 py-2.5 rounded-full bg-[#0071E3] text-white font-medium text-xs tracking-wider uppercase"
          >
            Explore Hardware
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto px-4 pt-28 sm:pt-32 pb-20 sm:pb-24 bg-[#F7F4EE]">
      <div className="text-center max-w-xl mx-auto mb-8 sm:mb-10">
        <h1 className="text-3xl sm:text-4xl font-semibold text-[#1D1D1F] tracking-tight">
          Checkout
        </h1>
        <p className="text-xs text-[#6E6E73] mt-1">
          Complete your hardware reservation with local Bangladeshi or international payment.
        </p>
      </div>

      <form onSubmit={handlePlaceOrder} className="grid grid-cols-1 lg:grid-cols-12 gap-6 sm:gap-10">
        
        {/* Customer & Delivery Form */}
        <div className="lg:col-span-7 space-y-6">
          <div className="p-5 sm:p-8 rounded-2xl sm:rounded-3xl bg-white border border-black/[0.06] shadow-sm space-y-5 sm:space-y-6">
            <div className="flex items-center justify-between">
              <h3 className="text-base font-semibold text-[#1D1D1F] flex items-center gap-2">
                <Truck className="w-5 h-5 text-[#0071E3]" />
                <span>1. Delivery Information</span>
              </h3>
              {user ? (
                <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-50 text-emerald-700 text-xs font-semibold">
                  <UserCheck className="w-3.5 h-3.5" />
                  <span>Logged in as {user.name.split(' ')[0]}</span>
                </div>
              ) : (
                <button
                  type="button"
                  onClick={() => setIsAuthModalOpen(true)}
                  className="text-xs text-[#0071E3] hover:underline font-medium"
                >
                  Sign In for 1-Click Fill
                </button>
              )}
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-medium text-[#1D1D1F] mb-1">Full Name *</label>
                <input
                  type="text"
                  required
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="e.g. Asif Mahmud"
                  className="w-full px-3.5 sm:px-4 py-3 sm:py-2.5 rounded-xl bg-[#F5F5F7] border border-black/10 text-base sm:text-sm text-[#1D1D1F] focus:outline-none focus:border-[#0071E3]"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-[#1D1D1F] mb-1">Phone Number (Required for BD) *</label>
                <input
                  type="tel"
                  required
                  value={phone}
                  onChange={(e) => setPhone(e.target.value)}
                  placeholder="017XXXXXXXX"
                  className="w-full px-3.5 sm:px-4 py-3 sm:py-2.5 rounded-xl bg-[#F5F5F7] border border-black/10 text-base sm:text-sm text-[#1D1D1F] focus:outline-none focus:border-[#0071E3]"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-medium text-[#1D1D1F] mb-1">Email (For e-Receipt)</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="name@domain.com"
                className="w-full px-3.5 sm:px-4 py-3 sm:py-2.5 rounded-xl bg-[#F5F5F7] border border-black/10 text-base sm:text-sm text-[#1D1D1F] focus:outline-none focus:border-[#0071E3]"
              />
            </div>

            <div>
              <div className="flex items-center justify-between mb-2">
                <label className="block text-xs font-medium text-[#1D1D1F]">Delivery Address *</label>
                <div className="inline-flex rounded-lg border border-black/10 bg-[#F5F5F7] p-0.5">
                  <button
                    type="button"
                    onClick={() => setAddressType('Home')}
                    className={`flex items-center gap-1.5 px-3 py-1 rounded-md text-xs font-medium transition-all ${
                      addressType === 'Home'
                        ? 'bg-white text-[#1D1D1F] shadow-xs'
                        : 'text-[#86868B] hover:text-[#1D1D1F]'
                    }`}
                  >
                    <Home className="w-3.5 h-3.5 text-[#0071E3]" />
                    <span>Home</span>
                  </button>
                  <button
                    type="button"
                    onClick={() => setAddressType('Office')}
                    className={`flex items-center gap-1.5 px-3 py-1 rounded-md text-xs font-medium transition-all ${
                      addressType === 'Office'
                        ? 'bg-white text-[#1D1D1F] shadow-xs'
                        : 'text-[#86868B] hover:text-[#1D1D1F]'
                    }`}
                  >
                    <Building className="w-3.5 h-3.5 text-[#0071E3]" />
                    <span>Office</span>
                  </button>
                </div>
              </div>
              <textarea
                rows={3}
                required
                value={address}
                onChange={(e) => setAddress(e.target.value)}
                placeholder={addressType === 'Home' ? "Apartment, Road, House, Area, City" : "Company Name, Office / Floor / Suite, Road, Area, City"}
                className="w-full px-3.5 sm:px-4 py-3 sm:py-2.5 rounded-xl bg-[#F5F5F7] border border-black/10 text-base sm:text-sm text-[#1D1D1F] focus:outline-none focus:border-[#0071E3]"
              />
            </div>

            {/* Delivery Zone Selector */}
            <div className="pt-2 border-t border-black/[0.06]">
              <div className="flex items-center justify-between mb-2">
                <label className="block text-xs font-medium text-[#1D1D1F]">Shipping Destination Zone *</label>
                <span className="text-[#0071E3] font-semibold text-[11px]">Official Secured Express Courier</span>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-2.5">
                {[
                  { id: 'dhaka', label: 'Dhaka Metro', fee: 70, time: '24-48 Hours' },
                  { id: 'greater_dhaka', label: 'Greater Dhaka', fee: 100, time: '48 Hours' },
                  { id: 'outside_dhaka', label: 'Outside Dhaka', fee: 140, time: '2-3 Days Nationwide' },
                ].map((z) => (
                  <button
                    key={z.id}
                    type="button"
                    onClick={() => setDeliveryZone(z.id as any)}
                    className={`p-3 rounded-xl border text-left transition-all ${
                      deliveryZone === z.id
                        ? 'border-[#0071E3] bg-[#0071E3]/5 text-[#1D1D1F] shadow-xs'
                        : 'border-black/10 bg-[#F5F5F7] text-[#86868B] hover:text-[#1D1D1F]'
                    }`}
                  >
                    <div className="flex items-center justify-between text-xs font-semibold">
                      <span className={deliveryZone === z.id ? 'text-[#0071E3]' : 'text-[#1D1D1F]'}>{z.label}</span>
                      <span className="text-[#1D1D1F]">৳{z.fee}</span>
                    </div>
                    <div className="text-[10px] text-[#86868B] mt-0.5">{z.time}</div>
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Payment Method Selector */}
          <div className="p-5 sm:p-8 rounded-2xl sm:rounded-3xl bg-white border border-black/[0.06] shadow-sm space-y-5 sm:space-y-6">
            <h3 className="text-base font-semibold text-[#1D1D1F] flex items-center gap-2">
              <CreditCard className="w-5 h-5 text-[#0071E3]" />
              <span>2. Payment Option</span>
            </h3>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {[
                { id: 'bKash', label: 'bKash (বিকাশ)', desc: 'Mobile Banking Transfer', icon: Smartphone },
                { id: 'Nagad', label: 'Nagad (নগদ)', desc: 'Mobile Banking', icon: Smartphone },
                { id: 'Cash on Delivery', label: 'Cash on Delivery (COD)', desc: 'Pay when receiving package', icon: Truck },
                { id: 'Bank Transfer', label: 'Bank Wire', desc: 'Direct Bangladesh Bank Account', icon: CreditCard },
                { id: 'Credit/Debit Card', label: 'Card (Visa/Mastercard)', desc: 'Global card checkout', icon: CreditCard },
              ].map(method => (
                <button
                  type="button"
                  key={method.id}
                  onClick={() => setPaymentMethod(method.id as any)}
                  className={`p-3.5 sm:p-4 rounded-xl sm:rounded-2xl text-left border transition-all ${
                    paymentMethod === method.id
                      ? 'border-[#0071E3] bg-[#0071E3]/5 text-[#1D1D1F] ring-1 ring-[#0071E3]'
                      : 'border-black/10 bg-white text-slate-500 hover:border-black/20'
                  }`}
                >
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-semibold text-sm text-[#1D1D1F]">{method.label}</span>
                    <method.icon className="w-4 h-4 text-[#0071E3]" />
                  </div>
                  <span className="text-xs text-[#86868B] block">{method.desc}</span>
                </button>
              ))}
            </div>

            {/* bKash / Nagad Guidance Box */}
            {(paymentMethod === 'bKash' || paymentMethod === 'Nagad') && (
              <div className="p-4 rounded-2xl bg-[#F5F5F7] border border-black/10 space-y-2 text-xs">
                <p className="font-semibold text-[#1D1D1F]">
                  Send Money / Payment to Official {paymentMethod} Number:
                </p>
                <div className="flex items-center gap-2 font-mono text-[#0071E3] font-bold text-sm">
                  <span>+880 1640-026177</span>
                  <span className="text-[10px] text-[#86868B] font-sans">(Personal/Merchant)</span>
                </div>
                <div>
                  <label className="block text-[11px] text-[#1D1D1F] mb-1 mt-2">
                    Enter {paymentMethod} Transaction ID (TrxID) *
                  </label>
                  <input
                    type="text"
                    required
                    value={transactionId}
                    onChange={(e) => setTransactionId(e.target.value)}
                    placeholder="e.g. BK9X82LA71"
                    className="w-full px-3 py-2 rounded-lg bg-white border border-black/10 text-[#1D1D1F] text-xs font-mono uppercase focus:outline-none focus:border-[#0071E3]"
                  />
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Order Summary Column */}
        <div className="lg:col-span-5">
          <div className="p-5 sm:p-8 rounded-2xl sm:rounded-3xl bg-white border border-black/[0.06] shadow-sm space-y-5 sm:space-y-6 sticky top-28">
            <h3 className="text-base font-semibold text-[#1D1D1F]">Order Summary</h3>

            <div className="space-y-4 max-h-72 overflow-y-auto pr-2">
              {cart.map(item => (
                <div key={item.product.id} className="flex items-center gap-3">
                  <div className="relative w-12 h-12 rounded-xl overflow-hidden bg-[#F5F5F7] flex-shrink-0 border border-black/[0.04]">
                    <Image src={item.product.image} alt={item.product.name} fill className="object-cover" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <h5 className="text-xs font-medium text-[#1D1D1F] truncate">{item.product.name}</h5>
                    <span className="text-[11px] text-[#86868B] font-mono">Qty: {item.quantity}</span>
                  </div>
                  <span className="text-xs font-mono text-[#1D1D1F] font-bold flex items-baseline">
                    <span className="text-[10px] font-normal text-gray-500 mr-1">৳</span>
                    <span>{(item.product.priceBDT * item.quantity).toLocaleString()}</span>
                  </span>
                </div>
              ))}
            </div>

            {/* Promo Code Input */}
            <div className="pt-3 border-t border-black/[0.06]">
              {appliedCoupon ? (
                <div className="flex items-center justify-between p-3 rounded-xl bg-emerald-50 border border-emerald-200">
                  <div className="flex items-center gap-2">
                    <Tag className="w-4 h-4 text-emerald-600" />
                    <div>
                      <span className="font-mono text-xs font-bold text-emerald-800 tracking-wider">
                        {appliedCoupon.code}
                      </span>
                      <p className="text-[10px] text-emerald-600">{appliedCoupon.description}</p>
                    </div>
                  </div>
                  <button
                    type="button"
                    onClick={() => setAppliedCoupon(null)}
                    className="p-1 text-emerald-600 hover:text-emerald-800 rounded-lg hover:bg-emerald-100 transition-colors"
                    title="Remove Promo Code"
                  >
                    <X className="w-3.5 h-3.5" />
                  </button>
                </div>
              ) : (
                <div className="space-y-1.5">
                  <div className="flex gap-2">
                    <input
                      type="text"
                      value={couponInput}
                      onChange={(e) => setCouponInput(e.target.value.toUpperCase())}
                      placeholder="Promo Code (e.g. NEXORA10)"
                      className="flex-1 px-3 py-2 rounded-xl bg-[#F5F5F7] border border-black/10 text-xs font-mono uppercase focus:outline-none focus:border-[#0071E3]"
                    />
                    <button
                      type="button"
                      disabled={couponLoading || !couponInput.trim()}
                      onClick={handleApplyCoupon}
                      className="px-4 py-2 rounded-xl bg-slate-900 text-white text-xs font-medium hover:bg-black disabled:opacity-50 transition-colors"
                    >
                      {couponLoading ? 'Checking...' : 'Apply'}
                    </button>
                  </div>
                  {couponMsg && (
                    <p className={`text-[11px] ${couponMsg.type === 'success' ? 'text-emerald-600' : 'text-rose-500'}`}>
                      {couponMsg.text}
                    </p>
                  )}
                </div>
              )}
            </div>

            <div className="space-y-2 pt-4 border-t border-black/[0.06] text-xs">
              <div className="flex justify-between text-[#86868B]">
                <span>Subtotal</span>
                <span className="font-mono text-[#1D1D1F] flex items-baseline">
                  <span className="text-[10px] font-normal text-gray-500 mr-1">৳</span>
                  <span>{rawSubtotal.toLocaleString()}</span>
                </span>
              </div>
              {discountBDT > 0 && (
                <div className="flex justify-between text-emerald-600 font-medium">
                  <span>Promo Discount ({appliedCoupon?.code})</span>
                  <span className="font-mono flex items-baseline">
                    <span className="text-[10px] mr-1">-৳</span>
                    <span>{discountBDT.toLocaleString()}</span>
                  </span>
                </div>
              )}
              <div className="flex justify-between text-[#86868B]">
                <span>Shipping ({deliveryZone === 'outside_dhaka' ? 'Nationwide' : deliveryZone === 'greater_dhaka' ? 'Greater Dhaka' : 'Dhaka Metro'})</span>
                <span className="font-mono text-[#1D1D1F] flex items-baseline">
                  {deliveryFee === 0 ? (
                    <span className="text-emerald-600 font-bold">FREE</span>
                  ) : (
                    <>
                      <span className="text-[10px] font-normal text-gray-500 mr-1">৳</span>
                      <span>{deliveryFee}</span>
                    </>
                  )}
                </span>
              </div>
              <div className="flex justify-between text-sm font-bold text-[#1D1D1F] pt-2 border-t border-black/[0.06]">
                <span>Total Amount</span>
                <span className="font-mono text-[#0071E3] text-base flex items-baseline">
                  <span className="text-xs font-normal text-[#0071E3]/70 mr-1">৳</span>
                  <span>{grandTotal.toLocaleString()}</span>
                </span>
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3.5 rounded-full bg-[#0071E3] hover:bg-[#0077ED] text-white font-medium text-sm tracking-wide transition-all shadow-sm flex items-center justify-center gap-2"
            >
              <span>{loading ? 'Confirming...' : 'Place Order'}</span>
              <ArrowRight className="w-4 h-4" />
            </button>

            <div className="text-center text-[11px] text-[#86868B]">
              <ShieldCheck className="w-3.5 h-3.5 inline mr-1 text-emerald-600" />
              <span>Encrypted checkout. Guaranteed genuine hardware.</span>
            </div>
          </div>
        </div>
      </form>
    </div>
  );
}

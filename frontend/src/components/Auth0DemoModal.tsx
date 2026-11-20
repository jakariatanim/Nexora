'use client';

import React, { useState } from 'react';
import Image from 'next/image';
import { 
  ShieldCheck, 
  X, 
  Lock, 
  Key, 
  Smartphone, 
  Fingerprint, 
  Mail, 
  CheckCircle2, 
  ExternalLink, 
  Sparkles, 
  Zap, 
  ArrowRight,
  RefreshCw,
  Users,
  Eye,
  FileCode
} from 'lucide-react';
import { useCart } from '../lib/cartContext';
import { User } from '../lib/types';
import { AUTH0_CONFIG } from '../lib/auth0-config';

interface Auth0DemoModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccessLogin?: (user: User) => void;
}

export const Auth0DemoModal: React.FC<Auth0DemoModalProps> = ({
  isOpen,
  onClose,
  onSuccessLogin,
}) => {
  const { setUser } = useCart();
  const [activeTab, setActiveTab] = useState<'demo' | 'benefits' | 'setup'>('demo');
  const [isSimulating, setIsSimulating] = useState(false);
  const [selectedProvider, setSelectedProvider] = useState<'google' | 'apple' | 'passkey' | 'email'>('google');
  const [simulatedEmail, setSimulatedEmail] = useState('jakariatanim03@gmail.com');
  const [simulatedName, setSimulatedName] = useState('Jakaria Tanim');
  const [step, setStep] = useState<'prompt' | 'authorizing' | 'success'>('prompt');

  if (!isOpen) return null;

  const handleSimulateLogin = () => {
    setIsSimulating(true);
    setStep('authorizing');

    setTimeout(() => {
      const mockUser: User = {
        id: `usr-auth0-${Date.now()}`,
        name: simulatedName,
        email: simulatedEmail,
        phone: '+8801700000001',
        tier: 'NEXORA VIP (Auth0 Verified)',
      };

      setUser(mockUser);
      localStorage.setItem('nexora_user', JSON.stringify(mockUser));
      if (onSuccessLogin) onSuccessLogin(mockUser);
      setStep('success');
      setIsSimulating(false);
    }, 1500);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-4 bg-black/75 backdrop-blur-md animate-fade-in">
      <div className="relative w-full max-w-2xl bg-white dark:bg-[#0E1322] border border-black/10 dark:border-white/15 rounded-3xl shadow-2xl overflow-hidden flex flex-col max-h-[92vh]">
        
        {/* Header */}
        <div className="px-6 py-4 bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white flex items-center justify-between border-b border-white/10">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-white/10 border border-white/20 flex items-center justify-center p-2 backdrop-blur-md">
              <ShieldCheck className="w-6 h-6 text-indigo-400" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-base sm:text-lg font-bold tracking-tight">
                  Auth0 Identity Platform Demo
                </h2>
                <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-indigo-500/30 text-indigo-200 border border-indigo-400/30">
                  {AUTH0_CONFIG.isConfigured ? 'Production Live' : 'Interactive Demo Mode'}
                </span>
              </div>
              <p className="text-xs text-slate-300">
                Enterprise Cloud Authentication & Social SSO for NEXORA
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-full bg-white/10 hover:bg-white/20 text-slate-300 hover:text-white transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Tab Navigation */}
        <div className="flex border-b border-black/10 dark:border-white/10 bg-slate-50 dark:bg-white/[0.02] px-6 text-xs sm:text-sm font-semibold">
          <button
            onClick={() => setActiveTab('demo')}
            className={`py-3 px-4 border-b-2 transition-all flex items-center gap-2 ${
              activeTab === 'demo'
                ? 'border-indigo-600 text-indigo-600 dark:text-indigo-400'
                : 'border-transparent text-slate-500 hover:text-slate-900 dark:hover:text-white'
            }`}
          >
            <Sparkles className="w-4 h-4" />
            <span>১. লাইভ ডেমো (Interactive Test)</span>
          </button>
          <button
            onClick={() => setActiveTab('benefits')}
            className={`py-3 px-4 border-b-2 transition-all flex items-center gap-2 ${
              activeTab === 'benefits'
                ? 'border-indigo-600 text-indigo-600 dark:text-indigo-400'
                : 'border-transparent text-slate-500 hover:text-slate-900 dark:hover:text-white'
            }`}
          >
            <Zap className="w-4 h-4" />
            <span>২. বাস্তব সুবিধা ও উদাহরণ</span>
          </button>
          <button
            onClick={() => setActiveTab('setup')}
            className={`py-3 px-4 border-b-2 transition-all flex items-center gap-2 ${
              activeTab === 'setup'
                ? 'border-indigo-600 text-indigo-600 dark:text-indigo-400'
                : 'border-transparent text-slate-500 hover:text-slate-900 dark:hover:text-white'
            }`}
          >
            <FileCode className="w-4 h-4" />
            <span>৩. লাইভ সেটআপ নিয়ম</span>
          </button>
        </div>

        {/* Content Area */}
        <div className="p-6 overflow-y-auto space-y-6 text-sm flex-1">
          
          {/* TAB 1: INTERACTIVE DEMO */}
          {activeTab === 'demo' && (
            <div className="space-y-5">
              <div className="p-4 rounded-2xl bg-indigo-50/70 dark:bg-indigo-950/30 border border-indigo-200/80 dark:border-indigo-800/40 text-xs sm:text-sm text-indigo-950 dark:text-indigo-200">
                <span className="font-bold">💡 টেস্ট করুন:</span> এটি দেখায় কাস্টমার যখন ওয়েবসাইটের <strong>"Continue with Google"</strong> বা <strong>"Apple ID"</strong> চাপবে, তখন Auth0 ব্যাকগ্রাউন্ডে কীভাবে টোকেন ভেরিফাই করে এবং ১-ক্লিকে কাস্টমারকে সাইন-ইন করায়।
              </div>

              {step === 'prompt' && (
                <div className="p-5 rounded-2xl bg-slate-50 dark:bg-white/5 border border-black/10 dark:border-white/10 space-y-4">
                  <div className="text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider">
                    লগইন মেথড নির্বাচন করুন:
                  </div>

                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
                    <button
                      type="button"
                      onClick={() => {
                        setSelectedProvider('google');
                        setSimulatedEmail('jakariatanim03@gmail.com');
                        setSimulatedName('Jakaria Tanim');
                      }}
                      className={`p-3 rounded-2xl border text-center transition-all ${
                        selectedProvider === 'google'
                          ? 'border-indigo-600 bg-indigo-50/50 dark:bg-indigo-900/30 text-indigo-700 dark:text-indigo-300 font-bold shadow-sm'
                          : 'border-black/10 dark:border-white/10 hover:bg-slate-100 dark:hover:bg-white/10 text-slate-700 dark:text-slate-300'
                      }`}
                    >
                      <div className="text-base mb-1">🌐</div>
                      <div className="text-xs font-semibold">Google OAuth</div>
                    </button>

                    <button
                      type="button"
                      onClick={() => {
                        setSelectedProvider('apple');
                        setSimulatedEmail('tanim.apple@icloud.com');
                        setSimulatedName('Jakaria Tanim (Apple)');
                      }}
                      className={`p-3 rounded-2xl border text-center transition-all ${
                        selectedProvider === 'apple'
                          ? 'border-indigo-600 bg-indigo-50/50 dark:bg-indigo-900/30 text-indigo-700 dark:text-indigo-300 font-bold shadow-sm'
                          : 'border-black/10 dark:border-white/10 hover:bg-slate-100 dark:hover:bg-white/10 text-slate-700 dark:text-slate-300'
                      }`}
                    >
                      <div className="text-base mb-1">🍎</div>
                      <div className="text-xs font-semibold">Apple ID</div>
                    </button>

                    <button
                      type="button"
                      onClick={() => {
                        setSelectedProvider('passkey');
                        setSimulatedEmail('biometric@nexora.com');
                        setSimulatedName('Passkey User');
                      }}
                      className={`p-3 rounded-2xl border text-center transition-all ${
                        selectedProvider === 'passkey'
                          ? 'border-indigo-600 bg-indigo-50/50 dark:bg-indigo-900/30 text-indigo-700 dark:text-indigo-300 font-bold shadow-sm'
                          : 'border-black/10 dark:border-white/10 hover:bg-slate-100 dark:hover:bg-white/10 text-slate-700 dark:text-slate-300'
                      }`}
                    >
                      <div className="text-base mb-1">🔑</div>
                      <div className="text-xs font-semibold">Passkey / 2FA</div>
                    </button>

                    <button
                      type="button"
                      onClick={() => {
                        setSelectedProvider('email');
                        setSimulatedEmail('customer@gmail.com');
                        setSimulatedName('Regular Customer');
                      }}
                      className={`p-3 rounded-2xl border text-center transition-all ${
                        selectedProvider === 'email'
                          ? 'border-indigo-600 bg-indigo-50/50 dark:bg-indigo-900/30 text-indigo-700 dark:text-indigo-300 font-bold shadow-sm'
                          : 'border-black/10 dark:border-white/10 hover:bg-slate-100 dark:hover:bg-white/10 text-slate-700 dark:text-slate-300'
                      }`}
                    >
                      <div className="text-base mb-1">✉️</div>
                      <div className="text-xs font-semibold">Passwordless</div>
                    </button>
                  </div>

                  <div className="space-y-2 pt-2">
                    <div>
                      <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                        টেস্ট কাস্টমার নাম:
                      </label>
                      <input
                        type="text"
                        value={simulatedName}
                        onChange={(e) => setSimulatedName(e.target.value)}
                        className="w-full px-3.5 py-2.5 rounded-xl border border-black/10 dark:border-white/15 bg-white dark:bg-black/30 text-sm font-semibold text-slate-900 dark:text-white"
                      />
                    </div>
                    <div>
                      <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                        টেস্ট ইমেইল এড্রেস:
                      </label>
                      <input
                        type="email"
                        value={simulatedEmail}
                        onChange={(e) => setSimulatedEmail(e.target.value)}
                        className="w-full px-3.5 py-2.5 rounded-xl border border-black/10 dark:border-white/15 bg-white dark:bg-black/30 text-sm font-semibold text-slate-900 dark:text-white"
                      />
                    </div>
                  </div>

                  <button
                    type="button"
                    onClick={handleSimulateLogin}
                    disabled={isSimulating}
                    className="w-full py-3.5 rounded-2xl bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-sm tracking-wide shadow-md transition-all active:scale-95 flex items-center justify-center gap-2"
                  >
                    <ShieldCheck className="w-5 h-5" />
                    <span>Auth0 দিয়ে ১-ক্লিক লগইন টেস্ট করুন</span>
                  </button>
                </div>
              )}

              {step === 'authorizing' && (
                <div className="p-8 rounded-2xl bg-slate-50 dark:bg-white/5 border border-black/10 dark:border-white/10 text-center space-y-4">
                  <div className="inline-block animate-spin p-3 rounded-full bg-indigo-100 dark:bg-indigo-900/50 text-indigo-600">
                    <RefreshCw className="w-8 h-8" />
                  </div>
                  <h3 className="text-base font-bold text-slate-900 dark:text-white">
                    Connecting to Auth0 Universal Login...
                  </h3>
                  <p className="text-xs text-slate-500 max-w-sm mx-auto font-mono">
                    Verifying OAuth2 / OIDC claims • Validating JWT Token Signature • Creating Secure Edge Session...
                  </p>
                </div>
              )}

              {step === 'success' && (
                <div className="p-6 rounded-2xl bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-300 dark:border-emerald-800 text-center space-y-4 animate-fade-in">
                  <div className="w-12 h-12 mx-auto rounded-full bg-emerald-100 dark:bg-emerald-900/50 text-emerald-600 flex items-center justify-center">
                    <CheckCircle2 className="w-7 h-7" />
                  </div>
                  <div className="space-y-1">
                    <h3 className="text-lg font-bold text-emerald-900 dark:text-emerald-200">
                      সফলভাবে Auth0 লগইন সম্পন্ন হয়েছে! 🎉
                    </h3>
                    <p className="text-xs text-emerald-700 dark:text-emerald-300">
                      কাস্টমার <strong className="font-bold">{simulatedName}</strong> ({simulatedEmail}) হিসেবে নেক্সরায় ভেরিফাইড সেশন তৈরি হয়েছে।
                    </p>
                  </div>

                  <div className="p-3 rounded-xl bg-white/70 dark:bg-white/5 border border-emerald-200 dark:border-white/10 text-left text-xs font-mono space-y-1 text-slate-700 dark:text-slate-300">
                    <div>🔒 <strong>Auth Status:</strong> Authenticated via Auth0 OIDC</div>
                    <div>🛡️ <strong>Email Verified:</strong> true (Signed by Google/Apple)</div>
                    <div>💎 <strong>Role:</strong> NEXORA VIP Customer</div>
                  </div>

                  <div className="flex gap-2 justify-center pt-2">
                    <button
                      type="button"
                      onClick={() => setStep('prompt')}
                      className="px-4 py-2 rounded-xl border border-emerald-400 text-xs font-semibold text-emerald-800 dark:text-emerald-300 hover:bg-emerald-100"
                    >
                      আবার টেস্ট করুন
                    </button>
                    <button
                      type="button"
                      onClick={onClose}
                      className="px-5 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-xs font-bold text-white shadow"
                    >
                      ওয়েবসাইটে ফিরে যান
                    </button>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* TAB 2: BENEFITS & EXAMPLES */}
          {activeTab === 'benefits' && (
            <div className="space-y-4">
              <h3 className="text-sm font-bold text-slate-900 dark:text-white uppercase tracking-wider">
                Auth0 ব্যবহার করলে নেক্সরা ওয়েবসাইটে কী কী বিশাল সুবিধা পাওয়া যাবে:
              </h3>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div className="p-4 rounded-2xl bg-slate-50 dark:bg-white/5 border border-black/5 dark:border-white/10 space-y-2">
                  <div className="flex items-center gap-2 text-indigo-600 dark:text-indigo-400 font-bold text-xs">
                    <Sparkles className="w-4 h-4" />
                    <span>১. ১-ক্লিকে গুগল ও অ্যাপল সাইন-ইন</span>
                  </div>
                  <p className="text-xs text-slate-600 dark:text-slate-300 leading-relaxed">
                    <strong>বাস্তব উদাহরণ:</strong> কাস্টমারকে কোনো ফর্ম পূরণ করতে হবে না। শুধু "Continue with Google" চাপলেই মোবাইল বা ল্যাপটপের জিমেইল দিয়ে সরাসরি একাউন্ট তৈরি ও লগইন হয়ে যাবে। এতে কাস্টমার কেনার আগ্রহ হারায় না।
                  </p>
                </div>

                <div className="p-4 rounded-2xl bg-slate-50 dark:bg-white/5 border border-black/5 dark:border-white/10 space-y-2">
                  <div className="flex items-center gap-2 text-emerald-600 dark:text-emerald-400 font-bold text-xs">
                    <ShieldCheck className="w-4 h-4" />
                    <span>২. জিরো পাসওয়ার্ড হ্যাকিং রিস্ক</span>
                  </div>
                  <p className="text-xs text-slate-600 dark:text-slate-300 leading-relaxed">
                    <strong>বাস্তব উদাহরণ:</strong> কোনো হ্যাকার যদি আপনার ডাটাবেস হ্যাক করার চেষ্টাও করে, কাস্টমারের কোনো পাসওয়ার্ড সেখানে থাকবে না! সমস্ত পাসওয়ার্ড ও ক্রেডেনশিয়াল Auth0 এর ব্যাংক-গ্রেড সিকিউর ভল্টে থাকবে।
                  </p>
                </div>

                <div className="p-4 rounded-2xl bg-slate-50 dark:bg-white/5 border border-black/5 dark:border-white/10 space-y-2">
                  <div className="flex items-center gap-2 text-amber-600 dark:text-amber-400 font-bold text-xs">
                    <Mail className="w-4 h-4" />
                    <span>৩. অটোমেটিক ইমেইল ভেরিফিকেশন</span>
                  </div>
                  <p className="text-xs text-slate-600 dark:text-slate-300 leading-relaxed">
                    <strong>বাস্তব উদাহরণ:</strong> কেউ পাসওয়ার্ড ভুলে গেলে "Forgot Password" চাপলে Auth0 নিজে থেকেই প্রফেশনাল রিসেট ইমেইল পাঠিয়ে দেবে। আপনাকে আলাদা কোনো মেইল সার্ভার কিনতে বা কনফিগার করতে হবে না।
                  </p>
                </div>

                <div className="p-4 rounded-2xl bg-slate-50 dark:bg-white/5 border border-black/5 dark:border-white/10 space-y-2">
                  <div className="flex items-center gap-2 text-rose-600 dark:text-rose-400 font-bold text-xs">
                    <Fingerprint className="w-4 h-4" />
                    <span>৪. ফেস আইডি ও ফিঙ্গারপ্রিন্ট (Passkeys)</span>
                  </div>
                  <p className="text-xs text-slate-600 dark:text-slate-300 leading-relaxed">
                    <strong>বাস্তব উদাহরণ:</strong> আইফোন বা অ্যান্ড্রয়েড ইউজাররা তাদের ফোনের ফেস আনলক বা ফিঙ্গারপ্রিন্ট দিয়ে এক নিমেষে লগইন করে তাদের ফ্ল্যাগশিপ গ্যাজেট অর্ডার ট্র্যাক করতে পারবে।
                  </p>
                </div>
              </div>

              <div className="p-4 rounded-2xl bg-emerald-50/70 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-800 text-xs text-emerald-900 dark:text-emerald-200">
                💰 <strong>খরচ কত?</strong> Auth0 প্রতি মাসে <strong>২৫,০০০ (25,000) জন অ্যাক্টিভ ভিজিটর পর্যন্ত একদম ফ্রি</strong> (Free Forever)। অর্থাৎ নেক্সরার মতো স্টার্টআপের জন্য কোনো টাকা দিতে হয় না।
              </div>
            </div>
          )}

          {/* TAB 3: SETUP INSTRUCTIONS */}
          {activeTab === 'setup' && (
            <div className="space-y-4">
              <h3 className="text-sm font-bold text-slate-900 dark:text-white uppercase tracking-wider">
                রিয়েল প্রোডাকশন অ্যাকাউন্ট কানেক্ট করার নিয়ম:
              </h3>

              <ol className="list-decimal list-inside space-y-2.5 text-xs text-slate-600 dark:text-slate-300">
                <li>
                  <strong className="text-slate-900 dark:text-white">auth0.com-এ সাইন-আপ:</strong> <a href="https://auth0.com" target="_blank" rel="noreferrer" className="text-indigo-600 dark:text-indigo-400 underline font-semibold">auth0.com</a> এ গিয়ে ফ্রিতে সাইন ইন করুন।
                </li>
                <li>
                  <strong className="text-slate-900 dark:text-white">Applications তৈরি:</strong> ড্যাশবোর্ড থেকে <em>Applications &gt; Applications &gt; Create Application</em> এ ক্লিক করুন এবং <strong>Single Page Web Applications</strong> সিলেক্ট করুন।
                </li>
                <li>
                  <strong className="text-slate-900 dark:text-white">Callback URL বসান:</strong> Settings ট্যাবে নিচের লিংকগুলো <em>Allowed Callback URLs</em> ও <em>Allowed Logout URLs</em> এ দিন:
                  <div className="p-2 rounded-xl bg-slate-100 dark:bg-white/5 font-mono text-[11px] mt-1 break-all">
                    https://nexora.pages.dev, https://nexorabd.pages.dev, http://localhost:3000
                  </div>
                </li>
                <li>
                  <strong className="text-slate-900 dark:text-white">Keys সংগ্রহ ও আমাকে প্রদান:</strong> Settings পেজের উপর থেকে <strong>Domain</strong> (যেমন `dev-xyz.us.auth0.com`) এবং <strong>Client ID</strong> কপি করে আমাকে দিয়ে দিন।
                </li>
              </ol>

              <div className="p-3 rounded-xl bg-slate-100 dark:bg-white/5 border border-black/5 dark:border-white/10 text-xs font-mono text-slate-700 dark:text-slate-300">
                🚀 চাবিকাঠি দুটো পেলেই আমি সাথে সাথে আপনার লাইভ ওয়েবসাইটে আসল Auth0 Google/Apple সাইন-ইন ফুল কানেক্ট করে দেব!
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="px-6 py-3.5 bg-slate-50 dark:bg-white/[0.03] border-t border-black/10 dark:border-white/10 flex items-center justify-between text-xs text-slate-500">
          <span>Protected by Auth0 by Okta • OpenID Connect (OIDC)</span>
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-xl bg-slate-200 dark:bg-white/10 hover:bg-slate-300 dark:hover:bg-white/20 text-slate-800 dark:text-white font-semibold transition-colors"
          >
            বন্ধ করুন (Close)
          </button>
        </div>

      </div>
    </div>
  );
};

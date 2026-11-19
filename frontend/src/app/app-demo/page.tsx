'use client';

import React, { useState, useEffect, useRef } from 'react';
import Link from 'next/link';
import { 
  Smartphone, 
  RotateCw, 
  RefreshCw, 
  ExternalLink, 
  ChevronLeft, 
  Compass, 
  Home, 
  Package, 
  ShoppingBag, 
  CheckCircle2, 
  Sparkles, 
  Layers, 
  QrCode,
  Info,
  Sliders,
  Laptop
} from 'lucide-react';

interface DevicePreset {
  id: string;
  name: string;
  brand: string;
  width: number;
  height: number;
  bezel: string;
  radius: string;
  hasDynamicIsland: boolean;
}

const DEVICES: DevicePreset[] = [
  {
    id: 'iphone16pro',
    name: 'iPhone 16 Pro',
    brand: 'Apple',
    width: 393,
    height: 852,
    bezel: 'p-3 bg-gradient-to-b from-[#2E3138] via-[#1C1E24] to-[#121316] ring-1 ring-white/20 shadow-[0_25px_70px_rgba(0,0,0,0.65)]',
    radius: 'rounded-[52px]',
    hasDynamicIsland: true,
  },
  {
    id: 's24ultra',
    name: 'Galaxy S24 Ultra',
    brand: 'Samsung',
    width: 412,
    height: 890,
    bezel: 'p-3 bg-gradient-to-b from-[#3A3F4D] via-[#20242E] to-[#14171E] ring-1 ring-white/15 shadow-[0_25px_70px_rgba(0,0,0,0.65)]',
    radius: 'rounded-[40px]',
    hasDynamicIsland: false,
  },
  {
    id: 'iphonese',
    name: 'Compact Phone',
    brand: 'Compact',
    width: 375,
    height: 720,
    bezel: 'p-3 bg-gradient-to-b from-[#2B2D33] via-[#1B1C20] to-[#0F1012] ring-1 ring-white/15 shadow-[0_20px_50px_rgba(0,0,0,0.55)]',
    radius: 'rounded-[44px]',
    hasDynamicIsland: true,
  },
];

export default function MobileAppDemoPage() {
  const [selectedDevice, setSelectedDevice] = useState<DevicePreset>(DEVICES[0]);
  const [currentPath, setCurrentPath] = useState('/');
  const [iframeKey, setIframeKey] = useState(0);
  const [zoomLevel, setZoomLevel] = useState(0.92);
  const [currentTime, setCurrentTime] = useState('09:41');
  const [showQrModal, setShowQrModal] = useState(false);
  const iframeRef = useRef<HTMLIFrameElement>(null);

  // Live Clock for device status bar
  useEffect(() => {
    const updateTime = () => {
      const now = new Date();
      let hours = now.getHours();
      const minutes = String(now.getMinutes()).padStart(2, '0');
      hours = hours % 12 || 12;
      setCurrentTime(`${hours}:${minutes}`);
    };
    updateTime();
    const timer = setInterval(updateTime, 30000);
    return () => clearInterval(timer);
  }, []);

  const handleReload = () => {
    setIframeKey((prev) => prev + 1);
  };

  const handleNavigate = (path: string) => {
    setCurrentPath(path);
  };

  // QR Code URL for local network testing
  const localNetworkUrl = 'http://10.13.130.250:3000';
  const qrCodeApiUrl = `https://api.qrserver.com/v1/create-qr-code/?size=240x240&data=${encodeURIComponent(localNetworkUrl)}&margin=10`;

  return (
    <div className="min-h-screen bg-[#070B18] text-white flex flex-col font-sans select-none overflow-x-hidden">
      
      {/* Top Studio Control Bar */}
      <header className="border-b border-white/10 bg-[#0B132B]/90 backdrop-blur-xl px-4 lg:px-8 py-3 sticky top-0 z-50 flex items-center justify-between gap-4">
        
        {/* Left: Back & Title */}
        <div className="flex items-center gap-4">
          <Link
            href="/"
            className="flex items-center gap-1.5 text-xs font-semibold px-3 py-1.5 rounded-full bg-white/10 hover:bg-white/20 text-white transition-all"
          >
            <ChevronLeft className="w-4 h-4" />
            <span>Back to Store</span>
          </Link>

          <div className="hidden sm:block border-l border-white/10 pl-4">
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
              <h1 className="text-sm font-bold tracking-tight text-white">NEXORA Mobile App Simulator</h1>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-[#0071E3]/20 text-[#38BDF8] font-medium">
                PWA v1.0
              </span>
            </div>
          </div>
        </div>

        {/* Center: Device Switcher */}
        <div className="flex items-center bg-black/40 p-1 rounded-2xl border border-white/10">
          {DEVICES.map((dev) => (
            <button
              key={dev.id}
              onClick={() => setSelectedDevice(dev)}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-medium transition-all ${
                selectedDevice.id === dev.id
                  ? 'bg-[#0071E3] text-white shadow-md'
                  : 'text-gray-400 hover:text-white'
              }`}
            >
              <Smartphone className="w-3.5 h-3.5" />
              <span>{dev.name}</span>
            </button>
          ))}
        </div>

        {/* Right: Quick Tools */}
        <div className="flex items-center gap-2">
          {/* Zoom Toggle */}
          <div className="hidden md:flex items-center bg-black/40 px-2 py-1 rounded-xl border border-white/10 text-xs text-gray-300 gap-1.5">
            <Sliders className="w-3 h-3 text-[#38BDF8]" />
            <span className="text-[11px] font-mono">{Math.round(zoomLevel * 100)}%</span>
            <button
              onClick={() => setZoomLevel((z) => Math.max(0.7, z - 0.05))}
              className="px-1.5 py-0.5 hover:bg-white/10 rounded"
              title="Zoom Out"
            >
              -
            </button>
            <button
              onClick={() => setZoomLevel((z) => Math.min(1.05, z + 0.05))}
              className="px-1.5 py-0.5 hover:bg-white/10 rounded"
              title="Zoom In"
            >
              +
            </button>
          </div>

          {/* Refresh Frame */}
          <button
            onClick={handleReload}
            className="p-2 rounded-xl bg-white/10 hover:bg-white/20 text-white transition-all"
            title="Reload Phone Screen"
          >
            <RefreshCw className="w-4 h-4" />
          </button>

          {/* Open Real Phone QR */}
          <button
            onClick={() => setShowQrModal(true)}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-gradient-to-r from-[#0071E3] to-[#38BDF8] text-white text-xs font-semibold shadow-md hover:brightness-110 transition-all"
          >
            <QrCode className="w-4 h-4" />
            <span className="hidden sm:inline">Scan on Mobile</span>
          </button>
        </div>
      </header>

      {/* Main Studio Workspace */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-4 lg:p-8 flex flex-col lg:flex-row items-center lg:items-start justify-center gap-8 lg:gap-12">
        
        {/* Left / Center: Interactive Phone Mockup */}
        <div className="flex flex-col items-center">
          
          {/* Quick Page Jump Navigation Tabs */}
          <div className="mb-4 flex items-center gap-2 bg-white/5 border border-white/10 p-1.5 rounded-2xl max-w-sm">
            {[
              { label: 'Store', path: '/', icon: Home },
              { label: 'Explore', path: '/explore', icon: Compass },
              { label: 'Track', path: '/track-order', icon: Package },
              { label: 'Checkout', path: '/checkout', icon: ShoppingBag },
            ].map((route) => {
              const Icon = route.icon;
              const isActive = currentPath === route.path;
              return (
                <button
                  key={route.path}
                  onClick={() => handleNavigate(route.path)}
                  className={`flex items-center gap-1 px-2.5 py-1 rounded-xl text-xs font-medium transition-all ${
                    isActive ? 'bg-white/20 text-white font-bold' : 'text-gray-400 hover:text-white'
                  }`}
                >
                  <Icon className="w-3.5 h-3.5" />
                  <span>{route.label}</span>
                </button>
              );
            })}
          </div>

          {/* Scaled Device Frame Container */}
          <div
            style={{
              transform: `scale(${zoomLevel})`,
              transformOrigin: 'top center',
              transition: 'transform 0.2s ease',
            }}
            className="relative"
          >
            {/* Realistic Smartphone Hardware Mockup */}
            <div
              className={`relative ${selectedDevice.radius} ${selectedDevice.bezel}`}
              style={{
                width: selectedDevice.width + 24,
                height: selectedDevice.height + 24,
              }}
            >
              {/* Outer Edge Metallic Hardware Buttons */}
              <div className="absolute -left-[5px] top-28 w-[3px] h-8 bg-[#4A4E5A] rounded-l-sm" title="Action Button" />
              <div className="absolute -left-[5px] top-40 w-[3px] h-12 bg-[#4A4E5A] rounded-l-sm" title="Volume Up" />
              <div className="absolute -left-[5px] top-56 w-[3px] h-12 bg-[#4A4E5A] rounded-l-sm" title="Volume Down" />
              <div className="absolute -right-[5px] top-36 w-[3px] h-16 bg-[#4A4E5A] rounded-r-sm" title="Power / Lock Button" />

              {/* Inner Screen Bezel */}
              <div
                className={`relative bg-[#0B132B] overflow-hidden ${selectedDevice.radius} border border-black/40`}
                style={{
                  width: selectedDevice.width,
                  height: selectedDevice.height,
                }}
              >
                {/* 1. iOS / Android Native Status Bar */}
                <div className="absolute top-0 left-0 right-0 h-11 z-30 flex items-center justify-between px-7 text-white text-[12px] font-semibold pointer-events-none select-none">
                  {/* Left: Live Time */}
                  <div className="w-14 text-left font-mono">{currentTime}</div>

                  {/* Center: Dynamic Island (Interactive Pill) */}
                  {selectedDevice.hasDynamicIsland && (
                    <div className="relative group pointer-events-auto">
                      <div className="h-[26px] w-[98px] bg-black rounded-full flex items-center justify-between px-2.5 ring-1 ring-white/10 shadow-md transition-all duration-300 group-hover:w-[130px]">
                        <span className="w-2.5 h-2.5 rounded-full bg-[#0071E3] flex-shrink-0"></span>
                        <span className="text-[10px] font-mono text-gray-300 tracking-wider">NEXORA</span>
                        <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 flex-shrink-0 animate-pulse"></span>
                      </div>
                    </div>
                  )}

                  {/* Right: 5G, Wi-Fi & Battery Status */}
                  <div className="w-14 flex items-center justify-end gap-1.5 text-xs text-white">
                    <span className="text-[10px] font-bold">5G</span>
                    <svg className="w-3.5 h-3.5 fill-current" viewBox="0 0 24 24">
                      <path d="M12 3c-4.97 0-9 4.03-9 9 0 2.12.74 4.07 1.97 5.61L12 22l7.03-4.39C20.26 16.07 21 14.12 21 12c0-4.97-4.03-9-9-9zm0 14.5c-3.03 0-5.5-2.47-5.5-5.5S8.97 6.5 12 6.5s5.5 2.47 5.5 5.5-2.47 5.5-5.5 5.5z"/>
                    </svg>
                    <div className="w-5 h-2.5 border border-white/80 rounded-sm p-[1px] flex items-center">
                      <div className="w-full h-full bg-emerald-400 rounded-2xs"></div>
                    </div>
                  </div>
                </div>

                {/* 2. Interactive Scrollable Web App Iframe */}
                <iframe
                  key={`${currentPath}-${iframeKey}`}
                  ref={iframeRef}
                  src={`${currentPath}${currentPath.includes('?') ? '&' : '?'}v=${iframeKey}`}
                  className="w-full h-full border-none pt-9 pb-2 bg-[#F7F4EE] dark:bg-[#070B18]"
                  title="NEXORA Mobile App Frame"
                  style={{
                    width: '100%',
                    height: '100%',
                    overflowY: 'auto',
                    scrollbarWidth: 'thin',
                  }}
                />

                {/* 3. iOS Bottom Home Indicator Bar */}
                <div className="absolute bottom-1.5 left-0 right-0 h-4 flex items-center justify-center z-30 pointer-events-none select-none">
                  <div className="w-32 h-1 bg-black/40 dark:bg-white/60 rounded-full"></div>
                </div>
              </div>
            </div>

            {/* Instruction tooltip right below device */}
            <div className="mt-3 text-center text-xs text-gray-400 flex items-center justify-center gap-1.5">
              <span>🖱️ স্ক্রল করতে মাউসের হুইল (Scroll Wheel) ফোনের স্ক্রিনের ওপর ঘুরান</span>
            </div>
          </div>
        </div>

        {/* Right Side: Feature Information & Real Phone Testing */}
        <div className="flex-1 max-w-md w-full space-y-6">
          
          {/* Box 1: Live Interactive Guide */}
          <div className="p-6 rounded-3xl bg-white/5 border border-white/10 space-y-4">
            <div className="flex items-center gap-2 text-[#38BDF8]">
              <Sparkles className="w-5 h-5" />
              <h2 className="text-base font-bold tracking-tight text-white">লাইভ মোবাইল ডেমো ফিচারস</h2>
            </div>
            
            <p className="text-xs text-gray-300 leading-relaxed">
              আপনি এখন সরাসরি আপনার পিসি থেকেই সম্পূর্ণ মোবাইল অভিজ্ঞতা দেখতে পাচ্ছেন। নিচের বিষয়গুলো টেস্ট করুন:
            </p>

            <ul className="space-y-3 text-xs text-gray-200">
              <li className="flex items-start gap-2.5">
                <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0 mt-0.5" />
                <span>
                  <strong>মাখনের মতো স্ক্রলিং:</strong> মাউসের হুইল ঘুরিয়ে পুরো প্রোডাক্ট ক্যাটালগ ও হিরো মোজাইক স্মুথলি স্ক্রল করুন।
                </span>
              </li>
              <li className="flex items-start gap-2.5">
                <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0 mt-0.5" />
                <span>
                  <strong>বটম অ্যাপ নেভিগেশন বার:</strong> নিচে ৫টি ট্যাব (Store, Explore, Track, Bag, Sign In) ক্লিক করে সরাসরি সুইচ করুন।
                </span>
              </li>
              <li className="flex items-start gap-2.5">
                <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0 mt-0.5" />
                <span>
                  <strong>লাইভ কার্ট কাউন্টার:</strong> প্রোডাক্টে ক্লিক করে "Add to Bag" চাপুন, ব্যাজের কাউন্টার তাৎক্ষণিক আপডেট হবে।
                </span>
              </li>
              <li className="flex items-start gap-2.5">
                <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0 mt-0.5" />
                <span>
                  <strong>ডিভাইস টগল:</strong> উপরের বার থেকে iPhone 16 Pro এবং Samsung Galaxy S24 Ultra এর স্ক্রিন সাইজ পরিবর্তন করে দেখুন।
                </span>
              </li>
            </ul>
          </div>

          {/* Box 2: Real Mobile Phone QR Code Scan */}
          <div className="p-6 rounded-3xl bg-gradient-to-br from-[#0B132B] to-[#121E3E] border border-white/10 space-y-4 shadow-xl">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2 text-[#38BDF8]">
                <QrCode className="w-5 h-5" />
                <h3 className="text-sm font-bold text-white">আসল মোবাইলে লাইভ দেখুন</h3>
              </div>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-400/20 text-emerald-300 font-semibold">
                Local WiFi Ready
              </span>
            </div>

            <p className="text-xs text-gray-300 leading-relaxed">
              আপনার মোবাইল ফোনটি যদি এই কম্পিউটারের একই ওয়াইফাই নেটওয়ার্কে থাকে, তবে নিচের QR কোডটি স্ক্যান করে এখনই মোবাইলে দেখুন:
            </p>

            <div className="flex items-center gap-4 bg-white/5 p-4 rounded-2xl border border-white/10">
              <div className="bg-white p-2 rounded-xl flex-shrink-0 shadow-md">
                <img
                  src={qrCodeApiUrl}
                  alt="NEXORA QR Code"
                  className="w-24 h-24 object-contain"
                />
              </div>
              <div className="space-y-1.5 text-xs">
                <div className="font-semibold text-white">মোবাইল ব্রাউজার লিঙ্ক:</div>
                <div className="font-mono text-[#38BDF8] break-all bg-black/40 px-2 py-1 rounded border border-white/10 text-[11px]">
                  {localNetworkUrl}
                </div>
                <div className="text-[11px] text-gray-400">
                  Chrome বা Safari দিয়ে ক্যামেরা তাক করলেই সরাসরি পেজ খুলবে।
                </div>
              </div>
            </div>
          </div>

          {/* Box 3: PWA Installation Guide */}
          <div className="p-5 rounded-3xl bg-white/5 border border-white/10 space-y-3">
            <h4 className="text-xs font-bold text-white uppercase tracking-wider flex items-center gap-1.5">
              <Info className="w-4 h-4 text-[#38BDF8]" />
              <span>মোবাইলে অফিশিয়াল অ্যাপ হিসেবে যেভাবে রাখবেন:</span>
            </h4>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs text-gray-300">
              <div className="bg-black/30 p-3 rounded-2xl border border-white/5 space-y-1">
                <div className="font-bold text-white">🤖 Android (Chrome)</div>
                <div className="text-[11px] text-gray-400">
                  মেনু (তিন ডট ⋮) চাপুন &gt; <strong>"Add to Home screen"</strong> বা "Install App" এ ক্লিক করুন।
                </div>
              </div>
              <div className="bg-black/30 p-3 rounded-2xl border border-white/5 space-y-1">
                <div className="font-bold text-white">🍏 iPhone (Safari)</div>
                <div className="text-[11px] text-gray-400">
                  নিচের শেয়ার আইকন (⎋) চাপুন &gt; স্ক্রল করে <strong>"Add to Home Screen"</strong> এ ট্যাপ করুন।
                </div>
              </div>
            </div>
          </div>

        </div>

      </main>

      {/* QR Code Large Modal */}
      {showQrModal && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-md flex items-center justify-center p-4">
          <div className="bg-[#0B132B] border border-white/20 rounded-3xl p-6 sm:p-8 max-w-sm w-full text-center space-y-4 shadow-2xl">
            <h3 className="text-lg font-bold text-white">মোবাইলে স্ক্যান করুন</h3>
            <p className="text-xs text-gray-300">
              আপনার মোবাইলের ক্যামেরা চালু করে নিচের কোডটি স্ক্যান করুন:
            </p>
            <div className="bg-white p-4 rounded-2xl inline-block shadow-inner mx-auto">
              <img
                src={qrCodeApiUrl}
                alt="NEXORA QR Code"
                className="w-48 h-48 object-contain"
              />
            </div>
            <div className="font-mono text-xs text-[#38BDF8] bg-black/40 py-2 px-3 rounded-xl border border-white/10 break-all">
              {localNetworkUrl}
            </div>
            <button
              onClick={() => setShowQrModal(false)}
              className="w-full py-2.5 rounded-full bg-white/10 hover:bg-white/20 text-white text-xs font-semibold transition-all"
            >
              বন্ধ করুন (Close)
            </button>
          </div>
        </div>
      )}

    </div>
  );
}

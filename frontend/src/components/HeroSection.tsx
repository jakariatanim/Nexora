'use client';

import React, { useState, useEffect } from 'react';
import Image from 'next/image';
import Link from 'next/link';
import { ArrowRight } from 'lucide-react';
import { useCart } from '../lib/cartContext';
import { Product } from '../lib/types';

interface TileItem {
  id?: string;
  name: string;
  image: string;
  href: string;
  shortName?: string;
  priceBDT?: number;
}

// 1. Tile 1 Items: Flagship Smartphones (Apple & Android Flagships)
const TILE_AUDIO_ITEMS: TileItem[] = [
  {
    id: "apple-iphone-16-pro-max",
    name: "Apple iPhone 16 Pro Max",
    image: "/products/apple-iphone-16-pro-max.png",
    href: "/product/apple-iphone-16-pro-max",
  },
  {
    id: "samsung-galaxy-s24-plus",
    name: "Samsung Galaxy S24+",
    image: "/products/samsung-galaxy-s24-plus.png",
    href: "/product/samsung-galaxy-s24-plus",
  },
  {
    id: "google-pixel-9-pro",
    name: "Google Pixel 9 Pro",
    image: "/products/google-pixel-9-pro.png",
    href: "/product/google-pixel-9-pro",
  },
  {
    id: "oneplus-12r",
    name: "OnePlus 12R Flagship",
    image: "/products/oneplus-12r.png",
    href: "/product/oneplus-12r",
  },
];

// 2. Tile 2 Items: Flagship Foldables & Ultra Phones (No Watch Straps!)
const TILE_WATCH_ITEMS: TileItem[] = [
  {
    id: "galaxy-z-fold-6",
    name: "Samsung Galaxy Z Fold 6",
    image: "/products/galaxy-z-fold-6.png",
    href: "/product/galaxy-z-fold-6",
  },
  {
    id: "xiaomi-14-ultra",
    name: "Xiaomi 14 Ultra Leica Pro",
    image: "/products/xiaomi-14-ultra.png",
    href: "/product/xiaomi-14-ultra",
  },
  {
    id: "oppo-find-n3",
    name: "Oppo Find N3 Flagship Fold",
    image: "/products/oppo-find-n3.png",
    href: "/product/oppo-find-n3",
  },
  {
    id: "vivo-x100-ultra",
    name: "Vivo X100 Ultra Zeiss 200MP",
    image: "/products/vivo-x100-ultra.png",
    href: "/product/vivo-x100-ultra",
  },
];

// 3. Tile 3 Items: THE SIGNATURE NEXORA LOGO (Products Rotating Inside)
const NEXORA_LOGO_PRODUCTS = [
  {
    id: "iphone-18-pro-max",
    name: "Apple iPhone 18 Pro Max",
    shortName: "iPhone 18 Pro",
    image: "/products/iphone-18-pro-max.png",
    priceBDT: 215000,
  },
  {
    id: "samsung-s24-ultra",
    name: "Samsung Galaxy S24 Ultra",
    shortName: "Galaxy S24 Ultra",
    image: "/products/samsung-s24-ultra.png",
    priceBDT: 178000,
  },
  {
    id: "macbook-pro-16-m3-max",
    name: "Apple MacBook Pro 16-inch",
    shortName: "MacBook Pro 16″",
    image: "/products/macbook-pro.png",
    priceBDT: 365000,
  },
  {
    id: "apple-watch-ultra-2",
    name: "Apple Watch Ultra 2",
    shortName: "Watch Ultra 2",
    image: "/products/apple-watch-ultra-2.png",
    priceBDT: 98000,
  },
  {
    id: "airpods-max",
    name: "Apple AirPods Max",
    shortName: "AirPods Max",
    image: "/products/airpods-max.png",
    priceBDT: 65000,
  },
  {
    id: "galaxy-z-fold-6",
    name: "Samsung Galaxy Z Fold 6",
    shortName: "Galaxy Z Fold 6",
    image: "/products/galaxy-z-fold-6.png",
    priceBDT: 225000,
  },
  {
    id: "pixel-9-pro-xl",
    name: "Google Pixel 9 Pro XL",
    shortName: "Pixel 9 Pro XL",
    image: "/products/pixel-9-pro-xl.png",
    priceBDT: 145000,
  },
];

// 4. Tile 4 Items: Studio Smartphones (Flagship Rotation)
const TILE_PHONE_ITEMS: TileItem[] = [
  {
    id: "iphone-18-pro-max",
    name: "iPhone 18 Pro Max (Wine Titanium)",
    image: "/products/iphone-18-pro-max.png",
    href: "/product/iphone-18-pro-max",
  },
  {
    id: "samsung-s24-ultra",
    name: "Samsung Galaxy S24 Ultra",
    image: "/products/samsung-s24-ultra.png",
    href: "/product/samsung-s24-ultra",
  },
  {
    id: "galaxy-z-fold-6",
    name: "Samsung Galaxy Z Fold 6",
    image: "/products/galaxy-z-fold-6.png",
    href: "/product/galaxy-z-fold-6",
  },
  {
    id: "pixel-9-pro-xl",
    name: "Google Pixel 9 Pro XL",
    image: "/products/pixel-9-pro-xl.png",
    href: "/product/pixel-9-pro-xl",
  },
];

// 5. Tile 5 Items: Flagship Workstations & Tablets (Top Right - No Watch Straps!)
const TILE_LINEUP_ITEMS: TileItem[] = [
  {
    id: "ipad-pro-m4",
    name: "Apple iPad Pro M4 Ultra Retina",
    image: "/products/ipad-pro-m4.png",
    href: "/product/ipad-pro-m4",
  },
  {
    id: "macbook-pro-16-m3-max",
    name: "Apple MacBook Pro 16-inch M3 Max",
    image: "/products/macbook-pro.png",
    href: "/product/macbook-pro-16-m3-max",
  },
  {
    id: "samsung-galaxy-s24-plus",
    name: "Samsung Galaxy S24+ Flagship",
    image: "/products/samsung-galaxy-s24-plus.png",
    href: "/product/samsung-galaxy-s24-plus",
  },
  {
    id: "google-pixel-9-pro",
    name: "Google Pixel 9 Pro Studio",
    image: "/products/google-pixel-9-pro.png",
    href: "/product/google-pixel-9-pro",
  },
];

// 6. Tile 6 Items: Multi-Brand Wireless Fast Chargers & Power Stations (Bottom Left)
const TILE_CHARGER_ITEMS: TileItem[] = [
  {
    id: "anker-maggo-qi2-cube",
    name: "Anker MagGo Qi2 3-in-1 Foldable Cube",
    image: "/products/anker-maggo-cube.png",
    href: "/product/anker-maggo-qi2-cube",
  },
  {
    id: "samsung-wireless-trio",
    name: "Samsung Wireless Charger Trio Station",
    image: "/products/samsung-wireless-trio.png",
    href: "/product/samsung-wireless-trio",
  },
  {
    id: "apple-magsafe-charger-25w",
    name: "Apple 25W MagSafe Wireless Charger",
    image: "/products/apple-magsafe-charger.png",
    href: "/product/apple-magsafe-charger-25w",
  },
  {
    id: "xiaomi-120w-hypercharge-adapter",
    name: "Xiaomi 120W HyperCharge GaN Adapter",
    image: "/products/xiaomi-120w-hypercharge-adapter.png",
    href: "/product/xiaomi-120w-hypercharge-adapter",
  },
];

// 7. Tile 8 Items: High-Fidelity Audio & Studio Acoustics (Bottom Right - PURE AUDIO, ZERO STRAPS!)
const TILE_BOTTOM_RIGHT_ITEMS: TileItem[] = [
  {
    id: "airpods-max",
    name: "Apple AirPods Max Studio Over-Ear",
    image: "/products/airpods-max.png",
    href: "/product/airpods-max",
  },
  {
    id: "airpods-pro-2",
    name: "Apple AirPods Pro 2 Active Noise Cancelling",
    image: "/products/airpods-pro-2.png",
    href: "/product/airpods-pro-2",
  },
  {
    id: "sony-wh1000xm5",
    name: "Sony WH-1000XM5 Studio Acoustics",
    image: "/products/sony-wh1000xm5.png",
    href: "/product/sony-wh1000xm5",
  },
  {
    id: "samsung-galaxy-buds3-pro",
    name: "Samsung Galaxy Buds3 Pro Hi-Fi Acoustics",
    image: "/products/samsung-galaxy-buds3-pro.png",
    href: "/product/samsung-galaxy-buds3-pro",
  },
];

export const HeroSection: React.FC = () => {
  const { addToCart, setIsCartOpen } = useCart();
  const [addedHeroId, setAddedHeroId] = useState<string | null>(null);

  const handleHeroAddToCartSilent = (product: Product) => {
    addToCart(product, 1, false);
    setAddedHeroId(product.id);
    setTimeout(() => {
      setAddedHeroId(prev => (prev === product.id ? null : prev));
    }, 1600);
  };

  // Dynamic cycling states for ALL living mosaic tiles (continuous autoplay, no pause button)
  const [audioIdx, setAudioIdx] = useState(0);
  const [watchIdx, setWatchIdx] = useState(0);
  const [logoSlideIdx, setLogoSlideIdx] = useState(0);
  const [phoneIdx, setPhoneIdx] = useState(0);
  const [lineupIdx, setLineupIdx] = useState(0);
  const [chargerIdx, setChargerIdx] = useState(0);
  const [bottomRightIdx, setBottomRightIdx] = useState(0);

  // Staggered asynchronous interval timers for the living Apple-standard mosaic
  useEffect(() => {
    // Logo centerpiece cycles smoothly every 1.6s
    const logoTimer = setInterval(() => {
      setLogoSlideIdx((prev) => (prev + 1) % NEXORA_LOGO_PRODUCTS.length);
    }, 1600);

    // Smartphones tile cycles every 2.1s
    const audioTimer = setInterval(() => {
      setAudioIdx((prev) => (prev + 1) % TILE_AUDIO_ITEMS.length);
    }, 2100);

    // Foldables tile cycles every 2.4s
    const watchTimer = setInterval(() => {
      setWatchIdx((prev) => (prev + 1) % TILE_WATCH_ITEMS.length);
    }, 2400);

    // Phones tile cycles every 2.0s
    const phoneTimer = setInterval(() => {
      setPhoneIdx((prev) => (prev + 1) % TILE_PHONE_ITEMS.length);
    }, 2000);

    // Lineup tile cycles every 2.6s
    const lineupTimer = setInterval(() => {
      setLineupIdx((prev) => (prev + 1) % TILE_LINEUP_ITEMS.length);
    }, 2600);

    // Charger tile cycles every 2.3s
    const chargerTimer = setInterval(() => {
      setChargerIdx((prev) => (prev + 1) % TILE_CHARGER_ITEMS.length);
    }, 2300);

    // Bottom right tile cycles every 2.5s
    const bottomRightTimer = setInterval(() => {
      setBottomRightIdx((prev) => (prev + 1) % TILE_BOTTOM_RIGHT_ITEMS.length);
    }, 2500);

    return () => {
      clearInterval(logoTimer);
      clearInterval(audioTimer);
      clearInterval(watchTimer);
      clearInterval(phoneTimer);
      clearInterval(lineupTimer);
      clearInterval(chargerTimer);
      clearInterval(bottomRightTimer);
    };
  }, []);

  const activeAudio = TILE_AUDIO_ITEMS[audioIdx];
  const activeWatch = TILE_WATCH_ITEMS[watchIdx];
  const activeLogoProduct = NEXORA_LOGO_PRODUCTS[logoSlideIdx];
  const activePhone = TILE_PHONE_ITEMS[phoneIdx];
  const activeLineup = TILE_LINEUP_ITEMS[lineupIdx];
  const activeCharger = TILE_CHARGER_ITEMS[chargerIdx];
  const activeBottomRight = TILE_BOTTOM_RIGHT_ITEMS[bottomRightIdx];

  const iphone18Pro: Product = {
    id: "iphone-18-pro-max",
    name: "Apple iPhone 18 Pro Max",
    tagline: "Titanium Unibody. Breakthrough A20 Pro Silicon.",
    category: "Smartphones",
    priceBDT: 215000,
    priceUSD: 1599,
    inStock: true,
    stockCount: 35,
    rating: 5.0,
    reviewCount: 164,
    image: "/products/iphone-18-pro-max.png",
    specs: ["A20 Pro Neural Bionic Architecture", "Grade 5 Titanium Unibody", "48MP Fusion 10x Optical Zoom"],
    description: "The pinnacle of Apple smartphone architecture with breakthrough A20 Pro neural silicon.",
  };

  const s24Ultra: Product = {
    id: "samsung-s24-ultra",
    name: "Samsung Galaxy S24 Ultra",
    tagline: "Galaxy AI is Here. 200MP Quad Telephoto & Titanium.",
    category: "Smartphones",
    priceBDT: 178000,
    priceUSD: 1370,
    inStock: true,
    stockCount: 22,
    rating: 4.9,
    reviewCount: 94,
    image: "/products/samsung-s24-ultra.png",
    specs: ["Snapdragon 8 Gen 3 for Galaxy", "Built-In S Pen Stylus", "200MP Quad Telephoto"],
    description: "The pinnacle of Samsung mobile craftsmanship.",
  };

  return (
    <div className="w-full flex flex-col items-center">
      {/* =========================================================================
          1. SIGNATURE LIVING MOSAIC (WITH ENLARGED NEXORA LOGO AT TOP CENTER)
             AUTOMATIC CONTINUOUS AUTOPLAY - NO PAUSE BUTTON - WARM APPLE HOLIDAY PALETTE
          ========================================================================= */}
      <section className="relative w-full max-w-[1400px] mx-auto px-2 sm:px-4 pt-24 pb-8 overflow-hidden select-none">
        
        {/* The Mosaic Grid Container */}
        <div className="w-full rounded-2xl sm:rounded-3xl overflow-hidden border border-black/[0.08] dark:border-white/10 shadow-sm bg-[#F5F5F7] dark:bg-[#0B1229]">
          
          {/* Top Row Grid (Symmetrical 12 Columns: 2 + 2 + 4 [Logo Centerpiece] + 2 + 2) */}
          <div className="grid grid-cols-12 h-56 sm:h-68 md:h-76 lg:h-84">
            
            {/* Tile 1: Flagship Smartphones (Col 2 on desktop; hidden on mobile for clean 3-tile symmetry) - WARM PEACH PALETTE */}
            <Link
              href={activeAudio.href}
              className="hidden sm:flex sm:col-span-2 bg-[#F8B195] relative items-center justify-center overflow-hidden border-r border-b border-black/[0.06] dark:border-white/10 group cursor-pointer p-3 sm:p-4 transition-colors"
              title={activeAudio.name}
            >
              <div 
                key={activeAudio.id || activeAudio.image}
                className="relative w-24 h-32 sm:w-28 sm:h-38 md:w-32 md:h-44 transform hover:scale-105 transition-all duration-700 ease-out animate-fade-in flex items-center justify-center"
              >
                <Image
                  src={activeAudio.image}
                  alt={activeAudio.name}
                  fill
                  className="object-contain drop-shadow-[0_12px_24px_rgba(0,0,0,0.2)]"
                  sizes="160px"
                />
              </div>
            </Link>

            {/* Tile 2: Flagship Foldables & Ultra Phones (Col 2) - WARM BUTTERCREAM PALETTE */}
            <Link
              href={activeWatch.href}
              className="col-span-3 sm:col-span-2 relative overflow-hidden border-r border-b border-black/[0.06] dark:border-white/10 bg-[#FEF7D2] group cursor-pointer flex items-center justify-center p-2.5 sm:p-3 transition-colors"
              title={activeWatch.name}
            >
              <div 
                key={activeWatch.id || activeWatch.image}
                className="relative w-24 h-32 sm:w-28 sm:h-38 md:w-32 md:h-44 transform hover:scale-105 transition-all duration-700 ease-out animate-fade-in flex items-center justify-center"
              >
                <Image
                  src={activeWatch.image}
                  alt={activeWatch.name}
                  fill
                  className="object-contain rounded-xl drop-shadow-[0_8px_16px_rgba(0,0,0,0.15)]"
                  sizes="220px"
                />
              </div>
            </Link>

            {/* =====================================================================
                Tile 3: THE SIGNATURE NEXORA LOGO (TOP CENTER! COL 4 - LARGE & PROMINENT)
                NO PLUS SIGN! REAL PRODUCTS ROTATING INSIDE THE APERTURE!
                WARM PORCELAIN IVORY BASE
                ===================================================================== */}
            <Link
              href={`/product/${activeLogoProduct.id}`}
              className="col-span-6 sm:col-span-4 bg-[#FDF6ED] flex flex-col items-center justify-center relative overflow-hidden border-r border-b border-black/[0.06] dark:border-white/10 p-3 sm:p-4 group cursor-pointer"
              title={`View ${activeLogoProduct.name} - ৳ ${activeLogoProduct.priceBDT.toLocaleString()}`}
            >
              {/* Centerpiece container - Enlarged per user request */}
              <div className="relative w-36 h-36 sm:w-48 sm:h-48 md:w-54 md:h-54 flex items-center justify-center">
                
                {/* 1. Festive 4-Quadrant Pattern Base clipped cleanly to Nexora Logo Shape */}
                <div 
                  className="w-32 h-32 sm:w-44 sm:h-44 md:w-48 md:h-48 relative rounded-3xl shadow-2xl overflow-hidden transition-transform duration-500 group-hover:scale-105"
                  style={{
                    maskImage: "url('/brand/nexora_icon_white_transparent.png')",
                    WebkitMaskImage: "url('/brand/nexora_icon_white_transparent.png')",
                    maskSize: "contain",
                    WebkitMaskSize: "contain",
                    maskRepeat: "no-repeat",
                    WebkitMaskRepeat: "no-repeat",
                    maskPosition: "center",
                    WebkitMaskPosition: "center",
                  }}
                >
                  {/* Quadrant 1: Top-Left Red Diagonal Stripes */}
                  <div className="absolute top-0 left-0 w-1/2 h-1/2 bg-[#DF2847] overflow-hidden">
                    <svg className="w-full h-full" viewBox="0 0 50 50">
                      <line x1="0" y1="0" x2="50" y2="50" stroke="#7E0C22" strokeWidth="6" />
                      <line x1="25" y1="0" x2="50" y2="25" stroke="#7E0C22" strokeWidth="6" />
                      <line x1="0" y1="25" x2="25" y2="50" stroke="#7E0C22" strokeWidth="6" />
                    </svg>
                  </div>

                  {/* Quadrant 2: Top-Right Plum Polka Dots */}
                  <div className="absolute top-0 right-0 w-1/2 h-1/2 bg-[#8A1C4E] flex items-center justify-center overflow-hidden">
                    <div className="w-full h-full opacity-60 bg-[radial-gradient(#F8A6C6_4px,transparent_4px)] [background-size:12px_12px]" />
                  </div>

                  {/* Quadrant 3: Bottom-Left Pink Polka Dots */}
                  <div className="absolute bottom-0 left-0 w-1/2 h-1/2 bg-[#F8A6C6] flex items-center justify-center overflow-hidden">
                    <div className="w-full h-full opacity-70 bg-[radial-gradient(#8A1C4E_4px,transparent_4px)] [background-size:12px_12px]" />
                  </div>

                  {/* Quadrant 4: Bottom-Right Red Diagonal Stripes */}
                  <div className="absolute bottom-0 right-0 w-1/2 h-1/2 bg-[#DF2847] overflow-hidden">
                    <svg className="w-full h-full" viewBox="0 0 50 50">
                      <line x1="0" y1="0" x2="50" y2="50" stroke="#7E0C22" strokeWidth="6" />
                      <line x1="25" y1="0" x2="50" y2="25" stroke="#7E0C22" strokeWidth="6" />
                      <line x1="0" y1="25" x2="25" y2="50" stroke="#7E0C22" strokeWidth="6" />
                    </svg>
                  </div>

                  {/* 2. REAL PRODUCT STUDIO SLIDE INSIDE THE NEXORA LOGO (ENLARGED & PROMINENT) */}
                  <div className="absolute inset-0 flex items-center justify-center p-2 z-10">
                    <div 
                      key={activeLogoProduct.id}
                      className="relative w-20 h-20 sm:w-28 sm:h-28 md:w-32 md:h-32 transition-all duration-700 ease-out transform animate-fade-in drop-shadow-[0_12px_24px_rgba(0,0,0,0.45)]"
                    >
                      <Image
                        src={activeLogoProduct.image}
                        alt={activeLogoProduct.name}
                        fill
                        className="object-contain"
                        sizes="(max-width: 768px) 110px, 140px"
                      />
                    </div>
                  </div>

                  {/* Aperture Edge Highlight */}
                  <div className="absolute inset-0 bg-gradient-to-tr from-cyan-400/20 via-transparent to-white/30 pointer-events-none" />
                </div>

              </div>

              {/* Dynamic Product Label & Direct Link Prompt */}
              <div className="mt-2 flex items-center gap-1.5 px-3 py-1 rounded-full bg-white/95 dark:bg-black/85 backdrop-blur-sm border border-black/10 dark:border-white/20 shadow-sm text-[10px] sm:text-xs font-semibold text-[#1D1D1F] dark:text-white group-hover:bg-[#0071E3] group-hover:text-white transition-colors">
                <span className="truncate max-w-[130px] sm:max-w-[160px]">{activeLogoProduct.shortName}</span>
                <ArrowRight className="w-3 h-3 flex-shrink-0" />
              </div>
            </Link>

            {/* Tile 4: Studio Smartphones (Col 3 on mobile, Col 2 on desktop) - WARM HONEY AMBER PALETTE */}
            <Link
              href={activePhone.href}
              className="col-span-3 sm:col-span-2 bg-[#F8B042] relative flex items-center justify-center p-2.5 sm:p-3 overflow-hidden sm:border-r border-b border-black/[0.06] dark:border-white/10 group cursor-pointer transition-colors"
              title={activePhone.name}
            >
              <div 
                key={activePhone.id || activePhone.image}
                className="relative w-24 h-32 sm:w-28 sm:h-38 md:w-32 md:h-44 transform hover:scale-105 transition-all duration-700 ease-out animate-fade-in flex items-center justify-center"
              >
                <Image
                  src={activePhone.image}
                  alt={activePhone.name}
                  fill
                  className="object-contain drop-shadow-[0_14px_28px_rgba(0,0,0,0.28)]"
                  sizes="180px"
                />
              </div>
            </Link>

            {/* Tile 5: Smartphone Lineup Displays (Col 2 on desktop; hidden on mobile for clean 3-tile symmetry) - SOFT WARM PEACH/CORAL ROSE */}
            <Link
              href={activeLineup.href}
              className="hidden sm:flex sm:col-span-2 bg-[#F5BCA9] relative items-center justify-center overflow-hidden border-b border-black/[0.06] dark:border-white/10 p-2 sm:p-3 group cursor-pointer transition-colors"
              title={activeLineup.name}
            >
              <div 
                key={activeLineup.image}
                className="relative w-full h-full max-h-48 transform hover:scale-105 transition-all duration-700 ease-out animate-fade-in flex items-center justify-center"
              >
                <Image
                  src={activeLineup.image}
                  alt={activeLineup.name}
                  fill
                  className="object-contain rounded-xl drop-shadow-[0_8px_16px_rgba(0,0,0,0.15)]"
                  sizes="220px"
                />
              </div>
            </Link>
          </div>

          {/* Bottom Row Grid (12 Columns: 3 + 6 [Center Banner] + 3) */}
          <div className="grid grid-cols-12 h-52 sm:h-64 md:h-72 lg:h-80">
            
            {/* Tile 6: Fast Wireless Chargers (Col 3) - WARM BUTTER YELLOW PALETTE */}
            <Link
              href={activeCharger.href}
              className="col-span-3 sm:col-span-3 bg-[#FCE99B] relative flex items-center justify-center overflow-hidden border-r border-black/[0.06] dark:border-white/10 p-3 group cursor-pointer"
              title={activeCharger.name}
            >
              <div 
                key={activeCharger.image}
                className="relative w-full h-full max-h-48 rounded-xl overflow-hidden shadow-sm transform hover:scale-105 transition-all duration-700 ease-out animate-fade-in flex items-center justify-center"
              >
                <Image
                  src={activeCharger.image}
                  alt={activeCharger.name}
                  fill
                  className="object-contain"
                  sizes="300px"
                />
              </div>
            </Link>

            {/* Tile 7: THE SIGNATURE CENTERPIECE BANNER (Col 6) - RICH WARM APPLE HOLIDAY CHESTNUT BROWN #5B2313 */}
            <div className="col-span-6 sm:col-span-6 bg-[#5B2313] dark:bg-[#4E1C0F] flex flex-col items-center justify-center text-center px-4 sm:px-8 relative overflow-hidden">
              <div className="max-w-md mx-auto space-y-2 sm:space-y-3 z-10">
                <h2 className="text-2xl sm:text-4xl md:text-5xl font-semibold tracking-tight text-white leading-tight">
                  Gifts they&apos;ll love.
                </h2>
                <p className="text-xs sm:text-base md:text-lg text-[#F5D8CE] font-normal tracking-tight">
                  Find their perfect match this holiday.
                </p>
                <div className="pt-2">
                  <Link
                    href="/explore"
                    className="inline-flex items-center justify-center px-6 sm:px-8 py-2 sm:py-2.5 rounded-full bg-[#0071E3] hover:bg-[#0077ED] text-white font-medium text-xs sm:text-sm tracking-wide transition-all shadow-md active:scale-95"
                  >
                    Shop gifts
                  </Link>
                </div>
              </div>
            </div>

            {/* Tile 8: Premium Wearables & High-Fidelity Audio (Col 3) - WARM CORAL PALETTE (NO STRAPS!) */}
            <Link
              href={activeBottomRight.href}
              className="col-span-3 sm:col-span-3 bg-[#FA6432] relative flex items-center justify-center overflow-hidden border-l border-black/[0.06] dark:border-white/10 p-3 group cursor-pointer"
              title={activeBottomRight.name}
            >
              <div 
                key={activeBottomRight.image}
                className="relative w-full h-full max-h-48 transform hover:scale-105 transition-all duration-700 ease-out animate-fade-in flex items-center justify-center"
              >
                <Image
                  src={activeBottomRight.image}
                  alt={activeBottomRight.name}
                  fill
                  className="object-contain rounded-xl drop-shadow-[0_12px_24px_rgba(0,0,0,0.18)]"
                  sizes="300px"
                />
              </div>
            </Link>

          </div>
        </div>
      </section>

      {/* =========================================================================
          2. APPLE BILLBOARD 1: iPHONE 18 PRO MAX (SLEEK 16:9 CINEMATIC LETTERBOX)
          ========================================================================= */}
      <section className="w-full max-w-6xl mx-auto px-4 sm:px-6 my-3 sm:my-8">
        <div className="rounded-2xl sm:rounded-3xl bg-[#F5F5F7] dark:bg-[#14141B] border border-black/[0.08] dark:border-white/10 shadow-sm p-5 sm:p-12 flex flex-col items-center justify-center text-center relative overflow-hidden group">
          {/* 1. Title & Subtitle */}
          <div className="max-w-3xl mx-auto space-y-1.5 sm:space-y-2.5 z-10">
            <Link href="/product/iphone-18-pro-max">
              <h2 className="text-2xl sm:text-5xl md:text-6xl font-semibold tracking-tight text-[#1D1D1F] dark:text-white leading-tight hover:text-[#0071E3] transition-colors">
                iPhone 18 Pro Max
              </h2>
            </Link>
            <p className="text-xs sm:text-xl md:text-2xl font-normal text-[#6E6E73] dark:text-[#A1A1A6] tracking-tight">
              Titanium Unibody. Breakthrough A20 Pro Silicon.
            </p>
          </div>

          {/* 2. Product Image in Center */}
          <Link href="/product/iphone-18-pro-max" className="relative my-3 sm:my-8 w-full max-w-2xl h-40 sm:h-72 md:h-80 flex items-center justify-center cursor-pointer">
            <div className="relative w-full h-full transform group-hover:scale-105 transition-transform duration-700">
              <Image
                src="/products/iphone-18-pro-studio.png"
                alt="Apple iPhone 18 Pro Max"
                fill
                priority
                className="object-contain drop-shadow-[0_20px_40px_rgba(0,0,0,0.18)]"
                sizes="(max-width: 768px) 260px, 580px"
              />
            </div>
          </Link>

          {/* 3. Below Product Image: Dual Action Buttons */}
          <div className="flex items-center justify-center gap-2 sm:gap-3 pt-1 sm:pt-2 z-10">
            <button
              onClick={() => handleHeroAddToCartSilent(iphone18Pro)}
              className="px-4 sm:px-6 py-2 sm:py-2.5 rounded-full border border-black/15 dark:border-white/20 bg-black/5 hover:bg-black/10 dark:bg-white/10 dark:hover:bg-white/15 text-[#1D1D1F] dark:text-white font-medium text-xs sm:text-sm tracking-wide transition-all shadow-sm active:scale-95"
            >
              {addedHeroId === iphone18Pro.id ? 'Added ✓' : 'Add to Cart'}
            </button>
            <button
              onClick={() => {
                addToCart(iphone18Pro, 1, true);
                setIsCartOpen(true);
              }}
              className="px-6 sm:px-8 py-2 sm:py-2.5 rounded-full bg-[#0071E3] hover:bg-[#0077ED] text-white font-medium text-xs sm:text-sm tracking-wide transition-all shadow-sm active:scale-95"
            >
              Buy
            </button>
          </div>
        </div>
      </section>

      {/* =========================================================================
          3. APPLE BILLBOARD 2: SAMSUNG GALAXY S24 ULTRA (SLEEK 16:9 CINEMATIC LETTERBOX)
          ========================================================================= */}
      <section className="w-full max-w-6xl mx-auto px-4 sm:px-6 my-3 sm:my-8">
        <div className="rounded-2xl sm:rounded-3xl bg-[#F0EDE6] dark:bg-[#0F1424] border border-black/[0.08] dark:border-white/10 shadow-sm p-5 sm:p-12 flex flex-col items-center justify-center text-center relative overflow-hidden group">
          {/* 1. Title & Subtitle */}
          <div className="max-w-3xl mx-auto space-y-1.5 sm:space-y-2.5 z-10">
            <Link href="/product/samsung-s24-ultra">
              <h2 className="text-2xl sm:text-5xl md:text-6xl font-semibold tracking-tight text-[#1D1D1F] dark:text-white leading-tight hover:text-[#0071E3] transition-colors">
                Galaxy S24 Ultra
              </h2>
            </Link>
            <p className="text-xs sm:text-xl md:text-2xl font-normal text-[#6E6E73] dark:text-[#A1A1A6] tracking-tight">
              Galaxy AI is Here. 200MP Quad Telephoto &amp; Titanium.
            </p>
          </div>

          {/* 2. Product Image in Center */}
          <Link href="/product/samsung-s24-ultra" className="relative my-3 sm:my-8 w-full max-w-2xl h-40 sm:h-72 md:h-80 flex items-center justify-center cursor-pointer">
            <div className="relative w-full h-full transform group-hover:scale-105 transition-transform duration-700">
              <Image
                src="/products/samsung-s24-ultra-studio.png"
                alt="Samsung Galaxy S24 Ultra"
                fill
                className="object-contain drop-shadow-[0_20px_40px_rgba(0,0,0,0.16)]"
                sizes="(max-width: 768px) 260px, 580px"
              />
            </div>
          </Link>

          {/* 3. Below Product Image: Dual Action Buttons */}
          <div className="flex items-center justify-center gap-2 sm:gap-3 pt-1 sm:pt-2 z-10">
            <button
              onClick={() => handleHeroAddToCartSilent(s24Ultra)}
              className="px-4 sm:px-6 py-2 sm:py-2.5 rounded-full border border-black/15 dark:border-white/20 bg-black/5 hover:bg-black/10 dark:bg-white/10 dark:hover:bg-white/15 text-[#1D1D1F] dark:text-white font-medium text-xs sm:text-sm tracking-wide transition-all shadow-sm active:scale-95"
            >
              {addedHeroId === s24Ultra.id ? 'Added ✓' : 'Add to Cart'}
            </button>
            <button
              onClick={() => {
                addToCart(s24Ultra, 1, true);
                setIsCartOpen(true);
              }}
              className="px-6 sm:px-8 py-2 sm:py-2.5 rounded-full bg-[#0071E3] hover:bg-[#0077ED] text-white font-medium text-xs sm:text-sm tracking-wide transition-all shadow-sm active:scale-95"
            >
              Buy
            </button>
          </div>
        </div>
      </section>

    </div>
  );
};

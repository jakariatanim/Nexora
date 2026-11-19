'use client';

import React, { useState } from 'react';
import Image from 'next/image';
import { Download, Check, Sparkles } from 'lucide-react';
import { usePWA } from './PWAProvider';

export const AppInstallBanner: React.FC = () => {
  const { installApp, isInstalled } = usePWA();
  const [installing, setInstalling] = useState(false);

  const handleInstallClick = async () => {
    setInstalling(true);
    await installApp();
    setTimeout(() => setInstalling(false), 2000);
  };

  return (
    <section className="py-12 px-4 max-w-6xl mx-auto">
      <div className="rounded-3xl p-6 sm:p-10 md:p-12 bg-white dark:bg-[#121624] border border-black/[0.06] dark:border-white/10 shadow-[0_4px_24px_rgba(0,0,0,0.03)] flex flex-col md:flex-row items-center justify-between gap-6 sm:gap-8 relative overflow-hidden">
        
        {/* Left Side: Icon & Copy */}
        <div className="flex items-center gap-4 sm:gap-6 z-10 text-center md:text-left flex-col md:flex-row">
          <div className="relative w-16 h-16 sm:w-20 sm:h-20 rounded-2xl bg-[#0B132B] flex items-center justify-center p-3 shadow-lg flex-shrink-0 border border-white/10">
            <Image
              src="/brand/nexora_icon_white_transparent.png"
              alt="NEXORA Web App"
              fill
              className="object-contain p-2"
            />
          </div>

          <div className="space-y-1 sm:space-y-1.5">
            <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-[#0071E3]/10 text-[#0071E3] dark:text-[#38BDF8] text-[11px] font-mono font-semibold">
              <Sparkles className="w-3 h-3" />
              <span>Official Progressive Web App</span>
            </div>
            <h3 className="text-xl sm:text-2xl md:text-3xl font-bold text-[#1D1D1F] dark:text-white tracking-tight">
              NEXORA Web App
            </h3>
            <p className="text-xs sm:text-sm text-[#424245] dark:text-[#E2E8F0] max-w-lg leading-relaxed">
              Install to your mobile Home Screen or desktop for offline catalog access, instant hardware tracking, and lightning-fast checkout.
            </p>
          </div>
        </div>

        {/* Right Side: Install Action Button */}
        <div className="z-10 w-full md:w-auto flex items-center justify-center">
          <button
            onClick={handleInstallClick}
            disabled={isInstalled || installing}
            className={`w-full sm:w-auto px-7 py-3.5 rounded-full font-bold text-xs sm:text-sm tracking-wide transition-all shadow-md active:scale-95 flex items-center justify-center gap-2.5 ${
              isInstalled
                ? 'bg-emerald-600 text-white cursor-default'
                : 'bg-[#0071E3] hover:bg-[#0077ED] text-white hover:shadow-lg hover:shadow-blue-500/25'
            }`}
          >
            {isInstalled ? (
              <>
                <Check className="w-4 h-4 text-white" />
                <span>NEXORA App Active</span>
              </>
            ) : installing ? (
              <span>Opening Install Prompt...</span>
            ) : (
              <>
                <Download className="w-4 h-4" />
                <span>Install NEXORA App</span>
              </>
            )}
          </button>
        </div>
      </div>
    </section>
  );
};

'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Smartphone, Sparkles } from 'lucide-react';

export const MobileSimulatorFloatingButton: React.FC = () => {
  const pathname = usePathname();

  // Hide on mobile screens, in admin panel, or when already on app-demo
  if (pathname?.startsWith('/myadminerapanel') || pathname?.startsWith('/app-demo')) {
    return null;
  }

  return (
    <div className="hidden md:block fixed bottom-6 right-6 z-40">
      <Link
        href="/app-demo"
        className="group flex items-center gap-2.5 px-4 py-2.5 rounded-full bg-[#0B132B]/90 hover:bg-[#0071E3] dark:bg-[#121624]/95 dark:hover:bg-[#0071E3] text-white border border-white/20 shadow-[0_8px_30px_rgba(0,0,0,0.35)] backdrop-blur-xl transition-all duration-300 hover:scale-105 active:scale-95"
        title="NEXORA Interactive Mobile Simulator"
      >
        <div className="relative">
          <Smartphone className="w-4 h-4 text-[#38BDF8] group-hover:text-white transition-colors" />
          <span className="absolute -top-1 -right-1 w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
        </div>
        <div className="flex flex-col text-left">
          <span className="text-xs font-bold tracking-tight text-white leading-none">
            Mobile App Demo
          </span>
          <span className="text-[9px] font-mono text-gray-300 group-hover:text-white/80 leading-tight">
            PC Interactive Simulator
          </span>
        </div>
      </Link>
    </div>
  );
};

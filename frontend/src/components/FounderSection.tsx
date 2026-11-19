'use client';

import React from 'react';
import Image from 'next/image';
import Link from 'next/link';
import { ChevronRight } from 'lucide-react';

export const FounderSection: React.FC = () => {
  return (
    <section className="py-20 px-4 relative overflow-hidden bg-[#EFECE4] dark:bg-[#070B18]">
      <div className="max-w-5xl mx-auto rounded-3xl p-8 sm:p-14 bg-white dark:bg-[#121624] border border-black/[0.06] dark:border-white/10 shadow-[0_4px_30px_rgba(0,0,0,0.04)] relative">
        
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 items-center">
          
          {/* Founder Portrait Stage */}
          <div className="lg:col-span-5 flex flex-col items-center">
            <div className="relative w-64 h-80 sm:w-72 sm:h-96 rounded-3xl overflow-hidden border border-black/[0.08] dark:border-white/10 shadow-md bg-[#F5F5F7] dark:bg-white/5">
              <Image
                src="/brand/founder_jakaria.png"
                alt="Jakaria Tanim - Founder & Visionary"
                fill
                priority
                className="object-cover object-top"
              />
            </div>
            <div className="mt-4 text-center">
              <h4 className="text-lg font-semibold text-[#1D1D1F] dark:text-white tracking-wide">
                Jakaria Tanim
              </h4>
              <span className="text-xs font-mono tracking-widest text-[#0071E3] dark:text-[#38BDF8] uppercase block mt-0.5 font-medium">
                Founder &amp; Chief Architect
              </span>
            </div>
          </div>

          {/* Vision Story (Centered on Mobile, Left-aligned on Desktop) */}
          <div className="lg:col-span-7 space-y-4 sm:space-y-5 text-center lg:text-left flex flex-col items-center lg:items-start">
            <span className="text-xs font-mono uppercase tracking-widest text-[#0071E3] dark:text-[#38BDF8] font-semibold">
              Founder&apos;s Vision
            </span>

            <h2 className="text-2xl sm:text-4xl font-semibold text-[#1D1D1F] dark:text-white tracking-tight leading-tight">
              &ldquo;Technology shouldn&apos;t shout. It should empower silently.&rdquo;
            </h2>

            <p className="text-sm sm:text-lg text-[#333336] dark:text-[#E2E8F0] font-normal leading-relaxed">
              At <strong className="text-[#1D1D1F] dark:text-white font-semibold">NEXORA</strong>, we stand at the threshold where intelligent automation and physical craftsmanship merge. Hardware shouldn&apos;t feel like a commodity—it should be a tactile, bespoke extension of human intelligence.
            </p>

            <p className="text-xs sm:text-base text-[#555558] dark:text-[#A1A1A6] font-normal leading-relaxed">
              My mission is to architect an ecosystem of high-precision wearables, acoustics, and autonomous gadgets that bring world-class engineering straight into your daily workflow.
            </p>

            {/* Full Vision Link (Centered on Mobile) */}
            <div className="pt-3 w-full flex justify-center lg:justify-start">
              <Link
                href="/founder"
                className="inline-flex items-center gap-1.5 px-7 py-3 rounded-full bg-[#1D1D1F] hover:bg-[#0071E3] text-white dark:bg-[#0071E3] dark:hover:bg-[#0077ED] font-medium text-sm tracking-wide transition-all shadow-sm hover:shadow-md hover:scale-105 active:scale-95"
              >
                <span>Read Full Vision</span>
                <ChevronRight className="w-4 h-4" />
              </Link>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

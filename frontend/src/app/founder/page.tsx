import React from 'react';
import Image from 'next/image';
import { fetchFounder } from '../../lib/api';
import { EmailIcon, LinkedInIcon, WhatsAppIcon, FacebookIcon } from '../../components/BrandIcons';

export const runtime = 'edge';
export const dynamic = 'force-dynamic';

export default async function FounderPage() {
  const founder = await fetchFounder();

  return (
    <div className="max-w-5xl mx-auto px-4 pt-28 sm:pt-36 pb-20 sm:pb-24 space-y-8 sm:space-y-12 bg-[#F7F4EE]">
      
      {/* Editorial Header */}
      <div className="text-center max-w-3xl mx-auto space-y-2 sm:space-y-3">
        <span className="text-xs font-mono uppercase tracking-widest text-[#0071E3] font-semibold block">
          Founder Profile
        </span>
        <h1 className="text-3xl sm:text-5xl font-semibold text-[#1D1D1F] tracking-tight">
          Architecting the Next Era
        </h1>
        <p className="text-sm sm:text-lg text-[#6E6E73] font-normal leading-relaxed">
          How founder <span className="text-[#1D1D1F] font-semibold">Jakaria Tanim</span> is converging autonomous AI workflows with bespoke physical engineering.
        </p>
      </div>

      {/* Main Profile Story Card */}
      <div className="rounded-2xl sm:rounded-3xl p-5 sm:p-14 bg-white border border-black/[0.06] shadow-[0_4px_30px_rgba(0,0,0,0.04)] grid grid-cols-1 md:grid-cols-12 gap-8 sm:gap-10 items-center">
        
        {/* Photo Stage */}
        <div className="md:col-span-5 flex flex-col items-center">
          <div className="relative w-64 sm:w-72 h-80 sm:h-96 max-w-full rounded-2xl sm:rounded-3xl overflow-hidden border border-black/[0.08] shadow-md bg-[#F5F5F7]">
            <Image
              src="/brand/founder_jakaria.png"
              alt="Jakaria Tanim"
              fill
              priority
              className="object-cover object-top"
            />
          </div>
          <div className="mt-4 text-center">
            <h3 className="text-lg sm:text-xl font-semibold text-[#1D1D1F] tracking-wide">
              {founder?.name || 'Jakaria Tanim'}
            </h3>
            <span className="text-xs font-mono text-[#0071E3] uppercase tracking-widest block mt-0.5 font-medium">
              {founder?.role || 'Founder & Chief Architect'}
            </span>
          </div>
        </div>

        {/* Narrative & Vision - Centered on Mobile, Left-aligned on Desktop */}
        <div className="md:col-span-7 space-y-5 text-center md:text-left flex flex-col items-center md:items-start">
          <div className="space-y-1.5">
            <span className="text-xs font-mono text-[#0071E3] uppercase tracking-widest font-semibold">
              Core Philosophy
            </span>
            <blockquote className="text-xl sm:text-2xl font-semibold text-[#1D1D1F] leading-snug">
              &ldquo;{founder?.vision || 'Bridging Autonomous AI Systems with Next-Generation Physical Hardware.'}&rdquo;
            </blockquote>
          </div>

          <p className="text-sm text-[#424245] leading-relaxed font-normal">
            {founder?.bio || 'Dedicated to crafting high-performance consumer gadgets that make intelligent systems tangible and accessible.'}
          </p>

          <div className="p-4 sm:p-5 rounded-2xl bg-[#F5F5F7] border border-black/[0.04] space-y-1.5 w-full text-left">
            <h4 className="text-xs font-mono uppercase tracking-widest text-[#1D1D1F] font-bold">
              Future Roadmap &amp; Ecosystem
            </h4>
            <p className="text-xs text-[#6E6E73] leading-relaxed font-normal">
              {founder?.futureGoals || 'Building an integrated ecosystem where wearables, acoustics, and aerial devices cooperate intuitively to elevate everyday human productivity.'}
            </p>
          </div>

          {/* Direct Channels - Email, WhatsApp, and LinkedIn */}
          <div className="pt-3 flex items-center justify-center md:justify-start gap-3.5">
            {/* 1. Email */}
            <a
              href="mailto:tanim@nexora.com"
              className="w-10 h-10 rounded-full flex items-center justify-center hover:scale-110 hover:shadow-lg transition-all duration-200"
              title="Email Founder (tanim@nexora.com)"
              aria-label="Email"
            >
              <EmailIcon className="w-10 h-10" />
            </a>

            {/* 2. WhatsApp (User-Uploaded Transparent Brand Logo) */}
            <a
              href="https://wa.me/8801640026177"
              target="_blank"
              rel="noreferrer"
              className="w-10 h-10 rounded-full flex items-center justify-center hover:scale-110 hover:shadow-lg transition-all duration-200"
              title="Chat on WhatsApp (+880 1640-026177)"
              aria-label="WhatsApp"
            >
              <WhatsAppIcon className="w-10 h-10" />
            </a>

            {/* 3. Facebook */}
            <a
              href="https://www.facebook.com/iamJakariaTanim"
              target="_blank"
              rel="noreferrer"
              className="w-10 h-10 rounded-full flex items-center justify-center hover:scale-110 hover:shadow-lg transition-all duration-200"
              title="Jakaria Tanim on Facebook"
              aria-label="Facebook"
            >
              <FacebookIcon className="w-10 h-10" />
            </a>

            {/* 4. LinkedIn */}
            <a
              href="https://www.linkedin.com"
              target="_blank"
              rel="noreferrer"
              className="w-10 h-10 rounded-full flex items-center justify-center hover:scale-110 hover:shadow-lg transition-all duration-200"
              title="Connect on LinkedIn"
              aria-label="LinkedIn"
            >
              <LinkedInIcon className="w-10 h-10" />
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}

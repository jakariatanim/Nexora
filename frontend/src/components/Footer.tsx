'use client';

import React from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { usePathname } from 'next/navigation';
import { Mail, MapPin } from 'lucide-react';

export const Footer: React.FC = () => {
  const pathname = usePathname();
  if (pathname?.startsWith('/myadminerapanel') || pathname?.startsWith('/app-demo')) return null;

  return (
    <footer className="border-t border-white/10 bg-[#0B132B] pt-16 pb-12 px-4 text-white">
      {/* 4-Column World-Class Architecture - 2x2 Grid on Mobile, 4 Columns on Desktop */}
      <div className="max-w-6xl mx-auto grid grid-cols-2 lg:grid-cols-4 items-start pb-12 border-b border-white/10 gap-x-6 gap-y-10 lg:gap-8">
        
        {/* Column 1: Brand & Vision (4 lines) */}
        <div className="space-y-4">
          <div className="h-7 flex items-center">
            <Link href="/" className="inline-flex items-center gap-2 group" aria-label="NEXORA Home">
              <div className="relative w-5 h-5 flex-shrink-0 transition-transform duration-500 group-hover:scale-105">
                <Image
                  src="/brand/nexora_icon_white_transparent.png"
                  alt="NEXORA"
                  fill
                  className="object-contain"
                />
              </div>
              <span className="text-xs sm:text-sm font-bold uppercase tracking-widest text-white leading-none">NEXORA</span>
            </Link>
          </div>
          <ul className="space-y-2.5 text-sm text-gray-300">
            <li className="h-6 flex items-center">
              <span>Step into the Next Era</span>
            </li>
            <li className="h-6 flex items-center">
              <span>Official Flagship Store</span>
            </li>
            <li className="h-6 flex items-center">
              <span>Crafted with Human Elegance</span>
            </li>
            <li className="h-6 flex items-center text-xs text-gray-300">
              <span>Directed by <strong className="text-white font-medium">Jakaria Tanim</strong></span>
            </li>
          </ul>
        </div>

        {/* Column 2: Flagship Hardware Categories (4 lines) */}
        <div className="space-y-4">
          <div className="h-7 flex items-center">
            <h4 className="text-xs sm:text-sm font-bold uppercase tracking-widest text-white leading-none">
              Flagship Hardware
            </h4>
          </div>
          <ul className="space-y-2.5 text-sm text-gray-300">
            <li className="h-6 flex items-center">
              <Link href="/explore?category=Smartphones" className="hover:text-white transition-colors">
                Flagship Smartphones
              </Link>
            </li>
            <li className="h-6 flex items-center">
              <Link href="/explore?category=Tablets" className="hover:text-white transition-colors">
                Tablets &amp; Laptops
              </Link>
            </li>
            <li className="h-6 flex items-center">
              <Link href="/explore?category=Smartwatches" className="hover:text-white transition-colors">
                Smartwatches &amp; Wearables
              </Link>
            </li>
            <li className="h-6 flex items-center">
              <Link href="/explore?category=Audio" className="hover:text-white transition-colors">
                Wireless Earbuds &amp; Audio
              </Link>
            </li>
          </ul>
        </div>

        {/* Column 3: Concierge & Client Care (4 lines, completely clean without green styling) */}
        <div className="space-y-4">
          <div className="h-7 flex items-center">
            <h4 className="text-xs sm:text-sm font-bold uppercase tracking-widest text-white leading-none">
              Concierge &amp; Care
            </h4>
          </div>
          <ul className="space-y-2.5 text-sm text-gray-300">
            <li className="h-6 flex items-center">
              <Link href="/track-order" className="hover:text-white transition-colors">
                Live Order Tracking
              </Link>
            </li>
            <li className="h-6 flex items-center">
              <Link href="/terms" className="hover:text-white transition-colors">
                1-Year Official Hardware Warranty
              </Link>
            </li>
            <li className="h-6 flex items-center">
              <Link href="/warranty-claim" className="hover:text-white transition-colors">
                7-Day Replacement Claim (RMA)
              </Link>
            </li>
            <li className="h-6 flex items-center">
              <Link href="/terms" className="hover:text-white transition-colors">
                Official Authenticity Guarantee
              </Link>
            </li>
          </ul>
        </div>

        {/* Column 4: Governance & Company (Right-aligned on desktop to match the social icons on the far right) */}
        <div className="space-y-4 text-left lg:text-right flex flex-col items-start lg:items-end">
          <div className="h-7 flex items-center justify-start lg:justify-end w-full">
            <h4 className="text-xs sm:text-sm font-bold uppercase tracking-widest text-white leading-none">
              Governance
            </h4>
          </div>
          <ul className="space-y-2.5 text-sm text-gray-300 w-full">
            <li className="h-6 flex items-center justify-start lg:justify-end">
              <Link href="/founder" className="hover:text-white transition-colors">
                Founder&apos;s Vision
              </Link>
            </li>
            <li className="h-6 flex items-center justify-start lg:justify-end">
              <Link href="/reviews" className="hover:text-white transition-colors">
                Customer Reviews
              </Link>
            </li>
            <li className="h-6 flex items-center justify-start lg:justify-end">
              <Link href="/terms" className="hover:text-white transition-colors">
                Terms &amp; Conditions
              </Link>
            </li>
            <li className="h-6 flex items-center justify-start lg:justify-end">
              <Link href="/privacy" className="hover:text-white transition-colors">
                Privacy Policy
              </Link>
            </li>
          </ul>
        </div>
      </div>

      {/* Bottom Bar: Copyright and Colorful Social Badges */}
      <div className="max-w-6xl mx-auto pt-6 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-gray-400">
        <div>
          &copy; {new Date().getFullYear()} NEXORA Technologies. All rights reserved.
        </div>

        {/* Colorful Brand Hover Social Icons (Uniform subtle default, blooms on hover) */}
        <div className="flex items-center gap-3">
          {/* WhatsApp */}
          <a
            href="https://wa.me/8801640026177"
            target="_blank"
            rel="noreferrer"
            className="w-8 h-8 rounded-full bg-white/5 border border-white/10 flex items-center justify-center text-gray-400 hover:text-white hover:bg-[#25D366] hover:border-[#25D366] hover:shadow-[0_0_14px_rgba(37,211,102,0.6)] hover:scale-110 transition-all duration-300"
            title="Chat on WhatsApp (+880 1640-026177)"
            aria-label="WhatsApp"
          >
            <svg className="w-4 h-4 fill-current transition-colors" viewBox="0 0 24 24">
              <path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-.868-2.031-.967-.272-.099-.47-.149-.669.149-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.372-.025-.521-.075-.148-.669-1.611-.916-2.206-.242-.579-.487-.501-.669-.51l-.57-.01c-.198 0-.52.074-.792.372s-1.04 1.016-1.04 2.479 1.065 2.876 1.213 3.074c.149.198 2.095 3.2 5.076 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.695.248-1.29.173-1.414z"/>
            </svg>
          </a>

          {/* Email */}
          <a
            href="mailto:support@nexora.com"
            className="w-8 h-8 rounded-full bg-white/5 border border-white/10 flex items-center justify-center text-gray-400 hover:text-white hover:bg-[#EA4335] hover:border-[#EA4335] hover:shadow-[0_0_14px_rgba(234,67,53,0.5)] hover:scale-110 transition-all duration-300"
            title="Email Support (support@nexora.com)"
            aria-label="Email"
          >
            <Mail className="w-4 h-4" />
          </a>

          {/* Google Maps */}
          <a
            href="https://maps.google.com/?q=Dhaka,Bangladesh"
            target="_blank"
            rel="noreferrer"
            className="w-8 h-8 rounded-full bg-white/5 border border-white/10 flex items-center justify-center text-gray-400 hover:text-white hover:bg-[#34A853] hover:border-[#34A853] hover:shadow-[0_0_14px_rgba(52,168,83,0.5)] hover:scale-110 transition-all duration-300"
            title="Dhaka Showroom on Google Maps"
            aria-label="Google Maps"
          >
            <MapPin className="w-4 h-4" />
          </a>

          {/* LinkedIn */}
          <a
            href="https://www.linkedin.com"
            target="_blank"
            rel="noreferrer"
            className="w-8 h-8 rounded-full bg-white/5 border border-white/10 flex items-center justify-center text-gray-400 hover:text-white hover:bg-[#0A66C2] hover:border-[#0A66C2] hover:shadow-[0_0_14px_rgba(10,102,194,0.5)] hover:scale-110 transition-all duration-300"
            title="Connect on LinkedIn"
            aria-label="LinkedIn"
          >
            <svg className="w-3.5 h-3.5 fill-current" viewBox="0 0 24 24">
              <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z" />
            </svg>
          </a>

          {/* Telegram */}
          <a
            href="https://t.me"
            target="_blank"
            rel="noreferrer"
            className="w-8 h-8 rounded-full bg-white/5 border border-white/10 flex items-center justify-center text-gray-400 hover:text-white hover:bg-[#229ED9] hover:border-[#229ED9] hover:shadow-[0_0_14px_rgba(34,158,217,0.5)] hover:scale-110 transition-all duration-300"
            title="Telegram Community"
            aria-label="Telegram"
          >
            <svg className="w-3.5 h-3.5 fill-current" viewBox="0 0 24 24">
              <path d="M12 0c-6.627 0-12 5.373-12 12s5.373 12 12 12 12-5.373 12-12-5.373-12-12-12zm5.894 8.221l-1.97 9.28c-.145.658-.537.818-1.084.508l-3-2.21-1.446 1.394c-.14.18-.357.34-.635.34l.213-3.053 5.56-5.023c.242-.213-.054-.333-.373-.121l-6.871 4.326-2.962-.924c-.643-.204-.657-.643.136-.953l11.57-4.461c.535-.194 1.006.128.862.867z" />
            </svg>
          </a>

          {/* Facebook */}
          <a
            href="https://www.facebook.com/iamJakariaTanim"
            target="_blank"
            rel="noreferrer"
            className="w-8 h-8 rounded-full bg-white/5 border border-white/10 flex items-center justify-center text-gray-400 hover:text-white hover:bg-[#1877F2] hover:border-[#1877F2] hover:shadow-[0_0_14px_rgba(24,119,242,0.6)] hover:scale-110 transition-all duration-300"
            title="Jakaria Tanim on Facebook"
            aria-label="Facebook"
          >
            <svg className="w-4 h-4 fill-current transition-colors" viewBox="0 0 24 24">
              <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z" />
            </svg>
          </a>
        </div>
      </div>
    </footer>
  );
};

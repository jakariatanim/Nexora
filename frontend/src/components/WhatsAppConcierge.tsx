'use client';

import React, { useState } from 'react';
import { MessageCircle, X } from 'lucide-react';

export const WhatsAppConcierge: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const phoneNumber = '8801640026177';
  const message = 'Hello NEXORA Concierge, I would like to inquire about your flagship hardware collection.';

  const handleOpenWhatsApp = () => {
    const url = `https://wa.me/${phoneNumber}?text=${encodeURIComponent(message)}`;
    window.open(url, '_blank', 'noopener,noreferrer');
  };

  return (
    <div className="fixed bottom-20 md:bottom-6 right-4 md:right-6 z-40 flex flex-col items-end print:hidden">
      {/* Expanded Quick Help Card */}
      {isOpen && (
        <div className="mb-3 w-72 rounded-2xl bg-white/95 dark:bg-[#151D30]/95 backdrop-blur-md border border-black/10 dark:border-white/10 p-4 shadow-2xl animate-fade-in text-left">
          <div className="flex items-center justify-between pb-2 border-b border-black/[0.06] dark:border-white/10">
            <div className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse" />
              <span className="text-xs font-semibold text-[#1D1D1F] dark:text-white">NEXORA Direct Concierge</span>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="text-gray-400 hover:text-gray-600 dark:hover:text-white"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
          <p className="text-xs text-gray-600 dark:text-gray-300 mt-2">
            Speak directly with our Apple, Sony & Flagship Gadget Specialists for instant order support and BTRC warranty queries.
          </p>
          <button
            onClick={handleOpenWhatsApp}
            className="w-full mt-3 py-2.5 px-3 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-medium text-xs flex items-center justify-center gap-2 shadow-md transition-all active:scale-[0.98]"
          >
            <MessageCircle className="w-4 h-4" />
            <span>Chat on WhatsApp (+880 1640-026177)</span>
          </button>
        </div>
      )}

      {/* Floating Toggle Button */}
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        className="group relative flex items-center gap-2.5 px-4 py-3 rounded-full bg-emerald-600 hover:bg-emerald-500 text-white shadow-lg hover:shadow-emerald-600/30 transition-all duration-300 active:scale-95"
        title="Direct WhatsApp Support"
        aria-label="Direct WhatsApp Support"
      >
        <span className="relative flex h-3 w-3">
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-white opacity-75"></span>
          <span className="relative inline-flex rounded-full h-3 w-3 bg-white"></span>
        </span>
        <MessageCircle className="w-5 h-5 transition-transform group-hover:scale-110" />
        <span className="text-xs font-semibold tracking-wide hidden sm:inline">Concierge Support</span>
      </button>
    </div>
  );
};

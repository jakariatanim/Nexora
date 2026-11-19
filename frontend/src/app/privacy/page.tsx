import React from 'react';

export default function PrivacyPage() {
  return (
    <div className="max-w-4xl mx-auto px-4 pt-36 pb-24 space-y-8">
      <div className="space-y-2">
        <span className="text-xs font-mono text-[#0071E3] dark:text-[#38BDF8] uppercase tracking-widest font-semibold block">
          Legal // Privacy Policy
        </span>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-[#1D1D1F] dark:text-white tracking-tight">
          Privacy Policy
        </h1>
        <p className="text-xs text-[#86868B] dark:text-slate-400 font-mono">
          Effective: November 2026 &bull; NEXORA Technologies
        </p>
      </div>

      <div className="space-y-8 text-sm sm:text-base leading-relaxed p-8 sm:p-12 rounded-3xl bg-white dark:bg-[#121624] border border-black/10 dark:border-white/10 shadow-sm">
        <section className="space-y-2.5">
          <h2 className="text-lg font-bold text-[#1D1D1F] dark:text-white">
            1. Data Collection &amp; Telemetry
          </h2>
          <p className="text-[#333336] dark:text-[#CBD5E1]">
            At NEXORA, we respect your privacy with the same rigor we engineer our hardware. We only collect the minimal information necessary to deliver your gadget (name, phone number, and delivery address) and authenticate your membership profile.
          </p>
        </section>

        <section className="space-y-2.5">
          <h2 className="text-lg font-bold text-[#1D1D1F] dark:text-white">
            2. No Third-Party Sharing
          </h2>
          <p className="text-[#333336] dark:text-[#CBD5E1]">
            We do not sell, rent, or trade your personal data with third-party advertising brokers. Your information remains strictly within our encrypted order routing systems.
          </p>
        </section>

        <section className="space-y-2.5">
          <h2 className="text-lg font-bold text-[#1D1D1F] dark:text-white">
            3. Cryptographic Transaction Security
          </h2>
          <p className="text-[#333336] dark:text-[#CBD5E1]">
            All checkout channels, including bKash, Nagad, Cash on Delivery (COD), and International Card transactions, utilize industry-standard TLS cryptographic protocols to ensure total integrity and customer confidentiality.
          </p>
        </section>

        <section className="space-y-2.5">
          <h2 className="text-lg font-bold text-[#1D1D1F] dark:text-white">
            4. Contact Our Data Governance Team
          </h2>
          <p className="text-[#333336] dark:text-[#CBD5E1]">
            If you have questions regarding personal records or wish to request data erasure, reach our team directly at{' '}
            <a href="mailto:support@nexora.com" className="text-[#0071E3] dark:text-[#38BDF8] underline font-medium">
              support@nexora.com
            </a>{' '}
            or WhatsApp{' '}
            <a href="https://wa.me/8801640026177" target="_blank" rel="noreferrer" className="text-[#0071E3] dark:text-[#38BDF8] underline font-medium">
              +880 1640-026177
            </a>.
          </p>
        </section>
      </div>
    </div>
  );
}

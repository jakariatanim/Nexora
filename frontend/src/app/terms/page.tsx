import React from 'react';

export default function TermsPage() {
  return (
    <div className="max-w-4xl mx-auto px-4 pt-36 pb-24 space-y-8">
      <div className="space-y-2">
        <span className="text-xs font-mono text-[#0071E3] dark:text-[#38BDF8] uppercase tracking-widest font-semibold block">
          Legal // Terms &amp; Conditions
        </span>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-[#1D1D1F] dark:text-white tracking-tight">
          Terms &amp; Conditions
        </h1>
        <p className="text-xs text-[#86868B] dark:text-slate-400 font-mono">
          Last updated: November 2026 &bull; NEXORA Technologies
        </p>
      </div>

      <div className="space-y-8 text-sm sm:text-base leading-relaxed p-8 sm:p-12 rounded-3xl bg-white dark:bg-[#121624] border border-black/10 dark:border-white/10 shadow-sm">
        <section className="space-y-2.5">
          <h2 className="text-lg font-bold text-[#1D1D1F] dark:text-white">
            1. Introduction &amp; Architectural Governance
          </h2>
          <p className="text-[#333336] dark:text-[#CBD5E1]">
            Welcome to NEXORA (&ldquo;Company&rdquo;, &ldquo;we&rdquo;, &ldquo;our&rdquo;), founded by Jakaria Tanim. By accessing our platform, purchasing hardware, or utilizing our services, you agree to comply with and be bound by the following terms.
          </p>
        </section>

        <section className="space-y-2.5">
          <h2 className="text-lg font-bold text-[#1D1D1F] dark:text-white">
            2. Orders &amp; Nationwide Delivery
          </h2>
          <p className="text-[#333336] dark:text-[#CBD5E1]">
            All hardware reservations placed via bKash, Nagad, Cash on Delivery (COD), or International Card are subject to stock availability. Upon confirmation, a unique tracking code (e.g., NX-2026-XXXX) is issued for real-time dispatch monitoring across all 64 districts in Bangladesh.
          </p>
        </section>

        <section className="space-y-2.5">
          <h2 className="text-lg font-bold text-[#1D1D1F] dark:text-white">
            3. Warranty &amp; Replacement
          </h2>
          <p className="text-[#333336] dark:text-[#CBD5E1]">
            Every authentic NEXORA device carries our 1-Year Official Hardware Warranty against manufacturing defects and a 7-Day Replacement Policy from delivery date.
          </p>
        </section>

        <section className="space-y-2.5">
          <h2 className="text-lg font-bold text-[#1D1D1F] dark:text-white">
            4. Intellectual Property
          </h2>
          <p className="text-[#333336] dark:text-[#CBD5E1]">
            The NEXORA trademarks, logotypes, bespoke hardware designs, and code architectures are the intellectual property of Jakaria Tanim and NEXORA Technologies. Unauthorized commercial replication is strictly prohibited.
          </p>
        </section>
      </div>
    </div>
  );
}

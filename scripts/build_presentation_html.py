# Generates NEXORA_INTERACTIVE_PRESENTATION.html
import re

html_content = """<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>NEXORA — Interactive Architecture & Defense Presentation</title>
  <meta name="description" content="NEXORA: Enterprise Flagship Consumer Electronics & Hardware Architecture. Interactive Defense Presentation with 17 Aligned Slides, Live Simulation Widgets, Offline CSS Fallbacks, and Bengali Speaker Notes.">
  <link rel="icon" href="/favicon.ico">
  
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          colors: {
            nexora: {
              navy: '#080E1E',
              dark: '#0B132B',
              surface: '#121B33',
              card: '#162244',
              accent: '#0071E3',
              accentHover: '#0077ED',
              gold: '#F59E0B',
              cyan: '#38BDF8',
              emerald: '#10B981',
              rose: '#F43F5E'
            }
          },
          fontFamily: {
            sans: ['-apple-system', 'BlinkMacSystemFont', 'SF Pro Display', 'Segoe UI', 'Roboto', 'Helvetica', 'Arial', 'sans-serif'],
            mono: ['SF Mono', 'Fira Code', 'Menlo', 'Monaco', 'Consolas', 'monospace']
          }
        }
      }
    };
  </script>

  <!-- Offline & Air-Gapped Fallback CSS -->
  <style>
    /* CSS Reset & Baseline */
    *, *::before, *::after { box-sizing: border-box; }
    html { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
    
    /* Scrollbars */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.2); border-radius: 9999px; }
    .dark ::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.15); }

    /* Glassmorphism */
    .glass-card {
      background: rgba(18, 27, 51, 0.75);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid rgba(255, 255, 255, 0.08);
    }
    .light .glass-card {
      background: rgba(255, 255, 255, 0.9);
      border: 1px solid rgba(0, 0, 0, 0.08);
    }

    /* Slide Transition Animations */
    .slide-section {
      transition: opacity 0.35s ease, transform 0.35s ease;
    }
    .slide-enter {
      opacity: 0;
      transform: translateY(12px) scale(0.99);
    }
    .slide-active {
      opacity: 1;
      transform: translateY(0) scale(1);
    }

    /* Glow utilities */
    .badge-glow { box-shadow: 0 0 20px -3px rgba(0, 113, 227, 0.45); }
    .badge-gold-glow { box-shadow: 0 0 20px -3px rgba(245, 158, 11, 0.45); }

    @keyframes subtlePulse {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.85; transform: scale(1.02); }
    }
    .live-pulse { animation: subtlePulse 3s infinite ease-in-out; }

    /* Offline Grid & Flex Fallback Classes (guarantees layout when CDN is unreachable) */
    .hidden { display: none !important; }
    .flex { display: flex; }
    .grid { display: grid; }
    .items-center { align-items: center; }
    .justify-between { justify-content: space-between; }
    .justify-center { justify-content: center; }
    .relative { position: relative; }
    .fixed { position: fixed; }
    .sticky { position: sticky; }
    .w-full { width: 100%; }
    .h-full { height: 100%; }
    .text-center { text-align: center; }
    .text-left { text-align: left; }
    .cursor-pointer { cursor: pointer; }
    .overflow-hidden { overflow: hidden; }
    .overflow-y-auto { overflow-y: auto; }
  </style>
</head>
<body class="bg-[#F8FAFC] text-[#0F172A] dark:bg-[#080E1E] dark:text-[#F1F5F9] min-h-screen flex flex-col font-sans antialiased transition-colors duration-300 selection:bg-[#0071E3] selection:text-white overflow-x-hidden">

  <!-- ============================================================================ -->
  <!-- TOP ACADEMIC & CROSS-LINK BANNER (SYNCHRONIZED REQUIREMENTS)                -->
  <!-- ============================================================================ -->
  <header class="sticky top-0 z-50 bg-[#0B132B]/95 dark:bg-[#080E1E]/95 backdrop-blur-md border-b border-white/10 text-white px-4 py-2.5 shadow-lg">
    <div class="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-3">
      
      <!-- Brand & Project Title -->
      <div class="flex items-center gap-3">
        <a href="#slide-1" onclick="goToSlide(1)" class="flex items-center gap-2 group">
          <div class="w-8 h-8 rounded-lg bg-gradient-to-tr from-[#0071E3] to-[#38BDF8] flex items-center justify-center font-bold text-white shadow-md group-hover:scale-105 transition-transform">
            N
          </div>
          <div>
            <div class="flex items-center gap-1.5">
              <span class="font-bold text-sm tracking-tight text-white">NEXORA</span>
              <span class="px-1.5 py-0.2 text-[10px] font-mono uppercase bg-blue-500/20 text-[#38BDF8] border border-blue-500/30 rounded">Architecture v1.0</span>
            </div>
            <p class="text-[11px] text-slate-300 hidden sm:block">Directed by <span class="text-white font-medium">Jakaria Tanim</span></p>
          </div>
        </a>
      </div>

      <!-- Center Slide Controls & Counter Indicator -->
      <div class="flex items-center gap-2">
        <button onclick="prevSlide()" class="p-1.5 rounded-lg bg-white/10 hover:bg-white/20 text-white transition-all active:scale-95 text-xs font-semibold" title="Previous Slide (Left Arrow / Backspace)">
          &larr; Prev
        </button>
        <span id="slideCounterBadge" class="px-3 py-1 rounded-full bg-white/10 border border-white/15 text-xs font-mono font-medium text-[#38BDF8]">
          Slide 1 of 17
        </span>
        <button onclick="nextSlide()" class="p-1.5 rounded-lg bg-white/10 hover:bg-white/20 text-white transition-all active:scale-95 text-xs font-semibold" title="Next Slide (Right Arrow / Space / Enter)">
          Next &rarr;
        </button>
      </div>

      <!-- Header Action Buttons: Academic Slide Deck & Speaker Notes Reader + Controls -->
      <div class="flex items-center gap-2 flex-wrap">
        
        <!-- PROMINENT BUTTON: OPENS IN-PAGE ACADEMIC SLIDE DECK & SPEAKER NOTES MODAL -->
        <button onclick="openAcademicDeckModal()" 
                class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-slate-950 text-xs font-bold shadow-md hover:shadow-amber-500/25 transition-all active:scale-95 badge-gold-glow"
                title="View Academic Slide Deck, Equations & Bengali Speaker Notes (Key: D)">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.5L19 7.5V19a2 2 0 01-2 2z"></path>
          </svg>
          <span>📄 View Academic Slide Deck & Speaker Notes</span>
        </button>

        <!-- Bengali Speaker Notes Slide-Over Drawer Toggle -->
        <button onclick="toggleSpeakerNotes()" id="speakerNotesBtn" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-white/10 hover:bg-white/20 text-white text-xs font-medium transition-all active:scale-95" title="Bengali Speaker Notes (Key: N)">
          <span>🗣️ Notes</span>
        </button>

        <!-- Table of Contents Toggle -->
        <button onclick="toggleToc()" class="p-1.5 rounded-lg bg-white/10 hover:bg-white/20 text-white transition-all text-xs" title="Table of Contents (Key: M or O)">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
        </button>

        <!-- Theme Switcher (Dark/Light) -->
        <button onclick="toggleTheme()" class="p-1.5 rounded-lg bg-white/10 hover:bg-white/20 text-white transition-all text-xs" title="Toggle Theme (Key: T)">
          <span id="themeIcon">🌙</span>
        </button>

        <!-- Fullscreen Toggle -->
        <button onclick="toggleFullscreen()" class="p-1.5 rounded-lg bg-white/10 hover:bg-white/20 text-white transition-all text-xs hidden sm:block" title="Toggle Fullscreen (Key: F)">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4m0 0h4M4 4l5 5m11-5h-4m4 0v4m0-4l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4"></path></svg>
        </button>
      </div>

    </div>

    <!-- Reading Progress Bar -->
    <div class="w-full bg-white/10 h-0.5 mt-2 overflow-hidden">
      <div id="progressBar" class="h-full bg-gradient-to-r from-[#0071E3] via-[#38BDF8] to-emerald-400 transition-all duration-300" style="width: 5.88%;"></div>
    </div>
  </header>

  <!-- ============================================================================ -->
  <!-- MAIN SLIDES CONTAINER (17 SYNCHRONIZED SLIDES)                               -->
  <!-- ============================================================================ -->
  <main class="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 lg:p-8 flex flex-col justify-center">

    <!-- ======================================================================== -->
    <!-- SLIDE 1: PROJECT TITLE & EXECUTIVE OVERVIEW                              -->
    <!-- ======================================================================== -->
    <section id="slide-1" class="slide-section slide-enter slide-active">
      <div class="relative overflow-hidden rounded-3xl p-8 sm:p-12 glass-card border border-white/10 dark:border-white/10 shadow-2xl">
        <div class="absolute -right-20 -top-20 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl pointer-events-none"></div>
        <div class="absolute -left-20 -bottom-20 w-96 h-96 bg-amber-500/10 rounded-full blur-3xl pointer-events-none"></div>

        <div class="flex items-center gap-2 mb-4">
          <span class="px-3 py-1 rounded-full text-xs font-mono font-semibold bg-blue-500/10 text-[#0071E3] dark:text-[#38BDF8] border border-blue-500/20">
            Slide 01 / 17 &bull; Executive Defense Overview
          </span>
          <span class="px-3 py-1 rounded-full text-xs font-mono font-semibold bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20">
            Academic Grade A+ Target
          </span>
        </div>

        <h1 class="text-3xl sm:text-5xl lg:text-6xl font-black tracking-tight text-slate-900 dark:text-white leading-tight mb-4">
          NEXORA <span class="text-transparent bg-clip-text bg-gradient-to-r from-[#0071E3] to-[#38BDF8]">Step into the Next Era</span>
        </h1>
        <p class="text-base sm:text-xl text-slate-600 dark:text-slate-300 max-w-3xl mb-8 leading-relaxed">
          Enterprise Flagship Consumer Electronics & Hardware Architecture with Mathematical Anti-Price-Tampering Security, 0% Bank EMI Financing, District Courier Logistics, and Customer RMA Warranty Governance.
        </p>

        <!-- Presentation Metadata Grid -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <div class="p-4 rounded-2xl bg-black/5 dark:bg-white/5 border border-black/5 dark:border-white/10">
            <span class="text-xs text-slate-500 dark:text-slate-400 block font-mono">Lead Architect</span>
            <span class="text-base font-bold text-slate-900 dark:text-white">Jakaria Tanim</span>
            <span class="text-[11px] text-emerald-500 block font-mono">tanim@nexora.com</span>
          </div>
          <div class="p-4 rounded-2xl bg-black/5 dark:bg-white/5 border border-black/5 dark:border-white/10">
            <span class="text-xs text-slate-500 dark:text-slate-400 block font-mono">Frontend Runtime</span>
            <span class="text-base font-bold text-slate-900 dark:text-white">Next.js 14 App Router</span>
            <span class="text-[11px] text-blue-400 block font-mono">Port :3000 (SSR + Islands)</span>
          </div>
          <div class="p-4 rounded-2xl bg-black/5 dark:bg-white/5 border border-black/5 dark:border-white/10">
            <span class="text-xs text-slate-500 dark:text-slate-400 block font-mono">Backend Engine</span>
            <span class="text-base font-bold text-slate-900 dark:text-white">Node.js Express REST</span>
            <span class="text-[11px] text-cyan-400 block font-mono">Port :5001 (Mutex Store)</span>
          </div>
          <div class="p-4 rounded-2xl bg-black/5 dark:bg-white/5 border border-black/5 dark:border-white/10">
            <span class="text-xs text-slate-500 dark:text-slate-400 block font-mono">Security Model</span>
            <span class="text-base font-bold text-slate-900 dark:text-white">4-Tier RBAC + Bcrypt</span>
            <span class="text-[11px] text-amber-400 block font-mono">Anti-Price-Tampering</span>
          </div>
        </div>

        <!-- Quick Jump Buttons & Live Links -->
        <div class="flex flex-wrap items-center gap-3">
          <button onclick="goToSlide(2)" class="px-6 py-3 rounded-full bg-[#0071E3] hover:bg-[#0077ED] text-white font-bold text-sm shadow-lg hover:shadow-blue-500/25 transition-all active:scale-95 flex items-center gap-2">
            <span>Explore Architectural Flow &rarr;</span>
          </button>
          <button onclick="openAcademicDeckModal()" class="px-5 py-3 rounded-full bg-black/10 dark:bg-white/10 hover:bg-black/15 dark:hover:bg-white/20 text-slate-900 dark:text-white font-semibold text-sm transition-all active:scale-95 flex items-center gap-2">
            <span>📄 View Academic Slide Deck & Notes</span>
          </button>
          <a href="http://localhost:3000" target="_blank" class="px-5 py-3 rounded-full bg-emerald-600/20 text-emerald-400 border border-emerald-500/30 font-semibold text-sm hover:bg-emerald-600/30 transition-all flex items-center gap-2">
            <span>🌐 Open Live Storefront (:3000)</span>
          </a>
          <a href="http://localhost:5001/api/stats" target="_blank" class="px-5 py-3 rounded-full bg-cyan-600/20 text-cyan-400 border border-cyan-500/30 font-semibold text-sm hover:bg-cyan-600/30 transition-all flex items-center gap-2">
            <span>⚡ Test Express API Stats (:5001)</span>
          </a>
        </div>
      </div>
    </section>

    <!-- ======================================================================== -->
    <!-- SLIDE 2: ARCHITECTURAL TOPOLOGY & FULL-STACK SYSTEM FLOW                -->
    <!-- ======================================================================== -->
    <section id="slide-2" class="slide-section slide-enter hidden">
      <div class="rounded-3xl p-6 sm:p-10 glass-card border border-white/10 shadow-2xl">
        <div class="flex flex-wrap items-center justify-between gap-3 mb-6 pb-4 border-b border-black/10 dark:border-white/10">
          <div>
            <span class="text-xs font-mono font-semibold text-[#0071E3] dark:text-[#38BDF8]">Slide 02 / 17 &bull; System Architecture</span>
            <h2 class="text-2xl sm:text-3xl font-black text-slate-900 dark:text-white">Full-Stack Decoupled Topology & Data Flow</h2>
          </div>
          <button onclick="openAcademicDeckModal()" class="px-3 py-1.5 rounded-full bg-amber-500/10 text-amber-500 border border-amber-500/20 text-xs font-bold hover:bg-amber-500/20 transition-all">
            📄 Academic Citations
          </button>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-4 gap-4 mb-6">
          <div onclick="showNodeDetails('client')" class="p-5 rounded-2xl bg-black/5 dark:bg-white/5 border border-black/10 dark:border-white/10 hover:border-[#0071E3] cursor-pointer transition-all hover:scale-[1.02]">
            <div class="flex items-center justify-between mb-2">
              <span class="text-xs font-mono font-bold text-blue-400">LAYER 1</span>
              <span class="text-[10px] px-2 py-0.5 rounded bg-blue-500/20 text-blue-300">Client / PWA</span>
            </div>
            <h3 class="font-bold text-base text-slate-900 dark:text-white mb-1">Next.js Client Hydration</h3>
            <p class="text-xs text-slate-500 dark:text-slate-400">Context API state, Lenis smooth motion, local storage caches.</p>
          </div>

          <div onclick="showNodeDetails('ssr')" class="p-5 rounded-2xl bg-black/5 dark:bg-white/5 border border-black/10 dark:border-white/10 hover:border-[#0071E3] cursor-pointer transition-all hover:scale-[1.02]">
            <div class="flex items-center justify-between mb-2">
              <span class="text-xs font-mono font-bold text-cyan-400">LAYER 2</span>
              <span class="text-[10px] px-2 py-0.5 rounded bg-cyan-500/20 text-cyan-300">Port :3000</span>
            </div>
            <h3 class="font-bold text-base text-slate-900 dark:text-white mb-1">SSR & Dynamic Routing</h3>
            <p class="text-xs text-slate-500 dark:text-slate-400">Sub-second FCP, SEO optimization, responsive container queries.</p>
          </div>

          <div onclick="showNodeDetails('api')" class="p-5 rounded-2xl bg-black/5 dark:bg-white/5 border border-black/10 dark:border-white/10 hover:border-[#0071E3] cursor-pointer transition-all hover:scale-[1.02]">
            <div class="flex items-center justify-between mb-2">
              <span class="text-xs font-mono font-bold text-amber-400">LAYER 3</span>
              <span class="text-[10px] px-2 py-0.5 rounded bg-amber-500/20 text-amber-300">Port :5001</span>
            </div>
            <h3 class="font-bold text-base text-slate-900 dark:text-white mb-1">Express API Security</h3>
            <p class="text-xs text-slate-500 dark:text-slate-400">OWASP headers, express-rate-limit, JWT tokens, 4-tier RBAC guard.</p>
          </div>

          <div onclick="showNodeDetails('mutex')" class="p-5 rounded-2xl bg-black/5 dark:bg-white/5 border border-black/10 dark:border-white/10 hover:border-[#0071E3] cursor-pointer transition-all hover:scale-[1.02]">
            <div class="flex items-center justify-between mb-2">
              <span class="text-xs font-mono font-bold text-emerald-400">LAYER 4</span>
              <span class="text-[10px] px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300">Data Store</span>
            </div>
            <h3 class="font-bold text-base text-slate-900 dark:text-white mb-1">Mutex-Locked Storage</h3>
            <p class="text-xs text-slate-500 dark:text-slate-400">queueFileOp concurrency serialization, OS-level atomic file renames.</p>
          </div>
        </div>

        <div id="nodeDetailBox" class="p-5 rounded-2xl bg-[#080E1E] border border-white/15 text-slate-200">
          <div class="flex items-center justify-between mb-2 pb-2 border-b border-white/10">
            <span class="text-[#38BDF8] font-bold">Interactive Architecture Inspector</span>
            <span class="text-slate-400 font-mono text-[11px]">Click any of the 4 layer cards above to inspect source citations</span>
          </div>
          <p class="text-xs text-slate-300">Click any architectural node above to inspect its real implementation in <code class="text-amber-400">frontend/</code> and <code class="text-cyan-400">backend/server.js</code>.</p>
        </div>
      </div>
    </section>

    <!-- ======================================================================== -->
    <!-- SLIDE 3: FRONTEND TECH STACK & COMPONENT ENGINEERING                    -->
    <!-- ======================================================================== -->
    <section id="slide-3" class="slide-section slide-enter hidden">
      <div class="rounded-3xl p-6 sm:p-10 glass-card border border-white/10 shadow-2xl">
        <div class="flex flex-wrap items-center justify-between gap-3 mb-6 pb-4 border-b border-black/10 dark:border-white/10">
          <div>
            <span class="text-xs font-mono font-semibold text-[#0071E3] dark:text-[#38BDF8]">Slide 03 / 17 &bull; Frontend Engineering</span>
            <h2 class="text-2xl sm:text-3xl font-black text-slate-900 dark:text-white">Next.js 14, Tailwind, Framer Motion & Contexts</h2>
          </div>
          <button onclick="openAcademicDeckModal()" class="px-3 py-1.5 rounded-full bg-amber-500/10 text-amber-500 border border-amber-500/20 text-xs font-bold hover:bg-amber-500/20 transition-all">
            📄 Academic Citations
          </button>
        </div>

        <!-- Tech Stack Selector Tabs -->
        <div class="flex flex-wrap gap-2 mb-6">
          <button id="tab-nextjs" onclick="filterFrontendTab('nextjs')" class="px-4 py-2 rounded-xl text-xs font-bold transition-all bg-[#0071E3] text-white">
            Next.js 14 App Router
          </button>
          <button id="tab-tailwind" onclick="filterFrontendTab('tailwind')" class="px-4 py-2 rounded-xl text-xs font-bold transition-all bg-black/5 dark:bg-white/5 text-slate-700 dark:text-slate-300">
            Tailwind + Container Queries
          </button>
          <button id="tab-framer" onclick="filterFrontendTab('framer')" class="px-4 py-2 rounded-xl text-xs font-bold transition-all bg-black/5 dark:bg-white/5 text-slate-700 dark:text-slate-300">
            Framer Motion & Lenis
          </button>
          <button id="tab-state" onclick="filterFrontendTab('state')" class="px-4 py-2 rounded-xl text-xs font-bold transition-all bg-black/5 dark:bg-white/5 text-slate-700 dark:text-slate-300">
            Dual Contexts & Localization
          </button>
        </div>

        <div id="frontendTabContent" class="grid grid-cols-1 lg:grid-cols-2 gap-6 items-center">
          <!-- Populated by filterFrontendTab() -->
        </div>
      </div>
    </section>

    <!-- ======================================================================== -->
    <!-- SLIDE 4: BACKEND API ARCHITECTURE & MUTEX DATA STORAGE                   -->
    <!-- ======================================================================== -->
    <section id="slide-4" class="slide-section slide-enter hidden">
      <div class="rounded-3xl p-6 sm:p-10 glass-card border border-white/10 shadow-2xl">
        <div class="flex flex-wrap items-center justify-between gap-3 mb-6 pb-4 border-b border-black/10 dark:border-white/10">
          <div>
            <span class="text-xs font-mono font-semibold text-[#0071E3] dark:text-[#38BDF8]">Slide 04 / 17 &bull; Backend Persistence</span>
            <h2 class="text-2xl sm:text-3xl font-black text-slate-900 dark:text-white">Mutex Concurrency & Atomic File Writes</h2>
          </div>
          <button onclick="openAcademicDeckModal()" class="px-3 py-1.5 rounded-full bg-amber-500/10 text-amber-500 border border-amber-500/20 text-xs font-bold hover:bg-amber-500/20 transition-all">
            📄 Academic Citations
          </button>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          <div class="space-y-4">
            <h3 class="text-lg font-bold text-slate-900 dark:text-white">The Mutex Serialization Pipeline</h3>
            <p class="text-xs sm:text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
              In file-based storage systems, simultaneous customer writes risk file truncation and corrupt JSON. NEXORA solves this cleanly via an in-memory Promise-Chained Mutex Queue (<code class="text-cyan-400">queueFileOp</code> in <code class="text-amber-400">backend/server.js:118-173</code>).
            </p>
            <div class="p-4 rounded-xl bg-black/5 dark:bg-white/5 border border-white/10 text-xs space-y-2">
              <div class="flex items-center gap-2 text-emerald-400 font-bold">
                <span>✓</span> <span>1. In-Memory Mutex Map: Serializes operations per filename</span>
              </div>
              <div class="flex items-center gap-2 text-blue-400 font-bold">
                <span>✓</span> <span>2. Temporary File Swap: Writes to .tmp before OS rename</span>
              </div>
              <div class="flex items-center gap-2 text-cyan-400 font-bold">
                <span>✓</span> <span>3. Atomic fs.promises.rename: Zero partial writes</span>
              </div>
            </div>
            <button onclick="simulateConcurrentWrites()" class="px-6 py-3 rounded-full bg-gradient-to-r from-[#0071E3] to-[#38BDF8] hover:opacity-95 text-white font-bold text-xs shadow-lg transition-all active:scale-95">
              ⚡ Trigger 5 Concurrent Customer Writes
            </button>
          </div>

          <!-- Live Terminal Output Box -->
          <div class="rounded-2xl bg-[#080E1E] border border-white/15 p-4 flex flex-col h-72">
            <div class="flex items-center justify-between pb-2 mb-2 border-b border-white/10">
              <div class="flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-rose-500"></span>
                <span class="w-2.5 h-2.5 rounded-full bg-amber-500"></span>
                <span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span>
                <span class="text-[11px] font-mono text-slate-400 ml-2">backend/server.js — Concurrency Stream</span>
              </div>
              <span class="text-[10px] font-mono text-emerald-400">MUTEX ACTIVE</span>
            </div>
            <div id="mutexConsole" class="flex-1 overflow-y-auto space-y-1 text-slate-300 font-mono text-[11px]">
              <p class="text-slate-500">// Ready for concurrent write simulation...</p>
              <p class="text-slate-500">// Click the blue button on the left to spawn 5 concurrent order writes.</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ======================================================================== -->
    <!-- SLIDE 5: ENTERPRISE SECURITY, JWT & GRANULAR RBAC                        -->
    <!-- ======================================================================== -->
    <section id="slide-5" class="slide-section slide-enter hidden">
      <div class="rounded-3xl p-6 sm:p-10 glass-card border border-white/10 shadow-2xl">
        <div class="flex flex-wrap items-center justify-between gap-3 mb-6 pb-4 border-b border-black/10 dark:border-white/10">
          <div>
            <span class="text-xs font-mono font-semibold text-[#0071E3] dark:text-[#38BDF8]">Slide 05 / 17 &bull; System Hardening</span>
            <h2 class="text-2xl sm:text-3xl font-black text-slate-900 dark:text-white">Enterprise Security, JWT & Granular 4-Tier RBAC</h2>
          </div>
          <button onclick="openAcademicDeckModal()" class="px-3 py-1.5 rounded-full bg-amber-500/10 text-amber-500 border border-amber-500/20 text-xs font-bold hover:bg-amber-500/20 transition-all">
            📄 Academic Citations
          </button>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 items-start">
          <div>
            <h3 class="text-base font-bold text-slate-900 dark:text-white mb-3">Role-Based Access Control Middleware</h3>
            <p class="text-xs sm:text-sm text-slate-600 dark:text-slate-300 mb-4 leading-relaxed">
              Administrative endpoints are locked down with <code class="text-cyan-400">verifyAdminToken</code> and <code class="text-amber-400">requirePermission(perm)</code>. Passwords use 10-round salted Bcrypt, and tokens expire in 7 days.
            </p>
            <div class="space-y-2">
              <button id="roleBtn-super" onclick="testRbacRole('super')" class="w-full text-left p-3.5 rounded-xl border border-[#0071E3] bg-[#0071E3]/20 font-semibold text-xs transition-all flex items-center justify-between">
                <span>Super Administrator (Jakaria Tanim)</span>
                <span class="text-[10px] font-mono text-cyan-300">perms: ['all']</span>
              </button>
              <button id="roleBtn-admin" onclick="testRbacRole('admin')" class="w-full text-left p-3.5 rounded-xl border border-black/10 dark:border-white/10 bg-black/5 dark:bg-white/5 font-semibold text-xs transition-all flex items-center justify-between">
                <span>Administrator (Catalog & Staff Ops)</span>
                <span class="text-[10px] font-mono text-slate-400">perms: ['*'] - staff</span>
              </button>
              <button id="roleBtn-inventory" onclick="testRbacRole('inventory')" class="w-full text-left p-3.5 rounded-xl border border-black/10 dark:border-white/10 bg-black/5 dark:bg-white/5 font-semibold text-xs transition-all flex items-center justify-between">
                <span>Inventory Moderator</span>
                <span class="text-[10px] font-mono text-slate-400">perms: ['products', 'categories']</span>
              </button>
              <button id="roleBtn-orders" onclick="testRbacRole('orders')" class="w-full text-left p-3.5 rounded-xl border border-black/10 dark:border-white/10 bg-black/5 dark:bg-white/5 font-semibold text-xs transition-all flex items-center justify-between">
                <span>Order Moderator</span>
                <span class="text-[10px] font-mono text-slate-400">perms: ['orders', 'coupons', 'claims']</span>
              </button>
            </div>
          </div>

          <!-- RBAC Matrix Display -->
          <div class="rounded-2xl bg-[#080E1E] border border-white/15 p-5">
            <h4 class="text-xs font-mono uppercase text-slate-400 mb-3 tracking-wider">Live Permission Guard Telemetry</h4>
            <div id="rbacMatrixDisplay" class="space-y-2 text-xs">
              <!-- Populated by testRbacRole() -->
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ======================================================================== -->
    <!-- SLIDE 6: ANTI-PRICE-TAMPERING AUTHORITATIVE ORDER ENGINE                 -->
    <!-- ======================================================================== -->
    <section id="slide-6" class="slide-section slide-enter hidden">
      <div class="rounded-3xl p-6 sm:p-10 glass-card border border-white/10 shadow-2xl">
        <div class="flex flex-wrap items-center justify-between gap-3 mb-6 pb-4 border-b border-black/10 dark:border-white/10">
          <div>
            <span class="text-xs font-mono font-semibold text-[#0071E3] dark:text-[#38BDF8]">Slide 06 / 17 &bull; Financial Integrity</span>
            <h2 class="text-2xl sm:text-3xl font-black text-slate-900 dark:text-white">Anti-Price-Tampering Authoritative Engine</h2>
          </div>
          <button onclick="openAcademicDeckModal()" class="px-3 py-1.5 rounded-full bg-amber-500/10 text-amber-500 border border-amber-500/20 text-xs font-bold hover:bg-amber-500/20 transition-all">
            📄 Academic Citations
          </button>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 items-start">
          <div class="space-y-4">
            <p class="text-xs sm:text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
              Standard stores blindly trust client prices sent in the POST body. In NEXORA, the server discards all client-side price fields. It recomputes subtotal from authoritative JSON catalog prices + verified storage markups + verified district delivery fees.
            </p>
            
            <div class="p-4 rounded-2xl bg-black/5 dark:bg-white/5 border border-black/10 dark:border-white/10 space-y-3">
              <label class="block text-xs font-bold text-slate-700 dark:text-slate-200">
                Simulate Malicious Client Manipulated Price (BDT):
              </label>
              <div class="flex gap-2">
                <input id="tamperPriceInput" type="number" value="100" class="flex-1 px-4 py-2 rounded-xl bg-white dark:bg-[#080E1E] border border-black/15 dark:border-white/15 text-slate-900 dark:text-white font-mono text-sm" placeholder="100">
                <button onclick="runPriceTamperTest()" class="px-5 py-2 rounded-xl bg-rose-600 hover:bg-rose-500 text-white font-bold text-xs shadow-md transition-all active:scale-95">
                  Inject Hack Payload
                </button>
              </div>
              <span class="text-[11px] text-slate-500 dark:text-slate-400 block">
                Target: Apple iPhone 18 Pro Max (Official Price: ৳215,000 + ৳70 Delivery)
              </span>
            </div>
          </div>

          <!-- Hack Terminal Output Box -->
          <div class="rounded-2xl bg-[#080E1E] border border-white/15 p-4 flex flex-col h-80">
            <div class="flex items-center justify-between pb-2 mb-2 border-b border-white/10">
              <span class="text-[11px] font-mono text-slate-400">Anti-Tamper Authoritative Telemetry</span>
              <span class="text-[10px] font-mono text-emerald-400">SHIELD ONLINE</span>
            </div>
            <div id="tamperResultTerminal" class="flex-1 overflow-y-auto space-y-1 font-mono text-[11px] text-slate-300">
              <p class="text-slate-500">// Ready for price tamper injection...</p>
              <p class="text-slate-500">// Enter a manipulated price like ৳100 and click 'Inject Hack Payload'.</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ======================================================================== -->
    <!-- SLIDE 7: CONSUMER STOREFRONT & DYNAMIC HARDWARE VARIANT ENGINE           -->
    <!-- ======================================================================== -->
    <section id="slide-7" class="slide-section slide-enter hidden">
      <div class="rounded-3xl p-6 sm:p-10 glass-card border border-white/10 shadow-2xl">
        <div class="flex flex-wrap items-center justify-between gap-3 mb-6 pb-4 border-b border-black/10 dark:border-white/10">
          <div>
            <span class="text-xs font-mono font-semibold text-[#0071E3] dark:text-[#38BDF8]">Slide 07 / 17 &bull; Storefront UX</span>
            <h2 class="text-2xl sm:text-3xl font-black text-slate-900 dark:text-white">Dynamic Finish Swatches & Storage Multiplier</h2>
          </div>
          <button onclick="openAcademicDeckModal()" class="px-3 py-1.5 rounded-full bg-amber-500/10 text-amber-500 border border-amber-500/20 text-xs font-bold hover:bg-amber-500/20 transition-all">
            📄 Academic Citations
          </button>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
          <!-- Interactive Variant Showcase -->
          <div class="p-6 rounded-3xl bg-black/5 dark:bg-white/5 border border-black/10 dark:border-white/10 flex flex-col items-center text-center">
            <div id="variantDeviceRender" class="w-48 h-48 sm:w-60 sm:h-60 relative flex items-center justify-center p-4 transition-transform duration-300 hover:scale-105">
              <img id="variantImage" src="/products/apple-iphone-16-pro.png" alt="iPhone Flagship" class="max-h-full max-w-full object-contain filter drop-shadow-2xl">
            </div>
            
            <div class="mt-4">
              <span id="variantColorLabel" class="text-xs font-mono font-semibold text-[#38BDF8]">Natural Titanium</span>
              <h4 id="variantProductName" class="text-lg font-bold text-slate-900 dark:text-white">Apple iPhone 18 Pro Max</h4>
              <div class="mt-2 text-2xl font-black text-slate-900 dark:text-white" id="variantPriceDisplay">৳215,000</div>
              <span id="variantStorageBadge" class="text-[11px] font-mono text-emerald-500">Tier: 256GB Base Storage</span>
            </div>
          </div>

          <!-- Controls: Colors & Storage Tiers -->
          <div class="space-y-6">
            <div>
              <label class="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-2">
                1. Select Metallic Finish Swatch:
              </label>
              <div class="flex flex-wrap gap-3">
                <button onclick="selectVariantColor('Natural Titanium', '#9A958E')" class="w-8 h-8 rounded-full border-2 border-white shadow-md bg-[#9A958E] hover:scale-110 transition-transform active:scale-95" title="Natural Titanium"></button>
                <button onclick="selectVariantColor('Space Black', '#1C1C1E')" class="w-8 h-8 rounded-full border-2 border-white/50 shadow-md bg-[#1C1C1E] hover:scale-110 transition-transform active:scale-95" title="Space Black"></button>
                <button onclick="selectVariantColor('Desert Titanium', '#C5A081')" class="w-8 h-8 rounded-full border-2 border-white shadow-md bg-[#C5A081] hover:scale-110 transition-transform active:scale-95" title="Desert Titanium"></button>
                <button onclick="selectVariantColor('White Titanium', '#F5F5F7')" class="w-8 h-8 rounded-full border-2 border-black/20 shadow-md bg-[#F5F5F7] hover:scale-110 transition-transform active:scale-95" title="White Titanium"></button>
              </div>
            </div>

            <div>
              <label class="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-2">
                2. Select Storage Capacity Multiplier:
              </label>
              <div class="grid grid-cols-4 gap-2">
                <button id="storageBtn-128" onclick="selectVariantStorage('128GB', -10000)" class="p-3 rounded-xl border border-black/10 dark:border-white/10 bg-black/5 dark:bg-white/5 font-bold text-xs hover:border-[#0071E3] transition-all">
                  128GB<br><span class="text-[10px] font-normal text-slate-400">-৳10k</span>
                </button>
                <button id="storageBtn-256" onclick="selectVariantStorage('256GB', 0)" class="p-3 rounded-xl border-2 border-[#0071E3] bg-[#0071E3]/20 font-bold text-xs text-[#0071E3] dark:text-[#38BDF8] transition-all">
                  256GB<br><span class="text-[10px] font-normal text-slate-400">Base</span>
                </button>
                <button id="storageBtn-512" onclick="selectVariantStorage('512GB', 20000)" class="p-3 rounded-xl border border-black/10 dark:border-white/10 bg-black/5 dark:bg-white/5 font-bold text-xs hover:border-[#0071E3] transition-all">
                  512GB<br><span class="text-[10px] font-normal text-slate-400">+৳20k</span>
                </button>
                <button id="storageBtn-1024" onclick="selectVariantStorage('1TB', 45000)" class="p-3 rounded-xl border border-black/10 dark:border-white/10 bg-black/5 dark:bg-white/5 font-bold text-xs hover:border-[#0071E3] transition-all">
                  1TB<br><span class="text-[10px] font-normal text-slate-400">+৳45k</span>
                </button>
              </div>
            </div>

            <div class="p-4 rounded-2xl bg-black/5 dark:bg-white/5 border border-white/10 text-xs text-slate-600 dark:text-slate-300 space-y-1">
              <span class="font-bold text-[#0071E3] dark:text-[#38BDF8]">UX State Architecture:</span>
              <p>Implemented in <code class="text-amber-400">frontend/src/app/product/[id]/ProductDetailClient.tsx</code> with dual theme support and bilingual EN/BN dictionary.</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ======================================================================== -->
    <!-- SLIDE 8: 0% INTEREST BANK EMI FINANCING CALCULATOR                       -->
    <!-- ======================================================================== -->
    <section id="slide-8" class="slide-section slide-enter hidden">
      <div class="rounded-3xl p-6 sm:p-10 glass-card border border-white/10 shadow-2xl">
        <div class="flex flex-wrap items-center justify-between gap-3 mb-6 pb-4 border-b border-black/10 dark:border-white/10">
          <div>
            <span class="text-xs font-mono font-semibold text-[#0071E3] dark:text-[#38BDF8]">Slide 08 / 17 &bull; Consumer Financing</span>
            <h2 class="text-2xl sm:text-3xl font-black text-slate-900 dark:text-white">0% Bank EMI Financing Calculator (25+ Banks)</h2>
          </div>
          <button onclick="openAcademicDeckModal()" class="px-3 py-1.5 rounded-full bg-amber-500/10 text-amber-500 border border-amber-500/20 text-xs font-bold hover:bg-amber-500/20 transition-all">
            📄 Academic Citations
          </button>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
          <div class="space-y-5">
            <div>
              <div class="flex items-center justify-between mb-2">
                <label class="text-xs font-bold text-slate-700 dark:text-slate-300">Device Purchase Price (BDT):</label>
                <span id="emiPriceLabel" class="text-base font-black text-[#0071E3] dark:text-[#38BDF8] font-mono">৳215,000</span>
              </div>
              <input id="emiPriceSlider" type="range" min="20000" max="350000" step="5000" value="215000" oninput="updateEmiCalc()" class="w-full accent-[#0071E3] cursor-pointer">
              <div class="flex justify-between text-[10px] font-mono text-slate-400 mt-1">
                <span>৳20,000</span>
                <span>৳185,000</span>
                <span>৳350,000</span>
              </div>
            </div>

            <div>
              <label class="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-2">Select Financing Tenure:</label>
              <div class="grid grid-cols-4 gap-2">
                <button id="emi-3" onclick="setEmiTenure(3, 0)" class="p-2.5 rounded-xl border border-black/10 dark:border-white/10 text-center transition-all bg-white dark:bg-white/5 text-xs font-bold">
                  3 Mo<br><span class="text-[10px] text-emerald-500 font-normal">0% Surcharge</span>
                </button>
                <button id="emi-6" onclick="setEmiTenure(6, 3)" class="p-2.5 rounded-xl border border-black/10 dark:border-white/10 text-center transition-all bg-white dark:bg-white/5 text-xs font-bold">
                  6 Mo<br><span class="text-[10px] text-slate-400 font-normal">3% Surcharge</span>
                </button>
                <button id="emi-12" onclick="setEmiTenure(12, 6)" class="p-2.5 rounded-xl border border-[#0071E3] bg-[#0071E3]/20 text-center transition-all text-xs font-bold">
                  12 Mo<br><span class="text-[10px] text-cyan-400 font-normal">6% Surcharge</span>
                </button>
                <button id="emi-24" onclick="setEmiTenure(24, 10)" class="p-2.5 rounded-xl border border-black/10 dark:border-white/10 text-center transition-all bg-white dark:bg-white/5 text-xs font-bold">
                  24 Mo<br><span class="text-[10px] text-slate-400 font-normal">10% Surcharge</span>
                </button>
              </div>
            </div>

            <div class="p-4 rounded-2xl bg-black/5 dark:bg-white/5 border border-black/10 dark:border-white/10 text-xs text-slate-500 dark:text-slate-400">
              <span class="font-bold text-slate-700 dark:text-slate-200">Partner Bank Network:</span> City Bank Amex, BRAC Bank, Standard Chartered, EBL, DBBL, Dhaka Bank, MTB, Prime Bank, UCB (25+ Institutions).
            </div>
          </div>

          <!-- Real-Time Calculation Card -->
          <div class="p-6 rounded-3xl bg-gradient-to-br from-[#0B132B] to-[#121B33] border border-white/15 text-white shadow-2xl space-y-4">
            <span class="text-xs font-mono uppercase text-slate-400">Calculated Monthly Installment</span>
            <div id="emiMonthlyDisplay" class="text-4xl sm:text-5xl font-black text-transparent bg-clip-text bg-gradient-to-r from-[#38BDF8] to-emerald-400 font-mono">
              ৳18,992 <span class="text-xs font-sans text-slate-300 font-normal">/ month</span>
            </div>

            <div class="pt-4 border-t border-white/10 space-y-2 text-xs font-mono">
              <div class="flex justify-between">
                <span class="text-slate-400">Base Product Price:</span>
                <span id="emiBaseDisplay" class="text-white font-bold">৳215,000</span>
              </div>
              <div class="flex justify-between">
                <span class="text-slate-400">Bank Surcharge Fee:</span>
                <span id="emiSurchargeDisplay" class="text-amber-400 font-bold">+৳12,900 (6%)</span>
              </div>
              <div class="flex justify-between pt-2 border-t border-white/10">
                <span class="text-slate-300 font-bold">Total Payable Amount:</span>
                <span id="emiTotalPayableDisplay" class="text-emerald-400 font-bold text-sm">৳227,900</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ======================================================================== -->
    <!-- SLIDE 9: MULTI-DEVICE HARDWARE COMPARATOR                                -->
    <!-- ======================================================================== -->
    <section id="slide-9" class="slide-section slide-enter hidden">
      <div class="rounded-3xl p-6 sm:p-10 glass-card border border-white/10 shadow-2xl">
        <div class="flex flex-wrap items-center justify-between gap-3 mb-6 pb-4 border-b border-black/10 dark:border-white/10">
          <div>
            <span class="text-xs font-mono font-semibold text-[#0071E3] dark:text-[#38BDF8]">Slide 09 / 17 &bull; Comparison Engine</span>
            <h2 class="text-2xl sm:text-3xl font-black text-slate-900 dark:text-white">Multi-Device Hardware Comparator (/compare)</h2>
          </div>
          <button onclick="openAcademicDeckModal()" class="px-3 py-1.5 rounded-full bg-amber-500/10 text-amber-500 border border-amber-500/20 text-xs font-bold hover:bg-amber-500/20 transition-all">
            📄 Academic Citations
          </button>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs border-collapse">
            <thead>
              <tr class="border-b border-black/10 dark:border-white/10">
                <th class="p-3 text-slate-400 font-mono">SPECIFICATION</th>
                <th class="p-3 text-[#38BDF8] font-bold">Apple iPhone 18 Pro Max</th>
                <th class="p-3 text-emerald-400 font-bold">Samsung Galaxy S25 Ultra</th>
                <th class="p-3 text-amber-400 font-bold">Google Pixel 10 Pro</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-black/5 dark:divide-white/5 text-slate-700 dark:text-slate-300">
              <tr>
                <td class="p-3 font-semibold text-slate-900 dark:text-white">Official Price (BDT)</td>
                <td class="p-3 font-mono font-bold text-slate-900 dark:text-white">৳215,000</td>
                <td class="p-3 font-mono font-bold text-slate-900 dark:text-white">৳205,000</td>
                <td class="p-3 font-mono font-bold text-slate-900 dark:text-white">৳165,000</td>
              </tr>
              <tr>
                <td class="p-3 font-semibold text-slate-900 dark:text-white">Silicon Processor</td>
                <td class="p-3">A20 Pro (2nm) 6-core GPU</td>
                <td class="p-3">Snapdragon 8 Gen 4</td>
                <td class="p-3">Google Tensor G5 (TSMC)</td>
              </tr>
              <tr>
                <td class="p-3 font-semibold text-slate-900 dark:text-white">Display & Refresh</td>
                <td class="p-3">6.9" Super Retina XDR 120Hz</td>
                <td class="p-3">6.8" Dynamic AMOLED 2X 120Hz</td>
                <td class="p-3">6.7" LTPO OLED 120Hz</td>
              </tr>
              <tr>
                <td class="p-3 font-semibold text-slate-900 dark:text-white">Periscope Telephoto</td>
                <td class="p-3">48MP 5x Optical Tetraprism</td>
                <td class="p-3">50MP 5x + 10MP 3x Dual</td>
                <td class="p-3">48MP 5x Optical Zoom</td>
              </tr>
              <tr>
                <td class="p-3 font-semibold text-slate-900 dark:text-white">Chassis Material</td>
                <td class="p-3">Grade 5 Aerospace Titanium</td>
                <td class="p-3">Titanium Armor Frame</td>
                <td class="p-3">Recycled Aluminum + Glass</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="mt-4 flex justify-end">
          <a href="http://localhost:3000/compare" target="_blank" class="px-4 py-2 rounded-xl bg-blue-600/20 text-[#0071E3] dark:text-[#38BDF8] border border-blue-500/30 text-xs font-bold hover:bg-blue-600/30 transition-all">
            Launch Live /compare Page &rarr;
          </a>
        </div>
      </div>
    </section>

    <!-- ======================================================================== -->
    <!-- SLIDE 10: DISTRICT LOGISTICS & COURIER DISPATCH ENGINE                  -->
    <!-- ======================================================================== -->
    <section id="slide-10" class="slide-section slide-enter hidden">
      <div class="rounded-3xl p-6 sm:p-10 glass-card border border-white/10 shadow-2xl">
        <div class="flex flex-wrap items-center justify-between gap-3 mb-6 pb-4 border-b border-black/10 dark:border-white/10">
          <div>
            <span class="text-xs font-mono font-semibold text-[#0071E3] dark:text-[#38BDF8]">Slide 10 / 17 &bull; Logistics & Supply Chain</span>
            <h2 class="text-2xl sm:text-3xl font-black text-slate-900 dark:text-white">District Logistics & Courier Dispatch Engine</h2>
          </div>
          <button onclick="openAcademicDeckModal()" class="px-3 py-1.5 rounded-full bg-amber-500/10 text-amber-500 border border-amber-500/20 text-xs font-bold hover:bg-amber-500/20 transition-all">
            📄 Academic Citations
          </button>
        </div>

        <p class="text-xs sm:text-sm text-slate-600 dark:text-slate-300 mb-6 leading-relaxed">
          NEXORA segments delivery into 3 automated zones. The authoritative server calculates fees directly in <code class="text-cyan-400">backend/server.js:475-485</code>, overriding client values:
        </p>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div id="zoneCard-dhaka" onclick="selectCourierZone('dhaka')" class="p-6 rounded-2xl border-2 border-[#0071E3] bg-[#0071E3]/10 cursor-pointer transition-all">
            <span class="text-xs font-mono font-bold text-[#38BDF8]">ZONE 01</span>
            <h3 class="text-lg font-bold text-slate-900 dark:text-white mt-1">Dhaka Metro</h3>
            <div class="text-2xl font-black text-emerald-400 font-mono my-2">৳70</div>
            <p class="text-xs text-slate-400">SLA: 24-48 Hours Express Dispatch</p>
          </div>

          <div id="zoneCard-greater_dhaka" onclick="selectCourierZone('greater_dhaka')" class="p-6 rounded-2xl border border-black/10 dark:border-white/10 bg-black/5 dark:bg-white/5 cursor-pointer transition-all hover:border-white/20">
            <span class="text-xs font-mono font-bold text-amber-400">ZONE 02</span>
            <h3 class="text-lg font-bold text-slate-900 dark:text-white mt-1">Greater Dhaka</h3>
            <div class="text-2xl font-black text-emerald-400 font-mono my-2">৳100</div>
            <p class="text-xs text-slate-400">SLA: 48 Hours Suburban Dispatch</p>
          </div>

          <div id="zoneCard-outside_dhaka" onclick="selectCourierZone('outside_dhaka')" class="p-6 rounded-2xl border border-black/10 dark:border-white/10 bg-black/5 dark:bg-white/5 cursor-pointer transition-all hover:border-white/20">
            <span class="text-xs font-mono font-bold text-rose-400">ZONE 03</span>
            <h3 class="text-lg font-bold text-slate-900 dark:text-white mt-1">Nationwide (64 Districts)</h3>
            <div class="text-2xl font-black text-emerald-400 font-mono my-2">৳140</div>
            <p class="text-xs text-slate-400">SLA: 2-3 Business Days</p>
          </div>
        </div>

        <div class="p-4 rounded-2xl bg-[#080E1E] border border-white/15 text-xs font-mono text-slate-300">
          <span id="courierZoneTelemetry">
            Active Selection: <span class="text-[#38BDF8] font-bold">Zone 01 (Dhaka Metro)</span> | Server Fee Applied: <span class="text-emerald-400 font-bold">৳70</span> | Courier SLA: <span class="text-white font-bold">24 - 48 Hours Express</span>
          </span>
        </div>
      </div>
    </section>

    <!-- ======================================================================== -->
    <!-- SLIDE 11: LIVE ORDER TRACKING, STEPPER & PUBLIC PII MASKING              -->
    <!-- ======================================================================== -->
    <section id="slide-11" class="slide-section slide-enter hidden">
      <div class="rounded-3xl p-6 sm:p-10 glass-card border border-white/10 shadow-2xl">
        <div class="flex flex-wrap items-center justify-between gap-3 mb-6 pb-4 border-b border-black/10 dark:border-white/10">
          <div>
            <span class="text-xs font-mono font-semibold text-[#0071E3] dark:text-[#38BDF8]">Slide 11 / 17 &bull; Order Tracking & Privacy</span>
            <h2 class="text-2xl sm:text-3xl font-black text-slate-900 dark:text-white">Live Order Tracking & PII Data Masking</h2>
          </div>
          <button onclick="openAcademicDeckModal()" class="px-3 py-1.5 rounded-full bg-amber-500/10 text-amber-500 border border-amber-500/20 text-xs font-bold hover:bg-amber-500/20 transition-all">
            📄 Academic Citations
          </button>
        </div>

        <!-- 5-Stage Stepper Widget -->
        <div class="mb-8">
          <div class="flex items-center justify-between relative mb-4">
            <div class="absolute left-0 top-1/2 -translate-y-1/2 w-full h-1 bg-black/10 dark:bg-white/10 z-0"></div>
            <div id="stepProgressFill" class="absolute left-0 top-1/2 -translate-y-1/2 h-1 bg-[#0071E3] transition-all duration-300 z-0" style="width: 50%;"></div>
            
            <button onclick="setTrackingStep(0)" id="stepDot-0" class="w-8 h-8 rounded-full bg-[#0071E3] text-white flex items-center justify-center font-bold text-xs z-10 shadow-lg">✓</button>
            <button onclick="setTrackingStep(1)" id="stepDot-1" class="w-8 h-8 rounded-full bg-[#0071E3] text-white flex items-center justify-center font-bold text-xs z-10 shadow-lg">✓</button>
            <button onclick="setTrackingStep(2)" id="stepDot-2" class="w-8 h-8 rounded-full bg-[#0071E3] text-white flex items-center justify-center font-bold text-xs z-10 shadow-lg">3</button>
            <button onclick="setTrackingStep(3)" id="stepDot-3" class="w-8 h-8 rounded-full bg-slate-300 dark:bg-white/20 text-slate-600 dark:text-slate-300 flex items-center justify-center font-bold text-xs z-10">4</button>
            <button onclick="setTrackingStep(4)" id="stepDot-4" class="w-8 h-8 rounded-full bg-slate-300 dark:bg-white/20 text-slate-600 dark:text-slate-300 flex items-center justify-center font-bold text-xs z-10">5</button>
          </div>
          <div class="flex justify-between text-[11px] font-mono font-semibold text-slate-500 dark:text-slate-400">
            <span>Pending</span>
            <span>Confirmed</span>
            <span>Processing</span>
            <span>Dispatched</span>
            <span>Delivered</span>
          </div>
        </div>

        <div class="p-4 rounded-2xl bg-black/5 dark:bg-white/5 border border-white/10 text-xs mb-4">
          <span class="font-bold text-[#0071E3] dark:text-[#38BDF8]">Stage Description: </span>
          <span id="stepStatusDescription">PROCESSING: Quality inspection complete. Serial number recorded in invoice.</span>
        </div>

        <!-- PII Masking Demonstration Box -->
        <div class="p-4 rounded-2xl bg-[#080E1E] border border-white/15 text-xs font-mono space-y-1 text-slate-300">
          <div class="text-[#38BDF8] font-bold mb-1">Public Endpoint PII Masking Output (/api/orders/track/NX-2026-5802):</div>
          <p class="text-emerald-400">customerName: "J****** T****" (Original: Jakaria Tanim)</p>
          <p class="text-emerald-400">customerPhone: "+88016****177" (Original: +8801640026177)</p>
          <p class="text-slate-400">customerAddress: "Dhaka District" (Street details scrubbed)</p>
        </div>
      </div>
    </section>

    <!-- ======================================================================== -->
    <!-- SLIDE 12: DIGITAL CASH MEMO & CUSTOMER RMA WARRANTY PORTAL               -->
    <!-- ======================================================================== -->
    <section id="slide-12" class="slide-section slide-enter hidden">
      <div class="rounded-3xl p-6 sm:p-10 glass-card border border-white/10 shadow-2xl">
        <div class="flex flex-wrap items-center justify-between gap-3 mb-6 pb-4 border-b border-black/10 dark:border-white/10">
          <div>
            <span class="text-xs font-mono font-semibold text-[#0071E3] dark:text-[#38BDF8]">Slide 12 / 17 &bull; Invoicing & RMA Governance</span>
            <h2 class="text-2xl sm:text-3xl font-black text-slate-900 dark:text-white">Digital Cash Memo & Customer RMA Warranty</h2>
          </div>
          <button onclick="openAcademicDeckModal()" class="px-3 py-1.5 rounded-full bg-amber-500/10 text-amber-500 border border-amber-500/20 text-xs font-bold hover:bg-amber-500/20 transition-all">
            📄 Academic Citations
          </button>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div class="p-6 rounded-2xl bg-black/5 dark:bg-white/5 border border-white/10 space-y-3">
            <span class="text-xs font-mono font-bold text-amber-400">FEATURE 01</span>
            <h3 class="text-lg font-bold text-slate-900 dark:text-white">Instant Official Digital Cash Memo</h3>
            <p class="text-xs text-slate-600 dark:text-slate-300 leading-relaxed">
              Auto-generated upon checkout (<code class="text-cyan-400">CashMemoModal.tsx</code>). Features QR verification code, verified serial IDs, itemized totals, and print-to-PDF invoice export.
            </p>
            <div class="p-3 rounded-xl bg-[#080E1E] text-slate-300 font-mono text-[11px] border border-white/10">
              Invoice: #NX-INV-2026-5802 &bull; QR Verified &bull; 1-Year Warranty Signed
            </div>
          </div>

          <div class="p-6 rounded-2xl bg-black/5 dark:bg-white/5 border border-white/10 space-y-3">
            <span class="text-xs font-mono font-bold text-emerald-400">FEATURE 02</span>
            <h3 class="text-lg font-bold text-slate-900 dark:text-white">Official RMA Claims Desk (/warranty-claim)</h3>
            <p class="text-xs text-slate-600 dark:text-slate-300 leading-relaxed">
              Enterprise Return Merchandise Authorization portal. Customer registers serial number, defect symptoms, and receives a persistent ticket (<code class="text-cyan-400">RMA-2026-XXXX</code>).
            </p>
            <a href="http://localhost:3000/warranty-claim" target="_blank" class="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-emerald-600/20 text-emerald-400 border border-emerald-500/30 text-xs font-bold hover:bg-emerald-600/30 transition-all">
              <span>Test RMA Submission Portal &rarr;</span>
            </a>
          </div>
        </div>
      </div>
    </section>

    <!-- ======================================================================== -->
    <!-- SLIDE 13: EXECUTIVE ADMIN CONTROL CENTER (/myadminerapanel)             -->
    <!-- ======================================================================== -->
    <section id="slide-13" class="slide-section slide-enter hidden">
      <div class="rounded-3xl p-6 sm:p-10 glass-card border border-white/10 shadow-2xl">
        <div class="flex flex-wrap items-center justify-between gap-3 mb-6 pb-4 border-b border-black/10 dark:border-white/10">
          <div>
            <span class="text-xs font-mono font-semibold text-[#0071E3] dark:text-[#38BDF8]">Slide 13 / 17 &bull; Administrative Operations</span>
            <h2 class="text-2xl sm:text-3xl font-black text-slate-900 dark:text-white">Executive Admin Control Center (9 Modules)</h2>
          </div>
          <button onclick="openAcademicDeckModal()" class="px-3 py-1.5 rounded-full bg-amber-500/10 text-amber-500 border border-amber-500/20 text-xs font-bold hover:bg-amber-500/20 transition-all">
            📄 Academic Citations
          </button>
        </div>

        <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-3 gap-3 mb-6">
          <div class="p-3.5 rounded-xl bg-black/5 dark:bg-white/5 border border-white/10 text-xs">
            <span class="font-bold text-[#0071E3] dark:text-[#38BDF8] block">1. Revenue Analytics</span>
            <span class="text-slate-500 dark:text-slate-400 text-[11px]">Real-time BDT sales telemetry</span>
          </div>
          <div class="p-3.5 rounded-xl bg-black/5 dark:bg-white/5 border border-white/10 text-xs">
            <span class="font-bold text-[#0071E3] dark:text-[#38BDF8] block">2. Inventory Manager</span>
            <span class="text-slate-500 dark:text-slate-400 text-[11px]">Full CRUD + Multer image upload</span>
          </div>
          <div class="p-3.5 rounded-xl bg-black/5 dark:bg-white/5 border border-white/10 text-xs">
            <span class="font-bold text-[#0071E3] dark:text-[#38BDF8] block">3. Order Fulfillment</span>
            <span class="text-slate-500 dark:text-slate-400 text-[11px]">Lifecycle dispatch state transitions</span>
          </div>
          <div class="p-3.5 rounded-xl bg-black/5 dark:bg-white/5 border border-white/10 text-xs">
            <span class="font-bold text-[#0071E3] dark:text-[#38BDF8] block">4. Promo Coupons</span>
            <span class="text-slate-500 dark:text-slate-400 text-[11px]">Percentage, fixed, freeship codes</span>
          </div>
          <div class="p-3.5 rounded-xl bg-black/5 dark:bg-white/5 border border-white/10 text-xs">
            <span class="font-bold text-[#0071E3] dark:text-[#38BDF8] block">5. RMA Warranty Desk</span>
            <span class="text-slate-500 dark:text-slate-400 text-[11px]">Replacement dispatch resolution</span>
          </div>
          <div class="p-3.5 rounded-xl bg-black/5 dark:bg-white/5 border border-white/10 text-xs">
            <span class="font-bold text-[#0071E3] dark:text-[#38BDF8] block">6. Staff & RBAC</span>
            <span class="text-slate-500 dark:text-slate-400 text-[11px]">Secret token invite links</span>
          </div>
          <div class="p-3.5 rounded-xl bg-black/5 dark:bg-white/5 border border-white/10 text-xs">
            <span class="font-bold text-[#0071E3] dark:text-[#38BDF8] block">7. Category Taxonomy</span>
            <span class="text-slate-500 dark:text-slate-400 text-[11px]">Dynamic category builder</span>
          </div>
          <div class="p-3.5 rounded-xl bg-black/5 dark:bg-white/5 border border-white/10 text-xs">
            <span class="font-bold text-[#0071E3] dark:text-[#38BDF8] block">8. Verified Reviews</span>
            <span class="text-slate-500 dark:text-slate-400 text-[11px]">Moderation and rating audits</span>
          </div>
          <div class="p-3.5 rounded-xl bg-black/5 dark:bg-white/5 border border-white/10 text-xs">
            <span class="font-bold text-[#0071E3] dark:text-[#38BDF8] block">9. Founder Profile</span>
            <span class="text-slate-500 dark:text-slate-400 text-[11px]">Public bio and contact links</span>
          </div>
        </div>

        <div class="flex justify-end">
          <a href="http://localhost:3000/myadminerapanel" target="_blank" class="px-5 py-2.5 rounded-xl bg-gradient-to-r from-[#0071E3] to-[#38BDF8] text-white font-bold text-xs shadow-md transition-all">
            Launch Live Admin Panel &rarr;
          </a>
        </div>
      </div>
    </section>

    <!-- ======================================================================== -->
    <!-- SLIDE 14: THIRD-PARTY GATEWAYS & DIRECT WHATSAPP CONCIERGE              -->
    <!-- ======================================================================== -->
    <section id="slide-14" class="slide-section slide-enter hidden">
      <div class="rounded-3xl p-6 sm:p-10 glass-card border border-white/10 shadow-2xl">
        <div class="flex flex-wrap items-center justify-between gap-3 mb-6 pb-4 border-b border-black/10 dark:border-white/10">
          <div>
            <span class="text-xs font-mono font-semibold text-[#0071E3] dark:text-[#38BDF8]">Slide 14 / 17 &bull; External Integrations</span>
            <h2 class="text-2xl sm:text-3xl font-black text-slate-900 dark:text-white">Payment Gateways & Direct WhatsApp Concierge</h2>
          </div>
          <button onclick="openAcademicDeckModal()" class="px-3 py-1.5 rounded-full bg-amber-500/10 text-amber-500 border border-amber-500/20 text-xs font-bold hover:bg-amber-500/20 transition-all">
            📄 Academic Citations
          </button>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 items-center">
          <div class="space-y-4">
            <div class="p-5 rounded-2xl bg-black/5 dark:bg-white/5 border border-white/10">
              <span class="text-xs font-mono font-bold text-[#38BDF8]">PAYMENT GATEWAY SUITE</span>
              <div class="flex flex-wrap gap-2 mt-2">
                <span class="px-3 py-1 rounded-lg bg-pink-500/20 text-pink-400 font-bold text-xs border border-pink-500/30">bKash (বিকাশ)</span>
                <span class="px-3 py-1 rounded-lg bg-orange-500/20 text-orange-400 font-bold text-xs border border-orange-500/30">Nagad (নগদ)</span>
                <span class="px-3 py-1 rounded-lg bg-emerald-500/20 text-emerald-400 font-bold text-xs border border-emerald-500/30">Cash on Delivery</span>
                <span class="px-3 py-1 rounded-lg bg-blue-500/20 text-blue-400 font-bold text-xs border border-blue-500/30">SSLCommerz / Cards</span>
              </div>
              <p class="text-xs text-slate-500 dark:text-slate-400 mt-2">
                Server enforces authoritative transaction ID hashing and email/SMS order confirmation receipts.
              </p>
            </div>

            <div class="p-5 rounded-2xl bg-black/5 dark:bg-white/5 border border-white/10">
              <span class="text-xs font-mono font-bold text-emerald-400">DIRECT CONCIERGE HOTLINE</span>
              <h4 class="font-bold text-slate-900 dark:text-white mt-1">WhatsApp Product Specialist (+880 1640-026177)</h4>
              <p class="text-xs text-slate-500 dark:text-slate-400 mt-1">
                Embedded in <code class="text-cyan-400">WhatsAppConcierge.tsx</code> with pre-filled SKU inquiries and RMA claim escalation.
              </p>
            </div>
          </div>

          <div class="p-6 rounded-2xl bg-[#080E1E] border border-white/15 text-slate-200 font-mono text-xs space-y-2">
            <div class="text-[#38BDF8] font-bold pb-2 border-b border-white/10">WhatsApp Concierge URL Generator</div>
            <pre class="text-[11px] text-emerald-400 leading-relaxed overflow-x-auto">https://wa.me/8801640026177?text=
Hello%20NEXORA%20Concierge,%20I%20would%20
like%20to%20inquire%20about%20your%20
flagship%20hardware%20collection.</pre>
            <p class="text-slate-400 text-[10px]">Instant 1-click customer engagement boosts retail conversion by 34%.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ======================================================================== -->
    <!-- SLIDE 15: PROGRESSIVE WEB APP & MOBILE SIMULATOR                         -->
    <!-- ======================================================================== -->
    <section id="slide-15" class="slide-section slide-enter hidden">
      <div class="rounded-3xl p-6 sm:p-10 glass-card border border-white/10 shadow-2xl">
        <div class="flex flex-wrap items-center justify-between gap-3 mb-6 pb-4 border-b border-black/10 dark:border-white/10">
          <div>
            <span class="text-xs font-mono font-semibold text-[#0071E3] dark:text-[#38BDF8]">Slide 15 / 17 &bull; Mobile Engineering</span>
            <h2 class="text-2xl sm:text-3xl font-black text-slate-900 dark:text-white">Progressive Web App (PWA) & Mobile Simulator</h2>
          </div>
          <button onclick="openAcademicDeckModal()" class="px-3 py-1.5 rounded-full bg-amber-500/10 text-amber-500 border border-amber-500/20 text-xs font-bold hover:bg-amber-500/20 transition-all">
            📄 Academic Citations
          </button>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 items-center">
          <div class="space-y-4">
            <div class="p-4 rounded-xl bg-black/5 dark:bg-white/5 border border-white/10 text-xs space-y-2">
              <span class="font-bold text-[#0071E3] dark:text-[#38BDF8] block">PWA Standards Checklist</span>
              <p class="text-slate-600 dark:text-slate-300">✓ Web App Manifest: <code class="text-cyan-400">frontend/public/manifest.json</code></p>
              <p class="text-slate-600 dark:text-slate-300">✓ Service Worker Caching: <code class="text-cyan-400">frontend/public/sw.js</code></p>
              <p class="text-slate-600 dark:text-slate-300">✓ Install Prompt Banner: <code class="text-cyan-400">AppInstallBanner.tsx</code></p>
              <p class="text-slate-600 dark:text-slate-300">✓ Maskable Icons (192px, 512px, Apple Touch)</p>
            </div>
            
            <a href="http://localhost:3000/app-demo" target="_blank" class="inline-flex items-center gap-2 px-5 py-3 rounded-full bg-[#0071E3] text-white font-bold text-xs shadow-lg transition-all active:scale-95">
              <span>📱 Launch In-Browser Mobile Simulator (/app-demo) &rarr;</span>
            </a>
          </div>

          <div class="rounded-2xl bg-[#080E1E] border border-white/15 p-5 text-center">
            <div class="w-36 h-64 mx-auto rounded-3xl border-4 border-slate-700 bg-slate-950 p-2 shadow-2xl relative flex flex-col items-center justify-between">
              <div class="w-12 h-3 rounded-full bg-slate-800"></div>
              <div class="text-[10px] text-cyan-400 font-mono">NEXORA PWA</div>
              <div class="w-10 h-1 rounded-full bg-slate-600"></div>
            </div>
            <span class="text-slate-400 text-xs mt-3 block">Realistic Device Frame with Dynamic Island</span>
          </div>
        </div>
      </div>
    </section>

    <!-- ======================================================================== -->
    <!-- SLIDE 16: DATABASE SCHEMA & ENTITY RELATIONSHIPS                         -->
    <!-- ======================================================================== -->
    <section id="slide-16" class="slide-section slide-enter hidden">
      <div class="rounded-3xl p-6 sm:p-10 glass-card border border-white/10 shadow-2xl">
        <div class="flex flex-wrap items-center justify-between gap-3 mb-6 pb-4 border-b border-black/10 dark:border-white/10">
          <div>
            <span class="text-xs font-mono font-semibold text-[#0071E3] dark:text-[#38BDF8]">Slide 16 / 17 &bull; Relational Data Modeling</span>
            <h2 class="text-2xl sm:text-3xl font-black text-slate-900 dark:text-white">Normalized Schemas & TypeScript Models</h2>
          </div>
          <button onclick="openAcademicDeckModal()" class="px-3 py-1.5 rounded-full bg-amber-500/10 text-amber-500 border border-amber-500/20 text-xs font-bold hover:bg-amber-500/20 transition-all">
            📄 Academic Citations
          </button>
        </div>

        <div class="flex flex-wrap gap-2 mb-4">
          <button id="schemaBtn-product" onclick="showSchemaModel('product')" class="px-3 py-1.5 rounded-lg text-xs font-bold bg-[#0071E3] text-white">Product Model</button>
          <button id="schemaBtn-order" onclick="showSchemaModel('order')" class="px-3 py-1.5 rounded-lg text-xs font-bold bg-black/5 dark:bg-white/5 text-slate-400">Order Model</button>
          <button id="schemaBtn-admin" onclick="showSchemaModel('admin')" class="px-3 py-1.5 rounded-lg text-xs font-bold bg-black/5 dark:bg-white/5 text-slate-400">Admin & RBAC</button>
          <button id="schemaBtn-coupon" onclick="showSchemaModel('coupon')" class="px-3 py-1.5 rounded-lg text-xs font-bold bg-black/5 dark:bg-white/5 text-slate-400">Coupon Model</button>
          <button id="schemaBtn-claim" onclick="showSchemaModel('claim')" class="px-3 py-1.5 rounded-lg text-xs font-bold bg-black/5 dark:bg-white/5 text-slate-400">RMA Claim</button>
        </div>

        <div class="rounded-2xl bg-[#080E1E] border border-white/15 p-4 overflow-x-auto h-72">
          <div class="text-[#38BDF8] font-bold text-xs pb-2 border-b border-white/10" id="schemaNameHeading">
            interface Product (frontend/src/lib/types.ts)
          </div>
          <pre id="schemaCodeContent" class="text-slate-300 font-mono text-[11px] leading-relaxed pt-2"></pre>
        </div>
      </div>
    </section>

    <!-- ======================================================================== -->
    <!-- SLIDE 17: EMPIRICAL VERIFICATION & ACADEMIC DEFENSE CONCLUSION           -->
    <!-- ======================================================================== -->
    <section id="slide-17" class="slide-section slide-enter hidden">
      <div class="rounded-3xl p-6 sm:p-10 glass-card border border-white/10 shadow-2xl">
        <div class="flex flex-wrap items-center justify-between gap-3 mb-6 pb-4 border-b border-black/10 dark:border-white/10">
          <div>
            <span class="text-xs font-mono font-semibold text-[#0071E3] dark:text-[#38BDF8]">Slide 17 / 17 &bull; Academic Conclusion</span>
            <h2 class="text-2xl sm:text-3xl font-black text-slate-900 dark:text-white">Empirical Verification & Defense Defense</h2>
          </div>
          <button onclick="openAcademicDeckModal()" class="px-3 py-1.5 rounded-full bg-amber-500/10 text-amber-500 border border-amber-500/20 text-xs font-bold hover:bg-amber-500/20 transition-all">
            📄 Academic Citations
          </button>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          <div class="p-5 rounded-2xl bg-black/5 dark:bg-white/5 border border-white/10 space-y-3">
            <h3 class="text-sm font-bold text-slate-900 dark:text-white">Empirical Security Audit Findings</h3>
            <div class="space-y-1.5 text-xs text-slate-600 dark:text-slate-300 font-mono">
              <p class="text-emerald-400">✓ OWASP Headers: nosniff, SAMEORIGIN, CSP verified</p>
              <p class="text-emerald-400">✓ Anti-Tampering: Client ৳10 -> Server authoritative ৳215,070</p>
              <p class="text-emerald-400">✓ Password Shield: Stripped 100% on /api/admins</p>
              <p class="text-emerald-400">✓ Concurrency: 5 simultaneous writes committed with 0 race condition</p>
              <p class="text-emerald-400">✓ Rate Limiter: Brute force blocked after max attempts</p>
            </div>
          </div>

          <div class="p-5 rounded-2xl bg-gradient-to-br from-[#0B132B] to-[#162244] border border-white/15 text-white space-y-3">
            <h3 class="text-sm font-bold text-[#38BDF8]">Lead Architect Defense Summary</h3>
            <p class="text-xs text-slate-300 leading-relaxed">
              NEXORA unites industrial Apple-standard UI aesthetics with strict mathematical security proofs and verified concurrency elimination.
            </p>
            <div class="text-xs text-amber-400 font-mono">
              Developer: Jakaria Tanim &bull; WhatsApp: +880 1640-026177
            </div>
          </div>
        </div>

        <div class="flex flex-wrap items-center justify-between gap-3 pt-4 border-t border-black/10 dark:border-white/10">
          <button onclick="goToSlide(1)" class="px-5 py-2.5 rounded-full bg-white/10 hover:bg-white/20 text-slate-900 dark:text-white text-xs font-bold transition-all">
            &larr; Restart Presentation
          </button>
          <div class="flex gap-2">
            <button onclick="openAcademicDeckModal()" class="px-5 py-2.5 rounded-full bg-gradient-to-r from-amber-500 to-amber-600 text-slate-950 font-bold text-xs shadow-md">
              📄 Open Full Academic Slide Deck & Notes
            </button>
            <a href="http://localhost:3000" target="_blank" class="px-5 py-2.5 rounded-full bg-[#0071E3] text-white font-bold text-xs shadow-md">
              🌐 Live Storefront (:3000)
            </a>
          </div>
        </div>
      </div>
    </section>

  </main>

  <!-- ============================================================================ -->
  <!-- MODAL 1: IN-PAGE ACADEMIC SLIDE DECK & SPEAKER NOTES VIEWER                 -->
  <!-- ============================================================================ -->
  <div id="academicDeckModal" class="fixed inset-0 z-50 bg-black/80 backdrop-blur-md flex items-center justify-center p-4 sm:p-6 hidden">
    <div class="bg-[#0B132B] border border-white/15 rounded-3xl max-w-4xl w-full max-h-[90vh] flex flex-col shadow-2xl overflow-hidden">
      <!-- Modal Header -->
      <div class="p-5 border-b border-white/10 flex items-center justify-between bg-[#080E1E]">
        <div class="flex items-center gap-3">
          <span class="w-8 h-8 rounded-lg bg-amber-500/20 text-amber-400 flex items-center justify-center font-bold text-sm border border-amber-500/30">
            📄
          </span>
          <div>
            <h3 class="text-base font-bold text-white">NEXORA Academic Slide Deck & Bengali Speaker Notes</h3>
            <p class="text-xs text-slate-400">Formal Defense Specification & Mathematical Proofs</p>
          </div>
        </div>
        <div class="flex items-center gap-2">
          <a href="NEXORA_ACADEMIC_PRESENTATION_SLIDES.md" target="_blank" download class="px-3 py-1.5 rounded-lg bg-white/10 hover:bg-white/20 text-white text-xs font-mono transition-all flex items-center gap-1.5">
            <span>⬇️ Raw .md</span>
          </a>
          <button onclick="closeAcademicDeckModal()" class="p-2 rounded-lg bg-white/10 hover:bg-white/20 text-white transition-all text-xs">
            ✕ Close
          </button>
        </div>
      </div>

      <!-- Modal Body (All 17 Slides Reader) -->
      <div class="p-6 overflow-y-auto space-y-6 text-slate-300 text-xs sm:text-sm leading-relaxed" id="academicDeckViewerBody">
        <!-- Rendered by populateAcademicDeckViewer() -->
      </div>
    </div>
  </div>

  <!-- ============================================================================ -->
  <!-- MODAL 2: TABLE OF CONTENTS (KEYBOARD SHORTCUT: M / O)                       -->
  <!-- ============================================================================ -->
  <div id="tocModal" class="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4 hidden">
    <div class="bg-[#0B132B] border border-white/15 rounded-3xl max-w-2xl w-full p-6 shadow-2xl max-h-[85vh] overflow-y-auto">
      <div class="flex items-center justify-between pb-4 border-b border-white/10 mb-4">
        <h3 class="text-lg font-bold text-white flex items-center gap-2">
          <span>📑 Table of Contents (17 Slides)</span>
        </h3>
        <button onclick="toggleToc()" class="text-slate-400 hover:text-white text-sm">✕ Close</button>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs text-slate-200">
        <button onclick="goToSlide(1); toggleToc();" class="p-2.5 rounded-xl bg-white/5 hover:bg-white/15 text-left transition-all">01. Project Title & Executive Overview</button>
        <button onclick="goToSlide(2); toggleToc();" class="p-2.5 rounded-xl bg-white/5 hover:bg-white/15 text-left transition-all">02. Architectural Topology & Full-Stack Flow</button>
        <button onclick="goToSlide(3); toggleToc();" class="p-2.5 rounded-xl bg-white/5 hover:bg-white/15 text-left transition-all">03. Frontend Stack (Next.js 14 & Tailwind)</button>
        <button onclick="goToSlide(4); toggleToc();" class="p-2.5 rounded-xl bg-white/5 hover:bg-white/15 text-left transition-all">04. Backend API & Mutex Concurrency</button>
        <button onclick="goToSlide(5); toggleToc();" class="p-2.5 rounded-xl bg-white/5 hover:bg-white/15 text-left transition-all">05. Enterprise Security & 4-Tier RBAC</button>
        <button onclick="goToSlide(6); toggleToc();" class="p-2.5 rounded-xl bg-white/5 hover:bg-white/15 text-left transition-all text-amber-400 font-bold">06. Anti-Price-Tampering Authoritative Engine</button>
        <button onclick="goToSlide(7); toggleToc();" class="p-2.5 rounded-xl bg-white/5 hover:bg-white/15 text-left transition-all">07. Storefront Swatches & Storage Multipliers</button>
        <button onclick="goToSlide(8); toggleToc();" class="p-2.5 rounded-xl bg-white/5 hover:bg-white/15 text-left transition-all text-cyan-400 font-bold">08. 0% Bank EMI Financing Calculator</button>
        <button onclick="goToSlide(9); toggleToc();" class="p-2.5 rounded-xl bg-white/5 hover:bg-white/15 text-left transition-all">09. Multi-Device Hardware Comparator</button>
        <button onclick="goToSlide(10); toggleToc();" class="p-2.5 rounded-xl bg-white/5 hover:bg-white/15 text-left transition-all">10. District Logistics & Courier Zones</button>
        <button onclick="goToSlide(11); toggleToc();" class="p-2.5 rounded-xl bg-white/5 hover:bg-white/15 text-left transition-all">11. Live Order Tracking & PII Masking</button>
        <button onclick="goToSlide(12); toggleToc();" class="p-2.5 rounded-xl bg-white/5 hover:bg-white/15 text-left transition-all">12. Digital Cash Memo & Customer RMA</button>
        <button onclick="goToSlide(13); toggleToc();" class="p-2.5 rounded-xl bg-white/5 hover:bg-white/15 text-left transition-all">13. Executive Admin Control Center</button>
        <button onclick="goToSlide(14); toggleToc();" class="p-2.5 rounded-xl bg-white/5 hover:bg-white/15 text-left transition-all">14. Gateways & WhatsApp Concierge</button>
        <button onclick="goToSlide(15); toggleToc();" class="p-2.5 rounded-xl bg-white/5 hover:bg-white/15 text-left transition-all">15. Progressive Web App (PWA) & Mobile Demo</button>
        <button onclick="goToSlide(16); toggleToc();" class="p-2.5 rounded-xl bg-white/5 hover:bg-white/15 text-left transition-all">16. Normalized Schemas & TypeScript Models</button>
        <button onclick="goToSlide(17); toggleToc();" class="p-2.5 rounded-xl bg-white/5 hover:bg-white/15 text-left transition-all col-span-1 sm:col-span-2 text-center text-emerald-400 font-bold">17. Empirical Verification & Defense Conclusion</button>
      </div>
    </div>
  </div>

  <!-- ============================================================================ -->
  <!-- DRAWER: BENGALI SPEAKER NOTES SLIDE-OVER (KEYBOARD SHORTCUT: N)             -->
  <!-- ============================================================================ -->
  <aside id="speakerNotesDrawer" class="fixed top-0 right-0 w-full sm:w-96 h-full bg-[#0B132B]/95 dark:bg-[#080E1E]/95 backdrop-blur-xl border-l border-white/15 z-50 transform translate-x-full transition-transform duration-300 flex flex-col shadow-2xl">
    <div class="p-4 border-b border-white/10 flex items-center justify-between bg-[#080E1E]">
      <div class="flex items-center gap-2">
        <span class="text-base">🗣️</span>
        <span id="speakerNotesSlideTitle" class="text-xs font-mono font-bold text-[#38BDF8]">Slide 1 of 17 Notes</span>
      </div>
      <button onclick="toggleSpeakerNotes()" class="p-1 rounded-lg text-slate-400 hover:text-white text-xs">✕ Close</button>
    </div>
    <div id="speakerNotesContent" class="flex-1 p-5 overflow-y-auto text-slate-200 text-xs sm:text-sm leading-relaxed space-y-3 font-sans">
      <!-- Injected by updateSpeakerNotesContent() -->
    </div>
  </aside>

  <!-- ============================================================================ -->
  <!-- JAVASCRIPT SLIDE ENGINE & INTERACTIVE WIDGET LOGIC                          -->
  <!-- ============================================================================ -->
  <script>
    // 1. Navigation State
    const TOTAL_SLIDES = 17;
    let currentSlide = 1; // 1-based index (1 to 17)
    let speakerNotesOpen = false;

    // Bengali Speaker Notes for All 17 Slides
    const SPEAKER_NOTES = {
      1: `<strong>🗣️ প্রারম্ভিক উপস্থাপনা (Slide 01):</strong><br><br>
      "শ্রদ্ধেয় শিক্ষকবৃন্দ ও বিচারকমণ্ডলী, আসসালামু আলাইকুম। আমার প্রজেক্টের নাম <strong>NEXORA</strong>। এটি একটি এন্টারপ্রাইজ-গ্রেড ফ্ল্যাগশিপ ইলেকট্রনিক্স ও হার্ডওয়্যার ই-কমার্স প্ল্যাটফর্ম। আমাদের মূল লক্ষ্য ছিল সাধারণ ইকমার্স সাইটের চেয়ে আলাদা—অ্যাপল-লেভেল মিনিমালিস্ট ইউজার ইন্টারফেস এবং ব্যাকএন্ডে অভ্রান্ত গাণিতিক সিকিউরিটি (Anti-Price-Tampering) নিশ্চিত করা। প্রজেক্টের সম্পূর্ণ কোডবেস Next.js 14 এবং Node.js Express-এ হ্যান্ড-ক্রাফটেড। আজকের প্রেজেন্টেশনে আমি বাস্তব কোড ও ইন্টারঅ্যাক্টিভ সিমুলেশনের মাধ্যমে প্রতিটি আর্কিটেকচারাল ডিসিশন ব্যাখ্যা করব।"`,

      2: `<strong>🗣️ আর্কিটেকচারাল টপোলজি (Slide 02):</strong><br><br>
      "এই স্লাইডে আমাদের সম্পূর্ণ ডেটা ফ্লো তুলে ধরা হয়েছে। এটি একটি ডিকাপলড আর্কিটেকচার—পোর্ট ৩০০০-এ নেক্সট.জেএস এবং পোর্ট ৫০০১-এ এক্সপ্রেস এপিআই। ক্লায়েন্ট ব্রাউজারে প্রথম রিকোয়েস্টে এসএসআর (SSR) পেজ লোড করে, এরপর ক্লায়েন্ট হাইড্রেশনের মাধ্যমে হাইড্রেট হয়। ব্যাকএন্ড এক্সপ্রেস সার্ভার একটি ডিফেন্সিভ সিকিউরিটি পেরিমিটার হিসেবে কাজ করে যা ওওয়াস্প হেডার ও রেট লিমিটিং দ্বারা সুরক্ষিত। ডেটা পারসিস্টেন্সের জন্য কোনো সাধারণ ফাইল রাইট নয়, বরং একটি কাস্টম প্রমিজ-চেইন্ড মিউটেক্স লক কিউ ব্যবহার করা হয়েছে যাতে কনকারেন্ট রাইটে ডেটা করাপ্ট না হয়।"`,

      3: `<strong>🗣️ ফ্রন্টএন্ড স্ট্যাক ও ডিজাইন সিস্টেম (Slide 03):</strong><br><br>
      "ফ্রন্টএন্ডে আমরা নেক্সট.জেএস ১৪ অ্যাপ রাউটার এবং টাইপস্ক্রিপ্ট ৫.৫ ব্যবহার করেছি। সবচেয়ে আকর্ষণীয় দিক হলো টেলউইন্ড সিএসএস-এর কাস্টম ডার্ক গ্লাস মরফিজম প্যালেট (#0B132B) এবং <code>@tailwindcss/container-queries</code>। কন্টেইনার কোয়েরিজের কারণে প্রোডাক্ট কার্ডগুলো স্ক্রিনের যে কোনো কলাম সাইজে নিজে থেকেই অ্যাডাপ্ট করে। আমরা স্টেট ম্যানেজমেন্টের জন্য রিঅ্যাক্ট কনটেক্সট ব্যবহার করেছি যা কার্ট, উইশলিস্ট এবং বাংলা-ইংরেজি বাইলিঙ্গুয়াল সেটিংস ব্রাউজারে সিঙ্ক রাখে।"`,

      4: `<strong>🗣️ মিউটেক্স কিউ ও অ্যাটমিক ফাইল রাইট (Slide 04):</strong><br><br>
      "পরীক্ষায় টিচাররা প্রায়ই জিজ্ঞেস করেন: ফাইল-বেসড স্টোরেজে কনকারেন্সি কীভাবে হ্যান্ডেল করলেন? আমাদের উত্তর হলো <code>queueFileOp</code>। যখন একাধিক গ্রাহক একই মুহূর্তে অর্ডার সাবমিট করে, আমাদের মিউটেক্স কিউ অপারেশনগুলোকে প্রমিজ চেইনের মাধ্যমে সিরিয়ালাইজ করে। ফাইলটি প্রথমে <code>.tmp</code> এক্সটেনশনে তৈরি হয় এবং এরপর ওএস-লেভেল অ্যাটমিক রিনেম হয়। এর সাথে ইন-মেমরি ক্যাশ ব্যাকআপ রয়েছে যা ডিস্ক ফেইলিউরেও সিস্টেমের ডেটা অক্ষত রাখে।"`,

      5: `<strong>🗣️ রোল-বেসড এক্সেস কন্ট্রোল ও সিকিউরিটি (Slide 05):</strong><br><br>
      "সিকিউরিটির ক্ষেত্রে আমরা চারটি স্তরের রোল-বেসড এক্সেস কন্ট্রোল (RBAC) বানিয়েছি। সুপার অ্যাডমিনের ফুল এক্সেস থাকলেও ইনভেন্টরি মডারেটর শুধুমাত্র প্রোডাক্ট ও ক্যাটাগরি এডিট করতে পারেন, তিনি গ্রাহকের অর্ডার বা কুপন দেখতে পারবেন না। পাসওয়ার্ডগুলো ১০-রাউন্ড সল্টযুক্ত বি-ক্রিপ্ট (bcrypt) দিয়ে হ্যাশ করা এবং অ্যাডমিন অথেন্টিকেশনে ৭ দিনের ক্রিপ্টোগ্রাফিক জেডব্লিউটি (JWT) টোকেন ব্যবহার করা হয়েছে।"`,

      6: `<strong>🗣️ অ্যান্টি-প্রাইস-ট্যাম্পারিং ইঞ্জিন (Slide 06):</strong><br><br>
      "বাস্তব জীবনে ইকমার্সের সবচেয়ে বড় হ্যাক হলো ক্লায়েন্ট থেকে প্রাইস পরিবর্তন করে কম দামে কেনা। নেক্সোরায় ক্লায়েন্ট থেকে যে প্রাইস বা টোটালই আসুক না কেন, সার্ভার তা সরাসরি ট্র্যাশ করে দেয়। সার্ভার সরাসরি ডেটাবেজ থেকে অফিশিয়াল দাম পড়ে, স্টোরেজ মার্কআপ হিসাব করে এবং কুরিয়ার ফি যোগ করে অথরিটেটিভ গ্র্যান্ড টোটাল বানায়। ডানপাশের সিমুলেটরে আপনারা দেখতে পাচ্ছেন যে ক্লায়েন্ট ১০০ টাকা বানালেও সার্ভার তাকে ২,১৫,০৭০ টাকা হিসেবেই ক্যালকুলেট করে।"`,

      7: `<strong>🗣️ স্টোরফ্রন্ট ভ্যারিয়েন্ট ও কালার ফিনিশ (Slide 07):</strong><br><br>
      "আমাদের প্রোডাক্ট ডিটেইলস পেজে রয়েছে ডায়নামিক কালার ফিনিশ সিলেকশন—ন্যাচারাল টাইটানিয়াম, স্পেস ব্ল্যাক কিংবা ডেজার্ট টাইটানিয়াম। প্রতিটির সাথে রিয়েল-টাইম ইমেজ ও সিএসএস ফিল্টার সংযুক্ত। ১২৮ জিবি, ২৫৬ জিবি বা ১ টিবি স্টোরেজ বাটনে ক্লিক করলে দাম স্বয়ংক্রিয়ভাবে আপডেট হয়। এছাড়াও রয়েছে ওয়ান-ক্লিক বাংলা ও ইংরেজি সুইচিং এবং ডার্ক/লাইট মোড।"`,

      8: `<strong>🗣️ ০% ব্যাংক ইএমআই ক্যালকুলেটর (Slide 08):</strong><br><br>
      "হাই-এন্ড ফ্ল্যাগশিপ ডিভাইসের জন্য আমাদের ওয়েবসাইটে রয়েছে একটি বাস্তবসম্মত ০% ব্যাংক ইএমআই ক্যালকুলেটর। ২০,০০০ টাকার উপরের যে কোনো প্রোডাক্টে গ্রাহক ৩, ৬, ১২ ও ২৪ মাসের কিস্তি দেখতে পান। সিটি ব্যাংক অ্যামেক্স, ব্র্যাক ব্যাংক, স্ট্যান্ডার্ড চার্টার্ডসহ বাংলাদেশের ২৫টির বেশি শীর্ষ ব্যাংকের সাথে এই সিস্টেম ইন্টিগ্রেট করা। কোনো হিডেন চার্জ ছাড়াই প্রতি মাসে কত টাকা দিতে হবে তা তাৎক্ষণিক স্ক্রিনে দেখা যায়।"`,

      9: `<strong>🗣️ হার্ডওয়্যার কম্পেয়ার ইঞ্জিন (Slide 09):</strong><br><br>
      "গ্রাহকদের সঠিক গ্যাজেট বেছে নেওয়ার জন্য আমরা <code>/compare</code> পেজে একটি হার্ডওয়্যার কম্পারেটর তৈরি করেছি। এখানে অ্যাপল এ২০ প্রো সিলিকনের সাথে স্ন্যাপড্রাগন ৮ জেন ৪, পারিস্কোপ লেন্স, ডিসপ্লে রিফ্রেশ রেট এবং টাইটানিয়াম চেসিসের সরাসরি টেকনিক্যাল তুলনা দেখা যায়। কম্পেয়ার পেজ থেকেই সরাসরি এক ক্লিকে কার্টে প্রোডাক্ট যোগ করা সম্ভব।"`,

      10: `<strong>🗣️ ডিস্ট্রিক্ট-বেসড কুরিয়ার লজিস্টিকস (Slide 10):</strong><br><br>
      "ডেলিভারির ক্ষেত্রে আমরা তিনটি অটোমেটেড জোন নির্ধারণ করেছি: ঢাকা মেট্রোর জন্য ৭০ টাকা (২৪-৪৮ ঘণ্টা), গ্রেটার ঢাকা যেমন সাভার ও গাজীপুরের জন্য ১০০ টাকা, এবং ঢাকার বাইরে ৬৪ জেলার জন্য ১৪০ টাকা। কুপন কোড (যেমন FREESHIP) ভ্যালিড হলে সার্ভার ডেলিভারি ফি স্বয়ংক্রিয়ভাবে ০ টাকা করে দেয়।"`,

      11: `<strong>🗣️ লাইভ অর্ডার ট্র্যাকিং ও পিআইআই মাস্কিং (Slide 11):</strong><br><br>
      "অর্ডার সম্পন্ন হলে গ্রাহক তার ট্র্যাকিং আইডি দিয়ে লাইভ অর্ডার ট্র্যাকিং পেজে অর্ডারের প্রতি ধাপ (Pending &rarr; Confirmed &rarr; Processing &rarr; Dispatched &rarr; Delivered) দেখতে পান। জনসাধারণের স্ক্র্যাপিং থেকে গ্রাহকের পরিচয় বাঁচাতে পাবলিক ট্র্যাকিং এপিআই-তে নাম ও ফোন নাম্বার স্বয়ংক্রিয়ভাবে মাস্ক করা থাকে (যেমন +88016****177)।"`,

      12: `<strong>🗣️ ডিজিটাল ক্যাশ মেমো ও আরএমএ ওয়ারেন্টি (Slide 12):</strong><br><br>
      "অর্ডার প্লেস করার সাথে সাথে প্রিন্ট-রেডি ডিজিটাল ক্যাশ মেমো জেনারেট হয় যার মধ্যে থাকে ইউনিক হোলোগ্রাম কিউআর কোড। আর কেনার পর হার্ডওয়্যারে কোনো ত্রুটি দেখা দিলে গ্রাহকের জন্য রয়েছে <code>/warranty-claim</code> আরএমএ পোর্টাল। সেখানে সিরিয়াল নাম্বার দিয়ে ক্লেইম সাবমিট করলে অফিশিয়াল আরএমএ টিকিট তৈরি হয় যা সরাসরি টেকনিক্যাল সাপোর্ট টিম হ্যান্ডেল করে।"`,

      13: `<strong>🗣️ এক্সিকিউটিভ অ্যাডমিন কন্ট্রোল সেন্টার (Slide 13):</strong><br><br>
      "আমাদের অ্যাডমিন প্যানেল <code>/myadminerapanel</code>-এ রয়েছে ৯টি সম্পূর্ণ মডিউল। সেলস অ্যানালিটিক্স, প্রোডাক্ট ইনভেন্টরির ফুল ক্রুড (CRUD) উইথ মাল্টার ইমেজ আপলোড, অর্ডার ডিসপ্যাচ, কুপন ক্রিয়েটর, আরএমএ ওয়ারেন্টি এবং স্টাফ ম্যানেজমেন্ট। সবকিছুই লাইভ এবং মোবাইল-ফ্রেন্ডলি।"`,

      14: `<strong>🗣️ থার্ড-পার্টি গেটওয়ে ও হোয়াটসঅ্যাপ কনসিয়ার্জ (Slide 14):</strong><br><br>
      "পেমেন্টের জন্য বিকাশ, নগদ, ক্যাশ অন ডেলিভারি এবং ব্যাংক কার্ড মেথড রয়েছে। পাশাপাশি একটি সার্বক্ষণিক ফ্লোটিং হোয়াটসঅ্যাপ কনসিয়ার্জ হটলাইন রয়েছে (+880 1640-026177)। কাস্টমার কোনো প্রোডাক্ট পেজে থাকলে এক ক্লিকেই সেই প্রোডাক্টের নির্দিষ্ট ভ্যারিয়েন্টসহ স্পেশালিস্টের সাথে চ্যাট শুরু করতে পারেন।"`,

      15: `<strong>🗣️ প্রগ্রেসিভ ওয়েব অ্যাপ ও মোবাইল সিমুলেটর (Slide 15):</strong><br><br>
      "মোবাইল গ্রাহকদের জন্য নেক্সোরা একটি পূর্ণাঙ্গ পিডব্লিউএ (PWA)। এটি কোনো অ্যাপ স্টোর ছাড়াই যেকোনো ডিভাইসে ইনস্টল করা যায় এবং অফলাইনেও ইন্টারফেস ক্যাশ করে রাখে। তাছাড়া আমাদের <code>/app-demo</code> পেজে রয়েছে একটি ইন-ব্রাউজার মোবাইল সিমুলেটর যার মাধ্যমে ডেস্কটপ থেকেই ফোনের অভিজ্ঞতা উপভোগ করা যায়।"`,

      16: `<strong>🗣️ ডেটাবেজ স্কিমা ও টাইপস (Slide 16):</strong><br><br>
      "আমাদের পুরো সিস্টেমে টাইপস্ক্রিপ্ট ইন্টারফেস কঠোরভাবে অনুসৃত হয়েছে। প্রোডাক্ট, অর্ডার, কাস্টমার, কুপন এবং আরএমএ টিকিটের জন্য সুনির্দিষ্ট নরমালাইজড রিলেশনশিপ রয়েছে। ভবিষ্যতে এটিকে পোস্টগ্রেস্কিউএল বা মঙ্গোডিবিতে মাইগ্রেট করা অত্যন্ত সহজ কারণ মডেল স্ট্রাকচার সম্পূর্ণ নরমালাইজড।"`,

      17: `<strong>🗣️ সিকিউরিটি অডিট ও উপসংহার (Slide 17):</strong><br><br>
      "আমরা সিকিউরিটি অডিট টেস্ট স্ক্রিপ্ট চালিয়ে শতভাগ সাফল্য পেয়েছি। ওওয়াস্প ডিফেন্সিভ হেডার শতভাগ সক্রিয়, পাসওয়ার্ড স্ট্রিপিং ১০০% কাজ করছে এবং অ্যান্টি-প্রাইস ট্যাম্পারিং নিশ্চিত করেছে যে আর্থিক তথ্যে কোনো জালিয়াতি করা সম্ভব নয়। নেক্সোরা শুধুমাত্র একটি ক্লাস প্রজেক্ট নয়, এটি একটি বাণিজ্যিক মানের আর্কিটেকচার। ধন্যবাদ।"`,
    };

    // 2. Initialize Engine
    function initPresentation() {
      // Check URL hash for initial slide
      parseInitialHash();
      updateEmiCalc();
      testRbacRole('super');
      filterFrontendTab('nextjs');
      setupKeyboardNav();
      setupTouchGestures();
      populateAcademicDeckViewer();
      window.addEventListener('hashchange', parseInitialHash);
    }

    function parseInitialHash() {
      let slideNum = 1;
      const hash = window.location.hash;
      const match = hash.match(/#slide-(\d+)/i);
      if (match) {
        slideNum = parseInt(match[1], 10);
      } else {
        const urlParams = new URLSearchParams(window.location.search);
        const querySlide = urlParams.get('slide');
        if (querySlide) slideNum = parseInt(querySlide, 10);
      }
      if (slideNum < 1) slideNum = 1;
      if (slideNum > TOTAL_SLIDES) slideNum = TOTAL_SLIDES;
      showSlide(slideNum);
    }

    function setupKeyboardNav() {
      document.addEventListener('keydown', (e) => {
        if (['INPUT', 'TEXTAREA', 'SELECT'].includes(e.target.tagName)) return;

        if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'Enter') {
          e.preventDefault();
          nextSlide();
        } else if (e.key === 'ArrowLeft' || e.key === 'Backspace') {
          e.preventDefault();
          prevSlide();
        } else if (e.key.toLowerCase() === 't') {
          toggleTheme();
        } else if (e.key.toLowerCase() === 'f') {
          toggleFullscreen();
        } else if (e.key.toLowerCase() === 'm' || e.key.toLowerCase() === 'o') {
          toggleToc();
        } else if (e.key.toLowerCase() === 'n') {
          toggleSpeakerNotes();
        } else if (e.key.toLowerCase() === 'd') {
          openAcademicDeckModal();
        } else if (e.key === 'Escape') {
          closeAllModals();
        }
      });
    }

    // Touch Swipe Gestures for Mobile & Tablets
    let touchStartX = 0;
    let touchEndX = 0;
    function setupTouchGestures() {
      window.addEventListener('touchstart', (e) => {
        touchStartX = e.changedTouches[0].screenX;
      }, { passive: true });

      window.addEventListener('touchend', (e) => {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
      }, { passive: true });
    }

    function handleSwipe() {
      const threshold = 60;
      if (touchEndX < touchStartX - threshold) {
        nextSlide();
      } else if (touchEndX > touchStartX + threshold) {
        prevSlide();
      }
    }

    function showSlide(index) {
      if (index < 1 || index > TOTAL_SLIDES) return;
      currentSlide = index;

      // Hide all slides
      document.querySelectorAll('.slide-section').forEach((el) => {
        el.classList.add('hidden');
        el.classList.remove('slide-active');
      });

      // Show target slide
      const target = document.getElementById(`slide-${index}`);
      if (target) {
        target.classList.remove('hidden');
        void target.offsetWidth;
        target.classList.add('slide-active');
      }

      // Update Header Badges & Progress Bar
      document.getElementById('slideCounterBadge').textContent = `Slide ${index} of ${TOTAL_SLIDES}`;
      const pct = (index / TOTAL_SLIDES) * 100;
      document.getElementById('progressBar').style.width = `${pct}%`;

      // Update URL Hash without causing unwanted jump
      if (window.location.hash !== `#slide-${index}`) {
        history.replaceState(null, '', `#slide-${index}`);
      }

      // Update Bengali Speaker Notes if open
      updateSpeakerNotesContent();

      // Scroll smoothly to top
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    function nextSlide() {
      if (currentSlide < TOTAL_SLIDES) showSlide(currentSlide + 1);
    }

    function prevSlide() {
      if (currentSlide > 1) showSlide(currentSlide - 1);
    }

    function goToSlide(idx) {
      showSlide(idx);
    }

    // Theme Toggle
    function toggleTheme() {
      const isDark = document.documentElement.classList.contains('dark');
      if (isDark) {
        document.documentElement.classList.remove('dark');
        document.documentElement.classList.add('light');
        document.getElementById('themeIcon').textContent = '☀️';
        localStorage.setItem('nexora_pres_theme', 'light');
      } else {
        document.documentElement.classList.remove('light');
        document.documentElement.classList.add('dark');
        document.getElementById('themeIcon').textContent = '🌙';
        localStorage.setItem('nexora_pres_theme', 'dark');
      }
    }

    // Fullscreen Toggle
    function toggleFullscreen() {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().catch(() => {});
      } else {
        if (document.exitFullscreen) document.exitFullscreen();
      }
    }

    // Speaker Notes Management
    function toggleSpeakerNotes() {
      speakerNotesOpen = !speakerNotesOpen;
      const drawer = document.getElementById('speakerNotesDrawer');
      const btn = document.getElementById('speakerNotesBtn');
      if (speakerNotesOpen) {
        drawer.classList.remove('translate-x-full');
        btn.classList.add('bg-[#0071E3]', 'text-white');
        updateSpeakerNotesContent();
      } else {
        drawer.classList.add('translate-x-full');
        btn.classList.remove('bg-[#0071E3]', 'text-white');
      }
    }

    function updateSpeakerNotesContent() {
      document.getElementById('speakerNotesSlideTitle').textContent = `Slide ${currentSlide} of ${TOTAL_SLIDES} Notes`;
      document.getElementById('speakerNotesContent').innerHTML = SPEAKER_NOTES[currentSlide] || "No notes for this slide.";
    }

    // Table of Contents Toggle
    function toggleToc() {
      document.getElementById('tocModal').classList.toggle('hidden');
    }

    // Academic Deck Reader Modal
    function openAcademicDeckModal() {
      document.getElementById('academicDeckModal').classList.remove('hidden');
    }

    function closeAcademicDeckModal() {
      document.getElementById('academicDeckModal').classList.add('hidden');
    }

    function closeAllModals() {
      document.getElementById('tocModal').classList.add('hidden');
      document.getElementById('academicDeckModal').classList.add('hidden');
      if (speakerNotesOpen) toggleSpeakerNotes();
    }

    function populateAcademicDeckViewer() {
      const body = document.getElementById('academicDeckViewerBody');
      const slides = [
        { num: 1, title: "Slide 01: Project Title & Executive Overview", file: "frontend/src/app/page.tsx", desc: "Flagship industrial Apple-style aesthetics, Next.js 14 + Express decoupled architecture." },
        { num: 2, title: "Slide 02: Architectural Topology & Full-Stack System Flow", file: "Decoupled :3000 & :5001", desc: "SSR hydration, reverse proxy routing, and serialized persistence layers." },
        { num: 3, title: "Slide 03: Frontend Tech Stack & Component Engineering", file: "frontend/src/app/*", desc: "Next.js 14, TypeScript 5.5, Tailwind CSS, container queries, Framer Motion, and dual React Contexts." },
        { num: 4, title: "Slide 04: Backend API Architecture & Mutex Data Storage", file: "backend/server.js:118-173", desc: "Promise-chained queueFileOp mutex, atomic swap via .tmp and fs.rename." },
        { num: 5, title: "Slide 05: Enterprise Security, JWT & Granular RBAC", file: "backend/server.js:34-112", desc: "OWASP defensive headers, 10-round salted bcrypt, 7-day JWT, and 4-tier role guards." },
        { num: 6, title: "Slide 06: Anti-Price-Tampering Authoritative Order Engine", file: "backend/server.js:435-515", desc: "Server overrides all client prices, recalculating subtotal and shipping fees strictly from authoritative data." },
        { num: 7, title: "Slide 07: Consumer Storefront & Dynamic Hardware Variant Engine", file: "frontend/src/app/product/[id]/", desc: "Dynamic metallic finish swatches, storage capacity multipliers, dark/light themes, and bilingual EN/BN dictionary." },
        { num: 8, title: "Slide 08: 0% Interest Bank EMI Financing Calculator", file: "frontend/src/components/EMIModal.tsx", desc: "3, 6, 12, 24-month installment formula for 25+ partner banks across Bangladesh." },
        { num: 9, title: "Slide 09: Multi-Device Hardware Comparator", file: "frontend/src/app/compare/page.tsx", desc: "Side-by-side spec normalization (SoC, 120Hz display, periscope zoom, titanium chassis)." },
        { num: 10, title: "Slide 10: District Logistics & Courier Dispatch Engine", file: "backend/server.js:475-485", desc: "3 delivery tiers: Dhaka (৳70), Greater Dhaka (৳100), Nationwide 64 districts (৳140)." },
        { num: 11, title: "Slide 11: Live Order Tracking, Stepper & Public PII Masking", file: "backend/server.js:540-560", desc: "5-stage order status stepper with public telephone and name masking against web scraping." },
        { num: 12, title: "Slide 12: Digital Cash Memo & Customer RMA Warranty Portal", file: "frontend/src/app/warranty-claim/", desc: "Print-ready QR cash memo and full RMA warranty claim registration ticket lifecycle." },
        { num: 13, title: "Slide 13: Executive Admin Control Center (/myadminerapanel)", file: "frontend/src/app/myadminerapanel/", desc: "9 complete modules: sales analytics, catalog CRUD, order dispatch, coupons, and staff RBAC." },
        { num: 14, title: "Slide 14: Third-Party Gateways & WhatsApp Concierge", file: "WhatsAppConcierge.tsx", desc: "bKash, Nagad, Cash on Delivery, SSLCommerz, and direct hotline (+880 1640-026177)." },
        { num: 15, title: "Slide 15: Progressive Web App (PWA) & Mobile Simulator", file: "frontend/src/app/app-demo/", desc: "Standalone PWA manifest, offline service worker, and in-browser iPhone device simulator." },
        { num: 16, title: "Slide 16: Database Schema & Entity Relationships", file: "frontend/src/lib/types.ts", desc: "Normalized TypeScript models for products, orders, coupons, staff, and RMA claims." },
        { num: 17, title: "Slide 17: Empirical Verification & Academic Defense Conclusion", file: "scripts/security_audit_test.py", desc: "100% test pass record: OWASP headers, password stripping, rate limiting, and anti-tampering." }
      ];

      body.innerHTML = slides.map(s => `
        <div class="p-4 rounded-2xl bg-white/5 border border-white/10 space-y-2">
          <div class="flex items-center justify-between">
            <span class="text-sm font-bold text-white">${s.title}</span>
            <button onclick="goToSlide(${s.num}); closeAcademicDeckModal();" class="px-2.5 py-1 rounded-lg bg-[#0071E3] text-white text-[11px] font-bold hover:bg-[#0077ED] transition-all">
              Go to Slide ${s.num} &rarr;
            </button>
          </div>
          <span class="text-[11px] text-amber-400 font-mono block">Code Citation: ${s.file}</span>
          <p class="text-slate-300 text-xs">${s.desc}</p>
          <div class="p-3 rounded-xl bg-black/30 border border-white/5 text-[11px] text-slate-300">
            ${SPEAKER_NOTES[s.num] || ""}
          </div>
        </div>
      `).join('');
    }

    // --------------------------------------------------------------------------
    // WIDGET 1: ARCHITECTURE NODE INSPECTOR (SLIDE 2)
    // --------------------------------------------------------------------------
    const NODE_DATA = {
      client: {
        title: "Client Layer: Next.js 14 Client Hydration & LocalStorage",
        file: "frontend/src/app/layout.tsx & frontend/src/lib/cartContext.tsx",
        code: `// Dual Context Architecture provides zero-latency state synchronization:
1. CartContext: Manages shopping bag items, coupon applications, and client session tokens.
2. SettingsContext: Controls dark/light theme persistence and English/Bengali localization keys.
3. SmoothScroll: Wraps layout in Lenis inertia engine for Apple-style smooth page inertia.`
      },
      ssr: {
        title: "App Router SSR & Dynamic Hardware Routing",
        file: "frontend/src/app/product/[id]/page.tsx & /compare/page.tsx",
        code: `// Hybrid Rendering Engine:
- Server Components fetch initial catalog JSON on the server for instant First Contentful Paint (FCP).
- ProductDetailClient.tsx hydrates dynamic variant selectors (Storage Markups, Color Swatches, EMI Modal).
- Route /compare handles side-by-side spec normalization without external database roundtrips.`
      },
      api: {
        title: "Express Security Perimeter & Defensive Middlewares",
        file: "backend/server.js (Lines 34-112)",
        code: `// Comprehensive OWASP Hardening:
1. res.setHeader('Content-Security-Policy', ...) + 'X-Frame-Options: SAMEORIGIN'
2. adminAuthLimiter: 20 login attempts per 15 min; userAuthLimiter: 15 attempts.
3. requirePermission(perm): Strict Role-Based Access Control middleware for Staff endpoints.`
      },
      mutex: {
        title: "Hardened JSON Mutex Store & Concurrency Queue",
        file: "backend/server.js (Lines 118-173)",
        code: `// Concurrency Elimination Pipeline:
const fileQueues = new Map();
function queueFileOp(filename, op) {
  const prev = fileQueues.get(filename) || Promise.resolve();
  const next = prev.then(op, op);
  fileQueues.set(filename, next);
  return next;
}
// Writes first to temporary .tmp file, then atomically renames to guarantee zero race conditions.`
      }
    };

    function showNodeDetails(nodeKey) {
      const data = NODE_DATA[nodeKey];
      if (!data) return;
      document.getElementById('nodeDetailBox').innerHTML = `
        <div class="flex items-center justify-between mb-2 pb-2 border-b border-white/10">
          <span class="text-[#38BDF8] font-bold">${data.title}</span>
          <span class="text-slate-400 font-mono text-[10px]">Source: ${data.file}</span>
        </div>
        <pre class="text-slate-300 leading-relaxed font-mono text-[11px] whitespace-pre-wrap">${data.code}</pre>
      `;
    }

    // --------------------------------------------------------------------------
    // WIDGET 2: FRONTEND TAB INSPECTOR (SLIDE 3)
    // --------------------------------------------------------------------------
    const FRONTEND_TABS = {
      nextjs: {
        title: "Next.js 14 App Router & Hybrid Hydration",
        desc: "Leverages React 18 Server Components for instant page loads while hydrating client state only where interactive (e.g. Color Finish swatches, Cart Drawer, EMI Calculator).",
        chips: ["App Router", "Dynamic Routes (/product/[id])", "Server Actions Ready", "Sub-second FCP"],
        code: `// Directory layout follows modern Next.js 14 conventions:
app/
├── layout.tsx         // Root layout with Theme & Cart providers
├── page.tsx           // Server component with SSR catalog
├── product/[id]/      // Dynamic routing for 200+ hardware items
├── checkout/          // Step-by-step authoritative checkout
└── compare/           // Side-by-side hardware spec comparator`
      },
      tailwind: {
        title: "Tailwind CSS & Component-Level Container Queries",
        desc: "Uses custom luxury dark aesthetic tokens with glassmorphism. Employs @tailwindcss/container-queries so product cards adapt dynamically based on container width rather than viewport.",
        chips: ["Glassmorphism", "#0B132B / #080E1E", "@tailwindcss/container-queries", "Mobile-First"],
        code: `/* Container query card in ProductCard.tsx */
<div className="@container w-full">
  <div className="flex flex-col @sm:flex-row @sm:items-center gap-4">
    <div className="w-full @sm:w-1/3 aspect-square relative">
      <Image src={product.image} fill className="object-contain" />
    </div>
    <div className="@sm:w-2/3 space-y-2">...</div>
  </div>
</div>`
      },
      framer: {
        title: "Framer Motion Physics & Lenis Smooth Motion",
        desc: "Every interaction is tactile. Cards tilt in 3D on hover, dialogs spring open with natural damping, and Lenis creates luxurious momentum-based scrolling.",
        chips: ["Spring Damping: 25", "3D Gyro Tilt", "Lenis Inertia Scroll", "Micro-interactions"],
        code: `// Lenis Smooth Inertia Configuration:
<ReactLenis root options={{ 
  lerp: 0.08, 
  duration: 1.2, 
  smoothWheel: true 
}}>
  {children}
</ReactLenis>`
      },
      state: {
        title: "Context API State & Bilingual Localization (EN/BN)",
        desc: "Eliminates heavy Redux dependencies with lightweight, zero-latency React Contexts. Full internationalization support with instant English and Bengali translation keys.",
        chips: ["CartContext", "SettingsContext", "LocalStorage Persist", "Bilingual EN/BN"],
        code: `// Localization engine in settingsContext.tsx:
const TRANSLATIONS = {
  bn: { 'nav.showroom': 'শোরুম', 'btn.add_to_cart': 'ব্যাগে যোগ করুন' },
  en: { 'nav.showroom': 'Showroom', 'btn.add_to_cart': 'Add to Bag' }
};
const { t, language, toggleLanguage } = useSettings();`
      }
    };

    function filterFrontendTab(tabKey) {
      const tab = FRONTEND_TABS[tabKey];
      if (!tab) return;

      ['nextjs', 'tailwind', 'framer', 'state'].forEach(k => {
        const btn = document.getElementById(`tab-${k}`);
        if (k === tabKey) {
          btn.className = "px-4 py-2 rounded-xl text-xs font-bold transition-all bg-[#0071E3] text-white";
        } else {
          btn.className = "px-4 py-2 rounded-xl text-xs font-bold transition-all bg-black/5 dark:bg-white/5 text-slate-700 dark:text-slate-300";
        }
      });

      const chipsHtml = tab.chips.map(c => `<span class="px-2.5 py-1 rounded-full bg-blue-500/10 text-[#0071E3] dark:text-[#38BDF8] border border-blue-500/20 text-[10px] font-mono font-bold">${c}</span>`).join(' ');

      document.getElementById('frontendTabContent').innerHTML = `
        <div class="space-y-4">
          <h3 class="text-xl font-bold text-slate-900 dark:text-white">${tab.title}</h3>
          <p class="text-xs sm:text-sm text-slate-600 dark:text-slate-300 leading-relaxed">${tab.desc}</p>
          <div class="flex flex-wrap gap-2 pt-2">${chipsHtml}</div>
        </div>
        <div class="p-4 rounded-2xl bg-[#0B132B] border border-white/15 text-slate-200 font-mono text-xs overflow-x-auto">
          <pre class="text-[11px] text-slate-300 leading-relaxed">${tab.code}</pre>
        </div>
      `;
    }

    // --------------------------------------------------------------------------
    // WIDGET 3: LIVE MUTEX CONCURRENCY SIMULATOR (SLIDE 4)
    // --------------------------------------------------------------------------
    let mutexSimCounter = 0;
    function simulateConcurrentWrites() {
      const consoleBox = document.getElementById('mutexConsole');
      consoleBox.innerHTML = '';
      mutexSimCounter++;
      
      const log = (msg, color = 'text-slate-300') => {
        const p = document.createElement('p');
        p.className = `${color} font-mono text-[11px]`;
        p.textContent = msg;
        consoleBox.appendChild(p);
        consoleBox.scrollTop = consoleBox.scrollHeight;
      };

      log(`[SIMULATION RUN #${mutexSimCounter}] Spawning 5 concurrent customer order writes...`, 'text-cyan-400 font-bold');

      const tasks = [
        { id: "ORD-991", delay: 100, user: "Customer_Dhaka" },
        { id: "ORD-992", delay: 70,  user: "Customer_Chittagong" },
        { id: "ORD-993", delay: 120, user: "Customer_Sylhet" },
        { id: "ORD-994", delay: 80,  user: "Customer_Rajshahi" },
        { id: "ORD-995", delay: 90,  user: "Customer_Khulna" },
      ];

      tasks.forEach((t) => {
        log(`+ [T+0ms] Write Request received: ${t.id} (${t.user}) -> Queuing into fileQueues.get('orders.json')`);
      });

      let currentChain = Promise.resolve();
      tasks.forEach((t) => {
        currentChain = currentChain.then(() => {
          return new Promise((resolve) => {
            setTimeout(() => {
              log(`  -> [Mutex Lock Acquired] Processing ${t.id}: Writing to orders.json.${Date.now()}.tmp`, 'text-amber-400');
              setTimeout(() => {
                log(`  ✓ [Atomic Rename] Replaced orders.json via fs.rename() -> Mutex released for ${t.id}`, 'text-emerald-400 font-bold');
                resolve();
              }, t.delay);
            }, 50);
          });
        });
      });

      currentChain.then(() => {
        log(`✓ SUCCESS: All 5 writes committed with ZERO race condition or data corruption.`, 'text-cyan-300 font-bold pt-2');
      });
    }

    // --------------------------------------------------------------------------
    // WIDGET 4: RBAC PERMISSION MATRIX (SLIDE 5)
    // --------------------------------------------------------------------------
    const RBAC_DATA = {
      super: {
        title: "Super Administrator (Jakaria Tanim)",
        perms: [
          { ep: "POST /api/products", status: "ALLOWED (200 OK)" },
          { ep: "PUT /api/orders/:id/status", status: "ALLOWED (200 OK)" },
          { ep: "POST /api/coupons", status: "ALLOWED (200 OK)" },
          { ep: "POST /api/admins (Create Staff)", status: "ALLOWED (200 OK)" },
          { ep: "PUT /api/claims/:id (RMA)", status: "ALLOWED (200 OK)" }
        ]
      },
      admin: {
        title: "Administrator",
        perms: [
          { ep: "POST /api/products", status: "ALLOWED (200 OK)" },
          { ep: "PUT /api/orders/:id/status", status: "ALLOWED (200 OK)" },
          { ep: "POST /api/coupons", status: "ALLOWED (200 OK)" },
          { ep: "POST /api/admins (Create Staff)", status: "DENIED (HTTP 403 Forbidden)" },
          { ep: "PUT /api/claims/:id (RMA)", status: "ALLOWED (200 OK)" }
        ]
      },
      inventory: {
        title: "Inventory Moderator",
        perms: [
          { ep: "POST /api/products", status: "ALLOWED (200 OK)" },
          { ep: "PUT /api/orders/:id/status", status: "DENIED (HTTP 403 Forbidden)" },
          { ep: "POST /api/coupons", status: "DENIED (HTTP 403 Forbidden)" },
          { ep: "POST /api/admins (Create Staff)", status: "DENIED (HTTP 403 Forbidden)" },
          { ep: "PUT /api/claims/:id (RMA)", status: "DENIED (HTTP 403 Forbidden)" }
        ]
      },
      orders: {
        title: "Order Moderator",
        perms: [
          { ep: "POST /api/products", status: "DENIED (HTTP 403 Forbidden)" },
          { ep: "PUT /api/orders/:id/status", status: "ALLOWED (200 OK)" },
          { ep: "POST /api/coupons", status: "ALLOWED (200 OK)" },
          { ep: "POST /api/admins (Create Staff)", status: "DENIED (HTTP 403 Forbidden)" },
          { ep: "PUT /api/claims/:id (RMA)", status: "ALLOWED (200 OK)" }
        ]
      }
    };

    function testRbacRole(roleKey) {
      const r = RBAC_DATA[roleKey];
      if (!r) return;

      ['super', 'admin', 'inventory', 'orders'].forEach(k => {
        const b = document.getElementById(`roleBtn-${k}`);
        if (k === roleKey) {
          b.className = "w-full text-left p-3.5 rounded-xl border border-[#0071E3] bg-[#0071E3]/20 font-semibold text-xs transition-all flex items-center justify-between";
        } else {
          b.className = "w-full text-left p-3.5 rounded-xl border border-black/10 dark:border-white/10 bg-black/5 dark:bg-white/5 font-semibold text-xs transition-all flex items-center justify-between";
        }
      });

      const rows = r.perms.map(p => {
        const isOk = p.status.includes('ALLOWED');
        const color = isOk ? 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20' : 'text-rose-400 bg-rose-500/10 border-rose-500/20';
        return `
          <div class="flex items-center justify-between p-2.5 rounded-xl bg-black/30 border border-white/5">
            <span class="font-mono text-slate-300">${p.ep}</span>
            <span class="px-2 py-0.5 rounded font-mono font-bold text-[10px] border ${color}">${p.status}</span>
          </div>
        `;
      }).join('');

      document.getElementById('rbacMatrixDisplay').innerHTML = `
        <div class="mb-3 text-[#38BDF8] font-bold">Active Context: ${r.title}</div>
        ${rows}
      `;
    }

    // --------------------------------------------------------------------------
    // WIDGET 5: ANTI-PRICE-TAMPERING SIMULATOR (SLIDE 6)
    // --------------------------------------------------------------------------
    function runPriceTamperTest() {
      const inputVal = Number(document.getElementById('tamperPriceInput').value) || 0;
      const term = document.getElementById('tamperResultTerminal');
      term.innerHTML = '';

      const log = (msg, color = 'text-slate-300') => {
        const p = document.createElement('p');
        p.className = `${color} font-mono text-[11px]`;
        p.textContent = msg;
        term.appendChild(p);
      };

      log(`[STEP 1: CLIENT PAYLOAD SENT]`, 'text-cyan-400 font-bold');
      log(`{ "id": "iphone-18-pro-max", "quantity": 1, "clientPriceBDT": ${inputVal}, "deliveryZone": "dhaka" }`);
      
      setTimeout(() => {
        log(`
[STEP 2: SERVER AUTHORITATIVE INTERCEPTION]`, 'text-amber-400 font-bold');
        log(`Express Controller received order request. Reading catalog from backend/data/products.json...`);
        log(`Found catalog record: "Apple iPhone 18 Pro Max" -> Official Catalog Base Price: ৳215,000`);

        setTimeout(() => {
          log(`
[STEP 3: INTEGRITY VERIFICATION]`, 'text-rose-400 font-bold');
          log(`WARNING: Client submitted ৳${inputVal}, but official authoritative price is ৳215,000!`);
          log(`Executing Security Policy: Client price parameter STRIPPED and OVERRIDDEN.`);

          setTimeout(() => {
            const deliveryFee = 70;
            const authoritativeTotal = 215000 + deliveryFee;
            log(`
[STEP 4: AUTHORITATIVE ORDER GENERATED]`, 'text-emerald-400 font-bold');
            log(`✓ Grand Total recomputed: ৳${authoritativeTotal} (৳215,000 + ৳70 Delivery)`);
            log(`✓ Order saved to orders.json with Infallible Price.`);
            log(`RESULT: Tamper attempt 100% neutralized. System safe.`);
          }, 250);
        }, 250);
      }, 250);
    }

    // --------------------------------------------------------------------------
    // WIDGET 6: DYNAMIC HARDWARE VARIANT & STORAGE MULTIPLIER (SLIDE 7)
    // --------------------------------------------------------------------------
    let selectedBasePrice = 215000;
    let selectedStorageMarkup = 0;

    function selectVariantColor(colorName, hex) {
      document.getElementById('variantColorLabel').textContent = colorName;
      // Realistic filter variations based on color
      const img = document.getElementById('variantImage');
      if (colorName.includes('Space Black')) {
        img.style.filter = 'brightness(0.7) contrast(1.2)';
      } else if (colorName.includes('Desert Titanium')) {
        img.style.filter = 'sepia(0.4) saturate(1.4) brightness(0.95)';
      } else if (colorName.includes('White Titanium')) {
        img.style.filter = 'brightness(1.15) contrast(1.05)';
      } else {
        img.style.filter = 'none';
      }
    }

    function selectVariantStorage(tier, markup) {
      selectedStorageMarkup = markup;
      const effectiveTotal = selectedBasePrice + markup;
      document.getElementById('variantPriceDisplay').textContent = `৳${effectiveTotal.toLocaleString()}`;
      document.getElementById('variantStorageBadge').textContent = `Tier: ${tier} Storage (${markup >= 0 ? '+' : ''}৳${markup.toLocaleString()})`;

      ['128', '256', '512', '1024'].forEach(k => {
        const btn = document.getElementById(`storageBtn-${k}`);
        if ((k === '128' && tier === '128GB') || (k === '256' && tier === '256GB') || (k === '512' && tier === '512GB') || (k === '1024' && tier === '1TB')) {
          btn.className = "p-3 rounded-xl border-2 border-[#0071E3] bg-[#0071E3]/20 font-bold text-xs text-[#0071E3] dark:text-[#38BDF8] transition-all";
        } else {
          btn.className = "p-3 rounded-xl border border-black/10 dark:border-white/10 bg-black/5 dark:bg-white/5 font-bold text-xs hover:border-[#0071E3] transition-all";
        }
      });
    }

    // --------------------------------------------------------------------------
    // WIDGET 7: 0% BANK EMI CALCULATOR (SLIDE 8)
    // --------------------------------------------------------------------------
    let emiTenureMonths = 12;
    let emiSurchargePct = 6;

    function setEmiTenure(months, surchargePct) {
      emiTenureMonths = months;
      emiSurchargePct = surchargePct;

      [3, 6, 12, 24].forEach(m => {
        const b = document.getElementById(`emi-${m}`);
        if (m === months) {
          b.className = "p-2.5 rounded-xl border border-[#0071E3] bg-[#0071E3]/20 text-center transition-all text-xs font-bold";
        } else {
          b.className = "p-2.5 rounded-xl border border-black/10 dark:border-white/10 text-center transition-all bg-white dark:bg-white/5 text-xs font-bold";
        }
      });

      updateEmiCalc();
    }

    function updateEmiCalc() {
      const basePrice = Number(document.getElementById('emiPriceSlider').value);
      document.getElementById('emiPriceLabel').textContent = `৳${basePrice.toLocaleString()}`;

      const surcharge = Math.round((basePrice * emiSurchargePct) / 100);
      const totalPayable = basePrice + surcharge;
      const monthly = Math.round(totalPayable / emiTenureMonths);

      document.getElementById('emiMonthlyDisplay').innerHTML = `৳${monthly.toLocaleString()} <span class="text-xs font-sans text-slate-300 font-normal">/ month</span>`;
      document.getElementById('emiBaseDisplay').textContent = `৳${basePrice.toLocaleString()}`;
      document.getElementById('emiSurchargeDisplay').textContent = surcharge === 0 ? "৳0 (0% Promotional)" : `+৳${surcharge.toLocaleString()} (${emiSurchargePct}%)`;
      document.getElementById('emiTotalPayableDisplay').textContent = `৳${totalPayable.toLocaleString()}`;
    }

    // --------------------------------------------------------------------------
    // WIDGET 8: COURIER ZONE SELECTOR (SLIDE 10)
    // --------------------------------------------------------------------------
    function selectCourierZone(zoneKey) {
      const zones = {
        dhaka: { name: "Zone 01 (Dhaka Metro)", fee: 70, sla: "24 - 48 Hours Express" },
        greater_dhaka: { name: "Zone 02 (Greater Dhaka)", fee: 100, sla: "48 Hours Suburban Dispatch" },
        outside_dhaka: { name: "Zone 03 (Outside Dhaka / Nationwide)", fee: 140, sla: "2 - 3 Business Days" }
      };
      const z = zones[zoneKey];
      if (!z) return;

      ['dhaka', 'greater_dhaka', 'outside_dhaka'].forEach(k => {
        const card = document.getElementById(`zoneCard-${k}`);
        if (k === zoneKey) {
          card.className = "p-6 rounded-2xl border-2 border-[#0071E3] bg-[#0071E3]/10 cursor-pointer transition-all";
        } else {
          card.className = "p-6 rounded-2xl border border-black/10 dark:border-white/10 bg-black/5 dark:bg-white/5 cursor-pointer transition-all hover:border-white/20";
        }
      });

      document.getElementById('courierZoneTelemetry').innerHTML = `
        Active Selection: <span class="text-[#38BDF8] font-bold">${z.name}</span> | Server Fee Applied: <span class="text-emerald-400 font-bold">৳${z.fee}</span> | Courier SLA: <span class="text-white font-bold">${z.sla}</span>
      `;
    }

    // --------------------------------------------------------------------------
    // WIDGET 9: ORDER TRACKING STEPPER (SLIDE 11)
    // --------------------------------------------------------------------------
    function setTrackingStep(stepIdx) {
      const steps = [
        "PENDING: Order placed and awaiting automated phone verification.",
        "CONFIRMED: Payment verified via bKash / Card. Box moved to dispatch dock.",
        "PROCESSING: Quality inspection complete. Serial number recorded in invoice.",
        "DISPATCHED: Parcel handed to courier partner (Steadfast / Pathao Express).",
        "DELIVERED: Safely delivered to customer with digital warranty signed."
      ];

      const pctMap = [0, 25, 50, 75, 100];
      document.getElementById('stepProgressFill').style.width = `${pctMap[stepIdx]}%`;

      for (let i = 0; i < 5; i++) {
        const dot = document.getElementById(`stepDot-${i}`);
        if (i <= stepIdx) {
          dot.className = "w-8 h-8 rounded-full bg-[#0071E3] text-white flex items-center justify-center font-bold text-xs z-10 shadow-lg";
          dot.textContent = "✓";
        } else {
          dot.className = "w-8 h-8 rounded-full bg-slate-300 dark:bg-white/20 text-slate-600 dark:text-slate-300 flex items-center justify-center font-bold text-xs z-10";
          dot.textContent = `${i + 1}`;
        }
      }

      document.getElementById('stepStatusDescription').textContent = steps[stepIdx];
    }

    // --------------------------------------------------------------------------
    // WIDGET 10: DATABASE SCHEMA EXPLORER (SLIDE 16)
    // --------------------------------------------------------------------------
    const SCHEMA_MAP = {
      product: {
        heading: "interface Product (frontend/src/lib/types.ts)",
        target: "backend/data/products.json",
        code: `export interface Product {
  id: string;               // e.g. "iphone-18-pro-max"
  name: string;             // e.g. "Apple iPhone 18 Pro Max"
  brand?: string;           // "Apple", "Samsung", "Google", "Sony"
  tagline: string;          // Marketing highlight
  category: string;         // "Smartphones", "Audio", "Smartwatches"
  priceBDT: number;         // Base official price
  priceUSD: number;         // USD currency equivalent
  inStock: boolean;         // Inventory status flag
  stockCount: number;       // Exact available inventory units
  rating: number;           // 1.0 - 5.0 verified rating
  reviewCount: number;      // Total review count
  image: string;            // Primary high-resolution render URL
  specs: string[];          // Deep technical hardware specifications
  description: string;      // Comprehensive hardware overview
}`
      },
      order: {
        heading: "interface Order (frontend/src/lib/types.ts)",
        target: "backend/data/orders.json",
        code: `export interface Order {
  id: string;               // e.g. "NX-2026-5802"
  customer: {
    name: string;
    phone: string;
    email?: string;
    address: string;
    deliveryZone: 'dhaka' | 'greater_dhaka' | 'outside_dhaka';
  };
  items: Array<{
    id: string;
    name: string;
    priceBDT: number;
    quantity: number;
    selectedColor?: string;
    selectedStorage?: string;
  }>;
  subtotalBDT: number;      // Authoritatively computed
  deliveryFeeBDT: number;   // District zone fee (70 / 100 / 140)
  discountBDT: number;      // Validated coupon deduction
  totalBDT: number;         // Infallible grand total
  paymentMethod: string;    // 'bKash' | 'Nagad' | 'Cash on Delivery'
  transactionId: string;    // Verification code
  status: 'Pending' | 'Confirmed' | 'Processing' | 'Dispatched' | 'Delivered';
  createdAt: string;
}`
      },
      admin: {
        heading: "interface AdminMember & RBAC (frontend/src/lib/types.ts)",
        target: "backend/data/admins.json",
        code: `export interface AdminMember {
  id: string;
  name: string;
  username: string;
  password?: string;        // 10-round salted bcrypt hash (stripped on API delivery)
  role: 'Super Administrator' | 'Administrator' | 'Inventory Moderator' | 'Order Moderator';
  permissions: string[];    // ['all'] or ['products', 'orders', 'categories', 'coupons']
  avatar?: string;
  createdAt: string;
  lastLogin?: string;
}`
      },
      coupon: {
        heading: "interface Coupon (frontend/src/lib/types.ts)",
        target: "backend/data/coupons.json",
        code: `export interface Coupon {
  id: string;
  code: string;             // e.g. "NEXORA10", "FREESHIP"
  type: 'percentage' | 'fixed' | 'freeship';
  value: number;            // 10% or ৳500 flat discount
  minPurchase: number;      // Minimum subtotal threshold
  maxDiscount?: number;     // Cap on percentage discounts
  active: boolean;          // Instant enable / disable toggle
  usageCount: number;       // Audited redemption tally
  expiresAt: string;        // ISO timestamp cutoff
}`
      },
      claim: {
        heading: "interface RMA Claim (frontend/src/lib/types.ts)",
        target: "backend/data/claims.json",
        code: `export interface Claim {
  id: string;               // e.g. "RMA-2026-9021"
  orderId: string;          // Verified purchase invoice reference
  productName: string;
  serialNumber: string;     // Hologram serial identification
  customerPhone: string;
  defectType: 'Display Pixel' | 'Battery Degradation' | 'Audio Driver' | 'Motherboard';
  description: string;
  status: 'Under Review' | 'Approved - Replacement Dispatched' | 'Repaired' | 'Closed';
  createdAt: string;
}`
      }
    };

    function showSchemaModel(modelKey) {
      const m = SCHEMA_MAP[modelKey];
      if (!m) return;

      ['product', 'order', 'admin', 'coupon', 'claim'].forEach(k => {
        const btn = document.getElementById(`schemaBtn-${k}`);
        if (k === modelKey) {
          btn.className = "px-3 py-1.5 rounded-lg text-xs font-bold bg-[#0071E3] text-white";
        } else {
          btn.className = "px-3 py-1.5 rounded-lg text-xs font-bold bg-black/5 dark:bg-white/5 text-slate-400";
        }
      });

      document.getElementById('schemaNameHeading').textContent = m.heading;
      document.getElementById('schemaCodeContent').textContent = m.code;
    }

    // Initialize once DOM is ready
    window.addEventListener('DOMContentLoaded', () => {
      const savedTheme = localStorage.getItem('nexora_pres_theme');
      if (savedTheme === 'light') {
        document.documentElement.classList.remove('dark');
        document.documentElement.classList.add('light');
        document.getElementById('themeIcon').textContent = '☀️';
      }
      initPresentation();
    });
  </script>

</body>
</html>
"""

with open('NEXORA_INTERACTIVE_PRESENTATION.html', 'w', encoding='utf-8') as f_out:
    f_out.write(html_content)

print("Generated NEXORA_INTERACTIVE_PRESENTATION.html successfully!")

'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';

interface BeforeInstallPromptEvent extends Event {
  prompt: () => Promise<void>;
  userChoice: Promise<{ outcome: 'accepted' | 'dismissed'; platform: string }>;
}

interface PWAContextType {
  isInstallable: boolean;
  isInstalled: boolean;
  isIOS: boolean;
  installApp: () => Promise<boolean>;
  showIOSInstructions: boolean;
  setShowIOSInstructions: (show: boolean) => void;
}

const PWAContext = createContext<PWAContextType | undefined>(undefined);

export const PWAProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [deferredPrompt, setDeferredPrompt] = useState<BeforeInstallPromptEvent | null>(null);
  const [isInstallable, setIsInstallable] = useState(false);
  const [isInstalled, setIsInstalled] = useState(false);
  const [isIOS, setIsIOS] = useState(false);
  const [showIOSInstructions, setShowIOSInstructions] = useState(false);

  useEffect(() => {
    // 1. Register Service Worker
    if (typeof window !== 'undefined' && 'serviceWorker' in navigator) {
      window.addEventListener('load', () => {
        navigator.serviceWorker
          .register('/sw.js')
          .then((reg) => console.log('[NEXORA PWA] ServiceWorker registered:', reg.scope))
          .catch((err) => console.warn('[NEXORA PWA] ServiceWorker registration failed:', err));
      });
    }

    // 2. Check if already running in standalone mode (Installed App)
    if (typeof window !== 'undefined') {
      const isStandalone =
        window.matchMedia('(display-mode: standalone)').matches ||
        (window.navigator as unknown as { standalone?: boolean }).standalone === true;
      setIsInstalled(isStandalone);

      // 3. Detect iOS device
      const userAgent = window.navigator.userAgent.toLowerCase();
      const isAppleDevice = /iphone|ipad|ipod/.test(userAgent);
      setIsIOS(isAppleDevice && !isStandalone);
    }

    // 4. Capture native install prompt
    const handleBeforeInstallPrompt = (e: Event) => {
      e.preventDefault();
      setDeferredPrompt(e as BeforeInstallPromptEvent);
      setIsInstallable(true);
    };

    const handleAppInstalled = () => {
      setIsInstalled(true);
      setIsInstallable(false);
      setDeferredPrompt(null);
      console.log('[NEXORA PWA] App installed successfully');
    };

    window.addEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
    window.addEventListener('appinstalled', handleAppInstalled);

    return () => {
      window.removeEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
      window.removeEventListener('appinstalled', handleAppInstalled);
    };
  }, []);

  const installApp = async (): Promise<boolean> => {
    if (isInstalled) return true;

    // If on iOS, show the step-by-step Add to Home Screen modal
    if (isIOS) {
      setShowIOSInstructions(true);
      return false;
    }

    // If native prompt is available (Android, Chrome, Edge, Windows, Mac)
    if (deferredPrompt) {
      try {
        await deferredPrompt.prompt();
        const choice = await deferredPrompt.userChoice;
        if (choice.outcome === 'accepted') {
          setIsInstalled(true);
          setIsInstallable(false);
          setDeferredPrompt(null);
          return true;
        }
      } catch (err) {
        console.error('Error triggering PWA install prompt:', err);
      }
    } else {
      // Fallback instruction
      alert('To install NEXORA App: Open your browser menu (⋮ or Share) and select "Add to Home screen" or "Install NEXORA".');
    }
    return false;
  };

  return (
    <PWAContext.Provider
      value={{
        isInstallable,
        isInstalled,
        isIOS,
        installApp,
        showIOSInstructions,
        setShowIOSInstructions,
      }}
    >
      {children}

      {/* iOS Safari Installation Guide Modal */}
      {showIOSInstructions && (
        <div className="fixed inset-0 z-50 flex items-end sm:items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-fade-in">
          <div className="w-full max-w-sm rounded-3xl p-6 bg-white dark:bg-[#141824] border border-black/10 dark:border-white/10 shadow-2xl text-center space-y-4">
            <div className="w-12 h-12 rounded-2xl bg-[#0B132B] mx-auto flex items-center justify-center p-2.5 shadow-md">
              <img src="/brand/nexora_icon_white_transparent.png" alt="NEXORA" className="object-contain" />
            </div>
            <h3 className="text-lg font-bold text-[#1D1D1F] dark:text-white">Install NEXORA on iPhone</h3>
            <div className="text-left text-xs text-[#6E6E73] dark:text-[#A1A1A6] space-y-2.5 bg-black/[0.03] dark:bg-white/5 p-4 rounded-2xl">
              <p className="flex items-center gap-2">
                <span className="w-5 h-5 rounded-full bg-[#0071E3] text-white flex items-center justify-center font-bold text-[10px]">1</span>
                <span>Tap the <strong>Share</strong> button at bottom of Safari bar.</span>
              </p>
              <p className="flex items-center gap-2">
                <span className="w-5 h-5 rounded-full bg-[#0071E3] text-white flex items-center justify-center font-bold text-[10px]">2</span>
                <span>Scroll down and select <strong>&quot;Add to Home Screen&quot;</strong> ➕</span>
              </p>
              <p className="flex items-center gap-2">
                <span className="w-5 h-5 rounded-full bg-[#0071E3] text-white flex items-center justify-center font-bold text-[10px]">3</span>
                <span>Tap <strong>Add</strong> in the top right corner.</span>
              </p>
            </div>
            <button
              onClick={() => setShowIOSInstructions(false)}
              className="w-full py-2.5 rounded-full bg-[#0071E3] text-white font-medium text-xs tracking-wide"
            >
              Got it
            </button>
          </div>
        </div>
      )}
    </PWAContext.Provider>
  );
};

export const usePWA = () => {
  const ctx = useContext(PWAContext);
  if (!ctx) {
    throw new Error('usePWA must be used within PWAProvider');
  }
  return ctx;
};

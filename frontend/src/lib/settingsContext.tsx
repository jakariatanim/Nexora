'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';

type Language = 'bn' | 'en';
type Theme = 'light' | 'dark';

interface SettingsContextType {
  language: Language;
  setLanguage: (lang: Language) => void;
  toggleLanguage: () => void;
  theme: Theme;
  setTheme: (theme: Theme) => void;
  toggleTheme: () => void;
  t: (key: string) => string;
}

const TRANSLATIONS: Record<Language, Record<string, string>> = {
  bn: {
    // Nav
    'nav.showroom': 'শোরুম',
    'nav.gadgets': 'গ্যাজেটসমূহ',
    'nav.founder': 'প্রতিষ্ঠাতার ভিশন',
    'nav.track': 'অর্ডার ট্র্যাক',
    'nav.signin': 'লগইন / সাইন-ইন',
    'nav.bag': 'ব্যাগ',
    // Hero & Mosaic
    'hero.mosaic_title': 'উপহার যা সবার পছন্দ।',
    'hero.mosaic_sub': 'এই উৎসবে আপনার পছন্দের সেরা গ্যাজেটটি বেছে নিন।',
    'hero.shop_gifts': 'উপহার কিনুন',
    'hero.iphone_title': 'iPhone 18 Pro Max',
    'hero.iphone_sub': 'টাইটানিয়াম ইউনিবডি। যুগান্তকারী A20 প্রো সিলিকন।',
    'hero.s24_title': 'Galaxy S24 Ultra',
    'hero.s24_sub': 'গ্যালাক্সি এআই এখন আপনার হাতে। ২০০ মেগাপিক্সেল ও টাইটানিয়াম।',
    'hero.learn_more': 'বিস্তারিত দেখুন',
    'hero.buy': 'কিনুন',
    'hero.view_product': 'প্রোডাক্ট দেখুন',
    // Featured
    'featured.title': 'সেরা ফ্ল্যাগশিপ কালেকশন',
    'featured.sub': 'সর্বোচ্চ পারফরম্যান্স ও প্রিমিয়াম বিল্ড কোয়ালিটির আসল গ্যাজেট।',
    'featured.more_title': 'আরও গ্যাজেট খুঁজছেন?',
    'featured.more_sub': 'আপনার পছন্দের ব্র্যান্ড বা ক্যাটাগরি অনুযায়ী আমাদের সম্পূর্ণ কালেকশন দেখুন।',
    'featured.browse_all': 'সকল গ্যাজেট ব্রাউজ করুন',
    'featured.smartphones': 'স্মার্টফোন',
    'featured.audio': 'হেডফোন ও অডিও',
    'featured.smartwatches': 'স্মার্টওয়াচ ও ব্যান্ড',
    'featured.laptops': 'ট্যাবলেট ও ল্যাপটপ',
    // Common
    'btn.add_to_cart': 'ব্যাগে যোগ করুন',
    'badge.in_stock': 'স্টকে আছে',
    'badge.out_of_stock': 'স্টক শেষ',
    'bdt': '৳',
  },
  en: {
    // Nav
    'nav.showroom': 'Showroom',
    'nav.gadgets': 'Gadgets',
    'nav.founder': "Founder's Vision",
    'nav.track': 'Track Order',
    'nav.signin': 'Sign In',
    'nav.bag': 'Bag',
    // Hero & Mosaic
    'hero.mosaic_title': "Gifts they'll love.",
    'hero.mosaic_sub': 'Find their perfect match this holiday.',
    'hero.shop_gifts': 'Shop gifts',
    'hero.iphone_title': 'iPhone 18 Pro Max',
    'hero.iphone_sub': 'Titanium Unibody. Breakthrough A20 Pro Silicon.',
    'hero.s24_title': 'Galaxy S24 Ultra',
    'hero.s24_sub': 'Galaxy AI is Here. 200MP Quad Telephoto & Titanium.',
    'hero.learn_more': 'Learn more',
    'hero.buy': 'Buy',
    'hero.view_product': 'View Product',
    // Featured
    'featured.title': 'Featured Flagships',
    'featured.sub': 'The highest-tier, in-demand devices curated for peak performance.',
    'featured.more_title': 'Looking for More Devices?',
    'featured.more_sub': 'Explore our complete interior archive filtered by your favorite brand or hardware category.',
    'featured.browse_all': 'Browse All Devices in Archive',
    'featured.smartphones': 'More Smartphones',
    'featured.audio': 'More Audio & Earbuds',
    'featured.smartwatches': 'More Smartwatches',
    'featured.laptops': 'Tablets & Laptops',
    // Common
    'btn.add_to_cart': 'Add to Bag',
    'badge.in_stock': 'In Stock',
    'badge.out_of_stock': 'Out of Stock',
    'bdt': '৳',
  }
};

const SettingsContext = createContext<SettingsContextType | undefined>(undefined);

export const SettingsProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [language, setLanguageState] = useState<Language>('en'); // Clean Apple English
  const [theme, setThemeState] = useState<Theme>('light'); // Default Light mode

  useEffect(() => {
    // Load from localStorage if present
    const savedLang = localStorage.getItem('nexora_lang') as Language;
    if (savedLang === 'bn' || savedLang === 'en') {
      setLanguageState(savedLang);
    }
    const savedTheme = localStorage.getItem('nexora_theme') as Theme;
    if (savedTheme === 'light' || savedTheme === 'dark') {
      setThemeState(savedTheme);
      applyTheme(savedTheme);
    } else {
      applyTheme('light');
    }
  }, []);

  const applyTheme = (th: Theme) => {
    const root = document.documentElement;
    if (th === 'dark') {
      root.classList.add('dark');
      root.classList.remove('light');
    } else {
      root.classList.remove('dark');
      root.classList.add('light');
    }
  };

  const setLanguage = (lang: Language) => {
    setLanguageState(lang);
    localStorage.setItem('nexora_lang', lang);
  };

  const toggleLanguage = () => {
    const next = language === 'bn' ? 'en' : 'bn';
    setLanguage(next);
  };

  const setTheme = (th: Theme) => {
    setThemeState(th);
    localStorage.setItem('nexora_theme', th);
    applyTheme(th);
  };

  const toggleTheme = () => {
    const next = theme === 'light' ? 'dark' : 'light';
    setTheme(next);
  };

  const t = (key: string): string => {
    return TRANSLATIONS[language]?.[key] || TRANSLATIONS['en']?.[key] || key;
  };

  return (
    <SettingsContext.Provider
      value={{
        language,
        setLanguage,
        toggleLanguage,
        theme,
        setTheme,
        toggleTheme,
        t,
      }}
    >
      {children}
    </SettingsContext.Provider>
  );
};

export const useSettings = () => {
  const ctx = useContext(SettingsContext);
  if (!ctx) {
    throw new Error('useSettings must be used within SettingsProvider');
  }
  return ctx;
};

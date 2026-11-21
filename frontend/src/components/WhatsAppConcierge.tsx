'use client';

import React, { useState, useRef, useEffect } from 'react';
import Link from 'next/link';
import { 
  X, 
  Send, 
  Truck, 
  ShieldCheck, 
  Package, 
  CreditCard, 
  Smartphone, 
  UserCheck, 
  ChevronRight,
  RotateCcw,
  ExternalLink
} from 'lucide-react';

interface ChatMessage {
  id: string;
  sender: 'concierge' | 'user';
  text: string;
  links?: { label: string; href: string }[];
  time: string;
}

type Lang = 'en' | 'bn';

const BRAND_GREETING = 'Hello, Welcome to the Next Era of Flagship Hardware.';

const CONTENT = {
  en: {
    title: 'NEXORA Client Support',
    subtitle: 'Dedicated Hardware Specialist • Online',
    welcome: `${BRAND_GREETING}\n\nHow can we assist your journey today? Select an inquiry below or message us directly:`,
    placeholder: 'Type your message or inquiry...',
    quickTitle: 'Common Inquiries',
    typing: 'Concierge is replying...',
    openNewTab: 'Open Standalone Support in New Tab',
    reset: 'Reset Conversation',
    close: 'Close',
    supportBtn: 'Support',
    topics: [
      {
        id: 'delivery',
        icon: Truck,
        label: '🚚 Delivery & Fees',
        question: 'What are the delivery timelines and shipping charges across Bangladesh?',
        reply: 'We offer express, insured hardware dispatch across Bangladesh:\n\n• Dhaka Metro: ৳70 (Guaranteed within 24 Hours)\n• Greater Dhaka: ৳100 (24 to 36 Hours)\n• Nationwide: ৳140 (Within 24 to 48 Hours)\n\nCash on Delivery (COD) is available nationwide—you can inspect your package upon delivery before completing payment.',
        links: [{ label: 'Browse Hardware Catalog', href: '/explore' }]
      },
      {
        id: 'track',
        icon: Package,
        label: '📦 Track Order',
        question: 'How do I track my active order in real time?',
        reply: 'Upon dispatch, you receive an automated SMS with your 5-digit Order ID (e.g. NX-94821). Simply visit our Live Satellite Order Tracker and enter your mobile number or Order ID to monitor packaging, dispatch, transit, and delivery progress.',
        links: [{ label: 'Open Live Order Tracker', href: '/track-order' }]
      },
      {
        id: 'warranty',
        icon: ShieldCheck,
        label: '🛡️ 1-Yr Warranty & RMA',
        question: 'What is the official warranty and RMA replacement coverage?',
        reply: 'Every flagship device sold by NEXORA carries:\n\n• 1-Year Official Hardware Warranty coverage\n• 7-Day Instant Replacement Guarantee (RMA)\n\nIf you encounter any manufacturing fault, submit an immediate claim via our online RMA Portal for instant inspection and replacement.',
        links: [{ label: 'Submit Warranty Claim', href: '/warranty-claim' }]
      },
      {
        id: 'payment',
        icon: CreditCard,
        label: '💳 Payment & COD',
        question: 'Which payment methods do you accept? Is COD available?',
        reply: 'We accept 100% Cash on Delivery (COD), bKash, Nagad, Visa, Mastercard, and Direct Bank Wire Transfer with zero hidden fees. 0% interest EMI options up to 36 months are also supported on major credit cards.',
        links: [{ label: 'Proceed to Secure Checkout', href: '/checkout' }]
      },
      {
        id: 'genuine',
        icon: Smartphone,
        label: '📱 100% Genuine',
        question: 'Are all devices brand new, factory sealed, and official?',
        reply: 'All devices curated by NEXORA are 100% original, brand new, and factory-sealed with intact manufacturer seals. Official IMEI and serial numbers from Apple, Samsung, Google, and Sony can be verified on official manufacturer portals.',
        links: [{ label: 'Explore Flagship Devices', href: '/explore' }]
      },
      {
        id: 'founder',
        icon: UserCheck,
        label: '👤 Founder Vision',
        question: 'How can I connect with Founder Jakaria Tanim or Head Office?',
        reply: 'NEXORA is directed by Founder & Chief Architect Jakaria Tanim. For enterprise procurement, VIP hardware concierge, or bulk inquiries, you can reach out directly via our Founder portal or executive line.',
        links: [{ label: 'Read Founder Vision', href: '/founder' }]
      }
    ]
  },
  bn: {
    title: 'নেক্সরা ক্লায়েন্ট সাপোর্ট',
    subtitle: 'ডেডিকেটেড গ্যাজেট স্পেশালিস্ট • অনলাইন',
    welcome: `${BRAND_GREETING}\n\nআজ আপনাকে কীভাবে সহযোগিতা করতে পারি? নিচের যেকোনো বিষয়ে ক্লিক করুন অথবা আপনার প্রশ্নটি লিখে জানান:`,
    placeholder: 'আপনার প্রশ্ন বা বার্তা লিখুন...',
    quickTitle: 'সাধারণ প্রশ্নসমূহ',
    typing: 'সাপোর্ট প্রতিনিধি লিখছেন...',
    openNewTab: 'নতুন ট্যাবে সাপোর্ট পেজ ওপেন করুন',
    reset: 'চ্যাট নতুন করে শুরু করুন',
    close: 'বন্ধ করুন',
    supportBtn: 'সাপোর্ট',
    topics: [
      {
        id: 'delivery',
        icon: Truck,
        label: '🚚 ডেলিভারি ও চার্জ',
        question: 'ডেলিভারি চার্জ এবং পৌঁছাতে কতদিন সময় লাগবে?',
        reply: 'NEXORA-তে আমরা সুপার-ফাস্ট হোম ডেলিভারি দিয়ে থাকি:\n\n• ঢাকা মেট্রো: ৳৭০ (২৪ ঘণ্টার মধ্যে এক্সপ্রেস ডেলিভারি)\n• গ্রেটার ঢাকা: ৳১০০ (২৪-৩৬ ঘণ্টা)\n• সারা বাংলাদেশ: ৳১৪০ (২৪-৪৮ ঘণ্টার মধ্যে নিরাপদ ডেলিভারি)\n\nক্যাশ অন ডেলিভারিতে প্রোডাক্ট হাতে পেয়ে চেক করে মূল্য পরিশোধ করতে পারবেন।',
        links: [{ label: 'ক্যাটালগ দেখুন', href: '/explore' }]
      },
      {
        id: 'track',
        icon: Package,
        label: '📦 অর্ডার ট্র্যাক',
        question: 'আমার অর্ডারটি এখন কোথায় আছে কীভাবে জানব?',
        reply: 'অর্ডার করার পর আপনাকে ৫ ডিজিটের একটি ট্র্যাকিং কোড (যেমন: NX-94821) এসএমএস দেওয়া হয়। আমাদের লাইভ ট্র্যাকিং পেজে গিয়ে আপনার ফোন নম্বর বা ট্র্যাকিং কোড দিলেই অর্ডারের বর্তমান অবস্থা লাইভ দেখতে পাবেন।',
        links: [{ label: 'লাইভ অর্ডার ট্র্যাকার', href: '/track-order' }]
      },
      {
        id: 'warranty',
        icon: ShieldCheck,
        label: '🛡️ ১ বছরের ওয়্যারেন্টি',
        question: 'প্রোডাক্টের ওয়ারেন্টি পলিসি এবং নষ্ট হলে কী সুবিধা পাব?',
        reply: 'NEXORA-র প্রতিটি গ্যাজেটে পাবেন:\n\n• ১ বছরের অফিশিয়াল হার্ডওয়্যার ওয়ারেন্টি\n• ৭ দিনের ইনস্ট্যান্ট রিপ্লেসমেন্ট গ্যারান্টি (RMA)\n\nকোনো সমস্যা হলে সরাসরি আমাদের অনলাইন RMA পোর্টালে ক্লেইম সাবমিট করতে পারবেন।',
        links: [{ label: 'ওয়ারেন্টি ক্লেইম পোর্টাল', href: '/warranty-claim' }]
      },
      {
        id: 'payment',
        icon: CreditCard,
        label: '💳 পেমেন্ট ও ক্যাশ অন ডেলিভারি',
        question: 'পেমেন্ট মেথড কী কী আছে? ক্যাশ অন ডেলিভারি হবে?',
        reply: 'হ্যাঁ, ১০০% ক্যাশ অন ডেলিভারি সুবিধা রয়েছে! এছাড়া বিকাশ (bKash), নগদ (Nagad), ভিসা/মাস্টারকার্ড ও ব্যাংক ট্রান্সফারে কোনো অতিরিক্ত ফি ছাড়াই পেমেন্ট করতে পারবেন।',
        links: [{ label: 'চেকআউট পেজ', href: '/checkout' }]
      },
      {
        id: 'genuine',
        icon: Smartphone,
        label: '📱 ১০০% আসল গ্যারান্টি',
        question: 'গ্যাজেটগুলো কি আসল ও ইনট্যাক্ট বক্স?',
        reply: 'NEXORA-র প্রতিটি প্রোডাক্ট ১০০% আসল, আন-অ্যাক্টিভেটেড ও ইনট্যাক্ট ফ্যাক্টরি সিল প্যাকড। বক্সের আইএমইআই (IMEI) ও সিরিয়াল নম্বর দিয়ে সরাসরি যাচাই করে নিতে পারবেন।',
        links: [{ label: 'প্রোডাক্ট কালেকশন', href: '/explore' }]
      },
      {
        id: 'founder',
        icon: UserCheck,
        label: '👤 ফাউন্ডার তানিম',
        question: 'প্রতিষ্ঠাতা জাকারিয়া তানিম বা হেড অফিসে কীভাবে কথা বলব?',
        reply: 'NEXORA পরিচালিত হচ্ছে ফাউন্ডার ও চিফ আর্কিটেক্ট জাকারিয়া তানিম (Jakaria Tanim)-এর সরাসরি তত্ত্বাবধানে। যেকোনো প্রয়োজনে সরাসরি তার সাথে যোগাযোগ করতে পারেন।',
        links: [{ label: 'ফাউন্ডার পেজ', href: '/founder' }]
      }
    ]
  }
};

export const WhatsAppConcierge: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [lang, setLang] = useState<Lang>('en');
  const [inputText, setInputText] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [showInquiries, setShowInquiries] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const chatContainerRef = useRef<HTMLDivElement>(null);

  const t = CONTENT[lang];

  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 'welcome',
      sender: 'concierge',
      text: CONTENT.en.welcome,
      time: 'Just now'
    }
  ]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    if (isOpen) {
      scrollToBottom();
    }
  }, [messages, isOpen, isTyping]);

  const handleOpenInNewTab = () => {
    // Opens the dedicated support page in a new browser tab
    window.open('/support', '_blank');
  };

  const handleToggleLang = (newLang: Lang) => {
    setLang(newLang);
    setMessages([
      {
        id: `welcome-${Date.now()}`,
        sender: 'concierge',
        text: CONTENT[newLang].welcome,
        time: 'Just now'
      }
    ]);
    setShowInquiries(true);
  };

  const handleTopicClick = (topic: typeof CONTENT['en']['topics'][0]) => {
    const userMsg: ChatMessage = {
      id: `user-${Date.now()}`,
      sender: 'user',
      text: topic.question,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages(prev => [...prev, userMsg]);
    setIsTyping(true);
    // Collapse inquiries list so the reply takes full focus and is completely visible!
    setShowInquiries(false);

    setTimeout(() => {
      const conciergeMsg: ChatMessage = {
        id: `concierge-${Date.now()}`,
        sender: 'concierge',
        text: topic.reply,
        links: topic.links,
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setMessages(prev => [...prev, conciergeMsg]);
      setIsTyping(false);
    }, 450);
  };

  const handleSendCustomMessage = (e: React.FormEvent) => {
    e.preventDefault();
    const query = inputText.trim();
    if (!query) return;

    const userMsg: ChatMessage = {
      id: `user-${Date.now()}`,
      sender: 'user',
      text: query,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages(prev => [...prev, userMsg]);
    setInputText('');
    setIsTyping(true);
    setShowInquiries(false);

    setTimeout(() => {
      const q = query.toLowerCase();
      let replyText = '';
      let replyLinks: { label: string; href: string }[] | undefined = undefined;

      if (q.includes('track') || q.includes('order') || q.includes('status') || q.includes('ট্র্যাক')) {
        replyText = lang === 'en'
          ? 'You can monitor your order dispatch and transit live on our satellite tracking portal using your Order ID or phone number.'
          : 'আপনার অর্ডারের বর্তমান অবস্থা লাইভ ট্র্যাক করতে আমাদের অর্ডার ট্র্যাকার ব্যবহার করুন।';
        replyLinks = [{ label: lang === 'en' ? 'Track Order Live' : 'অর্ডার ট্র্যাক করুন', href: '/track-order' }];
      } else if (q.includes('deliver') || q.includes('shipping') || q.includes('fee') || q.includes('charge') || q.includes('ডেলিভারি')) {
        replyText = lang === 'en'
          ? 'We dispatch across Bangladesh:\n• Dhaka Metro: ৳70 (Within 24 Hours)\n• Greater Dhaka: ৳100\n• Nationwide: ৳140 (24-48 Hours)\n\nCash on delivery is fully supported.'
          : 'ডেলিভারি চার্জ: ঢাকা মেট্রো ৭০৳ (২৪ ঘণ্টা), গ্রেটার ঢাকা ১০০৳, সারা বাংলাদেশ ১৪০৳ (২৪-৪৮ ঘণ্টা)।';
        replyLinks = [{ label: lang === 'en' ? 'Explore Devices' : 'ক্যাটালগ দেখুন', href: '/explore' }];
      } else if (q.includes('warrant') || q.includes('guarantee') || q.includes('rma') || q.includes('replace') || q.includes('ওয়ারেন্টি')) {
        replyText = lang === 'en'
          ? 'All hardware comes with a 1-Year Official Warranty and 7-Day Instant Replacement Guarantee (RMA).'
          : 'প্রতিটি গ্যাজেটে পাবেন ১ বছরের অফিসিয়াল ওয়্যারেন্টি এবং ৭ দিনের রিপ্লেসমেন্ট সুবিধা।';
        replyLinks = [{ label: lang === 'en' ? 'Warranty Portal' : 'ওয়ারেন্টি পোর্টাল', href: '/warranty-claim' }];
      } else if (q.includes('pay') || q.includes('cod') || q.includes('bkash') || q.includes('card') || q.includes('পেমেন্ট')) {
        replyText = lang === 'en'
          ? 'We accept Cash on Delivery (COD), bKash, Nagad, Visa, Mastercard, and Bank Wire Transfer with zero extra fees.'
          : 'আমরা ক্যাশ অন ডেলিভারি (COD), বিকাশ, নগদ ও কার্ড পেমেন্ট গ্রহণ করি।';
        replyLinks = [{ label: lang === 'en' ? 'Checkout' : 'চেকআউট', href: '/checkout' }];
      } else if (q.includes('authentic') || q.includes('original') || q.includes('genuine') || q.includes('seal') || q.includes('আসল')) {
        replyText = lang === 'en'
          ? 'All flagship hardware is 100% brand new, authentic, and factory-sealed with verified serial and IMEI numbers.'
          : 'নেক্সরার সকল প্রোডাক্ট ১০০% আসল, আন-অ্যাক্টিভেটেড এবং ইনট্যাক্ট সিল প্যাকড।';
      } else if (q.includes('tanim') || q.includes('founder') || q.includes('owner') || q.includes('তানিম')) {
        replyText = lang === 'en'
          ? 'NEXORA is founded and directed by Jakaria Tanim. You can review the founder architectural vision or connect directly.'
          : 'NEXORA পরিচালিত হচ্ছে ফাউন্ডার জাকারিয়া তানিমের সরাসরি তত্ত্বাবধানে।';
        replyLinks = [{ label: lang === 'en' ? 'Founder Vision' : 'ফাউন্ডার পেজ', href: '/founder' }];
      } else {
        replyText = lang === 'en'
          ? 'Thank you for your message! Our specialist concierge team is at your disposal. You can also chat directly on our executive WhatsApp hotline (+880 1640-026177) for instant assistance.'
          : 'আপনার বার্তার জন্য ধন্যবাদ! সরাসরি আমাদের প্রতিনিধির সাথে কথা বলতে হোয়াটসঅ্যাপে (+880 1640-026177) যোগাযোগ করতে পারেন।';
      }

      const conciergeMsg: ChatMessage = {
        id: `concierge-${Date.now()}`,
        sender: 'concierge',
        text: replyText,
        links: replyLinks,
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };

      setMessages(prev => [...prev, conciergeMsg]);
      setIsTyping(false);
    }, 450);
  };

  const handleReset = () => {
    setMessages([
      {
        id: `welcome-reset-${Date.now()}`,
        sender: 'concierge',
        text: t.welcome,
        time: 'Just now'
      }
    ]);
    setShowInquiries(true);
  };

  return (
    <div className="fixed bottom-20 md:bottom-6 right-4 md:right-6 z-40 flex flex-col items-end print:hidden">
      
      {/* Expanded Support Window (Prevents outer page scroll hijacking with data-lenis-prevent and overscroll-contain) */}
      {isOpen && (
        <div 
          ref={chatContainerRef}
          data-lenis-prevent="true"
          data-lenis-prevent-wheel="true"
          onWheel={(e) => e.stopPropagation()}
          className="mb-3 w-[92vw] sm:w-[390px] max-h-[600px] h-[520px] rounded-3xl bg-white dark:bg-[#070B18] border border-black/10 dark:border-white/20 shadow-[0_20px_60px_rgba(11,19,43,0.35)] overflow-hidden flex flex-col animate-fade-in text-left overscroll-contain"
        >
          {/* Header - Styled to match the Title Bar (#0B132B) */}
          <div className="px-5 py-3.5 bg-[#0B132B] dark:bg-[#070B18] text-white flex items-center justify-between border-b border-white/15">
            <div className="flex items-center gap-2.5">
              <span className="relative flex h-2.5 w-2.5 flex-shrink-0">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-400"></span>
              </span>
              <div>
                <h3 className="text-xs font-bold tracking-tight text-white">{t.title}</h3>
                <p className="text-[10px] text-white/70 font-medium">
                  {t.subtitle}
                </p>
              </div>
            </div>

            {/* Header Action Controls */}
            <div className="flex items-center gap-1.5">
              {/* Language Switcher Pill */}
              <div className="flex items-center bg-white/10 rounded-full p-0.5 border border-white/10 text-[10px] font-bold">
                <button
                  type="button"
                  onClick={() => handleToggleLang('en')}
                  className={`px-2 py-0.5 rounded-full transition-colors ${
                    lang === 'en' ? 'bg-white text-[#0B132B] shadow-xs' : 'text-white/80 hover:text-white'
                  }`}
                >
                  EN
                </button>
                <button
                  type="button"
                  onClick={() => handleToggleLang('bn')}
                  className={`px-2 py-0.5 rounded-full transition-colors ${
                    lang === 'bn' ? 'bg-white text-[#0B132B] shadow-xs' : 'text-white/80 hover:text-white'
                  }`}
                >
                  বাং
                </button>
              </div>

              {/* Open Standalone Page in New Tab Button */}
              <button
                type="button"
                onClick={handleOpenInNewTab}
                title={t.openNewTab}
                className="p-1.5 rounded-full text-white/80 hover:text-white hover:bg-white/10 transition-colors"
              >
                <ExternalLink className="w-4 h-4" />
              </button>

              {/* Reset Conversation Button */}
              <button
                type="button"
                onClick={handleReset}
                title={t.reset}
                className="p-1.5 rounded-full text-white/80 hover:text-white hover:bg-white/10 transition-colors"
              >
                <RotateCcw className="w-3.5 h-3.5" />
              </button>

              {/* Close Button */}
              <button
                type="button"
                onClick={() => setIsOpen(false)}
                title={t.close}
                className="p-1.5 rounded-full text-white/80 hover:text-white hover:bg-white/10 transition-colors"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* Chat Message Scroll Area - Strict Isolated Scroll */}
          <div 
            data-lenis-prevent="true"
            data-lenis-prevent-wheel="true"
            onWheel={(e) => e.stopPropagation()}
            className="flex-1 p-4 overflow-y-auto space-y-3.5 text-xs bg-slate-50/70 dark:bg-[#0A0E1A] overscroll-contain select-text"
          >
            {messages.map((m) => (
              <div
                key={m.id}
                className={`flex flex-col ${m.sender === 'user' ? 'items-end' : 'items-start'}`}
              >
                <div
                  className={`max-w-[85%] rounded-2xl p-3.5 shadow-xs leading-relaxed ${
                    m.sender === 'user'
                      ? 'bg-[#0B132B] dark:bg-[#0071E3] text-white rounded-br-xs'
                      : 'bg-white dark:bg-[#151D30] text-[#1D1D1F] dark:text-slate-100 border border-black/5 dark:border-white/10 rounded-bl-xs whitespace-pre-line'
                  }`}
                >
                  {m.text}

                  {/* Attached Direct Links */}
                  {m.links && m.links.length > 0 && (
                    <div className="mt-2.5 pt-2 border-t border-black/10 dark:border-white/10 space-y-1.5">
                      {m.links.map((link, idx) => (
                        <Link
                          key={idx}
                          href={link.href}
                          onClick={() => setIsOpen(false)}
                          className="inline-flex items-center gap-1.5 text-[11px] font-bold text-[#0071E3] dark:text-[#38BDF8] hover:underline bg-[#0071E3]/10 dark:bg-white/10 px-2.5 py-1 rounded-xl transition-colors"
                        >
                          <span>{link.label}</span>
                          <ChevronRight className="w-3 h-3" />
                        </Link>
                      ))}
                    </div>
                  )}
                </div>
                <span className="text-[9px] text-slate-400 mt-1 px-1 font-mono">
                  {m.time}
                </span>
              </div>
            ))}

            {/* Typing Indicator */}
            {isTyping && (
              <div className="flex items-center gap-1.5 text-slate-400 text-xs py-1">
                <span className="w-2 h-2 rounded-full bg-[#0071E3] animate-bounce" style={{ animationDelay: '0ms' }} />
                <span className="w-2 h-2 rounded-full bg-[#0071E3] animate-bounce" style={{ animationDelay: '150ms' }} />
                <span className="w-2 h-2 rounded-full bg-[#0071E3] animate-bounce" style={{ animationDelay: '300ms' }} />
                <span className="text-[10px] text-slate-500 ml-1 font-medium">{t.typing}</span>
              </div>
            )}

            {/* Compact Quick Topic Chips (2 to 3 per line) with Toggle */}
            <div className="pt-2">
              <div className="flex items-center justify-between pb-1.5 px-0.5">
                <span className="text-[10px] font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider">
                  {t.quickTitle}
                </span>
                <button
                  type="button"
                  onClick={() => setShowInquiries(!showInquiries)}
                  className="text-[10px] font-semibold text-[#0071E3] hover:underline"
                >
                  {showInquiries ? (lang === 'en' ? 'Hide ▲' : 'লুকান ▲') : (lang === 'en' ? 'Show (6) ▼' : 'দেখুন (৬) ▼')}
                </button>
              </div>

              {showInquiries && (
                <div className="flex flex-wrap gap-1.5 animate-fadeIn">
                  {t.topics.map((topic) => (
                    <button
                      key={topic.id}
                      type="button"
                      onClick={() => handleTopicClick(topic)}
                      className="text-left text-[11px] font-medium px-2.5 py-1.5 rounded-xl bg-white dark:bg-[#151D30] border border-black/10 dark:border-white/10 hover:border-[#0071E3] dark:hover:border-[#38BDF8] text-[#1D1D1F] dark:text-slate-200 hover:text-[#0071E3] dark:hover:text-[#38BDF8] transition-all shadow-xs active:scale-95 flex items-center gap-1"
                    >
                      <span>{topic.label}</span>
                    </button>
                  ))}
                </div>
              )}
            </div>

            <div ref={messagesEndRef} />
          </div>

          {/* Chat Input Bar */}
          <form
            onSubmit={handleSendCustomMessage}
            className="p-3 bg-white dark:bg-[#070B18] border-t border-black/10 dark:border-white/10 flex items-center gap-2"
          >
            <input
              type="text"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder={t.placeholder}
              className="flex-1 px-3.5 py-2.5 rounded-xl bg-slate-100 dark:bg-white/5 border border-black/5 dark:border-white/10 text-xs text-[#1D1D1F] dark:text-white placeholder-slate-400 focus:outline-none focus:border-[#0071E3]"
            />
            <button
              type="submit"
              disabled={!inputText.trim() || isTyping}
              className="p-2.5 rounded-xl bg-[#0B132B] dark:bg-[#0071E3] hover:bg-[#151D30] text-white disabled:opacity-40 transition-colors shadow-sm flex items-center justify-center flex-shrink-0"
              aria-label="Send"
            >
              <Send className="w-4 h-4" />
            </button>
          </form>
        </div>
      )}

      {/* Floating Trigger Button - Matches Title Bar Capsule (#0B132B) */}
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        className="group relative flex items-center gap-2 px-4 py-2.5 rounded-full bg-[#0B132B] dark:bg-[#070B18] hover:bg-[#151D30] text-white border border-white/20 shadow-[0_8px_32px_rgba(11,19,43,0.45)] transition-all duration-300 active:scale-95"
        title="Support"
        aria-label="Support"
      >
        <span className="relative flex h-2.5 w-2.5 flex-shrink-0">
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
          <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-400"></span>
        </span>
        <span className="text-xs font-semibold tracking-wide">
          {isOpen ? (lang === 'bn' ? 'বন্ধ করুন' : 'Close') : (lang === 'bn' ? 'সাপোর্ট' : 'Support')}
        </span>
      </button>

    </div>
  );
};

'use client';

import React, { useState, useRef, useEffect } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { 
  Send, 
  Truck, 
  ShieldCheck, 
  Package, 
  CreditCard, 
  Smartphone, 
  UserCheck, 
  RotateCcw,
  ExternalLink,
  ChevronRight,
  Headphones,
  CheckCircle2,
  ArrowLeft
} from 'lucide-react';
import { getConciergeAIResponse } from '@/lib/conciergeAI';

interface ChatMessage {
  id: string;
  sender: 'concierge' | 'user';
  text: string;
  links?: { label: string; href: string }[];
  time: string;
}

type Lang = 'en' | 'bn';

const TOPICS = {
  en: [
    {
      id: 'delivery',
      icon: Truck,
      label: '🚚 Delivery & Fees',
      question: 'What are the delivery timelines and shipping charges across Bangladesh?',
      reply: 'We offer insured express hardware dispatch across Bangladesh:\n\n• Dhaka Metro: ৳70 (Within 24 Hours)\n• Greater Dhaka: ৳100 (24 to 36 Hours)\n• Nationwide: ৳140 (24 to 48 Hours)\n\nCash on Delivery (COD) is available nationwide—inspect your package upon delivery before completing payment.',
      links: [{ label: 'Explore Hardware Catalog', href: '/explore' }]
    },
    {
      id: 'track',
      icon: Package,
      label: '📦 Track Order',
      question: 'How do I track my active order in real time?',
      reply: 'Upon dispatch, you receive an automated SMS with your 5-digit Order ID (e.g. NX-94821). Simply visit our Live Satellite Order Tracker and enter your mobile number or Order ID to monitor packaging, dispatch, and delivery progress.',
      links: [{ label: 'Open Live Order Tracker', href: '/track-order' }]
    },
    {
      id: 'warranty',
      icon: ShieldCheck,
      label: '🛡️ 1-Yr Warranty & RMA',
      question: 'What is the official warranty and RMA replacement coverage?',
      reply: 'Every flagship device sold by NEXORA carries:\n\n• 1-Year Official Hardware Warranty coverage\n• 7-Day Instant Replacement Guarantee (RMA)\n\nSubmit an immediate claim via our online RMA Portal for swift inspection and device replacement.',
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
      label: '📱 100% Genuine Guarantee',
      question: 'Are all devices brand new, factory sealed, and official?',
      reply: 'All devices curated by NEXORA are 100% original, brand new, and factory-sealed with intact manufacturer seals. Official IMEI and serial numbers from Apple, Samsung, Google, and Sony can be verified on official portals.',
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
  ],
  bn: [
    {
      id: 'delivery',
      icon: Truck,
      label: '🚚 ডেলিভারি ও চার্জ',
      question: 'ডেলিভারি চার্জ এবং পৌঁছাতে কতদিন সময় লাগবে?',
      reply: 'NEXORA-তে আমরা সুপার-ফাস্ট হোম ডেলিভারি দিয়ে থাকি:\n\n• ঢাকা মেট্রো: ৳৭০ (২৪ ঘণ্টার মধ্যে)\n• গ্রেটার ঢাকা: ৳১০০ (২৪-৩৬ ঘণ্টা)\n• সারা বাংলাদেশ: ৳১৪০ (২৪-৪৮ ঘণ্টার মধ্যে)\n\nক্যাশ অন ডেলিভারিতে প্রোডাক্ট হাতে পেয়ে চেক করে মূল্য পরিশোধ করতে পারবেন।',
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
};

export default function DedicatedSupportPage() {
  const [lang, setLang] = useState<Lang>('en');
  const [inputText, setInputText] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [showInquiries, setShowInquiries] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const latestReplyRef = useRef<HTMLDivElement>(null);

  const greeting = lang === 'en'
    ? 'Hello, Welcome to the Next Era of Flagship Hardware.\n\nHow can we assist your journey today? Select an inquiry below or message us directly:'
    : 'Hello, Welcome to the Next Era of Flagship Hardware.\n\nআজ আপনাকে কীভাবে সহযোগিতা করতে পারি? নিচের যেকোনো বিষয়ে ক্লিক করুন অথবা আপনার প্রশ্নটি লিখে জানান:';

  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 'welcome',
      sender: 'concierge',
      text: greeting,
      time: 'Just now'
    }
  ]);

  const currentTopics = TOPICS[lang];

  useEffect(() => {
    latestReplyRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }, [messages, isTyping]);

  const handleToggleLang = (newLang: Lang) => {
    setLang(newLang);
    const newGreeting = newLang === 'en'
      ? 'Hello, Welcome to the Next Era of Flagship Hardware.\n\nHow can we assist your journey today? Select an inquiry below or message us directly:'
      : 'Hello, Welcome to the Next Era of Flagship Hardware.\n\nআজ আপনাকে কীভাবে সহযোগিতা করতে পারি? নিচের যেকোনো বিষয়ে ক্লিক করুন অথবা আপনার প্রশ্নটি লিখে জানান:';
    
    setMessages([
      {
        id: `welcome-${Date.now()}`,
        sender: 'concierge',
        text: newGreeting,
        time: 'Just now'
      }
    ]);
    setShowInquiries(true);
  };

  const handleTopicClick = (topic: typeof TOPICS['en'][0]) => {
    const userMsg: ChatMessage = {
      id: `user-${Date.now()}`,
      sender: 'user',
      text: topic.question,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages(prev => [...prev, userMsg]);
    setIsTyping(true);
    setShowInquiries(false); // Auto collapse so reply is front and center

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
      const response = getConciergeAIResponse(query, lang);

      const conciergeMsg: ChatMessage = {
        id: `concierge-${Date.now()}`,
        sender: 'concierge',
        text: response.text,
        links: response.links,
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };

      setMessages(prev => [...prev, conciergeMsg]);
      setIsTyping(false);
    }, 450);
  };

  return (
    <div className="min-h-screen bg-[#F5F5F7] dark:bg-[#070B18] flex flex-col justify-between py-6 px-4 sm:px-6">
      <div className="max-w-4xl w-full mx-auto flex-1 flex flex-col bg-white dark:bg-[#0B132B] rounded-3xl border border-black/10 dark:border-white/15 shadow-2xl overflow-hidden">
        
        {/* Top Header */}
        <div className="px-6 py-4 bg-[#0B132B] text-white flex items-center justify-between border-b border-white/10">
          <div className="flex items-center gap-3">
            <Link href="/" className="p-2 rounded-xl bg-white/10 hover:bg-white/20 text-white transition-colors" title="Back to Store">
              <ArrowLeft className="w-5 h-5" />
            </Link>
            <div className="flex items-center gap-2">
              <span className="relative flex h-2.5 w-2.5">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-400"></span>
              </span>
              <div>
                <h1 className="text-base font-bold tracking-tight">NEXORA Dedicated Client Support</h1>
                <p className="text-xs text-white/70">Flagship Hardware Concierge • Step into the Next Era</p>
              </div>
            </div>
          </div>

          {/* Controls */}
          <div className="flex items-center gap-2">
            <div className="flex items-center bg-white/10 rounded-full p-0.5 border border-white/10 text-xs font-bold">
              <button
                type="button"
                onClick={() => handleToggleLang('en')}
                className={`px-3 py-1 rounded-full transition-colors ${
                  lang === 'en' ? 'bg-white text-[#0B132B] shadow-xs' : 'text-white/80 hover:text-white'
                }`}
              >
                EN
              </button>
              <button
                type="button"
                onClick={() => handleToggleLang('bn')}
                className={`px-3 py-1 rounded-full transition-colors ${
                  lang === 'bn' ? 'bg-white text-[#0B132B] shadow-xs' : 'text-white/80 hover:text-white'
                }`}
              >
                বাংলা
              </button>
            </div>

            <button
              type="button"
              onClick={() => {
                setMessages([{ id: 'welcome-reset', sender: 'concierge', text: greeting, time: 'Just now' }]);
                setShowInquiries(true);
              }}
              title="Reset"
              className="p-2 rounded-full bg-white/10 hover:bg-white/20 text-white transition-colors"
            >
              <RotateCcw className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Chat Messages */}
        <div className="flex-1 p-6 overflow-y-auto space-y-4 bg-slate-50/50 dark:bg-[#070B18]/60 text-sm">
          {messages.map((m, idx) => {
            const isLatest = idx === messages.length - 1;
            return (
              <div
                key={m.id}
                ref={isLatest ? latestReplyRef : null}
                className={`flex flex-col ${m.sender === 'user' ? 'items-end' : 'items-start'}`}
              >
                <div
                  className={`max-w-[80%] rounded-2xl p-4 shadow-xs leading-relaxed ${
                    m.sender === 'user'
                      ? 'bg-[#0B132B] dark:bg-[#0071E3] text-white rounded-br-xs'
                      : 'bg-white dark:bg-[#151D30] text-[#1D1D1F] dark:text-slate-100 border border-black/5 dark:border-white/10 rounded-bl-xs whitespace-pre-line'
                  }`}
                >
                  {m.text}

                  {m.links && m.links.length > 0 && (
                    <div className="mt-3 pt-2.5 border-t border-black/10 dark:border-white/10 flex flex-wrap gap-2">
                      {m.links.map((link, lIdx) => (
                        <Link
                          key={lIdx}
                          href={link.href}
                          className="inline-flex items-center gap-1.5 text-xs font-bold text-[#0071E3] dark:text-[#38BDF8] hover:underline bg-[#0071E3]/10 dark:bg-white/10 px-3 py-1.5 rounded-xl transition-colors"
                        >
                          <span>{link.label}</span>
                          <ChevronRight className="w-3.5 h-3.5" />
                        </Link>
                      ))}
                    </div>
                  )}
                </div>
                <span className="text-[10px] text-slate-400 mt-1 px-1 font-mono">
                  {m.time}
                </span>
              </div>
            );
          })}

          {isTyping && (
            <div className="flex items-center gap-2 text-slate-400 text-xs py-2">
              <span className="w-2.5 h-2.5 rounded-full bg-[#0071E3] animate-bounce" style={{ animationDelay: '0ms' }} />
              <span className="w-2.5 h-2.5 rounded-full bg-[#0071E3] animate-bounce" style={{ animationDelay: '150ms' }} />
              <span className="w-2.5 h-2.5 rounded-full bg-[#0071E3] animate-bounce" style={{ animationDelay: '300ms' }} />
              <span className="text-xs text-slate-500 font-medium">{lang === 'en' ? 'Concierge is typing...' : 'সাপোর্ট প্রতিনিধি লিখছেন...'}</span>
            </div>
          )}

          {/* Compact Inquiry Chips (2 to 3 per line) */}
          <div className="pt-2">
            <div className="flex items-center justify-between pb-2">
              <span className="text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider">
                {lang === 'en' ? 'Quick Topics' : 'কুইক টপিকসমূহ'}:
              </span>
              <button
                type="button"
                onClick={() => setShowInquiries(!showInquiries)}
                className="text-xs font-semibold text-[#0071E3] hover:underline"
              >
                {showInquiries ? (lang === 'en' ? 'Hide Topics ▲' : 'টপিক লুকান ▲') : (lang === 'en' ? 'Show Topics ▼' : 'টপিক দেখুন ▼')}
              </button>
            </div>

            {showInquiries && (
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
                {currentTopics.map((topic) => (
                  <button
                    key={topic.id}
                    type="button"
                    onClick={() => handleTopicClick(topic)}
                    className="p-2.5 rounded-xl bg-white dark:bg-[#151D30] border border-black/10 dark:border-white/10 hover:border-[#0071E3] text-[#1D1D1F] dark:text-slate-200 hover:text-[#0071E3] transition-all text-xs font-medium text-left flex items-center justify-between shadow-xs group"
                  >
                    <span className="truncate">{topic.label}</span>
                    <ChevronRight className="w-3.5 h-3.5 text-slate-400 group-hover:text-[#0071E3] flex-shrink-0" />
                  </button>
                ))}
              </div>
            )}
          </div>

          <div ref={messagesEndRef} />
        </div>

        {/* Bottom Input */}
        <form onSubmit={handleSendCustomMessage} className="p-4 bg-white dark:bg-[#0B132B] border-t border-black/10 dark:border-white/10 flex items-center gap-3">
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder={lang === 'en' ? 'Type your inquiry here...' : 'আপনার প্রশ্নটি এখানে লিখুন...'}
            className="flex-1 px-4 py-3 rounded-2xl bg-slate-100 dark:bg-white/5 border border-black/10 dark:border-white/10 text-sm text-[#1D1D1F] dark:text-white focus:outline-none focus:border-[#0071E3]"
          />
          <button
            type="submit"
            disabled={!inputText.trim() || isTyping}
            className="px-5 py-3 rounded-2xl bg-[#0071E3] hover:bg-[#0077ED] text-white font-semibold text-sm disabled:opacity-40 transition-colors shadow-md flex items-center gap-2"
          >
            <span>{lang === 'en' ? 'Send' : 'পাঠান'}</span>
            <Send className="w-4 h-4" />
          </button>
        </form>

      </div>
    </div>
  );
}

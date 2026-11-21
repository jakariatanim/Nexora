'use client';

import React, { useState, useRef, useEffect } from 'react';
import Link from 'next/link';
import { 
  Bot, 
  MessageCircle, 
  X, 
  Send, 
  Sparkles, 
  Truck, 
  ShieldCheck, 
  Package, 
  CreditCard, 
  Smartphone, 
  UserCheck, 
  ExternalLink,
  ChevronRight,
  RotateCcw,
  Headphones
} from 'lucide-react';

interface ChatMessage {
  id: string;
  sender: 'bot' | 'user';
  text: string;
  links?: { label: string; href: string }[];
  time: string;
}

const QUICK_TOPICS = [
  {
    id: 'delivery',
    icon: Truck,
    label: '🚚 ডেলিভারি চার্জ ও সময় কত?',
    question: 'ডেলিভারি চার্জ এবং পৌঁছাতে কতদিন সময় লাগবে?',
    reply: 'NEXORA-তে আমরা সুপার-ফাস্ট হোম ডেলিভারি দিয়ে থাকি:\n\n• ঢাকা মেট্রো: ৳৭০ (২৪ ঘণ্টার মধ্যে এক্সপ্রেস ডেলিভারি)\n• গ্রেটার ঢাকা: ৳১০০ (২৪-৩৬ ঘণ্টা)\n• সারা বাংলাদেশ: ৳১৪০ (৪৮ ঘণ্টার মধ্যে নিরাপদ ডেলিভারি)\n\nক্যাশ অন ডেলিভারিতে প্রোডাক্ট হাতে পেয়ে চেক করে মূল্য পরিশোধ করতে পারবেন।',
    links: [{ label: 'ক্যাটালগ দেখুন', href: '/explore' }]
  },
  {
    id: 'track',
    icon: Package,
    label: '📦 অর্ডার ট্র্যাক করব কীভাবে?',
    question: 'আমার অর্ডারটি এখন কোথায় আছে কীভাবে জানব?',
    reply: 'অর্ডার করার পর আপনাকে ৫ ডিজিটের একটি ট্র্যাকিং কোড (যেমন: NX-94821) এবং এসএমএস দেওয়া হয়। আমাদের লাইভ ট্র্যাকিং পেজে গিয়ে আপনার ফোন নম্বর বা ট্র্যাকিং কোড দিলেই অর্ডারের বর্তমান অবস্থা (প্যাকিং, ইন-ট্রানজিট, বা ডেলিভারি) রিয়েল-টাইমে দেখতে পাবেন।',
    links: [{ label: 'লাইভ অর্ডার ট্র্যাকার ওপেন করুন', href: '/track-order' }]
  },
  {
    id: 'warranty',
    icon: ShieldCheck,
    label: '🛡️ ওয়ারেন্টি ও ৭ দিনের রিপ্লেসমেন্ট',
    question: 'প্রোডাক্টের ওয়ারেন্টি পলিসি এবং নষ্ট হলে কী সুবিধা পাব?',
    reply: 'NEXORA-র প্রতিটি গ্যাজেটে পাবেন:\n\n• ১ বছরের অফিশিয়াল হার্ডওয়্যার ওয়ারেন্টি\n• ৭ দিনের ইনস্ট্যান্ট রিপ্লেসমেন্ট গ্যারান্টি (RMA)\n\nপ্রোডাক্টে কোনো ম্যানুফ্যাকচারিং ত্রুটি থাকলে সরাসরি আমাদের অনলাইন RMA পোর্টালে ক্লেইম সাবমিট করতে পারবেন।',
    links: [{ label: 'ওয়ারেন্টি ক্লেইম পোর্টাল', href: '/warranty-claim' }]
  },
  {
    id: 'payment',
    icon: CreditCard,
    label: '💳 ক্যাশ অন ডেলিভারি ও পেমেন্ট',
    question: 'পেমেন্ট মেথড কী কী আছে? ক্যাশ অন ডেলিভারি হবে?',
    reply: 'হ্যাঁ, ১০০% ক্যাশ অন ডেলিভারি সুবিধা রয়েছে! এছাড়া বিকাশ (bKash), নগদ (Nagad), ভিসা/মাস্টারকার্ড ও ব্যাংক ট্রান্সফারের মাধ্যমে সম্পূর্ণ সিকিউরড পেমেন্ট করতে পারবেন। কোনো হিডেন চার্জ নেই।',
    links: [{ label: 'চেকআউট পেজ', href: '/checkout' }]
  },
  {
    id: 'genuine',
    icon: Smartphone,
    label: '📱 প্রোডাক্ট কি ১০০% আসল ও অফিসিয়াল?',
    question: 'গ্যাজেটগুলো কি আসল ও ইনট্যাক্ট বক্স?',
    reply: 'NEXORA-র প্রতিটি প্রোডাক্ট ১০০% আসল, আন-অ্যাক্টিভেটেড ও ইনট্যাক্ট ফ্যাক্টরি সিল প্যাকড। Apple, Samsung, Google Pixel, Sony, OnePlus সহ ১০টি গ্লোবাল ফ্ল্যাগশিপ ব্র্যান্ডের অফিসিয়াল আইএমইআই (IMEI) ও সিরিয়াল নম্বর ওয়েবসাইটে যাচাই করে নিতে পারবেন।',
    links: [{ label: 'ফ্ল্যাগশিপ গ্যাজেট কালেকশন', href: '/explore' }]
  },
  {
    id: 'founder',
    icon: UserCheck,
    label: '👤 ফাউন্ডার জাকারিয়া তানিমের সাথে যোগাযোগ',
    question: 'প্রতিষ্ঠাতা জাকারিয়া তানিম বা হেড অফিসে কীভাবে কথা বলব?',
    reply: 'NEXORA পরিচালিত হচ্ছে ফাউন্ডার ও চিফ আর্কিটেক্ট জাকারিয়া তানিম (Jakaria Tanim)-এর সরাসরি তত্ত্বাবধানে। যেকোনো ভিআইপি ইনকোয়ারি বা বাল্ক অর্ডারের জন্য আপনি সরাসরি ওনারের সাথে যোগাযোগ করতে পারেন।',
    links: [{ label: 'ফাউন্ডারস ভিশন পেজ', href: '/founder' }]
  }
];

export const WhatsAppConcierge: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [mode, setMode] = useState<'ai' | 'whatsapp'>('ai');
  const [inputText, setInputText] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const phoneNumber = '8801640026177';
  const defaultWhatsAppMsg = 'Hello NEXORA Concierge, I would like to inquire about your flagship hardware collection.';

  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 'welcome',
      sender: 'bot',
      text: 'আসসালামু আলাইকুম! আমি NEXORA AI ভার্চুয়াল অ্যাসিস্ট্যান্ট 🤖\n\nফ্ল্যাগশিপ গ্যাজেট, ডেলিভারি, অর্ডার ট্র্যাকিং, ওয়ারেন্টি বা পেমেন্ট নিয়ে আপনার যেকোনো প্রশ্নে সাহায্য করতে আমি প্রস্তুত। নিচের যেকোনো বিষয়ে ক্লিক করুন অথবা আপনার প্রশ্নটি লিখে জানান:',
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

  const handleOpenWhatsApp = (customMsg?: string) => {
    const text = customMsg || defaultWhatsAppMsg;
    const url = `https://wa.me/${phoneNumber}?text=${encodeURIComponent(text)}`;
    window.open(url, '_blank', 'noopener,noreferrer');
  };

  const handleTopicClick = (topic: typeof QUICK_TOPICS[0]) => {
    const userMsg: ChatMessage = {
      id: `user-${Date.now()}`,
      sender: 'user',
      text: topic.question,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages(prev => [...prev, userMsg]);
    setIsTyping(true);

    setTimeout(() => {
      const botMsg: ChatMessage = {
        id: `bot-${Date.now()}`,
        sender: 'bot',
        text: topic.reply,
        links: topic.links,
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setMessages(prev => [...prev, botMsg]);
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

    // AI Query Intelligence Engine
    setTimeout(() => {
      const q = query.toLowerCase();
      let replyText = '';
      let replyLinks: { label: string; href: string }[] | undefined = undefined;

      if (q.includes('ট্র্যাক') || q.includes('track') || q.includes('কোথায়') || q.includes('অবস্থা')) {
        replyText = 'আপনার অর্ডারের লাইভ লোকেশন ও অগ্রগতি দেখতে আমাদের লাইভ অর্ডার ট্র্যাকার ব্যবহার করুন। অর্ডার করার সময় পাওয়া মোবাইল নম্বর অথবা অর্ডার আইডি (যেমন: NX-94821) ইনপুট দিলেই ৫-ধাপের লাইভ স্ট্যাটাস দেখতে পাবেন।';
        replyLinks = [{ label: 'লাইভ অর্ডার ট্র্যাকার', href: '/track-order' }];
      } else if (q.includes('ডেলিভারি') || q.includes('চার্জ') || q.includes('শিপিং') || q.includes('delivery') || q.includes('shipping')) {
        replyText = 'NEXORA-র ডেলিভারি রেট ও সময়সূচি:\n• ঢাকা মেট্রো: ৳৭০ (২৪ ঘণ্টা)\n• গ্রেটার ঢাকা: ৳১০০ (২৪-৩৬ ঘণ্টা)\n• সারা বাংলাদেশ: ৳১৪০ (২৪-৪৮ ঘণ্টা)\n\nপ্রোডাক্ট হাতে পেয়ে চেক করে ক্যাশ অন ডেলিভারিতে টাকা দেওয়ার সুবিধা রয়েছে।';
        replyLinks = [{ label: 'প্রোডাক্ট কালেকশন দেখুন', href: '/explore' }];
      } else if (q.includes('ওয়ারেন্টি') || q.includes('গ্যারান্টি') || q.includes('রিপ্লেস') || q.includes('নষ্ট') || q.includes('warranty') || q.includes('rma')) {
        replyText = 'আমাদের প্রতিটি প্রোডাক্টে পাবেন ১ বছরের অফিসিয়াল হার্ডওয়্যার ওয়্যারেন্টি এবং ৭ দিনের তাৎক্ষণিক রিপ্লেসমেন্ট গ্যারান্টি (RMA)। কোনো সমস্যা হলে নিচের লিংকে ক্লিক করে সরাসরি ক্লেইম জমা দিন।';
        replyLinks = [{ label: 'ওয়ারেন্টি ক্লেইম পোর্টাল', href: '/warranty-claim' }];
      } else if (q.includes('টাকা') || q.includes('পেমেন্ট') || q.includes('বিকাশ') || q.includes('নগদ') || q.includes('ক্যাশ') || q.includes('payment') || q.includes('cod')) {
        replyText = 'আমরা ক্যাশ অন ডেলিভারি (COD), বিকাশ, নগদ, মাস্টারকার্ড, ভিসা ও ব্যাংক ট্রান্সফার গ্রহণ করি। কোনো অতিরিক্ত ফি ছাড়াই আপনি অর্ডার নিশ্চিত করতে পারবেন।';
        replyLinks = [{ label: 'চেকআউট পেজে যান', href: '/checkout' }];
      } else if (q.includes('আসল') || q.includes('জেনুইন') || q.includes('নকল') || q.includes('original') || q.includes('genuine')) {
        replyText = 'NEXORA-র সকল প্রোডাক্ট ১০০% অরিজিনাল, আনটাচড এবং ফ্যাক্টরি ইনট্যাক্ট। বক্সের আইএমইআই (IMEI) ও সিরিয়াল নম্বর দিয়ে আপনি সরাসরি অফিসিয়াল ওয়েবসাইটে অথেন্টিসিটি যাচাই করতে পারবেন।';
      } else if (q.includes('তানিম') || q.includes('মালিক') || q.includes('ওনার') || q.includes('founder') || q.includes('owner')) {
        replyText = 'NEXORA প্ল্যাটফর্মটি প্রতিষ্ঠিত ও পরিচালিত হচ্ছে জাকারিয়া তানিম (Jakaria Tanim)-এর নেতৃত্বে। আপনি চাইলে সরাসরি তার সাথে যোগাযোগ করতে পারেন।';
        replyLinks = [{ label: 'ফাউন্ডার পেজ দেখুন', href: '/founder' }];
      } else if (q.includes('emi') || q.includes('কিস্তি')) {
        replyText = 'হ্যাঁ! দেশের শীর্ষস্থানীয় ব্যাংকের ক্রেডিট কার্ডের মাধ্যমে ০% সুদে ৩ থেকে ৩৬ মাস পর্যন্ত সহজ কিস্তিতে (EMI) কেনার সুবিধা রয়েছে।';
      } else {
        replyText = `আপনার প্রশ্নের জন্য ধন্যবাদ! আপনার বিষয়টি নিয়ে সরাসরি আমাদের বিশেষজ্ঞ টিমের সাথে কথা বলতে নিচের বাটনে ক্লিক করে হোয়াটসঅ্যাপে চ্যাট করুন:`;
      }

      const botMsg: ChatMessage = {
        id: `bot-${Date.now()}`,
        sender: 'bot',
        text: replyText,
        links: replyLinks,
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };

      setMessages(prev => [...prev, botMsg]);
      setIsTyping(false);
    }, 550);
  };

  const handleResetChat = () => {
    setMessages([
      {
        id: 'welcome-reset',
        sender: 'bot',
        text: 'আসসালামু আলাইকুম! আমি NEXORA AI ভার্চুয়াল অ্যাসিস্ট্যান্ট 🤖\nকীভাবে আপনাকে সহযোগিতা করতে পারি? নিচের যেকোনো টপিকে ক্লিক করুন:',
        time: 'Just now'
      }
    ]);
  };

  return (
    <div className="fixed bottom-20 md:bottom-6 right-4 md:right-6 z-40 flex flex-col items-end print:hidden">
      
      {/* Expanded AI Support Window */}
      {isOpen && (
        <div className="mb-3 w-[92vw] sm:w-[380px] max-h-[580px] h-[520px] rounded-3xl bg-white dark:bg-[#0E1322] border border-black/10 dark:border-white/15 shadow-2xl overflow-hidden flex flex-col animate-fade-in text-left">
          
          {/* Header */}
          <div className="px-4 py-3 bg-gradient-to-r from-[#0B132B] via-[#1C2541] to-[#0B132B] text-white flex items-center justify-between border-b border-white/10">
            <div className="flex items-center gap-2.5">
              <div className="relative w-8 h-8 rounded-xl bg-indigo-500/20 border border-indigo-400/30 flex items-center justify-center">
                <Bot className="w-5 h-5 text-indigo-400" />
                <span className="absolute -top-0.5 -right-0.5 w-2.5 h-2.5 rounded-full bg-emerald-500 ring-2 ring-[#0B132B]" />
              </div>
              <div>
                <div className="flex items-center gap-1.5">
                  <h3 className="text-xs font-bold tracking-tight">NEXORA AI Concierge</h3>
                  <span className="text-[9px] font-semibold bg-emerald-500/20 text-emerald-300 border border-emerald-400/30 px-1.5 py-0.2 rounded-full">
                    Online
                  </span>
                </div>
                <p className="text-[10px] text-slate-300">
                  Instant Automated Support & Hardware Expert
                </p>
              </div>
            </div>

            <div className="flex items-center gap-1">
              <button
                type="button"
                onClick={handleResetChat}
                title="চ্যাট রিসেট করুন"
                className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-white/10 transition-colors"
              >
                <RotateCcw className="w-3.5 h-3.5" />
              </button>
              <button
                type="button"
                onClick={() => setIsOpen(false)}
                className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-white/10 transition-colors"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* Mode Switch Tabs */}
          <div className="grid grid-cols-2 bg-slate-100 dark:bg-white/5 border-b border-black/[0.06] dark:border-white/10 p-1 text-xs font-semibold">
            <button
              type="button"
              onClick={() => setMode('ai')}
              className={`py-1.5 rounded-xl transition-all flex items-center justify-center gap-1.5 ${
                mode === 'ai'
                  ? 'bg-white dark:bg-[#1A2035] text-indigo-600 dark:text-indigo-400 shadow-sm'
                  : 'text-slate-500 hover:text-slate-900 dark:hover:text-white'
              }`}
            >
              <Sparkles className="w-3.5 h-3.5" />
              <span>রোবটিক এআই অ্যাসিস্ট্যান্ট</span>
            </button>
            <button
              type="button"
              onClick={() => setMode('whatsapp')}
              className={`py-1.5 rounded-xl transition-all flex items-center justify-center gap-1.5 ${
                mode === 'whatsapp'
                  ? 'bg-emerald-600 text-white shadow-sm'
                  : 'text-slate-500 hover:text-slate-900 dark:hover:text-white'
              }`}
            >
              <MessageCircle className="w-3.5 h-3.5" />
              <span>হোয়াটসঅ্যাপে মানুষ এজেন্ট</span>
            </button>
          </div>

          {/* Tab 1: AI Chat Area */}
          {mode === 'ai' && (
            <div className="flex-1 flex flex-col overflow-hidden bg-slate-50/60 dark:bg-[#0A0E1A]">
              
              {/* Message List */}
              <div className="flex-1 p-3.5 overflow-y-auto space-y-3 text-xs">
                {messages.map((m) => (
                  <div
                    key={m.id}
                    className={`flex flex-col ${m.sender === 'user' ? 'items-end' : 'items-start'}`}
                  >
                    <div
                      className={`max-w-[85%] rounded-2xl p-3 shadow-sm leading-relaxed ${
                        m.sender === 'user'
                          ? 'bg-indigo-600 text-white rounded-br-xs'
                          : 'bg-white dark:bg-[#151D30] text-slate-800 dark:text-slate-200 border border-black/5 dark:border-white/10 rounded-bl-xs whitespace-pre-line'
                      }`}
                    >
                      {m.text}

                      {/* Attached Links if any */}
                      {m.links && m.links.length > 0 && (
                        <div className="mt-2.5 pt-2 border-t border-black/10 dark:border-white/10 space-y-1.5">
                          {m.links.map((link, idx) => (
                            <Link
                              key={idx}
                              href={link.href}
                              onClick={() => setIsOpen(false)}
                              className="inline-flex items-center gap-1.5 text-[11px] font-bold text-indigo-600 dark:text-indigo-400 hover:underline bg-indigo-50 dark:bg-indigo-950/40 px-2.5 py-1 rounded-lg"
                            >
                              <span>{link.label}</span>
                              <ChevronRight className="w-3 h-3" />
                            </Link>
                          ))}
                        </div>
                      )}
                    </div>
                    <span className="text-[9px] text-slate-400 mt-0.5 px-1 font-mono">
                      {m.time}
                    </span>
                  </div>
                ))}

                {/* Typing Indicator */}
                {isTyping && (
                  <div className="flex items-center gap-1.5 text-slate-400 text-xs py-1">
                    <span className="w-2 h-2 rounded-full bg-indigo-500 animate-bounce" style={{ animationDelay: '0ms' }} />
                    <span className="w-2 h-2 rounded-full bg-indigo-500 animate-bounce" style={{ animationDelay: '150ms' }} />
                    <span className="w-2 h-2 rounded-full bg-indigo-500 animate-bounce" style={{ animationDelay: '300ms' }} />
                    <span className="text-[10px] text-slate-500 ml-1">NEXORA AI লিখছে...</span>
                  </div>
                )}

                {/* Quick Topic Chips */}
                <div className="pt-2 space-y-1.5">
                  <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider px-1">
                    কুইক টপিক সিলেক্ট করুন:
                  </div>
                  <div className="flex flex-wrap gap-1.5">
                    {QUICK_TOPICS.map((topic) => (
                      <button
                        key={topic.id}
                        type="button"
                        onClick={() => handleTopicClick(topic)}
                        className="text-left text-[11px] font-medium px-2.5 py-1.5 rounded-xl bg-white dark:bg-[#151D30] border border-black/10 dark:border-white/10 hover:border-indigo-500 dark:hover:border-indigo-400 text-slate-700 dark:text-slate-300 hover:text-indigo-600 dark:hover:text-indigo-400 transition-all shadow-xs active:scale-95"
                      >
                        {topic.label}
                      </button>
                    ))}
                  </div>
                </div>

                <div ref={messagesEndRef} />
              </div>

              {/* Chat Input Bar */}
              <form
                onSubmit={handleSendCustomMessage}
                className="p-2.5 bg-white dark:bg-[#0E1322] border-t border-black/10 dark:border-white/10 flex items-center gap-2"
              >
                <input
                  type="text"
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  placeholder="যেকোনো প্রশ্ন লিখে পাঠান..."
                  className="flex-1 px-3 py-2 rounded-xl bg-slate-100 dark:bg-white/5 border border-black/5 dark:border-white/10 text-xs text-slate-800 dark:text-white focus:outline-none focus:border-indigo-500"
                />
                <button
                  type="submit"
                  disabled={!inputText.trim() || isTyping}
                  className="p-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white disabled:opacity-40 transition-colors shadow-sm"
                  aria-label="Send Message"
                >
                  <Send className="w-4 h-4" />
                </button>
              </form>
            </div>
          )}

          {/* Tab 2: WhatsApp Human Agent Area */}
          {mode === 'whatsapp' && (
            <div className="flex-1 p-5 overflow-y-auto flex flex-col justify-between bg-slate-50 dark:bg-[#0A0E1A] text-center">
              <div className="space-y-3 pt-2">
                <div className="w-14 h-14 mx-auto rounded-2xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-600 dark:text-emerald-400 flex items-center justify-center">
                  <Headphones className="w-7 h-7" />
                </div>
                <div className="space-y-1">
                  <h4 className="text-sm font-bold text-slate-900 dark:text-white">
                    সরাসরি কাস্টমার কেয়ার প্রতিনিধির সাথে চ্যাট
                  </h4>
                  <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed max-w-xs mx-auto">
                    আমাদের অ্যাপল ও ফ্ল্যাগশিপ স্পেশালিস্টদের সাথে সরাসরি হোয়াটসঅ্যাপে কথা বলে অর্ডার ও টেকনিক্যাল সাপোর্ট নিন।
                  </p>
                </div>

                <div className="p-3 rounded-2xl bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-800/40 text-xs text-emerald-800 dark:text-emerald-300 font-semibold">
                  📞 অফিসিয়াল হটলাইন: +880 1640-026177 (২৪/৭ খোলা)
                </div>
              </div>

              <div className="space-y-2 pt-4">
                <button
                  type="button"
                  onClick={() => handleOpenWhatsApp()}
                  className="w-full py-3 rounded-2xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs flex items-center justify-center gap-2 shadow-lg hover:shadow-emerald-600/30 transition-all active:scale-95"
                >
                  <MessageCircle className="w-4 h-4" />
                  <span>WhatsApp-এ সরাসরি মেসেজ দিন</span>
                </button>
                <button
                  type="button"
                  onClick={() => setMode('ai')}
                  className="w-full py-2 text-xs text-slate-500 hover:text-slate-800 dark:hover:text-white"
                >
                  ← রোবটিক এআই অ্যাসিস্ট্যান্টে ফিরে যান
                </button>
              </div>
            </div>
          )}

          {/* Footer note */}
          <div className="px-3 py-1.5 bg-slate-100 dark:bg-white/[0.03] border-t border-black/5 dark:border-white/10 text-[10px] text-center text-slate-400 font-mono">
            Powered by NEXORA AI Concierge &bull; Directed by Jakaria Tanim
          </div>
        </div>
      )}

      {/* Floating Toggle Button */}
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        className="group relative flex items-center gap-2.5 px-4 py-3 rounded-full bg-gradient-to-r from-indigo-600 to-indigo-700 hover:from-indigo-500 hover:to-indigo-600 text-white shadow-xl hover:shadow-indigo-600/30 transition-all duration-300 active:scale-95"
        title="NEXORA AI Smart Concierge"
        aria-label="NEXORA AI Smart Concierge"
      >
        <span className="relative flex h-3 w-3">
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
          <span className="relative inline-flex rounded-full h-3 w-3 bg-emerald-400"></span>
        </span>
        <Bot className="w-5 h-5 transition-transform group-hover:scale-110" />
        <span className="text-xs font-bold tracking-wide hidden sm:inline">
          {isOpen ? 'Close Support' : 'AI Concierge Support'}
        </span>
      </button>

    </div>
  );
};

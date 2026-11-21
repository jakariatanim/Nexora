export interface ConciergeReply {
  text: string;
  links?: { label: string; href: string }[];
}

export function getConciergeAIResponse(rawQuery: string, lang: 'en' | 'bn'): ConciergeReply {
  const q = rawQuery.toLowerCase().trim();

  // 1. Buying / Order Placement Intent ("buy", "order", "kinbo", "kivabe", etc.)
  if (
    q.includes('buy') || 
    q.includes('purchase') || 
    q.includes('order') || 
    q.includes('kinbo') || 
    q.includes('kivabe kinbo') || 
    q.includes('order korbo') || 
    q.includes('order kivabe') || 
    q.includes('কিনব') || 
    q.includes('কিনতে চাই') || 
    q.includes('অর্ডার করব') || 
    q.includes('কিভাবে কিনব') || 
    q.includes('কিভাবে অর্ডার') || 
    q.includes('কেনার নিয়ম')
  ) {
    if (lang === 'en') {
      return {
        text: 'Buying flagship hardware on NEXORA is quick and 100% secure:\n\n1. Browse our catalog and select your desired device.\n2. Click "Add to Cart" or "Buy Now".\n3. In checkout, enter your shipping details.\n4. Choose Cash on Delivery (COD) or bKash / Card payment.\n\nYour order is dispatched via express insured courier within 24–48 hours nationwide!',
        links: [
          { label: 'Browse Hardware Catalog', href: '/explore' },
          { label: 'Go to Secure Checkout', href: '/checkout' }
        ]
      };
    } else {
      return {
        text: 'NEXORA থেকে প্রোডাক্ট অর্ডার করা খুবই সহজ ও নিরাপদ:\n\n১. আমাদের ক্যাটালগ থেকে আপনার পছন্দের ফোন বা গ্যাজেট সিলেক্ট করুন।\n২. "Add to Cart" অথবা "Buy Now" বাটনে চাপুন।\n৩. আপনার নাম, মোবাইল নম্বর এবং ডেলিভারির ঠিকানা দিন।\n৪. ক্যাশ অন ডেলিভারি (COD) বা বিকাশ/কার্ড পেমেন্ট সিলেক্ট করে অর্ডার কনফার্ম করুন।\n\nসারা দেশে ২৪ থেকে ৪৮ ঘণ্টার মধ্যে পার্সেল হাতে পেয়ে চেক করে টাকা পরিশোধ করতে পারবেন!',
        links: [
          { label: 'ক্যাটালগ ঘুরে দেখুন', href: '/explore' },
          { label: 'চেকআউট পেজ', href: '/checkout' }
        ]
      };
    }
  }

  // 2. Apple / iPhone Intent
  if (
    q.includes('iphone') || 
    q.includes('apple') || 
    q.includes('16 pro') || 
    q.includes('15 pro') || 
    q.includes('macbook') || 
    q.includes('airpods') || 
    q.includes('ipad') || 
    q.includes('আইফোন') || 
    q.includes('অ্যাপল') || 
    q.includes('এপল')
  ) {
    if (lang === 'en') {
      return {
        text: 'NEXORA curates 100% brand-new, authentic Apple flagships including iPhone 16 Pro Max, iPhone 16 Pro, iPhone 15 series, MacBook Pro/Air, and AirPods.\n\n• Factory-sealed with intact manufacturer pull tabs\n• Official 1-Year hardware warranty coverage\n• 7-Day instant replacement guarantee\n• IMEI & Serial verifiable on Apple portal',
        links: [
          { label: 'Browse Apple Catalog', href: '/explore' }
        ]
      };
    } else {
      return {
        text: 'NEXORA-তে পাচ্ছেন একদম নতুন ও ১০০% অথেনটিক ইনট্যাক্ট সিল করা Apple আইফোন (iPhone 16 Pro Max, 16 Pro, 15 Pro, MacBook ও AirPods)।\n\n• ইনট্যাক্ট সিল প্যাক ও অফিশিয়াল সিরিয়াল ভেরিফিকেশন\n• ১ বছরের অফিশিয়াল হার্ডওয়্যার ওয়্যারেন্টি\n• ৭ দিনের ইনস্ট্যান্ট রিপ্লেসমেন্ট গ্যারান্টি\n• ক্যাশ অন ডেলিভারিতে চেক করে নেওয়ার সুবিধা',
        links: [
          { label: 'আইফোন ক্যাটালগ দেখুন', href: '/explore' }
        ]
      };
    }
  }

  // 3. Samsung Galaxy Intent
  if (
    q.includes('samsung') || 
    q.includes('s24') || 
    q.includes('galaxy') || 
    q.includes('ultra') || 
    q.includes('fold') || 
    q.includes('flip') || 
    q.includes('স্যামসাং')
  ) {
    if (lang === 'en') {
      return {
        text: 'We feature authentic Samsung Galaxy flagships including the Galaxy S24 Ultra, S24+, and Galaxy Z Fold/Flip series. All devices are factory-sealed global editions backed by NEXORA 1-Year warranty.',
        links: [
          { label: 'Explore Samsung Galaxy', href: '/explore' }
        ]
      };
    } else {
      return {
        text: 'স্যামসাং গ্যালাক্সি S24 আল্ট্রা, Z Fold এবং সকল অফিশিয়াল স্যামসাং ফ্ল্যাগশিপ NEXORA-তে এভেইলেবল। ১০০% ইনট্যাক্ট বক্সে ১ বছরের অফিশিয়াল ওয়্যারেন্টি সহ দ্রুত ডেলিভারি দেওয়া হয়।',
        links: [
          { label: 'স্যামসাং গ্যাজেট দেখুন', href: '/explore' }
        ]
      };
    }
  }

  // 4. Sony / Audio / Headphones Intent
  if (
    q.includes('sony') || 
    q.includes('wh-1000') || 
    q.includes('headphone') || 
    q.includes('earphone') || 
    q.includes('audio') || 
    q.includes('sound') || 
    q.includes('হেডফোন') || 
    q.includes('ইয়ারফোন') || 
    q.includes('অডিও')
  ) {
    if (lang === 'en') {
      return {
        text: 'Experience world-class acoustic fidelity with Sony WH-1000XM5 and WF-1000XM5 noise-cancelling headphones, along with premium AirPods. All audio gear comes 100% factory-sealed with official warranty.',
        links: [
          { label: 'Browse Audio Gear', href: '/explore' }
        ]
      };
    } else {
      return {
        text: 'সোনির প্রিমিয়াম নয়েজ ক্যানসেলিং হেডফোন (Sony WH-1000XM5, WF-1000XM5) এবং অ্যাপল এয়ারপডস পাচ্ছেন ১০০% ইনট্যাক্ট সিল প্যাকড অবস্থায় ১ বছরের ওয়্যারেন্টি সহ।',
        links: [
          { label: 'অডিও ক্যাটালগ দেখুন', href: '/explore' }
        ]
      };
    }
  }

  // 5. Google Pixel Intent
  if (q.includes('pixel') || q.includes('পিক্সেল')) {
    if (lang === 'en') {
      return {
        text: 'Explore pure Android excellence with Google Pixel 9 Pro, Pixel 8 Pro, and Pixel accessories. 100% original, brand new, factory-unlocked, and backed by NEXORA 1-Year warranty.',
        links: [
          { label: 'Explore Google Pixel', href: '/explore' }
        ]
      };
    } else {
      return {
        text: 'গুগল পিক্সেল ৯ প্রো, পিক্সেল ৮ সহ সকল অথেনটিক গুগল ফ্ল্যাগশিপ ডিভাইস পাচ্ছেন NEXORA-তে, সম্পূর্ণ ১ বছরের অফিশিয়াল ওয়্যারেন্টি সহ।',
        links: [
          { label: 'পিক্সেল ডিভাইস দেখুন', href: '/explore' }
        ]
      };
    }
  }

  // 6. Price / Cost / EMI / Offers Intent
  if (
    q.includes('price') || 
    q.includes('cost') || 
    q.includes('rate') || 
    q.includes('dam') || 
    q.includes('koto dam') || 
    q.includes('dam koto') || 
    q.includes('koto taka') || 
    q.includes('taka') || 
    q.includes('discount') || 
    q.includes('offer') || 
    q.includes('emi') || 
    q.includes('kisti') || 
    q.includes('দাম') || 
    q.includes('টাকা') || 
    q.includes('মূল্য') || 
    q.includes('অফার') || 
    q.includes('ডিসকাউন্ট') || 
    q.includes('কিস্তি') || 
    q.includes('ইএমআই')
  ) {
    if (lang === 'en') {
      return {
        text: 'We provide competitive market pricing in Bangladesh with 0% interest EMI options up to 36 months on credit cards. You can check live prices, storage variants, and ongoing promotions directly in our catalog.',
        links: [
          { label: 'View Live Product Prices', href: '/explore' },
          { label: 'Explore 0% EMI Options', href: '/checkout' }
        ]
      };
    } else {
      return {
        text: 'NEXORA-তে সকল অরিজিনাল ফ্ল্যাগশিপ পাচ্ছেন সেরা ও যৌক্তিক মূল্যে। সাথে থাকছে ক্রেডিট কার্ডে ৩৬ মাস পর্যন্ত ০% সুদে সহজ কিস্তি (EMI) সুবিধা। আজকের লাইভ দাম ও অফার দেখতে আমাদের ক্যাটালগ চেক করুন।',
        links: [
          { label: 'প্রোডাক্টের লাইভ দাম দেখুন', href: '/explore' }
        ]
      };
    }
  }

  // 7. Delivery / Shipping Timeline & Charges Intent
  if (
    q.includes('deliver') || 
    q.includes('shipping') || 
    q.includes('fee') || 
    q.includes('charge') || 
    q.includes('kobe pabo') || 
    q.includes('kotodin') || 
    q.includes('ডেলিভারি') || 
    q.includes('চার্জ') || 
    q.includes('শিপিং') || 
    q.includes('কবে পাব') || 
    q.includes('কয়দিন')
  ) {
    if (lang === 'en') {
      return {
        text: 'We provide express, insured dispatch across Bangladesh:\n\n• Dhaka Metro: ৳70 (Guaranteed within 24 Hours)\n• Greater Dhaka: ৳100 (24–36 Hours)\n• Nationwide: ৳140 (24–48 Hours)\n\nCash on Delivery (COD) is available nationwide—inspect your package before completing payment.',
        links: [
          { label: 'Explore Hardware Catalog', href: '/explore' }
        ]
      };
    } else {
      return {
        text: 'আমাদের এক্সপ্রেস ও সুরক্ষিত ডেলিভারি চার্জ এবং সময়সীমা:\n\n• ঢাকা মেট্রো: ৳৭০ (২৪ ঘণ্টার মধ্যে গ্যারান্টিড)\n• গ্রেটার ঢাকা: ৳১০০ (২৪–৩৬ ঘণ্টা)\n• সারা বাংলাদেশ: ৳১৪০ (২৪–৪৮ ঘণ্টার মধ্যে)\n\nসারা দেশে ক্যাশ অন ডেলিভারি সুবিধা রয়েছে—প্রোডাক্ট চেক করে পেমেন্ট করার সুযোগ পাবেন।',
        links: [
          { label: 'ক্যাটালগ দেখুন', href: '/explore' }
        ]
      };
    }
  }

  // 8. Order Tracking Intent
  if (
    q.includes('track') || 
    q.includes('order') || 
    q.includes('status') || 
    q.includes('koi') || 
    q.includes('ট্র্যাক') || 
    q.includes('অর্ডার কই') || 
    q.includes('কোথায় আছে')
  ) {
    if (lang === 'en') {
      return {
        text: 'Track your active order in real time! Once your order is dispatched, you receive an automated SMS with your 5-digit Order ID (e.g. NX-94821). Simply enter your Order ID or phone number in our Live Satellite Tracker to view transit progress.',
        links: [
          { label: 'Open Live Order Tracker', href: '/track-order' }
        ]
      };
    } else {
      return {
        text: 'আপনার অর্ডারের বর্তমান অবস্থা লাইভ ট্র্যাক করতে পারবেন! অর্ডার পাঠানোর পর আপনার ফোনে ৫ ডিজিটের অর্ডার আইডি (যেমন: NX-94821) এসএমএস করা হয়। আমাদের লাইভ ট্র্যাকার পেজে গিয়ে আইডি বা মোবাইল নম্বর দিয়ে এখনই অবস্থান দেখুন।',
        links: [
          { label: 'লাইভ অর্ডার ট্র্যাকার', href: '/track-order' }
        ]
      };
    }
  }

  // 9. Warranty / RMA / Replacement Intent
  if (
    q.includes('warrant') || 
    q.includes('guarantee') || 
    q.includes('rma') || 
    q.includes('replace') || 
    q.includes('defect') || 
    q.includes('nosto') || 
    q.includes('ferot') || 
    q.includes('ওয়ারেন্টি') || 
    q.includes('গ্যারান্টি') || 
    q.includes('রিপ্লেসমেন্ট') || 
    q.includes('নষ্ট') || 
    q.includes('ফেরত')
  ) {
    if (lang === 'en') {
      return {
        text: 'Every flagship device sold by NEXORA carries:\n\n• 1-Year Official Hardware Warranty coverage\n• 7-Day Instant Replacement Guarantee (RMA)\n\nIf you experience any manufacturing fault, file an instant claim through our online RMA Portal for inspection and swift replacement.',
        links: [
          { label: 'Submit Warranty Claim', href: '/warranty-claim' }
        ]
      };
    } else {
      return {
        text: 'NEXORA-র প্রতিটি গ্যাজেটে রয়েছে পূর্ণ নিরাপত্তা:\n\n• ১ বছরের অফিশিয়াল হার্ডওয়্যার ওয়ারেন্টি\n• ৭ দিনের ইনস্ট্যান্ট রিপ্লেসমেন্ট গ্যারান্টি (RMA)\n\nকোনো ত্রুটি দেখা দিলে সরাসরি আমাদের অনলাইন ওয়্যারেন্টি পোর্টালে ক্লেইম সাবমিট করতে পারবেন।',
        links: [
          { label: 'ওয়ারেন্টি ক্লেইম পোর্টাল', href: '/warranty-claim' }
        ]
      };
    }
  }

  // 10. Payment / COD / bKash / Cards Intent
  if (
    q.includes('pay') || 
    q.includes('cod') || 
    q.includes('bkash') || 
    q.includes('nagad') || 
    q.includes('card') || 
    q.includes('visa') || 
    q.includes('পেমেন্ট') || 
    q.includes('বিকাশ') || 
    q.includes('নগদ') || 
    q.includes('ক্যাশ অন ডেলিভারি')
  ) {
    if (lang === 'en') {
      return {
        text: 'We accept 100% Cash on Delivery (COD), bKash, Nagad, Visa, Mastercard, and Direct Bank Wire Transfer with zero extra surcharges. 0% interest EMI options up to 36 months are also supported on major credit cards.',
        links: [
          { label: 'Proceed to Secure Checkout', href: '/checkout' }
        ]
      };
    } else {
      return {
        text: 'আমরা ১০০% ক্যাশ অন ডেলিভারি (COD), বিকাশ, নগদ, ভিসা ও মাস্টারকার্ড এবং ব্যাংক ট্রান্সফার গ্রহণ করি। কোনো অতিরিক্ত ফি নেই। এছাড়াও ক্রেডিট কার্ডে ৩৬ মাস পর্যন্ত ০% সহজ কিস্তি সুবিধা রয়েছে।',
        links: [
          { label: 'চেকআউট পেজ', href: '/checkout' }
        ]
      };
    }
  }

  // 11. Authenticity / Genuine / Seal Pack Intent
  if (
    q.includes('authentic') || 
    q.includes('genuine') || 
    q.includes('original') || 
    q.includes('seal') || 
    q.includes('pack') || 
    q.includes('asol') || 
    q.includes('আসল') || 
    q.includes('খাঁটি') || 
    q.includes('অরিজিনাল') || 
    q.includes('সিল প্যাক')
  ) {
    if (lang === 'en') {
      return {
        text: '100% Factory-Sealed Genuine Guarantee: All devices curated by NEXORA are original, brand new, and factory-sealed with intact manufacturer seals. Official IMEI and serial numbers can be verified on official manufacturer portals.',
        links: [
          { label: 'Explore Verified Devices', href: '/explore' }
        ]
      };
    } else {
      return {
        text: 'শতভাগ আসল ও সিল প্যাক নিশ্চয়তা: NEXORA-র প্রতিটি প্রোডাক্ট একদম ব্র্যান্ড নিউ, অফিশিয়াল ইনট্যাক্ট সিল প্যাকড। বক্সের অফিশিয়াল IMEI ও সিরিয়াল নম্বর প্রস্তুতকারকের অফিশিয়াল ওয়েবসাইটে ভেরিফাই করে নিতে পারবেন।',
        links: [
          { label: 'ক্যাটালগ দেখুন', href: '/explore' }
        ]
      };
    }
  }

  // 12. Location / Showroom / Office Intent
  if (
    q.includes('location') || 
    q.includes('address') || 
    q.includes('office') || 
    q.includes('shop') || 
    q.includes('store') || 
    q.includes('showroom') || 
    q.includes('dokan') || 
    q.includes('thikana') || 
    q.includes('কোথায়') || 
    q.includes('দোকান') || 
    q.includes('শোরুম') || 
    q.includes('ঠিকানা') || 
    q.includes('অফিস')
  ) {
    if (lang === 'en') {
      return {
        text: 'NEXORA operates as Bangladesh\'s premier online flagship store with fulfillment headquarters in Dhaka. We deliver directly to your doorstep across all 64 districts with Cash on Delivery and package inspection before payment.',
        links: [
          { label: 'Explore Hardware Catalog', href: '/explore' }
        ]
      };
    } else {
      return {
        text: 'NEXORA হলো বাংলাদেশের প্রিমিয়াম অনলাইন ফ্ল্যাগশিপ প্ল্যাটফর্ম। আমাদের সেন্ট্রাল ফুলফিলমেন্ট সেন্টার ঢাকাতে অবস্থিত। সারা দেশের ৬৪ জেলায় ঘরে বসেই ক্যাশ অন ডেলিভারিতে প্রোডাক্ট হাতে পেয়ে চেক করে নেওয়ার সুবিধা পাচ্ছেন।',
        links: [
          { label: 'ক্যাটালগ ঘুরে দেখুন', href: '/explore' }
        ]
      };
    }
  }

  // 13. Founder / Jakaria Tanim Intent
  if (
    q.includes('tanim') || 
    q.includes('jakaria') || 
    q.includes('founder') || 
    q.includes('owner') || 
    q.includes('malik') || 
    q.includes('তানিম') || 
    q.includes('জাকারিয়া') || 
    q.includes('ফাউন্ডার') || 
    q.includes('মালিক')
  ) {
    if (lang === 'en') {
      return {
        text: 'NEXORA is founded and directed by Jakaria Tanim (Chief Architect & Founder). For VIP client procurement or architectural partnerships, explore the Founder\'s vision portal.',
        links: [
          { label: 'Read Founder Vision', href: '/founder' }
        ]
      };
    } else {
      return {
        text: 'NEXORA পরিচালিত হচ্ছে ফাউন্ডার ও চিফ আর্কিটেক্ট জাকারিয়া তানিম (Jakaria Tanim)-এর সরাসরি তত্ত্বাবধানে। ভিআইপি প্রোকিউরমেন্ট বা এক্সিকিউটিভ যোগাযোগের জন্য আমাদের ফাউন্ডার পোর্টাল ভিজিট করতে পারেন।',
        links: [
          { label: 'ফাউন্ডার পেজ দেখুন', href: '/founder' }
        ]
      };
    }
  }

  // 14. Contact / WhatsApp / Phone / Human specialist Intent
  if (
    q.includes('contact') || 
    q.includes('call') || 
    q.includes('phone') || 
    q.includes('number') || 
    q.includes('hotline') || 
    q.includes('whatsapp') || 
    q.includes('human') || 
    q.includes('manush') || 
    q.includes('kotha') || 
    q.includes('কথা') || 
    q.includes('যোগাযোগ') || 
    q.includes('ফোন') || 
    q.includes('নাম্বার') || 
    q.includes('হোয়াটসঅ্যাপ') || 
    q.includes('মানুষ')
  ) {
    if (lang === 'en') {
      return {
        text: 'Our dedicated hardware concierge team is available to speak with you directly:\n\n• WhatsApp / Hotline: +880 1640-026177\n• Email: support@nexora.com\n• Active Hours: 10:00 AM – 11:00 PM (Every Day)',
        links: [
          { label: 'Open WhatsApp Chat', href: 'https://wa.me/8801640026177' }
        ]
      };
    } else {
      return {
        text: 'সরাসরি আমাদের প্রতিনিধির সাথে কথা বলতে পারেন:\n\n• হোয়াটসঅ্যাপ / হটলাইন: +880 1640-026177\n• ইমেইল: support@nexora.com\n• সেবা সময়: সকাল ১০টা – রাত ১১টা (প্রতিদিন)',
        links: [
          { label: 'হোয়াটসঅ্যাপে মেসেজ পাঠান', href: 'https://wa.me/8801640026177' }
        ]
      };
    }
  }

  // 15. Greetings / Politeness
  if (
    q.includes('hi') || 
    q.includes('hello') || 
    q.includes('hey') || 
    q.includes('salam') || 
    q.includes('assalamu') || 
    q.includes('হাই') || 
    q.includes('হ্যালো') || 
    q.includes('সালাম') || 
    q.includes('আসসালামু') || 
    q.includes('কেমন')
  ) {
    if (lang === 'en') {
      return {
        text: 'Hello, Welcome to the Next Era of Flagship Hardware!\n\nI am your NEXORA AI Concierge. How can I assist your flagship hardware journey today? Ask me about iPhones, Galaxy flagships, delivery timelines, order tracking, or how to place an order.',
        links: [
          { label: 'Browse Hardware Catalog', href: '/explore' },
          { label: 'Track Active Order', href: '/track-order' }
        ]
      };
    } else {
      return {
        text: 'Hello, Welcome to the Next Era of Flagship Hardware.\n\nআসসালামু আলাইকুম! আমি NEXORA এআই ভার্চুয়াল কনসিয়ার্জ। আইফোন, স্যামসাং গ্যালাক্সি, দাম, ডেলিভারি চার্জ, অর্ডার করার নিয়ম কিংবা ওয়ারেন্টি নিয়ে যেকোনো প্রশ্ন করুন—আমি সাথে সাথে উত্তর দিচ্ছি!',
        links: [
          { label: 'ক্যাটালগ ঘুরে দেখুন', href: '/explore' },
          { label: 'অর্ডার ট্র্যাক করুন', href: '/track-order' }
        ]
      };
    }
  }

  // 16. Fallback response with helpful actionable guidance
  if (lang === 'en') {
    return {
      text: `Thank you for contacting NEXORA Client Support. We are at your service for device consultations, specifications, and order assistance. You can browse our flagship catalog, track an active parcel, or connect directly on our WhatsApp hotline (+880 1640-026177).`,
      links: [
        { label: 'Explore Hardware Catalog', href: '/explore' },
        { label: 'Live Order Tracker', href: '/track-order' }
      ]
    };
  } else {
    return {
      text: `NEXORA ক্লায়েন্ট সাপোর্টে যোগাযোগ করার জন্য ধন্যবাদ! গ্যাজেট সম্পর্কিত তথ্য, স্পেসিফিকেশন কিংবা অর্ডার সংক্রান্ত যেকোনো প্রয়োজনে আমরা প্রস্তুত আছি। আপনি ক্যাটালগ দেখতে পারেন অথবা সরাসরি আমাদের হটলাইন হোয়াটসঅ্যাপে (+880 1640-026177) যোগাযোগ করতে পারেন।`,
      links: [
        { label: 'ক্যাটালগ ঘুরে দেখুন', href: '/explore' },
        { label: 'লাইভ অর্ডার ট্র্যাকার', href: '/track-order' }
      ]
    };
  }
}

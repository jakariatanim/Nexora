# -*- coding: utf-8 -*-
with open("frontend/src/app/product/[id]/ProductDetailClient.tsx", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Add icons if missing
old_icons = """  Sparkles,
  Heart
} from 'lucide-react';"""

new_icons = """  Sparkles,
  Heart,
  CreditCard,
  MessageCircle,
  HelpCircle,
  X,
  Layers,
  ChevronRight
} from 'lucide-react';"""

text = text.replace(old_icons, new_icons, 1)

# 2. Add state for variants, EMI modal, and active image angle
old_state = """  const [quantity, setQuantity] = useState(1);
  const [added, setAdded] = useState(false);
  const router = useRouter();"""

new_state = """  const [quantity, setQuantity] = useState(1);
  const [added, setAdded] = useState(false);
  const router = useRouter();

  // Multi-variant Selection
  const isPhone = product.category.toLowerCase().includes('phone') || product.name.toLowerCase().includes('iphone');
  const isAudio = product.category.toLowerCase().includes('audio') || product.category.toLowerCase().includes('earbud');
  
  const availableColors = isPhone
    ? [
        { name: 'Natural Titanium', hex: '#C5B9AC' },
        { name: 'Space Black', hex: '#1E1F21' },
        { name: 'Desert Titanium', hex: '#D19E75' },
        { name: 'White Titanium', hex: '#E5E7EB' }
      ]
    : isAudio
    ? [
        { name: 'Midnight Black', hex: '#111827' },
        { name: 'Platinum Silver', hex: '#CBD5E1' },
        { name: 'Pure White', hex: '#F8FAFC' }
      ]
    : [
        { name: 'Space Gray', hex: '#4B5563' },
        { name: 'Silver', hex: '#E2E8F0' },
        { name: 'Matte Black', hex: '#18181B' }
      ];

  const availableStorage = isPhone
    ? [
        { label: '128GB', markup: -10000 },
        { label: '256GB', markup: 0, tag: 'Standard' },
        { label: '512GB', markup: 20000 },
        { label: '1TB', markup: 45000 }
      ]
    : null;

  const [selectedColor, setSelectedColor] = useState(availableColors[0].name);
  const [selectedStorage, setSelectedStorage] = useState(availableStorage ? '256GB' : 'Standard');
  const [activeImageIndex, setActiveImageIndex] = useState(0);
  const [isEmiModalOpen, setIsEmiModalOpen] = useState(false);

  // Dynamic calculated price based on variant
  const currentMarkup = availableStorage?.find(s => s.label === selectedStorage)?.markup || 0;
  const currentPrice = Math.max(0, product.priceBDT + currentMarkup);"""

text = text.replace(old_state, new_state, 1)

# 3. Update handleAddToCart and handleBuyNow
old_handlers = """  const handleAddToCart = () => {
    addToCart(product, quantity);
    setAdded(true);
    setTimeout(() => setAdded(false), 2500);
  };

  const handleBuyNow = () => {
    addToCart(product, quantity);
    router.push('/checkout');
  };"""

new_handlers = """  const handleAddToCart = () => {
    addToCart(product, quantity, true, {
      color: selectedColor,
      storage: selectedStorage,
      priceBDT: currentPrice,
    });
    setAdded(true);
    setTimeout(() => setAdded(false), 2500);
  };

  const handleBuyNow = () => {
    addToCart(product, quantity, false, {
      color: selectedColor,
      storage: selectedStorage,
      priceBDT: currentPrice,
    });
    router.push('/checkout');
  };"""

text = text.replace(old_handlers, new_handlers, 1)

# 4. Add multi-angle thumbnails beneath main visual stage
old_image_box = """            <div className="relative w-full h-64 sm:h-80 md:h-[400px] lg:h-[440px]">
              <Image
                src={product.image}
                alt={product.name}
                fill
                priority
                className="object-contain transform group-hover:scale-105 transition-transform duration-700 drop-shadow-2xl"
              />
            </div>
          </div>"""

new_image_box = """            <div className="relative w-full h-64 sm:h-80 md:h-[400px] lg:h-[440px]">
              <Image
                src={product.image}
                alt={product.name}
                fill
                priority
                className={`object-contain transform transition-all duration-700 drop-shadow-2xl ${
                  activeImageIndex === 1 ? 'scale-105 rotate-3' : activeImageIndex === 2 ? 'scale-100 -rotate-3' : 'group-hover:scale-105'
                }`}
              />
            </div>

            {/* Multi-angle Preview Bar */}
            <div className="absolute bottom-4 left-1/2 -translate-x-1/2 z-20 flex items-center gap-2 px-3 py-1.5 rounded-full bg-white/80 dark:bg-black/60 backdrop-blur-md border border-black/10 dark:border-white/10 shadow-sm">
              {[
                { id: 0, label: 'Studio Front' },
                { id: 1, label: 'Perspective' },
                { id: 2, label: 'Detail Profile' },
              ].map((angle) => (
                <button
                  key={angle.id}
                  type="button"
                  onClick={() => setActiveImageIndex(angle.id)}
                  className={`px-2.5 py-1 rounded-full text-[11px] font-semibold transition-all ${
                    activeImageIndex === angle.id
                      ? 'bg-[#0071E3] text-white shadow-xs'
                      : 'text-[#86868B] hover:text-[#1D1D1F] dark:hover:text-white'
                  }`}
                >
                  {angle.label}
                </button>
              ))}
            </div>
          </div>"""

text = text.replace(old_image_box, new_image_box, 1)

# 5. Enhance Pricing Box with live price & 0% EMI trigger
old_price_box = """            {/* Pricing Box */}
            <div className="p-5 rounded-2xl bg-white border border-black/[0.06] shadow-sm">
              <span className="text-xs font-mono uppercase tracking-wider text-[#86868B] block">
                Official Guaranteed Price
              </span>
              <div className="flex items-baseline gap-3 mt-1.5">
                <span className="text-3xl sm:text-4xl font-extrabold text-[#1D1D1F] font-mono flex items-baseline">
                  <span className="text-xl sm:text-2xl font-semibold text-gray-500 mr-2">৳</span>
                  <span>{product.priceBDT.toLocaleString()}</span>
                </span>
                <span className="text-sm font-mono text-[#6E6E73]">
                  (~${product.priceUSD} USD)
                </span>
              </div>
            </div>"""

new_price_box = """            {/* Pricing Box & 0% EMI Banner */}
            <div className="p-5 rounded-2xl bg-white border border-black/[0.06] shadow-sm space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-mono uppercase tracking-wider text-[#86868B] block">
                  Official Guaranteed Price
                </span>
                <span className="px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
                  NBR VAT Included
                </span>
              </div>

              <div className="flex items-baseline gap-3">
                <span className="text-3xl sm:text-4xl font-extrabold text-[#1D1D1F] font-mono flex items-baseline">
                  <span className="text-xl sm:text-2xl font-semibold text-gray-500 mr-2">৳</span>
                  <span>{currentPrice.toLocaleString()}</span>
                </span>
                <span className="text-sm font-mono text-[#6E6E73]">
                  (~${Math.round(currentPrice / 134)} USD)
                </span>
              </div>

              {/* 0% EMI Feature Bar */}
              {currentPrice >= 20000 && (
                <div className="pt-2 border-t border-black/[0.06] flex items-center justify-between text-xs">
                  <div className="flex items-center gap-1.5 text-slate-700">
                    <CreditCard className="w-3.5 h-3.5 text-[#0071E3]" />
                    <span>0% EMI from <strong>৳{Math.round(currentPrice / 12).toLocaleString()}</strong>/mo (12 Mos)</span>
                  </div>
                  <button
                    type="button"
                    onClick={() => setIsEmiModalOpen(true)}
                    className="text-[#0071E3] hover:underline font-semibold flex items-center gap-0.5"
                  >
                    <span>View Plans</span>
                    <ChevronRight className="w-3 h-3" />
                  </button>
                </div>
              )}
            </div>

            {/* Variant Selectors (Color & Storage) */}
            <div className="p-5 rounded-2xl bg-white border border-black/[0.06] shadow-sm space-y-4">
              {/* Color Swatch Selector */}
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-semibold text-[#1D1D1F]">
                    Color Finish: <span className="text-[#0071E3] font-bold">{selectedColor}</span>
                  </span>
                </div>
                <div className="flex items-center gap-2.5">
                  {availableColors.map((c) => (
                    <button
                      key={c.name}
                      type="button"
                      onClick={() => setSelectedColor(c.name)}
                      className={`group relative p-1 rounded-full transition-all ${
                        selectedColor === c.name ? 'ring-2 ring-[#0071E3] scale-110' : 'hover:scale-105'
                      }`}
                      title={c.name}
                    >
                      <span
                        className="w-6 h-6 rounded-full block border border-black/10 shadow-xs"
                        style={{ backgroundColor: c.hex }}
                      />
                    </button>
                  ))}
                </div>
              </div>

              {/* Storage Capacity Selector */}
              {availableStorage && (
                <div className="pt-3 border-t border-black/[0.06]">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs font-semibold text-[#1D1D1F]">
                      Storage Capacity: <span className="text-[#0071E3] font-bold">{selectedStorage}</span>
                    </span>
                  </div>
                  <div className="grid grid-cols-4 gap-2">
                    {availableStorage.map((st) => (
                      <button
                        key={st.label}
                        type="button"
                        onClick={() => setSelectedStorage(st.label)}
                        className={`py-2 px-1 rounded-xl border text-center transition-all ${
                          selectedStorage === st.label
                            ? 'border-[#0071E3] bg-[#0071E3]/5 text-[#0071E3] font-bold shadow-xs'
                            : 'border-black/10 text-slate-700 hover:border-black/30'
                        }`}
                      >
                        <div className="text-xs">{st.label}</div>
                        {st.markup !== 0 && (
                          <div className="text-[10px] text-gray-500 font-mono">
                            {st.markup > 0 ? `+৳${(st.markup / 1000).toFixed(0)}k` : `-৳${(Math.abs(st.markup) / 1000).toFixed(0)}k`}
                          </div>
                        )}
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </div>"""

text = text.replace(old_price_box, new_price_box, 1)

# 6. Add WhatsApp Consultation Button right below Buy Now
old_buy_now = """              <button
                onClick={handleBuyNow}
                className="w-full py-4 rounded-full bg-[#0071E3] hover:bg-[#0077ED] text-white font-semibold text-sm tracking-wide uppercase transition-all shadow-md active:scale-[0.99] flex items-center justify-center gap-2"
              >
                <span>Instant Checkout</span>
              </button>"""

new_buy_now = """              <button
                onClick={handleBuyNow}
                className="w-full py-4 rounded-full bg-[#0071E3] hover:bg-[#0077ED] text-white font-semibold text-sm tracking-wide uppercase transition-all shadow-md active:scale-[0.99] flex items-center justify-center gap-2"
              >
                <span>Instant Checkout</span>
              </button>

              {/* Direct WhatsApp Concierge Button */}
              <a
                href={`https://wa.me/8801640026177?text=${encodeURIComponent(`Hello NEXORA, I would like to consult about ${product.name} (${selectedColor}, ${selectedStorage}).`)}`}
                target="_blank"
                rel="noopener noreferrer"
                className="w-full py-3 rounded-full border border-emerald-600/30 bg-emerald-50 hover:bg-emerald-100 text-emerald-800 font-medium text-xs tracking-wide transition-all flex items-center justify-center gap-2 shadow-xs"
              >
                <MessageCircle className="w-4 h-4 text-emerald-600" />
                <span>Chat with Apple/Gadget Specialist on WhatsApp</span>
              </a>"""

text = text.replace(old_buy_now, new_buy_now, 1)

# 7. Add EMI Modal at the bottom before closing tag
modal_code = """
      {/* 0% EMI Bank Installment Modal */}
      {isEmiModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-fade-in">
          <div className="bg-white rounded-3xl max-w-lg w-full p-6 sm:p-8 shadow-2xl border border-black/10 relative text-left">
            <button
              onClick={() => setIsEmiModalOpen(false)}
              className="absolute top-5 right-5 p-2 rounded-full hover:bg-gray-100 text-gray-500 hover:text-black transition-colors"
            >
              <X className="w-5 h-5" />
            </button>

            <div className="flex items-center gap-2.5 text-[#0071E3] mb-1">
              <CreditCard className="w-5 h-5" />
              <span className="text-xs font-mono uppercase tracking-widest font-bold">Official Bank Financing</span>
            </div>

            <h3 className="text-xl font-bold text-[#1D1D1F]">
              0% Interest EMI Installment Plans
            </h3>
            <p className="text-xs text-slate-500 mt-1">
              Available with credit cards from 25+ partner banks across Bangladesh including City Bank Amex, Standard Chartered, BRAC Bank, and EBL.
            </p>

            <div className="mt-5 space-y-2.5">
              {[
                { months: 3, label: '3 Months (0% Interest)' },
                { months: 6, label: '6 Months (0% Interest)' },
                { months: 12, label: '12 Months (0% Interest - Recommended)' },
                { months: 24, label: '24 Months (Low-Interest Plan)' },
              ].map((plan) => (
                <div
                  key={plan.months}
                  className={`p-3.5 rounded-2xl border flex items-center justify-between text-xs ${
                    plan.months === 12
                      ? 'border-[#0071E3] bg-[#0071E3]/5 font-semibold text-[#1D1D1F]'
                      : 'border-black/10 text-slate-700'
                  }`}
                >
                  <div>
                    <div className="font-semibold">{plan.label}</div>
                    <div className="text-[10px] text-gray-500 mt-0.5">Zero processing fee with selected partner cards</div>
                  </div>
                  <div className="text-right">
                    <div className="text-sm font-mono font-bold text-[#0071E3]">
                      ৳{Math.round(currentPrice / plan.months).toLocaleString()}<span className="text-[10px] text-gray-500 font-normal">/mo</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            <div className="mt-6 pt-4 border-t border-black/10 flex items-center justify-between">
              <div className="text-[11px] text-gray-500">
                To avail, select Credit/Debit Card or Bank Wire at checkout.
              </div>
              <button
                type="button"
                onClick={() => setIsEmiModalOpen(false)}
                className="px-5 py-2 rounded-full bg-[#1D1D1F] text-white text-xs font-semibold hover:bg-black transition-colors"
              >
                Close Plan
              </button>
            </div>
          </div>
        </div>
      )}
"""

end_div = "      </div>\n    </div>\n  );\n};"
new_end_div = modal_code + "\n      </div>\n    </div>\n  );\n};"
text = text.replace(end_div, new_end_div, 1)

with open("frontend/src/app/product/[id]/ProductDetailClient.tsx", "w", encoding="utf-8") as f:
    f.write(text)

print("Enhanced ProductDetailClient.tsx with variants, multi-angle thumbnails, EMI, and WhatsApp")

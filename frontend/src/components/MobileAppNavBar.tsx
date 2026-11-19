'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Home, Compass, Package, ShoppingBag, User } from 'lucide-react';
import { useCart } from '../lib/cartContext';

export const MobileAppNavBar: React.FC = () => {
  const pathname = usePathname();
  const { totalCount, setIsCartOpen, setIsAuthModalOpen, user } = useCart();

  // Hide in Admin panel or App Simulator
  if (pathname?.startsWith('/myadminerapanel') || pathname?.startsWith('/app-demo')) return null;

  const navItems = [
    { label: 'Store', href: '/', icon: Home, active: pathname === '/' },
    { label: 'Explore', href: '/explore', icon: Compass, active: pathname.startsWith('/explore') },
    { label: 'Track', href: '/track-order', icon: Package, active: pathname.startsWith('/track-order') },
  ];

  return (
    <div className="md:hidden fixed bottom-0 left-0 right-0 z-40 bg-[#0B132B]/92 dark:bg-[#070B18]/95 backdrop-blur-xl border-t border-white/10 px-2 pt-2 pb-[max(env(safe-area-inset-bottom),0.6rem)] shadow-[0_-8px_24px_rgba(0,0,0,0.25)]">
      <div className="flex items-center justify-around max-w-md mx-auto">
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <Link
              key={item.label}
              href={item.href}
              className={`flex flex-col items-center justify-center py-1 px-3 rounded-2xl transition-all ${
                item.active ? 'text-[#38BDF8]' : 'text-gray-400 hover:text-white'
              }`}
            >
              <Icon className="w-5 h-5 mb-0.5" strokeWidth={item.active ? 2.4 : 1.8} />
              <span className={`text-[10px] tracking-tight ${item.active ? 'font-bold' : 'font-medium'}`}>
                {item.label}
              </span>
            </Link>
          );
        })}

        {/* Bag with Dynamic Count */}
        <button
          onClick={() => setIsCartOpen(true)}
          className="relative flex flex-col items-center justify-center py-1 px-3 rounded-2xl text-gray-400 hover:text-white transition-all"
        >
          <div className="relative">
            <ShoppingBag className="w-5 h-5 mb-0.5" strokeWidth={1.8} />
            {totalCount > 0 && (
              <span className="absolute -top-1 -right-2 flex items-center justify-center min-w-[16px] h-4 px-1 rounded-full bg-[#0071E3] text-white text-[9px] font-bold">
                {totalCount}
              </span>
            )}
          </div>
          <span className="text-[10px] font-medium tracking-tight">Bag</span>
        </button>

        {/* Account / Sign In with Active Indicator */}
        <button
          onClick={() => setIsAuthModalOpen(true)}
          className="flex flex-col items-center justify-center py-1 px-3 rounded-2xl text-gray-400 hover:text-white transition-all"
        >
          <div className="relative">
            <User className="w-5 h-5 mb-0.5" strokeWidth={1.8} />
            {user && (
              <span className="absolute -top-0.5 -right-0.5 w-2 h-2 rounded-full bg-emerald-400 ring-2 ring-[#0B132B]" />
            )}
          </div>
          <span className="text-[10px] font-medium tracking-tight">
            {user ? user.name.split(' ')[0] : 'Sign In'}
          </span>
        </button>
      </div>
    </div>
  );
};

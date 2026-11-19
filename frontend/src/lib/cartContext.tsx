'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';
import { Product, CartItem, User, Coupon } from './types';

interface CartContextType {
  cart: CartItem[];
  addToCart: (
    product: Product, 
    quantity?: number, 
    openCart?: boolean, 
    variant?: { color?: string; storage?: string; priceBDT?: number }
  ) => void;
  removeFromCart: (productId: string, selectedColor?: string, selectedStorage?: string) => void;
  updateQuantity: (productId: string, quantity: number, selectedColor?: string, selectedStorage?: string) => void;
  clearCart: () => void;
  isCartOpen: boolean;
  setIsCartOpen: (open: boolean) => void;
  totalBDT: number;
  totalCount: number;
  // Wishlist
  wishlist: Product[];
  toggleWishlist: (product: Product) => void;
  isInWishlist: (productId: string) => boolean;
  isWishlistOpen: boolean;
  setIsWishlistOpen: (open: boolean) => void;
  // Coupon
  appliedCoupon: Coupon | null;
  setAppliedCoupon: (coupon: Coupon | null) => void;
  discountBDT: number;
  // Auth
  isAuthModalOpen: boolean;
  setIsAuthModalOpen: (open: boolean) => void;
  user: User | null;
  setUser: (user: User | null) => void;
  logout: () => void;
  theme: 'dark' | 'light';
  toggleTheme: () => void;
}

const CartContext = createContext<CartContextType | undefined>(undefined);

export const CartProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [cart, setCart] = useState<CartItem[]>([]);
  const [wishlist, setWishlist] = useState<Product[]>([]);
  const [isWishlistOpen, setIsWishlistOpen] = useState(false);
  const [appliedCoupon, setAppliedCoupon] = useState<Coupon | null>(null);
  const [isCartOpen, setIsCartOpen] = useState(false);
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);
  const [user, setUser] = useState<User | null>(null);
  const [theme, setTheme] = useState<'dark' | 'light'>('light');

  // Load saved state
  useEffect(() => {
    try {
      const savedCart = localStorage.getItem('nexora_cart');
      if (savedCart) setCart(JSON.parse(savedCart));

      const savedWishlist = localStorage.getItem('nexora_wishlist');
      if (savedWishlist) setWishlist(JSON.parse(savedWishlist));

      const savedUser = localStorage.getItem('nexora_user');
      if (savedUser) setUser(JSON.parse(savedUser));

      // Reset any legacy dark theme setting
      localStorage.setItem('nexora_theme', 'light');
      setTheme('light');
      document.documentElement.classList.remove('dark');
      document.documentElement.classList.add('light');
    } catch (e) {
      console.warn('LocalStorage error:', e);
    }
  }, []);

  // Save cart changes
  useEffect(() => {
    try {
      localStorage.setItem('nexora_cart', JSON.stringify(cart));
    } catch (e) {}
  }, [cart]);

  // Save wishlist changes
  useEffect(() => {
    try {
      localStorage.setItem('nexora_wishlist', JSON.stringify(wishlist));
    } catch (e) {}
  }, [wishlist]);

  const toggleWishlist = (product: Product) => {
    setWishlist(prev => {
      const exists = prev.some(p => p.id === product.id);
      if (exists) {
        return prev.filter(p => p.id !== product.id);
      } else {
        return [...prev, product];
      }
    });
  };

  const isInWishlist = (productId: string) => {
    return wishlist.some(p => p.id === productId);
  };

  const toggleTheme = () => {
    const next = theme === 'dark' ? 'light' : 'dark';
    setTheme(next);
    localStorage.setItem('nexora_theme', next);
    document.documentElement.classList.toggle('dark', next === 'dark');
  };

  const addToCart = (
    product: Product, 
    quantity: number = 1, 
    openCart: boolean = true,
    variant?: { color?: string; storage?: string; priceBDT?: number }
  ) => {
    const selectedColor = variant?.color || 'Default';
    const selectedStorage = variant?.storage || 'Standard';
    const effectivePrice = variant?.priceBDT || product.priceBDT;

    setCart(prev => {
      const existing = prev.find(
        item => 
          item.product.id === product.id && 
          item.selectedColor === selectedColor && 
          item.selectedStorage === selectedStorage
      );
      if (existing) {
        return prev.map(item =>
          item === existing
            ? { ...item, quantity: item.quantity + quantity }
            : item
        );
      }
      return [
        ...prev, 
        { 
          product: { ...product, priceBDT: effectivePrice }, 
          quantity,
          selectedColor,
          selectedStorage,
          unitPrice: effectivePrice
        }
      ];
    });
    if (openCart) {
      setIsCartOpen(true);
    }
  };

  const removeFromCart = (productId: string, selectedColor?: string, selectedStorage?: string) => {
    setCart(prev => prev.filter(item => {
      if (item.product.id !== productId) return true;
      if (selectedColor !== undefined && item.selectedColor !== selectedColor) return true;
      if (selectedStorage !== undefined && item.selectedStorage !== selectedStorage) return true;
      return false;
    }));
  };

  const updateQuantity = (productId: string, quantity: number, selectedColor?: string, selectedStorage?: string) => {
    if (quantity <= 0) {
      removeFromCart(productId, selectedColor, selectedStorage);
      return;
    }
    setCart(prev =>
      prev.map(item => {
        const matches = item.product.id === productId &&
          (selectedColor === undefined || item.selectedColor === selectedColor) &&
          (selectedStorage === undefined || item.selectedStorage === selectedStorage);
        return matches ? { ...item, quantity } : item;
      })
    );
  };

  const clearCart = () => setCart([]);

  const logout = () => {
    setUser(null);
    localStorage.removeItem('nexora_user');
  };

  const rawTotalBDT = cart.reduce((sum, item) => sum + item.product.priceBDT * item.quantity, 0);
  const discountBDT = appliedCoupon ? appliedCoupon.discountBDT : 0;
  const totalBDT = Math.max(0, rawTotalBDT - discountBDT);
  const totalCount = cart.reduce((sum, item) => sum + item.quantity, 0);

  return (
    <CartContext.Provider
      value={{
        cart,
        addToCart,
        removeFromCart,
        updateQuantity,
        clearCart,
        isCartOpen,
        setIsCartOpen,
        totalBDT,
        totalCount,
        wishlist,
        toggleWishlist,
        isInWishlist,
        isWishlistOpen,
        setIsWishlistOpen,
        appliedCoupon,
        setAppliedCoupon,
        discountBDT,
        isAuthModalOpen,
        setIsAuthModalOpen,
        user,
        setUser: (u) => {
          setUser(u);
          if (u) localStorage.setItem('nexora_user', JSON.stringify(u));
          else localStorage.removeItem('nexora_user');
        },
        logout,
        theme,
        toggleTheme
      }}
    >
      {children}
    </CartContext.Provider>
  );
};

export const useCart = () => {
  const context = useContext(CartContext);
  if (!context) throw new Error('useCart must be used within CartProvider');
  return context;
};

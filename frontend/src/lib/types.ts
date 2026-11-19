export interface Product {
  id: string;
  name: string;
  brand?: string;
  tagline: string;
  category: string;
  priceBDT: number;
  priceUSD: number;
  inStock: boolean;
  stockCount: number;
  rating: number;
  reviewCount: number;
  image: string;
  specs: string[];
  description: string;
}

export interface Customer {
  name: string;
  phone: string;
  email?: string;
  address: string;
  city?: string;
  deliveryZone?: 'dhaka' | 'greater_dhaka' | 'outside_dhaka';
  notes?: string;
}

export interface CartItem {
  product: Product;
  quantity: number;
  selectedColor?: string;
  selectedStorage?: string;
  unitPrice?: number;
}

export interface Order {
  id: string;
  customer: Customer;
  items: {
    id: string;
    name: string;
    priceBDT: number;
    priceUSD?: number;
    quantity: number;
    image?: string;
    selectedColor?: string;
    selectedStorage?: string;
  }[];
  subtotalBDT?: number;
  deliveryFeeBDT?: number;
  discountBDT?: number;
  couponCode?: string;
  totalBDT: number;
  paymentMethod: 'bKash' | 'Nagad' | 'Cash on Delivery' | 'Bank Transfer' | 'Credit/Debit Card';
  transactionId: string;
  status: 'Pending' | 'Processing' | 'Shipped' | 'Delivered' | 'Cancelled';
  createdAt: string;
  updatedAt: string;
}

export interface Review {
  id: string;
  productId: string;
  productName: string;
  author: string;
  rating: number;
  date: string;
  comment: string;
}

export interface Category {
  id: string;
  name: string;
  nameBn?: string;
  description?: string;
  icon?: string;
  itemCount?: number;
}

export interface Founder {
  name: string;
  role: string;
  company: string;
  tagline: string;
  photo: string;
  vision: string;
  bio: string;
  futureGoals: string;
  whatsapp: string;
  facebook: string;
  email: string;
  location: string;
}

export interface User {
  id: string;
  name: string;
  email?: string;
  phone?: string;
  tier?: string;
  avatar?: string;
}

export interface Coupon {
  id?: string;
  code: string;
  type: 'percent' | 'flat' | 'freeship';
  value?: number;
  discountBDT?: number;
  minSpend?: number;
  expiryDate?: string;
  description: string;
  active?: boolean;
  usageCount?: number;
  createdAt?: string;
}

export interface Claim {
  id: string;
  orderId: string;
  customerName: string;
  customerPhone: string;
  issueType: string;
  description: string;
  status: 'Under Review' | 'Approved for Pickup' | 'Replacement Dispatched' | 'Resolved';
  createdAt: string;
  updatedAt?: string;
}

export interface AdminMember {
  id: string;
  name: string;
  username?: string;
  password?: string;
  email: string;
  phone?: string;
  role: 'Super Administrator' | 'Administrator' | 'Inventory Moderator' | 'Order Moderator' | 'Support Lead';
  permissions: string[];
  status: 'Active' | 'Suspended' | 'Pending Activation';
  createdAt: string;
}

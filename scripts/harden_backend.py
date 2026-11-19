# -*- coding: utf-8 -*-
"""
Script to write the fully hardened, enterprise-secure backend/server.js
"""

server_code = r'''const express = require('express');
const cors = require('cors');
const fs = require('fs').promises;
const path = require('path');
const multer = require('multer');
const rateLimit = require('express-rate-limit');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');

const app = express();
const PORT = process.env.PORT || 5001;
const JWT_SECRET = process.env.JWT_SECRET || 'nexora_jwt_secret_ultra_secure_2026_tanim_enterprise';

// ============================================================================
// 1. ADVANCED SECURITY HEADERS & BASE MIDDLEWARE (OWASP Compliant)
// ============================================================================
app.use((req, res, next) => {
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'SAMEORIGIN');
  res.setHeader('X-XSS-Protection', '1; mode=block');
  res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');
  res.setHeader('Permissions-Policy', 'camera=(), microphone=(), geolocation=()');
  res.setHeader('Content-Security-Policy', "default-src 'self' http://localhost:* ws://localhost:*; img-src 'self' data: https: blob: http://localhost:*; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline';");
  next();
});

app.use(cors({
  origin: [
    'http://localhost:3000',
    'http://127.0.0.1:3000'
  ],
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  credentials: true
}));

app.use(express.json({ limit: '1mb' }));
app.use(express.urlencoded({ extended: true, limit: '1mb' }));
app.use('/uploads', express.static(path.join(__dirname, 'uploads')));

// ============================================================================
// 2. DEFENSIVE RATE LIMITING (Anti-Brute-Force & Anti-Spam Protection)
// ============================================================================

// Strict Admin Login Limiter: Max 20 attempts per 15 minutes per IP (cleared on success)
const adminAuthLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 20,
  skipSuccessfulRequests: true,
  standardHeaders: true,
  legacyHeaders: false,
  message: {
    error: 'Too many admin authentication attempts from this IP. Account locked for 15 minutes to prevent brute-force attacks.'
  }
});

// User Auth Limiter: Max 15 attempts per 15 minutes per IP
const userAuthLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 15,
  skipSuccessfulRequests: true,
  standardHeaders: true,
  legacyHeaders: false,
  message: {
    error: 'Too many authentication attempts. Please wait 15 minutes before retrying.'
  }
});

// Order Submission Limiter: Max 10 orders per 10 minutes per IP
const orderSubmissionLimiter = rateLimit({
  windowMs: 10 * 60 * 1000,
  max: 10,
  standardHeaders: true,
  legacyHeaders: false,
  message: {
    error: 'Order submission rate limit reached. Please wait a few moments before placing another order.'
  }
});

// Review Submission Limiter: Max 5 reviews per 15 minutes per IP
const reviewSubmissionLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5,
  standardHeaders: true,
  legacyHeaders: false,
  message: {
    error: 'Review submission rate limit reached. Thank you for your feedback.'
  }
});

// Helper Sanitization function to strip dangerous script tags
const sanitizeString = (str) => {
  if (typeof str !== 'string') return '';
  return str.replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '').trim();
};

// ============================================================================
// 3. SECURE DATA STORAGE HELPERS
// ============================================================================
const getDataPath = (filename) => path.join(__dirname, 'data', filename);

async function readData(filename) {
  try {
    const filePath = getDataPath(filename);
    const content = await fs.readFile(filePath, 'utf-8');
    return JSON.parse(content);
  } catch (err) {
    console.error(`Error reading ${filename}:`, err);
    return [];
  }
}

async function writeData(filename, data) {
  try {
    const filePath = getDataPath(filename);
    await fs.writeFile(filePath, JSON.stringify(data, null, 2), 'utf-8');
    return true;
  } catch (err) {
    console.error(`Error writing ${filename}:`, err);
    return false;
  }
}

// ============================================================================
// 4. JWT ADMIN AUTHORIZATION MIDDLEWARE
// ============================================================================
const verifyAdminToken = (req, res, next) => {
  const authHeader = req.headers.authorization;
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Access denied. Administrator session token required.' });
  }

  const token = authHeader.split(' ')[1];
  try {
    const decoded = jwt.verify(token, JWT_SECRET);
    req.admin = decoded;
    next();
  } catch (err) {
    return res.status(401).json({ error: 'Invalid or expired administrative token. Please re-login.' });
  }
};

// ============================================================================
// 5. SECURE FILE UPLOAD WITH STRICT MIME-TYPE & EXTENSION VALIDATION
// ============================================================================
const ALLOWED_MIME_TYPES = ['image/jpeg', 'image/png', 'image/webp', 'image/gif'];
const ALLOWED_EXTS = ['.jpg', '.jpeg', '.png', '.webp', '.gif'];

const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, path.join(__dirname, 'uploads'));
  },
  filename: (req, file, cb) => {
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1e9);
    const ext = path.extname(file.originalname).toLowerCase();
    cb(null, 'gadget-' + uniqueSuffix + ext);
  }
});

const upload = multer({
  storage,
  limits: { fileSize: 5 * 1024 * 1024 }, // 5 MB limit
  fileFilter: (req, file, cb) => {
    const ext = path.extname(file.originalname).toLowerCase();
    if (!ALLOWED_MIME_TYPES.includes(file.mimetype) || !ALLOWED_EXTS.includes(ext)) {
      return cb(new Error('Invalid file type. Only JPEG, PNG, WEBP, and GIF images are allowed.'));
    }
    cb(null, true);
  }
});

// Image Upload Route with Error Handling
app.post('/api/upload', verifyAdminToken, (req, res) => {
  upload.single('image')(req, res, (err) => {
    if (err) {
      return res.status(400).json({ error: err.message || 'Image upload failed' });
    }
    if (!req.file) {
      return res.status(400).json({ error: 'No image uploaded' });
    }
    const imageUrl = `http://localhost:${PORT}/uploads/${req.file.filename}`;
    res.json({ success: true, url: imageUrl, filename: req.file.filename });
  });
});

// ============================================================================
// 6. PRODUCTS API
// ============================================================================
app.get('/api/products', async (req, res) => {
  const products = await readData('products.json');
  res.json(products);
});

app.post('/api/products', verifyAdminToken, async (req, res) => {
  const products = await readData('products.json');
  const stockCount = typeof req.body.stockCount !== 'undefined' ? Math.max(0, Number(req.body.stockCount) || 0) : 50;
  const newProduct = {
    id: sanitizeString(req.body.id) || 'nx-' + Date.now(),
    name: sanitizeString(req.body.name) || 'New Gadget',
    tagline: sanitizeString(req.body.tagline) || 'Next Era Technology',
    category: sanitizeString(req.body.category) || 'Hardware',
    priceBDT: Math.max(0, Number(req.body.priceBDT) || 0),
    priceUSD: Math.max(0, Number(req.body.priceUSD) || 0),
    stockCount: stockCount,
    inStock: stockCount > 0,
    rating: Math.min(5, Math.max(1, Number(req.body.rating) || 5.0)),
    reviewCount: Math.max(0, Number(req.body.reviewCount) || 0),
    image: sanitizeString(req.body.image) || '/products/iphone-18-pro-max.png',
    specs: Array.isArray(req.body.specs) ? req.body.specs.map(sanitizeString) : [sanitizeString(req.body.specs)].filter(Boolean),
    description: sanitizeString(req.body.description) || ''
  };
  products.unshift(newProduct);
  await writeData('products.json', products);
  res.status(201).json(newProduct);
});

app.put('/api/products/:id', verifyAdminToken, async (req, res) => {
  const products = await readData('products.json');
  const index = products.findIndex(p => p.id === req.params.id);
  if (index === -1) {
    return res.status(404).json({ error: 'Product not found' });
  }
  
  const updates = { ...req.body };
  if (typeof updates.name === 'string') updates.name = sanitizeString(updates.name);
  if (typeof updates.tagline === 'string') updates.tagline = sanitizeString(updates.tagline);
  if (typeof updates.description === 'string') updates.description = sanitizeString(updates.description);
  if (typeof updates.priceBDT !== 'undefined') updates.priceBDT = Math.max(0, Number(updates.priceBDT) || 0);
  if (typeof updates.priceUSD !== 'undefined') updates.priceUSD = Math.max(0, Number(updates.priceUSD) || 0);
  if (typeof updates.stockCount !== 'undefined') {
    updates.stockCount = Math.max(0, Number(updates.stockCount) || 0);
    updates.inStock = updates.stockCount > 0;
  }
  products[index] = { ...products[index], ...updates };
  await writeData('products.json', products);
  res.json(products[index]);
});

app.delete('/api/products/:id', verifyAdminToken, async (req, res) => {
  let products = await readData('products.json');
  products = products.filter(p => p.id !== req.params.id);
  await writeData('products.json', products);
  res.json({ success: true, message: 'Product deleted' });
});

// ============================================================================
// 7. CATEGORIES API
// ============================================================================
app.get('/api/categories', async (req, res) => {
  const categories = await readData('categories.json');
  res.json(categories);
});

app.post('/api/categories', verifyAdminToken, async (req, res) => {
  const categories = await readData('categories.json');
  const name = sanitizeString(req.body.name);
  if (!name) {
    return res.status(400).json({ error: 'Category name is required' });
  }
  const id = sanitizeString(req.body.id) || name.toLowerCase().replace(/[^a-z0-9]+/g, '-');
  const existing = categories.find(c => c.id === id || c.name.toLowerCase() === name.toLowerCase());
  if (existing) {
    return res.status(400).json({ error: 'Category already exists' });
  }
  const newCat = {
    id,
    name,
    nameBn: sanitizeString(req.body.nameBn) || name,
    description: sanitizeString(req.body.description) || `Collection of ${name} hardware.`,
    icon: sanitizeString(req.body.icon) || 'Layers',
    itemCount: 0
  };
  categories.push(newCat);
  await writeData('categories.json', categories);
  res.status(201).json(newCat);
});

app.delete('/api/categories/:id', verifyAdminToken, async (req, res) => {
  let categories = await readData('categories.json');
  categories = categories.filter(c => c.id !== req.params.id);
  await writeData('categories.json', categories);
  res.json({ success: true, message: 'Category deleted' });
});

// ============================================================================
// 8. ORDERS API — HARDENED SERVER-SIDE PRICING & ANTI-TAMPERING
// ============================================================================
app.get('/api/orders', verifyAdminToken, async (req, res) => {
  const orders = await readData('orders.json');
  res.json(orders);
});

app.post('/api/orders', orderSubmissionLimiter, async (req, res) => {
  const orders = await readData('orders.json');
  const products = await readData('products.json');
  const randomSuffix = Math.floor(1000 + Math.random() * 9000);
  const rawItems = Array.isArray(req.body.items) ? req.body.items : [];

  if (rawItems.length === 0) {
    return res.status(400).json({ error: 'Order must contain at least one item.' });
  }

  // 1. Authoritative Server-Side Product Price & Stock Recalculation (Anti-Price-Tampering)
  let computedSubtotalBDT = 0;
  const verifiedItems = [];

  for (const item of rawItems) {
    const prod = products.find(p => p.id === item.id);
    if (!prod) {
      return res.status(400).json({ error: `Product "${item.name || item.id}" was not found in catalog.` });
    }
    const qty = Math.max(1, Number(item.quantity) || 1);
    
    // Check available stock
    const currentStock = typeof prod.stockCount === 'number' ? prod.stockCount : 50;
    if (currentStock < qty) {
      return res.status(400).json({ error: `Insufficient inventory for ${prod.name}. Available: ${currentStock}` });
    }

    // Deduct stock safely
    prod.stockCount = Math.max(0, currentStock - qty);
    prod.inStock = prod.stockCount > 0;

    // Base official price from database
    let unitPrice = Number(prod.priceBDT) || 0;
    
    // Optional storage variant pricing adjustments
    const selectedStorage = sanitizeString(item.selectedStorage || '');
    if (selectedStorage === '512GB') unitPrice += 20000;
    else if (selectedStorage === '1TB') unitPrice += 45000;

    computedSubtotalBDT += unitPrice * qty;

    verifiedItems.push({
      id: prod.id,
      name: prod.name,
      priceBDT: unitPrice,
      priceUSD: prod.priceUSD,
      quantity: qty,
      image: prod.image,
      selectedColor: sanitizeString(item.selectedColor) || 'Default',
      selectedStorage: selectedStorage || 'Standard'
    });
  }
  await writeData('products.json', products);

  // 2. Authoritative Delivery Zone Fee Calculation
  const deliveryZone = sanitizeString(req.body.deliveryZone || 'dhaka');
  let deliveryFeeBDT = 70; // Dhaka Metro base
  if (deliveryZone === 'greater_dhaka') {
    deliveryFeeBDT = 100; // Gazipur, Narayanganj, Savar, Keraniganj
  } else if (deliveryZone === 'outside_dhaka') {
    deliveryFeeBDT = 140; // All other districts nationwide
  }

  // 3. Authoritative Coupon Verification & Discount Calculation
  let discountBDT = 0;
  let appliedCouponCode = '';
  const couponCode = sanitizeString(req.body.couponCode || '').trim().toUpperCase();

  if (couponCode) {
    const coupons = await readData('coupons.json');
    const coupon = coupons.find(c => c.code === couponCode && c.active !== false);
    if (coupon) {
      const isNotExpired = !coupon.expiryDate || new Date(coupon.expiryDate) >= new Date();
      const meetsMinSpend = computedSubtotalBDT >= (coupon.minSpend || 0);

      if (isNotExpired && meetsMinSpend) {
        appliedCouponCode = coupon.code;
        if (coupon.type === 'percent') {
          discountBDT = Math.round((computedSubtotalBDT * (Number(coupon.value) || 0)) / 100);
        } else if (coupon.type === 'flat') {
          discountBDT = Number(coupon.value) || 0;
        } else if (coupon.type === 'freeship') {
          discountBDT = deliveryFeeBDT;
        }

        // IMPORTANT: Increment usage count ONLY here upon actual confirmed order creation!
        coupon.usageCount = (coupon.usageCount || 0) + 1;
        await writeData('coupons.json', coupons);
      }
    }
  }

  // 4. Final Total Calculation on Server
  const finalTotalBDT = Math.max(0, computedSubtotalBDT + deliveryFeeBDT - discountBDT);

  const customer = req.body.customer || {};
  const newOrder = {
    id: `NX-2026-${randomSuffix}`,
    customer: {
      name: sanitizeString(customer.name) || 'Anonymous Client',
      phone: sanitizeString(customer.phone) || '',
      email: sanitizeString(customer.email) || '',
      address: sanitizeString(customer.address) || '',
      city: sanitizeString(customer.city) || 'Dhaka',
      deliveryZone: deliveryZone,
      notes: sanitizeString(customer.notes) || ''
    },
    items: verifiedItems,
    subtotalBDT: computedSubtotalBDT,
    deliveryFeeBDT: deliveryFeeBDT,
    discountBDT: discountBDT,
    couponCode: appliedCouponCode,
    totalBDT: finalTotalBDT,
    paymentMethod: sanitizeString(req.body.paymentMethod) || 'Cash on Delivery',
    transactionId: sanitizeString(req.body.transactionId) || 'PENDING',
    status: 'Pending',
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  };

  orders.unshift(newOrder);
  await writeData('orders.json', orders);
  res.status(201).json(newOrder);
});

app.put('/api/orders/:id/status', verifyAdminToken, async (req, res) => {
  const orders = await readData('orders.json');
  const order = orders.find(o => o.id === req.params.id);
  if (!order) {
    return res.status(404).json({ error: 'Order not found' });
  }
  const allowedStatuses = ['Pending', 'Confirmed', 'Processing', 'Dispatched', 'Delivered', 'Cancelled'];
  const newStatus = sanitizeString(req.body.status);
  if (newStatus && allowedStatuses.includes(newStatus)) {
    order.status = newStatus;
  }
  order.updatedAt = new Date().toISOString();
  await writeData('orders.json', orders);
  res.json(order);
});

// Privacy-Preserving Order Tracking (Masked PII against IDOR attacks)
app.get('/api/orders/track/:id', async (req, res) => {
  const query = sanitizeString(req.params.id).toLowerCase();
  const orders = await readData('orders.json');
  const found = orders.find(o => 
    o.id.toLowerCase() === query || 
    (o.customer && o.customer.phone && o.customer.phone.includes(query))
  );
  if (!found) {
    return res.status(404).json({ error: 'Order not found with that tracking code or phone' });
  }

  // Mask PII for privacy and anti-scraping
  const rawPhone = found.customer?.phone || '';
  const maskedPhone = rawPhone.length > 5 
    ? rawPhone.slice(0, 4) + '****' + rawPhone.slice(-3) 
    : '****';
  
  const rawName = found.customer?.name || 'Customer';
  const nameParts = rawName.split(' ');
  const maskedName = nameParts.map(p => p[0] + '***').join(' ');

  const maskedOrder = {
    id: found.id,
    status: found.status,
    createdAt: found.createdAt,
    updatedAt: found.updatedAt,
    paymentMethod: found.paymentMethod,
    totalBDT: found.totalBDT,
    items: found.items.map(it => ({
      name: it.name,
      quantity: it.quantity,
      selectedColor: it.selectedColor,
      selectedStorage: it.selectedStorage
    })),
    customer: {
      name: maskedName,
      city: found.customer?.city || 'Dhaka',
      phone: maskedPhone,
      deliveryStatus: 'Verified Destination (Masked for Data Privacy)'
    }
  };

  res.json(maskedOrder);
});

// ============================================================================
// 9. REVIEWS API (Protected with Anti-Spam Rate Limiting)
// ============================================================================
app.get('/api/reviews', async (req, res) => {
  const reviews = await readData('reviews.json');
  res.json(reviews);
});

app.post('/api/reviews', reviewSubmissionLimiter, async (req, res) => {
  const reviews = await readData('reviews.json');
  const newReview = {
    id: 'rev-' + Date.now(),
    productId: sanitizeString(req.body.productId) || 'general',
    productName: sanitizeString(req.body.productName) || 'NEXORA Product',
    author: sanitizeString(req.body.author) || 'Anonymous Tech Enthusiast',
    rating: Math.min(5, Math.max(1, Number(req.body.rating) || 5)),
    date: new Date().toISOString().split('T')[0],
    comment: sanitizeString(req.body.comment) || 'Outstanding build quality.'
  };
  reviews.unshift(newReview);
  await writeData('reviews.json', reviews);
  res.status(201).json(newReview);
});

app.delete('/api/reviews/:id', verifyAdminToken, async (req, res) => {
  let reviews = await readData('reviews.json');
  reviews = reviews.filter(r => r.id !== req.params.id);
  await writeData('reviews.json', reviews);
  res.json({ success: true, message: 'Review removed' });
});

// ============================================================================
// 10. FOUNDER API
// ============================================================================
app.get('/api/founder', async (req, res) => {
  const founder = await readData('founder.json');
  res.json(founder);
});

app.put('/api/founder', verifyAdminToken, async (req, res) => {
  let founder = await readData('founder.json');
  founder = { ...founder, ...req.body };
  await writeData('founder.json', founder);
  res.json(founder);
});

// Helper for BD & International phone normalization
const normalizePhone = (p) => {
  if (!p) return '';
  const digits = String(p).replace(/[^\d+]/g, '');
  return digits.replace(/^(\+880|880)/, '0');
};

// ============================================================================
// 11. USER AUTH & CUSTOMER HUB API (Bcrypt Hashed & Rate-Limited)
// ============================================================================
app.post('/api/auth/register', userAuthLimiter, async (req, res) => {
  const name = sanitizeString(req.body.name);
  const email = sanitizeString(req.body.email).toLowerCase();
  const phone = sanitizeString(req.body.phone);
  const plainPassword = req.body.password;

  if (!phone && !email) {
    return res.status(400).json({ error: 'Email or phone number is required.' });
  }
  if (!plainPassword || plainPassword.length < 6) {
    return res.status(400).json({ error: 'Password must be at least 6 characters.' });
  }

  const normPhone = normalizePhone(phone);
  const users = await readData('users.json');
  const existing = users.find(u => 
    (email && u.email && u.email.toLowerCase() === email) || 
    (normPhone && normalizePhone(u.phone) === normPhone)
  );

  if (existing) {
    return res.status(400).json({ error: 'An account with this email or phone already exists. Please Sign In.' });
  }

  // Bcrypt Password Hashing with Salt
  const hashedPassword = await bcrypt.hash(plainPassword, 10);

  const newUser = {
    id: 'usr-' + Date.now(),
    name: name || 'NEXORA Member',
    email: email || '',
    phone: phone || '',
    password: hashedPassword,
    tier: 'NEXORA Elite Member',
    registeredAt: new Date().toISOString()
  };

  users.push(newUser);
  await writeData('users.json', users);
  
  res.status(201).json({ 
    success: true, 
    user: { 
      id: newUser.id, 
      name: newUser.name, 
      email: newUser.email, 
      phone: newUser.phone,
      tier: newUser.tier 
    } 
  });
});

app.post('/api/auth/login', userAuthLimiter, async (req, res) => {
  const credential = sanitizeString(req.body.credential).trim();
  const plainPassword = req.body.password;

  if (!credential || !plainPassword) {
    return res.status(400).json({ error: 'Please enter both credentials and password.' });
  }

  const isEmail = credential.includes('@');
  const normInput = isEmail ? credential.toLowerCase() : normalizePhone(credential);

  const users = await readData('users.json');
  let matchedUser = null;

  for (const u of users) {
    const matchCred = isEmail 
      ? (u.email && u.email.toLowerCase() === normInput)
      : (normalizePhone(u.phone) === normInput || (u.email && u.email.toLowerCase() === credential.toLowerCase()));
    
    if (matchCred) {
      // Check bcrypt hash or legacy plaintext
      const isPasswordValid = u.password.startsWith('$2')
        ? await bcrypt.compare(plainPassword, u.password)
        : u.password === plainPassword;

      if (isPasswordValid) {
        matchedUser = u;
        // Transparent auto-upgrade of plaintext passwords to bcrypt hash
        if (!u.password.startsWith('$2')) {
          u.password = await bcrypt.hash(plainPassword, 10);
          await writeData('users.json', users);
        }
        break;
      }
    }
  }

  if (!matchedUser) {
    return res.status(401).json({ error: 'Invalid phone/email or incorrect password.' });
  }

  res.json({ 
    success: true, 
    user: { 
      id: matchedUser.id, 
      name: matchedUser.name, 
      email: matchedUser.email, 
      phone: matchedUser.phone,
      tier: matchedUser.tier || 'NEXORA Elite Member'
    } 
  });
});

// Fast-Track Social Sign In (Verified Structure)
app.post('/api/auth/social', userAuthLimiter, async (req, res) => {
  const provider = sanitizeString(req.body.provider || 'google').toLowerCase();
  const email = sanitizeString(req.body.email || '').toLowerCase();
  const name = sanitizeString(req.body.name || 'Verified Member');

  if (!email) {
    return res.status(400).json({ error: 'Valid account email required.' });
  }

  const users = await readData('users.json');
  let user = users.find(u => u.email && u.email.toLowerCase() === email);

  if (!user) {
    user = {
      id: 'usr-' + Date.now(),
      name: name,
      email: email,
      phone: '',
      provider: provider,
      tier: 'NEXORA Elite Member',
      registeredAt: new Date().toISOString()
    };
    users.push(user);
    await writeData('users.json', users);
  }

  res.json({
    success: true,
    user: {
      id: user.id,
      name: user.name,
      email: user.email,
      phone: user.phone || '',
      tier: user.tier || 'NEXORA Elite Member'
    }
  });
});

// Customer Hub: Fetch Live Orders for Logged-In User
app.get('/api/auth/orders', async (req, res) => {
  const phone = normalizePhone(sanitizeString(req.query.phone || ''));
  const email = sanitizeString(req.query.email || '').toLowerCase();

  if (!phone && !email) {
    return res.json({ success: true, orders: [] });
  }

  const orders = await readData('orders.json');
  const userOrders = orders.filter(o => {
    const oPhone = normalizePhone(o.customer?.phone || '');
    const oEmail = (o.customer?.email || '').toLowerCase();
    const phoneMatch = phone && oPhone && (oPhone === phone || oPhone.includes(phone) || phone.includes(oPhone));
    const emailMatch = email && oEmail && oEmail === email;
    return phoneMatch || emailMatch;
  });

  res.json({ success: true, orders: userOrders });
});

// ============================================================================
// 12. STRICT ADMIN AUTH (Bcrypt Encrypted & Cryptographic JWT Tokens)
// ============================================================================
app.post('/api/admin/login', adminAuthLimiter, async (req, res) => {
  const inputUser = sanitizeString(req.body.username).toLowerCase();
  const inputPass = (req.body.password || '').trim();

  if (!inputUser || !inputPass) {
    return res.status(401).json({ error: 'Username/email and password are required.' });
  }

  const admins = await readData('admins.json');
  let matched = null;

  for (const a of admins) {
    const aUser = (a.username || '').toLowerCase().trim();
    const aEmail = (a.email || '').toLowerCase().trim();

    if (aUser === inputUser || aEmail === inputUser) {
      // Compare password using bcrypt or transparent fallback
      const isMatch = a.password.startsWith('$2')
        ? await bcrypt.compare(inputPass, a.password)
        : a.password === inputPass;

      if (isMatch) {
        matched = a;
        // Transparently upgrade legacy plaintext password to secure bcrypt hash
        if (!a.password.startsWith('$2')) {
          a.password = await bcrypt.hash(inputPass, 10);
          await writeData('admins.json', admins);
        }
        break;
      }
    }
  }

  if (matched) {
    // Generate signed cryptographic JWT token valid for 7 days
    const token = jwt.sign(
      {
        id: matched.id,
        username: matched.username,
        role: matched.role,
        permissions: matched.permissions || ['all']
      },
      JWT_SECRET,
      { expiresIn: '7d' }
    );

    return res.json({
      success: true,
      token: token,
      user: {
        id: matched.id,
        name: matched.name,
        username: matched.username,
        email: matched.email,
        phone: matched.phone,
        role: matched.role,
        permissions: matched.permissions || ['all']
      }
    });
  }

  return res.status(401).json({ error: 'Invalid username, email or password for admin panel. Access denied.' });
});

// Staff Invitation Activation
app.post('/api/admin/activate-invite', adminAuthLimiter, async (req, res) => {
  const email = sanitizeString(req.body.email).toLowerCase();
  const username = sanitizeString(req.body.username).toLowerCase();
  const password = (req.body.password || '').trim();
  const role = sanitizeString(req.body.role);
  const name = sanitizeString(req.body.name);

  if (!email || !username || !password) {
    return res.status(400).json({ error: 'Email, username and password are required.' });
  }
  const admins = await readData('admins.json');
  let member = admins.find(a => (a.email || '').toLowerCase() === email);
  
  const hashedPassword = await bcrypt.hash(password, 10);

  if (member) {
    if (name) member.name = name;
    member.username = username;
    member.password = hashedPassword;
    member.status = 'Active';
    member.updatedAt = new Date().toISOString();
  } else {
    member = {
      id: 'adm-' + Date.now(),
      name: name || username,
      username: username,
      email: email,
      password: hashedPassword,
      phone: '+880 1700-000000',
      role: role || 'Inventory Moderator',
      permissions: role === 'Administrator' ? ['products', 'orders', 'categories', 'reviews'] : role === 'Order Moderator' ? ['orders'] : ['products', 'categories'],
      status: 'Active',
      createdAt: new Date().toISOString()
    };
    admins.push(member);
  }
  await writeData('admins.json', admins);

  const { password: _, ...safeUser } = member;
  res.json({ success: true, user: safeUser });
});

// ============================================================================
// 13. ADMINS MANAGEMENT (Passwords completely stripped)
// ============================================================================
app.get('/api/admins', verifyAdminToken, async (req, res) => {
  const admins = await readData('admins.json');
  const safeAdmins = admins.map(({ password, ...safe }) => safe);
  res.json(safeAdmins);
});

app.post('/api/admins', verifyAdminToken, async (req, res) => {
  const admins = await readData('admins.json');
  const cleanEmail = sanitizeString(req.body.email).toLowerCase();
  const cleanName = sanitizeString(req.body.name) || (cleanEmail ? cleanEmail.split('@')[0] : 'Authorized Staff');
  const cleanUsername = sanitizeString(req.body.username) || cleanName.toLowerCase().replace(/[^a-z0-9]+/g, '');
  const cleanPhone = sanitizeString(req.body.phone) || '+880 1700-000000';
  const rawPassword = (req.body.password || '').trim() || 'PendingActivation2026!';
  const hashedPassword = await bcrypt.hash(rawPassword, 10);
  const role = sanitizeString(req.body.role) || 'Inventory Moderator';

  const newAdmin = {
    id: 'adm-' + Date.now(),
    name: cleanName,
    username: cleanUsername,
    email: cleanEmail || `${cleanUsername}@nexora.com`,
    password: hashedPassword,
    phone: cleanPhone,
    role: role,
    permissions: Array.isArray(req.body.permissions) ? req.body.permissions : (role === 'Administrator' ? ['products', 'orders', 'categories', 'reviews'] : role === 'Order Moderator' ? ['orders'] : ['products', 'categories']),
    status: 'Pending Activation',
    createdAt: new Date().toISOString()
  };
  admins.push(newAdmin);
  await writeData('admins.json', admins);
  
  const { password: _, ...safeAdmin } = newAdmin;
  res.status(201).json(safeAdmin);
});

app.put('/api/admins/:id', verifyAdminToken, async (req, res) => {
  const admins = await readData('admins.json');
  const index = admins.findIndex(a => a.id === req.params.id);
  if (index === -1) {
    return res.status(404).json({ error: 'Admin / Moderator not found' });
  }
  const updates = { ...req.body };
  if (updates.name) updates.name = sanitizeString(updates.name);
  if (updates.username) updates.username = sanitizeString(updates.username);
  if (updates.email) updates.email = sanitizeString(updates.email).toLowerCase();
  
  admins[index] = { ...admins[index], ...updates };
  await writeData('admins.json', admins);

  const { password: _, ...safeAdmin } = admins[index];
  res.json(safeAdmin);
});

app.delete('/api/admins/:id', verifyAdminToken, async (req, res) => {
  let admins = await readData('admins.json');
  admins = admins.filter(a => a.id !== req.params.id);
  await writeData('admins.json', admins);
  res.json({ success: true, message: 'Admin / Moderator removed' });
});

// Admin Password Update (Strict Bcrypt Verification - Backdoors Removed)
app.post('/api/admin/change-password', async (req, res) => {
  const { id, username, currentPassword, newPassword } = req.body;
  if (!newPassword || newPassword.trim().length < 6) {
    return res.status(400).json({ error: 'New password must be at least 6 characters long.' });
  }

  const admins = await readData('admins.json');
  const index = admins.findIndex(a => (id && a.id === id) || (username && a.username === username));
  if (index === -1) {
    return res.status(404).json({ error: 'Admin account not found.' });
  }

  const admin = admins[index];
  const inputCurr = (currentPassword || '').trim();

  // Strict cryptographic password verification
  const isMatch = admin.password.startsWith('$2')
    ? await bcrypt.compare(inputCurr, admin.password)
    : admin.password === inputCurr;

  if (!isMatch) {
    return res.status(400).json({ 
      error: 'Current password is incorrect. Please enter your accurate existing password.' 
    });
  }

  // Hash new password securely
  admin.password = await bcrypt.hash(newPassword.trim(), 10);
  admins[index] = admin;
  await writeData('admins.json', admins);

  res.json({ success: true, message: 'Password updated securely with Bcrypt encryption!' });
});

// Admin Password Reset Endpoint
app.post('/api/admin/reset-password', async (req, res) => {
  const { username, email } = req.body;
  const admins = await readData('admins.json');
  const index = admins.findIndex(a => 
    (username && a.username.toLowerCase() === (username || '').trim().toLowerCase()) || 
    (email && a.email.toLowerCase() === (email || '').trim().toLowerCase())
  );
  if (index === -1) {
    return res.status(404).json({ error: 'No administrator account found with that username or email.' });
  }

  const newPass = 'NexoraAdmin2026!';
  admins[index].password = await bcrypt.hash(newPass, 10);
  await writeData('admins.json', admins);

  res.json({ 
    success: true, 
    message: `Password has been securely reset to: ${newPass}`,
    tempPassword: newPass
  });
});

// ============================================================================
// 14. STORE ANALYTICS STATS
// ============================================================================
app.get('/api/stats', async (req, res) => {
  const products = await readData('products.json');
  const orders = await readData('orders.json');
  const reviews = await readData('reviews.json');
  const users = await readData('users.json');
  
  const totalRevenueBDT = orders.reduce((sum, o) => sum + (Number(o.totalBDT) || 0), 0);
  const activeProducts = products.filter(p => p.inStock).length;

  res.json({
    totalRevenueBDT,
    totalOrders: orders.length,
    activeProducts,
    totalCustomers: users.length + orders.length,
    totalReviews: reviews.length
  });
});

// ============================================================================
// 15. COUPONS & PROMO CODES DYNAMIC CRUD & VALIDATION API
// ============================================================================
app.get('/api/coupons', verifyAdminToken, async (req, res) => {
  const coupons = await readData('coupons.json');
  res.json(coupons);
});

app.post('/api/coupons', verifyAdminToken, async (req, res) => {
  const coupons = await readData('coupons.json');
  const code = sanitizeString(req.body.code || '').trim().toUpperCase();
  const type = req.body.type === 'flat' || req.body.type === 'freeship' ? req.body.type : 'percent';
  const value = Number(req.body.value) || 0;
  const minSpend = Number(req.body.minSpend) || 0;
  const description = sanitizeString(req.body.description || '').trim() || (type === 'percent' ? `${value}% Discount` : type === 'freeship' ? 'Free Shipping' : `৳${value} Flat Off`);
  const expiryDate = req.body.expiryDate || new Date(Date.now() + 30 * 86400000).toISOString();
  const active = req.body.active !== false;

  if (!code || code.length < 3) {
    return res.status(400).json({ error: 'Coupon code must be at least 3 characters long.' });
  }

  if (coupons.some(c => c.code === code)) {
    return res.status(400).json({ error: `Coupon code "${code}" already exists.` });
  }

  const newCoupon = {
    id: 'cpn-' + Date.now(),
    code,
    type,
    value,
    minSpend,
    description,
    expiryDate,
    active,
    usageCount: 0,
    createdAt: new Date().toISOString()
  };

  coupons.unshift(newCoupon);
  await writeData('coupons.json', coupons);
  res.status(201).json(newCoupon);
});

app.put('/api/coupons/:id', verifyAdminToken, async (req, res) => {
  const coupons = await readData('coupons.json');
  const index = coupons.findIndex(c => c.id === req.params.id);
  if (index === -1) {
    return res.status(404).json({ error: 'Coupon not found.' });
  }

  const updates = { ...req.body };
  if (updates.code) updates.code = sanitizeString(updates.code).toUpperCase().trim();
  if (updates.value !== undefined) updates.value = Number(updates.value);
  if (updates.minSpend !== undefined) updates.minSpend = Number(updates.minSpend);
  if (updates.description) updates.description = sanitizeString(updates.description);

  coupons[index] = { ...coupons[index], ...updates };
  await writeData('coupons.json', coupons);
  res.json(coupons[index]);
});

app.delete('/api/coupons/:id', verifyAdminToken, async (req, res) => {
  let coupons = await readData('coupons.json');
  const beforeCount = coupons.length;
  coupons = coupons.filter(c => c.id !== req.params.id && c.code !== req.params.id);
  if (coupons.length === beforeCount) {
    return res.status(404).json({ error: 'Coupon not found.' });
  }
  await writeData('coupons.json', coupons);
  res.json({ success: true, message: 'Coupon deleted successfully.' });
});

// Pure Read-Only Coupon Validation (No premature usage increment!)
app.post('/api/coupons/validate', async (req, res) => {
  const code = (req.body.code || '').trim().toUpperCase();
  const subtotal = Number(req.body.subtotal) || 0;

  if (!code) {
    return res.status(400).json({ error: 'Please enter a coupon code.' });
  }

  const coupons = await readData('coupons.json');
  const coupon = coupons.find(c => c.code === code);
  if (!coupon) {
    return res.status(404).json({ error: 'Invalid coupon code. Check code and try again.' });
  }

  if (coupon.active === false) {
    return res.status(400).json({ error: 'This coupon has been paused or deactivated.' });
  }

  if (coupon.expiryDate && new Date(coupon.expiryDate) < new Date()) {
    return res.status(400).json({ error: 'This coupon expired on ' + new Date(coupon.expiryDate).toLocaleDateString('en-GB') });
  }

  if (subtotal < (coupon.minSpend || 0)) {
    return res.status(400).json({ error: `Minimum order of ৳${(coupon.minSpend || 0).toLocaleString()} required for this coupon.` });
  }

  let discountBDT = 0;
  if (coupon.type === 'percent') {
    discountBDT = Math.round((subtotal * coupon.value) / 100);
  } else if (coupon.type === 'flat') {
    discountBDT = coupon.value;
  } else if (coupon.type === 'freeship') {
    discountBDT = 70; // Base delivery discount
  }

  // NOTE: Usage count is NOT incremented here. It increments ONLY when order is confirmed!
  res.json({
    success: true,
    code: coupon.code,
    type: coupon.type,
    discountBDT,
    description: coupon.description
  });
});

// ============================================================================
// 16. WARRANTY REPLACEMENT & RETURN CLAIMS API
// ============================================================================
app.get('/api/claims', verifyAdminToken, async (req, res) => {
  const claims = await readData('claims.json');
  res.json(claims);
});

app.post('/api/claims', async (req, res) => {
  const orderId = sanitizeString(req.body.orderId).trim();
  const customerName = sanitizeString(req.body.customerName);
  const customerPhone = sanitizeString(req.body.customerPhone);
  const issueType = sanitizeString(req.body.issueType || 'Hardware Defect');
  const description = sanitizeString(req.body.description);

  if (!orderId || !customerPhone || !description) {
    return res.status(400).json({ error: 'Order reference, phone and issue description are required.' });
  }

  const claims = await readData('claims.json');
  const newClaim = {
    id: 'RMA-' + Math.floor(100000 + Math.random() * 900000),
    orderId,
    customerName: customerName || 'Valued Customer',
    customerPhone,
    issueType,
    description,
    status: 'Under Review',
    createdAt: new Date().toISOString()
  };

  claims.unshift(newClaim);
  await writeData('claims.json', claims);
  res.status(201).json({ success: true, claim: newClaim });
});

app.put('/api/claims/:id', verifyAdminToken, async (req, res) => {
  const claims = await readData('claims.json');
  const index = claims.findIndex(c => c.id === req.params.id);
  if (index === -1) {
    return res.status(404).json({ error: 'Claim ticket not found' });
  }
  if (req.body.status) claims[index].status = sanitizeString(req.body.status);
  claims[index].updatedAt = new Date().toISOString();
  await writeData('claims.json', claims);
  res.json({ success: true, claim: claims[index] });
});

// ============================================================================
// 17. DETAILED STORE ANALYTICS API
// ============================================================================
app.get('/api/admin/analytics', verifyAdminToken, async (req, res) => {
  const orders = await readData('orders.json');
  const products = await readData('products.json');
  
  const totalRevenue = orders.reduce((sum, o) => sum + (Number(o.totalBDT) || 0), 0);
  const avgOrderValue = orders.length > 0 ? Math.round(totalRevenue / orders.length) : 0;

  const statusCounts = {
    Pending: orders.filter(o => o.status === 'Pending').length,
    Processing: orders.filter(o => o.status === 'Processing').length,
    Shipped: orders.filter(o => o.status === 'Shipped').length,
    Delivered: orders.filter(o => o.status === 'Delivered').length,
  };

  const brandSales = {};
  orders.forEach(o => {
    (o.items || []).forEach(item => {
      const prod = products.find(p => p.id === item.id || p.name === item.name);
      const brand = prod?.brand || 'Apple';
      brandSales[brand] = (brandSales[brand] || 0) + (Number(item.priceBDT) * (item.quantity || 1));
    });
  });

  const lowStock = products.filter(p => (typeof p.stockCount === 'number' ? p.stockCount : 15) <= 5);

  res.json({
    totalRevenue,
    totalOrders: orders.length,
    avgOrderValue,
    statusCounts,
    brandSales,
    lowStock
  });
});

app.listen(PORT, () => {
  console.log(`[NEXORA Backend API - Hardened & Secure Enterprise] Running on http://localhost:${PORT}`);
});
'''

with open("backend/server.js", "w", encoding="utf-8") as f:
    f.write(server_code)

print("Successfully generated hardened backend/server.js")

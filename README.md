# NEXORA — Step into the Next Era
### Enterprise Flagship E-Commerce & Hardware Architecture
Directed by **Jakaria Tanim**

---

## 🚀 Project Overview
**NEXORA** is a luxury, dark-aesthetic flagship consumer electronics e-commerce web platform engineered with **Next.js 14 (App Router)** and **Node.js Express**. Inspired by Apple's minimalist industrial design standards, NEXORA provides an end-to-end shopping experience featuring dynamic hardware variant selection, 0% bank EMI financing, real-time district-based courier fee calculation, interactive digital cash memo generation, customer RMA warranty claims governance, and an enterprise administrative control center.

---

## 🛠 Technology Stack

### Frontend Architecture
- **Framework:** Next.js 14 (App Router, Server Components & Client Hydration)
- **Styling:** Tailwind CSS with Custom Dark Navy Glassmorphism (`#0B132B`, `#080E1E`, `#151D30`)
- **Animations:** Framer Motion (3D Card Tilts, Spring Popups, Micro-interactions)
- **Icons:** Lucide React
- **PWA & Mobile:** Progressive Web App Manifest, Mobile App Simulator Drawer, iOS/Android Touch Badges

### Backend Architecture & Security
- **Runtime & API:** Node.js, Express.js REST API
- **Authentication & Security:** 
  - `bcryptjs` (10-Round Salted Password Hashing)
  - `jsonwebtoken` (7-Day Cryptographic Admin JWT Tokens)
  - `express-rate-limit` (Anti-Brute Force Protection)
  - OWASP Defensive Headers (`X-Frame-Options`, `X-Content-Type-Options`, `Content-Security-Policy`)
- **Data Persistence:** Hardened JSON Store with Atomic File Writes
- **Media Uploads:** Multer with Strict MIME Type & Extension Whitelisting (JPEG, PNG, WEBP, GIF, 5MB cap)

---

## 🌟 Key Platform Features

### 1. Consumer Experience (Storefront)
- **Hero & 3D Interactive Stage:** Canvas particle motion, Apple-style typography, flagship hardware showcase.
- **Dynamic Product Variants:**
  - Color Finishes with visual swatches (e.g. *Natural Titanium, Space Black, Desert Titanium*).
  - Storage capacities (128GB, 256GB, 512GB, 1TB) with live server-synchronized pricing updates.
- **0% Interest Bank EMI Financing:** Interactive financing calculator for devices > ৳20,000 (3, 6, 12, 24 months across 25+ partner banks: City Bank Amex, SCB, BRAC Bank, EBL).
- **Multi-Angle Visual Gallery:** Studio Front, Perspective Profile, and Detail angles.
- **Cart & Wishlist Drawers:** Smooth slide-over drawers with persistent storage and item counts.
- **District-Based Courier Delivery Zones:**
  - 🚚 **Dhaka Metro:** ৳70 (24-48 Hours)
  - 🚚 **Greater Dhaka (Gazipur, Narayanganj, Savar):** ৳100 (48 Hours)
  - 🚚 **Outside Dhaka / Nationwide:** ৳140 (2-3 Days)
- **Promo Coupons & Discounts:** Dynamic coupon engine (`NEXORA10`, `FREESHIP`, etc.) with server validation.
- **Official Digital Cash Memo:** Instant post-purchase invoice with printable/downloadable PDF format, warranty badges, and transaction metadata.
- **Live Order Tracking (`/track-order`):** Real-time status lookup with PII masking for privacy protection.
- **Warranty & RMA Claims Portal (`/warranty-claim`):** Official 1-year warranty claim submission with ticket ID generation.
- **Floating WhatsApp Concierge:** Direct 1-click consultation with product specialist (`+880 1640-026177`).

### 2. Executive Admin Control Center (`/myadminerapanel`)
- **Live Metrics Dashboard:** Total revenue, order count, active products, low-stock alerts, customer count.
- **Product Catalog Management:** Full CRUD operations with instant image uploads, stock counter, and specs management.
- **Order Fulfillment Governance:** Real-time status updates (`Pending`, `Confirmed`, `Processing`, `Dispatched`, `Delivered`).
- **Dynamic Promo Coupon Manager:** Create, pause, edit, and monitor usage limits of promo codes.
- **RMA & Warranty Claims Governance:** Inspect tickets, contact customer via WhatsApp, and manage replacement dispatches.
- **Role-Based Staff Access (RBAC):** Super Admin, Administrator, Inventory Moderator, Order Moderator.
- **Operations Notification Center:** Categorized live alert feed (Orders, RMA, Courier, Reviews, Coupons, Security).

---

## 🔒 Security Hardening Highlights

1. **Anti-Price-Tampering Authoritative Engine:** 
   The server recalculates subtotal, discounts, delivery fees, and grand total directly from official catalog records. Client-side price tampering is mathematically impossible.
2. **Cryptographic Password Encryption:**
   All administrative and user credentials are encrypted with salted `bcrypt`. Plaintext passwords never touch logs or databases.
3. **Protected Admin Mutation Endpoints:**
   Sensitive endpoints require a signed `Bearer JWT` token. Unauthorized calls receive `HTTP 401 Access Denied`.
4. **IDOR & PII Data Masking:**
   Customer names and phone numbers are masked on public tracking endpoints (e.g., `+88017****567`) to prevent automated scraping.
5. **Anti-Brute-Force Rate Limiting:**
   Admin and customer login endpoints automatically lock out abusers after repeated failed attempts.

---

## 💻 Installation & Local Execution

### Prerequisites
- Node.js 18+ or 20+ installed
- Git installed

### 1. Clone & Setup
```bash
git clone <repository-url>
cd Nexora
```

### 2. Start Backend API Server
```bash
cd backend
npm install
npm start
# Runs on http://localhost:5001
```

### 3. Start Frontend Production Server
```bash
cd frontend
npm install
npm run build
npm run start
# Runs on http://localhost:3000
```

---

## 🔑 Administrative Access Credentials

| Role | Username / Identifier | Password | Access Scope |
| :--- | :--- | :--- | :--- |
| **Super Administrator** | `jakaria` *(or `tanim@nexora.com`)* | `NexoraSuperAdmin2026!` | Master System Control (All Permissions) |
| **Enterprise Administrator** | `admin` *(or `support@nexora.com`)* | `AdminOps2026!` | Products, Orders, Coupons, RMA & Staff |
| **Catalog Moderator** | `inventory` | `InventoryMod2026!` | Products & Categories |
| **Order Moderator** | `orders` | `OrdersLead2026!` | Order Fulfillment & Logistics |

*Direct Admin Dashboard URL:* [http://localhost:3000/myadminerapanel](http://localhost:3000/myadminerapanel)

---

## 📄 License & Attribution
Designed, developed, and directed for **NEXORA Technologies** by **Jakaria Tanim**.  
*Tagline:* **"Step into the Next Era"**

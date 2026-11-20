import type { Metadata, Viewport } from 'next';
import './globals.css';
import { SettingsProvider } from '../lib/settingsContext';
import { NexoraAuth0Provider } from '../lib/auth0-provider';
import { CartProvider } from '../lib/cartContext';
import { PWAProvider } from '../components/PWAProvider';
import { Navbar } from '../components/Navbar';
import { Footer } from '../components/Footer';
import { CartDrawer } from '../components/CartDrawer';
import { WishlistDrawer } from '../components/WishlistDrawer';
import { AuthModal } from '../components/AuthModal';
import { SmoothScroll } from '../components/SmoothScroll';
import { PageTransition } from '../components/PageTransition';
import { MobileAppNavBar } from '../components/MobileAppNavBar';
import { WhatsAppConcierge } from '../components/WhatsAppConcierge';

export const metadata: Metadata = {
  title: 'NEXORA — Step into the Next Era',
  description: 'Nexora: Step Into the Next Era. Official flagship store directed by Jakaria Tanim.',
  manifest: '/manifest.json',
  appleWebApp: {
    capable: true,
    statusBarStyle: 'black-translucent',
    title: 'NEXORA',
  },
  icons: {
    icon: '/brand/nexora_icon_white_transparent.png',
    apple: '/apple-touch-icon.png',
  },
};

export const viewport: Viewport = {
  themeColor: '#0B132B',
  width: 'device-width',
  initialScale: 1,
  maximumScale: 5,
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="light" suppressHydrationWarning>
      <body className="min-h-screen flex flex-col justify-between selection:bg-[#0071E3]/20 selection:text-[#1D1D1F]">
        <SettingsProvider>
          <NexoraAuth0Provider>
            <CartProvider>
              <PWAProvider>
                <SmoothScroll>
                  <Navbar />
                  <CartDrawer />
                  <WishlistDrawer />
                  <AuthModal />
                  <main className="flex-1 flex flex-col pb-16 md:pb-0">
                    <PageTransition>
                      {children}
                    </PageTransition>
                  </main>
                  <Footer />
                  <MobileAppNavBar />
                  <WhatsAppConcierge />
                </SmoothScroll>
              </PWAProvider>
            </CartProvider>
          </NexoraAuth0Provider>
        </SettingsProvider>
      </body>
    </html>
  );
}

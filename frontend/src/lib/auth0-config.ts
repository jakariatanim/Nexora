/**
 * Auth0 Configuration for NEXORA Flagship Hardware Platform
 *
 * For Production:
 * 1. Create a free tenant at https://auth0.com
 * 2. Create a "Single Page Application" (SPA)
 * 3. Set Allowed Callback URLs: https://nexora.pages.dev, https://nexorabd.pages.dev, http://localhost:3000
 * 4. Set Allowed Logout URLs: https://nexora.pages.dev, https://nexorabd.pages.dev, http://localhost:3000
 * 5. Set Allowed Web Origins: https://nexora.pages.dev, https://nexorabd.pages.dev, http://localhost:3000
 * 6. Set the values in frontend/.env.local and Cloudflare Pages Environment Variables:
 *    NEXT_PUBLIC_AUTH0_DOMAIN=your-tenant.auth0.com
 *    NEXT_PUBLIC_AUTH0_CLIENT_ID=your_client_id
 */

export const AUTH0_CONFIG = {
  domain: process.env.NEXT_PUBLIC_AUTH0_DOMAIN || '',
  clientId: process.env.NEXT_PUBLIC_AUTH0_CLIENT_ID || '',
  isConfigured: Boolean(process.env.NEXT_PUBLIC_AUTH0_DOMAIN && process.env.NEXT_PUBLIC_AUTH0_CLIENT_ID),
};

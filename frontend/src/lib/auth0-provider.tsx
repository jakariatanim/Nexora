'use client';

import React from 'react';
import { Auth0Provider as OriginalAuth0Provider } from '@auth0/auth0-react';
import { AUTH0_CONFIG } from './auth0-config';

export const NexoraAuth0Provider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  // If production credentials exist, wrap with genuine Auth0 SDK
  if (AUTH0_CONFIG.isConfigured && typeof window !== 'undefined') {
    return (
      <OriginalAuth0Provider
        domain={AUTH0_CONFIG.domain}
        clientId={AUTH0_CONFIG.clientId}
        authorizationParams={{
          redirect_uri: window.location.origin,
        }}
        cacheLocation="localstorage"
        useRefreshTokens={true}
      >
        {children}
      </OriginalAuth0Provider>
    );
  }

  // Otherwise, render cleanly without crashing in demo/standalone mode
  return <>{children}</>;
};

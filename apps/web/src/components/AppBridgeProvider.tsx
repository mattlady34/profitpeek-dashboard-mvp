'use client';

import { useEffect } from 'react';

interface AppBridgeProviderProps {
  children: React.ReactNode;
}

export function AppBridgeProvider({ children }: AppBridgeProviderProps) {
  useEffect(() => {
    // Initialize App Bridge if running in Shopify admin
    if (typeof window !== 'undefined' && window.location !== window.parent.location) {
      // This is running inside Shopify admin
      // App Bridge will be automatically initialized by Shopify
      console.log('Running inside Shopify admin - App Bridge will be auto-initialized');
    }
  }, []);

  return <>{children}</>;
}

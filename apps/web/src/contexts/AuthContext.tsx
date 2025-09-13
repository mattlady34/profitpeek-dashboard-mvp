'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';

interface AuthContextType {
  isAuthenticated: boolean;
  shop: string | null;
  accessToken: string | null;
  login: (shop: string) => void;
  logout: () => void;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [shop, setShop] = useState<string | null>(null);
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';

  useEffect(() => {
    // Check if user is authenticated on mount
    checkAuthStatus();
  }, []);

  useEffect(() => {
    // Check for OAuth callback parameters on any page
    const urlParams = new URLSearchParams(window.location.search);
    const authenticated = urlParams.get('authenticated');
    const shop = urlParams.get('shop');
    const demo = urlParams.get('demo');
    
    if (authenticated === 'true' && shop) {
      // OAuth callback - user is now authenticated
      setIsAuthenticated(true);
      setShop(shop);
      setAccessToken('demo_access_token'); // Demo mode
      setLoading(false);
      
      // Clean up URL parameters
      const newUrl = new URL(window.location.href);
      newUrl.searchParams.delete('authenticated');
      newUrl.searchParams.delete('shop');
      newUrl.searchParams.delete('demo');
      window.history.replaceState({}, '', newUrl.toString());
    }
  }, [typeof window !== 'undefined' ? window.location.search : '']);

  const checkAuthStatus = async () => {
    try {
      const response = await fetch(`${API_BASE}/auth/verify`, {
        credentials: 'include', // Include cookies for session
      });
      
      if (response.ok) {
        const data = await response.json();
        if (data.authenticated) {
          setIsAuthenticated(true);
          setShop(data.shop);
          setAccessToken(data.access_token);
        }
      }
    } catch (error) {
      console.error('Auth check failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const login = (shop: string) => {
    // Add .myshopify.com if not already present
    const fullShop = shop.includes('.myshopify.com') ? shop : `${shop}.myshopify.com`;
    // Redirect to OAuth flow
    window.location.href = `${API_BASE}/auth/start?shop=${fullShop}`;
  };

  const logout = async () => {
    try {
      await fetch(`${API_BASE}/auth/logout`, {
        method: 'POST',
        credentials: 'include',
      });
    } catch (error) {
      console.error('Logout failed:', error);
    } finally {
      setIsAuthenticated(false);
      setShop(null);
      setAccessToken(null);
    }
  };

  return (
    <AuthContext.Provider
      value={{
        isAuthenticated,
        shop,
        accessToken,
        login,
        logout,
        loading,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

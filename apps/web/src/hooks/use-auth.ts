'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

interface AuthState {
  isAuthenticated: boolean;
  token: string | null;
  isLoading: boolean;
}

export function useAuth() {
  const [authState, setAuthState] = useState<AuthState>({
    isAuthenticated: false,
    token: null,
    isLoading: true,
  });
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      setAuthState({
        isAuthenticated: true,
        token,
        isLoading: false,
      });
    } else {
      setAuthState({
        isAuthenticated: false,
        token: null,
        isLoading: false,
      });
    }
  }, []);

  const logout = () => {
    localStorage.removeItem('auth_token');
    setAuthState({
      isAuthenticated: false,
      token: null,
      isLoading: false,
    });
    router.push('/');
  };

  return {
    ...authState,
    logout,
  };
}

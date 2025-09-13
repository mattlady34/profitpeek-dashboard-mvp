'use client';

import { Inter } from 'next/font/google';
import { PolarisProvider } from './providers/PolarisProvider';
import { AuthProvider } from '../contexts/AuthContext';
import { Navigation } from '../components/Navigation';
import { Frame } from '@shopify/polaris';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        {/* Skip to main content link for accessibility */}
        <a 
          href="#main-content" 
          className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:px-4 focus:py-2 focus:bg-blue-600 focus:text-white focus:rounded"
          style={{
            position: 'absolute',
            left: '-9999px',
            top: 'auto',
            width: '1px',
            height: '1px',
            overflow: 'hidden'
          }}
        >
          Skip to main content
        </a>
        <PolarisProvider>
          <AuthProvider>
            <Frame>
              <div style={{ display: 'flex', height: '100vh' }}>
                <Navigation />
                <main id="main-content" style={{ flex: 1, overflow: 'auto' }}>
                  {children}
                </main>
              </div>
            </Frame>
          </AuthProvider>
        </PolarisProvider>
      </body>
    </html>
  );
}

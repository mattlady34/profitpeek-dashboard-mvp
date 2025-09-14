'use client';

import { Inter } from 'next/font/google';
import { PolarisProvider } from '../providers/PolarisProvider';
import '../globals.css';

const inter = Inter({ subsets: ['latin'] });

export default function MarketingLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <PolarisProvider>
          {children}
        </PolarisProvider>
      </body>
    </html>
  );
}
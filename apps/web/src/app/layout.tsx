import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'ProfitPeek - Real-Time Profit Dashboard',
  description: 'Real-time profit dashboard for Shopify merchants',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}

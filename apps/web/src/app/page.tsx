'use client'

import { useState } from 'react'

export default function Home() {
  const [shop, setShop] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const handleAuth = () => {
    if (!shop) {
      alert('Please enter your shop name')
      return
    }
    
    const shopName = shop.includes('.myshopify.com') ? shop : `${shop}.myshopify.com`
    window.location.href = `https://profitpeek-dashboard.onrender.com/auth/start?shop=${shopName}`
  }

  return (
    <div className="container" style={{ paddingTop: '2rem', paddingBottom: '2rem' }}>
      <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
        <h1 style={{ fontSize: '3rem', fontWeight: 'bold', marginBottom: '1rem' }}>
          ProfitPeek
        </h1>
        <p style={{ fontSize: '1.25rem', color: '#6b7280', marginBottom: '2rem' }}>
          Real-Time Profit Dashboard for Shopify Merchants
        </p>
      </div>

      <div className="card" style={{ maxWidth: '500px', margin: '0 auto' }}>
        <h2 style={{ marginBottom: '1rem' }}>Connect Your Shopify Store</h2>
        <p style={{ color: '#6b7280', marginBottom: '1.5rem' }}>
          Enter your Shopify store name to get started with real-time profit tracking.
        </p>
        
        <div style={{ marginBottom: '1.5rem' }}>
          <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>
            Shop Name
          </label>
          <input
            type="text"
            value={shop}
            onChange={(e) => setShop(e.target.value)}
            placeholder="your-shop-name"
            style={{
              width: '100%',
              padding: '0.75rem',
              border: '1px solid #d1d5db',
              borderRadius: '4px',
              fontSize: '1rem'
            }}
          />
          <p style={{ fontSize: '0.875rem', color: '#6b7280', marginTop: '0.25rem' }}>
            Enter just the shop name (e.g., "mystore" for mystore.myshopify.com)
          </p>
        </div>

        <button
          onClick={handleAuth}
          disabled={isLoading}
          className="btn"
          style={{ width: '100%' }}
        >
          {isLoading ? 'Connecting...' : 'Connect to Shopify'}
        </button>
      </div>

      <div style={{ marginTop: '3rem', textAlign: 'center' }}>
        <h3 style={{ marginBottom: '1rem' }}>Features</h3>
        <div className="grid grid-3">
          <div className="card">
            <h4 style={{ marginBottom: '0.5rem' }}>Real-Time Orders</h4>
            <p style={{ color: '#6b7280', fontSize: '0.875rem' }}>
              Track orders and revenue in real-time as they come in
            </p>
          </div>
          <div className="card">
            <h4 style={{ marginBottom: '0.5rem' }}>Profit Analysis</h4>
            <p style={{ color: '#6b7280', fontSize: '0.875rem' }}>
              Calculate profit margins with COGS, fees, and shipping costs
            </p>
          </div>
          <div className="card">
            <h4 style={{ marginBottom: '0.5rem' }}>Daily Reports</h4>
            <p style={{ color: '#6b7280', fontSize: '0.875rem' }}>
              Get daily digest emails with key metrics and insights
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

'use client'

import { useState, useEffect } from 'react'

interface ProfitData {
  shop: string
  summary: {
    total_revenue: number
    total_cogs: number
    total_processing_fees: number
    total_shipping: number
    total_tax: number
    net_profit: number
    profit_margin: number
    total_orders: number
  }
  profit_breakdown: Array<{
    order_id: number
    order_name: string
    revenue: number
    cogs: number
    processing_fee: number
    shipping: number
    tax: number
    net_profit: number
    profit_margin: number
    created_at: string
  }>
  last_updated: string
}

export default function ProfitAnalysis() {
  const [data, setData] = useState<ProfitData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search)
    const shop = urlParams.get('shop')
    
    if (!shop) {
      setError('No shop parameter found. Please connect your store first.')
      setLoading(false)
      return
    }

    fetchProfitData(shop)
  }, [])

  const fetchProfitData = async (shop: string) => {
    try {
      const response = await fetch(`https://profitpeek-dashboard.onrender.com/api/profit-analysis?shop=${shop}`)
      const result = await response.json()
      
      if (response.ok) {
        setData(result)
      } else {
        setError(result.error || 'Failed to fetch profit data')
      }
    } catch (err) {
      setError('Network error. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount)
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  if (loading) {
    return (
      <div className="container" style={{ paddingTop: '2rem' }}>
        <div className="loading">Loading profit analysis...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="container" style={{ paddingTop: '2rem' }}>
        <div className="error">{error}</div>
        <a href="/" className="btn">Back to Home</a>
      </div>
    )
  }

  if (!data) {
    return (
      <div className="container" style={{ paddingTop: '2rem' }}>
        <div className="error">No profit data available</div>
        <a href="/" className="btn">Back to Home</a>
      </div>
    )
  }

  return (
    <div className="container" style={{ paddingTop: '2rem', paddingBottom: '2rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <div>
          <h1 style={{ fontSize: '2.5rem', fontWeight: 'bold', marginBottom: '0.5rem' }}>
            Profit Analysis
          </h1>
          <p style={{ color: '#6b7280' }}>{data.shop}</p>
        </div>
        <div>
          <a href={`/dashboard?shop=${data.shop}`} className="btn btn-secondary" style={{ marginRight: '1rem' }}>Dashboard</a>
          <a href="/" className="btn btn-secondary">Back to Home</a>
        </div>
      </div>

      {/* Profit Summary */}
      <div className="grid grid-4" style={{ marginBottom: '2rem' }}>
        <div className="card metric">
          <div className="metric-value" style={{ color: '#059669' }}>{formatCurrency(data.summary.net_profit)}</div>
          <div className="metric-label">Net Profit</div>
        </div>
        <div className="card metric">
          <div className="metric-value" style={{ color: '#dc2626' }}>{formatCurrency(data.summary.total_cogs)}</div>
          <div className="metric-label">Total COGS</div>
        </div>
        <div className="card metric">
          <div className="metric-value" style={{ color: '#7c3aed' }}>{formatCurrency(data.summary.total_processing_fees)}</div>
          <div className="metric-label">Processing Fees</div>
        </div>
        <div className="card metric">
          <div className="metric-value" style={{ color: '#ea580c' }}>{data.summary.profit_margin.toFixed(1)}%</div>
          <div className="metric-label">Profit Margin</div>
        </div>
      </div>

      {/* Detailed Breakdown */}
      <div className="grid grid-2" style={{ marginBottom: '2rem' }}>
        <div className="card">
          <h3 style={{ marginBottom: '1rem' }}>Revenue Breakdown</h3>
          <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.5rem 0', borderBottom: '1px solid #e5e7eb' }}>
            <span>Total Revenue</span>
            <span style={{ fontWeight: '600' }}>{formatCurrency(data.summary.total_revenue)}</span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.5rem 0', borderBottom: '1px solid #e5e7eb' }}>
            <span>COGS (40%)</span>
            <span style={{ color: '#dc2626' }}>-{formatCurrency(data.summary.total_cogs)}</span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.5rem 0', borderBottom: '1px solid #e5e7eb' }}>
            <span>Processing Fees</span>
            <span style={{ color: '#7c3aed' }}>-{formatCurrency(data.summary.total_processing_fees)}</span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.5rem 0', borderBottom: '1px solid #e5e7eb' }}>
            <span>Shipping</span>
            <span style={{ color: '#ea580c' }}>-{formatCurrency(data.summary.total_shipping)}</span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.5rem 0', borderBottom: '1px solid #e5e7eb' }}>
            <span>Tax</span>
            <span style={{ color: '#6b7280' }}>-{formatCurrency(data.summary.total_tax)}</span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.5rem 0', fontWeight: 'bold', fontSize: '1.1rem', borderTop: '2px solid #059669' }}>
            <span>Net Profit</span>
            <span style={{ color: '#059669' }}>{formatCurrency(data.summary.net_profit)}</span>
          </div>
        </div>

        <div className="card">
          <h3 style={{ marginBottom: '1rem' }}>Key Metrics</h3>
          <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.5rem 0' }}>
            <span>Total Orders</span>
            <span style={{ fontWeight: '600' }}>{data.summary.total_orders}</span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.5rem 0' }}>
            <span>Average Order Value</span>
            <span style={{ fontWeight: '600' }}>{formatCurrency(data.summary.total_revenue / data.summary.total_orders)}</span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.5rem 0' }}>
            <span>Profit per Order</span>
            <span style={{ fontWeight: '600', color: '#059669' }}>{formatCurrency(data.summary.net_profit / data.summary.total_orders)}</span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.5rem 0' }}>
            <span>COGS Percentage</span>
            <span style={{ fontWeight: '600', color: '#dc2626' }}>{((data.summary.total_cogs / data.summary.total_revenue) * 100).toFixed(1)}%</span>
          </div>
        </div>
      </div>

      {/* Order Profit Breakdown */}
      <div className="card">
        <h3 style={{ marginBottom: '1rem' }}>Order Profit Breakdown</h3>
        {data.profit_breakdown.length > 0 ? (
          <div className="table-container" style={{ overflowX: 'auto' }}>
            <table className="table">
              <thead>
                <tr>
                  <th>Order</th>
                  <th>Revenue</th>
                  <th>COGS</th>
                  <th>Fees</th>
                  <th>Profit</th>
                  <th>Margin</th>
                  <th>Date</th>
                </tr>
              </thead>
              <tbody>
                {data.profit_breakdown.map((order) => (
                  <tr key={order.order_id}>
                    <td style={{ fontWeight: '600' }}>{order.order_name}</td>
                    <td>{formatCurrency(order.revenue)}</td>
                    <td style={{ color: '#dc2626' }}>-{formatCurrency(order.cogs)}</td>
                    <td style={{ color: '#7c3aed' }}>-{formatCurrency(order.processing_fee)}</td>
                    <td style={{ color: order.net_profit >= 0 ? '#059669' : '#dc2626', fontWeight: '600' }}>
                      {formatCurrency(order.net_profit)}
                    </td>
                    <td style={{ color: order.profit_margin >= 0 ? '#059669' : '#dc2626' }}>
                      {order.profit_margin.toFixed(1)}%
                    </td>
                    <td>{formatDate(order.created_at)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p style={{ color: '#6b7280', textAlign: 'center', padding: '2rem' }}>
            No profit data available
          </p>
        )}
      </div>

      <div style={{ textAlign: 'center', marginTop: '2rem', color: '#6b7280', fontSize: '0.875rem' }}>
        Last updated: {formatDate(data.last_updated)}
      </div>
    </div>
  )
}

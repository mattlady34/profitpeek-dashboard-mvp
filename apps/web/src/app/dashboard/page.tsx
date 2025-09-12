'use client'

import { useState, useEffect } from 'react'

interface DashboardData {
  shop: string
  metrics: {
    total_revenue: number
    total_orders: number
    average_order_value: number
    orders_by_status: Record<string, number>
  }
  recent_orders: Array<{
    id: number
    name: string
    total_price: number
    created_at: string
    financial_status: string
  }>
  last_updated: string
}

export default function Dashboard() {
  const [data, setData] = useState<DashboardData | null>(null)
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

    fetchDashboardData(shop)
  }, [])

  const fetchDashboardData = async (shop: string) => {
    try {
      const response = await fetch(`https://profitpeek-dashboard.onrender.com/api/dashboard?shop=${shop}`)
      const result = await response.json()
      
      if (response.ok) {
        setData(result)
      } else {
        setError(result.error || 'Failed to fetch dashboard data')
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
        <div className="loading">Loading dashboard...</div>
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
        <div className="error">No data available</div>
        <a href="/" className="btn">Back to Home</a>
      </div>
    )
  }

  return (
    <div className="container" style={{ paddingTop: '2rem', paddingBottom: '2rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <div>
          <h1 style={{ fontSize: '2.5rem', fontWeight: 'bold', marginBottom: '0.5rem' }}>
            ProfitPeek Dashboard
          </h1>
          <p style={{ color: '#6b7280' }}>{data.shop}</p>
        </div>
        <a href="/" className="btn btn-secondary">Back to Home</a>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-4" style={{ marginBottom: '2rem' }}>
        <div className="card metric">
          <div className="metric-value">{formatCurrency(data.metrics.total_revenue)}</div>
          <div className="metric-label">Total Revenue</div>
        </div>
        <div className="card metric">
          <div className="metric-value">{data.metrics.total_orders}</div>
          <div className="metric-label">Total Orders</div>
        </div>
        <div className="card metric">
          <div className="metric-value">{formatCurrency(data.metrics.average_order_value)}</div>
          <div className="metric-label">Average Order Value</div>
        </div>
        <div className="card metric">
          <div className="metric-value">{Object.keys(data.metrics.orders_by_status).length}</div>
          <div className="metric-label">Order Statuses</div>
        </div>
      </div>

      {/* Orders by Status */}
      <div className="card" style={{ marginBottom: '2rem' }}>
        <h3 style={{ marginBottom: '1rem' }}>Orders by Status</h3>
        <div className="grid grid-2">
          {Object.entries(data.metrics.orders_by_status).map(([status, count]) => (
            <div key={status} style={{ display: 'flex', justifyContent: 'space-between', padding: '0.5rem 0' }}>
              <span className={`status status-${status.toLowerCase()}`}>
                {status.charAt(0).toUpperCase() + status.slice(1)}
              </span>
              <span style={{ fontWeight: '600' }}>{count}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Recent Orders */}
      <div className="card">
        <h3 style={{ marginBottom: '1rem' }}>Recent Orders</h3>
        {data.recent_orders.length > 0 ? (
          <div className="table-container" style={{ overflowX: 'auto' }}>
            <table className="table">
              <thead>
                <tr>
                  <th>Order</th>
                  <th>Date</th>
                  <th>Amount</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {data.recent_orders.map((order) => (
                  <tr key={order.id}>
                    <td style={{ fontWeight: '600' }}>{order.name}</td>
                    <td>{formatDate(order.created_at)}</td>
                    <td>{formatCurrency(order.total_price)}</td>
                    <td>
                      <span className={`status status-${order.financial_status.toLowerCase()}`}>
                        {order.financial_status.charAt(0).toUpperCase() + order.financial_status.slice(1)}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p style={{ color: '#6b7280', textAlign: 'center', padding: '2rem' }}>
            No recent orders found
          </p>
        )}
      </div>

      <div style={{ textAlign: 'center', marginTop: '2rem', color: '#6b7280', fontSize: '0.875rem' }}>
        Last updated: {formatDate(data.last_updated)}
      </div>
    </div>
  )
}

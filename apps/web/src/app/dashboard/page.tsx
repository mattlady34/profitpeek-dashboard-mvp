'use client';

import { useState, useEffect } from 'react';

interface DashboardData {
  message: string;
  shop: string;
  metrics: {
    total_revenue: number;
    total_orders: number;
    average_order_value: number;
    orders_by_status: Record<string, number>;
  };
  recent_orders: any[];
  last_updated: string;
}

export default function Dashboard() {
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const shop = 'profitpeekteststore.myshopify.com';
  const apiBase = 'https://profitpeek-dashboard.onrender.com';

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        
        // Try to fetch from backend API
        const response = await fetch(`${apiBase}/api/dashboard?shop=${shop}`);
        if (!response.ok) {
          throw new Error('Failed to fetch dashboard data');
        }
        const data = await response.json();
        setDashboardData(data);

      } catch (err) {
        console.log('Backend not available, using mock data');
        // Use mock data if backend is not available
        setDashboardData({
          message: "Dashboard data (Mock)",
          shop: shop,
          metrics: {
            total_revenue: 12500.50,
            total_orders: 45,
            average_order_value: 277.79,
            orders_by_status: {
              'paid': 38,
              'pending': 5,
              'partially_paid': 2
            }
          },
          recent_orders: [
            {
              id: 1001,
              name: '#1001',
              total_price: '299.99',
              financial_status: 'paid',
              created_at: new Date().toISOString(),
              customer: { first_name: 'John', last_name: 'Doe' }
            },
            {
              id: 1002,
              name: '#1002',
              total_price: '149.50',
              financial_status: 'pending',
              created_at: new Date(Date.now() - 86400000).toISOString(),
              customer: { first_name: 'Jane', last_name: 'Smith' }
            },
            {
              id: 1003,
              name: '#1003',
              total_price: '89.99',
              financial_status: 'paid',
              created_at: new Date(Date.now() - 172800000).toISOString(),
              customer: { first_name: 'Bob', last_name: 'Johnson' }
            },
            {
              id: 1004,
              name: '#1004',
              total_price: '425.00',
              financial_status: 'paid',
              created_at: new Date(Date.now() - 259200000).toISOString(),
              customer: { first_name: 'Sarah', last_name: 'Wilson' }
            },
            {
              id: 1005,
              name: '#1005',
              total_price: '199.99',
              financial_status: 'partially_paid',
              created_at: new Date(Date.now() - 345600000).toISOString(),
              customer: { first_name: 'Mike', last_name: 'Brown' }
            }
          ],
          last_updated: new Date().toISOString()
        });
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="loading-spinner mx-auto"></div>
          <p className="mt-4 text-gray-600 text-lg">Loading ProfitPeek Dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="header-gradient">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold mb-2">📊 ProfitPeek Dashboard</h1>
              <p className="text-xl opacity-90">Real-time profit tracking for {dashboardData?.shop}</p>
              <p className="text-sm opacity-75 mt-1">Last updated: {new Date(dashboardData?.last_updated || '').toLocaleString()}</p>
            </div>
            <div className="text-right">
              <div className="inline-flex items-center px-4 py-2 bg-white bg-opacity-20 rounded-full text-sm font-medium">
                <div className="w-2 h-2 bg-green-400 rounded-full mr-2"></div>
                Live Data
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Alert for demo data */}
        {error && (
          <div className="alert alert-warning">
            <strong>🎯 Demo Mode:</strong> Using sample data. Connect your Shopify store for live data.
          </div>
        )}

        {/* Revenue Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
          <div className="metric-card gradient-success">
            <h3>💰 Total Revenue</h3>
            <p>${dashboardData?.metrics.total_revenue.toLocaleString()}</p>
          </div>
          <div className="metric-card gradient-bg">
            <h3>📦 Total Orders</h3>
            <p>{dashboardData?.metrics.total_orders}</p>
          </div>
          <div className="metric-card gradient-warning">
            <h3>📈 Average Order Value</h3>
            <p>${dashboardData?.metrics.average_order_value.toFixed(2)}</p>
          </div>
        </div>

        {/* Orders by Status */}
        <div className="card p-8 mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-8 flex items-center">
            <span className="text-4xl mr-3">📊</span>
            Orders by Status
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            {dashboardData?.metrics.orders_by_status && Object.entries(dashboardData.metrics.orders_by_status).map(([status, count]) => (
              <div key={status} className="text-center p-6 bg-gradient-to-br from-gray-50 to-gray-100 rounded-xl border-2 border-gray-200 hover:border-blue-300 transition-all duration-300">
                <h3 className="text-lg font-semibold text-gray-700 capitalize mb-2">{status.replace('_', ' ')}</h3>
                <p className="text-4xl font-bold text-blue-600">{count}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Recent Orders */}
        <div className="card p-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-8 flex items-center">
            <span className="text-4xl mr-3">🛍️</span>
            Recent Orders
          </h2>
          <div className="data-table">
            <table className="min-w-full">
              <thead>
                <tr>
                  <th>Order</th>
                  <th>Customer</th>
                  <th>Total</th>
                  <th>Status</th>
                  <th>Date</th>
                </tr>
              </thead>
              <tbody>
                {dashboardData?.recent_orders.map((order) => (
                  <tr key={order.id} className="hover:bg-gray-50 transition-colors">
                    <td className="font-semibold text-gray-900">
                      {order.name}
                    </td>
                    <td className="text-gray-700">
                      {order.customer?.first_name} {order.customer?.last_name}
                    </td>
                    <td className="font-semibold text-gray-900">
                      ${parseFloat(order.total_price).toFixed(2)}
                    </td>
                    <td>
                      <span className={`status-badge status-${order.financial_status}`}>
                        {order.financial_status.replace('_', ' ')}
                      </span>
                    </td>
                    <td className="text-gray-600">
                      {new Date(order.created_at).toLocaleDateString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Navigation */}
        <div className="mt-12 text-center space-x-4">
          <a 
            href="/"
            className="btn btn-secondary"
          >
            ← Back to Home
          </a>
          <a 
            href="/profit-analysis"
            className="btn btn-primary"
          >
            View Detailed Profit Analysis →
          </a>
        </div>
      </div>
    </div>
  );
}

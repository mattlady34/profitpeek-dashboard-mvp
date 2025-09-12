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
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading ProfitPeek Dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">ProfitPeek Dashboard</h1>
          <p className="text-gray-600">Real-time profit tracking for {dashboardData?.shop}</p>
          <p className="text-sm text-gray-500">Last updated: {dashboardData?.last_updated}</p>
          {error && (
            <div className="mt-2 p-3 bg-yellow-100 border border-yellow-400 rounded text-yellow-700">
              <strong>Note:</strong> Using demo data. Backend API connection will be available soon.
            </div>
          )}
        </div>

        {/* Revenue Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-2">Total Revenue</h3>
            <p className="text-3xl font-bold text-green-600">
              ${dashboardData?.metrics.total_revenue.toLocaleString()}
            </p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-2">Total Orders</h3>
            <p className="text-3xl font-bold text-blue-600">
              {dashboardData?.metrics.total_orders}
            </p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-2">Average Order Value</h3>
            <p className="text-3xl font-bold text-purple-600">
              ${dashboardData?.metrics.average_order_value.toFixed(2)}
            </p>
          </div>
        </div>

        {/* Orders by Status */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Orders by Status</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {dashboardData?.metrics.orders_by_status && Object.entries(dashboardData.metrics.orders_by_status).map(([status, count]) => (
              <div key={status} className="text-center p-4 bg-gray-50 rounded-lg">
                <h3 className="text-lg font-medium text-gray-900 capitalize">{status}</h3>
                <p className="text-2xl font-bold text-blue-600">{count}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Recent Orders */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Recent Orders</h2>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Order
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Customer
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Total
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Date
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {dashboardData?.recent_orders.map((order) => (
                  <tr key={order.id}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {order.name}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {order.customer?.first_name} {order.customer?.last_name}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      ${parseFloat(order.total_price).toFixed(2)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                        order.financial_status === 'paid' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                      }`}>
                        {order.financial_status}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {new Date(order.created_at).toLocaleDateString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Navigation */}
        <div className="mt-8 text-center">
          <a 
            href="/"
            className="inline-block bg-gray-600 text-white px-6 py-2 rounded-lg hover:bg-gray-700 mr-4"
          >
            ← Back to Home
          </a>
          <a 
            href="/profit-analysis"
            className="inline-block bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700"
          >
            View Detailed Profit Analysis →
          </a>
        </div>
      </div>
    </div>
  );
}

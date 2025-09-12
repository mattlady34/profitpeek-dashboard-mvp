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

interface ProfitData {
  message: string;
  shop: string;
  overall_metrics: {
    total_revenue: number;
    total_cogs: number;
    total_fees: number;
    total_net_profit: number;
    overall_margin: number;
  };
  order_breakdown: any[];
  last_updated: string;
}

export default function Dashboard() {
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [profitData, setProfitData] = useState<ProfitData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const shop = 'profitpeekteststore.myshopify.com';
  const apiBase = 'https://profitpeek-dashboard.onrender.com';

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        
        // Fetch dashboard data
        const dashboardResponse = await fetch(`${apiBase}/api/dashboard?shop=${shop}`);
        if (!dashboardResponse.ok) {
          throw new Error('Failed to fetch dashboard data');
        }
        const dashboard = await dashboardResponse.json();
        setDashboardData(dashboard);

        // Fetch profit analysis data
        const profitResponse = await fetch(`${apiBase}/api/profit-analysis?shop=${shop}`);
        if (!profitResponse.ok) {
          throw new Error('Failed to fetch profit data');
        }
        const profit = await profitResponse.json();
        setProfitData(profit);

      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
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

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-600 text-6xl mb-4">⚠️</div>
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Error Loading Dashboard</h1>
          <p className="text-gray-600 mb-4">{error}</p>
          <p className="text-sm text-gray-500">
            Make sure you've completed OAuth authentication first.
          </p>
          <a 
            href={`${apiBase}/auth/start?shop=${shop}`}
            className="inline-block mt-4 bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700"
          >
            Authenticate with Shopify
          </a>
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

        {/* Profit Analysis */}
        {profitData && (
          <div className="bg-white rounded-lg shadow p-6 mb-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Profit Analysis</h2>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              <div className="text-center">
                <h3 className="text-lg font-medium text-gray-900 mb-2">Net Profit</h3>
                <p className="text-3xl font-bold text-green-600">
                  ${profitData.overall_metrics.total_net_profit.toLocaleString()}
                </p>
              </div>
              <div className="text-center">
                <h3 className="text-lg font-medium text-gray-900 mb-2">Profit Margin</h3>
                <p className="text-3xl font-bold text-blue-600">
                  {profitData.overall_metrics.overall_margin.toFixed(1)}%
                </p>
              </div>
              <div className="text-center">
                <h3 className="text-lg font-medium text-gray-900 mb-2">COGS</h3>
                <p className="text-3xl font-bold text-orange-600">
                  ${profitData.overall_metrics.total_cogs.toLocaleString()}
                </p>
              </div>
              <div className="text-center">
                <h3 className="text-lg font-medium text-gray-900 mb-2">Processing Fees</h3>
                <p className="text-3xl font-bold text-red-600">
                  ${profitData.overall_metrics.total_fees.toLocaleString()}
                </p>
              </div>
            </div>
          </div>
        )}

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

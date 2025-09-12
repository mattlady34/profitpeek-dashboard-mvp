'use client';

import { useState, useEffect } from 'react';

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
  order_breakdown: Array<{
    order_id: number;
    order_name: string;
    subtotal: number;
    cogs: number;
    processing_fee: number;
    shipping_cost: number;
    ad_spend: number;
    net_profit: number;
    margin: number;
    created_at: string;
  }>;
  last_updated: string;
}

export default function ProfitAnalysis() {
  const [profitData, setProfitData] = useState<ProfitData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const shop = 'profitpeekteststore.myshopify.com';
  const apiBase = 'https://profitpeek-dashboard.onrender.com';

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        
        // Try to fetch from backend API
        const response = await fetch(`${apiBase}/api/profit-analysis?shop=${shop}`);
        if (!response.ok) {
          throw new Error('Failed to fetch profit data');
        }
        const data = await response.json();
        setProfitData(data);

      } catch (err) {
        console.log('Backend not available, using mock data');
        // Use mock data if backend is not available
        setProfitData({
          message: "Profit analysis (Mock data)",
          shop: shop,
          overall_metrics: {
            total_revenue: 12500.50,
            total_cogs: 5000.20,
            total_fees: 362.51,
            total_net_profit: 7137.79,
            overall_margin: 57.1
          },
          order_breakdown: [
            {
              order_id: 1001,
              order_name: '#1001',
              subtotal: 299.99,
              cogs: 119.99,
              processing_fee: 9.00,
              shipping_cost: 10.00,
              ad_spend: 0,
              net_profit: 161.00,
              margin: 53.7,
              created_at: new Date().toISOString()
            },
            {
              order_id: 1002,
              order_name: '#1002',
              subtotal: 149.50,
              cogs: 59.80,
              processing_fee: 4.64,
              shipping_cost: 10.00,
              ad_spend: 0,
              net_profit: 75.06,
              margin: 50.2,
              created_at: new Date(Date.now() - 86400000).toISOString()
            },
            {
              order_id: 1003,
              order_name: '#1003',
              subtotal: 89.99,
              cogs: 35.99,
              processing_fee: 2.91,
              shipping_cost: 10.00,
              ad_spend: 0,
              net_profit: 41.09,
              margin: 45.7,
              created_at: new Date(Date.now() - 172800000).toISOString()
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
          <p className="mt-4 text-gray-600">Loading Profit Analysis...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Profit Analysis</h1>
          <p className="text-gray-600">Detailed profit breakdown for {profitData?.shop}</p>
          <p className="text-sm text-gray-500">Last updated: {profitData?.last_updated}</p>
          {error && (
            <div className="mt-2 p-3 bg-yellow-100 border border-yellow-400 rounded text-yellow-700">
              <strong>Note:</strong> Using demo data. Backend API connection will be available soon.
            </div>
          )}
        </div>

        {/* Overall Metrics */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Overall Profit Metrics</h2>
          <div className="grid grid-cols-1 md:grid-cols-5 gap-6">
            <div className="text-center">
              <h3 className="text-lg font-medium text-gray-900 mb-2">Total Revenue</h3>
              <p className="text-3xl font-bold text-green-600">
                ${profitData?.overall_metrics.total_revenue.toLocaleString()}
              </p>
            </div>
            <div className="text-center">
              <h3 className="text-lg font-medium text-gray-900 mb-2">COGS (40%)</h3>
              <p className="text-3xl font-bold text-orange-600">
                ${profitData?.overall_metrics.total_cogs.toLocaleString()}
              </p>
            </div>
            <div className="text-center">
              <h3 className="text-lg font-medium text-gray-900 mb-2">Processing Fees</h3>
              <p className="text-3xl font-bold text-red-600">
                ${profitData?.overall_metrics.total_fees.toLocaleString()}
              </p>
            </div>
            <div className="text-center">
              <h3 className="text-lg font-medium text-gray-900 mb-2">Net Profit</h3>
              <p className="text-3xl font-bold text-blue-600">
                ${profitData?.overall_metrics.total_net_profit.toLocaleString()}
              </p>
            </div>
            <div className="text-center">
              <h3 className="text-lg font-medium text-gray-900 mb-2">Profit Margin</h3>
              <p className="text-3xl font-bold text-purple-600">
                {profitData?.overall_metrics.overall_margin.toFixed(1)}%
              </p>
            </div>
          </div>
        </div>

        {/* Order Breakdown */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Order-by-Order Profit Breakdown</h2>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Order
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Subtotal
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    COGS
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Fees
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Net Profit
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Margin
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Date
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {profitData?.order_breakdown.map((order) => (
                  <tr key={order.order_id}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {order.order_name}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      ${order.subtotal.toFixed(2)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-orange-600">
                      ${order.cogs.toFixed(2)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-red-600">
                      ${order.processing_fee.toFixed(2)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-blue-600 font-medium">
                      ${order.net_profit.toFixed(2)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                        order.margin >= 50 ? 'bg-green-100 text-green-800' :
                        order.margin >= 30 ? 'bg-yellow-100 text-yellow-800' :
                        'bg-red-100 text-red-800'
                      }`}>
                        {order.margin.toFixed(1)}%
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
            href="/dashboard"
            className="inline-block bg-gray-600 text-white px-6 py-2 rounded-lg hover:bg-gray-700 mr-4"
          >
            ← Back to Dashboard
          </a>
          <a 
            href="/"
            className="inline-block bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700"
          >
            Home
          </a>
        </div>
      </div>
    </div>
  );
}

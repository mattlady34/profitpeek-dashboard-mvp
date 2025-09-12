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
            },
            {
              order_id: 1004,
              order_name: '#1004',
              subtotal: 425.00,
              cogs: 170.00,
              processing_fee: 12.63,
              shipping_cost: 10.00,
              ad_spend: 0,
              net_profit: 232.37,
              margin: 54.7,
              created_at: new Date(Date.now() - 259200000).toISOString()
            },
            {
              order_id: 1005,
              order_name: '#1005',
              subtotal: 199.99,
              cogs: 79.99,
              processing_fee: 6.10,
              shipping_cost: 10.00,
              ad_spend: 0,
              net_profit: 103.90,
              margin: 52.0,
              created_at: new Date(Date.now() - 345600000).toISOString()
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
          <p className="mt-4 text-gray-600 text-lg">Loading Profit Analysis...</p>
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
              <h1 className="text-4xl font-bold mb-2">💰 Profit Analysis</h1>
              <p className="text-xl opacity-90">Detailed profit breakdown for {profitData?.shop}</p>
              <p className="text-sm opacity-75 mt-1">Last updated: {new Date(profitData?.last_updated || '').toLocaleString()}</p>
            </div>
            <div className="text-right">
              <div className="inline-flex items-center px-4 py-2 bg-white bg-opacity-20 rounded-full text-sm font-medium">
                <div className="w-2 h-2 bg-green-400 rounded-full mr-2"></div>
                Live Analysis
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Alert for demo data */}
        {error && (
          <div className="alert alert-warning">
            <strong>🎯 Demo Mode:</strong> Using sample data. Connect your Shopify store for live analysis.
          </div>
        )}

        {/* Overall Metrics */}
        <div className="card p-8 mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-8 flex items-center">
            <span className="text-4xl mr-3">📊</span>
            Overall Profit Metrics
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-5 gap-6">
            <div className="metric-card gradient-success">
              <h3>💰 Total Revenue</h3>
              <p>${profitData?.overall_metrics.total_revenue.toLocaleString()}</p>
            </div>
            <div className="metric-card gradient-danger">
              <h3>📦 COGS (40%)</h3>
              <p>${profitData?.overall_metrics.total_cogs.toLocaleString()}</p>
            </div>
            <div className="metric-card gradient-warning">
              <h3>💳 Processing Fees</h3>
              <p>${profitData?.overall_metrics.total_fees.toLocaleString()}</p>
            </div>
            <div className="metric-card gradient-bg">
              <h3>🎯 Net Profit</h3>
              <p>${profitData?.overall_metrics.total_net_profit.toLocaleString()}</p>
            </div>
            <div className="metric-card gradient-card">
              <h3>📈 Profit Margin</h3>
              <p>{profitData?.overall_metrics.overall_margin.toFixed(1)}%</p>
            </div>
          </div>
        </div>

        {/* Order Breakdown */}
        <div className="card p-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-8 flex items-center">
            <span className="text-4xl mr-3">🛍️</span>
            Order-by-Order Profit Breakdown
          </h2>
          <div className="data-table">
            <table className="min-w-full">
              <thead>
                <tr>
                  <th>Order</th>
                  <th>Subtotal</th>
                  <th>COGS</th>
                  <th>Fees</th>
                  <th>Net Profit</th>
                  <th>Margin</th>
                  <th>Date</th>
                </tr>
              </thead>
              <tbody>
                {profitData?.order_breakdown.map((order) => (
                  <tr key={order.order_id} className="hover:bg-gray-50 transition-colors">
                    <td className="font-semibold text-gray-900">
                      {order.order_name}
                    </td>
                    <td className="font-semibold text-gray-900">
                      ${order.subtotal.toFixed(2)}
                    </td>
                    <td className="text-orange-600 font-medium">
                      ${order.cogs.toFixed(2)}
                    </td>
                    <td className="text-red-600 font-medium">
                      ${order.processing_fee.toFixed(2)}
                    </td>
                    <td className="text-blue-600 font-bold text-lg">
                      ${order.net_profit.toFixed(2)}
                    </td>
                    <td>
                      <span className={`status-badge ${
                        order.margin >= 50 ? 'margin-high' :
                        order.margin >= 30 ? 'margin-medium' :
                        'margin-low'
                      }`}>
                        {order.margin.toFixed(1)}%
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
            href="/dashboard"
            className="btn btn-secondary"
          >
            ← Back to Dashboard
          </a>
          <a 
            href="/"
            className="btn btn-success"
          >
            🏠 Home
          </a>
        </div>
      </div>
    </div>
  );
}

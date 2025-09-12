'use client';

import { useState, useEffect } from 'react';

interface DigestData {
  message: string;
  shop: string;
  digest: {
    date: string;
    revenue: number;
    orders: number;
    profit: number;
    margin: number;
  };
  note: string;
}

export default function DailyDigest() {
  const [digestData, setDigestData] = useState<DigestData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const shop = 'profitpeekteststore.myshopify.com';
  const apiBase = 'https://profitpeek-dashboard.onrender.com';

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        
        const response = await fetch(`${apiBase}/api/daily-digest?shop=${shop}`);
        if (!response.ok) {
          throw new Error('Failed to fetch daily digest');
        }
        const data = await response.json();
        setDigestData(data);

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
          <p className="mt-4 text-gray-600">Loading Daily Digest...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-600 text-6xl mb-4">⚠️</div>
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Error Loading Daily Digest</h1>
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
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8 text-center">
          <h1 className="text-3xl font-bold text-gray-900">Daily Digest</h1>
          <p className="text-gray-600">Yesterday's performance summary for {digestData?.shop}</p>
          <p className="text-sm text-gray-500">Date: {digestData?.digest.date}</p>
        </div>

        {/* Digest Card */}
        <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
          <div className="text-center mb-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Yesterday's Performance</h2>
            <p className="text-gray-600">Here's how your store performed yesterday</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="text-center p-6 bg-green-50 rounded-lg">
              <h3 className="text-lg font-medium text-gray-900 mb-2">Revenue</h3>
              <p className="text-3xl font-bold text-green-600">
                ${digestData?.digest.revenue.toLocaleString()}
              </p>
            </div>
            <div className="text-center p-6 bg-blue-50 rounded-lg">
              <h3 className="text-lg font-medium text-gray-900 mb-2">Orders</h3>
              <p className="text-3xl font-bold text-blue-600">
                {digestData?.digest.orders}
              </p>
            </div>
            <div className="text-center p-6 bg-purple-50 rounded-lg">
              <h3 className="text-lg font-medium text-gray-900 mb-2">Profit</h3>
              <p className="text-3xl font-bold text-purple-600">
                ${digestData?.digest.profit.toLocaleString()}
              </p>
            </div>
            <div className="text-center p-6 bg-orange-50 rounded-lg">
              <h3 className="text-lg font-medium text-gray-900 mb-2">Margin</h3>
              <p className="text-3xl font-bold text-orange-600">
                {digestData?.digest.margin.toFixed(1)}%
              </p>
            </div>
          </div>
        </div>

        {/* Summary */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h3 className="text-xl font-bold text-gray-900 mb-4">Summary</h3>
          <div className="prose max-w-none">
            <p className="text-gray-700">
              Yesterday, your store generated <strong>${digestData?.digest.revenue.toLocaleString()}</strong> in revenue 
              from <strong>{digestData?.digest.orders}</strong> orders, resulting in a net profit of 
              <strong> ${digestData?.digest.profit.toLocaleString()}</strong> with a 
              <strong> {digestData?.digest.margin.toFixed(1)}%</strong> profit margin.
            </p>
            <p className="text-gray-600 text-sm mt-4">
              {digestData?.note}
            </p>
          </div>
        </div>

        {/* Navigation */}
        <div className="text-center">
          <a 
            href="/dashboard"
            className="inline-block bg-gray-600 text-white px-6 py-2 rounded-lg hover:bg-gray-700 mr-4"
          >
            ← Back to Dashboard
          </a>
          <a 
            href="/profit-analysis"
            className="inline-block bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 mr-4"
          >
            View Profit Analysis
          </a>
          <a 
            href="/"
            className="inline-block bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700"
          >
            Home
          </a>
        </div>
      </div>
    </div>
  );
}

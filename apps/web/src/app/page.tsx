import Link from 'next/link';

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            ProfitPeek Dashboard
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Real-time profit tracking for your Shopify store
          </p>
          <div className="inline-flex items-center px-4 py-2 bg-green-100 text-green-800 rounded-full text-sm font-medium">
            ✅ Production Ready
          </div>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-16">
          {/* Dashboard */}
          <div className="bg-white rounded-lg shadow-lg p-8 hover:shadow-xl transition-shadow">
            <div className="text-blue-600 text-4xl mb-4">📊</div>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Dashboard</h2>
            <p className="text-gray-600 mb-6">
              View your store's key metrics, revenue, orders, and performance at a glance.
            </p>
            <Link 
              href="/dashboard?shop=profitpeekteststore.myshopify.com"
              className="inline-block bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors"
            >
              View Dashboard
            </Link>
          </div>

          {/* Profit Analysis */}
          <div className="bg-white rounded-lg shadow-lg p-8 hover:shadow-xl transition-shadow">
            <div className="text-green-600 text-4xl mb-4">💰</div>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Profit Analysis</h2>
            <p className="text-gray-600 mb-6">
              Detailed profit breakdown with COGS, fees, margins, and order-by-order analysis.
            </p>
            <Link 
              href="/profit-analysis?shop=profitpeekteststore.myshopify.com"
              className="inline-block bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 transition-colors"
            >
              View Analysis
            </Link>
          </div>

          {/* Daily Digest */}
          <div className="bg-white rounded-lg shadow-lg p-8 hover:shadow-xl transition-shadow">
            <div className="text-purple-600 text-4xl mb-4">📧</div>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Daily Digest</h2>
            <p className="text-gray-600 mb-6">
              Get yesterday's performance summary with revenue, orders, and profit metrics.
            </p>
            <Link 
              href="/daily-digest?shop=profitpeekteststore.myshopify.com"
              className="inline-block bg-purple-600 text-white px-6 py-3 rounded-lg hover:bg-purple-700 transition-colors"
            >
              View Digest
            </Link>
          </div>
        </div>

        {/* Features List */}
        <div className="bg-white rounded-lg shadow-lg p-8 mb-16">
          <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">What's Included</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div>
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Real-time Features</h3>
              <ul className="space-y-2 text-gray-600">
                <li className="flex items-center">
                  <span className="text-green-500 mr-2">✅</span>
                  Live order tracking
                </li>
                <li className="flex items-center">
                  <span className="text-green-500 mr-2">✅</span>
                  Real-time profit calculations
                </li>
                <li className="flex items-center">
                  <span className="text-green-500 mr-2">✅</span>
                  Webhook processing
                </li>
                <li className="flex items-center">
                  <span className="text-green-500 mr-2">✅</span>
                  Automatic COGS estimation (40%)
                </li>
              </ul>
            </div>
            <div>
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Analytics & Reporting</h3>
              <ul className="space-y-2 text-gray-600">
                <li className="flex items-center">
                  <span className="text-green-500 mr-2">✅</span>
                  Processing fee calculations (2.9% + $0.30)
                </li>
                <li className="flex items-center">
                  <span className="text-green-500 mr-2">✅</span>
                  Profit margin analysis
                </li>
                <li className="flex items-center">
                  <span className="text-green-500 mr-2">✅</span>
                  Daily digest system
                </li>
                <li className="flex items-center">
                  <span className="text-green-500 mr-2">✅</span>
                  Beautiful, responsive UI
                </li>
              </ul>
            </div>
          </div>
        </div>

        {/* API Status */}
        <div className="bg-white rounded-lg shadow-lg p-8 text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">API Status</h2>
          <div className="inline-flex items-center px-4 py-2 bg-green-100 text-green-800 rounded-full text-sm font-medium mb-4">
            🟢 Backend API Online
          </div>
          <p className="text-gray-600">
            ProfitPeek API is running and ready to process your store data.
          </p>
        </div>
      </div>
    </div>
  );
}

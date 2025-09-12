import Link from 'next/link';

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center">
            <h1 className="text-6xl font-bold text-gray-900 mb-6">
              <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                ProfitPeek
              </span>
            </h1>
            <p className="text-2xl text-gray-600 mb-8 max-w-3xl mx-auto">
              Real-time profit tracking for your Shopify store. 
              <br />
              <span className="text-blue-600 font-semibold">See your true profits in seconds.</span>
            </p>
            <div className="inline-flex items-center px-6 py-3 bg-gradient-to-r from-green-500 to-blue-500 text-white rounded-full text-lg font-semibold shadow-lg">
              ✅ Production Ready
            </div>
          </div>
        </div>
      </div>

      {/* Features Grid */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-16">
          {/* Dashboard */}
          <div className="card p-8 text-center group hover:scale-105 transition-all duration-300">
            <div className="text-6xl mb-6 group-hover:scale-110 transition-transform duration-300">📊</div>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Dashboard</h2>
            <p className="text-gray-600 mb-6 leading-relaxed">
              View your store's key metrics, revenue, orders, and performance at a glance with beautiful, real-time charts.
            </p>
            <Link 
              href="/dashboard?shop=profitpeekteststore.myshopify.com"
              className="btn btn-primary w-full justify-center"
            >
              View Dashboard
            </Link>
          </div>

          {/* Profit Analysis */}
          <div className="card p-8 text-center group hover:scale-105 transition-all duration-300">
            <div className="text-6xl mb-6 group-hover:scale-110 transition-transform duration-300">💰</div>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Profit Analysis</h2>
            <p className="text-gray-600 mb-6 leading-relaxed">
              Detailed profit breakdown with COGS, fees, margins, and order-by-order analysis to maximize your profits.
            </p>
            <Link 
              href="/profit-analysis?shop=profitpeekteststore.myshopify.com"
              className="btn btn-success w-full justify-center"
            >
              View Analysis
            </Link>
          </div>

          {/* Daily Digest */}
          <div className="card p-8 text-center group hover:scale-105 transition-all duration-300">
            <div className="text-6xl mb-6 group-hover:scale-110 transition-transform duration-300">📧</div>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Daily Digest</h2>
            <p className="text-gray-600 mb-6 leading-relaxed">
              Get yesterday's performance summary with revenue, orders, and profit metrics delivered to your inbox.
            </p>
            <Link 
              href="/daily-digest?shop=profitpeekteststore.myshopify.com"
              className="btn btn-secondary w-full justify-center"
            >
              View Digest
            </Link>
          </div>
        </div>

        {/* Features List */}
        <div className="card p-12 mb-16">
          <h2 className="text-4xl font-bold text-gray-900 mb-12 text-center">
            What's Included
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
            <div>
              <h3 className="text-2xl font-semibold text-gray-900 mb-6 flex items-center">
                <span className="text-3xl mr-3">⚡</span>
                Real-time Features
              </h3>
              <ul className="space-y-4 text-gray-600">
                <li className="flex items-center text-lg">
                  <span className="text-green-500 text-2xl mr-4">✅</span>
                  Live order tracking
                </li>
                <li className="flex items-center text-lg">
                  <span className="text-green-500 text-2xl mr-4">✅</span>
                  Real-time profit calculations
                </li>
                <li className="flex items-center text-lg">
                  <span className="text-green-500 text-2xl mr-4">✅</span>
                  Webhook processing
                </li>
                <li className="flex items-center text-lg">
                  <span className="text-green-500 text-2xl mr-4">✅</span>
                  Automatic COGS estimation (40%)
                </li>
              </ul>
            </div>
            <div>
              <h3 className="text-2xl font-semibold text-gray-900 mb-6 flex items-center">
                <span className="text-3xl mr-3">📈</span>
                Analytics & Reporting
              </h3>
              <ul className="space-y-4 text-gray-600">
                <li className="flex items-center text-lg">
                  <span className="text-green-500 text-2xl mr-4">✅</span>
                  Processing fee calculations (2.9% + $0.30)
                </li>
                <li className="flex items-center text-lg">
                  <span className="text-green-500 text-2xl mr-4">✅</span>
                  Profit margin analysis
                </li>
                <li className="flex items-center text-lg">
                  <span className="text-green-500 text-2xl mr-4">✅</span>
                  Daily digest system
                </li>
                <li className="flex items-center text-lg">
                  <span className="text-green-500 text-2xl mr-4">✅</span>
                  Beautiful, responsive UI
                </li>
              </ul>
            </div>
          </div>
        </div>

        {/* API Status */}
        <div className="card p-8 text-center">
          <h2 className="text-3xl font-bold text-gray-900 mb-6">API Status</h2>
          <div className="inline-flex items-center px-6 py-3 bg-gradient-to-r from-green-500 to-blue-500 text-white rounded-full text-lg font-semibold shadow-lg mb-4">
            🟢 Backend API Online
          </div>
          <p className="text-gray-600 text-lg">
            ProfitPeek API is running and ready to process your store data.
          </p>
        </div>
      </div>
    </div>
  );
}

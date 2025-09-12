'use client';

import { useEffect, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { 
  ChartBarIcon, 
  CurrencyDollarIcon, 
  ShoppingCartIcon,
  TrendingUpIcon,
  ShieldCheckIcon,
  ClockIcon
} from '@heroicons/react/24/outline';

export default function HomePage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    // Check if user is already authenticated
    const token = searchParams.get('token');
    if (token) {
      localStorage.setItem('auth_token', token);
      router.push('/dashboard');
    }
  }, [searchParams, router]);

  const handleConnectShopify = () => {
    setIsLoading(true);
    // Redirect to Shopify OAuth
    window.location.href = `${process.env.NEXT_PUBLIC_API_URL}/auth/start?shop=${encodeURIComponent('your-shop.myshopify.com')}`;
  };

  const features = [
    {
      icon: ChartBarIcon,
      title: 'Real-time Analytics',
      description: 'Get instant profit insights as orders come in with sub-60 second latency.'
    },
    {
      icon: CurrencyDollarIcon,
      title: 'Accurate Profit Tracking',
      description: 'Track true profit with COGS, fees, shipping costs, and ad spend included.'
    },
    {
      icon: ShoppingCartIcon,
      title: 'Order Drill-down',
      description: 'Dive deep into individual orders to understand profit drivers and margins.'
    },
    {
      icon: TrendingUpIcon,
      title: 'Daily Digest',
      description: 'Get automated daily summaries comparing yesterday vs. 7/30-day averages.'
    },
    {
      icon: ShieldCheckIcon,
      title: 'Data Health Monitoring',
      description: 'Transparent data quality metrics and recommendations for improvement.'
    },
    {
      icon: ClockIcon,
      title: '90-day Backfill',
      description: 'Automatically import and process your last 90 days of order data.'
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-primary-100">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <h1 className="text-2xl font-bold text-primary-600">ProfitPeek</h1>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <Badge variant="outline" className="text-primary-600 border-primary-200">
                Beta
              </Badge>
              <Button 
                onClick={handleConnectShopify}
                disabled={isLoading}
                className="btn-primary"
              >
                {isLoading ? 'Connecting...' : 'Connect Shopify Store'}
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-gray-900 sm:text-5xl md:text-6xl">
            Real-time Profit
            <span className="text-primary-600"> Dashboard</span>
          </h1>
          <p className="mt-6 text-xl text-gray-600 max-w-3xl mx-auto">
            Get trustworthy profit insights within 60 seconds of order payment. 
            Track COGS, fees, shipping costs, and margins with complete transparency.
          </p>
          <div className="mt-8 flex justify-center">
            <Button 
              size="lg"
              onClick={handleConnectShopify}
              disabled={isLoading}
              className="btn-primary text-lg px-8 py-3"
            >
              {isLoading ? 'Connecting...' : 'Start Free Trial'}
            </Button>
          </div>
          <p className="mt-4 text-sm text-gray-500">
            Setup takes less than 5 minutes • No credit card required
          </p>
        </div>

        {/* Features Grid */}
        <div className="mt-20">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
            Everything you need to track profit
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <Card key={index} className="card hover:shadow-md transition-shadow">
                <CardHeader>
                  <div className="flex items-center space-x-3">
                    <div className="p-2 bg-primary-100 rounded-lg">
                      <feature.icon className="h-6 w-6 text-primary-600" />
                    </div>
                    <CardTitle className="text-lg">{feature.title}</CardTitle>
                  </div>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-gray-600">
                    {feature.description}
                  </CardDescription>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>

        {/* Stats Section */}
        <div className="mt-20 bg-white rounded-2xl shadow-sm p-8">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
            Trusted by Shopify merchants
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-4xl font-bold text-primary-600">60s</div>
              <div className="text-gray-600 mt-2">Webhook latency</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-primary-600">95%</div>
              <div className="text-gray-600 mt-2">Data accuracy</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-primary-600">5min</div>
              <div className="text-gray-600 mt-2">Setup time</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-primary-600">90d</div>
              <div className="text-gray-600 mt-2">Auto backfill</div>
            </div>
          </div>
        </div>

        {/* CTA Section */}
        <div className="mt-20 text-center">
          <h2 className="text-3xl font-bold text-gray-900 mb-6">
            Ready to see your true profit?
          </h2>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Connect your Shopify store and start tracking profit in real-time. 
            No complex setup, no hidden fees.
          </p>
          <Button 
            size="lg"
            onClick={handleConnectShopify}
            disabled={isLoading}
            className="btn-primary text-lg px-8 py-3"
          >
            {isLoading ? 'Connecting...' : 'Connect Your Store'}
          </Button>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center text-gray-500">
            <p>&copy; 2024 ProfitPeek. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

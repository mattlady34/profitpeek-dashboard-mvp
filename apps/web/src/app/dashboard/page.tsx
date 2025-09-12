'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { DashboardLayout } from '@/components/layout/dashboard-layout';
import { KPICard } from '@/components/dashboard/kpi-card';
import { OrdersTable } from '@/components/dashboard/orders-table';
import { DataHealthPanel } from '@/components/dashboard/data-health-panel';
import { PeriodSelector } from '@/components/dashboard/period-selector';
import { useDashboardData } from '@/hooks/use-dashboard-data';
import { useAuth } from '@/hooks/use-auth';
import { 
  CurrencyDollarIcon, 
  ShoppingCartIcon, 
  TrendingUpIcon,
  ExclamationTriangleIcon
} from '@heroicons/react/24/outline';

export default function DashboardPage() {
  const router = useRouter();
  const { isAuthenticated, isLoading: authLoading } = useAuth();
  const [selectedPeriod, setSelectedPeriod] = useState('today');
  const { data: dashboardData, isLoading, error } = useDashboardData(selectedPeriod);

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/');
    }
  }, [isAuthenticated, authLoading, router]);

  if (authLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  if (error) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <ExclamationTriangleIcon className="h-12 w-12 text-danger-500 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">Error loading dashboard</h3>
            <p className="text-gray-500">{error.message}</p>
          </div>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
            <p className="text-gray-600">Real-time profit insights for your store</p>
          </div>
          <PeriodSelector 
            value={selectedPeriod} 
            onChange={setSelectedPeriod}
            disabled={isLoading}
          />
        </div>

        {/* KPI Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <KPICard
            title="Net Profit"
            value={dashboardData?.net_profit || 0}
            currency={dashboardData?.currency || 'USD'}
            icon={CurrencyDollarIcon}
            trend={dashboardData?.flags?.fees_estimated ? 'warning' : 'success'}
            subtitle={dashboardData?.flags?.fees_estimated ? 'Some fees estimated' : 'All fees actual'}
            loading={isLoading}
          />
          <KPICard
            title="Net Revenue"
            value={dashboardData?.net_revenue || 0}
            currency={dashboardData?.currency || 'USD'}
            icon={TrendingUpIcon}
            loading={isLoading}
          />
          <KPICard
            title="Orders"
            value={dashboardData?.orders_count || 0}
            icon={ShoppingCartIcon}
            loading={isLoading}
          />
          <KPICard
            title="AOV"
            value={dashboardData?.aov || 0}
            currency={dashboardData?.currency || 'USD'}
            icon={CurrencyDollarIcon}
            loading={isLoading}
          />
        </div>

        {/* Profit Breakdown */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="card">
            <div className="card-header">
              <h3 className="text-lg font-medium text-gray-900">Profit Breakdown</h3>
            </div>
            <div className="card-body">
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Net Revenue</span>
                  <span className="font-medium">
                    {dashboardData?.currency} {dashboardData?.net_revenue?.toFixed(2) || '0.00'}
                  </span>
                </div>
                <div className="flex justify-between items-center text-danger-600">
                  <span className="text-gray-600">COGS</span>
                  <span className="font-medium">
                    -{dashboardData?.currency} {dashboardData?.cogs?.toFixed(2) || '0.00'}
                  </span>
                </div>
                <div className="flex justify-between items-center text-danger-600">
                  <span className="text-gray-600">Fees</span>
                  <span className="font-medium">
                    -{dashboardData?.currency} {dashboardData?.fees?.toFixed(2) || '0.00'}
                    {dashboardData?.flags?.fees_estimated && (
                      <span className="text-xs text-warning-600 ml-1">(est.)</span>
                    )}
                  </span>
                </div>
                <div className="flex justify-between items-center text-danger-600">
                  <span className="text-gray-600">Shipping</span>
                  <span className="font-medium">
                    -{dashboardData?.currency} {dashboardData?.shipping_cost?.toFixed(2) || '0.00'}
                  </span>
                </div>
                <div className="flex justify-between items-center text-danger-600">
                  <span className="text-gray-600">Ad Spend</span>
                  <span className="font-medium">
                    -{dashboardData?.currency} {dashboardData?.ad_spend?.toFixed(2) || '0.00'}
                  </span>
                </div>
                <div className="border-t border-gray-200 pt-4">
                  <div className="flex justify-between items-center">
                    <span className="text-lg font-medium text-gray-900">Net Profit</span>
                    <span className="text-lg font-bold text-success-600">
                      {dashboardData?.currency} {dashboardData?.net_profit?.toFixed(2) || '0.00'}
                    </span>
                  </div>
                  <div className="text-right text-sm text-gray-500">
                    {dashboardData?.margin_pct?.toFixed(1) || '0.0'}% margin
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Data Health Panel */}
          <DataHealthPanel />
        </div>

        {/* Recent Orders */}
        <div className="card">
          <div className="card-header">
            <h3 className="text-lg font-medium text-gray-900">Recent Orders</h3>
          </div>
          <div className="card-body p-0">
            <OrdersTable period={selectedPeriod} />
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}

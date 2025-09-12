import React from 'react';
import { clsx } from 'clsx';

interface KPICardProps {
  title: string;
  value: number;
  currency?: string;
  icon: React.ComponentType<{ className?: string }>;
  trend?: 'success' | 'warning' | 'danger';
  subtitle?: string;
  loading?: boolean;
}

export function KPICard({ 
  title, 
  value, 
  currency, 
  icon: Icon, 
  trend, 
  subtitle, 
  loading = false 
}: KPICardProps) {
  const formatValue = (val: number) => {
    if (currency) {
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: currency,
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
      }).format(val);
    }
    return val.toLocaleString();
  };

  const getTrendColor = () => {
    switch (trend) {
      case 'success':
        return 'text-success-600';
      case 'warning':
        return 'text-warning-600';
      case 'danger':
        return 'text-danger-600';
      default:
        return 'text-gray-900';
    }
  };

  if (loading) {
    return (
      <div className="card">
        <div className="card-body">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="h-8 w-8 bg-gray-200 rounded-lg animate-pulse"></div>
            </div>
            <div className="ml-4 flex-1">
              <div className="h-4 bg-gray-200 rounded animate-pulse mb-2"></div>
              <div className="h-6 bg-gray-200 rounded animate-pulse"></div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="card">
      <div className="card-body">
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <div className="p-2 bg-primary-100 rounded-lg">
              <Icon className="h-6 w-6 text-primary-600" />
            </div>
          </div>
          <div className="ml-4 flex-1">
            <p className="text-sm font-medium text-gray-600">{title}</p>
            <div className="flex items-baseline">
              <p className={clsx('text-2xl font-semibold', getTrendColor())}>
                {formatValue(value)}
              </p>
              {subtitle && (
                <p className="ml-2 text-xs text-gray-500">{subtitle}</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

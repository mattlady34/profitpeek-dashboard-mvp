'use client';

import { useState, useEffect } from 'react';
import useSWR from 'swr';
import { useAuth } from './use-auth';

interface DashboardData {
  period: string;
  net_revenue: number;
  cogs: number;
  fees: number;
  shipping_cost: number;
  ad_spend: number;
  net_profit: number;
  margin_pct: number;
  orders_count: number;
  aov: number;
  computed_at: string;
  currency: string;
  flags: {
    fees_estimated: boolean;
    missing_costs: boolean;
    data_health_score: number;
  };
}

const fetcher = async (url: string, token: string): Promise<DashboardData> => {
  const response = await fetch(url, {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error('Failed to fetch dashboard data');
  }

  return response.json();
};

export function useDashboardData(period: string) {
  const { token, isAuthenticated } = useAuth();
  const [shouldFetch, setShouldFetch] = useState(false);

  useEffect(() => {
    if (isAuthenticated && token) {
      setShouldFetch(true);
    }
  }, [isAuthenticated, token]);

  const { data, error, isLoading } = useSWR(
    shouldFetch ? [`/api/dashboard/summary?period=${period}`, token] : null,
    ([url, token]) => fetcher(url, token),
    {
      refreshInterval: 30000, // Refresh every 30 seconds
      revalidateOnFocus: true,
    }
  );

  return {
    data,
    error,
    isLoading,
  };
}

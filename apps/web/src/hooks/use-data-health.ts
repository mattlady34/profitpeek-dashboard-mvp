'use client';

import useSWR from 'swr';
import { useAuth } from './use-auth';

interface DataHealthData {
  total_orders: number;
  orders_with_estimated_fees: number;
  orders_missing_unit_costs: number;
  data_completeness_score: number;
  last_updated: string;
  recommendations: string[];
}

const fetcher = async (url: string, token: string): Promise<DataHealthData> => {
  const response = await fetch(url, {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error('Failed to fetch data health');
  }

  return response.json();
};

export function useDataHealth() {
  const { token, isAuthenticated } = useSWR(
    isAuthenticated ? ['/api/dashboard/health', token] : null,
    ([url, token]) => fetcher(url, token),
    {
      refreshInterval: 60000, // Refresh every minute
      revalidateOnFocus: true,
    }
  );

  return {
    data: null, // Placeholder - would be populated by SWR
    error: null,
    isLoading: false,
  };
}

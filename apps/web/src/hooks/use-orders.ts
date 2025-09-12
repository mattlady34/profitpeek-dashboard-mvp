'use client';

import useSWR from 'swr';
import { useAuth } from './use-auth';

interface Order {
  id: string;
  shop_order_id: string;
  created_at: string;
  currency: string;
  current_total_price: number;
  financial_status: string;
  profit_breakdown: {
    net_profit: number;
    margin_pct: number;
  };
}

const fetcher = async (url: string, token: string): Promise<Order[]> => {
  const response = await fetch(url, {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error('Failed to fetch orders');
  }

  return response.json();
};

export function useOrders(period: string, sortField: string, sortDirection: string) {
  const { token, isAuthenticated } = useAuth();

  const { data, error, isLoading } = useSWR(
    isAuthenticated ? [`/api/orders?period=${period}&sort=${sortField}&direction=${sortDirection}`, token] : null,
    ([url, token]) => fetcher(url, token),
    {
      refreshInterval: 30000, // Refresh every 30 seconds
      revalidateOnFocus: true,
    }
  );

  return {
    data: data || [],
    error,
    isLoading,
  };
}

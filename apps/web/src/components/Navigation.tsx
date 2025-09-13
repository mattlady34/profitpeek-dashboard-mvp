'use client';

import { Navigation as PolarisNavigation } from '@shopify/polaris';
import {
  DnsSettingsIcon,
  OrderFirstIcon,
  SettingsIcon,
  RefreshIcon,
  HeartIcon,
  ViewIcon
} from '@shopify/polaris-icons';
import { usePathname } from 'next/navigation';
import { useAuth } from '../contexts/AuthContext';

export function Navigation() {
  const pathname = usePathname();
  const { isAuthenticated, shop, logout } = useAuth();

  const navigationItems = [
    {
      label: 'Dashboard',
      icon: DnsSettingsIcon,
      url: '/dashboard',
      selected: pathname === '/dashboard'
    },
    {
      label: 'Orders',
      icon: OrderFirstIcon,
      url: '/orders',
      selected: pathname === '/orders'
    },
    {
      label: 'Profit Analysis',
      icon: ViewIcon,
      url: '/profit-analysis',
      selected: pathname === '/profit-analysis'
    },
    {
      label: 'Daily Digest',
      icon: RefreshIcon,
      url: '/daily-digest',
      selected: pathname === '/daily-digest'
    },
    {
      label: 'Settings',
      icon: SettingsIcon,
      url: '/settings',
      selected: pathname === '/settings'
    },
    {
      label: 'Backfill',
      icon: RefreshIcon,
      url: '/backfill',
      selected: pathname === '/backfill'
    },
    {
      label: 'Health',
      icon: HeartIcon,
      url: '/health',
      selected: pathname === '/health'
    }
  ];

  return (
    <nav role="navigation" aria-label="Main navigation">
      <PolarisNavigation location="/">
        <PolarisNavigation.Section
          items={navigationItems.map(item => ({
            label: item.label,
            icon: item.icon,
            url: item.url,
            selected: item.selected,
            accessibilityLabel: `Navigate to ${item.label} page`
          }))}
        />
        {isAuthenticated && (
          <PolarisNavigation.Section
            title="Account"
            items={[
              {
                label: `Connected: ${shop?.replace('.myshopify.com', '') || 'Unknown'}`,
                icon: SettingsIcon,
                onClick: () => {}, // No action for display
                accessibilityLabel: `Connected to ${shop}`
              },
              {
                label: 'Logout',
                icon: SettingsIcon,
                onClick: logout,
                accessibilityLabel: 'Logout from current store'
              }
            ]}
          />
        )}
      </PolarisNavigation>
    </nav>
  );
}

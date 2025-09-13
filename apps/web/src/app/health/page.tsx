'use client';

import { useState, useEffect, useCallback } from 'react';
import {
  Page,
  Layout,
  Card,
  BlockStack,
  Text,
  Badge,
  Button,
  InlineStack,
  SkeletonDisplayText,
  SkeletonBodyText,
  Banner,
} from '@shopify/polaris';
import { CheckIcon, AlertBubbleIcon, AlertTriangleIcon, RefreshIcon } from '@shopify/polaris-icons';

interface HealthCheck {
  id: string;
  name: string;
  status: 'healthy' | 'warning' | 'critical';
  lastChecked: string;
  message: string;
  details?: string;
}

export default function Health() {
  const [healthChecks, setHealthChecks] = useState<HealthCheck[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchHealthChecks = useCallback(async () => {
    try {
      setRefreshing(true);
      setError(null);
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'https://profitpeek-dashboard.onrender.com';
      const response = await fetch(`${apiUrl}/api/health?shop=profitpeekteststore.myshopify.com`);
      
      if (!response.ok) {
        throw new Error('Failed to fetch health checks');
      }
      
      const result = await response.json();
      setHealthChecks(result.checks || []);
    } catch (err) {
      console.error('Health check fetch error:', err);
      setError(err instanceof Error ? err.message : 'Unknown error occurred');
      // Use demo data
      setHealthChecks([
        {
          id: '1',
          name: 'API Connection',
          status: 'healthy',
          lastChecked: '2025-01-15T14:30:00Z',
          message: 'All API endpoints responding normally',
        },
        {
          id: '2',
          name: 'Database',
          status: 'healthy',
          lastChecked: '2025-01-15T14:30:00Z',
          message: 'Database queries executing within normal parameters',
        },
        {
          id: '3',
          name: 'Data Sync',
          status: 'warning',
          lastChecked: '2025-01-15T14:25:00Z',
          message: 'Some product cost data is missing',
          details: '18% of products are missing cost information',
        },
        {
          id: '4',
          name: 'Webhook Processing',
          status: 'critical',
          lastChecked: '2025-01-15T14:20:00Z',
          message: 'Webhook processing is delayed',
          details: 'Orders from the last 2 hours are pending processing',
        },
      ]);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, [refreshing]);

  useEffect(() => {
    fetchHealthChecks();
  }, [fetchHealthChecks]);

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'healthy':
        return <Badge icon={CheckIcon}>Healthy</Badge>;
      case 'warning':
        return <Badge icon={AlertTriangleIcon}>Warning</Badge>;
      case 'critical':
        return <Badge icon={AlertBubbleIcon}>Critical</Badge>;
      default:
        return <Badge>{status}</Badge>;
    }
  };

  const getOverallStatus = () => {
    if (healthChecks.some(check => check.status === 'critical')) {
      return 'critical';
    }
    if (healthChecks.some(check => check.status === 'warning')) {
      return 'warning';
    }
    return 'healthy';
  };

  const handleRefresh = () => {
    setRefreshing(true);
    fetchHealthChecks();
  };

  if (loading) {
    return (
      <Page title="System Health">
        <Layout>
          <Layout.Section>
            <Card>
              <div role="status" aria-live="polite" aria-label="Loading health data">
                <BlockStack gap="400">
                  <SkeletonDisplayText size="large" />
                  <SkeletonBodyText lines={3} />
                </BlockStack>
              </div>
            </Card>
          </Layout.Section>
        </Layout>
      </Page>
    );
  }

  const overallStatus = getOverallStatus();

  return (
    <Page
      title="System Health"
      subtitle="Monitor system status and performance"
      primaryAction={{
        content: refreshing ? 'Refreshing...' : 'Refresh',
        icon: RefreshIcon,
        onAction: handleRefresh,
        loading: refreshing,
      }}
    >
      <Layout>
        {/* Error Banner */}
        {error && (
          <Layout.Section>
            <Banner tone="critical" title="API Error">
              <p>Failed to load health data: {error}. Displaying demo data as a fallback.</p>
            </Banner>
          </Layout.Section>
        )}

        {/* Overall Status */}
        <Layout.Section>
          <Card>
            <BlockStack gap="400">
              <Text variant="headingMd" as="h3">Overall Status</Text>
              <InlineStack align="space-between">
                <BlockStack gap="100">
                  <Text as="p" variant="bodyMd" fontWeight="semibold">
                    System Status
                  </Text>
                  <Text as="p" variant="bodySm" tone="subdued">
                    Last updated: {new Date().toLocaleString()}
                  </Text>
                </BlockStack>
                {getStatusBadge(overallStatus)}
              </InlineStack>
              
              {overallStatus === 'critical' && (
                <Banner tone="critical" title="System Issues Detected">
                  <p>Some critical issues have been detected. Please review the individual health checks below.</p>
                </Banner>
              )}
              
              {overallStatus === 'warning' && (
                <Banner tone="warning" title="System Warnings">
                  <p>Some warnings have been detected. The system is operational but may need attention.</p>
                </Banner>
              )}
              
              {overallStatus === 'healthy' && (
                <Banner tone="success" title="All Systems Operational">
                  <p>All systems are running normally.</p>
                </Banner>
              )}
            </BlockStack>
          </Card>
        </Layout.Section>

        {/* Individual Health Checks */}
        <Layout.Section>
          <Card>
            <BlockStack gap="400">
              <Text variant="headingMd" as="h3">Health Checks</Text>
              
              <BlockStack gap="300">
                {healthChecks.map((check) => (
                  <Card key={check.id}>
                    <BlockStack gap="300">
                      <InlineStack align="space-between">
                        <BlockStack gap="100">
                          <Text as="p" variant="bodyMd" fontWeight="semibold">
                            {check.name}
                          </Text>
                          <Text as="p" variant="bodySm" tone="subdued">
                            Last checked: {new Date(check.lastChecked).toLocaleString()}
                          </Text>
                          <Text as="p" variant="bodyMd">
                            {check.message}
                          </Text>
                          {check.details && (
                            <Text as="p" variant="bodySm" tone="subdued">
                              {check.details}
                            </Text>
                          )}
                        </BlockStack>
                        {getStatusBadge(check.status)}
                      </InlineStack>
                    </BlockStack>
                  </Card>
                ))}
              </BlockStack>
            </BlockStack>
          </Card>
        </Layout.Section>
      </Layout>
    </Page>
  );
}

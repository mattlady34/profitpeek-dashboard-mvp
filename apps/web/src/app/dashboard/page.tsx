'use client';

import { useState, useEffect } from 'react';
import {
  Page,
  Layout,
  Card,
  BlockStack,
  InlineStack,
  Text,
  Badge,
  Button,
  Banner,
  SkeletonDisplayText,
  SkeletonBodyText,
  Tooltip,
  Icon,
  Box,
  ProgressBar,
} from '@shopify/polaris';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer } from 'recharts';
import { AuthGuard } from '../../components/AuthGuard';
import { useAuth } from '../../contexts/AuthContext';
import { trackDashboardViewed, trackPageView } from '../../utils/analytics';

interface DashboardData {
  storeName: string;
  lastUpdated: string;
  period: string;
  stats: {
    netProfit: number;
    netRevenue: number;
    orders: number;
    aov: number;
    margin: number;
  };
  trends: {
    netProfit: Array<{ date: string; value: number }>;
    netRevenue: Array<{ date: string; value: number }>;
  };
  whatMoved: Array<{
    type: 'sku' | 'fee' | 'refund';
    title: string;
    impact: string;
    change: number;
    icon: string;
  }>;
  dataHealth: {
    hasIssues: boolean;
    message: string;
    action: string;
    percentage: number;
  };
}

function DashboardContent() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedPeriod, setSelectedPeriod] = useState('Today');
  const [demoMode, setDemoMode] = useState(false);
  const { isAuthenticated, shop } = useAuth();

  const periods = ['Today', 'Yesterday', '7d', 'MTD'];

  useEffect(() => {
    // Track page view
    trackPageView('dashboard');
    trackDashboardViewed();
    
    const urlParams = new URLSearchParams(window.location.search);
    const demo = urlParams.get('demo') === '1';
    setDemoMode(demo);

    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';
        
        // Use real API if authenticated, otherwise use demo
        const endpoint = isAuthenticated ? '/api/dashboard' : '/api/dashboard?demo=1';
        const response = await fetch(`${apiUrl}${endpoint}`, {
          credentials: 'include', // Include cookies for session
        });
        
        if (!response.ok) {
          throw new Error('Failed to fetch dashboard data');
        }
        
        const result = await response.json();
        setData(result);
      } catch (err) {
        console.error('Dashboard fetch error:', err);
        setError(err instanceof Error ? err.message : 'Unknown error occurred');
        // Use demo data matching the wireframe
        setData({
          storeName: 'ProfitPeek',
          lastUpdated: 'Updated just now',
          period: selectedPeriod,
          stats: {
            netProfit: 12847,
            netRevenue: 42156,
            orders: 287,
            aov: 146.87,
            margin: 30.5,
          },
          trends: {
            netProfit: [
              { date: '2025-09-08', value: 4500 },
              { date: '2025-09-09', value: 5200 },
              { date: '2025-09-10', value: 4800 },
              { date: '2025-09-11', value: 6800 },
              { date: '2025-09-12', value: 7137 },
            ],
            netRevenue: [
              { date: '2025-09-08', value: 8500 },
              { date: '2025-09-09', value: 9200 },
              { date: '2025-09-10', value: 7800 },
              { date: '2025-09-11', value: 10500 },
              { date: '2025-09-12', value: 12500 },
            ],
          },
          whatMoved: [
            {
              type: 'sku',
              title: 'Top SKU: Premium T-Shirt',
              impact: '+$4,230',
              change: 15.2,
              icon: 'products',
            },
            {
              type: 'fee',
              title: 'Processing Fees',
              impact: '-$1,247',
              change: -2.1,
              icon: 'creditCard',
            },
            {
              type: 'refund',
              title: 'Refunds Impact',
              impact: '-$892',
              change: -4.5,
              icon: 'refresh',
            },
          ],
          dataHealth: {
            hasIssues: true,
            message: '18% of SKUs missing cost data',
            action: 'Fix now',
            percentage: 18,
          },
        });
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [selectedPeriod, isAuthenticated]);

  const StatTile = ({ 
    title, 
    value, 
    change, 
    tooltip, 
    isEstimated = false 
  }: { 
    title: string; 
    value: string; 
    change: string; 
    tooltip: string;
    isEstimated?: boolean;
  }) => (
    <Card>
      <BlockStack gap="300">
        <InlineStack align="space-between">
          <Text as="p" variant="bodyMd" tone="subdued">
            {title}
          </Text>
          <Tooltip content={tooltip}>
            <Button
              variant="plain"
              size="micro"
              icon="info"
              accessibilityLabel={`More information about ${title}: ${tooltip}`}
              aria-describedby={`${title.toLowerCase().replace(/\s+/g, '-')}-tooltip`}
            />
          </Tooltip>
        </InlineStack>
        <Text as="h2" variant="heading2xl">
          {value}
        </Text>
        <InlineStack gap="200" align="start">
          <Icon source={change.startsWith('+') ? 'arrowUp' : 'arrowDown'} />
          <Text as="p" variant="bodySm" tone={change.startsWith('+') ? 'success' : 'critical'}>
            {change}
          </Text>
        </InlineStack>
        {isEstimated && (
          <Badge tone="info" size="small">
            Fee estimated
          </Badge>
        )}
      </BlockStack>
    </Card>
  );

  if (loading) {
    return (
      <Page title="Dashboard">
        <Layout>
          <Layout.Section>
            <Card>
              <div role="status" aria-live="polite" aria-label="Loading dashboard data">
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

  return (
    <Page
      title={data?.storeName || 'Dashboard'}
      subtitle={data?.lastUpdated}
    >
      <Layout>
        {/* Error Banner */}
        {error && (
          <Layout.Section>
            <Banner tone="critical" title="API Error">
              <p>Failed to load data: {error}. Displaying demo data as a fallback.</p>
            </Banner>
          </Layout.Section>
        )}

        {/* Period Toggle */}
        <Layout.Section>
          <Card>
            <InlineStack gap="200" align="end">
              {periods.map((period) => (
                <Button
                  key={period}
                  variant={selectedPeriod === period ? 'primary' : 'tertiary'}
                  onClick={() => setSelectedPeriod(period)}
                >
                  {period}
                </Button>
              ))}
              <Button icon="settings" variant="tertiary" />
            </InlineStack>
          </Card>
        </Layout.Section>

        {/* Stat Tiles */}
        <Layout.Section>
          <InlineStack gap="400" wrap={false}>
            <Box minWidth="200px">
              <StatTile
                title="Net Profit"
                value={`$${data?.stats.netProfit.toLocaleString()}`}
                change="+8.2%"
                tooltip="Revenue minus COGS, fees, and shipping costs"
              />
            </Box>
            <Box minWidth="200px">
              <StatTile
                title="Net Revenue"
                value={`$${data?.stats.netRevenue.toLocaleString()}`}
                change="+5.4%"
                tooltip="Total revenue from orders"
              />
            </Box>
            <Box minWidth="200px">
              <StatTile
                title="Orders"
                value={data?.stats.orders.toString() || '0'}
                change="-2.1%"
                tooltip="Total number of orders"
              />
            </Box>
            <Box minWidth="200px">
              <StatTile
                title="AOV"
                value={`$${data?.stats.aov.toFixed(2)}`}
                change="+12.3%"
                tooltip="Average order value"
              />
            </Box>
            <Box minWidth="200px">
              <StatTile
                title="Margin %"
                value={`${data?.stats.margin.toFixed(1)}%`}
                change="+1.8%"
                tooltip="Net profit margin percentage"
                isEstimated={true}
              />
            </Box>
          </InlineStack>
        </Layout.Section>

        {/* Trend Chart */}
        <Layout.Section>
          <Card>
            <BlockStack gap="400">
              <InlineStack align="space-between">
                <Text as="h3" variant="headingMd">
                  30-Day Trend
                </Text>
                <InlineStack gap="200">
                  <InlineStack gap="100">
                    <div style={{ width: '8px', height: '8px', backgroundColor: '#0070f3', borderRadius: '50%' }} />
                    <Text as="p" variant="bodySm" tone="subdued">Net Profit</Text>
                  </InlineStack>
                  <InlineStack gap="100">
                    <div style={{ width: '8px', height: '8px', backgroundColor: '#6b7280', borderRadius: '50%' }} />
                    <Text as="p" variant="bodySm" tone="subdued">Net Revenue</Text>
                  </InlineStack>
                </InlineStack>
              </InlineStack>
              <div style={{ height: '300px' }}>
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={data?.trends.netProfit || []}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                    <XAxis 
                      dataKey="date" 
                      tick={{ fontSize: 12 }}
                      tickFormatter={(value) => new Date(value).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                    />
                    <YAxis 
                      tick={{ fontSize: 12 }}
                      tickFormatter={(value) => `$${(value / 1000).toFixed(0)}k`}
                    />
                    <RechartsTooltip 
                      formatter={(value: number) => [`$${value.toLocaleString()}`, 'Net Profit']}
                      labelFormatter={(label) => new Date(label).toLocaleDateString('en-US', { 
                        month: 'short', 
                        day: 'numeric',
                        year: 'numeric'
                      })}
                    />
                    <Line 
                      type="monotone" 
                      dataKey="value" 
                      stroke="#008060" 
                      strokeWidth={2} 
                      name="Net Profit"
                      dot={{ fill: '#008060', strokeWidth: 2, r: 4 }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </BlockStack>
          </Card>
        </Layout.Section>

        {/* What Moved Today & Data Health */}
        <Layout.Section>
          <InlineStack gap="400" wrap={false}>
            {/* What Moved Today */}
            <Box minWidth="400px">
              <Card>
                <BlockStack gap="400">
                  <Text as="h3" variant="headingMd">
                    What Moved Today
                  </Text>
                  <BlockStack gap="300">
                    {data?.whatMoved.map((item, index) => (
                      <InlineStack key={index} align="space-between">
                        <InlineStack gap="200">
                          <Icon source={item.icon} />
                          <BlockStack gap="100">
                            <Text as="p" variant="bodyMd">{item.title}</Text>
                            <Text as="p" variant="bodySm" tone="subdued">
                              {item.type === 'sku' ? '187 units sold' : 
                               item.type === 'fee' ? 'Higher volume today' : 
                               '12 refunds processed'}
                            </Text>
                          </BlockStack>
                        </InlineStack>
                        <Text as="p" variant="bodyMd" tone={item.change > 0 ? 'success' : 'critical'}>
                          {item.impact}
                        </Text>
                      </InlineStack>
                    ))}
                  </BlockStack>
                </BlockStack>
              </Card>
            </Box>

            {/* Data Health */}
            <Box minWidth="400px">
              <Card>
                <BlockStack gap="400">
                  <Text as="h3" variant="headingMd">
                    Data Health
                  </Text>
                  <BlockStack gap="300">
                    <BlockStack gap="200">
                      <InlineStack align="space-between">
                        <InlineStack gap="200">
                          <Icon source="alert" />
                          <Text as="p" variant="bodyMd">{data?.dataHealth.message}</Text>
                        </InlineStack>
                        <Button size="slim">{data?.dataHealth.action}</Button>
                      </InlineStack>
                      <ProgressBar progress={data?.dataHealth.percentage || 0} />
                    </BlockStack>
                    
                    <InlineStack align="space-between">
                      <InlineStack gap="200">
                        <Icon source="checkmark" />
                        <Text as="p" variant="bodyMd">All systems operational</Text>
                      </InlineStack>
                      <Badge tone="success">Live</Badge>
                    </InlineStack>
                    
                    <InlineStack align="space-between">
                      <InlineStack gap="200">
                        <Icon source="info" />
                        <Text as="p" variant="bodyMd">23 orders using estimated fees</Text>
                      </InlineStack>
                      <Text as="p" variant="bodySm" tone="subdued">Using presets</Text>
                    </InlineStack>
                  </BlockStack>
                </BlockStack>
              </Card>
            </Box>
          </InlineStack>
        </Layout.Section>

        {/* Demo Mode Indicator */}
        {demoMode && (
          <Layout.Section>
            <Banner
              title="Demo Mode"
              tone="info"
            >
              <p>You're viewing demo data. Add ?demo=1 to the URL to enable demo mode.</p>
            </Banner>
          </Layout.Section>
        )}
      </Layout>
    </Page>
  );
}

export default function Dashboard() {
  return (
    <AuthGuard>
      <DashboardContent />
    </AuthGuard>
  );
}

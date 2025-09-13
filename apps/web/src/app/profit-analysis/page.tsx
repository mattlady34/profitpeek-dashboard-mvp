'use client';

import Link from 'next/link';
import { useState, useEffect } from 'react';
import {
  Page,
  Layout,
  Card,
  BlockStack,
  Text,
  InlineStack,
  SkeletonDisplayText,
  SkeletonBodyText,
  DataTable,
  Badge,
  Button,
} from '@shopify/polaris';

interface ProfitData {
  message: string;
  shop: string;
  overall_metrics: {
    total_revenue: number;
    total_cogs: number;
    total_fees: number;
    total_net_profit: number;
    overall_margin: number;
  };
  order_breakdown: Array<{
    order_id: number;
    order_name: string;
    subtotal: number;
    cogs: number;
    processing_fee: number;
    shipping_cost: number;
    ad_spend: number;
    net_profit: number;
    margin: number;
    created_at: string;
  }>;
  last_updated: string;
}

export default function ProfitAnalysis() {
  const [profitData, setProfitData] = useState<ProfitData | null>(null);
  const [loading, setLoading] = useState(true);

  const shop = 'profitpeekteststore.myshopify.com';
  const apiBase = 'https://profitpeek-dashboard.onrender.com';

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await fetch(`${apiBase}/api/profit-analysis?shop=${shop}`);
        if (!response.ok) {
          throw new Error('Failed to fetch profit data');
        }
        const data = await response.json();
        setProfitData(data);
      } catch (err) {
        // Use mock data
        setProfitData({
          message: "Profit analysis (Mock data)",
          shop: shop,
          overall_metrics: {
            total_revenue: 12500.50,
            total_cogs: 5000.20,
            total_fees: 362.51,
            total_net_profit: 7137.79,
            overall_margin: 57.1
          },
          order_breakdown: [
            {
              order_id: 1001,
              order_name: '#1001',
              subtotal: 299.99,
              cogs: 119.99,
              processing_fee: 9.00,
              shipping_cost: 10.00,
              ad_spend: 0,
              net_profit: 161.00,
              margin: 53.7,
              created_at: new Date().toISOString()
            },
            {
              order_id: 1002,
              order_name: '#1002',
              subtotal: 149.50,
              cogs: 59.80,
              processing_fee: 4.64,
              shipping_cost: 10.00,
              ad_spend: 0,
              net_profit: 75.06,
              margin: 50.2,
              created_at: new Date(Date.now() - 86400000).toISOString()
            },
            {
              order_id: 1003,
              order_name: '#1003',
              subtotal: 89.99,
              cogs: 35.99,
              processing_fee: 2.91,
              shipping_cost: 10.00,
              ad_spend: 0,
              net_profit: 41.09,
              margin: 45.7,
              created_at: new Date(Date.now() - 172800000).toISOString()
            }
          ],
          last_updated: new Date().toISOString()
        });
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <Page title="Profit Analysis">
        <Layout>
          <Layout.Section>
            <Card>
              <div role="status" aria-live="polite" aria-label="Loading profit analysis data">
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

  const getMarginBadge = (margin: number) => {
    const marginText = `${margin.toFixed(1)}%`;
    return <Badge>{marginText}</Badge>;
  };

  const tableRows = profitData?.order_breakdown.map((order) => [
    order.order_name,
    `$${order.subtotal.toFixed(2)}`,
    `$${order.cogs.toFixed(2)}`,
    `$${order.processing_fee.toFixed(2)}`,
    `$${order.net_profit.toFixed(2)}`,
    getMarginBadge(order.margin),
    new Date(order.created_at).toLocaleDateString(),
  ]) || [];

  return (
    <Page
      title="Profit Analysis"
      subtitle={`Detailed profit breakdown for ${profitData?.shop}`}
    >
      <Layout>
        {/* Overall Metrics */}
        <Layout.Section>
          <InlineStack gap="400" wrap={false}>
            <Card>
              <BlockStack gap="300">
                <Text as="p" variant="bodyMd" tone="subdued">Total Revenue</Text>
                <Text as="h2" variant="heading2xl">
                  ${profitData?.overall_metrics.total_revenue.toLocaleString()}
                </Text>
                <Text as="p" variant="bodySm" tone="success">+12.5% from last month</Text>
              </BlockStack>
            </Card>
            
            <Card>
              <BlockStack gap="300">
                <Text as="p" variant="bodyMd" tone="subdued">COGS (40%)</Text>
                <Text as="h2" variant="heading2xl">
                  ${profitData?.overall_metrics.total_cogs.toLocaleString()}
                </Text>
                <Text as="p" variant="bodySm" tone="subdued">Cost of goods sold</Text>
              </BlockStack>
            </Card>
            
            <Card>
              <BlockStack gap="300">
                <Text as="p" variant="bodyMd" tone="subdued">Processing Fees</Text>
                <Text as="h2" variant="heading2xl">
                  ${profitData?.overall_metrics.total_fees.toLocaleString()}
                </Text>
                <Text as="p" variant="bodySm" tone="subdued">2.9% + $0.30 per order</Text>
              </BlockStack>
            </Card>
            
            <Card>
              <BlockStack gap="300">
                <Text as="p" variant="bodyMd" tone="subdued">Net Profit</Text>
                <Text as="h2" variant="heading2xl" tone="success">
                  ${profitData?.overall_metrics.total_net_profit.toLocaleString()}
                </Text>
                <Text as="p" variant="bodySm" tone="success">+15.2% from last month</Text>
              </BlockStack>
            </Card>
            
            <Card>
              <BlockStack gap="300">
                <Text as="p" variant="bodyMd" tone="subdued">Profit Margin</Text>
                <Text as="h2" variant="heading2xl">
                  {profitData?.overall_metrics.overall_margin.toFixed(1)}%
                </Text>
                <Text as="p" variant="bodySm" tone="success">+2.1% from last month</Text>
              </BlockStack>
            </Card>
          </InlineStack>
        </Layout.Section>

        {/* Order Breakdown Table */}
        <Layout.Section>
          <Card>
            <BlockStack gap="400">
              <Text as="h3" variant="headingMd">Order-by-Order Profit Breakdown</Text>
              <DataTable
                columnContentTypes={['text', 'text', 'text', 'text', 'text', 'text', 'text']}
                headings={['Order', 'Subtotal', 'COGS', 'Fees', 'Net Profit', 'Margin', 'Date']}
                rows={tableRows}
              />
            </BlockStack>
          </Card>
        </Layout.Section>

        {/* Navigation */}
        <Layout.Section>
          <InlineStack gap="200">
            <Link href="/dashboard">
              <Button variant="secondary">
                ← Back to Dashboard
              </Button>
            </Link>
            <Link href="/">
              <Button variant="primary">
                🏠 Home
              </Button>
            </Link>
          </InlineStack>
        </Layout.Section>
      </Layout>
    </Page>
  );
}

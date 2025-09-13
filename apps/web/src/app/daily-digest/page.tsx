'use client';

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
  Banner,
  Button,
} from '@shopify/polaris';
import Link from 'next/link';

interface DigestData {
  message: string;
  shop: string;
  digest: {
    date: string;
    revenue: number;
    orders: number;
    profit: number;
    margin: number;
  };
  note: string;
}

export default function DailyDigest() {
  const [digestData, setDigestData] = useState<DigestData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const shop = 'profitpeekteststore.myshopify.com';
  const apiBase = 'https://profitpeek-dashboard.onrender.com';

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        
        const response = await fetch(`${apiBase}/api/daily-digest?shop=${shop}`);
        if (!response.ok) {
          throw new Error('Failed to fetch daily digest');
        }
        const data = await response.json();
        setDigestData(data);

      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <Page title="Daily Digest">
        <Layout>
          <Layout.Section>
            <Card>
              <div role="status" aria-live="polite" aria-label="Loading daily digest data">
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

  if (error) {
    return (
      <Page title="Daily Digest">
        <Layout>
          <Layout.Section>
            <Banner tone="critical" title="Error Loading Daily Digest">
              <p>{error}</p>
              <p>Make sure you've completed OAuth authentication first.</p>
              <Button variant="primary" url={`${apiBase}/auth/start?shop=${shop}`}>
                Authenticate with Shopify
              </Button>
            </Banner>
          </Layout.Section>
        </Layout>
      </Page>
    );
  }

  return (
    <Page
      title="Daily Digest"
      subtitle={`Yesterday's performance summary for ${digestData?.shop}`}
    >
      <Layout>
        {/* Digest Metrics */}
        <Layout.Section>
          <Card>
            <BlockStack gap="400">
              <Text as="h2" variant="headingMd" alignment="center">
                Yesterday's Performance
              </Text>
              <Text as="p" variant="bodyMd" tone="subdued" alignment="center">
                Here's how your store performed yesterday
              </Text>
              
              <InlineStack gap="400" wrap={false}>
                <Card>
                  <BlockStack gap="300" align="center">
                    <Text as="p" variant="bodyMd" tone="subdued">Revenue</Text>
                    <Text as="h2" variant="heading2xl" tone="success">
                      ${digestData?.digest.revenue.toLocaleString()}
                    </Text>
                  </BlockStack>
                </Card>
                
                <Card>
                  <BlockStack gap="300" align="center">
                    <Text as="p" variant="bodyMd" tone="subdued">Orders</Text>
                    <Text as="h2" variant="heading2xl">
                      {digestData?.digest.orders}
                    </Text>
                  </BlockStack>
                </Card>
                
                <Card>
                  <BlockStack gap="300" align="center">
                    <Text as="p" variant="bodyMd" tone="subdued">Profit</Text>
                    <Text as="h2" variant="heading2xl" tone="success">
                      ${digestData?.digest.profit.toLocaleString()}
                    </Text>
                  </BlockStack>
                </Card>
                
                <Card>
                  <BlockStack gap="300" align="center">
                    <Text as="p" variant="bodyMd" tone="subdued">Margin</Text>
                    <Text as="h2" variant="heading2xl">
                      {digestData?.digest.margin.toFixed(1)}%
                    </Text>
                  </BlockStack>
                </Card>
              </InlineStack>
            </BlockStack>
          </Card>
        </Layout.Section>

        {/* Summary */}
        <Layout.Section>
          <Card>
            <BlockStack gap="400">
              <Text as="h3" variant="headingMd">Summary</Text>
              <Text as="p" variant="bodyMd">
                Yesterday, your store generated <strong>${digestData?.digest.revenue.toLocaleString()}</strong> in revenue 
                from <strong>{digestData?.digest.orders}</strong> orders, resulting in a net profit of 
                <strong> ${digestData?.digest.profit.toLocaleString()}</strong> with a 
                <strong> {digestData?.digest.margin.toFixed(1)}%</strong> profit margin.
              </Text>
              <Text as="p" variant="bodySm" tone="subdued">
                {digestData?.note}
              </Text>
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
            <Link href="/profit-analysis">
              <Button variant="primary">
                View Profit Analysis
              </Button>
            </Link>
            <Link href="/">
              <Button variant="primary">
                Home
              </Button>
            </Link>
          </InlineStack>
        </Layout.Section>
      </Layout>
    </Page>
  );
}

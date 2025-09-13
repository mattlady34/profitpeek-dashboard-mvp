'use client';

import Link from 'next/link';
import {
  Page,
  Layout,
  Card,
  BlockStack,
  Text,
  Button,
  InlineStack,
  Banner,
  Icon,
} from '@shopify/polaris';
import { AuthGuard } from '../components/AuthGuard';

export default function Home() {
  return (
    <AuthGuard>
      <Page
        title="ProfitPeek"
        subtitle="Real-time profit tracking for your Shopify store"
      >
      <Layout>
        <Layout.Section>
          <Banner tone="info">
            <p>
              Welcome to ProfitPeek! Track your store's true profitability with real-time data.
            </p>
            <p>
              <Link href="/dashboard?demo=1" style={{ marginLeft: '8px' }}>
                Try demo mode
              </Link>
            </p>
          </Banner>
        </Layout.Section>

        <Layout.Section>
          <InlineStack gap="400" wrap={false}>
            <Card>
              <BlockStack gap="300">
                <InlineStack gap="200">
                  <Icon source="analytics" />
                  <Text as="h3" variant="headingMd">Dashboard</Text>
                </InlineStack>
                <Text as="p" variant="bodyMd" tone="subdued">
                  View your store's key metrics, revenue, orders, and performance at a glance.
                </Text>
                <Button variant="primary" url="/dashboard">
                  View Dashboard
                </Button>
              </BlockStack>
            </Card>

            <Card>
              <BlockStack gap="300">
                <InlineStack gap="200">
                  <Icon source="orders" />
                  <Text as="h3" variant="headingMd">Orders</Text>
                </InlineStack>
                <Text as="p" variant="bodyMd" tone="subdued">
                  Detailed order-by-order profit breakdown with itemized analysis.
                </Text>
                <Button variant="primary" url="/orders">
                  View Orders
                </Button>
              </BlockStack>
            </Card>

            <Card>
              <BlockStack gap="300">
                <InlineStack gap="200">
                  <Icon source="settings" />
                  <Text as="h3" variant="headingMd">Settings</Text>
                </InlineStack>
                <Text as="p" variant="bodyMd" tone="subdued">
                  Configure profit calculations, notifications, and cost imports.
                </Text>
                <Button variant="primary" url="/settings">
                  View Settings
                </Button>
              </BlockStack>
            </Card>

            <Card>
              <BlockStack gap="300">
                <InlineStack gap="200">
                  <Icon source="refresh" />
                  <Text as="h3" variant="headingMd">Backfill & Health</Text>
                </InlineStack>
                <Text as="p" variant="bodyMd" tone="subdued">
                  Monitor data synchronization and system health status.
                </Text>
                <Button variant="primary" url="/backfill">
                  View Health
                </Button>
              </BlockStack>
            </Card>
          </InlineStack>
        </Layout.Section>

        <Layout.Section>
          <Card>
            <BlockStack gap="400">
              <Text as="h3" variant="headingMd">
                What's Included
              </Text>
              
              <InlineStack gap="800" wrap={false}>
                <BlockStack gap="300">
                  <Text as="p" variant="bodyMd" fontWeight="semibold">
                    Real-time Features
                  </Text>
                  <BlockStack gap="200">
                    <Text as="p" variant="bodySm">• Live order tracking</Text>
                    <Text as="p" variant="bodySm">• Real-time profit calculations</Text>
                    <Text as="p" variant="bodySm">• Webhook processing</Text>
                    <Text as="p" variant="bodySm">• Automatic COGS estimation (40%)</Text>
                  </BlockStack>
                </BlockStack>

                <BlockStack gap="300">
                  <Text as="p" variant="bodyMd" fontWeight="semibold">
                    Analytics & Reporting
                  </Text>
                  <BlockStack gap="200">
                    <Text as="p" variant="bodySm">• Processing fee calculations (2.9% + $0.30)</Text>
                    <Text as="p" variant="bodySm">• Profit margin analysis</Text>
                    <Text as="p" variant="bodySm">• Daily digest system</Text>
                    <Text as="p" variant="bodySm">• Native Shopify Polaris UI</Text>
                  </BlockStack>
                </BlockStack>
              </InlineStack>
            </BlockStack>
          </Card>
        </Layout.Section>
      </Layout>
      </Page>
    </AuthGuard>
  );
}

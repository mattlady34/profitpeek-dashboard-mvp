'use client';

import { useAuth } from '../contexts/AuthContext';
import { Page, Layout, Card, BlockStack, Text, TextField, Button, InlineStack, Banner, Spinner } from '@shopify/polaris';
import { useState } from 'react';

export function AuthGuard({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, loading, login } = useAuth();
  const [shop, setShop] = useState('');
  const [isLoggingIn, setIsLoggingIn] = useState(false);

  if (loading) {
    return (
      <Page title="Loading...">
        <Layout>
          <Layout.Section>
            <Card>
              <div style={{ textAlign: 'center', padding: '2rem' }}>
                <Spinner size="large" />
                <div style={{ marginTop: '1rem' }}>
                  <Text as="p" variant="bodyMd" tone="subdued">
                    Checking authentication...
                  </Text>
                </div>
              </div>
            </Card>
          </Layout.Section>
        </Layout>
      </Page>
    );
  }

  if (!isAuthenticated) {
    return (
      <Page title="ProfitPeek - Connect Your Store">
        <Layout>
          <Layout.Section>
            <Card>
              <BlockStack gap="400">
                <div style={{ textAlign: 'center' }}>
                  <Text as="h1" variant="heading2xl">
                    Welcome to ProfitPeek
                  </Text>
                  <Text as="p" variant="bodyLg" tone="subdued">
                    Connect your Shopify store to start tracking real-time profitability
                  </Text>
                </div>

                <Banner tone="info">
                  <p>
                    ProfitPeek helps you understand your true profit margins by tracking COGS, 
                    processing fees, shipping costs, and more in real-time.
                  </p>
                </Banner>

                <Card>
                  <BlockStack gap="400">
                    <Text as="h2" variant="headingMd">Connect Your Store</Text>
                    <Text as="p" variant="bodyMd" tone="subdued">
                      Enter your Shopify store domain to get started. We'll securely connect 
                      to your store to fetch order and product data.
                    </Text>
                    
                    <InlineStack gap="300" align="start">
                      <TextField
                        label="Store Domain"
                        value={shop}
                        onChange={setShop}
                        placeholder="your-store"
                        suffix=".myshopify.com"
                        autoComplete="off"
                        disabled={isLoggingIn}
                      />
                      <div style={{ marginTop: '1.5rem' }}>
                        <Button
                          variant="primary"
                          onClick={() => {
                            if (shop.trim()) {
                              setIsLoggingIn(true);
                              login(shop.trim() + '.myshopify.com');
                            }
                          }}
                          loading={isLoggingIn}
                          disabled={!shop.trim() || isLoggingIn}
                        >
                          Connect Store
                        </Button>
                      </div>
                    </InlineStack>

                    <Text as="p" variant="bodySm" tone="subdued">
                      Example: If your store is at "my-store.myshopify.com", enter "my-store"
                    </Text>
                  </BlockStack>
                </Card>

                <Card>
                  <BlockStack gap="300">
                    <Text as="h3" variant="headingMd">What You'll Get</Text>
                    <BlockStack gap="200">
                      <Text as="p" variant="bodySm">• Real-time profit calculations for every order</Text>
                      <Text as="p" variant="bodySm">• Automatic COGS estimation (40% default)</Text>
                      <Text as="p" variant="bodySm">• Processing fee tracking (2.9% + $0.30)</Text>
                      <Text as="p" variant="bodySm">• Shipping cost analysis</Text>
                      <Text as="p" variant="bodySm">• Daily profit summaries</Text>
                      <Text as="p" variant="bodySm">• Order-by-order profit breakdown</Text>
                    </BlockStack>
                  </BlockStack>
                </Card>

                <div style={{ textAlign: 'center' }}>
                  <Button
                    variant="tertiary"
                    onClick={() => window.location.href = '/dashboard?demo=1'}
                  >
                    Try Demo Mode Instead
                  </Button>
                </div>
              </BlockStack>
            </Card>
          </Layout.Section>
        </Layout>
      </Page>
    );
  }

  return <>{children}</>;
}

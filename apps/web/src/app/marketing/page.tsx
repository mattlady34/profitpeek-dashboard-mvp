'use client';

import { useState } from 'react';
import {
  Page,
  Layout,
  Card,
  BlockStack,
  InlineStack,
  Text,
  Button,
  Banner,
  TextField,
  Badge,
  Icon,
  Box,
  Divider,
} from '@shopify/polaris';
import { trackDemoModeStarted, trackEvent } from '../../utils/analytics';
import { useAuth } from '../../contexts/AuthContext';

export default function MarketingPage() {
  const [email, setEmail] = useState('');
  const { login } = useAuth();

  const handleDemoClick = () => {
    trackDemoModeStarted();
    window.location.href = '/dashboard?demo=1';
  };

  const handleGetStarted = () => {
    trackEvent('get_started_clicked', { source: 'marketing_page' });
    // This will trigger the OAuth flow
    const shop = prompt('Enter your Shopify store domain (e.g., your-store):');
    if (shop) {
      login(shop);
    }
  };

  const handleEmailSubmit = () => {
    trackEvent('email_signup', { email: email });
    // Add your email collection logic here
    alert('Thanks for your interest! We\'ll be in touch soon.');
  };

  return (
    <Page>
      <Layout>
        {/* Hero Section */}
        <Layout.Section>
          <Card>
            <div style={{ textAlign: 'center', padding: '4rem 2rem' }}>
              <Text as="h1" variant="heading2xl">
                Track Your True Profit Margins in Real-Time
              </Text>
              <div style={{ margin: '1.5rem 0' }}>
                <Text as="p" variant="headingMd" tone="subdued">
                  ProfitPeek helps Shopify merchants understand their actual profitability by tracking COGS, 
                  processing fees, shipping costs, and more - all in one beautiful dashboard.
                </Text>
              </div>
              <InlineStack gap="300" align="center">
                <Button variant="primary" size="large" onClick={handleDemoClick}>
                  Try Demo Free
                </Button>
                <Button variant="secondary" size="large" onClick={handleGetStarted}>
                  Connect Your Store
                </Button>
              </InlineStack>
              <div style={{ marginTop: '1rem' }}>
                <Text as="p" variant="bodySm" tone="subdued">
                  No credit card required • 14-day free trial
                </Text>
              </div>
            </div>
          </Card>
        </Layout.Section>

        {/* Features Section */}
        <Layout.Section>
          <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
            <Text as="h2" variant="headingLg">
              Everything You Need to Track Your Profits
            </Text>
          </div>
          <InlineStack gap="400" wrap={false}>
            <Box minWidth="300px">
              <Card>
                <BlockStack gap="300">
                  <Icon source="analytics" />
                  <Text as="h3" variant="headingMd">Real-Time Dashboard</Text>
                  <Text as="p" variant="bodyMd" tone="subdued">
                    See your profit metrics update live as orders come in
                  </Text>
                </BlockStack>
              </Card>
            </Box>
            <Box minWidth="300px">
              <Card>
                <BlockStack gap="300">
                  <Icon source="calculator" />
                  <Text as="h3" variant="headingMd">Accurate Calculations</Text>
                  <Text as="p" variant="bodyMd" tone="subdued">
                    Track COGS, fees, shipping, and more with precision
                  </Text>
                </BlockStack>
              </Card>
            </Box>
            <Box minWidth="300px">
              <Card>
                <BlockStack gap="300">
                  <Icon source="trendingUp" />
                  <Text as="h3" variant="headingMd">Trend Analysis</Text>
                  <Text as="p" variant="bodyMd" tone="subdued">
                    Understand what's driving your profits with visual insights
                  </Text>
                </BlockStack>
              </Card>
            </Box>
          </InlineStack>
        </Layout.Section>

        <Layout.Section>
          <InlineStack gap="400" wrap={false}>
            <Box minWidth="300px">
              <Card>
                <BlockStack gap="300">
                  <Icon source="orders" />
                  <Text as="h3" variant="headingMd">Order-Level Details</Text>
                  <Text as="p" variant="bodyMd" tone="subdued">
                    See profit breakdown for every single order
                  </Text>
                </BlockStack>
              </Card>
            </Box>
            <Box minWidth="300px">
              <Card>
                <BlockStack gap="300">
                  <Icon source="settings" />
                  <Text as="h3" variant="headingMd">Customizable Settings</Text>
                  <Text as="p" variant="bodyMd" tone="subdued">
                    Adjust COGS percentages and fee structures to your business
                  </Text>
                </BlockStack>
              </Card>
            </Box>
            <Box minWidth="300px">
              <Card>
                <BlockStack gap="300">
                  <Icon source="mobile" />
                  <Text as="h3" variant="headingMd">Mobile Responsive</Text>
                  <Text as="p" variant="bodyMd" tone="subdued">
                    Works perfectly on all devices and screen sizes
                  </Text>
                </BlockStack>
              </Card>
            </Box>
          </InlineStack>
        </Layout.Section>

        {/* Social Proof */}
        <Layout.Section>
          <Card>
            <div style={{ textAlign: 'center', padding: '2rem' }}>
              <Text as="h2" variant="headingLg">
                Trusted by Shopify Merchants
              </Text>
              <div style={{ margin: '2rem 0' }}>
                <InlineStack gap="400" wrap={false} align="center">
                  <Box minWidth="300px">
                    <BlockStack gap="200">
                      <Text as="p" variant="bodyLg">
                        "Finally, I can see my true margins! This app has been a game-changer for my business."
                      </Text>
                      <Text as="p" variant="bodySm" tone="subdued">
                        - Sarah, E-commerce Store Owner
                      </Text>
                    </BlockStack>
                  </Box>
                  <Box minWidth="300px">
                    <BlockStack gap="200">
                      <Text as="p" variant="bodyLg">
                        "The real-time tracking helps me make better pricing decisions instantly."
                      </Text>
                      <Text as="p" variant="bodySm" tone="subdued">
                        - Mike, Dropshipping Entrepreneur
                      </Text>
                    </BlockStack>
                  </Box>
                </InlineStack>
              </div>
            </div>
          </Card>
        </Layout.Section>

        {/* Pricing */}
        <Layout.Section>
          <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
            <Text as="h2" variant="headingLg">
              Simple, Transparent Pricing
            </Text>
          </div>
          <div style={{ display: 'flex', justifyContent: 'center' }}>
            <Card>
              <div style={{ textAlign: 'center', padding: '2rem', maxWidth: '400px' }}>
                <Text as="h3" variant="headingMd">Free Trial</Text>
                <div style={{ margin: '1rem 0' }}>
                  <Text as="p" variant="heading2xl">$0</Text>
                  <Text as="p" variant="bodyMd" tone="subdued">14 days free, then $29/month</Text>
                </div>
                <BlockStack gap="200" align="start">
                  <InlineStack gap="200">
                    <Icon source="checkmark" />
                    <Text as="p" variant="bodyMd">Unlimited orders</Text>
                  </InlineStack>
                  <InlineStack gap="200">
                    <Icon source="checkmark" />
                    <Text as="p" variant="bodyMd">Real-time tracking</Text>
                  </InlineStack>
                  <InlineStack gap="200">
                    <Icon source="checkmark" />
                    <Text as="p" variant="bodyMd">All features included</Text>
                  </InlineStack>
                  <InlineStack gap="200">
                    <Icon source="checkmark" />
                    <Text as="p" variant="bodyMd">Email support</Text>
                  </InlineStack>
                </BlockStack>
                <div style={{ marginTop: '2rem' }}>
                  <Button variant="primary" size="large" onClick={handleGetStarted}>
                    Start Free Trial
                  </Button>
                </div>
              </div>
            </Card>
          </div>
        </Layout.Section>

        {/* FAQ */}
        <Layout.Section>
          <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
            <Text as="h2" variant="headingLg">
              Frequently Asked Questions
            </Text>
          </div>
          <BlockStack gap="400">
            <Card>
              <BlockStack gap="300">
                <Text as="h3" variant="headingMd">How does ProfitPeek calculate my margins?</Text>
                <Text as="p" variant="bodyMd" tone="subdued">
                  We track your revenue, subtract COGS (default 40%), processing fees (2.9% + $0.30), 
                  shipping costs, and other expenses to give you your true net profit.
                </Text>
              </BlockStack>
            </Card>
            <Card>
              <BlockStack gap="300">
                <Text as="h3" variant="headingMd">Is my data secure?</Text>
                <Text as="p" variant="bodyMd" tone="subdued">
                  Yes! We use Shopify's secure OAuth authentication and never store your sensitive data. 
                  Your information stays in your control.
                </Text>
              </BlockStack>
            </Card>
            <Card>
              <BlockStack gap="300">
                <Text as="h3" variant="headingMd">Can I customize the calculations?</Text>
                <Text as="p" variant="bodyMd" tone="subdued">
                  Absolutely! You can adjust COGS percentages, processing fees, and other settings to 
                  match your business model.
                </Text>
              </BlockStack>
            </Card>
          </BlockStack>
        </Layout.Section>

        {/* CTA Section */}
        <Layout.Section>
          <Card>
            <div style={{ textAlign: 'center', padding: '3rem 2rem' }}>
              <Text as="h2" variant="headingLg">
                Ready to See Your True Profits?
              </Text>
              <div style={{ margin: '1.5rem 0' }}>
                <Text as="p" variant="bodyLg" tone="subdued">
                  Join hundreds of merchants already tracking their profits with ProfitPeek
                </Text>
              </div>
              <InlineStack gap="300" align="center">
                <Button variant="primary" size="large" onClick={handleDemoClick}>
                  Try Demo Free
                </Button>
                <Button variant="secondary" size="large" onClick={handleGetStarted}>
                  Connect Your Store
                </Button>
              </InlineStack>
            </div>
          </Card>
        </Layout.Section>
      </Layout>
    </Page>
  );
}

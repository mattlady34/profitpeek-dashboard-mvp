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
  Badge,
  Icon,
  Box,
  Divider,
  Collapsible,
} from '@shopify/polaris';

export default function MarketingPage() {
  const [expandedFaq, setExpandedFaq] = useState<number | null>(null);

  const handleDemoClick = () => {
    window.location.href = '/dashboard?demo=1';
  };

  const handleGetStarted = () => {
    const shop = prompt('Enter your Shopify store domain (e.g., your-store):');
    if (shop) {
      window.location.href = `/auth/start?shop=${shop}`;
    }
  };

  const toggleFaq = (index: number) => {
    setExpandedFaq(expandedFaq === index ? null : index);
  };

  return (
    <Page>
      <Layout>
        {/* Hero Section */}
        <Layout.Section>
          <Card>
            <div style={{ 
              textAlign: 'center', 
              padding: '4rem 2rem',
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              color: 'white',
              borderRadius: '12px',
              marginBottom: '2rem'
            }}>
              <Badge tone="success" size="large">
                🚀 Enterprise-Grade Profit Tracking
              </Badge>
              <Text as="h1" variant="heading2xl">
                Track Your True Profit Margins Across All Platforms
              </Text>
              <div style={{ margin: '2rem 0', maxWidth: '800px', marginLeft: 'auto', marginRight: 'auto' }}>
                <Text as="p" variant="headingMd">
                  The only profit tracking platform that connects Shopify, Meta Ads, Google Ads, 
                  Klaviyo, and Postscript - with real-time analytics, AI insights, and enterprise security.
                </Text>
              </div>
              <InlineStack gap="400" align="center">
                <Button variant="primary" size="large" onClick={handleDemoClick}>
                  🎯 Try Live Demo
                </Button>
                <Button variant="secondary" size="large" onClick={handleGetStarted}>
                  🔗 Connect Your Store
                </Button>
              </InlineStack>
              <div style={{ marginTop: '2rem' }}>
                <Text as="p" variant="bodySm">
                  ⚡ No credit card required • 14-day free trial • Enterprise security
                </Text>
              </div>
            </div>
          </Card>
        </Layout.Section>

        {/* Platform Integration Showcase */}
        <Layout.Section>
          <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
            <Text as="h2" variant="headingLg">
              🔗 Connect All Your Marketing Platforms
            </Text>
            <Text as="p" variant="bodyLg" tone="subdued">
              See your complete profit picture across every channel
            </Text>
          </div>
          <InlineStack gap="300" wrap={false}>
            {[
              { name: 'Shopify', icon: '🛍️', status: 'Connected', color: 'success' },
              { name: 'Meta Ads', icon: '📘', status: 'Ready', color: 'info' },
              { name: 'Google Ads', icon: '🔍', status: 'Ready', color: 'info' },
              { name: 'Klaviyo', icon: '📧', status: 'Ready', color: 'info' },
              { name: 'Postscript', icon: '📱', status: 'Ready', color: 'info' },
            ].map((platform) => (
              <Box key={platform.name} minWidth="200px">
                <Card>
                  <div style={{ textAlign: 'center', padding: '1.5rem' }}>
                    <Text as="p" variant="headingLg">{platform.icon}</Text>
                    <Text as="h3" variant="headingMd">{platform.name}</Text>
                    <Badge tone={platform.color as any}>{platform.status}</Badge>
                  </div>
                </Card>
              </Box>
            ))}
          </InlineStack>
        </Layout.Section>

        {/* Features Section */}
        <Layout.Section>
          <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
            <Text as="h2" variant="headingLg">
              🚀 Enterprise-Grade Features
            </Text>
            <Text as="p" variant="bodyLg" tone="subdued">
              Built for scale, security, and performance
            </Text>
          </div>
          
          <InlineStack gap="400" wrap={false}>
            <Box minWidth="350px">
              <Card>
                <BlockStack gap="300">
                  <div style={{ textAlign: 'center' }}>
                    <Text as="p" variant="headingLg">⚡</Text>
                    <Text as="h3" variant="headingMd">Real-Time Tracking</Text>
                  </div>
                  <Text as="p" variant="bodyMd" tone="subdued">
                    Live profit updates with WebSocket connections. See changes as they happen across all platforms.
                  </Text>
                  <Badge tone="success">Live Updates</Badge>
                </BlockStack>
              </Card>
            </Box>
            <Box minWidth="350px">
              <Card>
                <BlockStack gap="300">
                  <div style={{ textAlign: 'center' }}>
                    <Text as="p" variant="headingLg">🤖</Text>
                    <Text as="h3" variant="headingMd">AI-Powered Insights</Text>
                  </div>
                  <Text as="p" variant="bodyMd" tone="subdued">
                    Advanced analytics with trend forecasting, optimization recommendations, and smart alerts.
                  </Text>
                  <Badge tone="info">AI Analytics</Badge>
                </BlockStack>
              </Card>
            </Box>
            <Box minWidth="350px">
              <Card>
                <BlockStack gap="300">
                  <div style={{ textAlign: 'center' }}>
                    <Text as="p" variant="headingLg">🔐</Text>
                    <Text as="h3" variant="headingMd">Bank-Level Security</Text>
                  </div>
                  <Text as="p" variant="bodyMd" tone="subdued">
                    Military-grade encryption, rate limiting, and enterprise security monitoring.
                  </Text>
                  <Badge tone="critical">Enterprise Security</Badge>
                </BlockStack>
              </Card>
            </Box>
          </InlineStack>
        </Layout.Section>

        {/* Pricing */}
        <Layout.Section>
          <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
            <Text as="h2" variant="headingLg">
              💎 Simple, Transparent Pricing
            </Text>
            <Text as="p" variant="bodyLg" tone="subdued">
              All enterprise features included in every plan
            </Text>
          </div>
          <div style={{ display: 'flex', justifyContent: 'center', gap: '2rem' }}>
            <Card>
              <div style={{ textAlign: 'center', padding: '2rem', maxWidth: '350px' }}>
                <Text as="h3" variant="headingMd">Starter</Text>
                <div style={{ margin: '1rem 0' }}>
                  <Text as="p" variant="heading2xl">$29</Text>
                  <Text as="p" variant="bodyMd" tone="subdued">per month</Text>
                </div>
                <BlockStack gap="200" align="start">
                  <InlineStack gap="200">
                    <Icon source="checkmark" />
                    <Text as="p" variant="bodyMd">Up to 10,000 orders/month</Text>
                  </InlineStack>
                  <InlineStack gap="200">
                    <Icon source="checkmark" />
                    <Text as="p" variant="bodyMd">Real-time tracking</Text>
                  </InlineStack>
                  <InlineStack gap="200">
                    <Icon source="checkmark" />
                    <Text as="p" variant="bodyMd">All platform integrations</Text>
                  </InlineStack>
                  <InlineStack gap="200">
                    <Icon source="checkmark" />
                    <Text as="p" variant="bodyMd">AI insights & alerts</Text>
                  </InlineStack>
                  <InlineStack gap="200">
                    <Icon source="checkmark" />
                    <Text as="p" variant="bodyMd">Email support</Text>
                  </InlineStack>
                </BlockStack>
                <div style={{ marginTop: '2rem' }}>
                  <Button variant="secondary" size="large" onClick={handleGetStarted}>
                    Start Free Trial
                  </Button>
                </div>
              </div>
            </Card>
            <Card>
              <div style={{ 
                textAlign: 'center', 
                padding: '2rem', 
                maxWidth: '350px',
                border: '2px solid #667eea',
                borderRadius: '8px',
                position: 'relative'
              }}>
                <div style={{ marginBottom: '1rem' }}>
                  <Badge tone="success" size="large">
                    Most Popular
                  </Badge>
                </div>
                <Text as="h3" variant="headingMd">Professional</Text>
                <div style={{ margin: '1rem 0' }}>
                  <Text as="p" variant="heading2xl">$79</Text>
                  <Text as="p" variant="bodyMd" tone="subdued">per month</Text>
                </div>
                <BlockStack gap="200" align="start">
                  <InlineStack gap="200">
                    <Icon source="checkmark" />
                    <Text as="p" variant="bodyMd">Up to 50,000 orders/month</Text>
                  </InlineStack>
                  <InlineStack gap="200">
                    <Icon source="checkmark" />
                    <Text as="p" variant="bodyMd">Advanced analytics</Text>
                  </InlineStack>
                  <InlineStack gap="200">
                    <Icon source="checkmark" />
                    <Text as="p" variant="bodyMd">Custom reporting</Text>
                  </InlineStack>
                  <InlineStack gap="200">
                    <Icon source="checkmark" />
                    <Text as="p" variant="bodyMd">Priority support</Text>
                  </InlineStack>
                  <InlineStack gap="200">
                    <Icon source="checkmark" />
                    <Text as="p" variant="bodyMd">API access</Text>
                  </InlineStack>
                </BlockStack>
                <div style={{ marginTop: '2rem' }}>
                  <Button variant="primary" size="large" onClick={handleGetStarted}>
                    Start Free Trial
                  </Button>
                </div>
              </div>
            </Card>
            <Card>
              <div style={{ textAlign: 'center', padding: '2rem', maxWidth: '350px' }}>
                <Text as="h3" variant="headingMd">Enterprise</Text>
                <div style={{ margin: '1rem 0' }}>
                  <Text as="p" variant="heading2xl">$199</Text>
                  <Text as="p" variant="bodyMd" tone="subdued">per month</Text>
                </div>
                <BlockStack gap="200" align="start">
                  <InlineStack gap="200">
                    <Icon source="checkmark" />
                    <Text as="p" variant="bodyMd">Unlimited orders</Text>
                  </InlineStack>
                  <InlineStack gap="200">
                    <Icon source="checkmark" />
                    <Text as="p" variant="bodyMd">White-label options</Text>
                  </InlineStack>
                  <InlineStack gap="200">
                    <Icon source="checkmark" />
                    <Text as="p" variant="bodyMd">Dedicated support</Text>
                  </InlineStack>
                  <InlineStack gap="200">
                    <Icon source="checkmark" />
                    <Text as="p" variant="bodyMd">Custom integrations</Text>
                  </InlineStack>
                  <InlineStack gap="200">
                    <Icon source="checkmark" />
                    <Text as="p" variant="bodyMd">SLA guarantee</Text>
                  </InlineStack>
                </BlockStack>
                <div style={{ marginTop: '2rem' }}>
                  <Button variant="secondary" size="large" onClick={handleGetStarted}>
                    Contact Sales
                  </Button>
                </div>
              </div>
            </Card>
          </div>
        </Layout.Section>

        {/* FAQ */}
        <Layout.Section>
          <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
            <Text as="h2" variant="headingLg">
              ❓ Frequently Asked Questions
            </Text>
          </div>
          <BlockStack gap="400">
            {[
              {
                question: "How does ProfitPeek calculate my true profit margins?",
                answer: "We track your revenue across all platforms (Shopify, Meta Ads, Google Ads, Klaviyo, Postscript) and subtract all costs including COGS (default 40%), processing fees (2.9% + $0.30), shipping costs, ad spend, and other expenses to give you your true net profit with real-time updates."
              },
              {
                question: "Is my data secure with enterprise-grade security?",
                answer: "Yes! We use military-grade encryption for all API keys, implement rate limiting and DDoS protection, provide enterprise security monitoring, and follow bank-level security standards. Your data is encrypted and never stored in plain text."
              },
              {
                question: "What makes ProfitPeek different from other profit tracking tools?",
                answer: "ProfitPeek is the only platform that connects ALL your marketing channels (Shopify, Meta Ads, Google Ads, Klaviyo, Postscript) with real-time WebSocket updates, AI-powered insights, trend forecasting, smart alerts, and enterprise-grade security - all in one unified dashboard."
              }
            ].map((faq, index) => (
              <Card key={index}>
                <div
                  onClick={() => toggleFaq(index)}
                  style={{ width: '100%', textAlign: 'left', padding: '1rem', cursor: 'pointer' }}
                >
                  <InlineStack align="space-between">
                    <Text as="h3" variant="headingMd">{faq.question}</Text>
                    <Icon source={expandedFaq === index ? "chevronUp" : "chevronDown"} />
                  </InlineStack>
                </div>
                <Collapsible
                  open={expandedFaq === index}
                  id={`faq-${index}`}
                  transition={{ duration: '200ms', timingFunction: 'ease-in-out' }}
                >
                  <div style={{ padding: '0 1rem 1rem 1rem' }}>
                    <Text as="p" variant="bodyMd" tone="subdued">
                      {faq.answer}
                    </Text>
                  </div>
                </Collapsible>
              </Card>
            ))}
          </BlockStack>
        </Layout.Section>

        {/* CTA Section */}
        <Layout.Section>
          <Card>
            <div style={{ 
              textAlign: 'center', 
              padding: '4rem 2rem',
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              color: 'white',
              borderRadius: '12px'
            }}>
              <Text as="h2" variant="headingLg">
                🚀 Ready to See Your True Profits?
              </Text>
              <div style={{ margin: '2rem 0' }}>
                <Text as="p" variant="bodyLg">
                  Join hundreds of merchants tracking their profits with the most advanced platform available
                </Text>
              </div>
              <InlineStack gap="400" align="center">
                <Button variant="primary" size="large" onClick={handleDemoClick}>
                  🎯 Try Live Demo
                </Button>
                <Button variant="secondary" size="large" onClick={handleGetStarted}>
                  🔗 Connect Your Store
                </Button>
              </InlineStack>
              <div style={{ marginTop: '2rem' }}>
                <Text as="p" variant="bodySm">
                  ⚡ 14-day free trial • No credit card required • Enterprise security
                </Text>
              </div>
            </div>
          </Card>
        </Layout.Section>
      </Layout>
    </Page>
  );
}
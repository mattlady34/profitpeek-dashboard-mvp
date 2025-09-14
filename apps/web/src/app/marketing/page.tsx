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
  Collapsible,
  List,
  ProgressBar,
  Spinner,
} from '@shopify/polaris';
// import { trackDemoModeStarted, trackEvent } from '../../utils/analytics';

export default function MarketingPage() {
  const [email, setEmail] = useState('');
  const [expandedFaq, setExpandedFaq] = useState<number | null>(null);

  const handleDemoClick = () => {
    // trackDemoModeStarted();
    window.location.href = '/dashboard?demo=1';
  };

  const handleGetStarted = () => {
    // trackEvent('get_started_clicked', { source: 'marketing_page' });
    const shop = prompt('Enter your Shopify store domain (e.g., your-store):');
    if (shop) {
      // Redirect to OAuth flow
      window.location.href = `/auth/start?shop=${shop}`;
    }
  };

  const handleEmailSubmit = () => {
    // trackEvent('email_signup', { email: email });
    alert('Thanks for your interest! We\'ll be in touch soon.');
  };

  const toggleFaq = (index: number) => {
    setExpandedFaq(expandedFaq === index ? null : index);
  };

  return (
    <Page>
      <Layout>
        {/* Hero Section - Enhanced */}
        <Layout.Section>
          <Card>
            <div style={{ 
              textAlign: 'center', 
              padding: '6rem 2rem',
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

        {/* Enterprise Features Grid */}
        <Layout.Section>
          <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
            <Text as="h2" variant="headingLg">
              🚀 Enterprise-Grade Features
            </Text>
            <Text as="p" variant="bodyLg" tone="subdued">
              Built for scale, security, and performance
            </Text>
          </div>
          
          {/* Row 1: Core Features */}
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

          {/* Row 2: Advanced Features */}
          <div style={{ marginTop: '2rem' }}>
            <InlineStack gap="400" wrap={false}>
              <Box minWidth="350px">
                <Card>
                  <BlockStack gap="300">
                    <div style={{ textAlign: 'center' }}>
                      <Text as="p" variant="headingLg">📊</Text>
                      <Text as="h3" variant="headingMd">Advanced Analytics</Text>
                    </div>
                    <Text as="p" variant="bodyMd" tone="subdued">
                      CPA, CPC, CPM analysis, revenue attribution, and cross-platform performance metrics.
                    </Text>
                    <Badge tone="info">Deep Analytics</Badge>
                  </BlockStack>
                </Card>
              </Box>
              <Box minWidth="350px">
                <Card>
                  <BlockStack gap="300">
                    <div style={{ textAlign: 'center' }}>
                      <Text as="p" variant="headingLg">🚨</Text>
                      <Text as="h3" variant="headingMd">Smart Alerts</Text>
                    </div>
                    <Text as="p" variant="bodyMd" tone="subdued">
                      Automated alerts for profit drops, cost spikes, ROAS declines, and optimization opportunities.
                    </Text>
                    <Badge tone="warning">Smart Monitoring</Badge>
                  </BlockStack>
                </Card>
              </Box>
              <Box minWidth="350px">
                <Card>
                  <BlockStack gap="300">
                    <div style={{ textAlign: 'center' }}>
                      <Text as="p" variant="headingLg">🔄</Text>
                      <Text as="h3" variant="headingMd">Auto Sync</Text>
                    </div>
                    <Text as="p" variant="bodyMd" tone="subdued">
                      Automatic data synchronization with retry logic, health monitoring, and error recovery.
                    </Text>
                    <Badge tone="success">Reliable Sync</Badge>
                  </BlockStack>
                </Card>
              </Box>
            </InlineStack>
          </div>
        </Layout.Section>

        {/* Profit Calculation Showcase */}
        <Layout.Section>
          <Card>
            <div style={{ textAlign: 'center', padding: '3rem 2rem' }}>
              <Text as="h2" variant="headingLg">
                💰 See Your True Profit Calculation
              </Text>
              <div style={{ margin: '2rem 0', maxWidth: '600px', marginLeft: 'auto', marginRight: 'auto' }}>
                <div style={{ 
                  background: '#f6f6f7', 
                  padding: '2rem', 
                  borderRadius: '8px',
                  textAlign: 'left'
                }}>
                  <BlockStack gap="200">
                    <InlineStack align="space-between">
                      <Text as="p" variant="bodyMd">Total Revenue</Text>
                      <Text as="p" variant="bodyMd" fontWeight="bold">$50,000</Text>
                    </InlineStack>
                    <Divider />
                    <InlineStack align="space-between">
                      <Text as="p" variant="bodyMd">COGS (40%)</Text>
                      <Text as="p" variant="bodyMd" tone="critical">-$20,000</Text>
                    </InlineStack>
                    <InlineStack align="space-between">
                      <Text as="p" variant="bodyMd">Processing Fees</Text>
                      <Text as="p" variant="bodyMd" tone="critical">-$1,500</Text>
                    </InlineStack>
                    <InlineStack align="space-between">
                      <Text as="p" variant="bodyMd">Shipping Costs</Text>
                      <Text as="p" variant="bodyMd" tone="critical">-$2,000</Text>
                    </InlineStack>
                    <InlineStack align="space-between">
                      <Text as="p" variant="bodyMd">Ad Spend</Text>
                      <Text as="p" variant="bodyMd" tone="critical">-$8,000</Text>
                    </InlineStack>
                    <Divider />
                    <InlineStack align="space-between">
                      <Text as="p" variant="bodyMd" fontWeight="bold">Net Profit</Text>
                      <Text as="p" variant="bodyMd" fontWeight="bold" tone="success">$18,500</Text>
                    </InlineStack>
                    <InlineStack align="space-between">
                      <Text as="p" variant="bodyMd">Profit Margin</Text>
                      <Text as="p" variant="bodyMd" fontWeight="bold" tone="success">37%</Text>
                    </InlineStack>
                  </BlockStack>
                </div>
              </div>
              <Text as="p" variant="bodyMd" tone="subdued">
                Track every cost across all platforms for accurate profit calculations
              </Text>
            </div>
          </Card>
        </Layout.Section>

        {/* Social Proof - Enhanced */}
        <Layout.Section>
          <Card>
            <div style={{ textAlign: 'center', padding: '3rem 2rem' }}>
              <Text as="h2" variant="headingLg">
                🏆 Trusted by Growing E-commerce Businesses
              </Text>
              <div style={{ margin: '2rem 0' }}>
                <InlineStack gap="400" wrap={false} align="center">
                  <Box minWidth="300px">
                    <Card>
                      <BlockStack gap="200" align="center">
                        <Text as="p" variant="headingLg">⭐⭐⭐⭐⭐</Text>
                        <Text as="p" variant="bodyLg">
                          "Finally, I can see my true margins across all platforms! The real-time tracking is incredible."
                        </Text>
                        <Text as="p" variant="bodySm" tone="subdued">
                          - Sarah Chen, Fashion Store ($2M ARR)
                        </Text>
                      </BlockStack>
                    </Card>
                  </Box>
                  <Box minWidth="300px">
                    <Card>
                      <BlockStack gap="200" align="center">
                        <Text as="p" variant="headingLg">⭐⭐⭐⭐⭐</Text>
                        <Text as="p" variant="bodyLg">
                          "The AI insights helped me optimize my ad spend and increase profits by 40%."
                        </Text>
                        <Text as="p" variant="bodySm" tone="subdued">
                          - Mike Rodriguez, Dropshipping ($5M ARR)
                        </Text>
                      </BlockStack>
                    </Card>
                  </Box>
                  <Box minWidth="300px">
                    <Card>
                      <BlockStack gap="200" align="center">
                        <Text as="p" variant="headingLg">⭐⭐⭐⭐⭐</Text>
                        <Text as="p" variant="bodyLg">
                          "Enterprise-grade security and real-time alerts give me peace of mind."
                        </Text>
                        <Text as="p" variant="bodySm" tone="subdued">
                          - Jennifer Kim, Electronics ($10M ARR)
                        </Text>
                      </BlockStack>
                    </Card>
                  </Box>
                </InlineStack>
              </div>
            </div>
          </Card>
        </Layout.Section>

        {/* Pricing - Enhanced */}
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

        {/* FAQ - Enhanced */}
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
              },
              {
                question: "Can I customize the profit calculations for my business?",
                answer: "Absolutely! You can adjust COGS percentages, processing fees, shipping costs, and other settings to match your specific business model. We also support custom cost categories and automated cost tracking."
              },
              {
                question: "Do you offer real-time tracking and alerts?",
                answer: "Yes! ProfitPeek provides real-time profit tracking with WebSocket connections, live dashboard updates, smart alerts for profit drops and cost spikes, and automated notifications for optimization opportunities."
              },
              {
                question: "What platforms can I connect to ProfitPeek?",
                answer: "Currently, we support Shopify (e-commerce), Meta Ads (Facebook/Instagram), Google Ads, Klaviyo (email marketing), and Postscript (SMS marketing). We're constantly adding new platform integrations based on user demand."
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

        {/* CTA Section - Enhanced */}
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
'use client';

import { useState } from 'react';
import {
  Page,
  Layout,
  Card,
  BlockStack,
  Text,
  TextField,
  Button,
  Select,
  InlineStack,
  Banner,
  Divider,
  DropZone,
  Icon,
  Box,
} from '@shopify/polaris';

export default function Settings() {
  const [profitPresets, setProfitPresets] = useState({
    feeFallback: '2.9',
    shippingRule: 'flat',
    adSpendFacebook: '',
    adSpendGoogle: '',
  });

  const [timeDigest, setTimeDigest] = useState({
    timezone: 'pacific',
    sendTime: '08:00',
    email: 'founder@company.com',
  });

  const [costs, setCosts] = useState<{
    csvFile: File | null;
  }>({
    csvFile: null,
  });

  const handleFeeFallbackChange = (value: string) => {
    setProfitPresets(prev => ({ ...prev, feeFallback: value }));
  };

  const handleShippingRuleChange = (value: string) => {
    setProfitPresets(prev => ({ ...prev, shippingRule: value }));
  };

  const handleTimezoneChange = (value: string) => {
    setTimeDigest(prev => ({ ...prev, timezone: value }));
  };

  const handleSendTimeChange = (value: string) => {
    setTimeDigest(prev => ({ ...prev, sendTime: value }));
  };

  const handleEmailChange = (value: string) => {
    setTimeDigest(prev => ({ ...prev, email: value }));
  };

  const handleTestEmail = () => {
    console.log('Sending test email to:', timeDigest.email);
  };

  const handleSavePresets = () => {
    console.log('Saving profit presets:', profitPresets);
  };

  const handleFileDrop = (files: File[]) => {
    if (files.length > 0) {
      setCosts(prev => ({ ...prev, csvFile: files[0] }));
    }
  };

  return (
    <Page
      title="Settings"
      subtitle="Configure profit calculations and notifications"
    >
      <Layout>
        {/* Settings Cards */}
        <Layout.Section>
          <InlineStack gap="400" wrap={false}>
            {/* Profit Presets Card */}
            <Box minWidth="300px">
              <Card>
                <BlockStack gap="400">
                  <InlineStack gap="200">
                    <Icon source="calculator" />
                    <Text as="h3" variant="headingMd">Profit Presets</Text>
                  </InlineStack>
                  <Text as="p" variant="bodyMd" tone="subdued">Configure default calculations</Text>
                  
                  <BlockStack gap="300">
                    <TextField
                      label="Fee Fallback Rate"
                      value={profitPresets.feeFallback}
                      onChange={handleFeeFallbackChange}
                      suffix="%"
                      helpText="Default processing fee percentage when not available"
                      autoComplete="off"
                    />
                    
                    <Select
                      label="Shipping Rule"
                      options={[
                        { label: 'Flat rate: $12', value: 'flat' },
                        { label: 'Percentage of order', value: 'percentage' },
                        { label: 'Free shipping threshold', value: 'threshold' },
                      ]}
                      value={profitPresets.shippingRule}
                      onChange={handleShippingRuleChange}
                    />
                    
                    <BlockStack gap="200">
                      <Text as="p" variant="bodyMd" tone="subdued">Ad Spend Fields</Text>
                      <InlineStack gap="200">
                        <Button size="slim">Facebook Ads</Button>
                        <Button size="slim">Google Ads</Button>
                      </InlineStack>
                    </BlockStack>
                  </BlockStack>
                  
                  <Button variant="primary" onClick={handleSavePresets}>
                    Save Presets
                  </Button>
                </BlockStack>
              </Card>
            </Box>

            {/* Time & Digest Card */}
            <Box minWidth="300px">
              <Card>
                <BlockStack gap="400">
                  <InlineStack gap="200">
                    <Icon source="clock" />
                    <Text as="h3" variant="headingMd">Time & Digest</Text>
                  </InlineStack>
                  <Text as="p" variant="bodyMd" tone="subdued">Daily email preferences</Text>
                  
                  <BlockStack gap="300">
                    <Select
                      label="Timezone"
                      options={[
                        { label: 'Pacific Time (PT)', value: 'pacific' },
                        { label: 'Eastern Time (ET)', value: 'eastern' },
                        { label: 'Central Time (CT)', value: 'central' },
                        { label: 'Mountain Time (MT)', value: 'mountain' },
                      ]}
                      value={timeDigest.timezone}
                      onChange={handleTimezoneChange}
                    />
                    
                    <TextField
                      label="Daily Send Time"
                      type="time"
                      value={timeDigest.sendTime}
                      onChange={handleSendTimeChange}
                      helpText="Time to send daily profit digest"
                      autoComplete="off"
                    />
                    
                    <TextField
                      label="Email Address"
                      type="email"
                      value={timeDigest.email}
                      onChange={handleEmailChange}
                      placeholder="founder@company.com"
                      autoComplete="email"
                    />
                  </BlockStack>
                  
                  <Button onClick={handleTestEmail}>
                    Send Test Email
                  </Button>
                </BlockStack>
              </Card>
            </Box>

            {/* Costs Import Card */}
            <Box minWidth="300px">
              <Card>
                <BlockStack gap="400">
                  <InlineStack gap="200">
                    <Icon source="upload" />
                    <Text as="h3" variant="headingMd">Costs Import</Text>
                  </InlineStack>
                  <Text as="p" variant="bodyMd" tone="subdued">Bulk upload unit costs</Text>
                  
                  <BlockStack gap="300">
                    <DropZone
                      onDrop={handleFileDrop}
                      accept=".csv"
                      type="file"
                    >
                      <DropZone.FileUpload />
                      <BlockStack gap="200" align="center">
                        <Icon source="cloud" />
                        <Text as="p" variant="bodyMd">
                          Drop your CSV file here or{' '}
                          <Button variant="tertiary" size="slim">
                            browse files
                          </Button>
                        </Text>
                      </BlockStack>
                    </DropZone>
                    
                    <Button variant="tertiary" onClick={() => window.open('/api/cost-template.csv')}>
                      Download CSV template
                    </Button>
                    
                    <Text as="p" variant="bodySm" tone="subdued">
                      Format: SKU, Unit Cost, Currency
                    </Text>
                    <Text as="p" variant="bodySm" tone="subdued">
                      Max file size: 5MB
                    </Text>
                  </BlockStack>
                </BlockStack>
              </Card>
            </Box>
          </InlineStack>
        </Layout.Section>
      </Layout>
    </Page>
  );
}

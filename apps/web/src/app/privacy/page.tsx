'use client';

import React from 'react';
import { Page, Layout, Card, Text, List, Link, BlockStack } from '@shopify/polaris';

export default function PrivacyPolicy() {
  return (
    <Page title="Privacy Policy" subtitle="Last updated: December 2024">
      <Layout>
        <Layout.Section>
          <Card>
            <BlockStack gap="400">
              <Text variant="headingMd" as="h2">
                Introduction
              </Text>
              <Text as="p">
                ProfitPeek ("we," "our," or "us") is committed to protecting your privacy. 
                This Privacy Policy explains how we collect, use, disclose, and safeguard 
                your information when you use our profit tracking and analytics service.
              </Text>

              <Text variant="headingMd" as="h2">
                Information We Collect
              </Text>
              
              <Text variant="headingSm" as="h3">
                Personal Information
              </Text>
              <List type="bullet">
                <List.Item>Business name and contact information</List.Item>
                <List.Item>Email address</List.Item>
                <List.Item>Shopify store information (with your permission)</List.Item>
                <List.Item>Social media account information (Facebook, Google, etc.)</List.Item>
              </List>

              <Text variant="headingSm" as="h3">
                Business Data
              </Text>
              <List type="bullet">
                <List.Item>Sales and revenue data from connected platforms</List.Item>
                <List.Item>Advertising spend and performance metrics</List.Item>
                <List.Item>Email marketing campaign data</List.Item>
                <List.Item>SMS marketing campaign data</List.Item>
                <List.Item>Product and order information</List.Item>
              </List>

              <Text variant="headingSm" as="h3">
                Technical Information
              </Text>
              <List type="bullet">
                <List.Item>IP address and device information</List.Item>
                <List.Item>Browser type and version</List.Item>
                <List.Item>Usage patterns and analytics data</List.Item>
                <List.Item>Cookies and similar tracking technologies</List.Item>
              </List>

              <Text variant="headingMd" as="h2">
                How We Use Your Information
              </Text>
              <List type="bullet">
                <List.Item>Provide and maintain our profit tracking services</List.Item>
                <List.Item>Analyze your business performance and generate insights</List.Item>
                <List.Item>Sync data across your connected platforms</List.Item>
                <List.Item>Send you service-related communications</List.Item>
                <List.Item>Improve our services and develop new features</List.Item>
                <List.Item>Comply with legal obligations</List.Item>
              </List>

              <Text variant="headingMd" as="h2">
                Data Sharing and Disclosure
              </Text>
              
              <Text variant="headingSm" as="h3">
                We may share your information with:
              </Text>
              <List type="bullet">
                <List.Item>
                  <strong>Connected Platforms:</strong> Shopify, Facebook, Google Ads, Klaviyo, Postscript 
                  (only with your explicit permission and only the data necessary for integration)
                </List.Item>
                <List.Item>
                  <strong>Service Providers:</strong> Third-party vendors who help us operate our service
                </List.Item>
                <List.Item>
                  <strong>Legal Requirements:</strong> When required by law or to protect our rights
                </List.Item>
                <List.Item>
                  <strong>Business Transfers:</strong> In connection with a merger, acquisition, or sale of assets
                </List.Item>
              </List>

              <Text variant="headingMd" as="h2">
                Data Security
              </Text>
              <Text as="p">
                We implement appropriate technical and organizational measures to protect your 
                personal information against unauthorized access, alteration, disclosure, or 
                destruction. This includes:
              </Text>
              <List type="bullet">
                <List.Item>Encryption of data in transit and at rest</List.Item>
                <List.Item>Regular security audits and updates</List.Item>
                <List.Item>Access controls and authentication</List.Item>
                <List.Item>Secure data centers and infrastructure</List.Item>
              </List>

              <Text variant="headingMd" as="h2">
                Your Rights and Choices
              </Text>
              <List type="bullet">
                <List.Item>
                  <strong>Access:</strong> Request access to your personal information
                </List.Item>
                <List.Item>
                  <strong>Correction:</strong> Request correction of inaccurate information
                </List.Item>
                <List.Item>
                  <strong>Deletion:</strong> Request deletion of your personal information
                </List.Item>
                <List.Item>
                  <strong>Portability:</strong> Request a copy of your data in a portable format
                </List.Item>
                <List.Item>
                  <strong>Opt-out:</strong> Unsubscribe from marketing communications
                </List.Item>
                <List.Item>
                  <strong>Data Processing:</strong> Object to certain processing of your data
                </List.Item>
              </List>

              <Text variant="headingMd" as="h2">
                Third-Party Integrations
              </Text>
              <Text as="p">
                Our service integrates with third-party platforms. Each platform has its own 
                privacy policy and data practices. We encourage you to review their privacy 
                policies:
              </Text>
              <List type="bullet">
                <List.Item>
                  <Link url="https://www.shopify.com/legal/privacy" external>
                    Shopify Privacy Policy
                  </Link>
                </List.Item>
                <List.Item>
                  <Link url="https://www.facebook.com/privacy/policy" external>
                    Facebook Privacy Policy
                  </Link>
                </List.Item>
                <List.Item>
                  <Link url="https://policies.google.com/privacy" external>
                    Google Privacy Policy
                  </Link>
                </List.Item>
                <List.Item>
                  <Link url="https://www.klaviyo.com/legal/privacy" external>
                    Klaviyo Privacy Policy
                  </Link>
                </List.Item>
                <List.Item>
                  <Link url="https://postscript.io/privacy" external>
                    Postscript Privacy Policy
                  </Link>
                </List.Item>
              </List>

              <Text variant="headingMd" as="h2">
                Data Retention
              </Text>
              <Text as="p">
                We retain your personal information for as long as necessary to provide our 
                services and fulfill the purposes outlined in this Privacy Policy, unless a 
                longer retention period is required or permitted by law. When you delete your 
                account, we will delete or anonymize your personal information within 30 days.
              </Text>

              <Text variant="headingMd" as="h2">
                International Data Transfers
              </Text>
              <Text as="p">
                Your information may be transferred to and processed in countries other than 
                your own. We ensure appropriate safeguards are in place to protect your 
                information in accordance with this Privacy Policy and applicable data 
                protection laws.
              </Text>

              <Text variant="headingMd" as="h2">
                Children's Privacy
              </Text>
              <Text as="p">
                Our service is not intended for children under 13 years of age. We do not 
                knowingly collect personal information from children under 13. If you are a 
                parent or guardian and believe your child has provided us with personal 
                information, please contact us.
              </Text>

              <Text variant="headingMd" as="h2">
                Changes to This Privacy Policy
              </Text>
              <Text as="p">
                We may update this Privacy Policy from time to time. We will notify you of 
                any changes by posting the new Privacy Policy on this page and updating the 
                "Last updated" date. You are advised to review this Privacy Policy periodically 
                for any changes.
              </Text>

              <Text variant="headingMd" as="h2">
                Contact Us
              </Text>
              <Text as="p">
                If you have any questions about this Privacy Policy or our privacy practices, 
                please contact us:
              </Text>
              <List type="bullet">
                <List.Item>Email: privacy@profitpeek.com</List.Item>
                <List.Item>Website: https://profitpeek-dashboard-mvp.netlify.app</List.Item>
                <List.Item>Address: [Your Business Address]</List.Item>
              </List>

              <Text variant="headingMd" as="h2">
                Compliance
              </Text>
              <Text as="p">
                This Privacy Policy complies with applicable data protection laws, including:
              </Text>
              <List type="bullet">
                <List.Item>General Data Protection Regulation (GDPR)</List.Item>
                <List.Item>California Consumer Privacy Act (CCPA)</List.Item>
                <List.Item>Personal Information Protection and Electronic Documents Act (PIPEDA)</List.Item>
                <List.Item>Other applicable privacy laws</List.Item>
              </List>

              <Text as="p" variant="bodyMd" tone="subdued">
                <em>
                  This Privacy Policy is effective as of December 2024 and will remain in effect 
                  except with respect to any changes in its provisions in the future, which will 
                  be in effect immediately after being posted on this page.
                </em>
              </Text>
            </BlockStack>
          </Card>
        </Layout.Section>
      </Layout>
    </Page>
  );
}

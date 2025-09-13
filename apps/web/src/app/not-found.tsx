'use client';

import { Page, Layout, Card, BlockStack, Text, Button } from '@shopify/polaris';
import Link from 'next/link';

export default function NotFound() {
  return (
    <Page title="Page Not Found">
      <Layout>
        <Layout.Section>
          <Card>
            <BlockStack gap="400" align="center">
              <Text as="h1" variant="heading2xl">
                404 - Page Not Found
              </Text>
              <Text as="p" variant="bodyMd" tone="subdued">
                The page you're looking for doesn't exist.
              </Text>
              <Link href="/dashboard">
                <Button variant="primary">
                  Go to Dashboard
                </Button>
              </Link>
            </BlockStack>
          </Card>
        </Layout.Section>
      </Layout>
    </Page>
  );
}

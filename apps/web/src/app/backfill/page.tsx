'use client';

import { useState, useEffect } from 'react';
import {
  Page,
  Layout,
  Card,
  BlockStack,
  Text,
  Badge,
  Button,
  InlineStack,
  SkeletonDisplayText,
  SkeletonBodyText,
  Banner,
} from '@shopify/polaris';
import { RefreshIcon, CheckIcon, AlertBubbleIcon } from '@shopify/polaris-icons';

interface BackfillJob {
  id: string;
  name: string;
  status: 'completed' | 'running' | 'failed' | 'pending';
  progress: number;
  startedAt: string;
  completedAt?: string;
  recordsProcessed: number;
  totalRecords: number;
}

export default function Backfill() {
  const [jobs, setJobs] = useState<BackfillJob[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchBackfillJobs = async () => {
      try {
        setLoading(true);
        setError(null);
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'https://profitpeek-dashboard.onrender.com';
        const response = await fetch(`${apiUrl}/api/backfill?shop=profitpeekteststore.myshopify.com`);
        
        if (!response.ok) {
          throw new Error('Failed to fetch backfill jobs');
        }
        
        const result = await response.json();
        setJobs(result.jobs || []);
      } catch (err) {
        console.error('Backfill fetch error:', err);
        setError(err instanceof Error ? err.message : 'Unknown error occurred');
        // Use demo data
        setJobs([
          {
            id: '1',
            name: 'Historical Orders Import',
            status: 'completed',
            progress: 100,
            startedAt: '2025-01-15T10:00:00Z',
            completedAt: '2025-01-15T10:45:00Z',
            recordsProcessed: 1250,
            totalRecords: 1250,
          },
          {
            id: '2',
            name: 'Product Cost Data Sync',
            status: 'running',
            progress: 65,
            startedAt: '2025-01-15T11:00:00Z',
            recordsProcessed: 650,
            totalRecords: 1000,
          },
          {
            id: '3',
            name: 'Fee Calculation Update',
            status: 'failed',
            progress: 30,
            startedAt: '2025-01-15T12:00:00Z',
            recordsProcessed: 300,
            totalRecords: 1000,
          },
        ]);
      } finally {
        setLoading(false);
      }
    };

    fetchBackfillJobs();
  }, []);

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'completed':
        return <Badge icon={CheckIcon}>Completed</Badge>;
      case 'running':
        return <Badge icon={RefreshIcon}>Running</Badge>;
      case 'failed':
        return <Badge icon={AlertBubbleIcon}>Failed</Badge>;
      case 'pending':
        return <Badge>Pending</Badge>;
      default:
        return <Badge>{status}</Badge>;
    }
  };

  const handleRetryJob = (jobId: string) => {
    console.log('Retrying job:', jobId);
    // Implement retry logic
  };

  const handleStartNewJob = () => {
    console.log('Starting new backfill job');
    // Implement new job logic
  };

  if (loading) {
    return (
      <Page title="Backfill">
        <Layout>
          <Layout.Section>
            <Card>
              <div role="status" aria-live="polite" aria-label="Loading backfill data">
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

  return (
    <Page
      title="Backfill"
      subtitle="Historical data import and synchronization"
      primaryAction={{
        content: 'Start New Job',
        onAction: handleStartNewJob,
      }}
    >
      <Layout>
        {/* Error Banner */}
        {error && (
          <Layout.Section>
            <Banner tone="critical" title="API Error">
              <p>Failed to load backfill data: {error}. Displaying demo data as a fallback.</p>
            </Banner>
          </Layout.Section>
        )}

        {/* What is Backfill Card */}
        <Layout.Section>
          <Card>
            <BlockStack gap="400">
              <Text variant="headingMd" as="h3">What is Backfill?</Text>
              <Text as="p" variant="bodyMd" tone="subdued">
                Backfill processes import historical data from your Shopify store to calculate accurate profit margins. 
                This includes orders, products, and cost data that may not have been tracked when orders were originally placed.
              </Text>
              <Text as="p" variant="bodyMd" tone="subdued">
                Backfill jobs run in the background and can take several hours depending on the amount of historical data.
              </Text>
            </BlockStack>
          </Card>
        </Layout.Section>

        {/* Backfill Jobs */}
        <Layout.Section>
          <Card>
            <BlockStack gap="400">
              <Text variant="headingMd" as="h3">Recent Backfill Jobs</Text>
              
              <BlockStack gap="300">
                {jobs.map((job) => (
                  <Card key={job.id}>
                    <BlockStack gap="300">
                      <InlineStack align="space-between">
                        <BlockStack gap="100">
                          <Text as="p" variant="bodyMd" fontWeight="semibold">
                            {job.name}
                          </Text>
                          <Text as="p" variant="bodySm" tone="subdued">
                            Started: {new Date(job.startedAt).toLocaleString()}
                          </Text>
                          {job.completedAt && (
                            <Text as="p" variant="bodySm" tone="subdued">
                              Completed: {new Date(job.completedAt).toLocaleString()}
                            </Text>
                          )}
                        </BlockStack>
                        <InlineStack gap="200" align="end">
                          {getStatusBadge(job.status)}
                          {job.status === 'failed' && (
                            <Button size="slim" onClick={() => handleRetryJob(job.id)}>
                              Retry
                            </Button>
                          )}
                        </InlineStack>
                      </InlineStack>
                      
                      <InlineStack align="space-between">
                        <Text as="p" variant="bodySm" tone="subdued">
                          {job.recordsProcessed.toLocaleString()} of {job.totalRecords.toLocaleString()} records processed
                        </Text>
                        <Text as="p" variant="bodySm" tone="subdued">
                          {job.progress}%
                        </Text>
                      </InlineStack>
                      
                      {job.status === 'running' && (
                        <div style={{ width: '100%', height: '4px', backgroundColor: '#f0f0f0', borderRadius: '2px' }}>
                          <div 
                            style={{ 
                              width: `${job.progress}%`, 
                              height: '100%', 
                              backgroundColor: '#008060', 
                              borderRadius: '2px',
                              transition: 'width 0.3s ease'
                            }} 
                          />
                        </div>
                      )}
                    </BlockStack>
                  </Card>
                ))}
              </BlockStack>
            </BlockStack>
          </Card>
        </Layout.Section>
      </Layout>
    </Page>
  );
}
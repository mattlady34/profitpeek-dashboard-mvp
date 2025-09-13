'use client';

import { useState, useEffect } from 'react';
import {
  Page,
  Layout,
  Card,
  DataTable,
  BlockStack,
  Text,
  Badge,
  Button,
  Sheet,
  InlineStack,
  Divider,
  SkeletonDisplayText,
  SkeletonBodyText,
  TextField,
  Select,
} from '@shopify/polaris';

interface Order {
  id: string;
  date: string;
  orderNumber: string;
  customer: string;
  revenue: number;
  cogs: number;
  fees: number;
  shipping: number;
  netProfit: number;
  margin: number;
  status: 'fulfilled' | 'processing' | 'returned';
  items: Array<{
    name: string;
    quantity: number;
    unitPrice: number;
    unitCost: number;
    totalRevenue: number;
    totalCost: number;
    profit: number;
    margin: number;
  }>;
}

export default function Orders() {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedOrder, setSelectedOrder] = useState<Order | null>(null);
  const [sheetOpen, setSheetOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        setLoading(true);
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'https://profitpeek-dashboard.onrender.com';
        const response = await fetch(`${apiUrl}/api/orders?shop=profitpeekteststore.myshopify.com`);
        
        if (!response.ok) {
          throw new Error('Failed to fetch orders');
        }
        
        const result = await response.json();
        setOrders(result.orders || []);
      } catch (err) {
        // Use demo data matching the wireframe
        setOrders([
          {
            id: '1',
            date: 'Jan 15, 2025',
            orderNumber: '#1047',
            customer: 'Sarah Johnson',
            revenue: 247.50,
            cogs: 98.20,
            fees: 7.43,
            shipping: 12.00,
            netProfit: 129.87,
            margin: 52.5,
            status: 'fulfilled',
            items: [
              {
                name: 'Premium T-Shirt',
                quantity: 2,
                unitPrice: 123.75,
                unitCost: 49.10,
                totalRevenue: 247.50,
                totalCost: 98.20,
                profit: 149.30,
                margin: 60.3,
              },
            ],
          },
          {
            id: '2',
            date: 'Jan 14, 2025',
            orderNumber: '#1046',
            customer: 'Mike Chen',
            revenue: 89.99,
            cogs: 32.15,
            fees: 2.70,
            shipping: 8.50,
            netProfit: 46.64,
            margin: 51.8,
            status: 'processing',
            items: [
              {
                name: 'Basic Widget',
                quantity: 1,
                unitPrice: 89.99,
                unitCost: 32.15,
                totalRevenue: 89.99,
                totalCost: 32.15,
                profit: 57.84,
                margin: 64.3,
              },
            ],
          },
          {
            id: '3',
            date: 'Jan 14, 2025',
            orderNumber: '#1045',
            customer: 'Emily Davis',
            revenue: 156.00,
            cogs: 62.40,
            fees: 4.68,
            shipping: 10.00,
            netProfit: 78.92,
            margin: 50.6,
            status: 'returned',
            items: [
              {
                name: 'Deluxe Package',
                quantity: 1,
                unitPrice: 156.00,
                unitCost: 62.40,
                totalRevenue: 156.00,
                totalCost: 62.40,
                profit: 93.60,
                margin: 60.0,
              },
            ],
          },
        ]);
      } finally {
        setLoading(false);
      }
    };

    fetchOrders();
  }, []);

  const handleRowClick = (order: Order) => {
    setSelectedOrder(order);
    setSheetOpen(true);
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'fulfilled':
        return <Badge tone="success">Fulfilled</Badge>;
      case 'processing':
        return <Badge tone="info">Processing</Badge>;
      case 'returned':
        return <Badge tone="critical">Returned</Badge>;
      default:
        return <Badge>Unknown</Badge>;
    }
  };

  const filteredOrders = orders.filter(order => {
    const matchesSearch = order.customer.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         order.orderNumber.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesFilter = filterStatus === 'all' || order.status === filterStatus;
    return matchesSearch && matchesFilter;
  });

  const rows = filteredOrders.map((order) => [
    order.date,
    order.orderNumber,
    order.customer,
    `$${order.revenue.toFixed(2)}`,
    `$${order.cogs.toFixed(2)}`,
    `$${order.fees.toFixed(2)}`,
    `$${order.shipping.toFixed(2)}`,
    `$${order.netProfit.toFixed(2)}`,
    `${order.margin.toFixed(1)}%`,
    getStatusBadge(order.status),
    <Button
      key={`view-${order.id}`}
      size="slim"
      variant="tertiary"
      onClick={() => handleRowClick(order)}
    >
      View Details
    </Button>
  ]);

  if (loading) {
    return (
      <Page title="Recent Orders">
        <Layout>
          <Layout.Section>
            <Card>
              <BlockStack gap="400">
                <SkeletonDisplayText size="large" />
                <SkeletonBodyText lines={5} />
              </BlockStack>
            </Card>
          </Layout.Section>
        </Layout>
      </Page>
    );
  }

  return (
    <>
      <Page
        title="Recent Orders"
        subtitle="Order-by-order profit breakdown"
      >
        <Layout>
          <Layout.Section>
            <Card>
              <BlockStack gap="400">
                <InlineStack align="space-between">
                  <Text as="h3" variant="headingMd">Recent Orders</Text>
                  <InlineStack gap="200">
                    <TextField
                      label="Search orders"
                      labelHidden
                      value={searchQuery}
                      onChange={setSearchQuery}
                      placeholder="Search orders..."
                      autoComplete="off"
                    />
                    <Select
                      label="Filter"
                      labelHidden
                      options={[
                        { label: 'All Status', value: 'all' },
                        { label: 'Fulfilled', value: 'fulfilled' },
                        { label: 'Processing', value: 'processing' },
                        { label: 'Returned', value: 'returned' },
                      ]}
                      value={filterStatus}
                      onChange={setFilterStatus}
                    />
                    <Button variant="tertiary">View all orders</Button>
                  </InlineStack>
                </InlineStack>
                
                <DataTable
                  columnContentTypes={['text', 'text', 'text', 'text', 'text', 'text', 'text', 'text', 'text', 'text', 'text']}
                  headings={['DATE', 'ORDER #', 'CUSTOMER', 'REVENUE', 'COGS', 'FEES', 'SHIPPING', 'NET PROFIT', 'MARGIN', 'STATUS', 'ACTIONS']}
                  rows={rows}
                />
              </BlockStack>
            </Card>
          </Layout.Section>
        </Layout>
      </Page>

      {/* Order Sheet */}
      <Sheet
        open={sheetOpen}
        onClose={() => setSheetOpen(false)}
        accessibilityLabel="Order Details"
      >
        <div style={{ padding: '20px' }}>
          {selectedOrder && (
            <BlockStack gap="400">
              <Text as="h2" variant="headingLg">
                Order Details - {selectedOrder.orderNumber}
              </Text>
              
              <BlockStack gap="400">
                <Text as="h3" variant="headingMd">
                  Order Summary
                </Text>
                
                <InlineStack gap="400">
                  <BlockStack gap="200">
                    <Text as="p" variant="bodyMd" tone="subdued">Revenue</Text>
                    <Text as="p" variant="headingMd">${selectedOrder.revenue.toFixed(2)}</Text>
                  </BlockStack>
                  <BlockStack gap="200">
                    <Text as="p" variant="bodyMd" tone="subdued">COGS</Text>
                    <Text as="p" variant="headingMd">${selectedOrder.cogs.toFixed(2)}</Text>
                  </BlockStack>
                  <BlockStack gap="200">
                    <Text as="p" variant="bodyMd" tone="subdued">Fees</Text>
                    <Text as="p" variant="headingMd">${selectedOrder.fees.toFixed(2)}</Text>
                  </BlockStack>
                  <BlockStack gap="200">
                    <Text as="p" variant="bodyMd" tone="subdued">Shipping</Text>
                    <Text as="p" variant="headingMd">${selectedOrder.shipping.toFixed(2)}</Text>
                  </BlockStack>
                  <BlockStack gap="200">
                    <Text as="p" variant="bodyMd" tone="subdued">Net Profit</Text>
                    <Text as="p" variant="headingMd" tone="success">${selectedOrder.netProfit.toFixed(2)}</Text>
                  </BlockStack>
                  <BlockStack gap="200">
                    <Text as="p" variant="bodyMd" tone="subdued">Margin</Text>
                    <Text as="p" variant="headingMd" tone="success">{selectedOrder.margin.toFixed(1)}%</Text>
                  </BlockStack>
                </InlineStack>

                <Divider />

                <Text as="h3" variant="headingMd">
                  Itemized Breakdown
                </Text>

                <DataTable
                  columnContentTypes={['text', 'text', 'text', 'text', 'text', 'text', 'text', 'text']}
                  headings={['Item', 'Qty', 'Unit Price', 'Unit Cost', 'Total Revenue', 'Total Cost', 'Profit', 'Margin']}
                  rows={selectedOrder.items.map(item => [
                    item.name,
                    item.quantity.toString(),
                    `$${item.unitPrice.toFixed(2)}`,
                    `$${item.unitCost.toFixed(2)}`,
                    `$${item.totalRevenue.toFixed(2)}`,
                    `$${item.totalCost.toFixed(2)}`,
                    `$${item.profit.toFixed(2)}`,
                    `${item.margin.toFixed(1)}%`,
                  ])}
                />
              </BlockStack>
            </BlockStack>
          )}
        </div>
      </Sheet>
    </>
  );
}

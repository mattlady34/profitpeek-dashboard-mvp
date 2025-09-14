# 🏗️ ProfitPeek Data Integration Architecture

## **Overview**
ProfitPeek will integrate with multiple platforms to provide a unified view of revenue, costs, and profit across all channels.

## **Data Sources**

### **Revenue Sources**
1. **Shopify** - Orders, products, customers, transactions
2. **Facebook Ads** - Ad spend, conversions, ROAS
3. **Google Ads** - Campaign performance, costs, conversions
4. **Other Channels** - Amazon, eBay, direct sales

### **Cost Sources**
1. **Shopify** - Product costs, shipping, fees
2. **Facebook Ads** - Ad spend, campaign costs
3. **Google Ads** - Campaign spend, keyword costs
4. **Klaviyo** - Email marketing costs
5. **Postscript** - SMS marketing costs
6. **Other Tools** - Influencer costs, affiliate fees

### **Profit Calculation**
```
Net Profit = Total Revenue - Total Costs
Total Revenue = Shopify Revenue + Other Channel Revenue
Total Costs = COGS + Marketing Costs + Platform Fees + Other Costs
```

## **Data Flow Architecture**

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Shopify   │    │  Facebook   │    │   Google    │
│    API      │    │    API      │    │    API      │
└──────┬──────┘    └──────┬──────┘    └──────┬──────┘
       │                  │                  │
       ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────┐
│              Data Integration Layer                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│  │   Shopify   │  │  Facebook   │  │   Google    │ │
│  │  Connector  │  │  Connector  │  │  Connector  │ │
│  └─────────────┘  └─────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────┘
       │                  │                  │
       ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────┐
│              Data Processing Layer                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│  │   Revenue   │  │    Cost     │  │   Profit    │ │
│  │  Processor  │  │  Processor  │  │ Calculator  │ │
│  └─────────────┘  └─────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────┘
       │                  │                  │
       ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────┐
│              Unified Data Store                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│  │   Orders    │  │  Campaigns  │  │   Products  │ │
│  │   Table     │  │   Table     │  │   Table     │ │
│  └─────────────┘  └─────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────┘
       │                  │                  │
       ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────┐
│              Dashboard & Analytics                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│  │   Revenue   │  │    Cost     │  │   Profit    │ │
│  │  Dashboard  │  │  Dashboard  │  │  Dashboard  │ │
│  └─────────────┘  └─────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────┘
```

## **API Integrations**

### **1. Shopify API**
- **Orders**: Revenue, customer data, product details
- **Products**: COGS, inventory, pricing
- **Transactions**: Payment processing fees
- **Customers**: Customer lifetime value

### **2. Facebook Marketing API**
- **Campaigns**: Ad spend, impressions, clicks
- **Conversions**: Purchase events, ROAS
- **Audiences**: Customer acquisition costs

### **3. Google Ads API**
- **Campaigns**: Ad spend, keywords, performance
- **Conversions**: Purchase events, ROAS
- **Keywords**: Cost per click, conversion rates

### **4. Klaviyo API**
- **Email Campaigns**: Send costs, open rates
- **Segments**: Customer segmentation data
- **Events**: Purchase events, customer behavior

### **5. Postscript API**
- **SMS Campaigns**: Send costs, delivery rates
- **Conversions**: Purchase events, ROAS
- **Subscribers**: Customer acquisition costs

## **Data Mapping**

### **Revenue Mapping**
```javascript
const revenueMapping = {
  shopify: {
    source: 'shopify_orders',
    fields: {
      order_id: 'id',
      revenue: 'total_price',
      date: 'created_at',
      customer_id: 'customer.id',
      products: 'line_items'
    }
  },
  facebook: {
    source: 'facebook_ads',
    fields: {
      campaign_id: 'id',
      revenue: 'conversion_value',
      date: 'date_start',
      adset_id: 'adset.id',
      ad_id: 'ad.id'
    }
  },
  google: {
    source: 'google_ads',
    fields: {
      campaign_id: 'campaign.id',
      revenue: 'conversions_value',
      date: 'date',
      keyword_id: 'keyword.id',
      ad_group_id: 'ad_group.id'
    }
  }
};
```

### **Cost Mapping**
```javascript
const costMapping = {
  shopify: {
    source: 'shopify_orders',
    fields: {
      order_id: 'id',
      cogs: 'line_items[].price * 0.4', // 40% default COGS
      shipping: 'shipping_lines[].price',
      fees: 'total_tax + gateway_fees',
      date: 'created_at'
    }
  },
  facebook: {
    source: 'facebook_ads',
    fields: {
      campaign_id: 'id',
      ad_spend: 'spend',
      date: 'date_start',
      campaign_name: 'name'
    }
  },
  google: {
    source: 'google_ads',
    fields: {
      campaign_id: 'campaign.id',
      ad_spend: 'cost_micros / 1000000',
      date: 'date',
      campaign_name: 'campaign.name'
    }
  },
  klaviyo: {
    source: 'klaviyo_campaigns',
    fields: {
      campaign_id: 'id',
      send_cost: 'estimated_cost',
      date: 'created_at',
      campaign_name: 'name'
    }
  },
  postscript: {
    source: 'postscript_campaigns',
    fields: {
      campaign_id: 'id',
      send_cost: 'cost',
      date: 'created_at',
      campaign_name: 'name'
    }
  }
};
```

## **Profit Calculation Engine**

### **Order-Level Profit Calculation**
```javascript
function calculateOrderProfit(order) {
  const revenue = order.total_price;
  const cogs = order.line_items.reduce((sum, item) => {
    return sum + (item.price * item.quantity * 0.4); // 40% COGS
  }, 0);
  const shipping = order.shipping_lines.reduce((sum, line) => sum + line.price, 0);
  const fees = order.total_tax + order.gateway_fees;
  const marketingCosts = getMarketingCostsForOrder(order);
  
  return {
    order_id: order.id,
    revenue: revenue,
    costs: cogs + shipping + fees + marketingCosts,
    profit: revenue - (cogs + shipping + fees + marketingCosts),
    margin: ((revenue - (cogs + shipping + fees + marketingCosts)) / revenue) * 100
  };
}
```

### **Campaign-Level Profit Calculation**
```javascript
function calculateCampaignProfit(campaign) {
  const revenue = campaign.conversions_value;
  const adSpend = campaign.spend;
  const attributedOrders = getAttributedOrders(campaign);
  const orderCosts = attributedOrders.reduce((sum, order) => {
    return sum + calculateOrderCosts(order);
  }, 0);
  
  return {
    campaign_id: campaign.id,
    revenue: revenue,
    costs: adSpend + orderCosts,
    profit: revenue - (adSpend + orderCosts),
    roas: revenue / adSpend
  };
}
```

## **Data Synchronization**

### **Real-Time Sync**
- Webhook-based updates for immediate data changes
- API polling for regular data refresh
- Queue-based processing for high-volume updates

### **Batch Sync**
- Daily full data synchronization
- Historical data backfill
- Data validation and cleanup

## **Data Storage**

### **Database Schema**
```sql
-- Orders table
CREATE TABLE orders (
  id VARCHAR(255) PRIMARY KEY,
  platform VARCHAR(50),
  revenue DECIMAL(10,2),
  cogs DECIMAL(10,2),
  shipping DECIMAL(10,2),
  fees DECIMAL(10,2),
  marketing_costs DECIMAL(10,2),
  profit DECIMAL(10,2),
  margin DECIMAL(5,2),
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

-- Campaigns table
CREATE TABLE campaigns (
  id VARCHAR(255) PRIMARY KEY,
  platform VARCHAR(50),
  name VARCHAR(255),
  ad_spend DECIMAL(10,2),
  revenue DECIMAL(10,2),
  profit DECIMAL(10,2),
  roas DECIMAL(5,2),
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

-- Products table
CREATE TABLE products (
  id VARCHAR(255) PRIMARY KEY,
  platform VARCHAR(50),
  name VARCHAR(255),
  cogs_percentage DECIMAL(5,2),
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);
```

## **Implementation Plan**

### **Phase 1: Core Integrations**
1. Shopify API integration
2. Facebook Marketing API integration
3. Basic profit calculation engine
4. Order-level profit tracking

### **Phase 2: Extended Integrations**
1. Google Ads API integration
2. Klaviyo API integration
3. Postscript API integration
4. Campaign-level profit tracking

### **Phase 3: Advanced Features**
1. Real-time data synchronization
2. Advanced profit analytics
3. Predictive profit modeling
4. Automated cost optimization

## **Security & Compliance**

### **API Security**
- OAuth 2.0 authentication for all platforms
- Secure credential storage
- Rate limiting and error handling
- Data encryption in transit and at rest

### **Data Privacy**
- GDPR compliance
- Data retention policies
- User consent management
- Data anonymization options

## **Monitoring & Alerts**

### **Data Health Monitoring**
- API connection status
- Data sync failures
- Data quality issues
- Performance metrics

### **Business Alerts**
- Profit margin drops
- High-cost campaigns
- Data sync failures
- Unusual spending patterns

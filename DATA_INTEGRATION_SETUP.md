# 🔗 Data Integration Setup Guide

## **Overview**
This guide will help you set up real data integrations for ProfitPeek to connect with Shopify, Facebook, Google, Klaviyo, and Postscript.

## **Prerequisites**
- Active accounts on all platforms
- API access permissions
- Environment variables configured

## **1. Shopify Integration**

### **Setup Steps:**
1. **Create Shopify App** (if not already done):
   - Go to [Shopify Partners Dashboard](https://partners.shopify.com)
   - Create new app
   - Get API key and secret

2. **Configure OAuth Scopes:**
   ```
   read_orders
   read_products
   read_customers
   read_inventory
   read_analytics
   read_fulfillments
   read_shipping
   read_returns
   ```

3. **Environment Variables:**
   ```bash
   SHOPIFY_API_KEY=your_api_key
   SHOPIFY_API_SECRET=your_api_secret
   SHOPIFY_REDIRECT_URI=https://your-domain.com/auth/callback
   ```

### **API Endpoints:**
- `POST /api/integrations/shopify` - Add Shopify connection
- `GET /api/integrations/status` - Check connection status

## **2. Facebook Marketing Integration**

### **Setup Steps:**
1. **Create Facebook App**:
   - Go to [Facebook Developers](https://developers.facebook.com)
   - Create new app
   - Add Marketing API product

2. **Get Access Token**:
   - Generate long-lived access token
   - Get Ad Account ID

3. **Environment Variables:**
   ```bash
   FACEBOOK_ACCESS_TOKEN=your_access_token
   FACEBOOK_AD_ACCOUNT_ID=your_ad_account_id
   ```

### **API Endpoints:**
- `POST /api/integrations/facebook` - Add Facebook connection
- `GET /api/integrations/status` - Check connection status

## **3. Google Ads Integration**

### **Setup Steps:**
1. **Create Google Cloud Project**:
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Create new project
   - Enable Google Ads API

2. **Get Credentials**:
   - Create OAuth 2.0 credentials
   - Get Developer Token from Google Ads
   - Get Customer ID

3. **Environment Variables:**
   ```bash
   GOOGLE_ACCESS_TOKEN=your_access_token
   GOOGLE_CUSTOMER_ID=your_customer_id
   GOOGLE_DEVELOPER_TOKEN=your_developer_token
   ```

### **API Endpoints:**
- `POST /api/integrations/google` - Add Google Ads connection
- `GET /api/integrations/status` - Check connection status

## **4. Klaviyo Integration**

### **Setup Steps:**
1. **Get API Key**:
   - Go to [Klaviyo Account Settings](https://www.klaviyo.com/account#api-keys-tab)
   - Generate new API key

2. **Environment Variables:**
   ```bash
   KLAVIYO_API_KEY=your_api_key
   ```

### **API Endpoints:**
- `POST /api/integrations/klaviyo` - Add Klaviyo connection
- `GET /api/integrations/status` - Check connection status

## **5. Postscript Integration**

### **Setup Steps:**
1. **Get API Key**:
   - Go to [Postscript Settings](https://app.postscript.io/settings/api)
   - Generate new API key

2. **Environment Variables:**
   ```bash
   POSTSCRIPT_API_KEY=your_api_key
   ```

### **API Endpoints:**
- `POST /api/integrations/postscript` - Add Postscript connection
- `GET /api/integrations/status` - Check connection status

## **6. Data Synchronization**

### **Sync All Data:**
```bash
curl -X POST https://your-api-domain.com/api/sync \
  -H "Content-Type: application/json" \
  -d '{
    "start_date": "2024-01-01",
    "end_date": "2024-01-31"
  }'
```

### **Calculate Profits:**
```bash
curl -X POST https://your-api-domain.com/api/profits \
  -H "Content-Type: application/json" \
  -d '{
    "orders": [...],
    "campaigns": [...]
  }'
```

## **7. Frontend Integration**

### **Add Integration Settings Page:**
```typescript
// Integration settings component
const IntegrationSettings = () => {
  const [integrations, setIntegrations] = useState({});
  
  const addIntegration = async (platform, credentials) => {
    const response = await fetch(`/api/integrations/${platform}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(credentials)
    });
    
    if (response.ok) {
      // Refresh integration status
      await refreshIntegrations();
    }
  };
  
  return (
    <Page title="Data Integrations">
      <Layout>
        <Layout.Section>
          <Card>
            <BlockStack gap="400">
              <Text as="h2" variant="headingMd">Connected Platforms</Text>
              {Object.entries(integrations).map(([platform, status]) => (
                <InlineStack key={platform} align="space-between">
                  <Text as="p" variant="bodyMd">{platform}</Text>
                  <Badge tone={status ? 'success' : 'critical'}>
                    {status ? 'Connected' : 'Disconnected'}
                  </Badge>
                </InlineStack>
              ))}
            </BlockStack>
          </Card>
        </Layout.Section>
      </Layout>
    </Page>
  );
};
```

## **8. Testing Integrations**

### **Test Connection Status:**
```bash
curl https://your-api-domain.com/api/integrations/status
```

### **Expected Response:**
```json
{
  "status": {
    "shopify": true,
    "facebook": true,
    "google": false,
    "klaviyo": true,
    "postscript": false
  },
  "available_platforms": ["shopify", "facebook", "klaviyo"]
}
```

## **9. Data Flow**

### **Revenue Sources:**
1. **Shopify Orders** → Revenue calculation
2. **Facebook Conversions** → Attribution revenue
3. **Google Ads Conversions** → Attribution revenue

### **Cost Sources:**
1. **Shopify** → COGS, shipping, fees
2. **Facebook** → Ad spend
3. **Google Ads** → Ad spend
4. **Klaviyo** → Email costs
5. **Postscript** → SMS costs

### **Profit Calculation:**
```
Net Profit = Total Revenue - Total Costs
Total Revenue = Shopify Revenue + Attributed Revenue
Total Costs = COGS + Marketing Costs + Platform Fees
```

## **10. Monitoring & Alerts**

### **Data Health Monitoring:**
- API connection status
- Data sync failures
- Missing cost data
- Unusual spending patterns

### **Business Alerts:**
- Profit margin drops
- High-cost campaigns
- Data sync failures
- Missing integrations

## **11. Security Considerations**

### **API Security:**
- Store credentials securely
- Use environment variables
- Implement rate limiting
- Monitor API usage

### **Data Privacy:**
- GDPR compliance
- Data retention policies
- User consent management
- Data anonymization

## **12. Troubleshooting**

### **Common Issues:**
1. **Authentication Failures**:
   - Check API keys
   - Verify permissions
   - Test connections

2. **Data Sync Issues**:
   - Check API limits
   - Verify date ranges
   - Monitor error logs

3. **Profit Calculation Errors**:
   - Verify cost mappings
   - Check data quality
   - Validate calculations

### **Debug Commands:**
```bash
# Test Shopify connection
curl -H "X-Shopify-Access-Token: YOUR_TOKEN" \
  https://your-shop.myshopify.com/admin/api/2023-10/shop.json

# Test Facebook connection
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://graph.facebook.com/v18.0/me

# Test Google Ads connection
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://googleads.googleapis.com/v14/customers/YOUR_CUSTOMER_ID
```

## **13. Next Steps**

1. **Set up all integrations** following this guide
2. **Test data synchronization** with sample data
3. **Configure profit calculations** for your business model
4. **Set up monitoring** and alerts
5. **Train your team** on the new system
6. **Monitor performance** and optimize

## **14. Support**

For technical support:
- Check the API documentation
- Review error logs
- Test individual connections
- Contact platform support if needed

For business questions:
- Review profit calculations
- Check data mappings
- Verify business logic
- Consult with your team

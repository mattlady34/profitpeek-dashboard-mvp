# 🛍️ Shopify Integration Setup Guide

## **Step-by-Step Shopify Setup**

### **1. Create/Update Shopify App**

1. **Go to Shopify Partners Dashboard**:
   - Visit: https://partners.shopify.com
   - Sign in with your Shopify account

2. **Create New App** (if you don't have one):
   - Click "Create app"
   - Choose "Public app"
   - App name: "ProfitPeek"
   - App URL: `https://profitpeek-dashboard-mvp.netlify.app`

3. **Configure App Settings**:
   - **App URL**: `https://profitpeek-dashboard-mvp.netlify.app`
   - **Allowed redirection URL(s)**:
     - `https://profitpeek-dashboard-mvp.netlify.app/auth/callback`
     - `https://profitpeek-api.onrender.com/auth/callback`

### **2. Set Required Scopes**

In your Shopify app settings, add these scopes:

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

### **3. Get API Credentials**

From your Shopify app dashboard, copy:
- **API key** (Client ID)
- **API secret key** (Client Secret)

### **4. Update Environment Variables**

Add these to your Render backend environment variables:

```bash
SHOPIFY_API_KEY=your_actual_api_key_here
SHOPIFY_API_SECRET=your_actual_api_secret_here
SHOPIFY_REDIRECT_URI=https://profitpeek-api.onrender.com/auth/callback
SHOPIFY_APP_URL=https://profitpeek-dashboard-mvp.netlify.app
```

### **5. Test the Integration**

1. **Test OAuth Flow**:
   ```bash
   curl "https://profitpeek-api.onrender.com/auth/start?shop=your-store.myshopify.com"
   ```

2. **Test API Connection**:
   ```bash
   curl "https://profitpeek-api.onrender.com/api/integrations/status"
   ```

### **6. Connect Your Store**

1. **Visit the app**: https://profitpeek-dashboard-mvp.netlify.app
2. **Click "Connect Your Store"**
3. **Enter your store domain** (e.g., "your-store")
4. **Complete OAuth flow**
5. **Start seeing real data!**

## **Expected Data Flow**

### **Revenue Data**:
- Order total prices
- Customer information
- Product details
- Order dates and status

### **Cost Data**:
- Product COGS (estimated at 40% by default)
- Shipping costs
- Payment processing fees (2.9% + $0.30)
- Platform fees

### **Profit Calculation**:
```
Net Profit = Revenue - COGS - Shipping - Fees
Margin = (Net Profit / Revenue) × 100
```

## **Troubleshooting**

### **Common Issues**:

1. **"Invalid shop domain"**:
   - Make sure you enter just the store name (e.g., "your-store")
   - Don't include ".myshopify.com"

2. **"OAuth failed"**:
   - Check your API key and secret
   - Verify redirect URLs match exactly
   - Ensure scopes are correct

3. **"No data showing"**:
   - Check if your store has orders
   - Verify API permissions
   - Check backend logs

### **Debug Commands**:

```bash
# Test Shopify API directly
curl -H "X-Shopify-Access-Token: YOUR_TOKEN" \
  https://your-store.myshopify.com/admin/api/2023-10/shop.json

# Check integration status
curl https://profitpeek-api.onrender.com/api/integrations/status
```

## **Next Steps After Shopify**

Once Shopify is working:
1. **Meta Ads** - Facebook/Instagram advertising data
2. **Google Ads** - Search and display advertising data  
3. **Klaviyo** - Email marketing costs and performance
4. **Postscript** - SMS marketing costs and performance

## **Support**

If you run into issues:
1. Check the Shopify Partners dashboard for app status
2. Verify all URLs and credentials
3. Test the OAuth flow step by step
4. Check backend logs for errors

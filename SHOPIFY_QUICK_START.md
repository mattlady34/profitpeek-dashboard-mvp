# 🛍️ Shopify Quick Start Guide

## **Step 1: Get Your Shopify App Credentials**

1. **Go to Shopify Partners Dashboard**: https://partners.shopify.com
2. **Find your ProfitPeek app** (or create a new one)
3. **Copy these credentials**:
   - API Key (Client ID)
   - API Secret Key (Client Secret)

## **Step 2: Test Shopify Connection**

### **Option A: Test with Your Live App**
1. **Visit**: https://profitpeek-dashboard-mvp.netlify.app
2. **Click "Connect Your Store"**
3. **Enter your store domain** (e.g., "your-store")
4. **Complete OAuth flow**
5. **See real data!**

### **Option B: Test with Demo Mode**
1. **Visit**: https://profitpeek-dashboard-mvp.netlify.app/dashboard?demo=1
2. **See demo data immediately**

## **Step 3: Update Your Shopify App Settings**

In your Shopify Partners dashboard, update these URLs:

**App URL**: `https://profitpeek-dashboard-mvp.netlify.app`

**Allowed redirection URL(s)**:
- `https://profitpeek-dashboard-mvp.netlify.app/auth/callback`
- `https://profitpeek-api.onrender.com/auth/callback`

**Required Scopes**:
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

## **Step 4: Update Backend Environment Variables**

In your Render backend, add these environment variables:

```bash
SHOPIFY_API_KEY=your_actual_api_key_here
SHOPIFY_API_SECRET=your_actual_api_secret_here
SHOPIFY_REDIRECT_URI=https://profitpeek-api.onrender.com/auth/callback
SHOPIFY_APP_URL=https://profitpeek-dashboard-mvp.netlify.app
```

## **Step 5: Test the Integration**

### **Test OAuth Flow**:
```bash
curl "https://profitpeek-api.onrender.com/auth/start?shop=your-store.myshopify.com"
```

### **Test API Connection**:
```bash
curl "https://profitpeek-api.onrender.com/api/dashboard?demo=1"
```

## **Expected Results**

Once connected, you should see:
- **Real order data** from your Shopify store
- **Actual revenue** calculations
- **Real profit margins** (with estimated COGS)
- **Live customer data**

## **Next Steps After Shopify**

Once Shopify is working:
1. **Meta Ads** - Facebook/Instagram advertising data
2. **Google Ads** - Search and display advertising data  
3. **Klaviyo** - Email marketing costs and performance
4. **Postscript** - SMS marketing costs and performance

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

## **Ready to Test?**

1. **Get your Shopify app credentials**
2. **Update the URLs in Shopify Partners**
3. **Test the OAuth flow**
4. **See your real data!**

Let me know when you have your Shopify app credentials and I'll help you set up the integration!

# 📘 Meta Ads Integration Setup Guide

## **Step-by-Step Meta Ads Setup**

### **1. Create Facebook App**

1. **Go to Facebook Developers**: https://developers.facebook.com
2. **Create New App**:
   - Click "Create App"
   - Choose "Business" as app type
   - App name: "ProfitPeek"
   - App contact email: your email
   - Business account: Select your business account

### **2. Add Marketing API Product**

1. **In your app dashboard**:
   - Click "Add Product"
   - Find "Marketing API" and click "Set Up"
   - This will give you access to ad data

### **3. Get Required Credentials**

You'll need these from your Facebook app:

**App ID**: Found in App Settings > Basic
**App Secret**: Found in App Settings > Basic (click "Show")
**Access Token**: Generate in Marketing API > Tools > Access Token Tool
**Ad Account ID**: Found in Ads Manager > Account Settings

### **4. Set Up Permissions**

Your app needs these permissions:
```
ads_read
ads_management
business_management
read_insights
```

### **5. Test the Integration**

Once you have the credentials, we can test:

```bash
# Test Facebook API connection
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  https://graph.facebook.com/v18.0/me

# Test Ad Account access
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  https://graph.facebook.com/v18.0/YOUR_AD_ACCOUNT_ID
```

## **What Data We'll Get**

### **Campaign Data**:
- Campaign name and ID
- Ad spend
- Impressions
- Clicks
- Conversions
- ROAS (Return on Ad Spend)

### **Ad Set Data**:
- Ad set performance
- Targeting information
- Budget and bid strategy

### **Ad Data**:
- Ad creative performance
- Click-through rates
- Conversion rates

## **Profit Calculation**

For Meta Ads, we'll calculate:
```
Campaign Profit = Conversion Value - Ad Spend - Attributed COGS
ROAS = Conversion Value / Ad Spend
```

## **Next Steps**

1. **Create your Facebook app**
2. **Get the required credentials**
3. **Test the API connection**
4. **Connect to ProfitPeek**

Let me know when you have your Facebook app credentials and I'll help you set up the integration!

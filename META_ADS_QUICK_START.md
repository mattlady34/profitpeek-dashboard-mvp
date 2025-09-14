# 📘 Meta Ads Quick Start Guide

## **🚀 Get Meta Ads Working in 5 Minutes**

### **Step 1: Create Facebook App**

1. **Go to Facebook Developers**: https://developers.facebook.com
2. **Click "Create App"**
3. **Choose "Business" as app type**
4. **Fill in details**:
   - App name: "ProfitPeek"
   - App contact email: your email
   - Business account: Select your business account

### **Step 2: Add Marketing API**

1. **In your app dashboard**:
   - Click "Add Product"
   - Find "Marketing API" and click "Set Up"
   - This gives you access to ad data

### **Step 3: Get Your Credentials**

**App ID**: 
- Go to App Settings > Basic
- Copy the "App ID"

**App Secret**:
- Go to App Settings > Basic
- Click "Show" next to App Secret
- Copy the secret

**Access Token**:
- Go to Marketing API > Tools > Access Token Tool
- Select your ad account
- Generate token with these permissions:
  - `ads_read`
  - `ads_management` 
  - `business_management`
  - `read_insights`

**Ad Account ID**:
- Go to Ads Manager > Account Settings
- Copy the "Ad Account ID" (format: act_123456789)

### **Step 4: Test the Integration**

Run our test script:

```bash
cd /Users/mattlady/profitpeek-dashboard
python3 test_meta_ads.py
```

Enter your credentials when prompted, and you'll see:
- ✅ Connection test
- 📊 Campaign data from last 30 days
- 💰 Profit calculations for each campaign
- 📈 Overall ROAS and profit margins

### **Step 5: What You'll Get**

**Campaign Data**:
- Campaign name and performance
- Ad spend and revenue
- Impressions, clicks, conversions
- ROAS (Return on Ad Spend)

**Profit Calculations**:
```
Campaign Profit = Conversion Value - Ad Spend - Attributed COGS
ROAS = Conversion Value / Ad Spend
```

**Real-time Sync**:
- Last 30 days of campaign data
- Daily profit tracking
- Performance insights

## **🔧 Troubleshooting**

### **Common Issues**:

1. **"Invalid access token"**:
   - Make sure you generated a long-lived token
   - Check that permissions include `ads_read` and `read_insights`

2. **"Ad account not found"**:
   - Verify your Ad Account ID format (should start with `act_`)
   - Make sure the token has access to that account

3. **"No campaigns found"**:
   - Check if campaigns ran in the last 30 days
   - Verify the ad account has active campaigns

4. **"Insufficient permissions"**:
   - Regenerate token with all required permissions
   - Make sure your Facebook account has admin access to the ad account

### **Debug Commands**:

```bash
# Test basic API connection
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  https://graph.facebook.com/v18.0/me

# Test ad account access
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  https://graph.facebook.com/v18.0/YOUR_AD_ACCOUNT_ID
```

## **📊 Expected Results**

Once connected, you'll see:

**Campaign Performance**:
- Ad spend vs. revenue
- Profit margins per campaign
- ROAS tracking
- Conversion attribution

**Profit Insights**:
- Which campaigns are profitable
- Cost per acquisition
- Revenue attribution
- ROI optimization opportunities

## **🚀 Next Steps**

After Meta Ads is working:
1. **Google Ads** - Search and display advertising
2. **Klaviyo** - Email marketing costs
3. **Postscript** - SMS marketing costs

## **💡 Pro Tips**

1. **Use long-lived tokens** (60 days) for production
2. **Set up webhooks** for real-time updates
3. **Monitor API limits** (Facebook has rate limits)
4. **Test with small date ranges** first

**Ready to test?** Get your Facebook app credentials and run the test script! 🚀

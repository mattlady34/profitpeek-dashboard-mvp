# 🔍 Google Ads Quick Start Guide

## **🚀 Get Google Ads Working in 5 Minutes**

### **Step 1: Create Google Cloud Project**

1. **Go to Google Cloud Console**: https://console.cloud.google.com
2. **Create New Project**:
   - Click "New Project"
   - Project name: "ProfitPeek"
   - Click "Create"

### **Step 2: Enable Google Ads API**

1. **In your project**:
   - Go to "APIs & Services" > "Library"
   - Search for "Google Ads API"
   - Click on it and "Enable"

### **Step 3: Create OAuth 2.0 Credentials**

1. **Go to "APIs & Services" > "Credentials"**
2. **Click "Create Credentials" > "OAuth 2.0 Client ID"**
3. **Choose "Web application"**
4. **Add authorized redirect URIs**:
   - `http://localhost:8080` (for testing)
   - `https://your-domain.com/oauth/callback` (for production)
5. **Download the JSON file** (you'll need this)

### **Step 4: Get Google Ads Developer Token**

1. **Go to Google Ads**: https://ads.google.com
2. **Sign in with your Google Ads account**
3. **Go to Tools & Settings > API Center**
4. **Apply for a developer token** (this can take a few days)
5. **Once approved, copy your developer token**

### **Step 5: Get Customer ID**

1. **In Google Ads**:
   - Go to Tools & Settings > Account Settings
   - Copy your "Customer ID" (10-digit number)

### **Step 6: Generate Access Token**

You'll need to generate an access token using OAuth 2.0. Here's a simple way:

```python
# Install required packages
pip install google-auth google-auth-oauthlib google-auth-httplib2

# Run this script to get your access token
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json

# Your OAuth 2.0 credentials file
SCOPES = ['https://www.googleapis.com/auth/adwords']
CREDENTIALS_FILE = 'path/to/your/credentials.json'

flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
creds = flow.run_local_server(port=0)

print(f"Access Token: {creds.token}")
print(f"Refresh Token: {creds.refresh_token}")
```

### **Step 7: Test the Integration**

Run our test script:

```bash
cd /Users/mattlady/profitpeek-dashboard
python3 test_google_ads.py
```

Enter your credentials when prompted, and you'll see:
- ✅ Connection test
- 📊 Campaign data from last 30 days
- 💰 Profit calculations for each campaign
- 🔍 Keyword performance data

## **What Data We'll Get**

### **Campaign Data**:
- Campaign name and performance
- Cost and conversion values
- Impressions, clicks, conversions
- ROAS (Return on Ad Spend)

### **Keyword Data**:
- Search terms performance
- Cost per keyword
- Conversion rates
- Search volume insights

### **Ad Group Data**:
- Ad group performance
- Budget allocation
- Targeting effectiveness

## **Profit Calculation**

For Google Ads, we'll calculate:
```
Campaign Profit = Conversion Value - Cost - Attributed COGS
ROAS = Conversion Value / Cost
```

## **Troubleshooting**

### **Common Issues**:

1. **"Invalid access token"**:
   - Make sure you generated a fresh token
   - Check that the token has the correct scopes

2. **"Customer not found"**:
   - Verify your Customer ID format (10 digits)
   - Make sure the token has access to that account

3. **"Developer token not approved"**:
   - Wait for Google to approve your developer token
   - Use test mode until approved

4. **"Insufficient permissions"**:
   - Make sure your Google account has admin access to the Google Ads account
   - Check that the OAuth scopes include adwords access

### **Debug Commands**:

```bash
# Test basic API connection
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "developer-token: YOUR_DEVELOPER_TOKEN" \
  https://googleads.googleapis.com/v14/customers/YOUR_CUSTOMER_ID
```

## **Expected Results**

Once connected, you'll see:

**Campaign Performance**:
- Cost vs. revenue
- Profit margins per campaign
- ROAS tracking
- Conversion attribution

**Keyword Insights**:
- Which keywords are profitable
- Cost per acquisition
- Search term performance
- ROI optimization opportunities

## **Next Steps**

After Google Ads is working:
1. **Klaviyo** - Email marketing costs
2. **Postscript** - SMS marketing costs
3. **Integration** - Connect all platforms

## **💡 Pro Tips**

1. **Use refresh tokens** for long-term access
2. **Monitor API quotas** (Google has daily limits)
3. **Test with small date ranges** first
4. **Use test accounts** during development

**Ready to test?** Get your Google Ads credentials and run the test script! 🚀

# 🔑 Complete API Credentials Guide

## **🚀 Get All Your API Keys in 30 Minutes**

This guide will walk you through getting API credentials for all platforms step-by-step.

---

## **1. 🛍️ Shopify API Credentials**

### **Step 1: Create Shopify App**
1. **Go to**: https://partners.shopify.com
2. **Sign in** with your Shopify account
3. **Click "Create app"**
4. **Choose "Public app"**
5. **App name**: "ProfitPeek"
6. **App URL**: `https://profitpeek-dashboard-mvp.netlify.app`
7. **Allowed redirection URL**: `https://profitpeek-dashboard-mvp.netlify.app/auth/callback`

### **Step 2: Get Credentials**
1. **In your app settings**:
   - **Client ID** = Your API Key
   - **Client Secret** = Your API Secret
2. **Copy both values** - you'll need them!

### **Step 3: Test**
```bash
python3 test_shopify.py
# Enter your Client ID and Client Secret when prompted
```

---

## **2. 📘 Meta Ads (Facebook) API Credentials**

### **Step 1: Create Facebook App**
1. **Go to**: https://developers.facebook.com
2. **Click "Create App"**
3. **Choose "Business"**
4. **App name**: "ProfitPeek"
5. **App contact email**: Your email

### **Step 2: Add Marketing API**
1. **In your app dashboard**:
   - Click "Add Product"
   - Find "Marketing API"
   - Click "Set Up"

### **Step 3: Get Access Token**
1. **Go to Tools & Settings > Access Tokens**
2. **Click "Generate Token"**
3. **Select your ad account**
4. **Copy the access token**

### **Step 4: Get Ad Account ID**
1. **Go to**: https://adsmanager.facebook.com
2. **Look at the URL**: `https://adsmanager.facebook.com/adsmanager/manage/campaigns/act=123456789`
3. **The number after `act=` is your Ad Account ID**

### **Step 5: Test**
```bash
python3 test_meta_ads.py
# Enter your Access Token and Ad Account ID when prompted
```

---

## **3. 🔍 Google Ads API Credentials**

### **Step 1: Create Google Cloud Project**
1. **Go to**: https://console.cloud.google.com
2. **Click "New Project"**
3. **Project name**: "ProfitPeek"
4. **Click "Create"**

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
   - `http://localhost:8080`
   - `https://profitpeek-dashboard-mvp.netlify.app/oauth/callback`
5. **Download the JSON file**

### **Step 4: Get Developer Token**
1. **Go to Google Ads**: https://ads.google.com
2. **Sign in with your Google Ads account**
3. **Go to Tools & Settings > API Center**
4. **Apply for a developer token** (can take a few days)
5. **Once approved, copy your developer token**

### **Step 5: Get Customer ID**
1. **In Google Ads**:
   - Go to Tools & Settings > Account Settings
   - Copy your "Customer ID" (10-digit number)

### **Step 6: Generate Access Token**
```python
# Install required packages
pip install google-auth google-auth-oauthlib google-auth-httplib2

# Run this script to get your access token
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json

SCOPES = ['https://www.googleapis.com/auth/adwords']
CREDENTIALS_FILE = 'path/to/your/credentials.json'

flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
creds = flow.run_local_server(port=0)

print(f"Access Token: {creds.token}")
print(f"Refresh Token: {creds.refresh_token}")
```

### **Step 7: Test**
```bash
python3 test_google_ads.py
# Enter your Access Token, Customer ID, and Developer Token when prompted
```

---

## **4. 📧 Klaviyo API Credentials**

### **Step 1: Get API Key**
1. **Go to Klaviyo**: https://www.klaviyo.com
2. **Sign in to your account**
3. **Go to Account > Settings > API Keys**
4. **Click "Create API Key"**
5. **Name**: "ProfitPeek"
6. **Copy the API key**

### **Step 2: Test**
```bash
python3 test_klaviyo.py
# Enter your API Key when prompted
```

---

## **5. 📱 Postscript API Credentials**

### **Step 1: Get API Key**
1. **Go to Postscript**: https://postscript.io
2. **Sign in to your account**
3. **Go to Settings > API**
4. **Click "Generate API Key"**
5. **Name**: "ProfitPeek"
6. **Copy the API key**

### **Step 2: Test**
```bash
python3 test_postscript.py
# Enter your API Key when prompted
```

---

## **📋 Quick Checklist**

### **Shopify** ✅
- [ ] Client ID (API Key)
- [ ] Client Secret
- [ ] App URL configured

### **Meta Ads** ✅
- [ ] Access Token
- [ ] Ad Account ID
- [ ] Marketing API enabled

### **Google Ads** ✅
- [ ] Access Token
- [ ] Customer ID
- [ ] Developer Token
- [ ] OAuth credentials file

### **Klaviyo** ✅
- [ ] API Key
- [ ] Account access

### **Postscript** ✅
- [ ] API Key
- [ ] Account access

---

## **🧪 Test All Integrations**

Once you have all credentials, test each one:

```bash
# Test each platform
python3 test_shopify.py
python3 test_meta_ads.py
python3 test_google_ads.py
python3 test_klaviyo.py
python3 test_postscript.py
```

## **💡 Pro Tips**

1. **Start with Shopify** - easiest to set up
2. **Test one platform at a time**
3. **Keep credentials secure** - don't commit them to git
4. **Use environment variables** for production
5. **Some platforms need approval** (Google Ads developer token)

## **🔧 Troubleshooting**

### **Common Issues**:
- **"Invalid credentials"** - Double-check your API keys
- **"Access denied"** - Make sure you have the right permissions
- **"Rate limited"** - Wait a few minutes and try again
- **"Token expired"** - Generate a new access token

### **Need Help?**
- Check the individual setup guides for each platform
- Look at the test script outputs for specific error messages
- Make sure your accounts have the right permissions

## **🚀 Ready to Go!**

Once you have all credentials, you'll be able to:
- ✅ Connect all platforms to ProfitPeek
- ✅ See real profit data across all channels
- ✅ Track ROAS and performance metrics
- ✅ Optimize your marketing spend

**Get your credentials and start testing!** 🎯

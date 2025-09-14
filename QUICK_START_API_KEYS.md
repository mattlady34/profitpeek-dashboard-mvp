# 🚀 Quick Start: Get Your API Keys

## **⏱️ 30 Minutes to Get All API Keys**

Follow this step-by-step guide to get all your API credentials quickly.

---

## **🎯 Start Here: Shopify (Easiest)**

### **1. Go to Shopify Partners**
- **URL**: https://partners.shopify.com
- **Sign in** with your Shopify account

### **2. Create App**
- Click **"Create app"**
- Choose **"Public app"**
- **App name**: "ProfitPeek"
- **App URL**: `https://profitpeek-dashboard-mvp.netlify.app`
- **Redirect URL**: `https://profitpeek-dashboard-mvp.netlify.app/auth/callback`

### **3. Get Your Keys**
- **Client ID** = Your API Key
- **Client Secret** = Your API Secret
- **Copy both!**

### **4. Test It**
```bash
python3 test_shopify.py
```

---

## **📘 Meta Ads (Facebook)**

### **1. Create Facebook App**
- **URL**: https://developers.facebook.com
- Click **"Create App"**
- Choose **"Business"**
- **App name**: "ProfitPeek"

### **2. Add Marketing API**
- In your app dashboard
- Click **"Add Product"**
- Find **"Marketing API"**
- Click **"Set Up"**

### **3. Get Access Token**
- Go to **Tools & Settings > Access Tokens**
- Click **"Generate Token"**
- Select your ad account
- **Copy the token**

### **4. Get Ad Account ID**
- Go to https://adsmanager.facebook.com
- Look at the URL: `act=123456789`
- **The number is your Ad Account ID**

### **5. Test It**
```bash
python3 test_meta_ads.py
```

---

## **🔍 Google Ads**

### **1. Create Google Cloud Project**
- **URL**: https://console.cloud.google.com
- Click **"New Project"**
- **Project name**: "ProfitPeek"

### **2. Enable Google Ads API**
- Go to **APIs & Services > Library**
- Search **"Google Ads API"**
- Click **"Enable"**

### **3. Create OAuth Credentials**
- Go to **APIs & Services > Credentials**
- Click **"Create Credentials > OAuth 2.0 Client ID"**
- Choose **"Web application"**
- Add redirect URI: `http://localhost:8080`
- **Download the JSON file**

### **4. Get Developer Token**
- Go to https://ads.google.com
- Go to **Tools & Settings > API Center**
- **Apply for developer token** (takes a few days)
- **Copy when approved**

### **5. Get Customer ID**
- In Google Ads
- Go to **Tools & Settings > Account Settings**
- **Copy your Customer ID** (10 digits)

### **6. Generate Access Token**
```python
pip install google-auth google-auth-oauthlib google-auth-httplib2

# Run this to get your access token
from google_auth_oauthlib.flow import InstalledAppFlow
SCOPES = ['https://www.googleapis.com/auth/adwords']
CREDENTIALS_FILE = 'path/to/your/credentials.json'

flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
creds = flow.run_local_server(port=0)
print(f"Access Token: {creds.token}")
```

### **7. Test It**
```bash
python3 test_google_ads.py
```

---

## **📧 Klaviyo**

### **1. Get API Key**
- **URL**: https://www.klaviyo.com
- Sign in to your account
- Go to **Account > Settings > API Keys**
- Click **"Create API Key"**
- **Name**: "ProfitPeek"
- **Copy the key**

### **2. Test It**
```bash
python3 test_klaviyo.py
```

---

## **📱 Postscript**

### **1. Get API Key**
- **URL**: https://postscript.io
- Sign in to your account
- Go to **Settings > API**
- Click **"Generate API Key"**
- **Name**: "ProfitPeek"
- **Copy the key**

### **2. Test It**
```bash
python3 test_postscript.py
```

---

## **✅ Test All Platforms**

Once you have all keys, test them:

```bash
# Test each platform
python3 test_shopify.py
python3 test_meta_ads.py
python3 test_google_ads.py
python3 test_klaviyo.py
python3 test_postscript.py
```

---

## **📋 Your API Keys Checklist**

- [ ] **Shopify**: Client ID + Client Secret
- [ ] **Meta Ads**: Access Token + Ad Account ID
- [ ] **Google Ads**: Access Token + Customer ID + Developer Token
- [ ] **Klaviyo**: API Key
- [ ] **Postscript**: API Key

---

## **💡 Pro Tips**

1. **Start with Shopify** - it's the easiest
2. **Test one platform at a time**
3. **Keep your keys secure** - don't share them
4. **Google Ads takes a few days** for developer token approval
5. **If you get stuck**, check the detailed guides

---

## **🚀 You're Done!**

Once you have all API keys and they're tested, you'll have:
- ✅ Real profit data from all platforms
- ✅ Unified dashboard showing all marketing spend
- ✅ ROAS tracking across all channels
- ✅ Complete profit optimization insights

**Ready to get your API keys?** Start with Shopify! 🎯

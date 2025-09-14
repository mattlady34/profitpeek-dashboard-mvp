# 🔑 API Keys Cheat Sheet

## **⚡ Super Quick Reference**

### **🛍️ Shopify (5 minutes)**
1. Go to https://partners.shopify.com
2. Create app → Public app
3. Copy **Client ID** and **Client Secret**
4. Test: `python3 test_shopify.py`

### **📘 Meta Ads (10 minutes)**
1. Go to https://developers.facebook.com
2. Create app → Business
3. Add Marketing API
4. Get **Access Token** from Tools & Settings
5. Get **Ad Account ID** from adsmanager.facebook.com URL
6. Test: `python3 test_meta_ads.py`

### **🔍 Google Ads (15 minutes)**
1. Go to https://console.cloud.google.com
2. Create project → Enable Google Ads API
3. Create OAuth credentials → Download JSON
4. Get **Developer Token** from ads.google.com (takes a few days)
5. Get **Customer ID** from account settings
6. Generate **Access Token** using OAuth flow
7. Test: `python3 test_google_ads.py`

### **📧 Klaviyo (2 minutes)**
1. Go to https://www.klaviyo.com
2. Account → Settings → API Keys
3. Create API key → Copy **API Key**
4. Test: `python3 test_klaviyo.py`

### **📱 Postscript (2 minutes)**
1. Go to https://postscript.io
2. Settings → API
3. Generate API key → Copy **API Key**
4. Test: `python3 test_postscript.py`

---

## **🧪 Test All Platforms**
```bash
python3 test_shopify.py
python3 test_meta_ads.py
python3 test_google_ads.py
python3 test_klaviyo.py
python3 test_postscript.py
```

---

## **📋 What You Need**
- **Shopify**: Client ID + Client Secret
- **Meta Ads**: Access Token + Ad Account ID
- **Google Ads**: Access Token + Customer ID + Developer Token
- **Klaviyo**: API Key
- **Postscript**: API Key

---

## **💡 Start Here**
1. **Shopify** (easiest)
2. **Klaviyo** (quick)
3. **Postscript** (quick)
4. **Meta Ads** (medium)
5. **Google Ads** (takes time for approval)

**Ready to go!** 🚀

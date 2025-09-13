# 🚀 Production URLs for ProfitPeek

## **Frontend (Netlify)**
- **Main App**: https://profitpeek-dashboard-mvp.netlify.app
- **Demo Mode**: https://profitpeek-dashboard-mvp.netlify.app/dashboard?demo=1

## **Backend (Render)**
- **API Base**: https://profitpeek-dashboard-mvp.onrender.com
- **Health Check**: https://profitpeek-dashboard-mvp.onrender.com/health

## **Shopify App Settings**
Update these in your Shopify Partners dashboard:

### **App URLs**
- **App URL**: `https://profitpeek-dashboard-mvp.netlify.app`
- **Redirect URL**: `https://profitpeek-dashboard-mvp.netlify.app/auth/callback`

### **Compliance Webhooks**
- **Customer data request**: `https://profitpeek-dashboard-mvp.onrender.com/webhooks/customers/data_request`
- **Customer data erasure**: `https://profitpeek-dashboard-mvp.onrender.com/webhooks/customers/redact`
- **Shop data erasure**: `https://profitpeek-dashboard-mvp.onrender.com/webhooks/shop/redact`

## **Render Environment Variables**
Update these in your Render dashboard:

```
SHOPIFY_APP_URL=https://profitpeek-dashboard-mvp.netlify.app
SHOPIFY_REDIRECT_URI=https://profitpeek-dashboard-mvp.netlify.app/auth/callback
NEXT_PUBLIC_API_URL=https://profitpeek-dashboard-mvp.onrender.com
```

## **Marketing URLs**
- **Landing Page**: https://profitpeek-dashboard-mvp.netlify.app
- **Beta Testing**: https://profitpeek-dashboard-mvp.netlify.app/dashboard?demo=1

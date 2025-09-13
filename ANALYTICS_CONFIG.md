# 📊 Analytics Configuration

## **Environment Variables to Set**

Add these to your Netlify environment variables:

### **Google Analytics 4**
```
NEXT_PUBLIC_GA_ID=G-XXXXXXXXXX
```

### **Mixpanel**
```
NEXT_PUBLIC_MIXPANEL_TOKEN=your_mixpanel_token_here
```

### **API Configuration**
```
NEXT_PUBLIC_API_URL=https://profitpeek-dashboard-mvp.onrender.com
```

## **Setup Instructions**

### **1. Google Analytics 4**
1. Go to [Google Analytics](https://analytics.google.com)
2. Create new property: "ProfitPeek Dashboard"
3. Get Measurement ID (G-XXXXXXXXXX)
4. Add to Netlify environment variables

### **2. Mixpanel**
1. Go to [Mixpanel](https://mixpanel.com)
2. Create project: "ProfitPeek"
3. Get Project Token
4. Add to Netlify environment variables

### **3. Netlify Environment Variables**
1. Go to your Netlify dashboard
2. Click "Site settings"
3. Click "Environment variables"
4. Add the variables above
5. Redeploy your site

## **Events Being Tracked**

### **User Events:**
- `app_loaded` - App initialization
- `demo_mode_started` - User clicked demo mode
- `store_connected` - OAuth completed
- `dashboard_viewed` - Dashboard page viewed
- `orders_viewed` - Orders page viewed
- `settings_updated` - Settings saved
- `page_viewed` - Any page view
- `error_occurred` - Any error

### **User Properties:**
- `shop` - Store domain
- `authenticated_at` - When user authenticated
- `demo_mode` - Whether in demo mode

## **Testing Analytics**

### **Local Testing:**
1. Set environment variables in `.env.local`
2. Run `npm run dev`
3. Check browser console for analytics calls
4. Verify events in Google Analytics/Mixpanel

### **Production Testing:**
1. Deploy with environment variables
2. Visit your app
3. Check analytics dashboards
4. Verify events are being tracked

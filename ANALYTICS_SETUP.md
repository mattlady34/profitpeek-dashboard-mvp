# 📊 Analytics Setup for ProfitPeek

## **1. Google Analytics 4**

### **Setup Steps:**
1. **Go to [Google Analytics](https://analytics.google.com)**
2. **Create new property**: "ProfitPeek Dashboard"
3. **Get Measurement ID**: `G-XXXXXXXXXX`
4. **Add to frontend**: Update `apps/web/src/app/layout.tsx`

### **Code to Add:**
```tsx
// Add to layout.tsx head section
<Script
  src={`https://www.googletagmanager.com/gtag/js?id=${process.env.NEXT_PUBLIC_GA_ID}`}
  strategy="afterInteractive"
/>
<Script id="google-analytics" strategy="afterInteractive">
  {`
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', '${process.env.NEXT_PUBLIC_GA_ID}');
  `}
</Script>
```

## **2. Mixpanel (User Analytics)**

### **Setup Steps:**
1. **Go to [Mixpanel](https://mixpanel.com)**
2. **Create project**: "ProfitPeek"
3. **Get Project Token**
4. **Track key events**: Login, Dashboard View, Order View, etc.

### **Key Events to Track:**
- `app_loaded` - App initialization
- `demo_mode_started` - User clicked demo mode
- `store_connected` - OAuth completed
- `dashboard_viewed` - Dashboard page viewed
- `orders_viewed` - Orders page viewed
- `settings_updated` - Settings saved

## **3. Error Tracking (Sentry)**

### **Setup Steps:**
1. **Go to [Sentry](https://sentry.io)**
2. **Create project**: "ProfitPeek Frontend"
3. **Get DSN**
4. **Add to frontend**: Error boundary and monitoring

## **4. Performance Monitoring**

### **Vercel Analytics (if using Vercel)**
- Automatic performance tracking
- Core Web Vitals monitoring
- Real User Monitoring (RUM)

### **Netlify Analytics**
- Built-in analytics for Netlify deployments
- Page views, unique visitors, top pages

## **5. Backend Monitoring**

### **Render Metrics**
- CPU usage
- Memory usage
- Response times
- Error rates

### **Custom Logging**
- API request/response logging
- Error logging
- Performance metrics

## **6. Business Metrics to Track**

### **User Engagement:**
- Daily/Monthly Active Users
- Session duration
- Page views per session
- Feature usage

### **Conversion Metrics:**
- Demo to signup conversion
- Trial to paid conversion
- User retention rates

### **Technical Metrics:**
- API response times
- Error rates
- Uptime percentage
- Load times

## **7. Dashboard Setup**

Create a simple analytics dashboard showing:
- User signups
- Demo mode usage
- API usage
- Error rates
- Performance metrics

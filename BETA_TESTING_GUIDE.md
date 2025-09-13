# 🚀 ProfitPeek Beta Testing Guide

## **What is ProfitPeek?**
ProfitPeek is a real-time profit tracking app for Shopify stores that helps you understand your true margins by tracking COGS, processing fees, shipping costs, and more.

## **🔗 Beta Testing Links**

### **Live App:**
- **Main App**: https://68c5da6bee13a200084d4ce0--profitpeek-dashboard-mvp.netlify.app
- **Demo Mode**: https://68c5da6bee13a200084d4ce0--profitpeek-dashboard-mvp.netlify.app/dashboard?demo=1

### **For Shopify Partners:**
- **App Store Listing**: [Coming Soon]
- **Install in Test Store**: [Coming Soon]

## **🧪 How to Test**

### **Option 1: Demo Mode (No Setup Required)**
1. Visit: https://68c5da6bee13a200084d4ce0--profitpeek-dashboard-mvp.netlify.app/dashboard?demo=1
2. See the app with realistic demo data
3. Test all features without connecting a real store

### **Option 2: Real Store Testing**
1. Visit: https://68c5da6bee13a200084d4ce0--profitpeek-dashboard-mvp.netlify.app
2. Enter your test store domain (e.g., "your-test-store")
3. Complete OAuth flow
4. See your real store data

## **📊 Features to Test**

### **Dashboard**
- [ ] Profit metrics display correctly
- [ ] Charts render properly
- [ ] "What Moved Today" section works
- [ ] Data health indicators show
- [ ] Period selector works (7d, 30d, 90d)

### **Orders Page**
- [ ] Order table loads
- [ ] Click "View Details" opens order sheet
- [ ] Order details show correctly
- [ ] Profit calculations are accurate

### **Settings Page**
- [ ] Form inputs work
- [ ] COGS percentage can be changed
- [ ] Processing fee settings work
- [ ] Save button functions

### **Other Pages**
- [ ] Profit Analysis page loads
- [ ] Daily Digest page works
- [ ] Backfill page functions
- [ ] Health page shows status

## **🐛 What to Report**

### **Critical Issues:**
- App won't load
- OAuth flow fails
- Data doesn't display
- Calculations are wrong

### **UI/UX Issues:**
- Buttons don't work
- Navigation is broken
- Mobile responsiveness issues
- Accessibility problems

### **Performance Issues:**
- Slow loading
- Charts don't render
- API timeouts

## **📝 Feedback Form**

Please report issues with:
1. **Store Name**: Your test store name
2. **Issue Type**: Bug/Feature Request/UI Issue
3. **Steps to Reproduce**: What you did
4. **Expected Result**: What should happen
5. **Actual Result**: What actually happened
6. **Screenshots**: If applicable

## **🔧 Technical Details**

- **Frontend**: Next.js + Shopify Polaris
- **Backend**: Flask + Python
- **Hosting**: Netlify (Frontend) + Render (Backend)
- **APIs**: Shopify Admin API v2023-10

## **📞 Support**

- **Email**: [Your support email]
- **GitHub Issues**: [Your GitHub repo]
- **Discord**: [Your Discord server]

---

**Thank you for testing ProfitPeek! Your feedback helps us build the best profit tracking tool for Shopify merchants.** 🎉

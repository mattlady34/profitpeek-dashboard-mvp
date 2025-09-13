# 🧪 Beta Testing Guide

## For Beta Testers

### How to Test ProfitPeek

1. **Visit the App**: Go to your deployed Vercel URL
2. **Try Demo Mode**: Click "Try Demo Mode" to see sample data
3. **Connect Real Store**: Enter your store domain (e.g., "mystore.myshopify.com")
4. **Authorize Access**: Grant permissions in Shopify
5. **Explore Dashboard**: Check all features and pages

### What to Test

#### ✅ Core Features
- [ ] Store connection and OAuth flow
- [ ] Dashboard loads with real data
- [ ] All navigation pages work
- [ ] Charts and metrics display correctly
- [ ] Mobile responsiveness
- [ ] Error handling

#### ✅ Data Accuracy
- [ ] Profit calculations are correct
- [ ] Order data matches Shopify admin
- [ ] Revenue numbers are accurate
- [ ] Margin calculations make sense

#### ✅ User Experience
- [ ] Loading states work properly
- [ ] Error messages are helpful
- [ ] Navigation is intuitive
- [ ] Design looks professional

### Reporting Issues

When you find issues, please report:
1. **What you were doing** when the issue occurred
2. **What you expected** to happen
3. **What actually happened** instead
4. **Screenshots** if helpful
5. **Browser and device** you're using

## For Developers

### Monitoring

1. **Render Dashboard**: Monitor backend performance and logs
2. **Vercel Dashboard**: Monitor frontend performance and builds
3. **Shopify Partners**: Monitor API usage and app performance

### Common Issues

#### Backend Issues
- **CORS errors**: Check Flask-CORS configuration
- **OAuth failures**: Verify redirect URLs match exactly
- **API timeouts**: Check Shopify API rate limits

#### Frontend Issues
- **Build failures**: Check for TypeScript errors
- **Environment variables**: Verify NEXT_PUBLIC_API_URL is set
- **Polaris components**: Check for missing imports

### Performance Optimization

1. **API Caching**: Implement Redis for frequently accessed data
2. **Image Optimization**: Use Next.js Image component
3. **Code Splitting**: Lazy load non-critical components
4. **CDN**: Use Vercel's global CDN

### Security Checklist

- [ ] Environment variables are secure
- [ ] OAuth state parameter is validated
- [ ] CORS is properly configured
- [ ] API endpoints are protected
- [ ] User sessions are secure

## 🎯 Success Metrics

### Technical Metrics
- **Uptime**: >99% availability
- **Load Time**: <3 seconds initial load
- **API Response**: <1 second for data requests
- **Error Rate**: <1% of requests

### User Metrics
- **Store Connections**: Number of stores connected
- **Session Duration**: How long users stay
- **Feature Usage**: Which features are most used
- **User Feedback**: Qualitative feedback scores

## 📞 Support

For technical support:
- **Email**: support@profitpeek.com
- **GitHub Issues**: Create issues in the repository
- **Documentation**: Check README.md and DEPLOYMENT.md

## 🚀 Next Steps After Beta

1. **Collect Feedback**: Survey beta users
2. **Fix Issues**: Address reported problems
3. **Add Features**: Implement requested improvements
4. **Scale Infrastructure**: Prepare for more users
5. **Launch Publicly**: Open to all Shopify stores

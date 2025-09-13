# ✅ Deployment Checklist

## Phase 1: GitHub Setup
- [ ] Create GitHub repository: `profitpeek-dashboard`
- [ ] Push code to GitHub
- [ ] Verify all files are uploaded

## Phase 2: Backend Deployment (Render)
- [ ] Create Render account
- [ ] Deploy backend service
- [ ] Set environment variables (with placeholder values)
- [ ] Test backend health endpoint
- [ ] Copy backend URL

## Phase 3: Frontend Deployment (Vercel)
- [ ] Create Vercel account
- [ ] Deploy frontend service
- [ ] Set environment variable: `NEXT_PUBLIC_API_URL`
- [ ] Test frontend loads
- [ ] Copy frontend URL

## Phase 4: Shopify App Creation
- [ ] Create Shopify Partners account
- [ ] Create new app: `ProfitPeek`
- [ ] Configure app URLs
- [ ] Set API scopes
- [ ] Copy API credentials

## Phase 5: Connect Everything
- [ ] Update Render with real Shopify API keys
- [ ] Update Vercel with correct backend URL
- [ ] Test OAuth flow with demo store
- [ ] Verify all features work

## Phase 6: Beta Testing
- [ ] Test with your development store
- [ ] Invite 5-10 beta testers
- [ ] Monitor performance and errors
- [ ] Collect feedback

## Phase 7: Production Launch
- [ ] Fix any critical issues
- [ ] Optimize performance
- [ ] Submit to Shopify App Store (optional)
- [ ] Launch publicly

## Quick Commands

### Push to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/profitpeek-dashboard.git
git push -u origin main
```

### Test Backend
```bash
curl https://your-render-app.onrender.com/health
```

### Test Frontend
Visit: `https://your-vercel-app.vercel.app`

## Support Files
- `RENDER_DEPLOYMENT.md` - Backend deployment guide
- `VERCEL_DEPLOYMENT.md` - Frontend deployment guide
- `SHOPIFY_APP_SETUP.md` - Shopify app setup guide
- `BETA_TESTING.md` - Beta testing instructions

## Emergency Contacts
- **Render Support**: support@render.com
- **Vercel Support**: help@vercel.com
- **Shopify Partners**: partners@shopify.com

# 🚀 Vercel Deployment Guide

## Step 1: Create Vercel Account
1. Go to [vercel.com](https://vercel.com)
2. Sign up with GitHub (recommended)
3. Connect your GitHub account

## Step 2: Deploy Frontend
1. Click "New Project"
2. Import your GitHub repository: `profitpeek-dashboard`
3. Configure the project:

### Project Settings
- **Framework Preset**: `Next.js`
- **Root Directory**: `apps/web`
- **Build Command**: `npm run build` (auto-detected)
- **Output Directory**: `.next` (auto-detected)
- **Install Command**: `npm install` (auto-detected)

## Step 3: Environment Variables
Add this environment variable in Vercel dashboard:

```
NEXT_PUBLIC_API_URL=https://your-render-app.onrender.com
```

**Note**: Replace with your actual Render backend URL.

## Step 4: Deploy
1. Click "Deploy"
2. Wait for deployment (2-3 minutes)
3. Copy your app URL (e.g., `https://profitpeek-dashboard.vercel.app`)

## Step 5: Test Frontend
1. Visit your Vercel URL
2. Try demo mode first
3. Test the OAuth flow (will fail until Shopify app is created)

## Troubleshooting
- **Build fails**: Check for TypeScript errors
- **Environment variables**: Make sure NEXT_PUBLIC_API_URL is set
- **API calls fail**: Verify backend URL is correct
- **Polaris errors**: Check for missing imports

## Next Steps
1. Create Shopify app
2. Update backend environment variables
3. Test complete OAuth flow
4. Deploy to production

## Custom Domain (Optional)
1. Go to Project Settings → Domains
2. Add your custom domain
3. Update DNS records as instructed
4. Update Shopify app URLs

# 🚀 Production Deployment Guide

## Step 1: Create GitHub Repository

1. Go to [GitHub](https://github.com) and create a new repository
2. Name it `profitpeek-dashboard`
3. Make it public or private (your choice)
4. Don't initialize with README (we already have one)

## Step 2: Push to GitHub

```bash
# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/profitpeek-dashboard.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 3: Deploy Backend to Render

1. Go to [Render](https://render.com) and sign up/login
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `profitpeek-api`
   - **Root Directory**: `apps/api`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Python Version**: `3.9`

5. Add Environment Variables:
   ```
   SHOPIFY_API_KEY=your_shopify_api_key
   SHOPIFY_API_SECRET=your_shopify_api_secret
   SHOPIFY_REDIRECT_URI=https://your-frontend-url.vercel.app/auth/callback
   SHOPIFY_APP_URL=https://your-frontend-url.vercel.app
   JWT_SECRET=your_jwt_secret_here
   ```

6. Click "Create Web Service"
7. Wait for deployment (5-10 minutes)
8. Copy your app URL (e.g., `https://profitpeek-api.onrender.com`)

## Step 4: Deploy Frontend to Vercel

1. Go to [Vercel](https://vercel.com) and sign up/login
2. Click "New Project"
3. Import your GitHub repository
4. Configure:
   - **Framework Preset**: Next.js
   - **Root Directory**: `apps/web`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`

5. Add Environment Variable:
   ```
   NEXT_PUBLIC_API_URL=https://your-render-app.onrender.com
   ```

6. Click "Deploy"
7. Wait for deployment (2-3 minutes)
8. Copy your app URL (e.g., `https://profitpeek-dashboard.vercel.app`)

## Step 5: Create Shopify App

1. Go to [Shopify Partners](https://partners.shopify.com)
2. Sign up/login and create a new app
3. Configure:
   - **App Name**: ProfitPeek
   - **App URL**: `https://your-frontend-url.vercel.app`
   - **Allowed redirection URL(s)**: `https://your-frontend-url.vercel.app/auth/callback`

4. Get your API credentials:
   - **API Key**: Copy from Partners dashboard
   - **API Secret Key**: Copy from Partners dashboard

5. Update your Render environment variables with real credentials

## Step 6: Test Production

1. Visit your Vercel URL
2. Try demo mode first
3. Test with a real store (use your dev store)
4. Verify all features work

## 🎉 You're Live!

Your ProfitPeek app is now deployed and ready for beta testing!

### Next Steps:
- Share with beta users
- Monitor performance
- Collect feedback
- Iterate and improve

### Support:
- Check Render logs for backend issues
- Check Vercel logs for frontend issues
- Monitor Shopify API usage

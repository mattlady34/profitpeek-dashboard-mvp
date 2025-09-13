# 🚀 Render Deployment Guide

## Step 1: Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up with GitHub (recommended)
3. Connect your GitHub account

## Step 2: Deploy Backend
1. Click "New +" → "Web Service"
2. Connect your GitHub repository: `profitpeek-dashboard`
3. Configure the service:

### Basic Settings
- **Name**: `profitpeek-api`
- **Root Directory**: `apps/api`
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`

### Advanced Settings
- **Python Version**: `3.9.18`
- **Instance Type**: `Starter` (free tier)
- **Auto-Deploy**: `Yes` (deploys on every push)

## Step 3: Environment Variables
Add these environment variables in Render dashboard:

```
SHOPIFY_API_KEY=your_shopify_api_key_here
SHOPIFY_API_SECRET=your_shopify_api_secret_here
SHOPIFY_REDIRECT_URI=https://your-frontend-url.vercel.app/auth/callback
SHOPIFY_APP_URL=https://your-frontend-url.vercel.app
JWT_SECRET=your_jwt_secret_here_make_it_long_and_random
```

**Note**: You'll get the real Shopify API keys in the next step.

## Step 4: Deploy
1. Click "Create Web Service"
2. Wait for deployment (5-10 minutes)
3. Copy your app URL (e.g., `https://profitpeek-api.onrender.com`)

## Step 5: Test Backend
Test your deployed backend:
```bash
curl https://your-render-app.onrender.com/health
```

Should return: `{"status": "healthy"}`

## Troubleshooting
- **Build fails**: Check Python version and dependencies
- **CORS errors**: Verify Flask-CORS is installed
- **Environment variables**: Make sure all are set correctly
- **Logs**: Check Render logs for detailed error messages

## Next Steps
1. Deploy frontend to Vercel
2. Create Shopify app
3. Update environment variables with real API keys
4. Test complete flow

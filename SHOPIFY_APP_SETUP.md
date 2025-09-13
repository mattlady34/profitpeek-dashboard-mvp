# 🚀 Shopify App Setup Guide

## Step 1: Create Shopify Partners Account
1. Go to [partners.shopify.com](https://partners.shopify.com)
2. Sign up for a free account
3. Verify your email address

## Step 2: Create New App
1. Click "Apps" → "Create app"
2. Choose "Create app manually"
3. Fill in app details:

### App Information
- **App name**: `ProfitPeek`
- **App URL**: `https://your-frontend-url.vercel.app`
- **Allowed redirection URL(s)**: 
  - `https://your-frontend-url.vercel.app/auth/callback`
  - `https://your-backend-url.onrender.com/auth/callback`

## Step 3: Configure App Settings
1. Go to "App setup" tab
2. Configure:

### App URLs
- **App URL**: `https://your-frontend-url.vercel.app`
- **Allowed redirection URLs**: 
  - `https://your-frontend-url.vercel.app/auth/callback`
  - `https://your-backend-url.onrender.com/auth/callback`

### App Access
- **Admin API access scopes**:
  - `read_products`
  - `read_orders`
  - `read_customers`
  - `read_inventory`
  - `read_analytics`

## Step 4: Get API Credentials
1. Go to "API credentials" tab
2. Copy your credentials:
   - **API key**: `shpat_...`
   - **API secret key**: `...`

## Step 5: Update Environment Variables
Update your Render backend with real credentials:

```
SHOPIFY_API_KEY=shpat_your_real_api_key
SHOPIFY_API_SECRET=your_real_api_secret
SHOPIFY_REDIRECT_URI=https://your-frontend-url.vercel.app/auth/callback
SHOPIFY_APP_URL=https://your-frontend-url.vercel.app
JWT_SECRET=your_jwt_secret_here
```

## Step 6: Test App Installation
1. Go to "Test your app" tab
2. Click "Select store" → Choose your development store
3. Install the app
4. Test the OAuth flow

## Step 7: Submit for Review (Optional)
1. Go to "Distribution" tab
2. Click "Create app listing"
3. Fill in app store listing details
4. Submit for review

## Troubleshooting
- **OAuth fails**: Check redirect URLs match exactly
- **API errors**: Verify scopes are correct
- **Installation fails**: Check app URL is accessible
- **CORS errors**: Verify backend CORS configuration

## Next Steps
1. Test with your development store
2. Invite beta testers
3. Monitor app performance
4. Collect user feedback

# ProfitPeek Dashboard

A real-time profit tracking dashboard for Shopify stores built with Next.js, Polaris, and Flask.

## 🚀 Features

- **Real-time Profit Tracking**: Monitor your store's true profitability
- **Shopify Integration**: Seamless OAuth and data sync
- **Polaris Design System**: Native Shopify admin experience
- **Demo Mode**: Test without connecting real stores
- **Responsive Design**: Works on all devices

## 🛠 Tech Stack

- **Frontend**: Next.js 14, React, TypeScript, Shopify Polaris
- **Backend**: Flask, Python, Shopify API
- **Deployment**: Vercel (Frontend), Render (Backend)

## 🚀 Quick Start

### Local Development

1. **Clone and install dependencies**:
   ```bash
   git clone <your-repo-url>
   cd profitpeek-dashboard
   ```

2. **Start the backend**:
   ```bash
   cd apps/api
   pip install -r requirements.txt
   python3 app.py
   ```

3. **Start the frontend**:
   ```bash
   cd apps/web
   npm install
   npm run dev
   ```

4. **Visit**: http://localhost:3000

### Production Deployment

1. **Deploy Backend to Render**:
   - Connect your GitHub repo
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `gunicorn app:app`
   - Add environment variables from `env.production`

2. **Deploy Frontend to Vercel**:
   - Connect your GitHub repo
   - Set root directory: `apps/web`
   - Add environment variable: `NEXT_PUBLIC_API_URL=https://your-render-app.onrender.com`

3. **Create Shopify App**:
   - Go to [Shopify Partners](https://partners.shopify.com)
   - Create new app
   - Update `shopify.app.toml` with your app details
   - Update environment variables with real API keys

## 🔧 Environment Variables

### Backend (Render)
```
SHOPIFY_API_KEY=your_shopify_api_key
SHOPIFY_API_SECRET=your_shopify_api_secret
SHOPIFY_REDIRECT_URI=https://your-frontend-url.vercel.app/auth/callback
SHOPIFY_APP_URL=https://your-frontend-url.vercel.app
JWT_SECRET=your_jwt_secret
```

### Frontend (Vercel)
```
NEXT_PUBLIC_API_URL=https://your-backend-url.onrender.com
```

## 📱 Usage

1. **Demo Mode**: Visit the app and click "Try Demo Mode" to see sample data
2. **Real Store**: Enter your store domain (e.g., "mystore.myshopify.com") to connect
3. **Dashboard**: View real-time profit metrics, trends, and insights

## 🎯 Beta Testing

Ready for beta testing with real Shopify stores! The app includes:
- Secure OAuth flow
- Real-time data sync
- Error handling and fallbacks
- Mobile-responsive design

## 📄 License

MIT License - see LICENSE file for details
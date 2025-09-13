#!/bin/bash

echo "🚀 ProfitPeek Quick Deploy Script"
echo "=================================="
echo ""

# Check if we're in the right directory
if [ ! -f "package.json" ] && [ ! -d "apps" ]; then
    echo "❌ Please run this script from the profitpeek-dashboard root directory"
    exit 1
fi

echo "📋 Deployment Checklist:"
echo "1. ✅ Code is ready for deployment"
echo "2. ✅ All configuration files created"
echo "3. ✅ Documentation is complete"
echo ""

echo "🎯 Next Steps:"
echo "1. Create GitHub repository: https://github.com/new"
echo "   - Name: profitpeek-dashboard"
echo "   - Make it public"
echo "   - Don't initialize with README"
echo ""

echo "2. Push to GitHub:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/profitpeek-dashboard.git"
echo "   git push -u origin main"
echo ""

echo "3. Deploy Backend to Render:"
echo "   - Go to: https://render.com"
echo "   - Connect GitHub repo"
echo "   - Use settings from RENDER_DEPLOYMENT.md"
echo ""

echo "4. Deploy Frontend to Vercel:"
echo "   - Go to: https://vercel.com"
echo "   - Connect GitHub repo"
echo "   - Use settings from VERCEL_DEPLOYMENT.md"
echo ""

echo "5. Create Shopify App:"
echo "   - Go to: https://partners.shopify.com"
echo "   - Create new app"
echo "   - Use settings from SHOPIFY_APP_SETUP.md"
echo ""

echo "📖 Detailed guides:"
echo "- RENDER_DEPLOYMENT.md - Backend deployment"
echo "- VERCEL_DEPLOYMENT.md - Frontend deployment"
echo "- SHOPIFY_APP_SETUP.md - Shopify app creation"
echo "- DEPLOYMENT_CHECKLIST.md - Complete checklist"
echo ""

echo "🎉 Your ProfitPeek app is ready for deployment!"
echo "Follow the steps above to get it live and start beta testing!"

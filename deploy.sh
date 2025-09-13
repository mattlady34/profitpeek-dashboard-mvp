#!/bin/bash

echo "🚀 Deploying ProfitPeek to Production..."

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit for ProfitPeek deployment"
fi

# Add remote repositories (you'll need to create these)
echo "📝 Next steps:"
echo "1. Create a GitHub repository for this project"
echo "2. Add the remote: git remote add origin https://github.com/yourusername/profitpeek-dashboard.git"
echo "3. Push to GitHub: git push -u origin main"
echo "4. Deploy backend to Render: https://render.com"
echo "5. Deploy frontend to Vercel: https://vercel.com"
echo ""
echo "🔧 Backend deployment steps:"
echo "- Connect GitHub repo to Render"
echo "- Set build command: pip install -r requirements.txt"
echo "- Set start command: gunicorn app:app"
echo "- Add environment variables from env.production"
echo ""
echo "🔧 Frontend deployment steps:"
echo "- Connect GitHub repo to Vercel"
echo "- Set root directory: apps/web"
echo "- Add environment variable: NEXT_PUBLIC_API_URL=https://your-render-app.onrender.com"
echo ""
echo "✅ Ready for deployment!"

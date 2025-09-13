#!/bin/bash

echo "🚀 Pushing ProfitPeek to GitHub..."

# Check if remote exists
if git remote get-url origin >/dev/null 2>&1; then
    echo "✅ Remote origin already exists"
else
    echo "❌ No remote origin found. Please create GitHub repository first:"
    echo "1. Go to https://github.com"
    echo "2. Create new repository: profitpeek-dashboard"
    echo "3. Copy the repository URL"
    echo "4. Run: git remote add origin <YOUR_REPO_URL>"
    echo "5. Then run this script again"
    exit 1
fi

# Push to GitHub
echo "📤 Pushing to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo "✅ Successfully pushed to GitHub!"
    echo ""
    echo "🎯 Next steps:"
    echo "1. Deploy backend to Render: https://render.com"
    echo "2. Deploy frontend to Vercel: https://vercel.com"
    echo "3. Create Shopify app: https://partners.shopify.com"
    echo ""
    echo "📖 See DEPLOYMENT.md for detailed instructions"
else
    echo "❌ Failed to push to GitHub. Please check your repository URL and try again."
fi

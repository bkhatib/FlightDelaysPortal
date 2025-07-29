#!/bin/bash

echo "🚀 Flight Delays Portal - Deployment Script"
echo "=========================================="

# Check if git is clean
if [ -n "$(git status --porcelain)" ]; then
    echo "❌ Please commit all changes before deploying"
    exit 1
fi

echo "✅ Git repository is clean"

# Push to GitHub
echo "📤 Pushing to GitHub..."
git push origin main

if [ $? -eq 0 ]; then
    echo "✅ Successfully pushed to GitHub"
    echo ""
    echo "🌐 Next Steps:"
    echo "1. Go to https://share.streamlit.io/"
    echo "2. Sign in with GitHub"
    echo "3. Click 'New app'"
    echo "4. Select repository: bkhatib/FlightDelaysPortal"
    echo "5. Set main file path: app.py"
    echo "6. Add your AWS credentials in the secrets section"
    echo "7. Click 'Deploy'"
    echo ""
    echo "🎉 Your app will be live at: https://your-app-name.streamlit.app"
else
    echo "❌ Failed to push to GitHub"
    exit 1
fi 
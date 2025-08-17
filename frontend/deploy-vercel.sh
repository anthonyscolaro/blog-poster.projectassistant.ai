#!/bin/bash

# Vercel Deployment Script for Blog Poster Frontend
# Project ID: prj_TX3JDSh6JPCDokdTlIucIVCcpFXJ

set -e

echo "🚀 Starting Vercel deployment for Blog Poster frontend..."
echo "Project ID: prj_TX3JDSh6JPCDokdTlIucIVCcpFXJ"
echo ""

# Check if we're in the frontend directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: Not in frontend directory. Please run this script from the frontend folder."
    exit 1
fi

# Check if node_modules exists, if not install dependencies
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Build the project locally first to catch any errors
echo "🔨 Building project locally..."
npm run build

if [ $? -eq 0 ]; then
    echo "✅ Local build successful!"
else
    echo "❌ Local build failed. Please fix errors before deploying."
    exit 1
fi

# Deploy to Vercel
echo ""
echo "🚢 Deploying to Vercel..."
echo "This will deploy to production environment"
echo ""

# Use the project ID directly if already linked
if [ -f ".vercel/project.json" ]; then
    echo "📎 Project already linked to Vercel"
    vercel --prod
else
    echo "🔗 Linking to Vercel project..."
    vercel link --project=blog-poster
    vercel --prod
fi

echo ""
echo "✨ Deployment complete!"
echo ""
echo "📝 Post-deployment checklist:"
echo "  [ ] Check deployment at: https://blog-poster.vercel.app"
echo "  [ ] Verify environment variables are set in Vercel dashboard"
echo "  [ ] Test authentication flow"
echo "  [ ] Check API connections"
echo "  [ ] Monitor error logs in Vercel dashboard"
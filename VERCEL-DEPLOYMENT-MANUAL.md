# Manual Vercel Deployment Guide

## Project Information
- **Project ID**: `prj_TX3JDSh6JPCDokdTlIucIVCcpFXJ`
- **Frontend Path**: `/frontend`
- **Framework**: Vite + React 19

## Step 1: Authenticate with Vercel

```bash
vercel login
```

Choose your preferred authentication method (GitHub recommended).

## Step 2: Link the Project

Navigate to the frontend directory and link to your existing project:

```bash
cd frontend
vercel link --project-id=prj_TX3JDSh6JPCDokdTlIucIVCcpFXJ
```

## Step 3: Pull Environment Variables (if they exist)

```bash
vercel env pull .env.local
```

## Step 4: Deploy to Production

```bash
vercel --prod
```

Or deploy to preview first:

```bash
vercel
```

## Alternative: Deploy via GitHub Integration

If you've connected your GitHub repository to Vercel:

1. The deployment should trigger automatically when you push to `main`
2. Check deployment status at: https://vercel.com/dashboard

## Environment Variables Required

Make sure these are set in your Vercel dashboard (Settings → Environment Variables):

```env
# Core Configuration (REQUIRED)
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key
VITE_API_URL=https://your-api.com

# App Configuration
VITE_APP_NAME=Blog Poster
VITE_APP_VERSION=1.0.0

# Optional Services
VITE_STRIPE_PUBLISHABLE_KEY=pk_live_...
VITE_SENTRY_DSN=https://...@sentry.io/...
VITE_GA_TRACKING_ID=G-XXXXXXXXXX
```

## Build Settings in Vercel Dashboard

If configuring through the dashboard, use these settings:

- **Framework Preset**: Vite
- **Root Directory**: `frontend`
- **Build Command**: `npm run build`
- **Output Directory**: `dist`
- **Install Command**: `npm install`

## Troubleshooting

### Build Fails
1. Check Node version (should be 18.x or higher)
2. Verify all environment variables are set
3. Check build logs in Vercel dashboard

### 404 Errors on Routes
The `vercel.json` file should handle SPA routing. If issues persist:
1. Verify `vercel.json` is in the `frontend` directory
2. Check that rewrites are configured correctly

### API Connection Issues
1. Verify `VITE_API_URL` is set correctly
2. Check CORS settings on your API
3. Ensure API is accessible from Vercel's servers

## Quick Deploy Script

Use the provided script for automated deployment:

```bash
cd frontend
./deploy-vercel.sh
```

## Monitoring

After deployment:
1. Visit: https://vercel.com/dashboard/project/prj_TX3JDSh6JPCDokdTlIucIVCcpFXJ
2. Check Functions tab for any serverless functions
3. Monitor Analytics for performance metrics
4. Review Logs for any errors
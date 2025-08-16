# 🚀 Vercel Deployment Guide for Blog-Poster Frontend

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub Repository**: Your code should be pushed to GitHub
3. **Supabase Project**: Set up at [supabase.com](https://supabase.com)
4. **FastAPI Backend**: Should be deployed separately (Digital Ocean, Railway, etc.)

## 📋 Step-by-Step Deployment

### Step 1: Import Project to Vercel

1. Go to [vercel.com/new](https://vercel.com/new)
2. Click "Import Git Repository"
3. Select your `blog-poster` repository
4. **IMPORTANT**: Set the Root Directory to `frontend`

### Step 2: Configure Build Settings

Vercel should auto-detect Vite, but verify these settings:

- **Framework Preset**: Vite
- **Root Directory**: `frontend`
- **Build Command**: `npm run build`
- **Output Directory**: `dist`
- **Install Command**: `npm install`

### Step 3: Set Environment Variables

In Vercel's Environment Variables section, add:

#### Required Variables:
```bash
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
VITE_API_URL=https://your-api.digitaloceanspaces.com
VITE_WS_URL=wss://your-api.digitaloceanspaces.com
VITE_STRIPE_PUBLISHABLE_KEY=pk_live_51H...
VITE_APP_NAME=Blog-Poster
VITE_APP_URL=https://your-app.vercel.app
```

#### Optional Variables:
```bash
VITE_GA_TRACKING_ID=G-XXXXXXXXXX
```

### Step 4: Deploy

1. Click "Deploy"
2. Wait for the build to complete (usually 2-3 minutes)
3. Your app will be live at `https://your-project.vercel.app`

## 🔧 Post-Deployment Configuration

### 1. Configure Supabase

Add your Vercel domain to Supabase:
1. Go to Supabase Dashboard → Authentication → URL Configuration
2. Add your Vercel URLs to:
   - Site URL: `https://your-app.vercel.app`
   - Redirect URLs: `https://your-app.vercel.app/*`

### 2. Update CORS on Backend

Add your Vercel domain to allowed origins in your FastAPI backend:

```python
# app.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-app.vercel.app",
        "https://your-custom-domain.com"  # If using custom domain
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 3. Configure Custom Domain (Optional)

1. Go to Vercel Dashboard → Settings → Domains
2. Add your custom domain
3. Follow DNS configuration instructions
4. Update environment variables:
   - `VITE_APP_URL=https://your-custom-domain.com`

## 🔍 Troubleshooting

### Common Issues:

#### 1. Build Fails
```bash
# Check Node version compatibility
node --version  # Should be 18.x or higher

# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
npm run build
```

#### 2. Supabase Connection Issues
- Verify `VITE_SUPABASE_URL` doesn't have trailing slash
- Ensure `VITE_SUPABASE_ANON_KEY` is the correct public anon key
- Check Supabase RLS policies are configured

#### 3. API Connection Issues
- Ensure backend is running and accessible
- Verify CORS is configured correctly
- Check API URL doesn't have trailing slash
- For WebSocket, ensure protocol matches (wss:// for https://)

#### 4. Environment Variables Not Working
- Restart development server after changing .env
- In Vercel, redeploy after changing environment variables
- All client-side env vars must start with `VITE_`

## 📝 Vercel Configuration File

The `vercel.json` file in the frontend directory handles:
- SPA routing (redirects all routes to index.html)
- Security headers
- Cache configuration

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "vite",
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

## 🚨 Production Checklist

Before going live:

- [ ] Set up production Supabase instance
- [ ] Configure Stripe production keys
- [ ] Deploy FastAPI backend to production
- [ ] Update all environment variables to production values
- [ ] Configure custom domain
- [ ] Set up monitoring (Vercel Analytics)
- [ ] Test all critical user flows
- [ ] Configure rate limiting on backend
- [ ] Set up error tracking (Sentry)
- [ ] Enable Vercel Web Analytics

## 📊 Monitoring

### Vercel Analytics
1. Go to Vercel Dashboard → Analytics
2. Enable Web Analytics (free tier available)
3. Monitor:
   - Page views
   - Performance metrics
   - Error rates

### Logs
- View real-time logs: Vercel Dashboard → Functions → Logs
- Check build logs for deployment issues

## 🔄 Updates and Redeployment

### Automatic Deployments
- Push to main branch triggers automatic deployment
- Preview deployments for pull requests

### Manual Redeployment
1. Go to Vercel Dashboard
2. Click "Redeploy"
3. Choose deployment to redeploy

### Rollback
1. Go to Deployments tab
2. Find previous working deployment
3. Click "..." → "Promote to Production"

## 💰 Costs

Vercel Hobby Plan (Free):
- 100GB bandwidth/month
- Unlimited deployments
- SSL included
- Good for development and small projects

Vercel Pro ($20/month):
- 1TB bandwidth/month
- Team collaboration
- Advanced analytics
- Priority support

## 🔗 Useful Links

- [Vercel Documentation](https://vercel.com/docs)
- [Vite on Vercel](https://vercel.com/guides/deploying-vite)
- [Environment Variables](https://vercel.com/docs/environment-variables)
- [Custom Domains](https://vercel.com/docs/custom-domains)

## Support

If you encounter issues:
1. Check Vercel Status: [status.vercel.com](https://status.vercel.com)
2. Review build logs in Vercel Dashboard
3. Check browser console for runtime errors
4. Verify all environment variables are set correctly
# 🚀 Blog-Poster Deployment Guide

## Architecture Overview

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Vercel        │────▶│  Digital Ocean   │────▶│   Supabase      │
│   (React 19)    │     │  (FastAPI)       │     │   (Database)    │
└─────────────────┘     └──────────────────┘     └─────────────────┘
     Frontend              Backend API            Auth + Storage
```

## Deployment Platforms

| Component | Platform | URL | Cost |
|-----------|----------|-----|------|
| Frontend | Vercel | blog-poster.vercel.app | Free |
| Backend API | Digital Ocean App Platform | api.blog-poster.app | $25/mo |
| Database | Supabase | your-project.supabase.co | Free tier |
| Redis Cache | Redis Cloud (optional) | - | Free tier |

## Quick Deploy

### 1. Deploy to Staging
```bash
./deploy.sh staging
```

### 2. Deploy to Production
```bash
./deploy.sh production
```

## Manual Deployment Steps

### Step 1: Set Up Digital Ocean

1. **Install doctl CLI**:
```bash
brew install doctl
doctl auth init
```

2. **Create the app** (first time only):
```bash
doctl apps create --spec app.yaml
```

3. **Update existing app**:
```bash
# Get app ID
APP_ID=$(doctl apps list --format ID,Name --no-header | grep "blog-poster" | awk '{print $1}')

# Update spec
doctl apps spec update $APP_ID --spec app.yaml

# Deploy
doctl apps create-deployment $APP_ID --wait
```

### Step 2: Configure Environment Variables

1. **Copy the example file**:
```bash
cp .env.production.example .env.production
```

2. **Set secrets in Digital Ocean**:
```bash
# Set each secret individually
doctl apps config set $APP_ID \
  --key SUPABASE_URL --value "https://xxx.supabase.co" \
  --type SECRET --scope RUN_TIME

doctl apps config set $APP_ID \
  --key ANTHROPIC_API_KEY --value "sk-ant-xxx" \
  --type SECRET --scope RUN_TIME

# ... repeat for all secrets
```

Or use the Digital Ocean dashboard:
1. Go to Apps → blog-poster-api → Settings
2. Click on "App-Level Environment Variables"
3. Add each secret variable

### Step 3: Connect GitHub for Auto-Deploy

1. In Digital Ocean dashboard:
   - Apps → blog-poster-api → Settings → GitHub
   - Connect repository: `anthonyscolaro/blog-poster`
   - Set branch: `main` for production, `staging` for staging
   - Enable "Autodeploy on push"

2. Add GitHub secret for CI/CD:
   - Go to GitHub repo → Settings → Secrets
   - Add `DIGITALOCEAN_ACCESS_TOKEN`
   - Get token from: https://cloud.digitalocean.com/account/api/tokens

### Step 4: Verify Deployment

```bash
# Get app URL
APP_URL=$(doctl apps get $APP_ID --format DefaultIngress --no-header)

# Test health endpoint
curl $APP_URL/health

# View API docs
open $APP_URL/api/docs

# Check logs
doctl apps logs $APP_ID --follow
```

## Environment-Specific Configuration

### Staging Environment
- **App Name**: blog-poster-staging
- **Branch**: staging
- **Instance**: basic-xxs ($5/month)
- **Workers**: 1
- **URL**: blog-poster-staging-xxxxx.ondigitalocean.app

### Production Environment
- **App Name**: blog-poster-api
- **Branch**: main
- **Instance**: professional-xs ($25/month)
- **Workers**: 2
- **Custom Domain**: api.blog-poster.app

## Monitoring & Debugging

### View Logs
```bash
# Live logs
doctl apps logs $APP_ID --follow

# Last 100 lines
doctl apps logs $APP_ID --tail 100

# Specific component
doctl apps logs $APP_ID --type run
```

### Check Deployment Status
```bash
# List all deployments
doctl apps list-deployments $APP_ID

# Get specific deployment
doctl apps get-deployment $APP_ID $DEPLOYMENT_ID
```

### Health Checks
The app includes automatic health checks at `/health` endpoint.
- Initial delay: 60 seconds
- Check interval: 30 seconds
- Timeout: 10 seconds
- Failure threshold: 3

### Rollback
```bash
# List deployments
doctl apps list-deployments $APP_ID

# Rollback to previous
doctl apps create-deployment $APP_ID \
  --deployment-id <PREVIOUS_DEPLOYMENT_ID>
```

## Cost Optimization

### Digital Ocean Pricing
- **Staging**: basic-xxs = $5/month (512MB RAM, 1 vCPU)
- **Production**: professional-xs = $25/month (2GB RAM, 1 vCPU)

### Tips to Reduce Costs
1. Use staging environment for testing
2. Scale down during low traffic periods
3. Enable autoscaling only for production
4. Use Supabase free tier for database
5. Cache aggressively with Redis

## Security Checklist

- [ ] All secrets stored as environment variables
- [ ] CORS configured for specific origins only
- [ ] SSL/TLS enabled (automatic on Digital Ocean)
- [ ] Non-root user in Docker container
- [ ] Health check endpoint doesn't expose sensitive data
- [ ] API keys rotated regularly
- [ ] Database connection uses SSL

## Troubleshooting

### App Won't Start
```bash
# Check build logs
doctl apps logs $APP_ID --type build

# Verify environment variables
doctl apps config get $APP_ID
```

### Database Connection Issues
- Verify DATABASE_URL format
- Check Supabase connection pooler settings
- Ensure IP allowlist includes Digital Ocean

### High Memory Usage
- Reduce worker count
- Implement connection pooling
- Add memory limits in Dockerfile

### Slow Response Times
- Enable caching with Redis
- Optimize database queries
- Use CDN for static assets
- Scale up instance size

## Support

- **Digital Ocean Support**: https://www.digitalocean.com/support/
- **Status Page**: https://status.digitalocean.com/
- **Community**: https://www.digitalocean.com/community/

## Next Steps

1. Set up custom domain
2. Configure monitoring (Sentry, DataDog)
3. Implement auto-scaling rules
4. Set up backup strategy
5. Create staging → production promotion workflow
name: "Simple Digital Ocean Deployment"
description: |

## Purpose
Deploy blog-poster to Digital Ocean App Platform with minimal complexity and maximum reliability.

## Goal
Get the app running in production with PostgreSQL, user auth, and basic monitoring.

## Deployment Strategy

### Phase 1: Basic Deployment (Day 1)
```yaml
Digital Ocean Setup:
  - Create DO account and project
  - Deploy Managed PostgreSQL ($15/mo)
  - Create App Platform app ($12/mo)
  - Connect GitHub repo
  - Set environment variables
  
First Deploy:
  - Push to main branch
  - Auto-deploy triggers
  - Run database migrations
  - Verify health endpoint
```

### Phase 2: Add Essentials (Day 2-3)
```yaml
User Management:
  - JWT authentication
  - Registration/login endpoints
  - User dashboard
  
Monitoring:
  - Sentry integration (free tier)
  - UptimeRobot (free tier)
  - Basic health checks
  
Backups:
  - DO automatic daily backups
  - Test restore procedure
```

### Phase 3: Production Ready (Day 4-5)
```yaml
Final Steps:
  - DNS setup via Cloudflare API
  - Custom domain: blogpost.projectassistant.ai
  - SSL certificate (automatic via DO)
  - Rate limiting configured
  - Cost tracking enabled
  - Documentation updated
```

## DNS Configuration

### Cloudflare Setup
```yaml
Domain: projectassistant.ai
Subdomains:
  - blogpost.projectassistant.ai → Digital Ocean App Platform
  - api.blogpost.projectassistant.ai → API endpoint (optional)
  
Cloudflare Credentials (in .env.local):
  CLOUDFLARE_API_TOKEN: "fXs1g6GiML2PwSARgU6YHKtTlN41ELhhuIlDboab"
  CLOUDFLARE_ZONE_ID: "2f922ade64e8b27117734e8ec0d112b6"
```

## Configuration

### App Spec (`.do/app.yaml`)
```yaml
name: blog-poster
region: nyc
domains:
  - domain: blogpost.projectassistant.ai
    type: PRIMARY
    zone: projectassistant.ai
services:
  - name: api
    github:
      repo: yourusername/blog-poster
      branch: main
      deploy_on_push: true
    dockerfile_path: Dockerfile
    instance_size: basic-xs
    instance_count: 1
    http_port: 8088
    health_check:
      http_path: /health
      initial_delay_seconds: 10
      period_seconds: 30
    routes:
      - path: /
    envs:
      - key: DATABASE_URL
        scope: RUN_TIME
        value: ${db.DATABASE_URL}
      - key: REDIS_URL
        scope: RUN_TIME
        value: ${redis.REDIS_URL}
      - key: SECRET_KEY
        scope: RUN_TIME
        type: SECRET
      - key: ANTHROPIC_API_KEY
        scope: RUN_TIME
        type: SECRET

databases:
  - name: db
    engine: PG
    version: "15"
    size: db-s-dev-database
    num_nodes: 1
```

### Environment Variables
```bash
# Production .env
DATABASE_URL=${db.DATABASE_URL}
REDIS_URL=redis://localhost:6379
SECRET_KEY=generate-a-secure-key
APP_ENV=production

# API Keys (stored as DO secrets)
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
JINA_API_KEY=jina_...

# Limits
MAX_MONTHLY_COST_PER_USER=50.00
MAX_ARTICLES_PER_USER=100

# Features
ENABLE_USER_REGISTRATION=true
ENABLE_RATE_LIMITING=true
```

## DNS Setup Commands

```bash
# Initial DNS setup (creates placeholder CNAME records)
python scripts/setup_cloudflare_dns.py

# After deploying to Digital Ocean, get your app URL:
doctl apps get $APP_ID --format "DefaultIngress"

# Update DNS to point to your DO app (example):
python scripts/setup_cloudflare_dns.py --ip your-app.ondigitalocean.app

# Or manually update in Cloudflare dashboard:
# blogpost.projectassistant.ai → CNAME → your-app.ondigitalocean.app
```

## Deployment Commands

```bash
# Initial setup
doctl auth init
doctl apps create --spec .do/app.yaml

# Deploy
git push origin main  # Auto-deploys

# Run migrations
doctl apps run $APP_ID -- alembic upgrade head

# Check logs
doctl apps logs $APP_ID --tail 100

# SSH into container (debugging)
doctl apps console $APP_ID
```

## Monitoring Setup

### 1. Health Checks
```python
@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "db": check_db(),
        "timestamp": datetime.utcnow()
    }
```

### 2. Sentry (Free Tier)
```python
# In app.py
import sentry_sdk
if settings.environment == "production":
    sentry_sdk.init(dsn=settings.sentry_dsn)
```

### 3. Simple Metrics
```python
@app.get("/metrics")
async def metrics():
    return {
        "users": count_users(),
        "articles_today": count_articles_today(),
        "active_pipelines": count_active_pipelines()
    }
```

## Cost Breakdown

```yaml
Monthly Costs:
  Digital Ocean:
    - App Platform Basic: $12
    - PostgreSQL Basic: $15
    - Total DO: $27/month
  
  Optional:
    - Redis (if needed): $15
    - Spaces (storage): $5
    - Total with options: $47/month
  
  External (Free Tiers):
    - Sentry: Free (5k events/mo)
    - SendGrid: Free (100 emails/day)
    - UptimeRobot: Free (50 monitors)
```

## What We're NOT Doing

❌ Kubernetes
❌ Load balancers
❌ Multi-region
❌ Blue-green deployments
❌ Complex CI/CD
❌ Terraform/IaC
❌ Service mesh
❌ API gateway

## Success Criteria

✅ App deployed and accessible
✅ Database connected
✅ Users can register/login
✅ Articles persist
✅ Costs < $50/month
✅ Deploys in < 5 minutes
✅ Recovery in < 30 minutes

## Troubleshooting

### Common Issues

**Database connection fails:**
```bash
# Check connection string
doctl databases connection $DB_ID
# Update app env var
doctl apps update $APP_ID --spec .do/app.yaml
```

**App won't start:**
```bash
# Check logs
doctl apps logs $APP_ID --type=run
# Check build logs
doctl apps logs $APP_ID --type=build
```

**Migrations fail:**
```bash
# Run manually
doctl apps console $APP_ID
> alembic upgrade head
```

## Next Steps

1. Create Digital Ocean account
2. Set up database
3. Deploy app
4. Configure domain
5. Test everything
6. Go live!
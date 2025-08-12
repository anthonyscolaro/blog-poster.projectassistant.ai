name: "Micro-SaaS Production Deployment Plan"
description: |

## Purpose
Deploy blog-poster as a simple, reliable micro-SaaS application on Digital Ocean with focus on practicality over enterprise complexity.

## Core Principles
1. **Keep It Simple**: No over-engineering, use proven patterns
2. **Single Deployment**: One environment, with staging tests locally
3. **Quick Recovery**: Simple backup/restore, not complex failover
4. **Cost Conscious**: Target < $200/month infrastructure

---

## Goal
Deploy a functional, monitored blog content generation system to Digital Ocean that just works reliably.

## Why
- **Current State**: Local-only, manual operation, no persistence
- **Target State**: Cloud-hosted, automated, with database persistence
- **Business Need**: Generate content automatically without manual intervention
- **Budget Reality**: This is micro-SaaS, not enterprise

## What
Essential production requirements:
- PostgreSQL database with pgvector
- User authentication & management
- Persistent pipeline storage (not memory-only)
- Basic monitoring & health checks
- Simple Digital Ocean deployment
- Automated backups

### Success Criteria
- [ ] Application deployed to Digital Ocean
- [ ] Database persistence working
- [ ] User authentication implemented
- [ ] Pipelines stored in database
- [ ] Basic monitoring active
- [ ] < $200/month total cost
- [ ] Daily backups configured

## Implementation Phases (Simplified)

### Phase 1: Core Infrastructure (Week 1)
**Goal**: Get the basics running in production

```yaml
Tasks:
  Database:
    - ✅ PostgreSQL with pgvector deployed locally
    - ✅ Migration script for existing data
    - Deploy Digital Ocean Managed PostgreSQL
    - Run migrations in production
    
  Application:
    - ✅ Database repositories implemented
    - ✅ Connection pooling & retry logic
    - Add user authentication (JWT)
    - Deploy to Digital Ocean App Platform
    
  Monitoring:
    - Basic health endpoints
    - Application logs to Digital Ocean
    - Simple uptime monitoring (UptimeRobot free tier)
    
Validation:
  - App accessible via HTTPS
  - Data persisted to database
  - Can create and retrieve articles
```

### Phase 2: User Management (Week 2)
**Goal**: Add multi-user support

```yaml
Tasks:
  Authentication:
    - User registration/login endpoints
    - JWT token management
    - Password reset via email
    - API key per user
    
  Authorization:
    - User owns their articles
    - Usage tracking per user
    - Rate limiting per user
    
  UI Updates:
    - Login/signup pages
    - User dashboard
    - API key management page
    
Validation:
  - Users can register and login
  - Articles are user-scoped
  - API keys work per user
```

### Phase 3: Production Features (Week 3)
**Goal**: Add essential production features

```yaml
Tasks:
  Pipeline Persistence:
    - ✅ Store pipelines in database
    - ✅ Track pipeline history
    - Add pipeline scheduling
    - Simple retry on failure
    
  Cost Management:
    - Track API usage per user
    - Monthly limits per user
    - Usage dashboard
    
  WordPress Integration:
    - Store WP credentials per user
    - Multiple WordPress site support
    - Publishing queue
    
Validation:
  - Pipelines persist across restarts
  - Cost tracking accurate
  - Can publish to multiple WP sites
```

### Phase 4: Deploy & Monitor (Week 4)
**Goal**: Go live with monitoring

```yaml
Tasks:
  Deployment:
    - Create Digital Ocean app spec
    - Configure environment variables
    - Deploy application
    - Set up custom domain
    
  Monitoring:
    - Sentry for error tracking (free tier)
    - Basic Grafana dashboard
    - Email alerts for failures
    - Daily backup verification
    
  Documentation:
    - User guide
    - API documentation
    - Troubleshooting guide
    
Validation:
  - Production app running 24/7
  - Errors tracked in Sentry
  - Backups running daily
  - Users can self-serve
```

## Simplified Infrastructure

```yaml
Digital Ocean Resources:
  App Platform:
    Web Service:
      - 1x Basic instance ($12/mo)
      - Auto-deploy from GitHub
      - Environment variables for secrets
      
  Managed Database:
    PostgreSQL:
      - Basic tier ($15/mo)
      - Daily backups included
      - pgvector extension
      
  Spaces (Optional):
    - For file storage if needed ($5/mo)
    
  Total: ~$32-50/month initially
  
External Services (Free Tiers):
  - Sentry: Error tracking
  - SendGrid: Transactional email (100/day free)
  - UptimeRobot: Uptime monitoring
  - GitHub Actions: CI/CD
```

## Simple Deployment Process

```bash
#!/bin/bash
# deploy.sh - Simple deployment

# 1. Run tests locally
pytest tests/

# 2. Push to main branch (triggers Digital Ocean deployment)
git push origin main

# 3. Run migrations
doctl apps run $APP_ID -- alembic upgrade head

# 4. Verify health
curl https://api.yourdomain.com/health

echo "Deployment complete!"
```

## Backup Strategy (Simple)

```python
# Daily backup script (runs as cron job)
import subprocess
from datetime import datetime

def daily_backup():
    """Simple daily backup"""
    
    # 1. Backup database (DO handles this automatically)
    print("Database backup handled by Digital Ocean")
    
    # 2. Export user data (optional)
    backup_file = f"backup_{datetime.now():%Y%m%d}.sql"
    subprocess.run([
        "pg_dump", DATABASE_URL, 
        "-f", backup_file
    ])
    
    # 3. Upload to Spaces (optional)
    upload_to_spaces(backup_file)
    
    # 4. Keep last 7 backups
    cleanup_old_backups()
```

## User Authentication (Simple JWT)

```python
# src/auth/authentication.py
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Simple JWT authentication"""
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Usage in routes
@app.get("/api/articles")
async def get_articles(user_id: str = Depends(get_current_user)):
    return get_user_articles(user_id)
```

## Monitoring (Practical Approach)

```python
# Simple health checks
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": check_database(),
        "redis": check_redis(),
        "timestamp": datetime.utcnow()
    }

# Basic metrics endpoint
@app.get("/metrics")
async def metrics():
    return {
        "articles_today": count_articles_today(),
        "active_users": count_active_users(),
        "api_calls_remaining": get_api_limits(),
        "error_rate": calculate_error_rate()
    }
```

## Testing Strategy (Practical)

```python
# Essential tests only
class TestProduction:
    def test_user_can_register_and_login(self):
        """Test auth flow"""
        
    def test_article_generation_pipeline(self):
        """Test core functionality"""
        
    def test_database_persistence(self):
        """Test data saves correctly"""
        
    def test_cost_tracking(self):
        """Test usage limits work"""
        
    def test_backup_restore(self):
        """Test backup process"""
```

## Simple Incident Response

### If the app goes down:
1. Check Digital Ocean status page
2. Check application logs: `doctl apps logs $APP_ID`
3. Restart app if needed: `doctl apps restart $APP_ID`
4. Check database connection
5. Restore from backup if data issue

### If costs spike:
1. Check usage dashboard
2. Identify high-usage user
3. Temporarily disable their access
4. Contact user about limits

## Success Metrics (Realistic)

```yaml
Technical:
  - Uptime: > 95% (it's okay to have some downtime)
  - Response time: < 2s for most requests
  - Error rate: < 1%
  
Business:
  - Active users: 10-50 to start
  - Articles/day: 10-100
  - Infrastructure cost: < $200/month
  
Operational:
  - Deploy time: < 10 minutes
  - Time to fix issues: < 2 hours
  - Backup success rate: 100%
```

## What We're NOT Doing

❌ Blue-green deployments (overkill)
❌ Kubernetes (too complex)
❌ Multi-region (not needed yet)
❌ Complex CI/CD pipelines
❌ Enterprise monitoring stack
❌ 99.99% uptime SLA
❌ Microservices architecture
❌ Event sourcing
❌ CQRS patterns

## Implementation Timeline

**Week 1**: Database & Basic Deployment
- Get PostgreSQL working in production
- Deploy basic app to Digital Ocean
- Verify data persistence

**Week 2**: Add User Management
- Implement authentication
- Add user dashboard
- Scope data to users

**Week 3**: Production Features
- Pipeline persistence
- Cost tracking
- Multi-site support

**Week 4**: Polish & Monitor
- Add monitoring
- Write documentation
- Handle edge cases

## Next Steps

1. ✅ Complete PostgreSQL migration
2. Deploy to Digital Ocean
3. Add user authentication
4. Implement cost tracking
5. Set up basic monitoring

## Success = It Just Works

✅ App runs reliably
✅ Users can generate content
✅ Data doesn't get lost
✅ Costs stay under control
✅ You can sleep at night
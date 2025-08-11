name: "Master Production Deployment Plan"
description: |

## Purpose
Orchestrate the complete transformation of blog-poster from a development prototype to a production-ready, scalable content generation platform deployed on Digital Ocean.

## Core Principles
1. **Phased Rollout**: Incremental deployment with validation at each stage
2. **Zero Downtime**: Blue-green deployment strategy
3. **Rollback Ready**: Every change reversible within minutes
4. **Cost Optimized**: Start small, scale based on metrics

---

## Goal
Deploy a fully functional, monitored, and scalable blog content generation system to Digital Ocean App Platform with all production requirements met.

## Why
- **Business Impact**: Enable automated content generation at scale
- **Current Limitations**: Local-only, no persistence, manual operation
- **Target State**: 24/7 automated operation, 100+ articles/day capability
- **ROI**: Reduce content creation costs by 80%

## What
Complete production deployment including:
- Database layer implementation
- Agent service implementation  
- Configuration and secrets management
- Monitoring and alerting
- Digital Ocean App Platform deployment
- Testing and validation
- Documentation and runbooks

### Success Criteria
- [ ] All 5 PRPs implemented
- [ ] Zero data loss on deployment
- [ ] 99.9% uptime from day 1
- [ ] < $500/month infrastructure cost
- [ ] Fully automated CI/CD pipeline
- [ ] Complete monitoring coverage
- [ ] Disaster recovery tested
- [ ] Team trained on operations

## Deployment Phases

### Phase 1: Foundation (Week 1-2)
**Goal**: Establish core infrastructure and persistence layer

```yaml
Tasks:
  Database Setup:
    - Deploy Digital Ocean Managed PostgreSQL
    - Create database schema
    - Implement SQLAlchemy models
    - Set up Alembic migrations
    - Migrate existing JSON data
    
  Basic Monitoring:
    - Deploy Prometheus
    - Set up basic health checks
    - Configure logging
    - Create initial dashboards
    
  Configuration:
    - Set up Digital Ocean secrets
    - Create environment configs
    - Implement config validation
    
Validation:
  - All data persisted to database
  - Zero data loss verified
  - Basic metrics flowing
  - Secrets properly managed
```

### Phase 2: Service Implementation (Week 3-4)
**Goal**: Implement all agent services with job queuing

```yaml
Tasks:
  Celery Setup:
    - Deploy Redis for queuing
    - Configure Celery workers
    - Implement retry logic
    - Set up task routing
    
  Agent Implementation:
    - Article Generator Agent
    - Fact Checker Agent
    - Competitor Monitor Agent
    - Topic Analyzer Agent
    - WordPress Publisher Agent
    
  Integration:
    - Connect agents to queue
    - Implement circuit breakers
    - Add error handling
    
Validation:
  - All agents functional
  - Job queue processing
  - Retry logic working
  - Error recovery tested
```

### Phase 3: Initial Deployment (Week 5)
**Goal**: Deploy to Digital Ocean staging environment

```yaml
Tasks:
  App Platform Setup:
    - Create app specification
    - Configure services
    - Set up databases
    - Configure domains
    
  Deployment:
    - Build Docker images
    - Push to registry
    - Deploy to staging
    - Run smoke tests
    
  Testing:
    - End-to-end pipeline test
    - Performance testing
    - Security scanning
    - Load testing
    
Validation:
  - Application accessible
  - All endpoints working
  - Database connected
  - Monitoring active
```

### Phase 4: Production Readiness (Week 6)
**Goal**: Complete monitoring, alerting, and documentation

```yaml
Tasks:
  Observability:
    - Complete Grafana dashboards
    - Configure all alerts
    - Set up PagerDuty
    - Implement tracing
    
  Documentation:
    - Operation runbooks
    - Incident response guides
    - API documentation
    - Architecture diagrams
    
  Security:
    - Security audit
    - Penetration testing
    - SSL certificates
    - Access controls
    
Validation:
  - All alerts tested
  - Runbooks validated
  - Security scan passed
  - Team trained
```

### Phase 5: Production Launch (Week 7)
**Goal**: Go live with production system

```yaml
Tasks:
  Production Deployment:
    - Deploy to production
    - Configure DNS
    - Enable auto-scaling
    - Activate monitoring
    
  Cutover:
    - Final data migration
    - Switch WordPress integration
    - Enable scheduled jobs
    - Monitor closely
    
  Optimization:
    - Performance tuning
    - Cost optimization
    - Cache configuration
    - Query optimization
    
Validation:
  - Production live
  - Articles generating
  - WordPress publishing
  - SLA metrics met
```

## Infrastructure Architecture

```yaml
Digital Ocean Resources:
  App Platform:
    API Service:
      - 2x Professional-XS instances
      - Auto-scaling 2-4 instances
      - Health checks enabled
      
    Worker Service:
      - 3x Professional-S instances
      - Separate queues per agent
      - Auto-restart on failure
      
  Managed Databases:
    PostgreSQL:
      - 2GB RAM, 1 vCPU
      - Daily backups
      - Read replica for analytics
      
    Redis:
      - 1GB RAM
      - Persistence enabled
      - Used for queuing and caching
      
  Spaces:
    - Static file storage
    - Backup storage
    - Log archives
    
  Monitoring:
    - Managed Kubernetes for monitoring stack
    - Or use monitoring droplet
    
Total Estimated Cost: $400-500/month
```

## Deployment Automation

```bash
#!/bin/bash
# deploy.sh - Automated deployment script

set -e

ENVIRONMENT=$1
VERSION=$2

echo "Deploying version $VERSION to $ENVIRONMENT"

# Run tests
echo "Running tests..."
pytest tests/ --cov=src --cov-report=term-missing

# Build Docker image
echo "Building Docker image..."
docker build -t blog-poster:$VERSION .

# Push to registry
echo "Pushing to Digital Ocean registry..."
doctl registry login
docker tag blog-poster:$VERSION registry.digitalocean.com/blogposter/api:$VERSION
docker push registry.digitalocean.com/blogposter/api:$VERSION

# Update app spec
echo "Updating app specification..."
sed -i "s/:latest/:$VERSION/g" .do/app.yaml

# Deploy
echo "Deploying to Digital Ocean..."
doctl apps create-deployment $APP_ID --spec .do/app.yaml

# Wait for deployment
echo "Waiting for deployment to complete..."
doctl apps get-deployment $APP_ID $DEPLOYMENT_ID --wait

# Run smoke tests
echo "Running smoke tests..."
python scripts/smoke_tests.py --env $ENVIRONMENT

# Update monitoring
echo "Updating monitoring dashboards..."
python scripts/update_dashboards.py --version $VERSION

echo "Deployment complete!"
```

## Rollback Strategy

```python
# scripts/rollback.py
import subprocess
import sys
from datetime import datetime

def rollback(environment: str, target_version: str):
    """Rollback to previous version"""
    
    print(f"Starting rollback to {target_version}")
    
    # 1. Create database backup
    print("Creating database backup...")
    subprocess.run([
        "pg_dump",
        os.getenv('DATABASE_URL'),
        "-f", f"backup_{datetime.now().isoformat()}.sql"
    ])
    
    # 2. Switch traffic to maintenance mode
    print("Enabling maintenance mode...")
    set_maintenance_mode(True)
    
    # 3. Deploy previous version
    print(f"Deploying version {target_version}...")
    subprocess.run([
        "doctl", "apps", "create-deployment",
        APP_ID, "--image", f"api:{target_version}"
    ])
    
    # 4. Run database migrations (if needed)
    print("Running migrations...")
    subprocess.run(["alembic", "downgrade", target_version])
    
    # 5. Verify health
    print("Verifying health...")
    if not check_health():
        print("Health check failed! Manual intervention required.")
        sys.exit(1)
        
    # 6. Disable maintenance mode
    print("Disabling maintenance mode...")
    set_maintenance_mode(False)
    
    print("Rollback complete!")
```

## Testing Strategy

```python
# tests/test_production_ready.py
import pytest
from typing import Dict

class TestProductionReadiness:
    """Validate production readiness"""
    
    def test_database_connectivity(self):
        """Test database connections"""
        assert db.execute("SELECT 1").scalar() == 1
        
    def test_redis_connectivity(self):
        """Test Redis connection"""
        assert redis.ping() == True
        
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
        
    def test_all_agents_functional(self):
        """Test all agents are working"""
        agents = [
            'competitor_monitor',
            'topic_analyzer',
            'article_generator',
            'fact_checker',
            'wordpress_publisher'
        ]
        
        for agent in agents:
            result = test_agent(agent)
            assert result["status"] == "success"
            
    def test_monitoring_metrics(self):
        """Test metrics are being collected"""
        metrics = get_metrics()
        assert len(metrics) > 0
        assert "pipeline_runs_total" in metrics
        
    def test_secret_management(self):
        """Test secrets are properly managed"""
        # Should not be able to access raw secrets
        with pytest.raises(Unauthorized):
            get_secret("ANTHROPIC_API_KEY")
            
    def test_configuration_validation(self):
        """Test configuration is valid"""
        config = load_config()
        errors = validate_config(config)
        assert len(errors) == 0
        
    def test_error_recovery(self):
        """Test error recovery mechanisms"""
        # Simulate failure
        cause_failure()
        
        # Should recover
        wait_for_recovery()
        
        assert check_health()["status"] == "healthy"
```

## Operational Runbooks

### Runbook: Pipeline Stuck
```markdown
## Symptoms
- Pipeline status shows "running" for > 30 minutes
- No new logs in last 10 minutes
- Worker appears hung

## Resolution
1. Check worker status:
   ```bash
   doctl apps logs $APP_ID --type=worker --tail=100
   ```

2. Check for deadlocks:
   ```sql
   SELECT * FROM pg_stat_activity WHERE state = 'active';
   ```

3. Restart stuck worker:
   ```bash
   doctl apps restart $APP_ID --component=worker
   ```

4. Retry pipeline:
   ```bash
   curl -X POST https://api.blogposter.com/pipeline/$ID/retry
   ```
```

### Runbook: High Cost Alert
```markdown
## Symptoms
- Cost exceeds daily budget
- Alert: "BudgetExceeded"

## Resolution
1. Check current spend:
   ```bash
   curl https://api.blogposter.com/metrics/costs/today
   ```

2. Identify high-cost pipelines:
   ```sql
   SELECT pipeline_id, total_cost 
   FROM pipelines 
   WHERE created_at > NOW() - INTERVAL '24 hours'
   ORDER BY total_cost DESC;
   ```

3. Temporarily disable generation:
   ```bash
   curl -X POST https://api.blogposter.com/config/pause-generation
   ```

4. Review and optimize prompts
```

## Team Training Plan

```yaml
Week 1:
  - Architecture overview
  - Local development setup
  - Basic operations
  
Week 2:
  - Monitoring and alerting
  - Incident response
  - Runbook walkthrough
  
Week 3:
  - Deployment process
  - Configuration management
  - Security practices
  
Week 4:
  - Performance optimization
  - Cost management
  - Advanced troubleshooting
```

## Success Metrics

```yaml
Technical Metrics:
  - Uptime: > 99.9%
  - Response time: < 1s (p95)
  - Error rate: < 0.1%
  - Recovery time: < 30 minutes
  
Business Metrics:
  - Articles/day: > 10
  - Cost/article: < $1.50
  - Publishing success: > 95%
  - SEO score average: > 85
  
Operational Metrics:
  - Deployment frequency: Weekly
  - Lead time: < 1 day
  - MTTR: < 30 minutes
  - Change failure rate: < 5%
```

## Risk Mitigation

```yaml
Risks:
  API Rate Limits:
    Mitigation: Implement rate limiting, queue throttling
    
  Cost Overrun:
    Mitigation: Budget alerts, automatic pausing
    
  Data Loss:
    Mitigation: Daily backups, point-in-time recovery
    
  Security Breach:
    Mitigation: Encrypted secrets, audit logging, access controls
    
  Service Outage:
    Mitigation: Multi-region deployment, auto-failover
```

---

## Implementation Timeline

**Month 1**: Foundation & Services
- Week 1-2: Database & Configuration
- Week 3-4: Agent Implementation

**Month 2**: Deployment & Production
- Week 5: Staging Deployment
- Week 6: Production Readiness
- Week 7: Production Launch
- Week 8: Optimization & Tuning

## Next Steps

1. Review and approve all 5 PRPs
2. Set up Digital Ocean project
3. Begin Phase 1 implementation
4. Schedule weekly progress reviews
5. Assign team responsibilities

## Success Criteria

✅ All production gaps addressed
✅ System deployed and operational
✅ Generating 10+ articles daily
✅ 99.9% uptime achieved
✅ Total cost < $500/month
✅ Team fully trained
✅ Documentation complete
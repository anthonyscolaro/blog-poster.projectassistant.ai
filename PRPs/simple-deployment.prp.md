name: "Simple Digital Ocean Deployment for Single User"
description: |

## Purpose
Get the blog-poster app deployed to Digital Ocean as quickly and simply as possible for single-user operation on servicedogus.org.

## Core Principles
1. **Simplicity First**: Minimal infrastructure, maximum functionality
2. **Cost Effective**: Target < $50/month total cost
3. **Quick Deployment**: Get it running today, optimize later
4. **Single User**: No need for auth, multi-tenancy, or complex scaling

---

## Goal
Deploy a working blog content generator to Digital Ocean that can create and publish articles to servicedogus.org.

## Why
- **Current Issue**: Running locally requires computer to be on
- **Solution**: Cloud deployment for 24/7 availability
- **Benefit**: Can generate articles anytime from anywhere

## What
Simple deployment with:
- Single Digital Ocean App Platform service
- SQLite for data (or just JSON files)
- Basic environment variables for secrets
- No complex monitoring (just use DO's built-in)

### Success Criteria
- [x] App accessible via web browser
- [x] Can generate articles using Claude API
- [x] Articles publish to WordPress
- [x] Data persists between restarts
- [x] Total cost under $50/month

## Deployment Steps

### Step 1: Prepare the App (30 minutes)
```bash
# 1. Update Dockerfile to use production settings
# 2. Ensure data directory is persistent
# 3. Test locally with Docker
docker build -t blog-poster .
docker run -p 8088:8088 blog-poster
```

### Step 2: Create Digital Ocean App (15 minutes)
```yaml
# .do/app.yaml
name: blog-poster-simple
region: nyc

services:
  - name: web
    github:
      repo: anthonyscolaro/blog-poster
      branch: main
      deploy_on_push: true
    
    dockerfile_path: Dockerfile
    http_port: 8088
    
    instance_size_slug: basic-xxs  # $4/month
    instance_count: 1
    
    health_check:
      http_path: /health
      timeout_seconds: 10
      
    envs:
      # API Keys
      - key: ANTHROPIC_API_KEY
        type: SECRET
        value: "sk-ant-..."  # Add via DO dashboard
      
      - key: JINA_API_KEY
        type: SECRET
        value: "jina_..."
        
      # WordPress Config
      - key: WORDPRESS_URL
        value: "https://servicedogus.org"
        
      - key: WP_USERNAME
        type: SECRET
        value: "your-username"
        
      - key: WP_APP_PASSWORD
        type: SECRET
        value: "xxxx xxxx xxxx xxxx"
        
      # App Config
      - key: ENVIRONMENT
        value: "production"
        
      - key: MAX_COST_PER_ARTICLE
        value: "2.00"
        
      - key: MAX_MONTHLY_COST
        value: "100.00"
```

### Step 3: Deploy with CLI (10 minutes)
```bash
# Create the app
doctl apps create --spec .do/app.yaml

# Get the app ID
doctl apps list

# Watch deployment
doctl apps get <app-id>

# Get the URL
doctl apps get <app-id> --format "DefaultIngress"
```

### Step 4: Configure Persistent Storage (Optional)
If you need data to persist:
```yaml
# Add a volume mount
mounts:
  - path: /app/data
    source_path: /data
```

Or just use Digital Ocean Spaces for file storage (S3-compatible).

### Step 5: Set Up Domain (Optional)
```bash
# Add custom domain
doctl apps update <app-id> --spec .do/app.yaml

# In app.yaml add:
domains:
  - domain: blog-tools.servicedogus.org
    type: PRIMARY
```

## Cost Breakdown
```yaml
Monthly Costs:
  App Platform:
    - Basic-XXS instance: $4/month
    - Or Basic-XS for more memory: $10/month
    
  Storage (if needed):
    - Spaces (S3-like): $5/month for 250GB
    
  Total: $4-15/month
  
API Costs (separate):
  - Anthropic Claude: ~$0.50-2.00 per article
  - Jina AI: Free tier or ~$0.10 per scrape
```

## What We're NOT Doing
- ❌ No PostgreSQL (use SQLite or files)
- ❌ No Redis (use in-memory queuing)
- ❌ No Celery (simple async with FastAPI)
- ❌ No monitoring stack (use DO's dashboard)
- ❌ No load balancing (single instance)
- ❌ No CI/CD pipeline (manual deploys are fine)
- ❌ No backup strategy (can regenerate articles)
- ❌ No blue-green deployments
- ❌ No auto-scaling

## Quick Fixes Needed Before Deploy

### 1. Make Article Generator Actually Work
```python
# src/services/article_generator.py
async def generate_article(topic: str) -> Dict:
    """Actually call Claude API"""
    claude = AsyncAnthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    
    response = await claude.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4000,
        messages=[{
            "role": "user",
            "content": f"Write a 1500+ word SEO article about: {topic}"
        }]
    )
    
    return {
        "content": response.content[0].text,
        "cost": calculate_cost(response.usage)
    }
```

### 2. Use Local File Storage
```python
# src/services/storage.py
import json
from pathlib import Path

DATA_DIR = Path("/app/data")
DATA_DIR.mkdir(exist_ok=True)

def save_article(article: Dict) -> str:
    """Save article to JSON file"""
    filename = f"{article['slug']}_{datetime.now().isoformat()}.json"
    filepath = DATA_DIR / "articles" / filename
    
    with open(filepath, 'w') as f:
        json.dump(article, f)
    
    return str(filepath)
```

### 3. Simplify the Pipeline
```python
# Just make it work
async def run_pipeline(topic: str):
    # 1. Generate article
    article = await generate_article(topic)
    
    # 2. Save locally
    save_article(article)
    
    # 3. Publish to WordPress
    result = await publish_to_wordpress(article)
    
    return {"success": True, "article": article, "wp_result": result}
```

## Deployment Checklist
- [ ] Test locally with real API keys
- [ ] Verify WordPress publishing works
- [ ] Create Digital Ocean account
- [ ] Install doctl CLI
- [ ] Create app with spec file
- [ ] Add secrets via DO dashboard
- [ ] Test the deployed app
- [ ] Generate first article in production

## Maintenance
- Check logs: `doctl apps logs <app-id> --tail 100`
- Restart if needed: `doctl apps restart <app-id>`
- Update code: Just push to GitHub (if auto-deploy enabled)
- Check costs: DO dashboard shows resource usage

---

## Timeline: Deploy Today!
1. **Hour 1**: Fix article generator to use real Claude API
2. **Hour 2**: Test locally with production credentials  
3. **Hour 3**: Deploy to Digital Ocean
4. **Hour 4**: Test and generate first article

No complex infrastructure, no over-engineering. Just a simple tool deployed to the cloud that works for your needs.
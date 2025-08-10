# Blog-Poster Quick Start Guide

Get the blog-poster service up and running in 5 minutes!

## Prerequisites Check

```bash
# Verify Docker is installed
docker --version  # Should be 2.0+

# Check available ports
lsof -i :8088 || echo "Port 8088 is free ✓"
lsof -i :6333 || echo "Port 6333 is free ✓"
```

## 🚀 5-Minute Setup

### 1. Configure Environment (1 min)

```bash
# Copy and edit environment file
cp .env.local.example .env.local
nano .env.local
```

Add your API keys:
```bash
ANTHROPIC_API_KEY=sk-ant-api03-xxxxx  # Required
JINA_API_KEY=jina_xxxxx              # Required for scraping
WORDPRESS_URL=https://your-wp-site.com
WP_USERNAME=admin
WP_APP_PASSWORD=xxxx xxxx xxxx xxxx   # From WP Admin
```

### 2. Start Services (2 min)

```bash
# Start all services
docker compose up -d

# Wait for services to be ready
sleep 30

# Verify health
curl http://localhost:8088/health
```

### 3. Test the System (2 min)

```bash
# Test SEO linting
curl -X POST http://localhost:8088/seo/lint \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Quick Test",
    "meta_desc": "Testing the blog-poster service",
    "word_count": 1500
  }'

# Test WordPress connection
curl -X POST http://localhost:8088/publish/wp \
  -H "Content-Type: application/json" \
  -d '{
    "frontmatter": {
      "title": "Test Post",
      "slug": "test-post",
      "category": "ADA Compliance"
    },
    "markdown": "# Test\n\nThis is a test.",
    "status": "DRAFT"
  }'
```

## 📝 Common Workflows

### Generate an Article

```bash
# Create topic input file
cat > topic.json << 'EOF'
{
  "topic": "Service Dog Training Requirements",
  "keywords": ["service dog", "training", "ADA", "requirements"],
  "target_length": 2000,
  "style": "informative",
  "include_citations": true
}
EOF

# Trigger article generation
curl -X POST http://localhost:8088/agent/run \
  -H "Content-Type: application/json" \
  -d @topic.json
```

### Check SEO Compliance

```bash
curl -X POST http://localhost:8088/seo/lint \
  -H "Content-Type: application/json" \
  -d @test-seo.json
```

### Publish to WordPress

```bash
# Publish as draft
curl -X POST http://localhost:8088/publish/wp \
  -H "Content-Type: application/json" \
  -d @test-input.json

# Response includes WordPress post ID and URL
```

## 🎯 API Endpoints

| Endpoint | Method | Description | Status |
|----------|--------|-------------|---------|
| `/health` | GET | Service health check | ✅ Working |
| `/seo/lint` | POST | Validate SEO compliance | ✅ Working |
| `/publish/wp` | POST | Publish to WordPress | ✅ Working |
| `/agent/run` | POST | Run article generation | ⚠️ Stubbed |
| `/docs` | GET | OpenAPI documentation | ✅ Working |

## 📊 Monitor Services

### View Logs
```bash
# All services
docker compose logs -f

# Specific service
docker compose logs api -f --tail=50
```

### Check Status
```bash
# Service status
docker compose ps

# API metrics (if implemented)
curl http://localhost:8088/metrics

# Qdrant dashboard
open http://localhost:6333/dashboard
```

## 🔧 Quick Fixes

### Services Not Starting?
```bash
# Reset everything
docker compose down -v
docker compose up -d --build
```

### WordPress Connection Failed?
```bash
# Check SSL setting in .env.local
WP_VERIFY_SSL=false  # For local development

# Regenerate Application Password in WP Admin
```

### Port Already in Use?
```bash
# Find and kill process
lsof -i :8088
kill -9 <PID>
```

## 📚 Test Data Files

The project includes test files for quick validation:

- `test-input.json` - Sample article for publishing
- `test-seo.json` - SEO validation test
- `topic-input.json` - Article generation request

## 🚦 Service Status Indicators

✅ **Healthy Service**:
```json
{"status":"healthy","services":{"api":"ok","qdrant":"ok","redis":"ok"}}
```

⚠️ **Degraded Service**:
```json
{"status":"degraded","services":{"api":"ok","qdrant":"error","redis":"ok"}}
```

## 📖 Next Steps

1. **Explore the API**: http://localhost:8088/docs
2. **Configure WordPress**: Ensure categories and users are set up
3. **Test Full Workflow**: Generate → Review → Publish
4. **Set Up Monitoring**: Configure alerts for production
5. **Implement Missing Agents**: Complete stubbed functionality

## 🆘 Getting Help

- **API Documentation**: http://localhost:8088/docs
- **Service Logs**: `docker compose logs -f`
- **Setup Guide**: See [SETUP.md](SETUP.md)
- **Full Documentation**: See [README.md](../../README.md)

## 🎉 Success Checklist

- [ ] Environment configured (`.env.local`)
- [ ] Services running (`docker compose ps`)
- [ ] Health check passing (`/health`)
- [ ] SEO linting working (`/seo/lint`)
- [ ] WordPress connected (`/publish/wp`)
- [ ] Test article published

Once all items are checked, your blog-poster service is ready! 🚀
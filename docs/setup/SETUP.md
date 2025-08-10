# Blog-Poster Setup Guide

## Prerequisites

Before setting up the blog-poster service, ensure you have:

- Docker and Docker Compose installed (v2.0+)
- Python 3.11+ (for local development)
- API keys for:
  - Anthropic Claude API (`ANTHROPIC_API_KEY`)
  - Jina AI for web scraping (`JINA_API_KEY`)
  - WordPress with WPGraphQL installed
- At least 8GB RAM available for Docker
- Ports available: 8088, 6333, 5433, 6384

## 🚀 Quick Setup

### 1. Clone and Configure

```bash
# Navigate to project directory
cd ~/apps/blog-poster

# Copy environment template
cp .env.local.example .env.local

# Edit with your credentials
nano .env.local
```

### 2. Configure Environment Variables

Edit `.env.local` with your credentials:

```bash
# LLM Provider (at least one required)
ANTHROPIC_API_KEY=sk-ant-api03-xxxxx
OPENAI_API_KEY=sk-xxxxx  # Optional fallback

# Web Scraping
JINA_API_KEY=jina_xxxxx

# WordPress Configuration
WORDPRESS_URL=https://wp.servicedogus.test
WORDPRESS_LOCAL_URL=https://host.docker.internal:8445  # For Docker
WP_USERNAME=admin
WP_APP_PASSWORD=xxxx xxxx xxxx xxxx  # Generate in WP Admin

# Optional Settings
WP_VERIFY_SSL=false  # For local development with self-signed certs
MAX_COST_PER_ARTICLE=0.50
MAX_MONTHLY_COST=100.00
```

### 3. Start Services

```bash
# Build and start all services
docker compose up -d --build

# Verify services are running
docker compose ps

# Check logs
docker compose logs -f
```

### 4. Verify Installation

```bash
# API health check
curl http://localhost:8088/health

# Should return:
# {"status":"healthy","services":{"api":"ok","qdrant":"ok","redis":"ok"}}
```

## 📋 WordPress Setup

### Generate Application Password

1. Log into WordPress Admin
2. Go to Users → Your Profile  
3. Scroll to "Application Passwords"
4. Enter name: "Blog Poster"
5. Click "Add New Application Password"
6. Copy the generated password (spaces included)
7. Add to `.env.local` as `WP_APP_PASSWORD`

### Install Required Plugins

Ensure your WordPress site has:

- **WPGraphQL** - For content management
- **WPGraphQL JWT Authentication** (optional) - For JWT auth
- **Application Passwords** - Built into WordPress 5.6+

### Configure WPGraphQL

1. Install and activate WPGraphQL plugin
2. Go to GraphQL → Settings
3. Enable "Public Introspection"
4. Set GraphQL endpoint to `/graphql`

### Test WordPress Connection

```bash
# Test publishing endpoint
curl -X POST http://localhost:8088/publish/wp \
  -H "Content-Type: application/json" \
  -d '{
    "frontmatter": {
      "title": "Connection Test",
      "slug": "connection-test",
      "category": "ADA Compliance"
    },
    "markdown": "# Test\n\nTesting connection.",
    "status": "DRAFT"
  }'
```

## 🔧 Service Configuration

### Port Allocation

| Service | Port | Description |
|---------|------|-------------|
| API | 8088 | FastAPI REST endpoints |
| Qdrant | 6333 | Vector database |
| PostgreSQL | 5433 | pgvector embeddings |
| Redis | 6384 | Queue and cache |

### Database Initialization

#### Qdrant Collections

The service automatically creates required collections on startup:
- `internal_links` - For semantic search of existing content
- `competitors` - For competitor content analysis

#### PostgreSQL with pgvector

The pgvector extension is automatically installed. To verify:

```bash
docker exec -it blog-vectors psql -U postgres -d vectors -c "SELECT * FROM pg_extension WHERE extname = 'vector';"
```

## 🧪 Testing the Setup

### 1. Test SEO Linting

```bash
curl -X POST http://localhost:8088/seo/lint \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Service Dog Requirements Under ADA",
    "meta_desc": "Learn about ADA service dog requirements and your rights.",
    "word_count": 1500,
    "h1_count": 1,
    "h2_count": 5
  }'
```

### 2. Test Article Generation (Stubbed)

```bash
curl -X POST http://localhost:8088/agent/run \
  -H "Content-Type: application/json" \
  -d @topic-input.json
```

### 3. Test Publishing

```bash
curl -X POST http://localhost:8088/publish/wp \
  -H "Content-Type: application/json" \
  -d @test-input.json
```

## 🐛 Troubleshooting

### Port Conflicts

If you see "bind: address already in use":

```bash
# Find process using port
lsof -i :8088  # Replace with conflicting port

# Kill process
kill -9 <PID>

# Or change port in docker-compose.yml
```

### WordPress Connection Issues

1. **SSL Certificate Errors**:
   ```bash
   # Set in .env.local
   WP_VERIFY_SSL=false
   ```

2. **Authentication Failures**:
   - Regenerate Application Password
   - Ensure password includes spaces
   - Check username is correct

3. **GraphQL Errors**:
   - Verify WPGraphQL is activated
   - Check endpoint URL: `/graphql`
   - Enable WordPress debug mode

### Docker Issues

```bash
# Reset everything
docker compose down -v
docker compose up -d --build

# Check disk space
docker system df

# Clean up
docker system prune -a
```

### API Key Issues

1. **Anthropic API**:
   - Verify key starts with `sk-ant-`
   - Check usage limits at console.anthropic.com
   
2. **Jina AI**:
   - Verify key format `jina_xxxxx`
   - Check rate limits

## 🚀 Local Development

### Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run without Docker
export $(cat .env.local | xargs)
uvicorn app:app --reload --port 8088
```

### Development Tools

```bash
# Format code
black .

# Type checking
mypy app.py

# Linting
flake8 .
```

## 📊 Monitoring

### Service Health

```bash
# API metrics
curl http://localhost:8088/metrics

# Qdrant dashboard
open http://localhost:6333/dashboard

# Redis monitoring
docker exec blog-redis redis-cli monitor
```

### Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs api -f --tail=100
```

## 🔐 Security Considerations

1. **Never commit `.env.local`** - It contains sensitive API keys
2. **Use Application Passwords** - More secure than regular passwords
3. **Enable SSL in production** - Set `WP_VERIFY_SSL=true`
4. **Rotate API keys regularly** - Update in `.env.local`
5. **Monitor costs** - Set budget limits in environment variables

## 📚 Next Steps

Once setup is complete:

1. Review the API documentation at http://localhost:8088/docs
2. Test the workflow with sample data
3. Configure content categories in WordPress
4. Set up monitoring dashboards
5. Create initial article topics

For usage instructions, see [QUICKSTART.md](QUICKSTART.md).
For production deployment, see [Infrastructure Setup](../deployment/INFRASTRUCTURE_SETUP.md).
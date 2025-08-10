# Blog Poster - Automated SEO Content Generation Service

An independent AI-powered service for automated blog content generation, monitoring, and publishing for ServiceDogUS.

## Overview

Blog Poster is a multi-agent system that:
- Monitors competitor content and trends
- Analyzes topics for SEO opportunities
- Generates high-quality, fact-checked articles
- Publishes content to WordPress via WPGraphQL
- Operates completely independently from the main ServiceDogUS site

### Implementation Status
**Current Stage**: MVP Functional (80% Complete)
- ✅ Infrastructure and Docker setup complete
- ✅ WordPress publishing fully functional
- ✅ Article generation with AI working
- ✅ Competitor monitoring implemented
- ✅ Development tools configured (hot reload, linting)
- ⚠️ Legal fact checker stubbed
- ❌ Vector search pending

See [PROGRESS.md](PROGRESS.md) for detailed status.

## Architecture

This service runs separately from the main ServiceDogUS application with its own:
- Docker containers
- Port allocations
- Configuration files
- Database instances

### Port Allocation

| Service | Port | Description |
|---------|------|-------------|
| API | 8088 | FastAPI REST endpoints |
| Qdrant | 6333 | Vector database for semantic search |
| PostgreSQL | 5433 | pgvector for embeddings |
| Redis | 6384 | Job queue and caching |

Note: These ports are different from the main site to avoid conflicts.

## 🚀 Quick Start

```bash
# 1. Clone and configure
git clone https://github.com/anthonyscolaro/blog-poster.git
cd blog-poster
cp .env.example .env.local

# 2. Edit .env.local with your credentials:
#    - WordPress username/password
#    - AI API keys (Anthropic or OpenAI)
#    - Web scraping keys (optional)
nano .env.local

# 3. Start services
docker compose up -d

# 4. Verify health
curl http://localhost:8088/health

# 5. Test WordPress connection
python examples/test_direct_publish.py

# 6. Run complete workflow
python examples/complete_workflow.py
```

For detailed setup instructions, see [docs/setup/QUICKSTART.md](docs/setup/QUICKSTART.md).

## Configuration

### Required Environment Variables

```env
# AI Provider (at least one required)
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...

# Web Scraping
JINA_API_KEY=jina_...

# WordPress Connection
WORDPRESS_URL=http://localhost:8084
WORDPRESS_ADMIN_USER=admin
WORDPRESS_ADMIN_PASSWORD=your-password
```

### WordPress Integration

The service connects to your WordPress site via REST API.

#### Local Development Setup
1. Install **JSON Basic Authentication** plugin for local WordPress
2. Configure permalinks (Settings → Permalinks → Custom: `/%category%/%postname%/`)
3. Set credentials in `.env.local`:
   ```env
   WP_AUTH_METHOD=basic
   WP_USERNAME=your-username
   WP_APP_PASSWORD=your-password
   ```

#### Production Setup
1. Use Application Passwords (requires HTTPS)
2. Generate password in WordPress Admin → Users → Profile
3. Update `.env.local` with production URL and credentials

## Usage

### Test WordPress Connection

```bash
# Check if WordPress is accessible
curl http://localhost:8088/wordpress/test

# Or use the Python test script
python examples/test_wordpress_publish.py
```

### Generate and Publish an Article

```bash
# Complete workflow: Generate → Publish
python examples/complete_workflow.py

# Or use individual endpoints:

# 1. Generate article with AI
curl -X POST "http://localhost:8088/article/generate" \
  -G --data-urlencode "topic=Service Dog Training Tips" \
  --data-urlencode "primary_keyword=service dog training" \
  --data-urlencode "min_words=800" \
  --data-urlencode "max_words=1200"

# 2. Publish to WordPress
curl -X POST "http://localhost:8088/publish/wp" \
  -G --data-urlencode "title=Your Article Title" \
  --data-urlencode "content=Article content here..." \
  --data-urlencode "status=draft"
```

### Monitor Competitors

```bash
# Scan competitor websites
curl -X POST http://localhost:8088/competitors/scan

# Get competitor insights
curl http://localhost:8088/competitors/insights
```

### Check SEO Compliance

```bash
curl -X POST http://localhost:8088/seo/lint \
  -H "Content-Type: application/json" \
  -d @examples/test-seo.json
```

## Development

### Available Commands

```bash
make format    # Format code with black/isort
make lint      # Run linting checks
make logs      # View API logs
make restart   # Restart API container
make shell     # Access container shell
```

### Testing Scripts

```bash
# Test WordPress publishing
python examples/test_direct_publish.py

# Complete workflow test
python examples/complete_workflow.py

# Quick credentials check
./examples/quick_test.sh
```

### Hot Reload

The API automatically reloads when you modify code. No container restart needed!

## Agents

### 1. Competitor Monitoring Agent (✅ Implemented)
- Scrapes competitor blogs with Jina AI
- Falls back to Bright Data for social media
- Tracks trending topics and content gaps
- **Status**: Fully functional

### 2. Topic Analysis Agent (✅ Implemented)
- Analyzes trending topics from competitors
- Identifies content opportunities
- Scores topics by SEO potential
- **Status**: Working within competitor agent

### 3. Article Generation Agent (✅ Implemented)
- Uses Claude 3.5 Sonnet (primary)
- Falls back to GPT-4 Turbo
- Generates SEO-optimized content
- Tracks costs per article
- **Status**: Fully functional with valid API keys

### 4. Legal Fact Checker Agent (⚠️ Stubbed)
- Will verify legal claims
- Ensures ADA compliance accuracy
- **Status**: Returns hardcoded "verified"

### 5. WordPress Publishing Agent (✅ Functional)
- Publishes via REST API
- Supports Basic Auth (local) and App Passwords (production)
- Creates draft or published posts
- Sets SEO metadata
- **Status**: Fully implemented and working

## Docker Commands

```bash
# Start services
docker compose up -d

# Stop services
docker compose down

# View logs
docker compose logs -f [service-name]

# Restart a specific service
docker compose restart api

# Remove all data and start fresh
docker compose down -v
docker compose up -d --build
```

## Directory Structure

```
blog-poster/
├── app.py                  # Main FastAPI application
├── contracts.py            # Pydantic models
├── orchestrator.py         # Workflow orchestration
├── wordpress_agent.py      # WordPress publishing
├── docker-compose.yml      # Service definitions
├── requirements.txt        # Python dependencies
├── .env.local             # Configuration (git-ignored)
├── .env.local.example     # Configuration template
├── data/                  # Persistent data (git-ignored)
│   ├── competitors/       # Scraped content
│   ├── articles/          # Generated articles
│   └── logs/              # Application logs
└── sonnet-3.5-prompt.txt  # AI system prompt
```

## Monitoring

### Health Checks

```bash
# API health
curl http://localhost:8088/health

# Qdrant status
curl http://localhost:6333/collections

# View metrics
curl http://localhost:8088/metrics
```

### Dashboards

- API Documentation: http://localhost:8088/docs
- Qdrant Dashboard: http://localhost:6333/dashboard

## Troubleshooting

### Services Not Starting

```bash
# Check logs for errors
docker compose logs api
docker compose logs qdrant

# Verify port availability
lsof -i :8088
lsof -i :6333
lsof -i :5433
lsof -i :6384
```

### Connection Issues

1. Verify WordPress URL in `.env.local`
2. Check WordPress authentication credentials
3. Ensure WPGraphQL is accessible
4. Verify SSL settings for local development

### API Key Issues

1. Ensure API keys are correctly set in `.env.local`
2. Verify API key quotas and limits
3. Check rate limiting settings

## Development

### Running Locally (Without Docker)

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export $(cat .env.local | xargs)

# Run the API
uvicorn app:app --reload --port 8088
```

### Testing

**Note**: Test suite not yet implemented. Planned testing structure:

```bash
# Future test commands (not yet available):
# pytest tests/
# python -m agents.topic_analysis --test
# python -m tools.prompt_validator
```

### Creating Missing Components

To complete the implementation, the following need to be created:
1. Agent implementations in `/agents/` directory
2. LLM integration in article generation
3. Jina AI scraping integration
4. Vector search implementation
5. Test suite in `/tests/` directory

## Production Deployment

For production deployment:

1. Use production environment variables
2. Enable HTTPS/SSL
3. Set up proper monitoring and alerting
4. Configure backup strategies
5. Implement rate limiting
6. Use managed databases (RDS, Cloud SQL)

## Security Considerations

- API keys are stored in `.env.local` (never commit)
- WordPress credentials use Application Passwords
- All external URLs are validated
- Content is fact-checked before publishing
- Rate limiting prevents API abuse

## Cost Management

The service includes cost controls:
- `MAX_COST_PER_ARTICLE`: Limits per-article spending
- `MAX_MONTHLY_COST`: Monthly budget cap
- Cost tracking and alerts at 80% threshold

## 📚 Documentation

All documentation is organized in the `docs/` directory:

- **[Documentation Index](docs/index.md)** - Complete documentation overview
- **[Setup Guide](docs/setup/SETUP.md)** - Detailed installation instructions  
- **[Quick Start](docs/setup/QUICKSTART.md)** - 5-minute setup
- **[API Documentation](docs/api/blog-poster.md)** - Endpoint details
- **[Development Guides](docs/guides/)** - Best practices and workflows
- **[Deployment Guides](docs/deployment/)** - Production deployment

## 📁 Project Structure

```
blog-poster/
├── app.py                    # Main FastAPI application
├── orchestrator.py           # Workflow orchestration  
├── wordpress_agent.py        # WordPress publishing
├── contracts.py              # Data models
├── docker-compose.yml        # Services
├── docs/                     # All documentation
├── PRPs/                     # Product requirements
├── config/                   # Configuration files
├── examples/                 # Example requests
├── scripts/                  # Utility scripts
└── tests/                    # Test suite (planned)
```

## Troubleshooting

### Common Issues

#### WordPress Connection Failed
- Ensure permalinks are set to `/%category%/%postname%/`
- Verify JSON Basic Authentication plugin is activated
- Check username/password in `.env.local`
- Restart API container: `make restart`

#### Article Generation Failed
- Verify AI API keys in `.env.local`
- Check if keys are valid and have credits
- Use `docker logs blog-api` to see detailed errors

#### Container Issues
```bash
# Check container status
docker ps

# View logs
docker logs blog-api --tail 50

# Restart all services
docker compose down && docker compose up -d
```

## Support

For issues or questions:
1. Check [Documentation](docs/index.md)
2. Review [Quick Start Guide](docs/setup/QUICKSTART.md)
3. View [Progress Tracking](PROGRESS.md)
4. Check [Task Management](TASK.md)
5. View logs: `docker compose logs -f`
6. API docs: http://localhost:8088/docs

## License

Part of the ServiceDogUS platform. See main repository for license details.
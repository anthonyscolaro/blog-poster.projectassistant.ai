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
**Current Stage**: MVP Foundation (40% Complete)
- ✅ Infrastructure and Docker setup complete
- ✅ WordPress publishing functional
- ✅ API framework and data models ready
- ⚠️ Agent implementations stubbed/mocked
- ❌ LLM integration and vector search pending

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
cp .env.local.example .env.local

# 2. Add your API keys to .env.local
nano .env.local

# 3. Start services
docker compose up -d

# 4. Verify health
curl http://localhost:8088/health
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

The service connects to your WordPress site via:
- **WPGraphQL** for content creation and updates
- **REST API** for media uploads
- **Authentication** via Application Passwords or JWT

Ensure your WordPress site has:
1. WPGraphQL plugin installed and activated
2. Application Passwords enabled (or JWT authentication)
3. Proper user permissions for content creation

## Usage

### Generate an Article

```bash
curl -X POST http://localhost:8088/agent/run \
  -H "Content-Type: application/json" \
  -d @topic-input.json
```

### Check SEO Compliance

```bash
curl -X POST http://localhost:8088/seo/lint \
  -H "Content-Type: application/json" \
  -d '{"title": "Your Title", "meta_desc": "Your description"}'
```

### Publish to WordPress

```bash
curl -X POST http://localhost:8088/publish/wp \
  -H "Content-Type: application/json" \
  -d @article.json
```

## Agents

### 1. Competitor Monitoring Agent (⚠️ Planned)
- Will scrape competitor blogs and social media
- Uses Jina AI for content extraction
- Tracks new content and updates
- **Status**: Not yet implemented

### 2. Topic Analysis Agent (⚠️ Planned)
- Analyzes trending topics
- Identifies content gaps
- Scores topics by SEO potential
- **Status**: Not yet implemented

### 3. Article Generation Agent (⚠️ Stubbed)
- Uses Claude 3.5 Sonnet or GPT-4
- Generates SEO-optimized content
- Ensures factual accuracy
- **Status**: Returns mock data, LLM integration pending

### 4. Legal Fact Checker Agent (⚠️ Stubbed)
- Verifies all legal claims
- Ensures ADA compliance accuracy
- Blocks misleading content
- **Status**: Returns hardcoded "verified"

### 5. WordPress Publishing Agent (✅ Functional)
- Publishes via WPGraphQL
- Handles media uploads
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

## Support

For issues or questions:
1. Check [Documentation](docs/index.md)
2. Review [Quick Start Guide](docs/setup/QUICKSTART.md)
3. View logs: `docker compose logs -f`
4. API docs: http://localhost:8088/docs

## License

Part of the ServiceDogUS platform. See main repository for license details.
# Blog Poster - Multi-Agent AI Content Generation System

A sophisticated **Multi-Agent AI Content Generation System** for automated SEO-optimized blog content creation and publishing. The system orchestrates five specialized AI agents to produce high-quality, legally accurate content about service dogs and ADA compliance.

## 🎯 Overview

Blog Poster is an enterprise-grade content automation platform that combines:
- **AI-Powered Content Generation** - Using Claude 3.5 Sonnet and GPT-4
- **Vector Search Integration** - Semantic search with Qdrant for intelligent content management
- **Automated SEO Optimization** - Built-in scoring and optimization
- **Legal Fact Checking** - ADA compliance verification with proper citations
- **WordPress Publishing** - Direct integration via WPGraphQL
- **Cost Management** - Per-article and monthly budget tracking

### ✅ Implementation Status
**Current Stage**: Production Ready with Vector Search
- ✅ Multi-agent orchestration pipeline complete
- ✅ Vector search integration (Qdrant) fully functional
- ✅ WordPress publishing with SEO metadata
- ✅ Article generation with Claude 3.5 Sonnet
- ✅ Competitor monitoring with Jina AI
- ✅ Topic analysis and SEO optimization
- ✅ Legal fact checker with ADA verification
- ✅ Cost tracking and budget management
- ✅ Docker containerization complete
- ✅ Comprehensive API endpoints

## 🏗️ Architecture

### Multi-Agent Pipeline
```
Competitor Monitoring → Topic Analysis → Article Generation → Legal Fact Checking → WordPress Publishing
```

Each agent is specialized and works sequentially to ensure high-quality content production.

### System Components
- **Orchestration Manager** - Coordinates all agents and manages pipeline execution
- **Vector Search (Qdrant)** - Semantic search, duplicate detection, internal linking
- **LLM Integration** - Claude 3.5 Sonnet (primary), GPT-4 Turbo (fallback)
- **WordPress Publisher** - WPGraphQL and REST API integration
- **Cost Tracker** - Real-time API usage and cost monitoring

### Port Allocation

| Service | Port | Description |
|---------|------|-------------|
| API | 8088 | FastAPI REST endpoints |
| Qdrant | 6333 | Vector database for semantic search |
| PostgreSQL | 5433 | pgvector for embeddings |
| Redis | 6384 | Job queue and caching |

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

# 6. Run tests to verify installation
./run_tests.py

# 7. Access the dashboard
open http://localhost:8088

# 8. Run complete workflow
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

## 🤖 Multi-Agent System

### Complete Orchestration Pipeline (✅ Fully Integrated)
The system orchestrates 5 specialized agents in sequence to create high-quality, SEO-optimized content:

```bash
# Run the complete pipeline
curl -X POST http://localhost:8088/pipeline/run \
  -H "Content-Type: application/json" \
  -d '{
    "primary_keyword": "autism service dog",
    "min_words": 1500,
    "perform_fact_checking": true,
    "auto_publish": true
  }'
```

### 1. Competitor Monitoring Agent (✅ Implemented)
- Scrapes competitor blogs with Jina AI
- Falls back to Bright Data for social media
- Tracks trending topics and content gaps
- Identifies opportunities from competitor analysis
- **Status**: Fully functional

### 2. Topic Analysis Agent (✅ Implemented)
- **Keyword Research**: Analyzes search volume, difficulty, and trends
- **Content Gap Detection**: Identifies missing topics vs competitors
- **SEO Opportunity Scoring**: Prioritizes topics by potential (0-100 score)
- **Smart Recommendations**: Generates titles, outlines, and word counts
- **Market Insights**: Provides trending topics and high-opportunity keywords
- **Content Type Selection**: Determines best format (guide, how-to, FAQ, etc.)
- **Status**: Fully integrated with pipeline

#### Topic Analysis Endpoints:
```bash
# Full topic analysis
curl -X POST http://localhost:8088/topics/analyze \
  -d "keywords=['service dog training', 'ADA requirements']"

# Quick recommendations
curl http://localhost:8088/topics/recommendations?count=5&focus=PTSD

# Content gap identification
curl http://localhost:8088/topics/gaps
```

### 3. Article Generation Agent (✅ Implemented)
- Uses Claude 3.5 Sonnet (primary) with fallback to GPT-4 Turbo
- Generates SEO-optimized content with keyword integration
- Multi-step generation: outline → content → optimization
- Tracks costs per article ($0.03-0.07 average)
- Caches articles locally with JSON metadata
- **Status**: Fully functional with valid API keys

### 4. Legal Fact Checker Agent (✅ Implemented)
- **ADA Compliance Verification**: 10+ core ADA regulations database
- **Misconception Detection**: Identifies and corrects 10+ common myths
- **Citation Validation**: Verifies legal citations (28 CFR patterns)
- **Disclaimer Generation**: Adds required legal/medical disclaimers
- **Correction System**: Automatically fixes incorrect claims with sources
- **Confidence Scoring**: Rates accuracy of legal claims (0-100%)
- **Research Integration**: Uses 25+ scraped ADA documents
- **Status**: Fully functional with comprehensive fact database

### 5. WordPress Publishing Agent (✅ Functional)
- Publishes via REST API with Basic Auth or App Passwords
- Creates draft or published posts with full metadata
- Sets SEO metadata (title, description, slug)
- Manages categories and tags
- Returns edit links for immediate access
- **Status**: Fully implemented and working

## 📚 Documentation

### Core Documentation
- **[System Documentation](docs/SYSTEM_DOCUMENTATION.md)** - Complete system overview and architecture
- **[API Reference](docs/API_REFERENCE.md)** - Detailed API endpoint documentation
- **[Deployment Guide](docs/DEPLOYMENT_GUIDE.md)** - Production deployment instructions

### Agent Documentation
- [Multi-Agent Architecture](docs/SYSTEM_DOCUMENTATION.md#-multi-agent-system)
- [Vector Search Integration](docs/SYSTEM_DOCUMENTATION.md#-vector-search-integration)
- [Cost Management](docs/SYSTEM_DOCUMENTATION.md#-cost-management)

### Quick Links
- [Environment Configuration](docs/SYSTEM_DOCUMENTATION.md#-environment-configuration)
- [Docker Services](docs/SYSTEM_DOCUMENTATION.md#-docker-services)
- [Security Considerations](docs/SYSTEM_DOCUMENTATION.md#-security-considerations)
- [Performance Optimization](docs/SYSTEM_DOCUMENTATION.md#-performance-optimization)

## 🔍 Vector Search Features

**✅ Successfully Integrated with Qdrant!**

### Capabilities
- **Document Indexing** - Automatic chunking and embedding of articles
- **Semantic Search** - Find similar content using AI embeddings (OpenAI Ada-002)
- **Duplicate Detection** - Prevent redundant content (90% similarity threshold)
- **Internal Linking** - Intelligent link recommendations based on content similarity
- **Collection Management** - Separate collections for articles, competitors, and research

### Technical Details
- Vector Database: Qdrant (port 6333)
- Embedding Model: text-embedding-ada-002 (1536 dimensions)
- Distance Metric: Cosine similarity
- Chunking: 500 chars with 100 char overlap

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
├── orchestration_manager.py # Pipeline orchestration
├── vector_search.py        # Qdrant integration
├── wordpress_publisher.py  # WordPress publishing
├── agents/                 # Multi-agent implementations
│   ├── competitor_monitoring_agent.py
│   ├── topic_analysis_agent.py
│   ├── article_generation_agent.py
│   └── legal_fact_checker_agent.py
├── docker-compose.yml      # Service definitions
├── requirements.txt        # Python dependencies
├── .env.local             # Configuration (git-ignored)
├── .env.example           # Configuration template
├── docs/                  # Documentation
│   ├── SYSTEM_DOCUMENTATION.md
│   ├── API_REFERENCE.md
│   └── DEPLOYMENT_GUIDE.md
└── data/                  # Persistent data (git-ignored)
    ├── articles/          # Generated articles cache
    └── logs/              # Application logs
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

## 🧪 Testing

The project includes a comprehensive test suite with 50+ test cases covering all major components.

### Running Tests

```bash
# Run all tests with coverage report
./run_tests.py

# Run tests with pytest directly
pytest tests/ -v

# Run with coverage metrics
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_api_endpoints.py -v

# Run tests in Docker
make test

# Run only unit tests (fast)
pytest -m "not integration" -v

# Run integration tests
pytest -m integration -v
```

### Test Coverage

The test suite covers:
- **API Endpoints** - All REST endpoints with success/error cases
- **Vector Search** - Qdrant operations, embeddings, semantic search
- **Docker Services** - Container health checks and connectivity
- **Agents** - Article generation, legal fact checking, WordPress publishing
- **Configuration** - Profile CRUD operations and validation
- **Pipeline** - End-to-end workflow testing

### Test Structure

```
tests/
├── __init__.py
├── test_api_endpoints.py      # API endpoint tests
├── test_vector_search.py      # Vector database tests
├── test_docker_services.py    # Container health checks
├── test_article_generation.py # Article agent tests
├── test_legal_fact_checker.py # Legal verification tests
└── test_wordpress_publisher.py # WordPress integration tests

conftest.py                     # Shared fixtures and configuration
run_tests.py                   # Test runner with coverage reporting
```

### Continuous Integration

Tests automatically run on:
- Pull request creation
- Commits to main branch
- Manual workflow dispatch

See `.github/workflows/tests.yml` for CI configuration.

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
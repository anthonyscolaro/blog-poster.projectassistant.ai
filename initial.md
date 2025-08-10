## FEATURE: Blog-Poster - Automated SEO Content Generation Service

### Core System
- **Multi-agent orchestration system** for automated blog content generation and publishing
- **FastAPI REST API** serving as the main orchestration layer with health checks and monitoring
- **WordPress integration** via WPGraphQL and REST API for content publishing
- **Docker-based microservices** architecture with Redis, Qdrant, and PostgreSQL+pgvector

### Agents
1. **Competitor Monitoring Agent** - Scrapes competitor content using Jina AI for insights
2. **Topic Analysis Agent** - Identifies trending topics and content gaps with SEO scoring
3. **Article Generation Agent** - Uses Claude 3.5 Sonnet or GPT-4 for content creation
4. **Legal Fact Checker Agent** - Verifies claims and ensures ADA compliance accuracy
5. **WordPress Publishing Agent** - Handles content publishing with media uploads and SEO metadata

### Key Technologies
- **FastAPI** for API endpoints and agent orchestration
- **Anthropic Claude 3.5 Sonnet** as primary LLM (with OpenAI fallback)
- **Qdrant** for vector search and semantic similarity
- **PostgreSQL with pgvector** for embeddings storage
- **Redis** for job queuing and caching
- **WPGraphQL** for WordPress content management

## ARCHITECTURE:

### Service Ports
| Service | Port | Description |
|---------|------|-------------|
| API | 8088 | FastAPI REST endpoints |
| Qdrant | 6333 | Vector database |
| PostgreSQL | 5433 | pgvector embeddings |
| Redis | 6384 | Queue and cache |

### Data Flow
1. Competitor content monitoring → Topic analysis
2. Topic selection → Article generation with SEO optimization
3. Fact checking and verification → WordPress publishing
4. Automatic internal linking and media generation

## CURRENT IMPLEMENTATION:

- `app.py` - Main FastAPI application with `/agent/run`, `/seo/lint`, `/publish/wp` endpoints
- `orchestrator.py` - Workflow orchestration with state management and retry logic
- `wordpress_agent.py` - WordPress publishing with JWT/Basic auth support
- `contracts.py` - Pydantic models for strong typing and validation
- `docker-compose.yml` - Complete containerized stack

## OTHER CONSIDERATIONS:

- **Environment configuration** via `.env.local` with API keys and WordPress credentials
- **SEO optimization** with meta titles, descriptions, canonical URLs, and schema markup
- **Cost management** with per-article and monthly budget caps
- **Fact-checking** for legal claims and ADA compliance accuracy
- **Media handling** with Base64 image uploads and alt text generation

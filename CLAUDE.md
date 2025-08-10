### 🔄 Blog-Poster Project Context
- **Multi-Agent Architecture** - The blog-poster system uses 5 specialized agents working in sequence:
  1. **Competitor Monitoring Agent** - Tracks industry content using Jina AI
  2. **Topic Analysis Agent** - Identifies SEO opportunities and content gaps
  3. **Article Generation Agent** - Creates SEO-optimized content with Claude 3.5 Sonnet
  4. **Legal Fact Checker Agent** - Verifies ADA compliance claims and legal accuracy
  5. **WordPress Publishing Agent** - Handles content deployment via WPGraphQL
  
- **Docker-First Development** - All services run in Docker containers:
  - API service on port 8088 (FastAPI)
  - Qdrant vector DB on port 6333
  - PostgreSQL with pgvector on port 5433
  - Redis queue on port 6384
  
- **SEO Excellence Standards**:
  - Title tags under 60 characters
  - Meta descriptions under 155 characters
  - Minimum 1500 words per article
  - Internal linking to related content
  - Schema.org structured data
  - Canonical URL management
  
- **WordPress Integration** - Two authentication methods supported:
  - JWT tokens via WPGraphQL JWT Authentication
  - Application Passwords for REST API
  - SSL verification can be disabled for local development
  
- **Service Dog & ADA Focus** - All content must:
  - Be factually accurate about ADA requirements
  - Include proper legal citations (28 CFR §36.302, etc.)
  - Distinguish between service dogs and ESAs
  - Include appropriate disclaimers
  
- **Cost Management**:
  - Track per-article costs (LLM API usage)
  - Enforce monthly budget limits
  - Alert at 80% threshold
  - Stop generation at budget cap
  
- **Testing Requirements**:
  - Run `docker compose up` and verify all services start
  - Test endpoints: `/health`, `/seo/lint`, `/publish/wp`
  - Validate SEO compliance with test payloads
  - Ensure WordPress connection works
  
- **Current Implementation Status**:
  - ✅ FastAPI orchestration framework
  - ✅ WordPress publishing agent
  - ✅ Docker compose stack
  - ✅ Pydantic data models
  - ⚠️ Agent implementations (stubbed)
  - ⚠️ LLM integration (mocked)
  - ❌ Unit tests
  - ❌ Production deployment

### 💻 Development Guidelines

- **API-First Approach** - All functionality exposed through FastAPI endpoints:
  - `/agent/run` - Trigger full article generation workflow
  - `/seo/lint` - Validate SEO compliance
  - `/publish/wp` - Publish to WordPress
  - `/health` - Service health check
  
- **LLM Model Configuration**:
  - Primary: Claude 3.5 Sonnet (`claude-3-5-sonnet-20241022`)
  - Fallback: GPT-4 Turbo (`gpt-4-turbo-preview`)
  - Set via `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` environment variables
  
- **Environment Variables** (`.env.local`):
  ```bash
  # Required
  ANTHROPIC_API_KEY=sk-ant-...
  JINA_API_KEY=jina_...
  WORDPRESS_URL=https://wp.servicedogus.test
  WP_USERNAME=admin
  WP_APP_PASSWORD=xxxx xxxx xxxx xxxx
  
  # Optional
  WP_VERIFY_SSL=false  # For local development
  MAX_COST_PER_ARTICLE=0.50
  MAX_MONTHLY_COST=100.00
  ```
  
- **Testing Workflow**:
  1. Start services: `docker compose up -d`
  2. Check health: `curl http://localhost:8088/health`
  3. Test SEO: `curl -X POST http://localhost:8088/seo/lint -d @test-seo.json`
  4. Test publish: `curl -X POST http://localhost:8088/publish/wp -d @test-input.json`
  
- **Common Issues & Solutions**:
  - **Qdrant unhealthy**: Relax health check, use `service_started` condition
  - **WordPress connection failed**: Check SSL settings, use `host.docker.internal`
  - **Port conflicts**: Ensure ports 8088, 6333, 5433, 6384 are free

### 🧱 Code Structure & Modularity
- **Never create a file longer than 500 lines of code.** If a file approaches this limit, refactor by splitting it into modules or helper files.
- **When creating AI prompts do not hardcode examples but make everything dynamic or based off the context of what the prompt is for**
- **Always refer to the specific Phase document you are on** - If you are on phase 1, use phase-1.md, if you are on phase 2, use phase-2.md, if you are on phase 3, use phase-3.md
- **Agents should be designed as intelligent human beings** by giving them decision making, ability to do detailed research using LocalDocs and Jina, and not just your basic prompts that generate absolute shit. This is absolutely vital.
- **Organize code into clearly separated modules**, grouped by feature or responsibility.
  For agents this looks like:
    - `agent.py` - Main agent definition and execution logic 
    - `tools.py` - Tool functions used by the agent 
    - `prompts.py` - System prompts
- **Use clear, consistent imports** (prefer relative imports within packages).
- **Use clear, consistent imports** (prefer relative imports within packages).
- **Use python_dotenv and load_env()** for environment variables.
- **Follow Port Allocation Strategy** - See `PORT_ALLOCATION_STRATEGY.md` for team-wide port assignments. Also reference `/Users/anthonyscolaro/apps/localdocs/data/port-registry.md` for active port assignments across all team projects.

### 🧪 Testing & Reliability
- **Always create Pytest unit tests for new features** (functions, classes, routes, etc).
- **After updating any logic**, check whether existing unit tests need to be updated. If so, do it.
- **Tests should live in a `/tests` folder** mirroring the main app structure.
  - Include at least:
    - 1 test for expected use
    - 1 edge case
    - 1 failure case
- **Docker Testing** - Everything must be confirmed to work perfectly through Docker. Use Docker for all testing so the server runs and can be tested end-to-end.

### ✅ Task Completion
- **Mark completed tasks in `TASK.md`** immediately after finishing them.
- Add new sub-tasks or TODOs discovered during development to `TASK.md` under a "Discovered During Work" section.

### 📎 Style & Conventions
- **Use Python** as the primary language.
- **Follow PEP8**, use type hints, and format with `black`.
- **Use `pydantic` for data validation**.
- Use `FastAPI` for APIs and `SQLAlchemy` or `SQLModel` for ORM if applicable.
- Write **docstrings for every function** using the Google style:
  ```python
  def example():
      """
      Brief summary.

      Args:
          param1 (type): Description.

      Returns:
          type: Description.
      """
  ```

### 📚 Documentation & Explainability
- **Update `README.md`** when new features are added, dependencies change, or setup steps are modified.
- **Comment non-obvious code** and ensure everything is understandable to a mid-level developer.
- When writing complex logic, **add an inline `# Reason:` comment** explaining the why, not just the what.

### 🧠 AI Behavior Rules
- **Never assume missing context. Ask questions if uncertain.**
- **Never hallucinate libraries or functions** – only use known, verified Python packages.
- **Always confirm file paths and module names** exist before referencing them in code or tests.
- **Never delete or overwrite existing code** unless explicitly instructed to or if part of a task from `TASK.md`.

### 🎯 Enhanced Context Engineering Rules
- **Hybrid Documentation Approach** - Use both Jina research and LocalDocs collections strategically based on project phase and requirements.
- **Team Knowledge Sharing** - All LocalDocs collections should be exportable and shareable across team members and projects.
- **Dynamic Documentation Updates** - Keep LocalDocs collections current by regularly updating sources and re-exporting collections.
- **Cross-Project Efficiency** - Leverage LocalDocs collections from previous projects to accelerate development on similar features.
- **Research Quality Validation** - If a Jina scrape fails or returns minimal content, scrape again until you get meaningful content.
- **Multi-Agent Coordination** - When using multiple agents for research, ensure coordinated output that contributes to unified documentation structure.

### 🚀 Deployment Excellence
- **Infrastructure as Code** - All deployment processes should be automated and reproducible through scripts and configuration files.
- **Complete Deployment Validation** - Test all endpoints, health checks, and user flows after deployment completion.
- **Documentation-Driven Deployment** - Use the established collections in `docs/deployment-workflows/` and `docs/infrastructure-guides/` for consistent deployment approaches.

Do what has been asked; nothing more, nothing less.
NEVER create files unless they're absolutely necessary for achieving your goal.
ALWAYS prefer editing an existing file to creating a new one.
NEVER proactively create documentation files (*.md) or README files. Only create documentation files if explicitly requested by the User.
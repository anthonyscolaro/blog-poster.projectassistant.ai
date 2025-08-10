# Blog-Poster Documentation

Welcome to the Blog-Poster documentation. This automated SEO content generation service helps create and publish high-quality articles to WordPress.

## 📚 Documentation Structure

### Getting Started
- [Quick Start Guide](setup/QUICKSTART.md) - Get running in 5 minutes
- [Full Setup Guide](setup/SETUP.md) - Detailed installation and configuration
- [README](../README.md) - Project overview and status

### Development Guides
- [Research Guide](guides/RESEARCH_GUIDE.md) - How to research and gather documentation
- [LocalDocs Guide](guides/LOCALDOCS_GUIDE.md) - Documentation management system
- [Workflow Management](guides/WORKFLOW_MANAGEMENT.md) - Development workflows and best practices

### API & Technical
- [API Documentation](api/blog-poster.md) - Endpoint details and examples
- [AI Prompt Template](api/sonnet-3.5-prompt.txt) - Claude 3.5 Sonnet system prompt

### Deployment & Infrastructure
- [Infrastructure Setup](deployment/INFRASTRUCTURE_SETUP.md) - Production deployment guide
- [Port Allocation Strategy](deployment/PORT_ALLOCATION_STRATEGY.md) - Port management across services
- [Portainer Deployment](deployment/PORTAINER_DEPLOYMENT.md) - Container management with Portainer

### Project Management
- [Product Requirements](../PRPs/blog-poster.prp.md) - Full PRP with validation scripts
- [Progress Tracking](../PROGRESS.md) - Current implementation status
- [Claude Instructions](../CLAUDE.md) - AI assistant configuration

## 🏗️ Project Structure

```
blog-poster/
├── app.py                    # Main FastAPI application
├── orchestrator.py           # Workflow orchestration
├── wordpress_agent.py        # WordPress publishing agent
├── contracts.py              # Pydantic data models
├── docker-compose.yml        # Service orchestration
│
├── docs/                     # Documentation
│   ├── setup/               # Installation & quickstart
│   ├── guides/              # Development guides
│   ├── api/                 # API documentation
│   └── deployment/          # Infrastructure guides
│
├── PRPs/                    # Product Requirement Prompts
├── research/                # Jina research data
├── config/                  # Configuration files
├── examples/                # Example requests/responses
├── scripts/                 # Utility scripts
└── tests/                   # Test suite (to be implemented)
```

## 🚀 Quick Links

- **API Endpoint**: http://localhost:8088/docs
- **Health Check**: http://localhost:8088/health
- **Qdrant Dashboard**: http://localhost:6333/dashboard

## 📊 Implementation Status

Current Stage: **MVP Foundation (40% Complete)**

- ✅ Infrastructure and Docker setup
- ✅ WordPress publishing functional
- ✅ API framework and data models
- ⚠️ Agent implementations (stubbed)
- ❌ LLM integration pending
- ❌ Test suite needed

See [PROGRESS.md](../PROGRESS.md) for detailed status.

## 🆘 Getting Help

1. Check the [Quick Start Guide](setup/QUICKSTART.md) for common issues
2. Review [Setup Guide](setup/SETUP.md) for detailed configuration
3. See API examples in [examples/](../examples/) directory
4. Check logs: `docker compose logs -f`

## 🔗 External Resources

- [WPGraphQL Documentation](https://www.wpgraphql.com/docs/)
- [Anthropic Claude API](https://docs.anthropic.com/)
- [Jina AI Documentation](https://docs.jina.ai/)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
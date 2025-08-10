# Hybrid Research Workflow Guide

## Overview

This template uses a **hybrid approach** combining the proven Jina scraping methodology with LocalDocs for organized, reusable documentation management.

## When to Use Each Approach

### Use Jina Research (research/ directory) for:
- **New project PRP generation** - Comprehensive page-by-page analysis
- **Technology deep-dives** - Understanding new frameworks or APIs in detail  
- **Implementation-specific research** - Getting granular details for complex integrations
- **Documentation exploration** - When you need to understand the full scope of a technology

### Use LocalDocs (docs/ directory) for:
- **Reusable API references** - Endpoints and schemas you'll reference repeatedly
- **Deployment workflow documentation** - Infrastructure setup and deployment processes
- **Cross-project knowledge sharing** - Documentation that benefits multiple projects
- **Team collaboration** - Shared collections that standardize team knowledge

## Workflow Integration

### 1. Start with Project Assessment

**For New/Unknown Technologies:**
```bash
# Begin with comprehensive Jina research
curl "https://r.jina.ai/https://docs.newtech.com/getting-started/" \
  -H "Authorization: Bearer $JINA_TOKEN" > research/newtech/page1/getting-started.md

curl "https://r.jina.ai/https://docs.newtech.com/api-reference/" \
  -H "Authorization: Bearer $JINA_TOKEN" > research/newtech/page2/api-reference.md
```

**For Established Technologies:**
```bash
# Jump straight to LocalDocs for organized collections
python /Users/anthonyscolaro/apps/localdocs/bin/localdocs add \
  https://docs.establishedtech.com/api \
  https://docs.establishedtech.com/deployment
```

### 2. Jina Research Workflow (research/ directory)

#### Comprehensive Documentation Scraping
```bash
# Set up directory structure
mkdir -p research/[technology]/page{1..8}

# Scrape key documentation pages
curl "https://r.jina.ai/https://docs.api.com/guide/" \
  -H "Authorization: Bearer $JINA_TOKEN" > research/api/page1/guide.md

curl "https://r.jina.ai/https://docs.api.com/reference/" \
  -H "Authorization: Bearer $JINA_TOKEN" > research/api/page2/reference.md

curl "https://r.jina.ai/https://docs.api.com/authentication/" \
  -H "Authorization: Bearer $JINA_TOKEN" > research/api/page3/auth.md
```

#### Quality Assurance
```bash
# Check scraped content quality
ls -la research/api/page*/*.md

# If scraping failed or content is minimal, retry
curl "https://r.jina.ai/https://docs.api.com/guide/" \
  -H "Authorization: Bearer $JINA_TOKEN" > research/api/page1/guide.md
```

#### Create Technology Summary
```bash
# Compile findings into llm.txt for AI context
cat > research/api/llm.txt << 'EOF'
# API Technology Summary

## Key Concepts
- REST API with JWT authentication
- Rate limiting: 1000 requests/hour
- Webhooks support for real-time events

## Authentication
- API keys via Authorization header
- JWT tokens for user-specific operations
- OAuth2 for third-party integrations

## Core Endpoints
- GET /users - List users
- POST /users - Create user
- PUT /users/{id} - Update user
- DELETE /users/{id} - Delete user

## Implementation Notes
- Always validate webhook signatures
- Use exponential backoff for rate limits
- Cache API responses when possible
EOF
```

### 3. LocalDocs Workflow (docs/ directory)

#### Collect Key Documentation
```bash
# Add essential API documentation
python /Users/anthonyscolaro/apps/localdocs/bin/localdocs add \
  https://docs.api.com/reference \
  https://docs.api.com/authentication \
  https://docs.api.com/webhooks
```

#### Organize with Meaningful Metadata
```bash
# Set descriptive names, descriptions, and tags
python /Users/anthonyscolaro/apps/localdocs/bin/localdocs set a1b2c3d4 \
  -n "API Reference" \
  -d "Core REST API endpoints and schemas" \
  -t "api,rest,reference"

python /Users/anthonyscolaro/apps/localdocs/bin/localdocs set e5f6g7h8 \
  -n "Authentication Guide" \
  -d "JWT, OAuth2, and API key authentication methods" \
  -t "api,auth,security"

python /Users/anthonyscolaro/apps/localdocs/bin/localdocs set i9j0k1l2 \
  -n "Webhooks Documentation" \
  -d "Real-time event handling via webhooks" \
  -t "api,webhooks,events"
```

#### Export Collections for Team Use
```bash
# Create focused collections
python /Users/anthonyscolaro/apps/localdocs/bin/localdocs export api-integration \
  --format claude \
  --include a1b2c3d4,e5f6g7h8,i9j0k1l2

# Create deployment-specific collection
python /Users/anthonyscolaro/apps/localdocs/bin/localdocs export deployment-workflow \
  --format claude \
  --tags deployment,infrastructure
```

### 4. Using Documentation in Development

#### Reference Jina Research
```markdown
# In your PRP or implementation notes
Based on comprehensive research in research/api/llm.txt, the API supports:
- JWT authentication (see research/api/page3/auth.md)
- Rate limiting of 1000 req/hour (research/api/page2/reference.md)
- Webhook validation patterns (research/api/page4/webhooks.md)
```

#### Reference LocalDocs Collections
```python
# In your code comments and documentation
"""
User authentication implementation.

See @docs/api-integration/e5f6g7h8.md for JWT token handling.
See @docs/api-integration/a1b2c3d4.md for endpoint specifications.
"""
```

### 5. Multi-Agent Research Coordination

#### Parallel Jina Research
```bash
# Agent 1: Core API documentation
curl "https://r.jina.ai/https://docs.api.com/core/" \
  -H "Authorization: Bearer $JINA_TOKEN" > research/api/page1/core.md

# Agent 2: Authentication systems  
curl "https://r.jina.ai/https://docs.auth.com/oauth/" \
  -H "Authorization: Bearer $JINA_TOKEN" > research/auth/page1/oauth.md

# Agent 3: Deployment infrastructure
curl "https://r.jina.ai/https://docs.deploy.com/containers/" \
  -H "Authorization: Bearer $JINA_TOKEN" > research/deploy/page1/containers.md
```

#### LocalDocs Organization Agent
```bash
# Agent 4: Consolidate research into LocalDocs
python /Users/anthonyscolaro/apps/localdocs/bin/localdocs add \
  https://docs.api.com/core \
  https://docs.auth.com/oauth \
  https://docs.deploy.com/containers

# Export organized collections
python /Users/anthonyscolaro/apps/localdocs/bin/localdocs export project-foundation --format claude
```

## Best Practices

### Research Quality
- **Retry failed scrapes** - If Jina returns minimal content, scrape again
- **Verify completeness** - Ensure all key documentation areas are covered
- **Cross-reference sources** - Validate information across multiple pages

### Organization Standards
- **Consistent tagging** - Use standardized tags (api, auth, deployment, etc.)
- **Descriptive metadata** - Names and descriptions should be clear and searchable
- **Logical collections** - Group related documentation for specific use cases

### Team Collaboration
- **Shared conventions** - Establish team standards for tags and naming
- **Regular updates** - Keep LocalDocs collections current with source changes
- **Export formats** - Use Claude format for development, JSON for data exchange

### Documentation Integration
- **Context-aware references** - Choose Jina research for deep context, LocalDocs for quick reference
- **Update workflows** - Establish processes for keeping documentation current
- **Cross-project leverage** - Reuse LocalDocs collections across similar projects

## Migration from Pure Jina Approach

### Step 1: Preserve Existing Research
```bash
# Keep existing research/ directory structure
# No changes needed to current Jina workflow
```

### Step 2: Identify Reusable Content
```bash
# Extract key URLs from existing research
grep -r "https://" research/ | grep -E "(docs\.|api\.|guide\.)" > urls-for-localdocs.txt
```

### Step 3: Add LocalDocs Layer
```bash
# Add reusable documentation to LocalDocs
python /Users/anthonyscolaro/apps/localdocs/bin/localdocs add -f urls-for-localdocs.txt

# Organize and export
python /Users/anthonyscolaro/apps/localdocs/bin/localdocs export legacy-apis --format claude
```

### Step 4: Hybrid Development
```bash
# New projects: Start with LocalDocs check
python /Users/anthonyscolaro/apps/localdocs/bin/localdocs list --tags api

# If not found: Use Jina for comprehensive research
# If found: Leverage existing collections and extend as needed
```

This hybrid approach preserves the depth and comprehensiveness of Jina research while adding the organizational benefits and team collaboration features of LocalDocs.
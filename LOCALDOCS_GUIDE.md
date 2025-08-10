# LocalDocs Integration Guide

## Overview

LocalDocs transforms scattered API documentation into organized, reusable collections that integrate seamlessly with Claude Code through @file references.

## Quick Start

### 1. Basic LocalDocs Commands

```bash
# Add documentation sources
python /Users/anthonyscolaro/apps/localdocs/bin/localdocs add https://docs.example.com/api

# View your collection
python /Users/anthonyscolaro/apps/localdocs/bin/localdocs list

# Organize with metadata
python /Users/anthonyscolaro/apps/localdocs/bin/localdocs set a1b2c3d4 \
  -n "Example API" \
  -d "REST API reference documentation" \
  -t "api,rest,example"

# Export collection for Claude
python /Users/anthonyscolaro/apps/localdocs/bin/localdocs export api-reference --format claude
```

### 2. Project Integration

```bash
# Initialize LocalDocs in your project
touch localdocs.config.json

# Create documentation directories
mkdir -p docs/{api-collections,deployment-workflows,infrastructure-guides}
```

## Collection Management

### Adding Documentation

#### Single URL
```bash
python /Users/anthonyscolaro/apps/localdocs/bin/localdocs add https://docs.api.com/reference
```

#### Multiple URLs
```bash
python /Users/anthonyscolaro/apps/localdocs/bin/localdocs add \
  https://docs.api.com/authentication \
  https://docs.api.com/webhooks \
  https://docs.api.com/rate-limits
```

#### From File
```bash
# Create URL list
cat > api-urls.txt << 'EOF'
https://docs.api.com/getting-started
https://docs.api.com/api-reference  
https://docs.api.com/authentication
https://docs.api.com/webhooks
EOF

# Add from file
python /Users/anthonyscolaro/apps/localdocs/bin/localdocs add -f api-urls.txt
```

#### Interactive Mode
```bash
# Enter interactive URL collection
python /Users/anthonyscolaro/apps/localdocs/bin/localdocs add
# Then paste URLs one per line, empty line to finish
```

### Organizing Collections

#### View Current Collection
```bash
# List all documents
python /Users/anthonyscolaro/apps/localdocs/bin/localdocs list

# Filter by tags
python /Users/anthonyscolaro/apps/localdocs/bin/localdocs list --tags api,authentication
```

#### Set Meaningful Metadata
```bash
# Organize each document with clear metadata
python /Users/anthonyscolaro/apps/localdocs/bin/localdocs set a1b2c3d4 \
  -n "API Authentication" \
  -d "JWT, OAuth2, and API key authentication methods" \
  -t "api,auth,security,jwt"

python /Users/anthonyscolaro/apps/localdocs/bin/localdocs set e5f6g7h8 \
  -n "Webhook Integration" \
  -d "Real-time event handling and webhook validation" \
  -t "api,webhooks,events,realtime"
```

#### Recommended Tagging Conventions
- **Technology**: `api`, `database`, `frontend`, `backend`
- **Category**: `auth`, `deployment`, `monitoring`, `testing`  
- **Complexity**: `beginner`, `advanced`, `reference`
- **Project Phase**: `setup`, `development`, `production`

### Exporting Collections

#### Claude Format (Recommended)
```bash
# Export with @file references for Claude integration
python /Users/anthonyscolaro/apps/localdocs/bin/localdocs export api-docs --format claude

# Result: api-docs/claude-refs.md with content like:
# See @a1b2c3d4.md for API authentication methods.
# See @e5f6g7h8.md for webhook integration guide.
```

#### Selective Exports
```bash
# Export specific documents only
python /Users/anthonyscolaro/apps/localdocs/bin/localdocs export auth-only \
  --format claude \
  --include a1b2c3d4,f9g0h1i2

# Export by tags
python /Users/anthonyscolaro/apps/localdocs/bin/localdocs export deployment-docs \
  --format claude \
  --tags deployment,infrastructure
```

#### Other Export Formats
```bash
# Table of contents format
python /Users/anthonyscolaro/apps/localdocs/bin/localdocs export project-docs --format toc

# JSON format for programmatic use
python /Users/anthonyscolaro/apps/localdocs/bin/localdocs export data-backup --format json

# Soft links (no file copying, absolute paths)
python /Users/anthonyscolaro/apps/localdocs/bin/localdocs export quick-refs --soft-links
```

## Advanced Usage

### Interactive Document Manager

```bash
# Launch visual document manager
python /Users/anthonyscolaro/apps/localdocs/bin/localdocs manage
```

**Interactive Features:**
- **Navigation**: `j/k` or arrow keys to move
- **Selection**: `Space` to toggle selection
- **Bulk Operations**: `a` to select/deselect all
- **Tag Filtering**: `f` to filter by tags
- **Actions**: `d` delete, `x` export, `u` update, `s` set metadata
- **Exit**: `q` to quit

### Keeping Documentation Current

#### Update Single Document
```bash
# Re-download specific document
python /Users/anthonyscolaro/apps/localdocs/bin/localdocs update a1b2c3d4
```

#### Update All Documents  
```bash
# Refresh entire collection from sources
python /Users/anthonyscolaro/apps/localdocs/bin/localdocs update

# Re-export updated collections
python /Users/anthonyscolaro/apps/localdocs/bin/localdocs export api-docs --format claude
```

#### Automation with Cron
```bash
# Add to crontab for weekly updates
# 0 0 * * 0 cd /path/to/project && python /Users/anthonyscolaro/apps/localdocs/bin/localdocs update && python /Users/anthonyscolaro/apps/localdocs/bin/localdocs export api-docs --format claude
```

## Integration with Development

### Using @file References

#### In Code Comments
```python
"""
User authentication service.

Authentication flow documented at:
See @docs/api-integration/a1b2c3d4.md for JWT implementation details.
See @docs/api-integration/e5f6g7h8.md for OAuth2 setup process.
"""

class AuthService:
    def authenticate_user(self, token: str) -> bool:
        # Implementation based on @docs/api-integration/a1b2c3d4.md
        pass
```

#### In Documentation
```markdown
# User Management API

This service handles user authentication and management.

## Authentication
See @docs/api-integration/auth-guide.md for complete authentication setup.

## Rate Limiting  
See @docs/api-integration/rate-limits.md for current rate limiting policies.

## Webhooks
See @docs/api-integration/webhooks.md for event handling implementation.
```

#### In PRP Generation
```markdown
# Product Requirements Prompt

## API Integration Requirements
Based on documentation analysis:

**Authentication**: See @docs/api-integration/auth-methods.md
- JWT tokens with 1-hour expiration
- Refresh token rotation every 30 days
- API key fallback for service-to-service

**Error Handling**: See @docs/api-integration/error-codes.md  
- Standard HTTP status codes
- Detailed error messages in response body
- Retry logic for 5xx errors
```

### Team Collaboration

#### Sharing Collections
```bash
# Export collection for team sharing
python /Users/anthonyscolaro/apps/localdocs/bin/localdocs export team-apis --format json

# Team member imports
cp team-apis/data.json ~/.localdocs/imported-team-collection.json
python /Users/anthonyscolaro/apps/localdocs/bin/localdocs import team-collection.json
```

#### Standardized Collections
```bash
# Create project template collections
python /Users/anthonyscolaro/apps/localdocs/bin/localdocs export deployment-template \
  --format claude \
  --tags deployment,infrastructure,portainer

python /Users/anthonyscolaro/apps/localdocs/bin/localdocs export api-template \
  --format claude \
  --tags api,authentication,reference
```

## Project Structure Integration

### Recommended Directory Organization
```
your-project/
├── docs/                           # LocalDocs exports
│   ├── api-collections/
│   │   ├── claude-refs.md
│   │   ├── a1b2c3d4.md
│   │   └── localdocs.config.json
│   ├── deployment-workflows/
│   │   ├── claude-refs.md
│   │   └── ...
│   └── infrastructure-guides/
│       ├── claude-refs.md  
│       └── ...
├── research/                       # Jina research (detailed)
│   └── [technology]/
│       ├── page1/scraped.md
│       └── llm.txt
├── memory/                         # Best practices
├── localdocs.config.json          # Project LocalDocs config
└── README.md
```

### Configuration Management

#### Project-Specific Config
```json
{
  "storage_directory": ".",
  "documents": {
    "a1b2c3d4": {
      "url": "https://docs.api.com/auth",
      "name": "API Authentication",
      "description": "JWT and OAuth2 authentication methods",
      "tags": ["api", "auth", "security"]
    }
  }
}
```

#### Global vs Project Collections
```bash
# Global collections (user home)
~/.localdocs/localdocs.config.json

# Project collections (project directory)  
./localdocs.config.json

# LocalDocs automatically uses project config when available
```

## Benefits Summary

### Individual Benefits
- **Eliminate Research Duplication**: Research once, reuse across projects
- **Organized Knowledge**: Clear metadata and tagging system
- **Current Documentation**: Easy updates keep references fresh
- **Claude Integration**: Native @file references for accurate implementation

### Team Benefits  
- **Shared Knowledge Base**: Consistent documentation across team
- **Onboarding Acceleration**: New team members get instant access to organized references
- **Quality Consistency**: Standardized research and documentation practices
- **Cross-Project Leverage**: Reuse collections across similar projects

### Project Benefits
- **Faster Development**: Instant access to organized API references
- **Reduced Errors**: Accurate, current documentation reduces implementation mistakes
- **Better Context**: Rich @file references provide AI assistants with precise context
- **Maintainable Codebase**: Clear documentation trails for future developers

This LocalDocs integration transforms individual research efforts into collaborative, reusable knowledge assets that benefit entire teams and project portfolios.
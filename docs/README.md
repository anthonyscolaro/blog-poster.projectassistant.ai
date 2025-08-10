# Documentation Collections

This directory contains LocalDocs exports with organized, reusable documentation collections for Claude integration.

## Directory Structure

```
docs/
├── api-collections/           # API references and schemas
├── deployment-workflows/      # Infrastructure and deployment guides  
├── infrastructure-guides/     # Server setup and configuration
└── README.md                  # This file
```

## Usage

### Reference in Code
```python
"""
User authentication implementation.

See @docs/api-collections/auth-guide.md for JWT token handling.
See @docs/deployment-workflows/portainer-api.md for deployment process.
"""
```

### Reference in Documentation
```markdown
## API Integration
See @docs/api-collections/claude-refs.md for complete API reference.

## Deployment Process  
See @docs/deployment-workflows/claude-refs.md for infrastructure setup.
```

## Collection Management

### Creating Collections
```bash
# Add documentation to LocalDocs
python /Users/anthonyscolaro/apps/localdocs/bin/localdocs add https://docs.api.com

# Export to docs directory
python /Users/anthonyscolaro/apps/localdocs/bin/localdocs export api-collections --format claude
```

### Updating Collections
```bash
# Update source documentation
python /Users/anthonyscolaro/apps/localdocs/bin/localdocs update

# Re-export collections
python /Users/anthonyscolaro/apps/localdocs/bin/localdocs export api-collections --format claude
```

## Benefits

- **Organized References**: Clean @file paths for Claude integration
- **Team Sharing**: Consistent documentation across projects  
- **Dynamic Updates**: Keep documentation current with sources
- **Cross-Project Reuse**: Export collections to other projects

See [LocalDocs Guide](../LOCALDOCS_GUIDE.md) for complete usage instructions.
# Portainer Deployment Template

This template provides a reusable Portainer API deployment script for containerized applications.

## Quick Start

1. **Copy the template to your project:**
   ```bash
   cp scripts/portainer_deploy_template.py your-project/scripts/portainer_deploy.py
   ```

2. **Configure the template** by editing the `PROJECT_CONFIG` section:
   ```python
   PROJECT_CONFIG = {
       "PROJECT_NAME": "your-project-name",
       "DEFAULT_STACK_NAME": "your-project-dev",
       "ENV_FILE": ".env.portainer",
       "COMPOSE_FILE": "docker-compose.dev.yml",
       "DEFAULT_ENDPOINT_ID": 3,
       "DEFAULT_PORTAINER_URL": "https://portainer.example.com",
       "DOMAINS": {
           "frontend": "FRONTEND_DOMAIN",
           "api": "API_DOMAIN", 
           "database": "PGADMIN_DOMAIN"
       }
   }
   ```

3. **Create environment file** (`.env.portainer`):
   ```bash
   # Portainer Configuration
   PORTAINER_URL=https://portainer.example.com
   PORTAINER_API_KEY=ptr_your_api_key_here
   PORTAINER_WEB_USER=admin
   PORTAINER_WEB_PASS=your_password
   PORTAINER_ENDPOINT_ID=3
   
   # Stack Configuration
   STACK_NAME=your-project-dev
   
   # Domain Configuration (optional)
   FRONTEND_DOMAIN=your-project.example.com
   API_DOMAIN=api-your-project.example.com
   PGADMIN_DOMAIN=db-your-project.example.com
   
   # Add your application environment variables here
   DATABASE_URL=postgresql://user:pass@db:5432/dbname
   JWT_SECRET=your_jwt_secret
   ```

4. **Run the deployment:**
   ```bash
   python scripts/portainer_deploy.py
   ```

## Configuration Guide

### Required Files

- **Environment File** (`.env.portainer`): Contains Portainer credentials and application environment variables
- **Docker Compose File** (`docker-compose.dev.yml`): Your application's compose configuration
- **Deployment Script** (`portainer_deploy.py`): The configured deployment script

### Template Customization

Edit these key sections in the script:

#### 1. Project Configuration
```python
PROJECT_CONFIG = {
    "PROJECT_NAME": "your-app",           # Used for container cleanup
    "DEFAULT_STACK_NAME": "your-app-dev", # Default stack name
    "ENV_FILE": ".env.portainer",         # Environment file path
    "COMPOSE_FILE": "docker-compose.dev.yml", # Compose file path
    "DEFAULT_ENDPOINT_ID": 3,             # Portainer environment ID
    "DEFAULT_PORTAINER_URL": "https://portainer.example.com",
    "DOMAINS": {                          # For success message display
        "frontend": "FRONTEND_DOMAIN",
        "api": "API_DOMAIN",
        "database": "PGADMIN_DOMAIN"
    }
}
```

#### 2. Environment Variables

Required variables in `.env.portainer`:
- `PORTAINER_URL`: Your Portainer instance URL
- `PORTAINER_API_KEY`: API key from Portainer settings
- `PORTAINER_WEB_PASS`: Admin password (fallback)

Optional variables:
- `STACK_NAME`: Override default stack name
- `PORTAINER_ENDPOINT_ID`: Override default environment ID
- Domain variables for success message

## Features

### Intelligent Stack Management
- **Conflict Detection**: Automatically detects existing stacks with same name
- **Container Cleanup**: Removes conflicting containers before deployment
- **Force Delete**: Attempts multiple deletion strategies for stuck stacks
- **Timestamped Fallback**: Uses timestamped stack names if cleanup fails

### Robust Error Handling
- **Authentication Verification**: Tests API key before deployment
- **Environment Validation**: Verifies Portainer environments
- **File Validation**: Checks for required configuration files
- **Detailed Logging**: Provides clear status messages throughout process

### Deployment Process
1. Load and validate configuration files
2. Authenticate with Portainer API
3. List available environments for verification
4. Check for existing stacks and clean up if needed
5. Deploy new stack with environment variables
6. Display success message with application URLs

## Troubleshooting

### Common Issues

**Authentication Failed**
- Verify `PORTAINER_API_KEY` in `.env.portainer`
- Check Portainer URL is accessible
- Ensure API key has appropriate permissions

**Stack Deployment Failed**
- Verify Docker Compose file syntax
- Check environment variables are correctly formatted
- Ensure target environment (endpoint) exists

**Container Cleanup Issues**
- Script will automatically attempt multiple cleanup strategies
- Manual container removal may be needed in rare cases
- Check Portainer UI for stuck resources

### Debug Mode
Add debug logging by modifying the script:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Security Notes

- Store API keys securely in environment files
- Add `.env.portainer` to `.gitignore`
- Use least-privilege API keys when possible
- Regularly rotate API keys

## Example Project Structure

```
your-project/
├── scripts/
│   └── portainer_deploy.py          # Configured template
├── docker-compose.dev.yml           # Your compose file
├── .env.portainer                   # Portainer config (gitignored)
├── .gitignore                       # Include .env.portainer
└── README.md                        # Your project docs
```
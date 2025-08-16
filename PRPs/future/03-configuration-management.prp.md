name: "Configuration Management & Secrets Handling"
description: |

## Purpose
Implement secure, centralized configuration management with proper secrets handling, environment isolation, and runtime configuration updates without code changes.

## Core Principles
1. **Security First**: Never expose secrets, encrypt at rest, audit access
2. **Environment Isolation**: Clear separation between dev/staging/production
3. **Dynamic Configuration**: Update configs without deployment
4. **Single Source of Truth**: Centralized configuration management

---

## Goal
Replace scattered .env files with a secure configuration system using Digital Ocean's secrets management, environment-specific configs, and runtime configuration updates.

## Why
- **Security Risk**: Plain text secrets in .env files
- **No Audit Trail**: Can't track who accessed/changed configs
- **Environment Confusion**: Easy to use wrong environment configs
- **Deployment Friction**: Config changes require redeployment

## What
Implement a hierarchical configuration system with:
- Digital Ocean Secrets Manager for sensitive data
- Environment-specific configuration profiles
- Runtime configuration API
- Encrypted local development secrets
- Configuration validation and schema

### Success Criteria
- [ ] Zero secrets in code or plain text files
- [ ] All configs validated against schema
- [ ] Environment isolation enforced
- [ ] Audit log for all config access
- [ ] Runtime config updates without restart
- [ ] Encrypted secrets at rest
- [ ] Role-based access control
- [ ] Configuration versioning

## All Needed Context

### Current Configuration Chaos
```yaml
Current State:
  Files:
    - .env.local
    - .env.prod
    - .env.example
    - .env.local.example
    - Config profiles in database
    
  Issues:
    - Secrets in plain text
    - No validation
    - Manual sync between environments
    - No version control for secrets
    - Mixed concerns (app config + secrets)
```

### Target Configuration Architecture

```python
# src/config/schema.py
from pydantic import BaseSettings, Field, SecretStr, validator
from typing import Optional, Dict, Any
import os

class DatabaseConfig(BaseSettings):
    """Database configuration"""
    host: str = Field(..., env='DB_HOST')
    port: int = Field(5432, env='DB_PORT')
    name: str = Field(..., env='DB_NAME')
    user: str = Field(..., env='DB_USER')
    password: SecretStr = Field(..., env='DB_PASSWORD')
    pool_size: int = Field(20, env='DB_POOL_SIZE')
    
    @property
    def url(self) -> str:
        return f"postgresql://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.name}"

class RedisConfig(BaseSettings):
    """Redis configuration"""
    host: str = Field('localhost', env='REDIS_HOST')
    port: int = Field(6379, env='REDIS_PORT')
    password: Optional[SecretStr] = Field(None, env='REDIS_PASSWORD')
    db: int = Field(0, env='REDIS_DB')

class APIKeysConfig(BaseSettings):
    """External API keys"""
    anthropic_key: SecretStr = Field(..., env='ANTHROPIC_API_KEY')
    openai_key: Optional[SecretStr] = Field(None, env='OPENAI_API_KEY')
    jina_key: SecretStr = Field(..., env='JINA_API_KEY')
    bright_data_key: Optional[SecretStr] = Field(None, env='BRIGHT_DATA_API_KEY')
    
class WordPressConfig(BaseSettings):
    """WordPress configuration"""
    url: str = Field(..., env='WORDPRESS_URL')
    username: str = Field(..., env='WP_USERNAME')
    password: SecretStr = Field(..., env='WP_PASSWORD')
    auth_method: str = Field('basic', env='WP_AUTH_METHOD')
    verify_ssl: bool = Field(True, env='WP_VERIFY_SSL')

class ContentConfig(BaseSettings):
    """Content generation settings"""
    min_words: int = Field(1500, env='ARTICLE_MIN_WORDS')
    max_words: int = Field(3000, env='ARTICLE_MAX_WORDS')
    max_cost_per_article: float = Field(1.50, env='MAX_COST_PER_ARTICLE')
    max_monthly_cost: float = Field(500.00, env='MAX_MONTHLY_COST')
    
class ApplicationConfig(BaseSettings):
    """Main application configuration"""
    environment: str = Field('development', env='ENVIRONMENT')
    debug: bool = Field(False, env='DEBUG')
    log_level: str = Field('INFO', env='LOG_LEVEL')
    
    # Sub-configurations
    database: DatabaseConfig = DatabaseConfig()
    redis: RedisConfig = RedisConfig()
    api_keys: APIKeysConfig = APIKeysConfig()
    wordpress: WordPressConfig = WordPressConfig()
    content: ContentConfig = ContentConfig()
    
    class Config:
        env_file = '.env'
        case_sensitive = False
        
    @validator('environment')
    def validate_environment(cls, v):
        allowed = ['development', 'staging', 'production']
        if v not in allowed:
            raise ValueError(f"Environment must be one of {allowed}")
        return v
```

### Secrets Management Implementation

```python
# src/config/secrets_manager.py
import hvac
from typing import Dict, Any, Optional
import json
from cryptography.fernet import Fernet
import os

class SecretsManager:
    """Manages secrets using HashiCorp Vault or DO Secrets"""
    
    def __init__(self, backend: str = 'digitalocean'):
        self.backend = backend
        if backend == 'vault':
            self.client = hvac.Client(
                url=os.getenv('VAULT_URL'),
                token=os.getenv('VAULT_TOKEN')
            )
        elif backend == 'digitalocean':
            self.client = DigitalOceanSecretsClient()
        elif backend == 'local':
            self.client = LocalEncryptedStore()
            
    def get_secret(self, key: str, version: Optional[str] = None) -> str:
        """Retrieve a secret value"""
        try:
            if self.backend == 'vault':
                response = self.client.secrets.kv.v2.read_secret_version(
                    path=key,
                    version=version
                )
                return response['data']['data']['value']
                
            elif self.backend == 'digitalocean':
                return self.client.get_secret(key)
                
            elif self.backend == 'local':
                return self.client.get(key)
                
        except Exception as e:
            logger.error(f"Failed to retrieve secret {key}: {e}")
            raise
            
    def set_secret(self, key: str, value: str, metadata: Dict = None) -> None:
        """Store a secret value"""
        if self.backend == 'vault':
            self.client.secrets.kv.v2.create_or_update_secret(
                path=key,
                secret={'value': value},
                metadata=metadata
            )
        elif self.backend == 'digitalocean':
            self.client.create_secret(key, value, metadata)
        elif self.backend == 'local':
            self.client.set(key, value)
            
    def rotate_secret(self, key: str, new_value: str) -> None:
        """Rotate a secret value"""
        # Keep old version for rollback
        old_value = self.get_secret(key)
        self.set_secret(f"{key}_previous", old_value)
        self.set_secret(key, new_value)
        
        # Log rotation
        self.audit_log('secret_rotated', {'key': key})

class LocalEncryptedStore:
    """Local encrypted storage for development"""
    
    def __init__(self, key_file: str = '.secrets.key'):
        self.key_file = key_file
        self.secrets_file = '.secrets.enc'
        self.cipher = self._get_cipher()
        
    def _get_cipher(self) -> Fernet:
        """Get or create encryption key"""
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as f:
                key = f.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)
            os.chmod(self.key_file, 0o600)
            
        return Fernet(key)
        
    def get(self, key: str) -> str:
        """Get encrypted secret"""
        if not os.path.exists(self.secrets_file):
            return None
            
        with open(self.secrets_file, 'rb') as f:
            encrypted_data = f.read()
            
        decrypted = self.cipher.decrypt(encrypted_data)
        secrets = json.loads(decrypted)
        return secrets.get(key)
        
    def set(self, key: str, value: str) -> None:
        """Set encrypted secret"""
        secrets = {}
        if os.path.exists(self.secrets_file):
            with open(self.secrets_file, 'rb') as f:
                encrypted_data = f.read()
            decrypted = self.cipher.decrypt(encrypted_data)
            secrets = json.loads(decrypted)
            
        secrets[key] = value
        encrypted = self.cipher.encrypt(json.dumps(secrets).encode())
        
        with open(self.secrets_file, 'wb') as f:
            f.write(encrypted)
        os.chmod(self.secrets_file, 0o600)
```

### Environment-Specific Configuration

```python
# src/config/environment.py
from typing import Dict, Any
import os

class EnvironmentConfig:
    """Environment-specific configuration loader"""
    
    CONFIGS = {
        'development': {
            'database': {
                'host': 'localhost',
                'port': 5433,
                'name': 'blogposter_dev'
            },
            'redis': {
                'host': 'localhost',
                'port': 6384
            },
            'wordpress': {
                'url': 'http://localhost:8084',
                'verify_ssl': False
            },
            'features': {
                'auto_publish': False,
                'fact_checking': True,
                'cost_tracking': True
            }
        },
        'staging': {
            'database': {
                'host': 'db-staging.digitalocean.com',
                'port': 25060,
                'name': 'blogposter_staging'
            },
            'redis': {
                'host': 'redis-staging.digitalocean.com',
                'port': 25061
            },
            'wordpress': {
                'url': 'https://staging.servicedogus.com',
                'verify_ssl': True
            },
            'features': {
                'auto_publish': False,
                'fact_checking': True,
                'cost_tracking': True
            }
        },
        'production': {
            'database': {
                'host': 'db-prod.digitalocean.com',
                'port': 25060,
                'name': 'blogposter_prod'
            },
            'redis': {
                'host': 'redis-prod.digitalocean.com',
                'port': 25061
            },
            'wordpress': {
                'url': 'https://servicedogus.com',
                'verify_ssl': True
            },
            'features': {
                'auto_publish': True,
                'fact_checking': True,
                'cost_tracking': True
            }
        }
    }
    
    @classmethod
    def get_config(cls, environment: str = None) -> Dict[str, Any]:
        """Get configuration for environment"""
        env = environment or os.getenv('ENVIRONMENT', 'development')
        
        if env not in cls.CONFIGS:
            raise ValueError(f"Unknown environment: {env}")
            
        return cls.CONFIGS[env]
```

### Runtime Configuration API

```python
# src/routers/config.py
from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any

router = APIRouter(prefix="/config", tags=["configuration"])

@router.get("/")
async def get_configuration(
    user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get current configuration (non-sensitive only)"""
    if not user.is_admin:
        raise HTTPException(403, "Admin access required")
        
    config = get_app_config()
    
    # Remove sensitive values
    sanitized = {
        'environment': config.environment,
        'debug': config.debug,
        'features': config.features,
        'content': {
            'min_words': config.content.min_words,
            'max_words': config.content.max_words
        }
    }
    
    return sanitized

@router.post("/update")
async def update_configuration(
    updates: Dict[str, Any],
    user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Update runtime configuration"""
    if not user.is_admin:
        raise HTTPException(403, "Admin access required")
        
    # Validate updates
    validated = validate_config_updates(updates)
    
    # Apply updates
    config_manager.apply_updates(validated)
    
    # Log changes
    audit_log.record('config_updated', {
        'user': user.id,
        'changes': validated
    })
    
    return {'status': 'updated', 'changes': validated}

@router.post("/secrets/rotate")
async def rotate_secret(
    secret_name: str,
    user: User = Depends(get_current_admin)
) -> Dict[str, Any]:
    """Rotate a secret"""
    
    # Generate new secret
    new_value = generate_secure_secret()
    
    # Rotate in secrets manager
    secrets_manager.rotate_secret(secret_name, new_value)
    
    # Update dependent services
    await update_dependent_services(secret_name)
    
    return {'status': 'rotated', 'secret': secret_name}
```

### Configuration Validation

```python
# src/config/validator.py
from pydantic import ValidationError
from typing import Dict, Any, List

class ConfigValidator:
    """Validates configuration against schema"""
    
    def validate(self, config: Dict[str, Any]) -> List[str]:
        """Validate configuration and return errors"""
        errors = []
        
        # Check required fields
        required = [
            'database.host',
            'database.name',
            'api_keys.anthropic_key',
            'wordpress.url'
        ]
        
        for field in required:
            if not self._get_nested(config, field):
                errors.append(f"Missing required field: {field}")
                
        # Validate types
        try:
            ApplicationConfig(**config)
        except ValidationError as e:
            errors.extend([str(err) for err in e.errors()])
            
        # Custom validations
        if config.get('content', {}).get('max_cost_per_article', 0) > 10:
            errors.append("Max cost per article seems too high")
            
        return errors
        
    def _get_nested(self, data: Dict, path: str) -> Any:
        """Get nested dictionary value by dot path"""
        keys = path.split('.')
        value = data
        for key in keys:
            value = value.get(key)
            if value is None:
                return None
        return value
```

### Digital Ocean Integration

```python
# src/config/do_secrets.py
import doctl
from typing import Dict, Optional

class DigitalOceanSecretsClient:
    """Digital Ocean secrets management"""
    
    def __init__(self):
        self.project_id = os.getenv('DO_PROJECT_ID')
        
    def get_secret(self, name: str) -> str:
        """Get secret from DO"""
        # Use doctl or DO API
        result = subprocess.run(
            ['doctl', 'apps', 'config', 'get', name],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            raise Exception(f"Failed to get secret: {result.stderr}")
            
        return result.stdout.strip()
        
    def create_secret(self, name: str, value: str, metadata: Dict = None):
        """Create or update secret"""
        subprocess.run(
            ['doctl', 'apps', 'config', 'set', f"{name}={value}"],
            check=True
        )
        
    def list_secrets(self) -> List[str]:
        """List all secrets"""
        result = subprocess.run(
            ['doctl', 'apps', 'config', 'list'],
            capture_output=True,
            text=True
        )
        
        # Parse output
        secrets = []
        for line in result.stdout.splitlines()[1:]:  # Skip header
            if line:
                secrets.append(line.split()[0])
                
        return secrets
```

### Deployment Configuration Files

```yaml
# .do/app.yaml
name: blog-poster
region: nyc
environments:
  - name: production
    env_vars:
      - key: ENVIRONMENT
        value: "production"
      - key: DATABASE_URL
        scope: RUN_TIME
        type: SECRET
      - key: ANTHROPIC_API_KEY
        scope: RUN_TIME
        type: SECRET
      - key: JINA_API_KEY
        scope: RUN_TIME
        type: SECRET
      - key: WORDPRESS_URL
        value: "https://servicedogus.com"
        
services:
  - name: api
    http_port: 8088
    instance_size_slug: professional-xs
    instance_count: 2
    health_check:
      http_path: /health
      
  - name: worker
    instance_size_slug: professional-s
    instance_count: 3
    run_command: celery -A src.celery_app worker
    
databases:
  - name: postgres
    engine: pg
    version: "15"
    size: db-s-1vcpu-1gb
    num_nodes: 1
    
  - name: redis
    engine: redis
    version: "7"
    size: db-s-1vcpu-1gb
```

### Security Best Practices

```python
# src/config/security.py
import hashlib
import hmac
from typing import Any

class SecureConfig:
    """Security utilities for configuration"""
    
    @staticmethod
    def mask_secret(value: str) -> str:
        """Mask secret for display"""
        if len(value) <= 8:
            return '*' * len(value)
        return value[:4] + '*' * (len(value) - 8) + value[-4:]
        
    @staticmethod
    def hash_secret(value: str) -> str:
        """Hash secret for storage"""
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac('sha256', value.encode(), salt, 100000)
        return salt.hex() + key.hex()
        
    @staticmethod
    def verify_secret(stored: str, provided: str) -> bool:
        """Verify secret against hash"""
        salt = bytes.fromhex(stored[:64])
        stored_key = stored[64:]
        new_key = hashlib.pbkdf2_hmac('sha256', provided.encode(), salt, 100000)
        return hmac.compare_digest(stored_key, new_key.hex())
```

### Audit Logging

```python
# src/config/audit.py
from datetime import datetime
import json

class ConfigAuditLog:
    """Audit log for configuration changes"""
    
    def __init__(self, db_session):
        self.db = db_session
        
    def record(self, action: str, details: Dict[str, Any]):
        """Record configuration action"""
        entry = ConfigAuditEntry(
            timestamp=datetime.utcnow(),
            action=action,
            user_id=get_current_user_id(),
            ip_address=get_client_ip(),
            details=json.dumps(details)
        )
        
        self.db.add(entry)
        self.db.commit()
        
        # Alert on sensitive changes
        if action in ['secret_accessed', 'secret_rotated', 'config_updated']:
            self.send_alert(action, details)
```

---

## Implementation Priority
1. **Week 1**: Secrets manager and encryption
2. **Week 2**: Environment configuration system
3. **Week 3**: Runtime configuration API
4. **Week 4**: Audit logging and monitoring

## Success Metrics
- Zero plain text secrets in codebase
- 100% configuration validation coverage
- < 1 second configuration reload time
- Complete audit trail for all changes
- Zero configuration-related incidents
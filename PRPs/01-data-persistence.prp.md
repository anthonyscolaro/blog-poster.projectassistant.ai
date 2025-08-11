name: "Data Persistence - Simple PostgreSQL Implementation"
description: |

## Purpose
Implement straightforward database persistence using PostgreSQL with pgvector for the blog-poster micro-SaaS.

## Core Principles
1. **Keep It Simple**: Use SQLAlchemy ORM, avoid complex patterns
2. **Just Enough**: Only the tables we actually need
3. **Practical Indexing**: Index what we query, not everything
4. **Simple Migrations**: Alembic for schema changes

---

## Goal
Move from file-based storage to PostgreSQL database with basic user management and data persistence.

## Why
- **Current State**: JSON files, lost on restart, single-user only
- **Target State**: PostgreSQL persistence, multi-user support
- **Business Need**: Users need their data to persist

## What
Essential database models:
- Users & authentication
- Articles with user ownership
- Pipeline runs & history
- API keys per user
- Simple cost tracking

### Success Criteria
- [x] PostgreSQL with pgvector working
- [x] Data migrated from JSON files
- [x] Repository pattern implemented
- [ ] User authentication added
- [ ] Articles scoped to users
- [ ] Basic cost tracking

## Database Schema (Simplified)

```sql
-- Users table (simple)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    api_key VARCHAR(255) UNIQUE,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Articles (what we already have + user_id)
CREATE TABLE articles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    title VARCHAR(500) NOT NULL,
    slug VARCHAR(500) NOT NULL,
    content_markdown TEXT,
    content_html TEXT,
    meta_description VARCHAR(320),
    primary_keyword VARCHAR(100),
    seo_score FLOAT,
    wp_post_id INTEGER,
    wp_url TEXT,
    status VARCHAR(50) DEFAULT 'draft',
    created_at TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_user_articles (user_id),
    INDEX idx_slug (slug)
);

-- Pipeline runs (simplified)
CREATE TABLE pipelines (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    article_id UUID REFERENCES articles(id),
    status VARCHAR(50),
    total_cost DECIMAL(10,4),
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    error_message TEXT,
    
    INDEX idx_user_pipelines (user_id)
);

-- API keys (per user limits)
CREATE TABLE api_usage (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    month DATE,
    articles_generated INTEGER DEFAULT 0,
    total_cost DECIMAL(10,2) DEFAULT 0,
    
    UNIQUE(user_id, month)
);
```

## Implementation Steps

### ✅ Already Done
```python
# We've already implemented:
- SQLAlchemy models (src/database/models.py)
- Repository pattern (src/database/repositories.py)
- Connection pooling (src/database/connection.py)
- Migration script (scripts/migrate_to_postgres.py)
- Retry logic with tenacity
```

### 📝 Still Needed

#### 1. User Model & Authentication
```python
# src/database/models.py - Add User model
class User(Base):
    __tablename__ = 'users'
    
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    api_key = Column(String(255), unique=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    articles = relationship("Article", back_populates="user")
    pipelines = relationship("Pipeline", back_populates="user")
```

#### 2. Simple Authentication
```python
# src/auth/simple_auth.py
from passlib.context import CryptContext
import jwt

pwd_context = CryptContext(schemes=["bcrypt"])

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(user_id: str) -> str:
    return jwt.encode(
        {"user_id": user_id, "exp": datetime.utcnow() + timedelta(days=7)},
        settings.secret_key,
        algorithm="HS256"
    )
```

#### 3. User Scoping
```python
# Update repositories to filter by user
class ArticleRepository:
    def get_user_articles(self, user_id: str, limit: int = 20):
        return self.db.query(Article)\
            .filter(Article.user_id == user_id)\
            .order_by(Article.created_at.desc())\
            .limit(limit)\
            .all()
    
    def create_for_user(self, user_id: str, data: dict):
        data['user_id'] = user_id
        return self.create(data)
```

#### 4. Cost Tracking (Simple)
```python
# src/services/cost_tracker.py
class CostTracker:
    def track_usage(self, user_id: str, cost: float):
        """Track API usage per user per month"""
        current_month = datetime.now().replace(day=1)
        
        usage = db.query(ApiUsage).filter(
            ApiUsage.user_id == user_id,
            ApiUsage.month == current_month
        ).first()
        
        if not usage:
            usage = ApiUsage(user_id=user_id, month=current_month)
            db.add(usage)
        
        usage.articles_generated += 1
        usage.total_cost += cost
        db.commit()
        
        # Check limits
        if usage.total_cost > settings.max_monthly_cost_per_user:
            raise UsageLimitExceeded()
```

## Migration Strategy

### Step 1: Add User Support
```bash
# Create migration for users table
alembic revision -m "add_users_table"

# Edit migration file to add users table
# Run migration
alembic upgrade head
```

### Step 2: Update Existing Data
```python
# One-time script to assign existing articles to admin user
def assign_to_admin():
    admin = User(
        email="admin@example.com",
        password_hash=hash_password("changeme"),
        api_key=generate_api_key()
    )
    db.add(admin)
    db.commit()
    
    # Update all existing articles
    db.execute("UPDATE articles SET user_id = :user_id", {"user_id": admin.id})
    db.commit()
```

## Configuration Updates

```python
# .env additions
SECRET_KEY=your-secret-key-for-jwt
MAX_MONTHLY_COST_PER_USER=50.00
MAX_ARTICLES_PER_USER_PER_MONTH=100
ENABLE_USER_REGISTRATION=true
```

## Testing Requirements

```python
# tests/test_user_management.py
def test_user_registration():
    """User can register and login"""
    
def test_user_owns_articles():
    """User can only see their own articles"""
    
def test_cost_limits():
    """User blocked when exceeding limits"""
    
def test_api_key_per_user():
    """Each user has unique API key"""
```

## What We're NOT Implementing

❌ Complex RBAC (just user/admin is enough)
❌ Team/organization management
❌ Audit logs for everything
❌ Soft deletes
❌ Event sourcing
❌ Database sharding
❌ Read replicas (DO handles backups)

## Success Metrics

✅ Users can register and login
✅ Data persists across restarts
✅ Each user sees only their data
✅ Cost tracking works
✅ Backups happen automatically (via DO)

## Next Steps

1. ✅ PostgreSQL deployed and working
2. Add users table via migration
3. Implement authentication endpoints
4. Update all queries to filter by user
5. Add cost tracking
6. Test with multiple users
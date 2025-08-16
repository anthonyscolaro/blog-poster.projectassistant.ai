# Supabase Cloud to Local Docker Sync Guide

## Overview
This guide explains how to sync your Supabase cloud database with your local Docker development environment for the Blog-Poster project.

## Prerequisites
- Supabase CLI installed (`npm install -g supabase`)
- Docker and Docker Compose running locally
- Access to your Supabase cloud project

## Method 1: Database Migration Export (Recommended)

### Step 1: Export Schema from Cloud
```bash
# Login to Supabase
supabase login

# Link to your cloud project
supabase link --project-ref <your-project-ref>

# Export the database schema
supabase db dump -f supabase/schema.sql

# Export seed data (optional)
supabase db dump --data-only -f supabase/seed.sql
```

### Step 2: Start Local Supabase
```bash
# Initialize local Supabase if not already done
supabase init

# Start local Supabase with Docker
supabase start

# This will start:
# - PostgreSQL on port 54322
# - Studio on port 54323
# - API on port 54321
```

### Step 3: Apply Schema to Local
```bash
# Reset local database and apply schema
supabase db reset

# Or manually apply schema
psql postgresql://postgres:postgres@localhost:54322/postgres < supabase/schema.sql

# Apply seed data if exported
psql postgresql://postgres:postgres@localhost:54322/postgres < supabase/seed.sql
```

## Method 2: Direct Database Sync with pg_dump

### Step 1: Get Cloud Database Credentials
```bash
# From Supabase Dashboard > Settings > Database
# Connection string: postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
```

### Step 2: Create Backup from Cloud
```bash
# Export entire database
pg_dump postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres \
  --schema=public \
  --schema=auth \
  --schema=audit \
  --no-owner \
  --no-privileges \
  > backup.sql

# Or export schema only (no data)
pg_dump postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres \
  --schema-only \
  --schema=public \
  --schema=auth \
  --schema=audit \
  > schema-only.sql
```

### Step 3: Import to Local Docker
```bash
# Import to local Supabase
psql postgresql://postgres:postgres@localhost:54322/postgres < backup.sql

# Or import to custom Docker PostgreSQL
docker exec -i blog-poster-postgres psql -U postgres < backup.sql
```

## Method 3: Using Docker Compose with Supabase

### docker-compose.yml Configuration
```yaml
version: '3.8'

services:
  postgres:
    image: supabase/postgres:15.1.0.117
    container_name: blog-poster-postgres
    ports:
      - "5433:5432"  # Different port to avoid conflicts
    environment:
      POSTGRES_DB: postgres
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-postgres}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./supabase/migrations:/docker-entrypoint-initdb.d
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  supabase-studio:
    image: supabase/studio:latest
    container_name: blog-poster-studio
    ports:
      - "54323:3000"
    environment:
      STUDIO_PG_META_URL: http://postgres:5432
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-postgres}
    depends_on:
      postgres:
        condition: service_healthy

volumes:
  postgres_data:
```

### Environment Variables (.env.local)
```bash
# Local Supabase
VITE_SUPABASE_URL=http://localhost:54321
VITE_SUPABASE_ANON_KEY=your-local-anon-key

# Cloud Supabase (for reference)
# VITE_SUPABASE_URL=https://[PROJECT-REF].supabase.co
# VITE_SUPABASE_ANON_KEY=your-cloud-anon-key
```

## Method 4: Automated Sync Script

### Create sync-supabase.sh
```bash
#!/bin/bash

# Configuration
CLOUD_DB_URL="postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres"
LOCAL_DB_URL="postgresql://postgres:postgres@localhost:54322/postgres"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Starting Supabase Cloud to Local Sync...${NC}"

# Step 1: Export from cloud
echo -e "${GREEN}Exporting from cloud...${NC}"
pg_dump $CLOUD_DB_URL \
  --schema=public \
  --schema=auth \
  --schema=audit \
  --no-owner \
  --no-privileges \
  --clean \
  --if-exists \
  > /tmp/supabase-backup.sql

# Step 2: Stop local services
echo -e "${GREEN}Stopping local services...${NC}"
docker compose down

# Step 3: Start fresh local database
echo -e "${GREEN}Starting fresh local database...${NC}"
docker compose up -d postgres
sleep 5  # Wait for postgres to be ready

# Step 4: Import to local
echo -e "${GREEN}Importing to local database...${NC}"
psql $LOCAL_DB_URL < /tmp/supabase-backup.sql

# Step 5: Start all services
echo -e "${GREEN}Starting all services...${NC}"
docker compose up -d

# Step 6: Cleanup
rm /tmp/supabase-backup.sql

echo -e "${GREEN}Sync complete! Local database is now in sync with cloud.${NC}"
```

### Make executable and run
```bash
chmod +x sync-supabase.sh
./sync-supabase.sh
```

## Best Practices

### 1. Development Workflow
```bash
# Daily sync routine
1. Pull latest schema changes from cloud
2. Apply to local Docker environment  
3. Test features locally
4. Push migrations to cloud when ready
```

### 2. Migration Management
```bash
# Create new migration
supabase migration new <migration-name>

# Apply migrations locally
supabase db reset

# Push migrations to cloud
supabase db push
```

### 3. Separate Development Data
- Use different data in local vs cloud
- Keep sensitive data only in cloud
- Use seed data for local development

### 4. Environment Configuration
```javascript
// src/services/supabase.ts
const supabaseUrl = process.env.NODE_ENV === 'development' 
  ? process.env.VITE_SUPABASE_LOCAL_URL 
  : process.env.VITE_SUPABASE_URL;

const supabaseAnonKey = process.env.NODE_ENV === 'development'
  ? process.env.VITE_SUPABASE_LOCAL_ANON_KEY
  : process.env.VITE_SUPABASE_ANON_KEY;
```

## Troubleshooting

### Common Issues

1. **Port Conflicts**
```bash
# Check if ports are in use
lsof -i :54322  # Supabase PostgreSQL
lsof -i :5433   # Custom PostgreSQL

# Kill process using port
kill -9 <PID>
```

2. **Permission Issues**
```bash
# Fix volume permissions
docker exec blog-poster-postgres chown -R postgres:postgres /var/lib/postgresql/data
```

3. **Extension Errors**
```sql
-- If extensions fail to create
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "pgjwt";
```

4. **RLS Policy Conflicts**
```sql
-- Drop all policies before import
DO $$ 
DECLARE
  r RECORD;
BEGIN
  FOR r IN (SELECT schemaname, tablename FROM pg_tables WHERE schemaname = 'public') 
  LOOP
    EXECUTE format('DROP POLICY IF EXISTS ALL ON %I.%I', r.schemaname, r.tablename);
  END LOOP;
END $$;
```

## Verification

### Check Sync Status
```sql
-- Connect to local database
psql postgresql://postgres:postgres@localhost:54322/postgres

-- Check tables exist
\dt public.*

-- Check RLS is enabled
SELECT tablename, rowsecurity 
FROM pg_tables 
WHERE schemaname = 'public';

-- Check functions
SELECT routine_name 
FROM information_schema.routines 
WHERE routine_schema = 'public';

-- Test a query
SELECT * FROM public.organizations LIMIT 1;
```

## Security Notes

⚠️ **Never commit credentials to git**
- Use `.env.local` (gitignored)
- Use environment variables in CI/CD
- Rotate passwords regularly

⚠️ **Production Data**
- Be careful with production data in local
- Consider data masking for sensitive info
- Use separate test accounts locally

## Next Steps

1. Set up local Supabase with Docker
2. Sync schema from cloud
3. Configure environment variables
4. Test authentication flow locally
5. Develop features with hot reload
6. Push migrations back to cloud when ready

This setup ensures your local Docker environment stays in sync with your Supabase cloud database while maintaining security and data isolation.
-- Part 1: Extensions, Schemas, and Core Tables

-- Step 1: Enable Required Extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "pgsodium";
CREATE EXTENSION IF NOT EXISTS "vector";
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";

-- Step 2: Create Schemas
CREATE SCHEMA IF NOT EXISTS audit;
CREATE SCHEMA IF NOT EXISTS billing;
CREATE SCHEMA IF NOT EXISTS content;

-- Grant usage
GRANT USAGE ON SCHEMA audit TO authenticated;
GRANT USAGE ON SCHEMA billing TO authenticated;
GRANT USAGE ON SCHEMA content TO authenticated;

-- Step 3: Create Migration Tracking
CREATE TABLE IF NOT EXISTS public.schema_migrations (
  version TEXT PRIMARY KEY,
  executed_at TIMESTAMPTZ DEFAULT NOW(),
  executed_by TEXT DEFAULT current_user
);

INSERT INTO public.schema_migrations (version) VALUES ('001_initial_setup') ON CONFLICT DO NOTHING;

-- Step 4: Ensure Organizations table has all required columns
DO $$
BEGIN
  -- Add missing columns if they don't exist
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'organizations' AND column_name = 'billing_cycle_start') THEN
    ALTER TABLE public.organizations ADD COLUMN billing_cycle_start DATE DEFAULT CURRENT_DATE;
  END IF;
  
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'organizations' AND column_name = 'billing_cycle_end') THEN
    ALTER TABLE public.organizations ADD COLUMN billing_cycle_end DATE DEFAULT (CURRENT_DATE + INTERVAL '30 days');
  END IF;
END $$;

-- Step 5: Ensure Profiles table has all required columns
DO $$
BEGIN
  -- Add missing columns if they don't exist
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'profiles' AND column_name = 'platform_role') THEN
    ALTER TABLE public.profiles ADD COLUMN platform_role TEXT DEFAULT 'user' CHECK (platform_role IN ('user', 'admin', 'super_admin'));
  END IF;
  
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'profiles' AND column_name = 'failed_login_attempts') THEN
    ALTER TABLE public.profiles ADD COLUMN failed_login_attempts INTEGER DEFAULT 0;
  END IF;
  
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'profiles' AND column_name = 'account_locked_until') THEN
    ALTER TABLE public.profiles ADD COLUMN account_locked_until TIMESTAMPTZ;
  END IF;
END $$;

-- Step 6: Create API Keys Table if not exists
CREATE TABLE IF NOT EXISTS public.organization_api_keys (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID NOT NULL REFERENCES public.organizations(id) ON DELETE CASCADE,
  
  service TEXT NOT NULL CHECK (service IN ('anthropic', 'openai', 'jina', 'wordpress', 'custom')),
  key_name TEXT NOT NULL,
  key_hint TEXT,
  encrypted_key TEXT NOT NULL,
  key_hash TEXT NOT NULL,
  
  -- Security
  last_used_at TIMESTAMPTZ,
  last_used_ip INET,
  usage_count INTEGER DEFAULT 0,
  rate_limit_per_hour INTEGER DEFAULT 100,
  rate_limit_per_day INTEGER DEFAULT 1000,
  allowed_ips INET[],
  expires_at TIMESTAMPTZ,
  
  -- Audit
  created_by UUID REFERENCES auth.users(id),
  revoked_at TIMESTAMPTZ,
  revoked_by UUID REFERENCES auth.users(id),
  revoke_reason TEXT,
  
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  
  UNIQUE(organization_id, service, key_name)
);

-- Step 7: Ensure Articles table has all required columns
DO $$
BEGIN
  -- Add missing columns if they don't exist
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'articles' AND column_name = 'keyword_density') THEN
    ALTER TABLE public.articles ADD COLUMN keyword_density DECIMAL(5,2);
  END IF;
  
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'articles' AND column_name = 'headings_count') THEN
    ALTER TABLE public.articles ADD COLUMN headings_count INTEGER DEFAULT 0;
  END IF;
  
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'articles' AND column_name = 'links_internal') THEN
    ALTER TABLE public.articles ADD COLUMN links_internal INTEGER DEFAULT 0;
  END IF;
  
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'articles' AND column_name = 'links_external') THEN
    ALTER TABLE public.articles ADD COLUMN links_external INTEGER DEFAULT 0;
  END IF;
END $$;

-- Step 8: Ensure Pipelines table has all required columns  
DO $$
BEGIN
  -- Add missing columns if they don't exist
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'pipelines' AND column_name = 'template_id') THEN
    ALTER TABLE public.pipelines ADD COLUMN template_id UUID;
  END IF;
  
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'pipelines' AND column_name = 'execution_time') THEN
    ALTER TABLE public.pipelines ADD COLUMN execution_time INTEGER;
  END IF;
  
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'pipelines' AND column_name = 'estimated_completion') THEN
    ALTER TABLE public.pipelines ADD COLUMN estimated_completion TIMESTAMPTZ;
  END IF;
END $$;

-- Step 9: Create Audit Log Table if not exists
CREATE TABLE IF NOT EXISTS audit.audit_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID REFERENCES public.organizations(id) ON DELETE SET NULL,
  user_id UUID REFERENCES auth.users(id) ON DELETE SET NULL,
  
  -- Audit details
  action TEXT NOT NULL,
  entity_type TEXT NOT NULL,
  entity_id UUID,
  
  -- Change tracking
  old_values JSONB,
  new_values JSONB,
  changed_fields TEXT[],
  
  -- Context
  ip_address INET,
  user_agent TEXT,
  session_id TEXT,
  
  -- Result
  success BOOLEAN DEFAULT TRUE,
  error_message TEXT,
  
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Step 10: Create Basic Indexes
CREATE INDEX IF NOT EXISTS idx_organizations_slug ON public.organizations(slug) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_organizations_plan ON public.organizations(plan) WHERE deleted_at IS NULL;

CREATE INDEX IF NOT EXISTS idx_profiles_email ON public.profiles(email) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_profiles_organization ON public.profiles(organization_id) WHERE deleted_at IS NULL;

CREATE INDEX IF NOT EXISTS idx_articles_organization ON public.articles(organization_id) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_articles_status ON public.articles(status) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_articles_published ON public.articles(published_at DESC) WHERE deleted_at IS NULL AND status = 'published';

CREATE INDEX IF NOT EXISTS idx_pipelines_organization ON public.pipelines(organization_id);
CREATE INDEX IF NOT EXISTS idx_pipelines_status ON public.pipelines(status);

CREATE INDEX IF NOT EXISTS idx_audit_log_organization ON audit.audit_log(organization_id);
CREATE INDEX IF NOT EXISTS idx_audit_log_created ON audit.audit_log(created_at DESC);

-- Verification query
SELECT COUNT(*) AS tables_created FROM information_schema.tables 
WHERE table_schema IN ('public', 'audit');
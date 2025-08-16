-- Part 1: Enable Required Extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "pgsodium";
CREATE EXTENSION IF NOT EXISTS "vector";
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";

-- Part 2: Create Schemas
CREATE SCHEMA IF NOT EXISTS audit;
CREATE SCHEMA IF NOT EXISTS billing;
CREATE SCHEMA IF NOT EXISTS content;

-- Grant usage
GRANT USAGE ON SCHEMA audit TO authenticated;
GRANT USAGE ON SCHEMA billing TO authenticated;
GRANT USAGE ON SCHEMA content TO authenticated;

-- Part 3: Migration Tracking
CREATE TABLE IF NOT EXISTS public.schema_migrations (
  version TEXT PRIMARY KEY,
  executed_at TIMESTAMPTZ DEFAULT NOW(),
  executed_by TEXT DEFAULT current_user
);

INSERT INTO public.schema_migrations (version) VALUES ('001_initial_setup');

-- Part 4: Organizations Table
CREATE TABLE IF NOT EXISTS public.organizations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  slug TEXT UNIQUE NOT NULL,
  
  -- Billing
  plan TEXT DEFAULT 'free' CHECK (plan IN ('free', 'starter', 'professional', 'enterprise')),
  subscription_status TEXT DEFAULT 'active' CHECK (subscription_status IN ('active', 'cancelled', 'past_due', 'unpaid', 'trialing')),
  stripe_customer_id TEXT,
  stripe_subscription_id TEXT,
  
  -- Limits
  articles_limit INTEGER DEFAULT 2,
  articles_used INTEGER DEFAULT 0,
  team_members_limit INTEGER DEFAULT 1,
  team_members_used INTEGER DEFAULT 1,
  monthly_budget DECIMAL(10,2) DEFAULT 100.00,
  current_month_cost DECIMAL(10,2) DEFAULT 0.00,
  budget_alert_threshold INTEGER DEFAULT 80,
  
  -- Billing cycle
  billing_cycle_start DATE DEFAULT CURRENT_DATE,
  billing_cycle_end DATE DEFAULT (CURRENT_DATE + INTERVAL '30 days'),
  trial_ends_at TIMESTAMPTZ,
  
  -- Settings
  settings JSONB DEFAULT '{
    "branding": {"logo": null, "primary_color": "#667eea"},
    "integrations": {"slack_webhook": null, "discord_webhook": null},
    "security": {"require_2fa": false, "allowed_domains": [], "ip_whitelist": []},
    "features": {"api_access": false, "custom_branding": false}
  }'::jsonb,
  
  contact_email TEXT,
  billing_email TEXT,
  deleted_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Part 5: Profiles Table
CREATE TABLE IF NOT EXISTS public.profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  organization_id UUID REFERENCES public.organizations(id) ON DELETE CASCADE,
  
  email TEXT UNIQUE NOT NULL,
  full_name TEXT,
  avatar_url TEXT,
  
  -- Roles
  role TEXT DEFAULT 'member' CHECK (role IN ('owner', 'admin', 'editor', 'member', 'viewer')),
  platform_role TEXT DEFAULT 'user' CHECK (platform_role IN ('user', 'admin', 'super_admin')),
  
  -- Settings
  notification_preferences JSONB DEFAULT '{"email": true, "browser": true}'::jsonb,
  timezone TEXT DEFAULT 'America/New_York',
  
  -- Security
  two_factor_enabled BOOLEAN DEFAULT FALSE,
  last_password_change TIMESTAMPTZ DEFAULT NOW(),
  failed_login_attempts INTEGER DEFAULT 0,
  account_locked_until TIMESTAMPTZ,
  
  -- Onboarding
  onboarding_completed BOOLEAN DEFAULT FALSE,
  onboarding_step INTEGER DEFAULT 0,
  
  deleted_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  last_login_at TIMESTAMPTZ,
  last_activity_at TIMESTAMPTZ
);

-- Part 6: API Keys Table
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

-- Part 7: Articles Table
CREATE TABLE IF NOT EXISTS public.articles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID NOT NULL REFERENCES public.organizations(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  
  -- Content
  title TEXT NOT NULL,
  slug TEXT NOT NULL,
  content TEXT,
  content_html TEXT,
  excerpt TEXT,
  featured_image TEXT,
  images TEXT[],
  
  -- SEO
  meta_title TEXT,
  meta_description TEXT,
  canonical_url TEXT,
  schema_markup JSONB,
  keywords TEXT[],
  focus_keyword TEXT,
  seo_score INTEGER DEFAULT 0 CHECK (seo_score >= 0 AND seo_score <= 100),
  readability_score INTEGER DEFAULT 0 CHECK (readability_score >= 0 AND readability_score <= 100),
  keyword_density DECIMAL(5,2),
  
  -- Metrics
  word_count INTEGER DEFAULT 0,
  reading_time INTEGER DEFAULT 0,
  headings_count INTEGER DEFAULT 0,
  links_internal INTEGER DEFAULT 0,
  links_external INTEGER DEFAULT 0,
  
  -- Status
  status TEXT DEFAULT 'draft' CHECK (status IN ('draft', 'review', 'approved', 'scheduled', 'published', 'archived')),
  review_status TEXT CHECK (review_status IN ('pending', 'approved', 'rejected', 'changes_requested')),
  reviewed_by UUID REFERENCES auth.users(id),
  reviewed_at TIMESTAMPTZ,
  
  -- Cost
  generation_cost DECIMAL(10,4) DEFAULT 0.00,
  tokens_used INTEGER DEFAULT 0,
  
  -- WordPress
  wordpress_id TEXT,
  wordpress_url TEXT,
  wordpress_site TEXT,
  sync_status TEXT CHECK (sync_status IN ('pending', 'synced', 'failed', 'out_of_sync')),
  last_synced_at TIMESTAMPTZ,
  
  -- Publishing
  published_at TIMESTAMPTZ,
  scheduled_for TIMESTAMPTZ,
  unpublished_at TIMESTAMPTZ,
  
  -- Legal
  legal_reviewed BOOLEAN DEFAULT FALSE,
  legal_review_status TEXT CHECK (legal_review_status IN ('pending', 'passed', 'failed', 'flagged')),
  legal_notes TEXT,
  citations JSONB DEFAULT '[]'::jsonb,
  compliance_flags TEXT[],
  
  -- Performance
  views_count INTEGER DEFAULT 0,
  shares_count INTEGER DEFAULT 0,
  
  -- Version control
  version INTEGER DEFAULT 1,
  previous_versions JSONB DEFAULT '[]'::jsonb,
  
  deleted_at TIMESTAMPTZ,
  deleted_by UUID REFERENCES auth.users(id),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  
  UNIQUE(organization_id, slug)
);

-- Part 8: Pipelines Table
CREATE TABLE IF NOT EXISTS public.pipelines (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID NOT NULL REFERENCES public.organizations(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  article_id UUID REFERENCES public.articles(id) ON DELETE SET NULL,
  
  name TEXT NOT NULL,
  description TEXT,
  
  -- Status
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'queued', 'running', 'completed', 'failed', 'cancelled', 'paused')),
  priority INTEGER DEFAULT 5 CHECK (priority >= 1 AND priority <= 10),
  progress INTEGER DEFAULT 0 CHECK (progress >= 0 AND progress <= 100),
  
  -- Agent tracking
  agents_completed JSONB DEFAULT '[]'::jsonb,
  current_agent TEXT,
  agent_status JSONB DEFAULT '{}'::jsonb,
  agent_logs JSONB DEFAULT '[]'::jsonb,
  
  -- Configuration
  config JSONB DEFAULT '{}'::jsonb,
  template_id UUID,
  
  -- Cost
  estimated_cost DECIMAL(10,4) DEFAULT 0.00,
  total_cost DECIMAL(10,4) DEFAULT 0.00,
  cost_breakdown JSONB DEFAULT '{}'::jsonb,
  
  -- Error handling
  error_message TEXT,
  error_details JSONB,
  error_code TEXT,
  retry_count INTEGER DEFAULT 0,
  max_retries INTEGER DEFAULT 3,
  
  -- Timing
  queued_at TIMESTAMPTZ,
  started_at TIMESTAMPTZ,
  completed_at TIMESTAMPTZ,
  execution_time INTEGER,
  estimated_completion TIMESTAMPTZ,
  
  -- Results
  results JSONB DEFAULT '{}'::jsonb,
  metrics JSONB DEFAULT '{}'::jsonb,
  
  -- Cancellation
  cancelled_by UUID REFERENCES auth.users(id),
  cancellation_reason TEXT,
  
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Part 9: Audit Log Table
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

-- Part 10: Create Indexes
-- Organization indexes
CREATE INDEX IF NOT EXISTS idx_organizations_slug ON public.organizations(slug) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_organizations_plan ON public.organizations(plan) WHERE deleted_at IS NULL;

-- Profile indexes
CREATE INDEX IF NOT EXISTS idx_profiles_email ON public.profiles(email) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_profiles_organization ON public.profiles(organization_id) WHERE deleted_at IS NULL;

-- Article indexes
CREATE INDEX IF NOT EXISTS idx_articles_organization ON public.articles(organization_id) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_articles_status ON public.articles(status) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_articles_published ON public.articles(published_at DESC) WHERE deleted_at IS NULL AND status = 'published';

-- Pipeline indexes
CREATE INDEX IF NOT EXISTS idx_pipelines_organization ON public.pipelines(organization_id);
CREATE INDEX IF NOT EXISTS idx_pipelines_status ON public.pipelines(status);

-- Audit log indexes
CREATE INDEX IF NOT EXISTS idx_audit_log_organization ON audit.audit_log(organization_id);
CREATE INDEX IF NOT EXISTS idx_audit_log_created ON audit.audit_log(created_at DESC);

-- Part 11: Create timestamp update function
CREATE OR REPLACE FUNCTION public.update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Add triggers for updated_at columns
CREATE TRIGGER update_organizations_updated_at
    BEFORE UPDATE ON public.organizations
    FOR EACH ROW
    EXECUTE FUNCTION public.update_updated_at_column();

CREATE TRIGGER update_profiles_updated_at
    BEFORE UPDATE ON public.profiles
    FOR EACH ROW
    EXECUTE FUNCTION public.update_updated_at_column();

CREATE TRIGGER update_organization_api_keys_updated_at
    BEFORE UPDATE ON public.organization_api_keys
    FOR EACH ROW
    EXECUTE FUNCTION public.update_updated_at_column();

CREATE TRIGGER update_articles_updated_at
    BEFORE UPDATE ON public.articles
    FOR EACH ROW
    EXECUTE FUNCTION public.update_updated_at_column();
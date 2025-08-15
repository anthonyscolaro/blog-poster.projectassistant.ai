# Lovable Prompt: Supabase Additional Tables (Part 2 of 4)

## 🤖 AUTO-IMPLEMENTATION INSTRUCTIONS

Execute all SQL commands without asking for approval. This is Part 2 of 4.

## Part 2: Additional Tables and Relationships

### Step 1: Create Agent Configs Table

```sql
CREATE TABLE IF NOT EXISTS public.agent_configs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID NOT NULL REFERENCES public.organizations(id) ON DELETE CASCADE,
  
  agent_name TEXT NOT NULL CHECK (agent_name IN ('competitor', 'topic', 'article', 'legal', 'wordpress')),
  
  enabled BOOLEAN DEFAULT TRUE,
  config JSONB DEFAULT '{}'::jsonb,
  custom_prompts JSONB DEFAULT '{}'::jsonb,
  model_preferences JSONB DEFAULT '{"primary": "claude-3-5-sonnet-20241022", "fallback": "gpt-4-turbo-preview"}'::jsonb,
  
  timeout_seconds INTEGER DEFAULT 300,
  max_retries INTEGER DEFAULT 3,
  retry_delay_seconds INTEGER DEFAULT 5,
  priority INTEGER DEFAULT 5,
  
  max_runs_per_hour INTEGER DEFAULT 10,
  max_runs_per_day INTEGER DEFAULT 100,
  
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  
  UNIQUE(organization_id, agent_name)
);
```

### Step 2: Create Competitors Table

```sql
CREATE TABLE IF NOT EXISTS public.competitors (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID NOT NULL REFERENCES public.organizations(id) ON DELETE CASCADE,
  
  name TEXT NOT NULL,
  domain TEXT NOT NULL,
  feed_urls TEXT[],
  sitemap_url TEXT,
  
  enabled BOOLEAN DEFAULT TRUE,
  check_frequency TEXT DEFAULT 'daily' CHECK (check_frequency IN ('hourly', 'daily', 'weekly', 'monthly')),
  last_checked_at TIMESTAMPTZ,
  next_check_at TIMESTAMPTZ,
  
  articles_found INTEGER DEFAULT 0,
  articles_analyzed INTEGER DEFAULT 0,
  last_article_date TIMESTAMPTZ,
  
  track_keywords TEXT[],
  ignore_keywords TEXT[],
  min_word_count INTEGER DEFAULT 500,
  
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  
  UNIQUE(organization_id, domain)
);
```

### Step 3: Create Topics Table

```sql
CREATE TABLE IF NOT EXISTS public.topics (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID NOT NULL REFERENCES public.organizations(id) ON DELETE CASCADE,
  
  keyword TEXT NOT NULL,
  topic_cluster TEXT,
  search_volume INTEGER,
  trend TEXT CHECK (trend IN ('rising', 'steady', 'declining')),
  competition_level TEXT CHECK (competition_level IN ('low', 'medium', 'high')),
  
  difficulty_score INTEGER CHECK (difficulty_score >= 0 AND difficulty_score <= 100),
  opportunity_score INTEGER CHECK (opportunity_score >= 0 AND opportunity_score <= 100),
  cpc DECIMAL(10,2),
  
  status TEXT DEFAULT 'identified' CHECK (status IN ('identified', 'researching', 'approved', 'in_progress', 'completed', 'rejected', 'archived')),
  
  related_keywords TEXT[],
  questions TEXT[],
  competitor_coverage JSONB DEFAULT '{}'::jsonb,
  content_gaps TEXT[],
  
  assigned_to UUID REFERENCES auth.users(id),
  assigned_at TIMESTAMPTZ,
  
  identified_at TIMESTAMPTZ DEFAULT NOW(),
  approved_at TIMESTAMPTZ,
  approved_by UUID REFERENCES auth.users(id),
  completed_at TIMESTAMPTZ,
  
  UNIQUE(organization_id, keyword)
);
```

### Step 4: Create Cost Tracking Table

```sql
CREATE TABLE IF NOT EXISTS public.cost_tracking (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID NOT NULL REFERENCES public.organizations(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  
  pipeline_id UUID REFERENCES public.pipelines(id) ON DELETE CASCADE,
  article_id UUID REFERENCES public.articles(id) ON DELETE CASCADE,
  
  service TEXT NOT NULL CHECK (service IN ('anthropic', 'openai', 'jina', 'wordpress', 'supabase', 'other')),
  service_detail TEXT,
  amount DECIMAL(10,6) NOT NULL,
  
  tokens_used INTEGER,
  tokens_input INTEGER,
  tokens_output INTEGER,
  api_calls INTEGER DEFAULT 1,
  
  billing_month DATE DEFAULT DATE_TRUNC('month', CURRENT_DATE),
  billing_cycle UUID,
  
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Add index for performance
CREATE INDEX IF NOT EXISTS idx_cost_org_month ON public.cost_tracking(organization_id, billing_month);
```

### Step 5: Create Invitations Table

```sql
CREATE TABLE IF NOT EXISTS public.invitations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID NOT NULL REFERENCES public.organizations(id) ON DELETE CASCADE,
  
  email TEXT NOT NULL,
  role TEXT NOT NULL CHECK (role IN ('admin', 'editor', 'member', 'viewer')),
  
  token TEXT UNIQUE NOT NULL DEFAULT encode(gen_random_bytes(32), 'hex'),
  
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'accepted', 'rejected', 'expired', 'cancelled')),
  
  invited_by UUID NOT NULL REFERENCES auth.users(id),
  accepted_by UUID REFERENCES auth.users(id),
  accepted_at TIMESTAMPTZ,
  
  expires_at TIMESTAMPTZ DEFAULT (NOW() + INTERVAL '7 days'),
  
  created_at TIMESTAMPTZ DEFAULT NOW(),
  
  UNIQUE(organization_id, email, status)
);
```

### Step 6: Create Webhook Logs Table

```sql
CREATE TABLE IF NOT EXISTS public.webhook_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID NOT NULL REFERENCES public.organizations(id) ON DELETE CASCADE,
  
  event_type TEXT NOT NULL,
  webhook_url TEXT NOT NULL,
  payload JSONB NOT NULL,
  headers JSONB,
  
  status_code INTEGER,
  response_body TEXT,
  response_headers JSONB,
  
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'success', 'failed', 'retrying')),
  delivered BOOLEAN DEFAULT FALSE,
  
  retry_count INTEGER DEFAULT 0,
  max_retries INTEGER DEFAULT 3,
  next_retry_at TIMESTAMPTZ,
  
  error_message TEXT,
  
  created_at TIMESTAMPTZ DEFAULT NOW(),
  delivered_at TIMESTAMPTZ
);
```

### Step 7: Create Rate Limits Table

```sql
CREATE TABLE IF NOT EXISTS public.rate_limits (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID NOT NULL REFERENCES public.organizations(id) ON DELETE CASCADE,
  
  endpoint TEXT NOT NULL,
  method TEXT NOT NULL,
  
  requests_count INTEGER DEFAULT 0,
  period_start TIMESTAMPTZ DEFAULT NOW(),
  period_end TIMESTAMPTZ DEFAULT (NOW() + INTERVAL '1 hour'),
  
  max_requests INTEGER DEFAULT 100,
  
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  
  UNIQUE(organization_id, endpoint, method, period_start)
);
```

### Step 8: Add More Indexes

```sql
-- Cost tracking indexes
CREATE INDEX IF NOT EXISTS idx_cost_tracking_organization ON public.cost_tracking(organization_id);
CREATE INDEX IF NOT EXISTS idx_cost_tracking_month ON public.cost_tracking(billing_month);
CREATE INDEX IF NOT EXISTS idx_cost_tracking_service ON public.cost_tracking(service);

-- Topics indexes
CREATE INDEX IF NOT EXISTS idx_topics_organization ON public.topics(organization_id);
CREATE INDEX IF NOT EXISTS idx_topics_status ON public.topics(status);
CREATE INDEX IF NOT EXISTS idx_topics_keyword ON public.topics(keyword);

-- API keys indexes
CREATE INDEX IF NOT EXISTS idx_api_keys_organization ON public.organization_api_keys(organization_id);
CREATE INDEX IF NOT EXISTS idx_api_keys_hash ON public.organization_api_keys(key_hash) WHERE is_active = TRUE;

-- Invitations indexes
CREATE INDEX IF NOT EXISTS idx_invitations_organization ON public.invitations(organization_id);
CREATE INDEX IF NOT EXISTS idx_invitations_email ON public.invitations(email);
CREATE INDEX IF NOT EXISTS idx_invitations_token ON public.invitations(token);

-- Webhook logs indexes
CREATE INDEX IF NOT EXISTS idx_webhook_logs_organization ON public.webhook_logs(organization_id);
CREATE INDEX IF NOT EXISTS idx_webhook_logs_status ON public.webhook_logs(status);
```

### Step 9: Enable Row Level Security on All Tables

```sql
-- Enable RLS
ALTER TABLE public.organizations ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.organization_api_keys ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.articles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.pipelines ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.agent_configs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.competitors ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.topics ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.cost_tracking ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.webhook_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.invitations ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.rate_limits ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit.audit_log ENABLE ROW LEVEL SECURITY;
```

## Verification

After running this part, verify with:
```sql
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public' 
ORDER BY table_name;
```

Expected: All additional tables created (agent_configs, competitors, topics, cost_tracking, invitations, webhook_logs, rate_limits)

**Continue with Part 3 (09c-supabase-setup-security.md)**
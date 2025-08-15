# Lovable Prompt: Supabase Views & Final Setup (Part 4 of 4)

## 🤖 AUTO-IMPLEMENTATION INSTRUCTIONS

Execute all SQL commands without asking for approval. This is Part 4 of 4 - the final part.

## Part 4: Views, Storage, and Final Configuration

### Step 1: Create Dashboard View

```sql
-- Organization dashboard view
CREATE OR REPLACE VIEW public.organization_dashboard AS
SELECT 
  o.id,
  o.name,
  o.plan,
  o.subscription_status,
  o.articles_limit,
  o.articles_used,
  o.monthly_budget,
  o.current_month_cost,
  ROUND((o.current_month_cost / NULLIF(o.monthly_budget, 0) * 100)::numeric, 2) AS budget_percentage,
  o.trial_ends_at,
  COUNT(DISTINCT p.id) AS team_members,
  COUNT(DISTINCT a.id) FILTER (WHERE a.status = 'published') AS published_articles,
  COUNT(DISTINCT a.id) FILTER (WHERE a.status = 'draft') AS draft_articles,
  COUNT(DISTINCT pip.id) FILTER (WHERE pip.status = 'running') AS active_pipelines,
  COUNT(DISTINCT pip.id) FILTER (WHERE pip.status = 'completed') AS completed_pipelines
FROM public.organizations o
LEFT JOIN public.profiles p ON p.organization_id = o.id AND p.deleted_at IS NULL
LEFT JOIN public.articles a ON a.organization_id = o.id AND a.deleted_at IS NULL
LEFT JOIN public.pipelines pip ON pip.organization_id = o.id
WHERE o.deleted_at IS NULL
GROUP BY o.id;
```

### Step 2: Create Article Performance View

```sql
-- Article performance view
CREATE OR REPLACE VIEW public.article_performance AS
SELECT 
  a.id,
  a.organization_id,
  a.title,
  a.status,
  a.published_at,
  a.seo_score,
  a.readability_score,
  a.word_count,
  a.generation_cost,
  a.views_count,
  a.shares_count,
  CASE 
    WHEN a.views_count > 0 
    THEN ROUND((a.shares_count::numeric / a.views_count * 100), 2)
    ELSE 0
  END AS engagement_rate,
  u.full_name AS author_name,
  u.email AS author_email
FROM public.articles a
JOIN public.profiles u ON u.id = a.user_id
WHERE a.deleted_at IS NULL;
```

### Step 3: Create Cost Analysis View

```sql
-- Cost analysis view
CREATE OR REPLACE VIEW public.cost_analysis AS
SELECT 
  organization_id,
  billing_month,
  service,
  COUNT(*) AS api_calls,
  SUM(tokens_used) AS total_tokens,
  SUM(amount) AS total_cost,
  AVG(amount) AS avg_cost_per_call,
  MAX(amount) AS max_cost,
  MIN(amount) AS min_cost
FROM public.cost_tracking
GROUP BY organization_id, billing_month, service
ORDER BY billing_month DESC, total_cost DESC;
```

### Step 4: Create Recent Activity View

```sql
-- Recent activity view
CREATE OR REPLACE VIEW public.recent_activity AS
SELECT * FROM (
  SELECT 
    'article_created' AS activity_type,
    id AS activity_id,
    organization_id,
    user_id,
    title AS description,
    NULL AS details,
    created_at AS occurred_at
  FROM public.articles
  WHERE deleted_at IS NULL
  
  UNION ALL
  
  SELECT 
    'pipeline_' || status AS activity_type,
    id AS activity_id,
    organization_id,
    user_id,
    name AS description,
    jsonb_build_object(
      'progress', progress,
      'cost', total_cost
    ) AS details,
    COALESCE(completed_at, started_at, created_at) AS occurred_at
  FROM public.pipelines
  
  UNION ALL
  
  SELECT 
    'invitation_sent' AS activity_type,
    id AS activity_id,
    organization_id,
    invited_by AS user_id,
    'Invitation to ' || email AS description,
    jsonb_build_object('role', role) AS details,
    created_at AS occurred_at
  FROM public.invitations
  WHERE status = 'pending'
) AS combined
ORDER BY occurred_at DESC
LIMIT 100;
```

### Step 5: Create Article Stats View

```sql
-- Article statistics view
CREATE OR REPLACE VIEW public.article_stats AS
SELECT 
  organization_id,
  COUNT(*) as total_articles,
  COUNT(CASE WHEN status = 'published' THEN 1 END) as published_articles,
  COUNT(CASE WHEN status = 'draft' THEN 1 END) as draft_articles,
  AVG(seo_score) as avg_seo_score,
  AVG(word_count) as avg_word_count,
  SUM(generation_cost) as total_cost
FROM public.articles
WHERE deleted_at IS NULL
GROUP BY organization_id;
```

### Step 6: Create Pipeline Stats View

```sql
-- Pipeline statistics view
CREATE OR REPLACE VIEW public.pipeline_stats AS
SELECT 
  organization_id,
  COUNT(*) as total_runs,
  COUNT(CASE WHEN status = 'completed' THEN 1 END) as successful_runs,
  COUNT(CASE WHEN status = 'failed' THEN 1 END) as failed_runs,
  AVG(execution_time) as avg_execution_time,
  SUM(total_cost) as total_cost
FROM public.pipelines
GROUP BY organization_id;
```

### Step 7: Setup Storage Buckets

```sql
-- Create storage buckets (run in SQL editor)
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES 
  ('articles', 'articles', true, 5242880, ARRAY[
    'image/jpeg', 'image/png', 'image/gif', 'image/webp', 'image/svg+xml'
  ]),
  ('organization-assets', 'organization-assets', true, 10485760, ARRAY[
    'image/jpeg', 'image/png', 'image/svg+xml'
  ]),
  ('exports', 'exports', false, 52428800, ARRAY[
    'application/pdf', 'text/csv', 'application/json', 'application/zip'
  ])
ON CONFLICT (id) DO NOTHING;
```

### Step 8: Storage Policies

```sql
-- Storage policies for articles
CREATE POLICY "Org users can upload article images" ON storage.objects
  FOR INSERT WITH CHECK (
    bucket_id = 'articles' 
    AND (storage.foldername(name))[1] = (
      SELECT organization_id::text 
      FROM public.profiles 
      WHERE id = auth.uid()
    )
  );

CREATE POLICY "Public can view article images" ON storage.objects
  FOR SELECT USING (bucket_id = 'articles');

CREATE POLICY "Org users can update article images" ON storage.objects
  FOR UPDATE USING (
    bucket_id = 'articles' 
    AND (storage.foldername(name))[1] = (
      SELECT organization_id::text 
      FROM public.profiles 
      WHERE id = auth.uid()
    )
  );

CREATE POLICY "Org users can delete article images" ON storage.objects
  FOR DELETE USING (
    bucket_id = 'articles' 
    AND (storage.foldername(name))[1] = (
      SELECT organization_id::text 
      FROM public.profiles 
      WHERE id = auth.uid()
    )
  );

-- Policies for organization assets
CREATE POLICY "Admins can manage org assets" ON storage.objects
  FOR ALL USING (
    bucket_id = 'organization-assets'
    AND EXISTS (
      SELECT 1 FROM public.profiles 
      WHERE id = auth.uid() 
      AND role IN ('owner', 'admin')
      AND organization_id::text = (storage.foldername(name))[1]
    )
  );

-- Policies for exports
CREATE POLICY "Users can access own exports" ON storage.objects
  FOR ALL USING (
    bucket_id = 'exports'
    AND auth.uid()::text = (storage.foldername(name))[1]
  );
```

### Step 9: Enable Realtime

```sql
-- Enable realtime for specific tables
ALTER PUBLICATION supabase_realtime ADD TABLE public.pipelines;
ALTER PUBLICATION supabase_realtime ADD TABLE public.articles;
ALTER PUBLICATION supabase_realtime ADD TABLE public.cost_tracking;
```

### Step 10: Create Helper Functions

```sql
-- Get system health function
CREATE OR REPLACE FUNCTION public.get_system_health()
RETURNS TABLE(
  metric TEXT,
  value NUMERIC,
  status TEXT,
  details JSONB
) 
SECURITY DEFINER
SET search_path = public, pg_catalog
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  WITH metrics AS (
    SELECT 
      'active_organizations' AS metric,
      COUNT(DISTINCT id)::numeric AS value,
      CASE 
        WHEN COUNT(DISTINCT id) > 0 THEN 'healthy'
        ELSE 'warning'
      END AS status,
      jsonb_build_object('count', COUNT(DISTINCT id)) AS details
    FROM public.organizations
    WHERE deleted_at IS NULL
    
    UNION ALL
    
    SELECT 
      'active_pipelines' AS metric,
      COUNT(*)::numeric AS value,
      CASE 
        WHEN COUNT(*) < 100 THEN 'healthy'
        WHEN COUNT(*) < 500 THEN 'warning'
        ELSE 'critical'
      END AS status,
      jsonb_build_object('count', COUNT(*)) AS details
    FROM public.pipelines
    WHERE status = 'running'
    
    UNION ALL
    
    SELECT 
      'failed_pipelines_24h' AS metric,
      COUNT(*)::numeric AS value,
      CASE 
        WHEN COUNT(*) < 5 THEN 'healthy'
        WHEN COUNT(*) < 20 THEN 'warning'
        ELSE 'critical'
      END AS status,
      jsonb_build_object('count', COUNT(*)) AS details
    FROM public.pipelines
    WHERE status = 'failed'
    AND created_at > NOW() - INTERVAL '24 hours'
  )
  SELECT * FROM metrics;
END;
$$;

-- Rate limit check function
CREATE OR REPLACE FUNCTION public.check_rate_limit(
  p_organization_id UUID,
  p_endpoint TEXT,
  p_method TEXT DEFAULT 'GET'
)
RETURNS BOOLEAN 
SECURITY DEFINER
SET search_path = public, pg_catalog
LANGUAGE plpgsql
AS $$
DECLARE
  v_current_count INTEGER;
  v_max_requests INTEGER;
BEGIN
  -- Get or create rate limit record
  INSERT INTO public.rate_limits (
    organization_id, endpoint, method, requests_count, max_requests
  )
  VALUES (
    p_organization_id, p_endpoint, p_method, 1, 100
  )
  ON CONFLICT (organization_id, endpoint, method, period_start) 
  DO UPDATE SET 
    requests_count = rate_limits.requests_count + 1
  RETURNING requests_count, max_requests 
  INTO v_current_count, v_max_requests;
  
  -- Check if limit exceeded
  IF v_current_count > v_max_requests THEN
    INSERT INTO audit.audit_log (
      organization_id, action, entity_type, entity_id, success, error_message
    )
    VALUES (
      p_organization_id, 'rate_limit.exceeded', 'api_endpoint', NULL, FALSE,
      format('Rate limit exceeded for %s %s: %s/%s', p_method, p_endpoint, v_current_count, v_max_requests)
    );
    RETURN FALSE;
  END IF;
  
  RETURN TRUE;
END;
$$;
```

## Final Verification

Run these queries to verify everything is set up correctly:

```sql
-- Check tables
SELECT table_name, 
       CASE WHEN row_security_enabled THEN '✅ RLS' ELSE '❌ No RLS' END AS security
FROM information_schema.tables t
JOIN pg_tables pt ON t.table_name = pt.tablename
WHERE t.table_schema = 'public'
ORDER BY table_name;

-- Check policies
SELECT tablename, COUNT(*) as policy_count
FROM pg_policies 
WHERE schemaname = 'public'
GROUP BY tablename
ORDER BY tablename;

-- Check functions
SELECT routine_name
FROM information_schema.routines 
WHERE routine_schema = 'public'
ORDER BY routine_name;

-- Check views
SELECT table_name
FROM information_schema.views
WHERE table_schema = 'public'
ORDER BY table_name;

-- Test health check
SELECT * FROM public.get_system_health();
```

### Step 8: Security Hardening Verification

```sql
-- Ensure all tables have RLS enabled
DO $$
DECLARE
    r RECORD;
BEGIN
    FOR r IN (
        SELECT tablename 
        FROM pg_tables 
        WHERE schemaname = 'public' 
        AND tablename NOT IN ('schema_migrations', 'supabase_functions_migrations')
        AND NOT rowsecurity
    ) LOOP
        EXECUTE format('ALTER TABLE public.%I ENABLE ROW LEVEL SECURITY', r.tablename);
        RAISE NOTICE 'Enabled RLS on table: %', r.tablename;
    END LOOP;
END $$;

-- Verify all functions have proper search_path
DO $$
DECLARE
    r RECORD;
BEGIN
    FOR r IN (
        SELECT proname 
        FROM pg_proc 
        WHERE pronamespace = 'public'::regnamespace
        AND prosecdef = true
        AND proconfig IS NULL OR NOT (proconfig @> ARRAY['search_path=public, pg_catalog'])
    ) LOOP
        RAISE WARNING 'Function % lacks proper search_path setting', r.proname;
    END LOOP;
END $$;

-- Create additional performance indexes
CREATE INDEX IF NOT EXISTS idx_profiles_organization_id ON public.profiles(organization_id);
CREATE INDEX IF NOT EXISTS idx_articles_organization_id ON public.articles(organization_id);
CREATE INDEX IF NOT EXISTS idx_pipelines_organization_id ON public.pipelines(organization_id);
CREATE INDEX IF NOT EXISTS idx_audit_log_organization_id ON audit.audit_log(organization_id);
CREATE INDEX IF NOT EXISTS idx_audit_log_created_at ON audit.audit_log(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_articles_status ON public.articles(status);
CREATE INDEX IF NOT EXISTS idx_pipelines_status ON public.pipelines(status);

-- Refresh database statistics for query optimization
ANALYZE;

-- Verification queries
-- Check all tables have RLS enabled
SELECT tablename, rowsecurity 
FROM pg_tables 
WHERE schemaname = 'public' 
AND tablename NOT IN ('schema_migrations', 'supabase_functions_migrations')
ORDER BY tablename;

-- Check views don't have SECURITY DEFINER
SELECT viewname 
FROM pg_views 
WHERE schemaname = 'public' 
AND definition LIKE '%SECURITY DEFINER%';

-- Check functions have proper search_path
SELECT proname, proconfig
FROM pg_proc 
WHERE pronamespace = 'public'::regnamespace
AND prosecdef = true;

-- Test organization data isolation
-- This should only return data for the current user's organization
SELECT * FROM public.organization_dashboard;
```

## 🎉 Setup Complete!

Your Supabase database is now fully configured with:
- ✅ All tables with proper relationships
- ✅ Row Level Security on all tables
- ✅ Automatic organization creation on signup
- ✅ Cost tracking and budget enforcement
- ✅ Audit logging
- ✅ Rate limiting
- ✅ Storage buckets with policies
- ✅ Realtime subscriptions
- ✅ Dashboard views for analytics
- ✅ Helper functions for operations

**Next Steps:**
1. Test by creating a user account
2. Verify organization and profile are created
3. Continue with the frontend implementation prompts
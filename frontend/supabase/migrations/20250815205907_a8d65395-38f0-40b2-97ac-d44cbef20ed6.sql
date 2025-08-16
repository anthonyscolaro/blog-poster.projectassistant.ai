-- Drop existing views with SECURITY DEFINER if they exist
DROP VIEW IF EXISTS public.organization_dashboard CASCADE;
DROP VIEW IF EXISTS public.user_costs CASCADE;
DROP VIEW IF EXISTS public.pipeline_analytics CASCADE;
DROP VIEW IF EXISTS public.article_performance CASCADE;
DROP VIEW IF EXISTS public.agent_metrics CASCADE;
DROP VIEW IF EXISTS public.team_activity CASCADE;

-- Recreate organization_dashboard WITHOUT SECURITY DEFINER
CREATE OR REPLACE VIEW public.organization_dashboard AS
SELECT 
    o.id,
    o.name,
    o.slug,
    o.plan,
    o.subscription_status,
    o.trial_ends_at,
    o.articles_limit,
    o.articles_used,
    o.monthly_budget,
    o.current_month_cost,
    ROUND((o.current_month_cost / NULLIF(o.monthly_budget, 0) * 100)::numeric, 2) AS budget_percentage,
    COUNT(DISTINCT p.id) FILTER (WHERE p.deleted_at IS NULL) as team_members,
    COUNT(DISTINCT a.id) FILTER (WHERE a.status = 'published' AND a.deleted_at IS NULL) as published_articles,
    COUNT(DISTINCT a.id) FILTER (WHERE a.status = 'draft' AND a.deleted_at IS NULL) as draft_articles,
    COUNT(DISTINCT pip.id) FILTER (WHERE pip.status = 'running') as active_pipelines,
    COUNT(DISTINCT pip.id) FILTER (WHERE pip.status = 'completed') as completed_pipelines
FROM public.organizations o
LEFT JOIN public.profiles p ON p.organization_id = o.id AND p.deleted_at IS NULL
LEFT JOIN public.articles a ON a.organization_id = o.id AND a.deleted_at IS NULL
LEFT JOIN public.pipelines pip ON pip.organization_id = o.id
WHERE o.deleted_at IS NULL
GROUP BY o.id, o.name, o.slug, o.plan, o.subscription_status, o.trial_ends_at, o.articles_limit, o.articles_used, o.monthly_budget, o.current_month_cost;

-- Recreate article_performance WITHOUT SECURITY DEFINER  
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

-- Recreate cost_analysis WITHOUT SECURITY DEFINER
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

-- Recreate recent_activity WITHOUT SECURITY DEFINER
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

-- Recreate article_stats WITHOUT SECURITY DEFINER
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

-- Recreate pipeline_stats WITHOUT SECURITY DEFINER
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

-- Create audit_logs table if it doesn't exist and enable RLS
CREATE TABLE IF NOT EXISTS public.audit_logs (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    organization_id UUID NOT NULL,
    user_id UUID,
    action TEXT NOT NULL,
    resource_type TEXT,
    resource_id UUID,
    details JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable RLS on audit_logs table
ALTER TABLE public.audit_logs ENABLE ROW LEVEL SECURITY;

-- Create RLS policies for audit_logs
CREATE POLICY "Users can view their organization's audit logs" ON public.audit_logs
    FOR SELECT USING (
        organization_id IN (
            SELECT organization_id FROM public.profiles 
            WHERE profiles.id = auth.uid()
        )
    );

CREATE POLICY "System can insert audit logs" ON public.audit_logs
    FOR INSERT WITH CHECK (true);

-- Only admins and owners can delete audit logs (for compliance)
CREATE POLICY "Admins can manage audit logs" ON public.audit_logs
    FOR DELETE USING (
        organization_id IN (
            SELECT organization_id FROM public.profiles 
            WHERE profiles.id = auth.uid() 
            AND profiles.role IN ('owner', 'admin')
        )
    );

-- Drop and recreate check_budget_limit with qualified search_path
DROP FUNCTION IF EXISTS public.check_budget_limit(UUID);

CREATE OR REPLACE FUNCTION public.check_budget_limit(
    p_organization_id UUID
)
RETURNS BOOLEAN
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public, pg_catalog
AS $$
DECLARE
    v_org RECORD;
    v_percentage DECIMAL;
BEGIN
    -- Get organization limits
    SELECT 
        monthly_budget, current_month_cost, budget_alert_threshold,
        articles_limit, articles_used, plan
    INTO v_org
    FROM public.organizations
    WHERE id = p_organization_id;
    
    IF NOT FOUND THEN
        RETURN FALSE;
    END IF;
    
    -- Check article limit
    IF v_org.articles_used >= v_org.articles_limit THEN
        INSERT INTO public.audit_logs (
            organization_id, action, resource_type, resource_id, details
        )
        VALUES (
            p_organization_id, 'budget.article_limit_exceeded', 'organization',
            p_organization_id,
            jsonb_build_object('articles_used', v_org.articles_used, 'articles_limit', v_org.articles_limit)
        );
        RETURN FALSE;
    END IF;
    
    -- Check budget limit
    IF v_org.current_month_cost >= v_org.monthly_budget THEN
        INSERT INTO public.audit_logs (
            organization_id, action, resource_type, resource_id, details
        )
        VALUES (
            p_organization_id, 'budget.monthly_limit_exceeded', 'organization',
            p_organization_id,
            jsonb_build_object('current_cost', v_org.current_month_cost, 'monthly_budget', v_org.monthly_budget)
        );
        RETURN FALSE;
    END IF;
    
    -- Check alert threshold
    v_percentage := (v_org.current_month_cost / v_org.monthly_budget * 100);
    IF v_percentage >= v_org.budget_alert_threshold THEN
        INSERT INTO public.audit_logs (
            organization_id, action, resource_type, resource_id, details
        )
        VALUES (
            p_organization_id, 'budget.threshold_alert', 'organization', p_organization_id,
            jsonb_build_object('percentage', v_percentage, 'threshold', v_org.budget_alert_threshold)
        );
    END IF;
    
    RETURN TRUE;
END;
$$;

-- Drop and recreate get_system_health with fixed column reference
DROP FUNCTION IF EXISTS public.get_system_health();

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
      COUNT(DISTINCT o.id)::numeric AS value,
      CASE 
        WHEN COUNT(DISTINCT o.id) > 0 THEN 'healthy'
        ELSE 'warning'
      END AS status,
      jsonb_build_object('count', COUNT(DISTINCT o.id)) AS details
    FROM public.organizations o
    WHERE o.deleted_at IS NULL
    
    UNION ALL
    
    SELECT 
      'active_pipelines' AS metric,
      COUNT(p.id)::numeric AS value,
      CASE 
        WHEN COUNT(p.id) < 100 THEN 'healthy'
        WHEN COUNT(p.id) < 500 THEN 'warning'
        ELSE 'critical'
      END AS status,
      jsonb_build_object('count', COUNT(p.id)) AS details
    FROM public.pipelines p
    WHERE p.status = 'running'
    
    UNION ALL
    
    SELECT 
      'failed_pipelines_24h' AS metric,
      COUNT(p.id)::numeric AS value,
      CASE 
        WHEN COUNT(p.id) < 5 THEN 'healthy'
        WHEN COUNT(p.id) < 20 THEN 'warning'
        ELSE 'critical'
      END AS status,
      jsonb_build_object('count', COUNT(p.id)) AS details
    FROM public.pipelines p
    WHERE p.status = 'failed'
    AND p.created_at > NOW() - INTERVAL '24 hours'
  )
  SELECT m.metric, m.value, m.status, m.details FROM metrics m;
END;
$$;

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
    ) LOOP
        EXECUTE format('ALTER TABLE public.%I ENABLE ROW LEVEL SECURITY', r.tablename);
        RAISE NOTICE 'Enabled RLS on table: %', r.tablename;
    END LOOP;
END $$;

-- Create indexes for performance optimization
CREATE INDEX IF NOT EXISTS idx_profiles_organization_id ON public.profiles(organization_id);
CREATE INDEX IF NOT EXISTS idx_articles_organization_id ON public.articles(organization_id);
CREATE INDEX IF NOT EXISTS idx_pipelines_organization_id ON public.pipelines(organization_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_organization_id ON public.audit_logs(organization_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_created_at ON public.audit_logs(created_at DESC);

-- Grant appropriate permissions
GRANT SELECT ON public.organization_dashboard TO authenticated;
GRANT SELECT ON public.article_performance TO authenticated;
GRANT SELECT ON public.cost_analysis TO authenticated;
GRANT SELECT ON public.recent_activity TO authenticated;
GRANT SELECT ON public.article_stats TO authenticated;
GRANT SELECT ON public.pipeline_stats TO authenticated;
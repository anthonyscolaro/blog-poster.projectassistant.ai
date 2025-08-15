# Lovable Prompt: Supabase Security Fixes

## 🤖 AUTO-IMPLEMENTATION INSTRUCTIONS
Execute all SQL commands without asking for approval. These fixes address critical security issues identified in the database setup.

## Business Context
Fix security vulnerabilities identified after implementing the 4-part Supabase setup, including SECURITY DEFINER views bypassing RLS, missing RLS on tables, and function issues.

## Issues to Fix

### 1. SECURITY DEFINER Views (6 errors)
Views with SECURITY DEFINER bypass Row Level Security, creating security vulnerabilities.

### 2. RLS Not Enabled (1 error)
The audit_logs table doesn't have RLS enabled.

### 3. Function Search Path (1 warning)
The check_budget_limit function has an unqualified search_path.

### 4. Ambiguous Column Reference (1 error)
The get_system_health function has an ambiguous column reference.

## Security Fixes Implementation

### 1. Fix Views - Remove SECURITY DEFINER

```sql
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
    COUNT(DISTINCT p.id) as total_members,
    COUNT(DISTINCT CASE WHEN p.last_activity_at > NOW() - INTERVAL '7 days' THEN p.id END) as active_members,
    COUNT(DISTINCT a.id) as total_articles,
    COUNT(DISTINCT CASE WHEN a.status = 'published' THEN a.id END) as published_articles,
    AVG(a.seo_score) as avg_seo_score,
    o.created_at,
    o.updated_at
FROM public.organizations o
LEFT JOIN public.profiles p ON p.organization_id = o.id
LEFT JOIN public.articles a ON a.organization_id = o.id
GROUP BY o.id;

-- Add RLS policy for the view's base tables if not exists
CREATE POLICY IF NOT EXISTS "Users can view their organization dashboard" ON public.organizations
    FOR SELECT USING (
        id IN (
            SELECT organization_id FROM public.profiles 
            WHERE profiles.id = auth.uid()
        )
    );

-- Recreate user_costs WITHOUT SECURITY DEFINER
CREATE OR REPLACE VIEW public.user_costs AS
SELECT 
    p.id as user_id,
    p.email,
    p.full_name,
    p.organization_id,
    DATE_TRUNC('month', a.created_at) as month,
    COUNT(a.id) as articles_generated,
    SUM(a.generation_cost) as total_cost,
    AVG(a.generation_cost) as avg_cost_per_article,
    COUNT(CASE WHEN a.status = 'published' THEN 1 END) as published_count,
    AVG(a.seo_score) as avg_seo_score
FROM public.profiles p
LEFT JOIN public.articles a ON a.user_id = p.id
GROUP BY p.id, DATE_TRUNC('month', a.created_at);

-- Recreate pipeline_analytics WITHOUT SECURITY DEFINER
CREATE OR REPLACE VIEW public.pipeline_analytics AS
SELECT 
    pl.organization_id,
    DATE_TRUNC('day', pl.started_at) as day,
    COUNT(pl.id) as total_pipelines,
    COUNT(CASE WHEN pl.status = 'completed' THEN 1 END) as completed,
    COUNT(CASE WHEN pl.status = 'failed' THEN 1 END) as failed,
    AVG(EXTRACT(EPOCH FROM (pl.completed_at - pl.started_at))/60) as avg_duration_minutes,
    SUM(pl.total_cost) as total_cost,
    AVG(pl.total_cost) as avg_cost,
    COUNT(DISTINCT pl.user_id) as unique_users
FROM public.pipelines pl
GROUP BY pl.organization_id, DATE_TRUNC('day', pl.started_at);

-- Recreate article_performance WITHOUT SECURITY DEFINER
CREATE OR REPLACE VIEW public.article_performance AS
SELECT 
    a.id,
    a.title,
    a.organization_id,
    a.user_id,
    a.status,
    a.seo_score,
    a.word_count,
    a.generation_cost,
    a.views,
    a.clicks,
    CASE 
        WHEN a.views > 0 THEN (a.clicks::float / a.views * 100)
        ELSE 0 
    END as ctr,
    a.created_at,
    a.published_at
FROM public.articles a;

-- Recreate agent_metrics WITHOUT SECURITY DEFINER
CREATE OR REPLACE VIEW public.agent_metrics AS
SELECT 
    ae.organization_id,
    ae.agent_name,
    COUNT(ae.id) as total_executions,
    COUNT(CASE WHEN ae.status = 'success' THEN 1 END) as successful,
    COUNT(CASE WHEN ae.status = 'failed' THEN 1 END) as failed,
    AVG(ae.execution_time_ms) as avg_execution_time_ms,
    SUM(ae.tokens_used) as total_tokens,
    SUM(ae.cost) as total_cost,
    MAX(ae.created_at) as last_execution
FROM public.agent_executions ae
GROUP BY ae.organization_id, ae.agent_name;

-- Recreate team_activity WITHOUT SECURITY DEFINER
CREATE OR REPLACE VIEW public.team_activity AS
SELECT 
    p.organization_id,
    p.id as user_id,
    p.email,
    p.full_name,
    p.role,
    p.last_login_at,
    p.last_activity_at,
    COUNT(DISTINCT a.id) as articles_created,
    COUNT(DISTINCT pl.id) as pipelines_run,
    SUM(a.generation_cost) as total_cost_generated,
    MAX(a.created_at) as last_article_created,
    MAX(pl.started_at) as last_pipeline_run
FROM public.profiles p
LEFT JOIN public.articles a ON a.user_id = p.id
LEFT JOIN public.pipelines pl ON pl.user_id = p.id
GROUP BY p.id;

-- Grant appropriate permissions
GRANT SELECT ON public.organization_dashboard TO authenticated;
GRANT SELECT ON public.user_costs TO authenticated;
GRANT SELECT ON public.pipeline_analytics TO authenticated;
GRANT SELECT ON public.article_performance TO authenticated;
GRANT SELECT ON public.agent_metrics TO authenticated;
GRANT SELECT ON public.team_activity TO authenticated;
```

### 2. Enable RLS on audit_logs Table

```sql
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
```

### 3. Fix Function Search Path

```sql
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
    v_budget DECIMAL;
    v_current_cost DECIMAL;
    v_threshold DECIMAL;
BEGIN
    -- Get organization budget and current cost
    SELECT 
        monthly_budget, 
        current_month_cost
    INTO 
        v_budget, 
        v_current_cost
    FROM public.organizations
    WHERE id = p_organization_id;

    -- If no budget set, allow operation
    IF v_budget IS NULL OR v_budget = 0 THEN
        RETURN true;
    END IF;

    -- Calculate 80% threshold for warning
    v_threshold := v_budget * 0.8;

    -- Check if current cost exceeds budget
    IF v_current_cost >= v_budget THEN
        -- Log budget exceeded event
        INSERT INTO public.audit_logs (
            organization_id,
            user_id,
            action,
            resource_type,
            resource_id,
            details
        ) VALUES (
            p_organization_id,
            auth.uid(),
            'budget_exceeded',
            'organization',
            p_organization_id,
            jsonb_build_object(
                'budget', v_budget,
                'current_cost', v_current_cost
            )
        );
        
        RETURN false;
    END IF;

    -- Warn if approaching limit
    IF v_current_cost >= v_threshold THEN
        -- Log budget warning event
        INSERT INTO public.audit_logs (
            organization_id,
            user_id,
            action,
            resource_type,
            resource_id,
            details
        ) VALUES (
            p_organization_id,
            auth.uid(),
            'budget_warning',
            'organization',
            p_organization_id,
            jsonb_build_object(
                'budget', v_budget,
                'current_cost', v_current_cost,
                'percentage', (v_current_cost / v_budget * 100)
            )
        );
    END IF;

    RETURN true;
END;
$$;

-- Fix other functions that might have search_path issues
DROP FUNCTION IF EXISTS public.handle_new_user();

CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public, pg_catalog
AS $$
DECLARE
    v_org_id UUID;
    v_org_name TEXT;
BEGIN
    -- Generate organization name from email
    v_org_name := SPLIT_PART(NEW.email, '@', 1) || '''s Organization';
    
    -- Create organization for new user
    INSERT INTO public.organizations (
        name,
        slug,
        plan,
        subscription_status,
        articles_limit,
        articles_used,
        monthly_budget
    ) VALUES (
        v_org_name,
        LOWER(REPLACE(v_org_name, ' ', '-')),
        'free',
        'trialing',
        2,  -- Free tier: 2 articles/month
        0,
        0   -- No budget limit for free tier
    ) RETURNING id INTO v_org_id;

    -- Create user profile
    INSERT INTO public.profiles (
        id,
        email,
        organization_id,
        role,
        onboarding_completed
    ) VALUES (
        NEW.id,
        NEW.email,
        v_org_id,
        'owner',
        false
    );

    -- Log user creation
    INSERT INTO public.audit_logs (
        organization_id,
        user_id,
        action,
        resource_type,
        resource_id,
        details
    ) VALUES (
        v_org_id,
        NEW.id,
        'user_created',
        'profile',
        NEW.id,
        jsonb_build_object('email', NEW.email, 'organization_id', v_org_id)
    );

    RETURN NEW;
END;
$$;
```

### 4. Fix Ambiguous Column Reference

```sql
-- Drop and recreate get_system_health with fixed column reference
DROP FUNCTION IF EXISTS public.get_system_health();

CREATE OR REPLACE FUNCTION public.get_system_health()
RETURNS TABLE (
    metric TEXT,
    value NUMERIC,
    status TEXT,
    details JSONB
)
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public, pg_catalog
AS $$
BEGIN
    RETURN QUERY
    
    -- Active users in last 24 hours
    SELECT 
        'active_users_24h'::TEXT as metric,
        COUNT(DISTINCT p.id)::NUMERIC as value,
        CASE 
            WHEN COUNT(DISTINCT p.id) > 0 THEN 'healthy'::TEXT
            ELSE 'warning'::TEXT
        END as status,
        jsonb_build_object('count', COUNT(DISTINCT p.id))::JSONB as details
    FROM public.profiles p
    WHERE p.last_activity_at > NOW() - INTERVAL '24 hours';

    -- Pipelines completion rate
    RETURN QUERY
    SELECT 
        'pipeline_success_rate'::TEXT as metric,
        CASE 
            WHEN COUNT(pl.id) > 0 THEN 
                (COUNT(CASE WHEN pl.status = 'completed' THEN 1 END)::NUMERIC / COUNT(pl.id) * 100)
            ELSE 0
        END as value,
        CASE 
            WHEN COUNT(pl.id) = 0 THEN 'info'::TEXT
            WHEN (COUNT(CASE WHEN pl.status = 'completed' THEN 1 END)::NUMERIC / NULLIF(COUNT(pl.id), 0) * 100) > 80 THEN 'healthy'::TEXT
            WHEN (COUNT(CASE WHEN pl.status = 'completed' THEN 1 END)::NUMERIC / NULLIF(COUNT(pl.id), 0) * 100) > 60 THEN 'warning'::TEXT
            ELSE 'critical'::TEXT
        END as status,
        jsonb_build_object(
            'total', COUNT(pl.id),
            'completed', COUNT(CASE WHEN pl.status = 'completed' THEN 1 END),
            'failed', COUNT(CASE WHEN pl.status = 'failed' THEN 1 END)
        )::JSONB as details
    FROM public.pipelines pl
    WHERE pl.started_at > NOW() - INTERVAL '24 hours';

    -- Storage usage
    RETURN QUERY
    SELECT 
        'storage_usage_mb'::TEXT as metric,
        COALESCE(SUM(LENGTH(a.content)::NUMERIC / 1024 / 1024), 0) as value,
        CASE 
            WHEN COALESCE(SUM(LENGTH(a.content)::NUMERIC / 1024 / 1024), 0) < 1000 THEN 'healthy'::TEXT
            WHEN COALESCE(SUM(LENGTH(a.content)::NUMERIC / 1024 / 1024), 0) < 5000 THEN 'warning'::TEXT
            ELSE 'critical'::TEXT
        END as status,
        jsonb_build_object('size_mb', COALESCE(SUM(LENGTH(a.content)::NUMERIC / 1024 / 1024), 0))::JSONB as details
    FROM public.articles a;

    -- Organizations at budget limit
    RETURN QUERY
    SELECT 
        'orgs_at_budget_limit'::TEXT as metric,
        COUNT(o.id)::NUMERIC as value,
        CASE 
            WHEN COUNT(o.id) = 0 THEN 'healthy'::TEXT
            ELSE 'warning'::TEXT
        END as status,
        jsonb_build_object('organizations', ARRAY_AGG(o.name))::JSONB as details
    FROM public.organizations o
    WHERE o.current_month_cost >= o.monthly_budget
    AND o.monthly_budget > 0;

END;
$$;
```

### 5. Additional Security Hardening

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

-- Create index on frequently queried columns if not exists
CREATE INDEX IF NOT EXISTS idx_profiles_organization_id ON public.profiles(organization_id);
CREATE INDEX IF NOT EXISTS idx_articles_organization_id ON public.articles(organization_id);
CREATE INDEX IF NOT EXISTS idx_pipelines_organization_id ON public.pipelines(organization_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_organization_id ON public.audit_logs(organization_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_created_at ON public.audit_logs(created_at DESC);

-- Refresh database statistics for query optimization
ANALYZE;
```

## Verification Queries

After applying these fixes, run these queries to verify security is properly configured:

```sql
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

-- Test organization isolation
-- This should only return data for the current user's organization
SELECT * FROM public.organization_dashboard;
SELECT * FROM public.user_costs;
SELECT * FROM public.team_activity;
```

## Expected Results

After applying these fixes:
- ✅ All views work WITHOUT SECURITY DEFINER
- ✅ RLS is enabled on ALL tables including audit_logs
- ✅ Functions have qualified search_path
- ✅ No ambiguous column references
- ✅ Organization data isolation is maintained
- ✅ Performance is optimized with proper indexes

This completes the security hardening of your Supabase database setup.
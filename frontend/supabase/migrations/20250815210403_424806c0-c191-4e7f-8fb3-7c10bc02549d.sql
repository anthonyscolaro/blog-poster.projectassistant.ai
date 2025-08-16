-- Drop all triggers that depend on functions we need to update
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
DROP TRIGGER IF EXISTS update_org_monthly_cost ON public.cost_tracking;
DROP TRIGGER IF EXISTS initialize_org_defaults ON public.organizations;
DROP TRIGGER IF EXISTS update_articles_updated_at ON public.articles;
DROP TRIGGER IF EXISTS update_profiles_updated_at ON public.profiles;
DROP TRIGGER IF EXISTS update_organizations_updated_at ON public.organizations;

-- Now drop functions
DROP FUNCTION IF EXISTS public.handle_new_user() CASCADE;
DROP FUNCTION IF EXISTS public.check_rate_limit(UUID, TEXT, TEXT) CASCADE;
DROP FUNCTION IF EXISTS public.update_monthly_cost() CASCADE;
DROP FUNCTION IF EXISTS public.initialize_organization_defaults() CASCADE;

-- Recreate all functions with proper search_path
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public, pg_catalog
AS $$
DECLARE
    v_org_id UUID;
    v_org_name TEXT;
    v_org_slug TEXT;
    v_counter INTEGER := 0;
BEGIN
    -- Generate organization name
    v_org_name := COALESCE(
        NEW.raw_user_meta_data->>'company',
        NEW.raw_user_meta_data->>'organization',
        SPLIT_PART(NEW.email, '@', 1) || '''s Organization'
    );
    
    -- Generate unique slug
    v_org_slug := LOWER(REGEXP_REPLACE(v_org_name, '[^a-z0-9]+', '-', 'g'));
    v_org_slug := TRIM(BOTH '-' FROM v_org_slug);
    
    -- Ensure slug uniqueness
    WHILE EXISTS (SELECT 1 FROM public.organizations WHERE slug = v_org_slug) LOOP
        v_counter := v_counter + 1;
        v_org_slug := v_org_slug || '-' || v_counter;
    END LOOP;
    
    -- Create organization
    INSERT INTO public.organizations (
        name, slug, contact_email, billing_email, trial_ends_at
    )
    VALUES (
        v_org_name, v_org_slug, NEW.email, NEW.email,
        NOW() + INTERVAL '14 days'
    )
    RETURNING id INTO v_org_id;
    
    -- Create profile
    INSERT INTO public.profiles (
        id, organization_id, email, full_name, role, avatar_url
    )
    VALUES (
        NEW.id, v_org_id, NEW.email,
        COALESCE(NEW.raw_user_meta_data->>'full_name', SPLIT_PART(NEW.email, '@', 1)),
        'owner',
        NEW.raw_user_meta_data->>'avatar_url'
    );
    
    RETURN NEW;
EXCEPTION WHEN OTHERS THEN
    RAISE WARNING 'Error in handle_new_user: %', SQLERRM;
    RETURN NEW;
END;
$$;

CREATE OR REPLACE FUNCTION public.check_rate_limit(
    p_organization_id UUID,
    p_endpoint TEXT,
    p_method TEXT DEFAULT 'GET'
)
RETURNS BOOLEAN
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public, pg_catalog
AS $$
DECLARE
    v_current_count INTEGER;
    v_max_requests INTEGER;
BEGIN
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
    
    IF v_current_count > v_max_requests THEN
        RETURN FALSE;
    END IF;
    
    RETURN TRUE;
END;
$$;

CREATE OR REPLACE FUNCTION public.update_monthly_cost()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public, pg_catalog
AS $$
BEGIN
    UPDATE public.organizations
    SET 
        current_month_cost = (
            SELECT COALESCE(SUM(amount), 0)
            FROM public.cost_tracking
            WHERE organization_id = NEW.organization_id
            AND billing_month = DATE_TRUNC('month', CURRENT_DATE)
        ),
        articles_used = (
            SELECT COUNT(*)
            FROM public.articles
            WHERE organization_id = NEW.organization_id
            AND DATE_TRUNC('month', created_at) = DATE_TRUNC('month', CURRENT_DATE)
            AND deleted_at IS NULL
        )
    WHERE id = NEW.organization_id;
    
    RETURN NEW;
END;
$$;

CREATE OR REPLACE FUNCTION public.initialize_organization_defaults()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public, pg_catalog
AS $$
BEGIN
    INSERT INTO public.agent_configs (organization_id, agent_name, config)
    SELECT 
        NEW.id,
        agent_name,
        jsonb_build_object(
            'enabled', true,
            'max_retries', 3,
            'timeout', 300,
            'model', CASE 
                WHEN agent_name = 'article' THEN 'claude-3-5-sonnet-20241022'
                ELSE 'gpt-4-turbo-preview'
            END
        )
    FROM (VALUES 
        ('competitor'),
        ('topic'),
        ('article'),
        ('legal'),
        ('wordpress')
    ) AS agents(agent_name);
    
    RETURN NEW;
END;
$$;

-- Recreate all triggers
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

CREATE TRIGGER update_org_monthly_cost
  AFTER INSERT ON public.cost_tracking
  FOR EACH ROW EXECUTE FUNCTION public.update_monthly_cost();

CREATE TRIGGER initialize_org_defaults
  AFTER INSERT ON public.organizations
  FOR EACH ROW EXECUTE FUNCTION public.initialize_organization_defaults();

CREATE TRIGGER update_articles_updated_at
  BEFORE UPDATE ON public.articles
  FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();

CREATE TRIGGER update_profiles_updated_at
  BEFORE UPDATE ON public.profiles
  FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();

CREATE TRIGGER update_organizations_updated_at
  BEFORE UPDATE ON public.organizations
  FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();
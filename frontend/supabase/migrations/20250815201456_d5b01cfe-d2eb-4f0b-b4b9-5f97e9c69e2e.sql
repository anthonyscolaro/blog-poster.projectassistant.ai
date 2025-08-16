-- Part 3: Row Level Security Policies and Functions

-- Step 1: Organizations RLS Policies
CREATE POLICY "Users can view their organization" ON public.organizations
  FOR SELECT USING (
    id IN (
      SELECT organization_id FROM public.profiles 
      WHERE profiles.id = auth.uid()
    )
  );

CREATE POLICY "Organization owners can update" ON public.organizations
  FOR UPDATE USING (
    id IN (
      SELECT organization_id FROM public.profiles 
      WHERE profiles.id = auth.uid() AND role = 'owner'
    )
  );

-- Step 2: Profiles RLS Policies
CREATE POLICY "Users can view profiles in their org" ON public.profiles
  FOR SELECT USING (
    organization_id IN (
      SELECT organization_id FROM public.profiles p2
      WHERE p2.id = auth.uid()
    )
  );

CREATE POLICY "Users can update own profile" ON public.profiles
  FOR UPDATE USING (id = auth.uid());

CREATE POLICY "Users can insert own profile" ON public.profiles
  FOR INSERT WITH CHECK (id = auth.uid());

-- Step 3: Articles RLS Policies
CREATE POLICY "Users can view org articles" ON public.articles
  FOR SELECT USING (
    organization_id = (
      SELECT organization_id FROM public.profiles 
      WHERE profiles.id = auth.uid()
    )
  );

CREATE POLICY "Users can create articles" ON public.articles
  FOR INSERT WITH CHECK (
    organization_id = (
      SELECT organization_id FROM public.profiles 
      WHERE profiles.id = auth.uid()
    )
    AND user_id = auth.uid()
  );

CREATE POLICY "Users can update org articles" ON public.articles
  FOR UPDATE USING (
    organization_id = (
      SELECT organization_id FROM public.profiles 
      WHERE profiles.id = auth.uid()
    )
    AND (
      user_id = auth.uid() 
      OR EXISTS (
        SELECT 1 FROM public.profiles 
        WHERE profiles.id = auth.uid() 
        AND role IN ('owner', 'admin', 'editor')
      )
    )
  );

CREATE POLICY "Article authors can delete" ON public.articles
  FOR DELETE USING (
    user_id = auth.uid()
    OR EXISTS (
      SELECT 1 FROM public.profiles 
      WHERE profiles.id = auth.uid() 
      AND profiles.organization_id = articles.organization_id
      AND role IN ('owner', 'admin')
    )
  );

-- Step 4: Pipeline RLS Policies
CREATE POLICY "Users can view org pipelines" ON public.pipelines
  FOR SELECT USING (
    organization_id = (
      SELECT organization_id FROM public.profiles 
      WHERE profiles.id = auth.uid()
    )
  );

CREATE POLICY "Users can create pipelines" ON public.pipelines
  FOR INSERT WITH CHECK (
    organization_id = (
      SELECT organization_id FROM public.profiles 
      WHERE profiles.id = auth.uid()
    )
    AND user_id = auth.uid()
  );

CREATE POLICY "Users can update own pipelines" ON public.pipelines
  FOR UPDATE USING (
    user_id = auth.uid()
    OR EXISTS (
      SELECT 1 FROM public.profiles 
      WHERE profiles.id = auth.uid() 
      AND profiles.organization_id = pipelines.organization_id
      AND role IN ('owner', 'admin')
    )
  );

-- Step 5: Other Table RLS Policies
-- API Keys policies
CREATE POLICY "Admins can view org API keys" ON public.organization_api_keys
  FOR SELECT USING (
    organization_id IN (
      SELECT organization_id FROM public.profiles 
      WHERE profiles.id = auth.uid() AND role IN ('owner', 'admin')
    )
  );

CREATE POLICY "Admins can manage org API keys" ON public.organization_api_keys
  FOR ALL USING (
    organization_id IN (
      SELECT organization_id FROM public.profiles 
      WHERE profiles.id = auth.uid() AND role IN ('owner', 'admin')
    )
  );

-- Agent configs policies
CREATE POLICY "Users can view org agent configs" ON public.agent_configs
  FOR SELECT USING (
    organization_id = (
      SELECT organization_id FROM public.profiles 
      WHERE profiles.id = auth.uid()
    )
  );

CREATE POLICY "Admins can manage agent configs" ON public.agent_configs
  FOR ALL USING (
    organization_id IN (
      SELECT organization_id FROM public.profiles 
      WHERE profiles.id = auth.uid() AND role IN ('owner', 'admin')
    )
  );

-- Competitors policies
CREATE POLICY "Users can view org competitors" ON public.competitors
  FOR SELECT USING (
    organization_id = (
      SELECT organization_id FROM public.profiles 
      WHERE profiles.id = auth.uid()
    )
  );

CREATE POLICY "Admins can manage competitors" ON public.competitors
  FOR ALL USING (
    organization_id IN (
      SELECT organization_id FROM public.profiles 
      WHERE profiles.id = auth.uid() AND role IN ('owner', 'admin')
    )
  );

-- Topics policies
CREATE POLICY "Users can view org topics" ON public.topics
  FOR SELECT USING (
    organization_id = (
      SELECT organization_id FROM public.profiles 
      WHERE profiles.id = auth.uid()
    )
  );

CREATE POLICY "Editors can manage topics" ON public.topics
  FOR ALL USING (
    organization_id IN (
      SELECT organization_id FROM public.profiles 
      WHERE profiles.id = auth.uid() AND role IN ('owner', 'admin', 'editor')
    )
  );

-- Cost tracking policies
CREATE POLICY "Users can view org costs" ON public.cost_tracking
  FOR SELECT USING (
    organization_id = (
      SELECT organization_id FROM public.profiles 
      WHERE profiles.id = auth.uid()
    )
  );

CREATE POLICY "System can insert costs" ON public.cost_tracking
  FOR INSERT WITH CHECK (
    organization_id = (
      SELECT organization_id FROM public.profiles 
      WHERE profiles.id = auth.uid()
    )
  );

-- Webhook logs policies
CREATE POLICY "Users can view org webhooks" ON public.webhook_logs
  FOR SELECT USING (
    organization_id = (
      SELECT organization_id FROM public.profiles 
      WHERE profiles.id = auth.uid()
    )
  );

-- Invitations policies
CREATE POLICY "Admins can manage invitations" ON public.invitations
  FOR ALL USING (
    organization_id IN (
      SELECT organization_id FROM public.profiles 
      WHERE profiles.id = auth.uid() AND role IN ('owner', 'admin')
    )
  );

CREATE POLICY "Users can view own invitations" ON public.invitations
  FOR SELECT USING (
    email = (SELECT email FROM public.profiles WHERE id = auth.uid())
  );

-- Audit log policies
CREATE POLICY "Users can view org audit logs" ON audit.audit_log
  FOR SELECT USING (
    organization_id = (
      SELECT organization_id FROM public.profiles 
      WHERE profiles.id = auth.uid()
    )
  );

-- Rate limits policies
CREATE POLICY "System can manage rate limits" ON public.rate_limits
  FOR ALL USING (
    organization_id = (
      SELECT organization_id FROM public.profiles 
      WHERE profiles.id = auth.uid()
    )
  );

-- Step 6: Create User Signup Handler Function
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER 
SECURITY DEFINER
SET search_path = public
LANGUAGE plpgsql
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
  
  -- Log signup
  INSERT INTO audit.audit_log (
    organization_id, user_id, action, entity_type, entity_id, new_values
  )
  VALUES (
    v_org_id, NEW.id, 'user.signup', 'organization', v_org_id,
    jsonb_build_object('organization_name', v_org_name, 'plan', 'free')
  );
  
  RETURN NEW;
EXCEPTION WHEN OTHERS THEN
  RAISE WARNING 'Error in handle_new_user: %', SQLERRM;
  RETURN NEW;
END;
$$;

-- Create trigger
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- Step 7: Create Update Timestamp Function
CREATE OR REPLACE FUNCTION public.update_updated_at()
RETURNS TRIGGER 
LANGUAGE plpgsql
AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$;

-- Add triggers to tables with updated_at
CREATE TRIGGER update_organizations_updated_at BEFORE UPDATE ON public.organizations
  FOR EACH ROW EXECUTE FUNCTION public.update_updated_at();

CREATE TRIGGER update_profiles_updated_at BEFORE UPDATE ON public.profiles
  FOR EACH ROW EXECUTE FUNCTION public.update_updated_at();

CREATE TRIGGER update_articles_updated_at BEFORE UPDATE ON public.articles
  FOR EACH ROW EXECUTE FUNCTION public.update_updated_at();

CREATE TRIGGER update_agent_configs_updated_at BEFORE UPDATE ON public.agent_configs
  FOR EACH ROW EXECUTE FUNCTION public.update_updated_at();

CREATE TRIGGER update_competitors_updated_at BEFORE UPDATE ON public.competitors
  FOR EACH ROW EXECUTE FUNCTION public.update_updated_at();

CREATE TRIGGER update_organization_api_keys_updated_at BEFORE UPDATE ON public.organization_api_keys
  FOR EACH ROW EXECUTE FUNCTION public.update_updated_at();

-- Step 8: Create Budget Check Function
CREATE OR REPLACE FUNCTION public.check_budget_limit(p_organization_id UUID)
RETURNS BOOLEAN 
SECURITY DEFINER
SET search_path = public
LANGUAGE plpgsql
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
    INSERT INTO audit.audit_log (
      organization_id, action, entity_type, entity_id, success, error_message
    )
    VALUES (
      p_organization_id, 'budget.article_limit_exceeded', 'organization',
      p_organization_id, FALSE,
      format('Article limit reached: %s/%s', v_org.articles_used, v_org.articles_limit)
    );
    RETURN FALSE;
  END IF;
  
  -- Check budget limit
  IF v_org.current_month_cost >= v_org.monthly_budget THEN
    INSERT INTO audit.audit_log (
      organization_id, action, entity_type, entity_id, success, error_message
    )
    VALUES (
      p_organization_id, 'budget.monthly_limit_exceeded', 'organization',
      p_organization_id, FALSE,
      format('Budget exceeded: $%s/$%s', v_org.current_month_cost, v_org.monthly_budget)
    );
    RETURN FALSE;
  END IF;
  
  -- Check alert threshold
  v_percentage := (v_org.current_month_cost / v_org.monthly_budget * 100);
  IF v_percentage >= v_org.budget_alert_threshold THEN
    INSERT INTO audit.audit_log (
      organization_id, action, entity_type, entity_id, new_values
    )
    VALUES (
      p_organization_id, 'budget.threshold_alert', 'organization', p_organization_id,
      jsonb_build_object('percentage', v_percentage, 'threshold', v_org.budget_alert_threshold)
    );
  END IF;
  
  RETURN TRUE;
END;
$$;

-- Step 9: Create Cost Update Function
CREATE OR REPLACE FUNCTION public.update_monthly_cost()
RETURNS TRIGGER 
SECURITY DEFINER
SET search_path = public
LANGUAGE plpgsql
AS $$
BEGIN
  -- Update organization monthly cost and article count
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

-- Create trigger
DROP TRIGGER IF EXISTS update_org_monthly_cost ON public.cost_tracking;
CREATE TRIGGER update_org_monthly_cost
  AFTER INSERT OR UPDATE ON public.cost_tracking
  FOR EACH ROW EXECUTE FUNCTION public.update_monthly_cost();

-- Step 10: Create Organization Defaults Function
CREATE OR REPLACE FUNCTION public.initialize_organization_defaults()
RETURNS TRIGGER 
SECURITY DEFINER
SET search_path = public
LANGUAGE plpgsql
AS $$
BEGIN
  -- Insert default agent configurations
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

-- Create trigger
DROP TRIGGER IF EXISTS initialize_org_defaults ON public.organizations;
CREATE TRIGGER initialize_org_defaults
  AFTER INSERT ON public.organizations
  FOR EACH ROW EXECUTE FUNCTION public.initialize_organization_defaults();
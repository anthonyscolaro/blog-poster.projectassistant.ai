-- RPC Functions for Supabase Integration
-- Run these in your Supabase SQL editor

-- Function to check if organization is within budget limit
CREATE OR REPLACE FUNCTION check_budget_limit(p_organization_id UUID)
RETURNS BOOLEAN AS $$
DECLARE
  v_monthly_budget DECIMAL;
  v_current_cost DECIMAL;
BEGIN
  SELECT monthly_budget, current_month_cost
  INTO v_monthly_budget, v_current_cost
  FROM organizations
  WHERE id = p_organization_id;
  
  IF NOT FOUND THEN
    RETURN FALSE;
  END IF;
  
  -- Return true if within 80% of budget
  RETURN v_current_cost < (v_monthly_budget * 0.8);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to increment failed login attempts
CREATE OR REPLACE FUNCTION increment_failed_login(p_email TEXT)
RETURNS TABLE(attempts INTEGER, locked_until TIMESTAMPTZ) AS $$
DECLARE
  v_attempts INTEGER;
  v_locked_until TIMESTAMPTZ;
BEGIN
  UPDATE profiles
  SET 
    failed_login_attempts = COALESCE(failed_login_attempts, 0) + 1,
    account_locked_until = CASE 
      WHEN COALESCE(failed_login_attempts, 0) >= 4 
      THEN NOW() + INTERVAL '30 minutes'
      ELSE account_locked_until
    END
  WHERE email = p_email
  RETURNING failed_login_attempts, account_locked_until
  INTO v_attempts, v_locked_until;
  
  RETURN QUERY SELECT v_attempts, v_locked_until;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to reset failed login attempts
CREATE OR REPLACE FUNCTION reset_failed_login(p_user_id UUID)
RETURNS VOID AS $$
BEGIN
  UPDATE profiles
  SET 
    failed_login_attempts = 0,
    account_locked_until = NULL,
    last_login_at = NOW()
  WHERE id = p_user_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to update last activity
CREATE OR REPLACE FUNCTION update_last_activity(p_user_id UUID)
RETURNS VOID AS $$
BEGIN
  UPDATE profiles
  SET last_activity_at = NOW()
  WHERE id = p_user_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Row Level Security Policies
ALTER TABLE organizations ENABLE ROW LEVEL SECURITY;
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

-- Organizations: Users can only see their own organization
CREATE POLICY "Users can view own organization" ON organizations
  FOR SELECT USING (
    id IN (
      SELECT organization_id FROM profiles 
      WHERE profiles.id = auth.uid()
    )
  );

-- Profiles: Users can view profiles in their organization
CREATE POLICY "Users can view organization profiles" ON profiles
  FOR SELECT USING (
    organization_id IN (
      SELECT organization_id FROM profiles 
      WHERE profiles.id = auth.uid()
    )
  );

-- Profiles: Users can update their own profile
CREATE POLICY "Users can update own profile" ON profiles
  FOR UPDATE USING (id = auth.uid());

-- Add RLS to our custom tables
ALTER TABLE articles ENABLE ROW LEVEL SECURITY;
ALTER TABLE pipelines ENABLE ROW LEVEL SECURITY;

-- Articles: Filter by organization
CREATE POLICY "Users can view organization articles" ON articles
  FOR ALL USING (
    organization_id IN (
      SELECT organization_id FROM profiles 
      WHERE profiles.id = auth.uid()
    )
  );

-- Pipelines: Filter by organization  
CREATE POLICY "Users can view organization pipelines" ON pipelines
  FOR ALL USING (
    organization_id IN (
      SELECT organization_id FROM profiles 
      WHERE profiles.id = auth.uid()
    )
  );
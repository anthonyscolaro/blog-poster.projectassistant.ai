-- Create subscribers table for subscription management
CREATE TABLE IF NOT EXISTS public.subscribers (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  email TEXT NOT NULL UNIQUE,
  stripe_customer_id TEXT UNIQUE,
  stripe_subscription_id TEXT,
  subscribed BOOLEAN NOT NULL DEFAULT false,
  subscription_tier TEXT DEFAULT 'free',
  subscription_status TEXT DEFAULT 'inactive',
  subscription_end TIMESTAMPTZ,
  trial_ends_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Create usage tracking table
CREATE TABLE IF NOT EXISTS public.usage_tracking (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID REFERENCES public.organizations(id) ON DELETE CASCADE,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  resource_type TEXT NOT NULL, -- 'article', 'api_call', 'storage'
  resource_id TEXT,
  amount DECIMAL(10,4) DEFAULT 0, -- cost in dollars
  usage_count INTEGER DEFAULT 1,
  billing_month DATE NOT NULL DEFAULT DATE_TRUNC('month', CURRENT_DATE),
  metadata JSONB,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Create payment history table
CREATE TABLE IF NOT EXISTS public.payment_history (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID REFERENCES public.organizations(id) ON DELETE CASCADE,
  stripe_payment_intent_id TEXT UNIQUE,
  stripe_invoice_id TEXT,
  amount DECIMAL(10,2) NOT NULL,
  currency TEXT DEFAULT 'usd',
  status TEXT NOT NULL, -- 'succeeded', 'failed', 'pending', 'refunded'
  payment_method TEXT,
  description TEXT,
  metadata JSONB,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Enable RLS
ALTER TABLE public.subscribers ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.usage_tracking ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.payment_history ENABLE ROW LEVEL SECURITY;

-- Subscribers policies
CREATE POLICY "subscribers_select_own" ON public.subscribers
FOR SELECT USING (user_id = auth.uid() OR email = auth.email());

CREATE POLICY "subscribers_insert" ON public.subscribers
FOR INSERT WITH CHECK (true);

CREATE POLICY "subscribers_update" ON public.subscribers
FOR UPDATE USING (true);

-- Usage tracking policies
CREATE POLICY "usage_select_own_org" ON public.usage_tracking
FOR SELECT USING (
  organization_id IN (
    SELECT organization_id FROM public.profiles WHERE id = auth.uid()
  )
);

CREATE POLICY "usage_insert" ON public.usage_tracking
FOR INSERT WITH CHECK (true);

-- Payment history policies
CREATE POLICY "payment_select_own_org" ON public.payment_history
FOR SELECT USING (
  organization_id IN (
    SELECT organization_id FROM public.profiles WHERE id = auth.uid()
  )
);

CREATE POLICY "payment_insert" ON public.payment_history
FOR INSERT WITH CHECK (true);

-- Add subscription fields to organizations
ALTER TABLE public.organizations 
ADD COLUMN IF NOT EXISTS subscription_tier TEXT DEFAULT 'free',
ADD COLUMN IF NOT EXISTS subscription_status TEXT DEFAULT 'inactive',
ADD COLUMN IF NOT EXISTS stripe_customer_id TEXT,
ADD COLUMN IF NOT EXISTS monthly_article_limit INTEGER DEFAULT 2,
ADD COLUMN IF NOT EXISTS current_month_articles INTEGER DEFAULT 0;
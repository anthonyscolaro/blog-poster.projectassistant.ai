// Core application types for Blog-Poster Dashboard

export interface User {
  id: string
  email: string
  full_name?: string
  avatar_url?: string
  organization_id: string
  role: 'owner' | 'admin' | 'editor' | 'member'
  created_at: string
  updated_at: string
}

export interface Organization {
  id: string
  name: string
  slug: string
  plan: 'free' | 'pro' | 'enterprise'
  subscription_status: 'active' | 'trialing' | 'past_due' | 'canceled'
  articles_limit: number
  articles_used: number
  monthly_budget: number
  current_month_cost: number
  trial_ends_at?: string
  created_at: string
  updated_at: string
}

export interface Article {
  id: string
  organization_id: string
  user_id: string
  title: string
  slug: string
  content?: string
  meta_title?: string
  meta_description?: string
  focus_keyword?: string
  keywords?: string[]
  status: 'draft' | 'review' | 'published' | 'archived'
  seo_score: number
  readability_score: number
  word_count: number
  generation_cost: number
  views_count: number
  shares_count: number
  published_at?: string
  created_at: string
  updated_at: string
}

export interface Pipeline {
  id: string
  organization_id: string
  user_id: string
  name: string
  description?: string
  status: 'pending' | 'running' | 'completed' | 'failed' | 'cancelled'
  progress: number
  current_agent?: string
  total_cost: number
  created_at: string
  updated_at: string
}

export interface AgentConfig {
  id: string
  organization_id: string
  agent_name: string
  enabled: boolean
  max_retries: number
  timeout_seconds: number
  config: Record<string, any>
  created_at: string
  updated_at: string
}

// React 19 enhanced types
export interface AsyncComponentProps<T = any> {
  promise: Promise<T>
  fallback?: React.ReactNode
}

export interface ActionState<T = any> {
  pending: boolean
  data?: T
  error?: string
}

// WebSocket types for real-time updates
export interface WebSocketMessage {
  type: 'pipeline_update' | 'article_update' | 'cost_update' | 'notification' | 'dashboard_update'
  payload: any
  timestamp: string
}

// Dashboard analytics types
export interface DashboardStats {
  total_articles: number
  published_articles: number
  draft_articles: number
  active_pipelines: number
  monthly_cost: number
  budget_percentage: number
}

export interface ChartData {
  name: string
  value: number
  date?: string
}
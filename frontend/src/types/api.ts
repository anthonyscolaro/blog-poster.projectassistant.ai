// API Types for FastAPI Backend Integration

export interface ApiResponse<T> {
  data: T
  message: string
  success: boolean
  error?: string
  metadata?: {
    organization_id: string
    user_id: string
    request_id: string
  }
}

export interface PipelineRequest {
  topic?: string
  keywords?: string[]
  target_word_count?: number
  auto_publish?: boolean
  competitor_urls?: string[]
  tone?: 'professional' | 'friendly' | 'authoritative'
  custom_instructions?: string
}

export interface PipelineResult {
  pipeline_id: string
  status: 'pending' | 'running' | 'completed' | 'failed' | 'cancelled'
  started_at: string
  completed_at?: string
  agents_completed: string[]
  current_agent?: string
  progress_percentage: number
  
  // Results from each agent
  competitor_insights?: CompetitorInsights
  topic_analysis?: TopicAnalysis
  generated_article?: GeneratedArticle
  legal_check_results?: LegalCheckResults
  wordpress_result?: WordPressResult
  
  // Cost tracking
  total_cost: number
  agent_costs: Record<string, number>
  
  // Errors if any
  error_message?: string
  failed_agent?: string
}

export interface AgentStatus {
  agent_id: string
  name: string
  type: 'competitor_monitoring' | 'topic_analysis' | 'article_generation' | 'legal_checker' | 'wordpress_publisher'
  status: 'healthy' | 'degraded' | 'offline'
  last_check: string
  response_time_ms: number
  error_rate: number
  dependencies: {
    name: string
    status: 'healthy' | 'error'
  }[]
}

export interface SystemMetrics {
  total_articles_generated: number
  total_pipelines_run: number
  success_rate: number
  average_processing_time_minutes: number
  active_pipelines: number
  
  cost_metrics: {
    monthly_spend: number
    daily_spend: number
    average_cost_per_article: number
    api_usage: {
      anthropic: number
      openai: number
      jina: number
    }
  }
  
  performance_metrics: {
    average_seo_score: number
    average_word_count: number
    publishing_success_rate: number
  }
}

export interface WebSocketMessage {
  type: 'pipeline_progress' | 'agent_status' | 'article_complete' | 'error' | 'pong'
  payload: any
}

export interface ArticleGenerationRequest {
  title?: string
  keywords?: string[]
  target_word_count?: number
  tone?: string
  custom_instructions?: string
}

export interface SEOAnalysisRequest {
  content: string
  target_keyword?: string
}

export interface WordPressPublishRequest {
  article_id: string
  site_id?: string
  status?: 'draft' | 'publish'
}

// API Error type
export interface ApiError extends Error {
  status?: number
  code?: string
  details?: Record<string, unknown>
}

// Cost tracking types
export interface CostMetrics {
  total_cost: number
  monthly_spend: number
  daily_spend: number
  average_cost_per_article: number
  cost_breakdown: {
    llm: number
    storage: number
    api_calls: number
  }
  period: 'daily' | 'monthly' | 'yearly'
}

// Health check types
export interface HealthStatus {
  status: 'healthy' | 'degraded' | 'unhealthy'
  version: string
  timestamp: string
  dependencies?: DependencyStatus[]
}

export interface DependencyStatus {
  name: string
  status: 'healthy' | 'error'
  message?: string
  response_time_ms?: number
}

// SEO Analysis types
export interface SEOAnalysisResult {
  score: number
  issues: SEOIssue[]
  suggestions: string[]
  meta: {
    title_length: number
    description_length: number
    keyword_density: number
    readability_score: number
  }
}

export interface SEOIssue {
  type: 'error' | 'warning' | 'info'
  message: string
  location?: string
  suggestion?: string
}

// Article generation types
export interface GeneratedArticle {
  id?: string
  title: string
  content: string
  word_count: number
  seo_score: number
  meta_description: string
  keywords: string[]
  featured_image_url?: string
  categories?: string[]
  tags?: string[]
}

export interface ArticleGenerationResult {
  article: GeneratedArticle
  cost: number
  generation_time_seconds: number
  model_used: string
}

// WordPress types
export interface WordPressResult {
  post_id: number
  post_url: string
  status: 'published' | 'draft' | 'scheduled'
  publish_date?: string
  edit_url?: string
}

// Agent result types
export interface CompetitorInsights {
  competitors: CompetitorData[]
  trending_topics: string[]
  content_gaps: string[]
  keyword_opportunities: string[]
}

export interface CompetitorData {
  url: string
  domain: string
  title: string
  published_date?: string
  word_count: number
  estimated_traffic?: number
  keywords: string[]
}

export interface TopicAnalysis {
  recommended_topic: string
  target_keywords: string[]
  search_volume: number
  competition_level: 'low' | 'medium' | 'high'
  content_outline: string[]
  related_questions: string[]
}

export interface LegalCheckResults {
  passed: boolean
  issues: LegalIssue[]
  citations_needed: string[]
  disclaimer_required: boolean
}

export interface LegalIssue {
  severity: 'critical' | 'warning' | 'info'
  description: string
  location: string
  suggestion: string
}
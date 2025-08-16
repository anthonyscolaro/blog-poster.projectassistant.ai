import { getAuthHeaders } from './auth'
import { 
  ApiResponse, 
  ApiError,
  PipelineRequest, 
  PipelineResult, 
  AgentStatus, 
  SystemMetrics, 
  ArticleGenerationRequest,
  ArticleGenerationResult,
  SEOAnalysisRequest,
  SEOAnalysisResult,
  WordPressPublishRequest,
  WordPressResult,
  CostMetrics,
  HealthStatus,
  DependencyStatus
} from '@/types/api'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8088'

// API Paths - CORRECTED to match actual backend
const API_PATHS = {
  health: '/api/v1/health',
  pipeline: '/api/v1/pipeline',
  articles: '/api/v1/api/articles',
  monitoring: '/api/v1/monitoring',
  auth: '/api/v1/auth',
  seo: '/api/v1/seo',
  wordpress: '/api/v1/publish'
}


class ApiService {
  private baseURL: string

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL
  }

  // Helper to determine if error is retryable
  private isRetryableError(error: ApiError | Error): boolean {
    const apiError = error as ApiError
    // Don't retry on client errors (4xx) except 429 (rate limit)
    if (apiError.status && apiError.status >= 400 && apiError.status < 500 && apiError.status !== 429) {
      return false
    }
    // Retry on network errors, 5xx errors, and rate limits
    return true
  }

  // Exponential backoff with jitter
  private async delay(attempt: number): Promise<void> {
    const baseDelay = 1000 // 1 second
    const maxDelay = 30000 // 30 seconds
    const jitter = Math.random() * 1000 // 0-1 second random jitter
    const delay = Math.min(baseDelay * Math.pow(2, attempt) + jitter, maxDelay)
    return new Promise(resolve => setTimeout(resolve, delay))
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {},
    retries: number = 3
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`
    let lastError: ApiError | Error | null = null

    for (let attempt = 0; attempt <= retries; attempt++) {
      try {
        const headers = await getAuthHeaders()
        
        // Add security headers
        const secureHeaders = {
          ...headers,
          'X-Content-Type-Options': 'nosniff',
          'X-Frame-Options': 'DENY',
          'X-XSS-Protection': '1; mode=block',
          ...options.headers,
        }
        
        const config: RequestInit = {
          ...options,
          headers: secureHeaders,
        }

        const response = await fetch(url, config)
        
        if (!response.ok) {
          const error = await response.json().catch(() => ({ 
            message: `HTTP error! status: ${response.status}`,
            status: response.status 
          }))
          const apiError = new Error(error.message || `HTTP error! status: ${response.status}`) as ApiError
          apiError.status = response.status
          throw apiError
        }

        const wrapped: ApiResponse<T> = await response.json()
        
        // IMPORTANT: Unwrap the response
        if (!wrapped.success) {
          throw new Error(wrapped.error || wrapped.message)
        }
        
        return wrapped.data
      } catch (error) {
        lastError = error
        console.error(`API request failed (attempt ${attempt + 1}/${retries + 1}): ${endpoint}`, error)
        
        // Check if we should retry
        if (attempt < retries && this.isRetryableError(error)) {
          console.log(`Retrying request to ${endpoint} after delay...`)
          await this.delay(attempt)
          continue
        }
        
        // Return mock data in development if API unavailable and retries exhausted
        if (!import.meta.env.PROD && this.shouldUseMockData(endpoint)) {
          console.log(`Using mock data for ${endpoint}`)
          return this.getMockData<T>(endpoint)
        }
        
        throw error
      }
    }
    
    throw lastError
  }

  // Pipeline operations - CORRECTED PATHS
  async runPipeline(request: PipelineRequest): Promise<PipelineResult> {
    return this.request<PipelineResult>(`${API_PATHS.pipeline}/run`, {
      method: 'POST',
      body: JSON.stringify(request)
    })
  }

  async getPipelineStatus(pipelineId: string): Promise<PipelineResult> {
    return this.request<PipelineResult>(`${API_PATHS.pipeline}/${pipelineId}/details`)
  }

  async getPipelineHistory(): Promise<PipelineResult[]> {
    return this.request<PipelineResult[]>(`${API_PATHS.pipeline}/history`)
  }

  async cancelPipeline(pipelineId: string): Promise<void> {
    return this.request<void>(`${API_PATHS.pipeline}/${pipelineId}/cancel`, {
      method: 'POST'
    })
  }

  async getCosts(): Promise<CostMetrics> {
    return this.request<CostMetrics>(`${API_PATHS.pipeline}/costs`)
  }

  // Article operations - CORRECTED PATHS
  async generateArticle(request: ArticleGenerationRequest): Promise<ArticleGenerationResult> {
    return this.request<ArticleGenerationResult>(`${API_PATHS.articles}/generate`, {
      method: 'POST',
      body: JSON.stringify(request)
    })
  }

  async deleteArticle(articleId: string): Promise<void> {
    return this.request<void>(`${API_PATHS.articles}/${articleId}`, {
      method: 'DELETE'
    })
  }

  // Monitoring - CORRECTED PATHS
  async getAgentsStatus(): Promise<AgentStatus[]> {
    return this.request<AgentStatus[]>(`${API_PATHS.monitoring}/agents/status`)
  }

  async getSystemMetrics(): Promise<SystemMetrics> {
    return this.request<SystemMetrics>(`${API_PATHS.monitoring}/metrics`)
  }

  async checkDependencies(): Promise<DependencyStatus[]> {
    return this.request<DependencyStatus[]>(`${API_PATHS.monitoring}/health/dependencies`)
  }

  // SEO operations
  async analyzeSEO(request: SEOAnalysisRequest): Promise<SEOAnalysisResult> {
    return this.request<SEOAnalysisResult>(`${API_PATHS.seo}/analyze`, {
      method: 'POST',
      body: JSON.stringify(request)
    })
  }

  async lintSEO(content: string): Promise<SEOAnalysisResult> {
    return this.request<SEOAnalysisResult>(`${API_PATHS.seo}/lint`, {
      method: 'POST',
      body: JSON.stringify({ content })
    })
  }

  // WordPress publishing
  async publishToWordPress(request: WordPressPublishRequest): Promise<WordPressResult> {
    return this.request<WordPressResult>(`${API_PATHS.wordpress}/wp`, {
      method: 'POST',
      body: JSON.stringify(request)
    })
  }

  // Health check
  async getHealth(): Promise<HealthStatus> {
    return this.request<HealthStatus>(API_PATHS.health)
  }

  private shouldUseMockData(endpoint: string): boolean {
    const mockableEndpoints = [
      API_PATHS.health,
      API_PATHS.pipeline,
      API_PATHS.monitoring
    ]
    return mockableEndpoints.some(mock => endpoint.startsWith(mock))
  }

  private getMockData<T>(endpoint: string): T {
    const mockDataMap: Record<string, unknown> = {
      [API_PATHS.health]: {
        status: 'healthy',
        version: '3.0.0',
        timestamp: new Date().toISOString()
      },
      [`${API_PATHS.pipeline}/history`]: [
        {
          pipeline_id: 'pipeline_20240817_001',
          status: 'completed',
          started_at: new Date(Date.now() - 3600000).toISOString(),
          completed_at: new Date().toISOString(),
          agents_completed: ['competitor_monitoring', 'topic_analysis', 'article_generation', 'legal_checker', 'wordpress_publisher'],
          progress_percentage: 100,
          total_cost: 2.45,
          agent_costs: {
            competitor_monitoring: 0.15,
            topic_analysis: 0.25,
            article_generation: 1.50,
            legal_checker: 0.35,
            wordpress_publisher: 0.20
          },
          generated_article: {
            title: 'Understanding Service Dog Rights Under the ADA',
            content: '# Service Dog Rights...',
            word_count: 2150,
            seo_score: 95,
            meta_description: 'Complete guide to service dog rights and ADA compliance',
            keywords: ['service dog', 'ADA', 'disability rights']
          }
        }
      ],
      [`${API_PATHS.monitoring}/agents/status`]: [
        {
          agent_id: 'agent_competitor',
          name: 'Competitor Monitoring Agent',
          type: 'competitor_monitoring',
          status: 'healthy',
          last_check: new Date().toISOString(),
          response_time_ms: 245,
          error_rate: 0.02,
          dependencies: [
            { name: 'Jina AI', status: 'healthy' },
            { name: 'Vector DB', status: 'healthy' }
          ]
        },
        {
          agent_id: 'agent_topic',
          name: 'Topic Analysis Agent',
          type: 'topic_analysis',
          status: 'healthy',
          last_check: new Date().toISOString(),
          response_time_ms: 320,
          error_rate: 0.01,
          dependencies: [
            { name: 'OpenAI API', status: 'healthy' },
            { name: 'Search API', status: 'healthy' }
          ]
        }
      ],
      [`${API_PATHS.monitoring}/metrics`]: {
        total_articles_generated: 1247,
        total_pipelines_run: 1389,
        success_rate: 89.7,
        average_processing_time_minutes: 12.5,
        active_pipelines: 3,
        cost_metrics: {
          monthly_spend: 342.75,
          daily_spend: 11.42,
          average_cost_per_article: 2.31,
          api_usage: {
            anthropic: 156.20,
            openai: 98.45,
            jina: 88.10
          }
        },
        performance_metrics: {
          average_seo_score: 87.3,
          average_word_count: 1842,
          publishing_success_rate: 94.2
        }
      }
    }

    // Find matching mock data
    for (const [key, value] of Object.entries(mockDataMap)) {
      if (endpoint.includes(key)) {
        return value as T
      }
    }

    return null as T
  }
}

export const apiService = new ApiService()
export default apiService
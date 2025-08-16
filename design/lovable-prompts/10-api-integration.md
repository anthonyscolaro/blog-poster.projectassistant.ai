# Lovable Prompt: API Integration & Real-time Updates (CORRECTED)

## Business Context:
Implementing comprehensive API integration layer to connect the Blog-Poster dashboard with the FastAPI backend running on port 8088. This includes service layer architecture, native WebSocket connections for real-time updates, Supabase authentication, and robust error handling.

## User Story:
"As a content manager, I want the dashboard to seamlessly communicate with the backend API, receive real-time updates on pipeline progress, and gracefully handle connection issues without breaking the user experience."

## Technical Requirements:
- Complete API service layer with TypeScript interfaces matching actual backend
- Native WebSocket integration (not Socket.IO) for real-time pipeline updates
- Supabase JWT authentication with organization context
- Robust error handling with proper response unwrapping
- Mock data fallbacks when API unavailable
- Loading states and optimistic updates
- Multi-tenant organization isolation

## CRITICAL CORRECTIONS FROM ACTUAL BACKEND:

### 1. API Base Path Structure
```typescript
// CORRECT paths based on actual backend:
const API_PATHS = {
  health: '/api/v1/health',
  pipeline: '/api/v1/pipeline',  // SINGULAR, not plural
  articles: '/api/v1/api/articles',  // Double 'api' prefix
  monitoring: '/api/v1/monitoring',
  auth: '/api/v1/auth',
  seo: '/api/v1/seo',
  wordpress: '/api/v1/publish'
}
```

### 2. Response Wrapper Format
```typescript
// ALL responses are wrapped in this format:
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
```

### 3. Authentication Implementation
```typescript
// src/services/auth.ts
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

// Get JWT token for API calls
export async function getAuthToken(): Promise<string | null> {
  const { data: { session } } = await supabase.auth.getSession()
  return session?.access_token || null
}

// Add organization context to headers
export async function getAuthHeaders(): Promise<Record<string, string>> {
  const token = await getAuthToken()
  const { data: profile } = await supabase
    .from('profiles')
    .select('organization_id')
    .single()
  
  return {
    'Authorization': token ? `Bearer ${token}` : '',
    'X-Organization-ID': profile?.organization_id || '',
    'Content-Type': 'application/json'
  }
}
```

### 4. Correct TypeScript Interfaces
```typescript
// src/types/api.ts - CORRECTED to match actual backend

export interface PipelineRequest {
  topic?: string  // Optional - can be auto-determined
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
  competitor_insights?: any
  topic_analysis?: any
  generated_article?: {
    title: string
    content: string
    word_count: number
    seo_score: number
    meta_description: string
    keywords: string[]
  }
  legal_check_results?: any
  wordpress_result?: {
    post_id: number
    post_url: string
    status: string
  }
  
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
```

### 5. Correct API Service Implementation
```typescript
// src/services/api.ts - CORRECTED version
import { getAuthHeaders } from './auth'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8088'

class ApiService {
  private baseURL: string

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`
    const headers = await getAuthHeaders()
    
    const config: RequestInit = {
      ...options,
      headers: {
        ...headers,
        ...options.headers,
      },
    }

    try {
      const response = await fetch(url, config)
      
      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.message || `HTTP error! status: ${response.status}`)
      }

      const wrapped: ApiResponse<T> = await response.json()
      
      // IMPORTANT: Unwrap the response
      if (!wrapped.success) {
        throw new Error(wrapped.error || wrapped.message)
      }
      
      return wrapped.data
    } catch (error) {
      console.error(`API request failed: ${endpoint}`, error)
      
      // Return mock data in development if API unavailable
      if (!import.meta.env.PROD && this.shouldUseMockData(endpoint)) {
        return this.getMockData<T>(endpoint)
      }
      
      throw error
    }
  }

  // Pipeline operations - CORRECTED PATHS
  async runPipeline(request: PipelineRequest): Promise<PipelineResult> {
    return this.request<PipelineResult>('/api/v1/pipeline/run', {
      method: 'POST',
      body: JSON.stringify(request)
    })
  }

  async getPipelineStatus(pipelineId: string): Promise<PipelineResult> {
    return this.request<PipelineResult>(`/api/v1/pipeline/${pipelineId}/details`)
  }

  async getPipelineHistory(): Promise<PipelineResult[]> {
    return this.request<PipelineResult[]>('/api/v1/pipeline/history')
  }

  async getCosts(): Promise<any> {
    return this.request<any>('/api/v1/pipeline/costs')
  }

  // Article operations - CORRECTED PATHS
  async generateArticle(request: any): Promise<any> {
    return this.request<any>('/api/v1/api/articles/generate', {
      method: 'POST',
      body: JSON.stringify(request)
    })
  }

  async deleteArticle(articleId: string): Promise<void> {
    return this.request<void>(`/api/v1/api/articles/${articleId}`, {
      method: 'DELETE'
    })
  }

  // Monitoring - CORRECTED PATHS
  async getAgentsStatus(): Promise<AgentStatus[]> {
    return this.request<AgentStatus[]>('/api/v1/monitoring/agents/status')
  }

  async getSystemMetrics(): Promise<SystemMetrics> {
    return this.request<SystemMetrics>('/api/v1/monitoring/metrics')
  }

  async checkDependencies(): Promise<any> {
    return this.request<any>('/api/v1/monitoring/health/dependencies')
  }

  // SEO operations
  async lintSEO(content: string): Promise<any> {
    return this.request<any>('/api/v1/seo/lint', {
      method: 'POST',
      body: JSON.stringify({ content })
    })
  }

  // WordPress publishing
  async publishToWordPress(articleId: string): Promise<any> {
    return this.request<any>('/api/v1/publish/wp', {
      method: 'POST',
      body: JSON.stringify({ article_id: articleId })
    })
  }

  // Health check
  async getHealth(): Promise<any> {
    return this.request<any>('/api/v1/health')
  }

  private shouldUseMockData(endpoint: string): boolean {
    const mockableEndpoints = [
      '/api/v1/health',
      '/api/v1/pipeline',
      '/api/v1/monitoring'
    ]
    return mockableEndpoints.some(mock => endpoint.startsWith(mock))
  }

  private getMockData<T>(endpoint: string): T {
    // Mock data implementation...
    const mockDataMap: Record<string, any> = {
      '/api/v1/health': {
        status: 'healthy',
        version: '3.0.0',
        timestamp: new Date().toISOString()
      },
      '/api/v1/pipeline/history': [
        {
          pipeline_id: 'pipeline_20240817_001',
          status: 'completed',
          started_at: new Date(Date.now() - 3600000).toISOString(),
          completed_at: new Date().toISOString(),
          agents_completed: ['competitor_monitoring', 'topic_analysis', 'article_generation', 'legal_checker', 'wordpress_publisher'],
          progress_percentage: 100,
          total_cost: 2.45,
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
      '/api/v1/monitoring/agents/status': [
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
        }
      ]
    }

    return mockDataMap[endpoint] as T || null as T
  }
}

export const apiService = new ApiService()
export default apiService
```

### 6. Native WebSocket Implementation (NOT Socket.IO)
```typescript
// src/services/websocket.ts - CORRECTED for native WebSocket
import { getAuthToken } from './auth'

class WebSocketService {
  private ws: WebSocket | null = null
  private reconnectAttempts = 0
  private maxReconnectAttempts = 5
  private reconnectDelay = 1000
  private listeners: Map<string, Set<Function>> = new Map()
  private pingInterval: number | null = null

  async connect(pipelineId?: string) {
    const token = await getAuthToken()
    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const wsHost = import.meta.env.VITE_API_URL?.replace(/^https?:/, '') || 'localhost:8088'
    
    // Use the correct WebSocket endpoint
    const endpoint = pipelineId 
      ? `/api/v1/ws/pipeline/${pipelineId}?token=${token}`
      : `/api/v1/ws/notifications?token=${token}`
    
    const wsUrl = `${wsProtocol}//${wsHost}${endpoint}`
    
    this.ws = new WebSocket(wsUrl)

    this.ws.onopen = () => {
      console.log('WebSocket connected')
      this.reconnectAttempts = 0
      this.startPing()
      this.emit('connected', null)
    }

    this.ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        
        // Handle different message types from backend
        switch (data.type) {
          case 'pipeline_progress':
            this.emit('pipeline_progress', data.payload)
            break
          case 'agent_status':
            this.emit('agent_status', data.payload)
            break
          case 'article_complete':
            this.emit('article_complete', data.payload)
            break
          case 'error':
            this.emit('error', data.payload)
            break
          case 'pong':
            // Heartbeat response
            break
          default:
            console.warn('Unknown WebSocket message type:', data.type)
        }
      } catch (error) {
        console.error('Failed to parse WebSocket message:', error)
      }
    }

    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error)
      this.emit('error', error)
    }

    this.ws.onclose = (event) => {
      console.log('WebSocket disconnected:', event.code, event.reason)
      this.stopPing()
      this.emit('disconnected', event)
      
      // Attempt reconnection
      if (this.reconnectAttempts < this.maxReconnectAttempts) {
        this.reconnectAttempts++
        setTimeout(() => {
          console.log(`Reconnecting... (attempt ${this.reconnectAttempts})`)
          this.connect(pipelineId)
        }, this.reconnectDelay * this.reconnectAttempts)
      }
    }

    return this.ws
  }

  disconnect() {
    this.stopPing()
    if (this.ws) {
      this.ws.close(1000, 'Client disconnect')
      this.ws = null
    }
    this.listeners.clear()
  }

  // Send commands to backend
  send(type: string, payload: any) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({ type, payload }))
    } else {
      console.error('WebSocket not connected')
    }
  }

  // Pipeline control commands
  pausePipeline(pipelineId: string) {
    this.send('pause_pipeline', { pipeline_id: pipelineId })
  }

  resumePipeline(pipelineId: string) {
    this.send('resume_pipeline', { pipeline_id: pipelineId })
  }

  cancelPipeline(pipelineId: string) {
    this.send('cancel_pipeline', { pipeline_id: pipelineId })
  }

  // Event handling
  on(event: string, callback: Function) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, new Set())
    }
    this.listeners.get(event)!.add(callback)
  }

  off(event: string, callback: Function) {
    this.listeners.get(event)?.delete(callback)
  }

  private emit(event: string, data: any) {
    this.listeners.get(event)?.forEach(callback => callback(data))
  }

  // Heartbeat to keep connection alive
  private startPing() {
    this.pingInterval = window.setInterval(() => {
      if (this.ws && this.ws.readyState === WebSocket.OPEN) {
        this.ws.send(JSON.stringify({ type: 'ping' }))
      }
    }, 30000) // Ping every 30 seconds
  }

  private stopPing() {
    if (this.pingInterval) {
      clearInterval(this.pingInterval)
      this.pingInterval = null
    }
  }

  isConnected(): boolean {
    return this.ws?.readyState === WebSocket.OPEN
  }
}

export const wsService = new WebSocketService()
export default wsService
```

### 7. React Query Hooks - CORRECTED
```typescript
// src/hooks/useApi.ts - CORRECTED to match actual API
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { toast } from 'sonner'  // Using sonner instead of react-hot-toast (Lovable preference)
import apiService from '@/services/api'
import { PipelineRequest, PipelineResult } from '@/types/api'

// Pipeline hooks - CORRECTED
export function usePipelineHistory() {
  return useQuery({
    queryKey: ['pipeline', 'history'],
    queryFn: () => apiService.getPipelineHistory(),
    refetchInterval: 30000,
    staleTime: 10000,
  })
}

export function usePipelineStatus(pipelineId: string) {
  return useQuery({
    queryKey: ['pipeline', pipelineId],
    queryFn: () => apiService.getPipelineStatus(pipelineId),
    enabled: !!pipelineId,
    refetchInterval: 5000, // Poll every 5 seconds while running
  })
}

export function useRunPipeline() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: (request: PipelineRequest) => apiService.runPipeline(request),
    onSuccess: (result) => {
      queryClient.invalidateQueries({ queryKey: ['pipeline'] })
      toast.success('Pipeline started successfully!')
      
      // Connect WebSocket for this pipeline
      wsService.connect(result.pipeline_id)
    },
    onError: (error: Error) => {
      console.error('Failed to start pipeline:', error)
      toast.error(error.message || 'Failed to start pipeline')
    },
  })
}

// Monitoring hooks - CORRECTED
export function useAgentsStatus() {
  return useQuery({
    queryKey: ['monitoring', 'agents'],
    queryFn: () => apiService.getAgentsStatus(),
    refetchInterval: 10000,
  })
}

export function useSystemMetrics() {
  return useQuery({
    queryKey: ['monitoring', 'metrics'],
    queryFn: () => apiService.getSystemMetrics(),
    refetchInterval: 30000,
  })
}

// Cost tracking
export function useCostMetrics() {
  return useQuery({
    queryKey: ['costs'],
    queryFn: () => apiService.getCosts(),
    refetchInterval: 60000, // Update every minute
  })
}

// Health check with organization context
export function useHealthCheck() {
  return useQuery({
    queryKey: ['health'],
    queryFn: () => apiService.getHealth(),
    refetchInterval: 60000,
    retry: 3,
  })
}
```

### 8. WebSocket Hook - CORRECTED
```typescript
// src/hooks/useWebSocket.ts - CORRECTED for native WebSocket
import { useEffect, useCallback, useState } from 'react'
import { useQueryClient } from '@tanstack/react-query'
import { toast } from 'sonner'
import wsService from '@/services/websocket'

export function usePipelineWebSocket(pipelineId?: string) {
  const queryClient = useQueryClient()
  const [isConnected, setIsConnected] = useState(false)

  useEffect(() => {
    if (!pipelineId) return

    // Connect to pipeline-specific WebSocket
    wsService.connect(pipelineId)

    // Handle connection events
    const handleConnected = () => setIsConnected(true)
    const handleDisconnected = () => setIsConnected(false)

    // Handle pipeline progress
    const handlePipelineProgress = (progress: any) => {
      // Update cache with real-time progress
      queryClient.setQueryData(['pipeline', pipelineId], (oldData: any) => {
        if (oldData) {
          return {
            ...oldData,
            progress_percentage: progress.percentage,
            current_agent: progress.current_agent,
            agents_completed: progress.agents_completed,
          }
        }
        return oldData
      })

      // Show progress notifications
      if (progress.percentage === 100) {
        toast.success(`Pipeline completed successfully!`)
        queryClient.invalidateQueries({ queryKey: ['pipeline', 'history'] })
      } else if (progress.message) {
        toast.info(progress.message)
      }
    }

    // Handle errors
    const handleError = (error: any) => {
      toast.error(error.message || 'Pipeline error occurred')
      queryClient.invalidateQueries({ queryKey: ['pipeline', pipelineId] })
    }

    // Handle article completion
    const handleArticleComplete = (article: any) => {
      toast.success(`Article "${article.title}" has been generated!`)
      queryClient.invalidateQueries({ queryKey: ['articles'] })
    }

    // Register event listeners
    wsService.on('connected', handleConnected)
    wsService.on('disconnected', handleDisconnected)
    wsService.on('pipeline_progress', handlePipelineProgress)
    wsService.on('error', handleError)
    wsService.on('article_complete', handleArticleComplete)

    // Cleanup
    return () => {
      wsService.off('connected', handleConnected)
      wsService.off('disconnected', handleDisconnected)
      wsService.off('pipeline_progress', handlePipelineProgress)
      wsService.off('error', handleError)
      wsService.off('article_complete', handleArticleComplete)
      wsService.disconnect()
    }
  }, [pipelineId, queryClient])

  const pausePipeline = useCallback(() => {
    if (pipelineId) {
      wsService.pausePipeline(pipelineId)
    }
  }, [pipelineId])

  const resumePipeline = useCallback(() => {
    if (pipelineId) {
      wsService.resumePipeline(pipelineId)
    }
  }, [pipelineId])

  const cancelPipeline = useCallback(() => {
    if (pipelineId) {
      wsService.cancelPipeline(pipelineId)
    }
  }, [pipelineId])

  return {
    isConnected,
    pausePipeline,
    resumePipeline,
    cancelPipeline,
  }
}

// General notifications WebSocket
export function useNotificationsWebSocket() {
  const queryClient = useQueryClient()
  const [isConnected, setIsConnected] = useState(false)

  useEffect(() => {
    // Connect to general notifications
    wsService.connect()

    const handleConnected = () => setIsConnected(true)
    const handleDisconnected = () => setIsConnected(false)

    const handleAgentStatus = (status: any) => {
      queryClient.invalidateQueries({ queryKey: ['monitoring', 'agents'] })
      
      if (status.status === 'error' || status.status === 'offline') {
        toast.error(`Agent ${status.name} is ${status.status}`)
      }
    }

    wsService.on('connected', handleConnected)
    wsService.on('disconnected', handleDisconnected)
    wsService.on('agent_status', handleAgentStatus)

    return () => {
      wsService.off('connected', handleConnected)
      wsService.off('disconnected', handleDisconnected)
      wsService.off('agent_status', handleAgentStatus)
      wsService.disconnect()
    }
  }, [queryClient])

  return { isConnected }
}
```

## Key Implementation Notes:

1. **Use Supabase Client**: The backend expects Supabase JWT tokens, not simple bearer tokens
2. **Response Unwrapping**: All API responses are wrapped and must be unwrapped
3. **Native WebSocket**: Use native WebSocket API, not Socket.IO
4. **Organization Context**: Include X-Organization-ID header in all requests
5. **Path Corrections**: Use the exact paths from the backend (pipeline singular, double api prefix)
6. **Error Handling**: Backend returns structured errors in the response wrapper
7. **Real-time Updates**: WebSocket messages have type/payload structure
8. **Cost Tracking**: Backend tracks costs at multiple levels (pipeline, agent, API usage)

## Success Criteria:
- ✅ API service layer matches actual backend structure
- ✅ Native WebSocket implementation (not Socket.IO)
- ✅ Supabase authentication integration
- ✅ Proper response unwrapping
- ✅ Organization-based multi-tenancy
- ✅ Real-time pipeline progress updates
- ✅ Error handling with fallbacks
- ✅ Cost tracking and monitoring

This corrected implementation will work with the actual FastAPI backend at port 8088.
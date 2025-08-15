# Lovable Prompt: API Integration & Real-time Updates

## Business Context:
Implementing comprehensive API integration layer to connect the Blog-Poster dashboard with the FastAPI backend running on port 8088. This includes service layer architecture, WebSocket connections for real-time updates, robust error handling, and mock data fallbacks for offline development.

## User Story:
"As a content manager, I want the dashboard to seamlessly communicate with the backend API, receive real-time updates on pipeline progress, and gracefully handle connection issues without breaking the user experience."

## Technical Requirements:
- Complete API service layer with TypeScript interfaces
- WebSocket integration for real-time pipeline updates
- Robust error handling and retry logic
- Mock data fallbacks when API unavailable
- Request/response interceptors for authentication
- Loading states and optimistic updates
- React 19 use() hook for promise-based data fetching
- Server Components for initial data loading where applicable

## Prompt for Lovable:

Create a comprehensive API integration layer for the Blog-Poster dashboard with real-time capabilities and robust error handling.

### API Service Layer

```typescript
// src/types/api.ts
export interface ApiResponse<T> {
  data: T
  message: string
  success: boolean
}

export interface PipelineStatus {
  id: string
  name: string
  status: 'pending' | 'running' | 'completed' | 'failed' | 'paused'
  progress: number
  currentAgent: string
  startTime: string
  endTime?: string
  error?: string
  cost: number
}

export interface Article {
  id: string
  title: string
  content: string
  status: 'draft' | 'published' | 'pending'
  wordCount: number
  seoScore: number
  publishedAt?: string
  tags: string[]
  meta: {
    description: string
    keywords: string[]
    canonicalUrl?: string
  }
  cost: number
}

export interface Agent {
  id: string
  name: string
  status: 'healthy' | 'warning' | 'error' | 'offline'
  lastCheck: string
  responseTime: number
  errorRate: number
}

export interface SystemMetrics {
  totalArticles: number
  successRate: number
  avgProcessingTime: number
  activePipelines: number
  monthlySpend: number
  apiUsage: {
    anthropic: number
    jina: number
  }
}

export interface CreatePipelineRequest {
  name: string
  topic: string
  keywords: string[]
  targetWordCount: number
  autoPublish: boolean
}

export interface PipelineProgress {
  pipelineId: string
  stage: string
  progress: number
  message: string
  timestamp: string
}
```

```typescript
// src/services/api.ts
import { QueryClient } from '@tanstack/react-query'

const API_BASE_URL = import.meta.env.PROD ? '/api' : 'http://localhost:8088'

class ApiService {
  private baseURL: string
  private queryClient: QueryClient

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL
    this.queryClient = new QueryClient()
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    const url = `${this.baseURL}${endpoint}`
    
    const defaultHeaders = {
      'Content-Type': 'application/json',
      ...options.headers,
    }

    // Add auth token if available
    const token = localStorage.getItem('auth_token')
    if (token) {
      defaultHeaders.Authorization = `Bearer ${token}`
    }

    const config: RequestInit = {
      ...options,
      headers: defaultHeaders,
    }

    try {
      const response = await fetch(url, config)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      return data
    } catch (error) {
      console.error(`API request failed: ${endpoint}`, error)
      
      // Return mock data if API is unavailable and we're in development
      if (!import.meta.env.PROD && this.shouldUseMockData(endpoint)) {
        return this.getMockData<T>(endpoint)
      }
      
      throw error
    }
  }

  private shouldUseMockData(endpoint: string): boolean {
    // Use mock data for common endpoints when API is unavailable
    const mockableEndpoints = [
      '/health',
      '/pipelines',
      '/articles',
      '/agents/status',
      '/metrics'
    ]
    return mockableEndpoints.some(mock => endpoint.startsWith(mock))
  }

  private getMockData<T>(endpoint: string): ApiResponse<T> {
    // Mock data based on endpoint
    const mockDataMap: Record<string, any> = {
      '/health': {
        data: { status: 'healthy', version: '1.0.0' },
        message: 'Service healthy (mock data)',
        success: true
      },
      '/pipelines': {
        data: [
          {
            id: '1',
            name: 'Service Dog Training',
            status: 'running',
            progress: 65,
            currentAgent: 'Article Generation Agent',
            startTime: new Date().toISOString(),
            cost: 2.34
          },
          {
            id: '2',
            name: 'ADA Compliance Guide',
            status: 'completed',
            progress: 100,
            currentAgent: 'WordPress Publishing Agent',
            startTime: new Date(Date.now() - 3600000).toISOString(),
            endTime: new Date().toISOString(),
            cost: 1.89
          }
        ],
        message: 'Pipelines retrieved (mock data)',
        success: true
      },
      '/articles': {
        data: [
          {
            id: '1',
            title: 'Complete Guide to Service Dog Training Methods',
            content: '# Service Dog Training...',
            status: 'published',
            wordCount: 2150,
            seoScore: 95,
            publishedAt: new Date().toISOString(),
            tags: ['Service Dogs', 'Training', 'ADA'],
            meta: {
              description: 'Comprehensive guide to service dog training methods',
              keywords: ['service dog', 'training', 'ADA compliance']
            },
            cost: 1.23
          }
        ],
        message: 'Articles retrieved (mock data)',
        success: true
      },
      '/agents/status': {
        data: [
          {
            id: '1',
            name: 'Competitor Monitoring Agent',
            status: 'healthy',
            lastCheck: new Date().toISOString(),
            responseTime: 250,
            errorRate: 0.02
          },
          {
            id: '2',
            name: 'Article Generation Agent',
            status: 'warning',
            lastCheck: new Date().toISOString(),
            responseTime: 1200,
            errorRate: 0.08
          }
        ],
        message: 'Agent status retrieved (mock data)',
        success: true
      },
      '/metrics': {
        data: {
          totalArticles: 24,
          successRate: 0.96,
          avgProcessingTime: 3.2,
          activePipelines: 5,
          monthlySpend: 45.67,
          apiUsage: {
            anthropic: 1250,
            jina: 890
          }
        },
        message: 'Metrics retrieved (mock data)',
        success: true
      }
    }

    const mockData = mockDataMap[endpoint] || {
      data: null,
      message: 'Mock data not available',
      success: false
    }

    return mockData as ApiResponse<T>
  }

  // Health check
  async getHealth() {
    return this.request<{ status: string; version: string }>('/health')
  }

  // Pipeline operations
  async getPipelines() {
    return this.request<PipelineStatus[]>('/pipelines')
  }

  async createPipeline(data: CreatePipelineRequest) {
    return this.request<PipelineStatus>('/pipelines', {
      method: 'POST',
      body: JSON.stringify(data)
    })
  }

  async getPipeline(id: string) {
    return this.request<PipelineStatus>(`/pipelines/${id}`)
  }

  async startPipeline(id: string) {
    return this.request<PipelineStatus>(`/pipelines/${id}/start`, {
      method: 'POST'
    })
  }

  async pausePipeline(id: string) {
    return this.request<PipelineStatus>(`/pipelines/${id}/pause`, {
      method: 'POST'
    })
  }

  async stopPipeline(id: string) {
    return this.request<PipelineStatus>(`/pipelines/${id}/stop`, {
      method: 'POST'
    })
  }

  // Article operations
  async getArticles() {
    return this.request<Article[]>('/articles')
  }

  async getArticle(id: string) {
    return this.request<Article>(`/articles/${id}`)
  }

  async publishArticle(id: string) {
    return this.request<Article>(`/articles/${id}/publish`, {
      method: 'POST'
    })
  }

  async deleteArticle(id: string) {
    return this.request<void>(`/articles/${id}`, {
      method: 'DELETE'
    })
  }

  // System monitoring
  async getAgentStatus() {
    return this.request<Agent[]>('/agents/status')
  }

  async getMetrics() {
    return this.request<SystemMetrics>('/metrics')
  }

  // SEO operations
  async lintSEO(content: string) {
    return this.request<{ score: number; issues: string[] }>('/seo/lint', {
      method: 'POST',
      body: JSON.stringify({ content })
    })
  }
}

export const apiService = new ApiService()
export default apiService
```

### WebSocket Service for Real-time Updates

```typescript
// src/services/websocket.ts
import { io, Socket } from 'socket.io-client'
import { PipelineProgress } from '@/types/api'

class WebSocketService {
  private socket: Socket | null = null
  private reconnectAttempts = 0
  private maxReconnectAttempts = 5
  private reconnectDelay = 1000

  connect() {
    const wsUrl = import.meta.env.PROD ? '' : 'http://localhost:8088'
    
    this.socket = io(wsUrl, {
      path: '/ws',
      transports: ['websocket', 'polling'],
      reconnection: true,
      reconnectionAttempts: this.maxReconnectAttempts,
      reconnectionDelay: this.reconnectDelay,
    })

    this.socket.on('connect', () => {
      console.log('WebSocket connected')
      this.reconnectAttempts = 0
    })

    this.socket.on('disconnect', (reason) => {
      console.log('WebSocket disconnected:', reason)
    })

    this.socket.on('reconnect', (attemptNumber) => {
      console.log('WebSocket reconnected after', attemptNumber, 'attempts')
    })

    this.socket.on('reconnect_error', (error) => {
      this.reconnectAttempts++
      console.error('WebSocket reconnect error:', error)
      
      if (this.reconnectAttempts >= this.maxReconnectAttempts) {
        console.error('Max reconnection attempts reached')
      }
    })

    return this.socket
  }

  disconnect() {
    if (this.socket) {
      this.socket.disconnect()
      this.socket = null
    }
  }

  // Pipeline progress updates
  onPipelineProgress(callback: (progress: PipelineProgress) => void) {
    if (this.socket) {
      this.socket.on('pipeline_progress', callback)
    }
  }

  offPipelineProgress() {
    if (this.socket) {
      this.socket.off('pipeline_progress')
    }
  }

  // Agent status updates
  onAgentStatusUpdate(callback: (status: any) => void) {
    if (this.socket) {
      this.socket.on('agent_status', callback)
    }
  }

  offAgentStatusUpdate() {
    if (this.socket) {
      this.socket.off('agent_status')
    }
  }

  // System alerts
  onSystemAlert(callback: (alert: any) => void) {
    if (this.socket) {
      this.socket.on('system_alert', callback)
    }
  }

  offSystemAlert() {
    if (this.socket) {
      this.socket.off('system_alert')
    }
  }

  // Article completion
  onArticleComplete(callback: (article: any) => void) {
    if (this.socket) {
      this.socket.on('article_complete', callback)
    }
  }

  offArticleComplete() {
    if (this.socket) {
      this.socket.off('article_complete')
    }
  }

  // Join/leave rooms for specific pipeline updates
  joinPipelineRoom(pipelineId: string) {
    if (this.socket) {
      this.socket.emit('join_pipeline', pipelineId)
    }
  }

  leavePipelineRoom(pipelineId: string) {
    if (this.socket) {
      this.socket.emit('leave_pipeline', pipelineId)
    }
  }

  isConnected(): boolean {
    return this.socket?.connected || false
  }
}

export const wsService = new WebSocketService()
export default wsService
```

### React Query Hooks for Data Management

```typescript
// src/hooks/useApi.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { toast } from 'react-hot-toast'
import apiService from '@/services/api'
import { CreatePipelineRequest, PipelineStatus, Article } from '@/types/api'

// Pipeline hooks
export function usePipelines() {
  return useQuery({
    queryKey: ['pipelines'],
    queryFn: () => apiService.getPipelines(),
    refetchInterval: 30000, // Refetch every 30 seconds
    staleTime: 10000, // Consider data stale after 10 seconds
  })
}

export function usePipeline(id: string) {
  return useQuery({
    queryKey: ['pipeline', id],
    queryFn: () => apiService.getPipeline(id),
    enabled: !!id,
  })
}

export function useCreatePipeline() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: (data: CreatePipelineRequest) => apiService.createPipeline(data),
    onSuccess: (response) => {
      queryClient.invalidateQueries({ queryKey: ['pipelines'] })
      toast.success('Pipeline created successfully!')
    },
    onError: (error) => {
      console.error('Failed to create pipeline:', error)
      toast.error('Failed to create pipeline. Please try again.')
    },
  })
}

export function useStartPipeline() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: (id: string) => apiService.startPipeline(id),
    onSuccess: (response) => {
      queryClient.invalidateQueries({ queryKey: ['pipelines'] })
      queryClient.invalidateQueries({ queryKey: ['pipeline', response.data.id] })
      toast.success('Pipeline started!')
    },
    onError: (error) => {
      console.error('Failed to start pipeline:', error)
      toast.error('Failed to start pipeline. Please check system status.')
    },
  })
}

export function usePausePipeline() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: (id: string) => apiService.pausePipeline(id),
    onSuccess: (response) => {
      queryClient.invalidateQueries({ queryKey: ['pipelines'] })
      queryClient.invalidateQueries({ queryKey: ['pipeline', response.data.id] })
      toast.success('Pipeline paused')
    },
    onError: (error) => {
      console.error('Failed to pause pipeline:', error)
      toast.error('Failed to pause pipeline')
    },
  })
}

export function useStopPipeline() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: (id: string) => apiService.stopPipeline(id),
    onSuccess: (response) => {
      queryClient.invalidateQueries({ queryKey: ['pipelines'] })
      queryClient.invalidateQueries({ queryKey: ['pipeline', response.data.id] })
      toast.success('Pipeline stopped')
    },
    onError: (error) => {
      console.error('Failed to stop pipeline:', error)
      toast.error('Failed to stop pipeline')
    },
  })
}

// Article hooks
export function useArticles() {
  return useQuery({
    queryKey: ['articles'],
    queryFn: () => apiService.getArticles(),
    staleTime: 60000, // Consider data stale after 1 minute
  })
}

export function useArticle(id: string) {
  return useQuery({
    queryKey: ['article', id],
    queryFn: () => apiService.getArticle(id),
    enabled: !!id,
  })
}

export function usePublishArticle() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: (id: string) => apiService.publishArticle(id),
    onSuccess: (response) => {
      queryClient.invalidateQueries({ queryKey: ['articles'] })
      queryClient.invalidateQueries({ queryKey: ['article', response.data.id] })
      toast.success('Article published successfully!')
    },
    onError: (error) => {
      console.error('Failed to publish article:', error)
      toast.error('Failed to publish article. Please check WordPress connection.')
    },
  })
}

export function useDeleteArticle() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: (id: string) => apiService.deleteArticle(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['articles'] })
      toast.success('Article deleted')
    },
    onError: (error) => {
      console.error('Failed to delete article:', error)
      toast.error('Failed to delete article')
    },
  })
}

// System monitoring hooks
export function useAgentStatus() {
  return useQuery({
    queryKey: ['agents', 'status'],
    queryFn: () => apiService.getAgentStatus(),
    refetchInterval: 10000, // Refetch every 10 seconds for monitoring
  })
}

export function useSystemMetrics() {
  return useQuery({
    queryKey: ['metrics'],
    queryFn: () => apiService.getMetrics(),
    refetchInterval: 30000, // Refetch every 30 seconds
  })
}

// Health check
export function useHealthCheck() {
  return useQuery({
    queryKey: ['health'],
    queryFn: () => apiService.getHealth(),
    refetchInterval: 60000, // Check every minute
    retry: 3,
  })
}

// SEO hooks
export function useSEOLint() {
  return useMutation({
    mutationFn: (content: string) => apiService.lintSEO(content),
    onError: (error) => {
      console.error('SEO lint failed:', error)
      toast.error('Failed to analyze SEO. Please try again.')
    },
  })
}
```

### WebSocket Hook for Real-time Updates

```typescript
// src/hooks/useWebSocket.ts
import { useEffect, useCallback } from 'react'
import { useQueryClient } from '@tanstack/react-query'
import { toast } from 'react-hot-toast'
import wsService from '@/services/websocket'
import { PipelineProgress } from '@/types/api'

export function useWebSocketConnection() {
  const queryClient = useQueryClient()

  useEffect(() => {
    const socket = wsService.connect()

    // Handle pipeline progress updates
    const handlePipelineProgress = (progress: PipelineProgress) => {
      // Update pipeline data in cache
      queryClient.setQueryData(['pipeline', progress.pipelineId], (oldData: any) => {
        if (oldData?.data) {
          return {
            ...oldData,
            data: {
              ...oldData.data,
              progress: progress.progress,
              currentAgent: progress.stage,
            }
          }
        }
        return oldData
      })

      // Invalidate pipelines list to ensure consistency
      queryClient.invalidateQueries({ queryKey: ['pipelines'] })

      // Show progress notification
      if (progress.progress === 100) {
        toast.success(`Pipeline "${progress.pipelineId}" completed!`)
      }
    }

    // Handle agent status updates
    const handleAgentStatusUpdate = (status: any) => {
      queryClient.invalidateQueries({ queryKey: ['agents', 'status'] })
      
      if (status.status === 'error') {
        toast.error(`Agent ${status.name} is experiencing issues`)
      }
    }

    // Handle system alerts
    const handleSystemAlert = (alert: any) => {
      switch (alert.level) {
        case 'error':
          toast.error(alert.message)
          break
        case 'warning':
          toast.custom((t) => (
            <div className={`${t.visible ? 'animate-enter' : 'animate-leave'} max-w-md w-full bg-yellow-100 border border-yellow-400 text-yellow-700 px-4 py-3 rounded shadow-lg`}>
              <strong className="font-bold">Warning: </strong>
              <span className="block sm:inline">{alert.message}</span>
            </div>
          ))
          break
        case 'info':
          toast.success(alert.message)
          break
      }
    }

    // Handle article completion
    const handleArticleComplete = (article: any) => {
      queryClient.invalidateQueries({ queryKey: ['articles'] })
      toast.success(`Article "${article.title}" has been generated!`)
    }

    // Set up event listeners
    wsService.onPipelineProgress(handlePipelineProgress)
    wsService.onAgentStatusUpdate(handleAgentStatusUpdate)
    wsService.onSystemAlert(handleSystemAlert)
    wsService.onArticleComplete(handleArticleComplete)

    // Cleanup on unmount
    return () => {
      wsService.offPipelineProgress()
      wsService.offAgentStatusUpdate()
      wsService.offSystemAlert()
      wsService.offArticleComplete()
      wsService.disconnect()
    }
  }, [queryClient])

  const joinPipelineRoom = useCallback((pipelineId: string) => {
    wsService.joinPipelineRoom(pipelineId)
  }, [])

  const leavePipelineRoom = useCallback((pipelineId: string) => {
    wsService.leavePipelineRoom(pipelineId)
  }, [])

  return {
    isConnected: wsService.isConnected(),
    joinPipelineRoom,
    leavePipelineRoom,
  }
}

// Hook for monitoring specific pipeline progress
export function usePipelineProgress(pipelineId: string) {
  const queryClient = useQueryClient()

  useEffect(() => {
    if (!pipelineId) return

    wsService.joinPipelineRoom(pipelineId)

    return () => {
      wsService.leavePipelineRoom(pipelineId)
    }
  }, [pipelineId])

  return useCallback((progress: PipelineProgress) => {
    if (progress.pipelineId === pipelineId) {
      queryClient.setQueryData(['pipeline', pipelineId], (oldData: any) => {
        if (oldData?.data) {
          return {
            ...oldData,
            data: {
              ...oldData.data,
              progress: progress.progress,
              currentAgent: progress.stage,
            }
          }
        }
        return oldData
      })
    }
  }, [pipelineId, queryClient])
}
```

### Loading States and Error Boundaries

```typescript
// src/components/LoadingSpinner.tsx
import { cn } from '@/lib/utils'

interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg'
  className?: string
}

export function LoadingSpinner({ size = 'md', className }: LoadingSpinnerProps) {
  const sizeClasses = {
    sm: 'h-4 w-4',
    md: 'h-8 w-8',
    lg: 'h-12 w-12',
  }

  return (
    <div className={cn('animate-spin rounded-full border-2 border-primary-200 border-t-primary-600', sizeClasses[size], className)} />
  )
}

// src/components/ErrorBoundary.tsx
import { Component, ErrorInfo, ReactNode } from 'react'
import { AlertTriangle, RefreshCw } from 'lucide-react'

interface Props {
  children: ReactNode
}

interface State {
  hasError: boolean
  error?: Error
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
  }

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error }
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Uncaught error:', error, errorInfo)
  }

  public render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900">
          <div className="text-center">
            <AlertTriangle className="h-16 w-16 text-red-500 mx-auto mb-4" />
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
              Something went wrong
            </h1>
            <p className="text-gray-600 dark:text-gray-400 mb-4">
              {this.state.error?.message || 'An unexpected error occurred'}
            </p>
            <button
              onClick={() => window.location.reload()}
              className="inline-flex items-center space-x-2 bg-purple-gradient text-white px-4 py-2 rounded-md hover:opacity-90"
            >
              <RefreshCw className="h-4 w-4" />
              <span>Reload Page</span>
            </button>
          </div>
        </div>
      )
    }

    return this.props.children
  }
}

// src/components/ConnectionStatus.tsx
import { Wifi, WifiOff } from 'lucide-react'
import { useWebSocketConnection } from '@/hooks/useWebSocket'

export function ConnectionStatus() {
  const { isConnected } = useWebSocketConnection()

  if (isConnected) return null

  return (
    <div className="fixed bottom-4 right-4 bg-yellow-100 border border-yellow-400 text-yellow-700 px-4 py-2 rounded-lg shadow-lg flex items-center space-x-2">
      <WifiOff className="h-4 w-4" />
      <span className="text-sm">Connection lost - using cached data</span>
    </div>
  )
}
```

### Updated App.tsx with Error Boundary and WebSocket

```typescript
// src/App.tsx (updated)
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
import { Toaster } from 'react-hot-toast'
import { ThemeProvider } from '@/contexts/ThemeContext'
import { AuthProvider } from '@/contexts/AuthContext'
import { ErrorBoundary } from '@/components/ErrorBoundary'
import { ConnectionStatus } from '@/components/ConnectionStatus'
import { Layout } from '@/components/Layout'
import { ProtectedRoute } from '@/components/ProtectedRoute'
import { useWebSocketConnection } from '@/hooks/useWebSocket'

// Pages
import Login from '@/pages/Login'
import Register from '@/pages/Register'
import Dashboard from '@/pages/Dashboard'
import Pipeline from '@/pages/Pipeline'
import Articles from '@/pages/Articles'
import ArticleDetail from '@/pages/ArticleDetail'
import Monitoring from '@/pages/Monitoring'
import Settings from '@/pages/Settings'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60 * 1000, // 1 minute
      refetchOnWindowFocus: false,
      retry: (failureCount, error) => {
        // Don't retry on 4xx errors
        if (error instanceof Error && error.message.includes('4')) {
          return false
        }
        return failureCount < 3
      },
    },
    mutations: {
      retry: 1,
    },
  },
})

function AppContent() {
  useWebSocketConnection()

  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Layout />
            </ProtectedRoute>
          }
        >
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="pipeline" element={<Pipeline />} />
          <Route path="articles" element={<Articles />} />
          <Route path="articles/:id" element={<ArticleDetail />} />
          <Route path="monitoring" element={<Monitoring />} />
          <Route path="settings" element={<Settings />} />
        </Route>
      </Routes>
      <ConnectionStatus />
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: '#363636',
            color: '#fff',
          },
          success: {
            style: {
              background: '#10b981',
            },
          },
          error: {
            style: {
              background: '#ef4444',
            },
          },
        }}
      />
    </Router>
  )
}

function App() {
  return (
    <ErrorBoundary>
      <QueryClientProvider client={queryClient}>
        <ThemeProvider>
          <AuthProvider>
            <AppContent />
          </AuthProvider>
        </ThemeProvider>
        <ReactQueryDevtools initialIsOpen={false} />
      </QueryClientProvider>
    </ErrorBoundary>
  )
}

export default App
```

**Success Criteria:**
- Complete API service layer with TypeScript interfaces
- WebSocket integration for real-time updates
- Robust error handling with fallback to mock data
- React Query hooks for data management
- Loading states and error boundaries
- Connection status monitoring
- Optimistic updates and cache invalidation
- Toast notifications for user feedback
- Retry logic and graceful degradation

This implementation provides a production-ready API integration layer that gracefully handles network issues, provides real-time updates, and maintains excellent user experience even when the backend is unavailable.
# Lovable Prompt: Pipeline Management System

## Business Context:
The pipeline management system is the orchestration center for Blog-Poster's 5-agent content generation workflow. It provides real-time monitoring, configuration, and control over the automated content creation process, ensuring quality SEO content while managing costs and tracking performance.

## User Story:
"As a content manager, I want to initiate, monitor, and manage the 5-agent content generation pipeline in real-time, with the ability to configure agents, track costs, view execution logs, and intervene when necessary to ensure quality output."

## Pipeline Requirements:
- **5-Agent Orchestration**: Sequential execution of Competitor Monitoring → Topic Analysis → Article Generation → Legal Fact Checker → WordPress Publishing
- **Real-time WebSocket Updates**: Live progress tracking and log streaming
- **Cost Monitoring**: Per-execution cost tracking with budget controls
- **Agent Configuration**: Individual agent parameters and settings
- **Execution History**: Searchable log of past pipeline runs

## Prompt for Lovable:

Create a comprehensive pipeline management system for the Blog-Poster platform that orchestrates 5 AI agents in sequence to generate legally-compliant, SEO-optimized articles. The system provides real-time monitoring, cost tracking, and detailed execution logs.

**Pipeline Management Components:**

### Main Pipeline Page
```typescript
// src/pages/Pipeline.tsx
import { useState, useEffect } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { apiClient } from '@/services/api'
import { PipelineConfiguration } from '@/components/pipeline/PipelineConfiguration'
import { ExecutionMonitor } from '@/components/pipeline/ExecutionMonitor'
import { PipelineHistory } from '@/components/pipeline/PipelineHistory'
import { AgentStatus } from '@/components/pipeline/AgentStatus'
import { CostTracker } from '@/components/pipeline/CostTracker'
import { ExecutionLogs } from '@/components/pipeline/ExecutionLogs'
import { Play, Square, Settings, History, DollarSign } from 'lucide-react'
import { useWebSocket } from '@/hooks/useWebSocket'
import toast from 'react-hot-toast'

interface PipelineExecution {
  id: string
  status: 'pending' | 'running' | 'completed' | 'failed' | 'cancelled'
  currentAgent: string | null
  agentsCompleted: string[]
  startedAt: string
  completedAt: string | null
  totalCost: number
  estimatedCost: number
  configuration: PipelineConfig
  articleId: string | null
  logs: ExecutionLog[]
  errorMessage: string | null
}

interface PipelineConfig {
  topic: string
  targetKeywords: string[]
  competitorUrls: string[]
  wordCountMin: number
  wordCountMax: number
  seoOptimization: boolean
  legalReview: boolean
  autoPublish: boolean
  wordpressSiteId: string | null
  budgetLimit: number
}

export default function Pipeline() {
  const [activeTab, setActiveTab] = useState<'monitor' | 'config' | 'history' | 'logs'>('monitor')
  const [currentExecution, setCurrentExecution] = useState<PipelineExecution | null>(null)
  const queryClient = useQueryClient()

  // WebSocket connection for real-time updates
  const { isConnected, lastMessage } = useWebSocket('/ws/pipeline', {
    onMessage: (data) => {
      if (data.type === 'execution_update') {
        setCurrentExecution(data.execution)
        queryClient.invalidateQueries({ queryKey: ['pipeline-execution'] })
      } else if (data.type === 'agent_progress') {
        toast.success(`${data.agent} completed successfully`)
      } else if (data.type === 'execution_error') {
        toast.error(`Pipeline failed: ${data.error}`)
      }
    }
  })

  // Query current execution
  const { data: execution, isLoading } = useQuery({
    queryKey: ['pipeline-execution', 'current'],
    queryFn: () => apiClient.get<PipelineExecution>('/api/pipeline/current'),
    refetchInterval: currentExecution?.status === 'running' ? 5000 : 30000,
  })

  // Start pipeline mutation
  const startPipelineMutation = useMutation({
    mutationFn: (config: PipelineConfig) => 
      apiClient.post('/api/pipeline/start', config),
    onSuccess: (data) => {
      setCurrentExecution(data)
      toast.success('Pipeline started successfully!')
      setActiveTab('monitor')
    },
    onError: (error: any) => {
      toast.error(`Failed to start pipeline: ${error.message}`)
    }
  })

  // Stop pipeline mutation
  const stopPipelineMutation = useMutation({
    mutationFn: (executionId: string) => 
      apiClient.post(`/api/pipeline/${executionId}/stop`),
    onSuccess: () => {
      toast.success('Pipeline stopped')
      setCurrentExecution(null)
    }
  })

  const isRunning = currentExecution?.status === 'running'
  const canStart = !isRunning && isConnected

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            Content Pipeline
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Orchestrate 5 AI agents to generate SEO-optimized articles
          </p>
        </div>

        {/* Connection Status */}
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <div className={`h-2 w-2 rounded-full ${
              isConnected ? 'bg-green-500' : 'bg-red-500'
            }`} />
            <span className="text-sm text-gray-600 dark:text-gray-400">
              {isConnected ? 'Connected' : 'Disconnected'}
            </span>
          </div>

          {/* Pipeline Controls */}
          <div className="flex items-center gap-2">
            {isRunning ? (
              <button
                onClick={() => stopPipelineMutation.mutate(currentExecution.id)}
                className="inline-flex items-center px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
                disabled={stopPipelineMutation.isPending}
              >
                <Square className="h-4 w-4 mr-2" />
                Stop Pipeline
              </button>
            ) : (
              <button
                onClick={() => setActiveTab('config')}
                className="inline-flex items-center px-4 py-2 bg-purple-gradient text-white rounded-lg hover:opacity-90"
                disabled={!canStart}
              >
                <Play className="h-4 w-4 mr-2" />
                Start Pipeline
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Tab Navigation */}
      <div className="flex space-x-1 mb-6">
        {[
          { id: 'monitor', label: 'Monitor', icon: Play },
          { id: 'config', label: 'Configuration', icon: Settings },
          { id: 'history', label: 'History', icon: History },
          { id: 'logs', label: 'Logs', icon: DollarSign },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`flex items-center px-4 py-2 rounded-lg font-medium transition-colors ${
              activeTab === tab.id
                ? 'bg-purple-100 dark:bg-purple-900 text-purple-700 dark:text-purple-300'
                : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800'
            }`}
          >
            <tab.icon className="h-4 w-4 mr-2" />
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div className="space-y-6">
        {activeTab === 'monitor' && (
          <>
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Execution Monitor */}
              <div className="lg:col-span-2">
                <ExecutionMonitor 
                  execution={currentExecution || execution} 
                  isLoading={isLoading} 
                />
              </div>

              {/* Cost Tracker */}
              <div>
                <CostTracker execution={currentExecution || execution} />
              </div>
            </div>

            {/* Agent Status Grid */}
            <AgentStatus 
              execution={currentExecution || execution}
              isConnected={isConnected}
            />
          </>
        )}

        {activeTab === 'config' && (
          <PipelineConfiguration
            onStart={(config) => startPipelineMutation.mutate(config)}
            isStarting={startPipelineMutation.isPending}
            disabled={isRunning}
          />
        )}

        {activeTab === 'history' && (
          <PipelineHistory />
        )}

        {activeTab === 'logs' && (
          <ExecutionLogs 
            executionId={currentExecution?.id || execution?.id}
            isLive={isRunning}
          />
        )}
      </div>
    </div>
  )
}
```

### Execution Monitor Component
```typescript
// src/components/pipeline/ExecutionMonitor.tsx
import { useState } from 'react'
import { 
  Play, 
  CheckCircle2, 
  XCircle, 
  Clock, 
  Loader2,
  AlertTriangle,
  Eye
} from 'lucide-react'
import { formatDistanceToNow } from 'date-fns'

const AGENTS = [
  { 
    id: 'competitor_monitoring', 
    name: 'Competitor Monitor', 
    icon: '🔍',
    description: 'Analyzes competitor content and identifies gaps',
    avgDuration: 45 
  },
  { 
    id: 'topic_analysis', 
    name: 'Topic Analyzer', 
    icon: '📊',
    description: 'Extracts SEO opportunities and content structure',
    avgDuration: 30
  },
  { 
    id: 'article_generation', 
    name: 'Article Generator', 
    icon: '✍️',
    description: 'Creates SEO-optimized content using Claude 3.5 Sonnet',
    avgDuration: 120
  },
  { 
    id: 'legal_fact_checker', 
    name: 'Legal Fact Checker', 
    icon: '⚖️',
    description: 'Verifies ADA compliance claims and legal accuracy',
    avgDuration: 60
  },
  { 
    id: 'wordpress_publishing', 
    name: 'WordPress Publisher', 
    icon: '🚀',
    description: 'Publishes content with proper formatting and SEO',
    avgDuration: 20
  },
]

interface ExecutionMonitorProps {
  execution: PipelineExecution | null
  isLoading: boolean
}

export function ExecutionMonitor({ execution, isLoading }: ExecutionMonitorProps) {
  const [expandedAgent, setExpandedAgent] = useState<string | null>(null)

  if (isLoading) {
    return <ExecutionMonitorSkeleton />
  }

  if (!execution) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-xl p-8 shadow-sm border border-gray-200 dark:border-gray-700">
        <div className="text-center">
          <Play className="h-16 w-16 text-gray-300 dark:text-gray-600 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
            No Active Pipeline
          </h3>
          <p className="text-gray-600 dark:text-gray-400 mb-4">
            Start a new pipeline to begin generating content
          </p>
        </div>
      </div>
    )
  }

  const getExecutionProgress = () => {
    const totalAgents = AGENTS.length
    const completedAgents = execution.agentsCompleted.length
    return Math.round((completedAgents / totalAgents) * 100)
  }

  const getExecutionDuration = () => {
    const start = new Date(execution.startedAt)
    const end = execution.completedAt ? new Date(execution.completedAt) : new Date()
    return end.getTime() - start.getTime()
  }

  const formatDuration = (ms: number) => {
    const seconds = Math.floor(ms / 1000)
    const minutes = Math.floor(seconds / 60)
    const remainingSeconds = seconds % 60
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700">
      {/* Execution Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
            Pipeline Execution
          </h3>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            Started {formatDistanceToNow(new Date(execution.startedAt), { addSuffix: true })}
          </p>
        </div>
        
        <div className="text-right">
          <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
            execution.status === 'running' 
              ? 'bg-blue-100 text-blue-700 dark:bg-blue-900/20 dark:text-blue-400'
              : execution.status === 'completed'
              ? 'bg-green-100 text-green-700 dark:bg-green-900/20 dark:text-green-400'
              : execution.status === 'failed'
              ? 'bg-red-100 text-red-700 dark:bg-red-900/20 dark:text-red-400'
              : 'bg-gray-100 text-gray-700 dark:bg-gray-900/20 dark:text-gray-400'
          }`}>
            {execution.status === 'running' && <Loader2 className="h-3 w-3 mr-1 animate-spin" />}
            {execution.status === 'completed' && <CheckCircle2 className="h-3 w-3 mr-1" />}
            {execution.status === 'failed' && <XCircle className="h-3 w-3 mr-1" />}
            {execution.status.toUpperCase()}
          </div>
          <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
            Duration: {formatDuration(getExecutionDuration())}
          </p>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
            Overall Progress
          </span>
          <span className="text-sm text-gray-600 dark:text-gray-400">
            {getExecutionProgress()}%
          </span>
        </div>
        <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
          <div 
            className="bg-purple-600 h-2 rounded-full transition-all duration-500"
            style={{ width: `${getExecutionProgress()}%` }}
          />
        </div>
      </div>

      {/* Agent Progress */}
      <div className="space-y-3">
        {AGENTS.map((agent, index) => {
          const isCompleted = execution.agentsCompleted.includes(agent.id)
          const isCurrent = execution.currentAgent === agent.id
          const isFailed = execution.status === 'failed' && isCurrent
          const isExpanded = expandedAgent === agent.id
          
          return (
            <div 
              key={agent.id} 
              className="border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden"
            >
              <div 
                className="flex items-center p-4 cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-900"
                onClick={() => setExpandedAgent(isExpanded ? null : agent.id)}
              >
                <div className="flex items-center flex-1">
                  <span className="text-2xl mr-3">{agent.icon}</span>
                  <div className="flex-1">
                    <div className="flex items-center justify-between mb-1">
                      <h4 className="font-medium text-gray-900 dark:text-white">
                        {agent.name}
                      </h4>
                      <div className="flex items-center gap-2">
                        {isCompleted && (
                          <CheckCircle2 className="h-4 w-4 text-green-500" />
                        )}
                        {isCurrent && !isFailed && (
                          <Loader2 className="h-4 w-4 text-blue-500 animate-spin" />
                        )}
                        {isFailed && (
                          <XCircle className="h-4 w-4 text-red-500" />
                        )}
                        <Eye className="h-4 w-4 text-gray-400" />
                      </div>
                    </div>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      {agent.description}
                    </p>
                    
                    {/* Agent Progress Bar */}
                    <div className="mt-2 w-full bg-gray-200 dark:bg-gray-700 rounded-full h-1">
                      <div 
                        className={`h-1 rounded-full transition-all duration-500 ${
                          isCompleted 
                            ? 'bg-green-500 w-full'
                            : isCurrent
                            ? 'bg-blue-500 w-1/2 animate-pulse'
                            : isFailed
                            ? 'bg-red-500 w-1/2'
                            : 'bg-gray-300 w-0'
                        }`}
                      />
                    </div>
                  </div>
                </div>
              </div>
              
              {/* Expanded Agent Details */}
              {isExpanded && (
                <div className="px-4 pb-4 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900">
                  <div className="grid grid-cols-2 gap-4 mt-4">
                    <div>
                      <p className="text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">
                        Expected Duration
                      </p>
                      <p className="text-sm text-gray-900 dark:text-white">
                        ~{agent.avgDuration}s
                      </p>
                    </div>
                    <div>
                      <p className="text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">
                        Status
                      </p>
                      <p className="text-sm text-gray-900 dark:text-white">
                        {isCompleted ? 'Completed' : isCurrent ? 'In Progress' : 'Pending'}
                      </p>
                    </div>
                  </div>
                  
                  {/* Agent-specific output preview */}
                  {isCompleted && (
                    <div className="mt-3">
                      <p className="text-xs font-medium text-gray-600 dark:text-gray-400 mb-2">
                        Output Preview
                      </p>
                      <div className="bg-white dark:bg-gray-800 rounded p-3 text-xs">
                        <code className="text-gray-700 dark:text-gray-300">
                          Agent completed successfully. View full output in logs.
                        </code>
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          )
        })}
      </div>

      {/* Error Message */}
      {execution.errorMessage && (
        <div className="mt-6 p-4 bg-red-50 dark:bg-red-900/20 rounded-lg border border-red-200 dark:border-red-800">
          <div className="flex items-start">
            <AlertTriangle className="h-5 w-5 text-red-600 dark:text-red-400 mr-3 mt-0.5" />
            <div>
              <p className="text-sm font-medium text-red-700 dark:text-red-300">
                Pipeline Failed
              </p>
              <p className="text-sm text-red-600 dark:text-red-400 mt-1">
                {execution.errorMessage}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Generated Article Preview */}
      {execution.status === 'completed' && execution.articleId && (
        <div className="mt-6 p-4 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-800">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-green-700 dark:text-green-300">
                Article Generated Successfully!
              </p>
              <p className="text-sm text-green-600 dark:text-green-400 mt-1">
                Your article has been created and is ready for review.
              </p>
            </div>
            <button className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700">
              View Article
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

function ExecutionMonitorSkeleton() {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700">
      <div className="animate-pulse space-y-6">
        <div className="flex items-center justify-between">
          <div className="space-y-2">
            <div className="h-6 bg-gray-200 dark:bg-gray-700 rounded w-32" />
            <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-24" />
          </div>
          <div className="h-6 bg-gray-200 dark:bg-gray-700 rounded w-20" />
        </div>
        
        <div className="space-y-2">
          <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-24" />
          <div className="h-2 bg-gray-200 dark:bg-gray-700 rounded" />
        </div>
        
        {Array.from({ length: 5 }).map((_, i) => (
          <div key={i} className="flex items-center space-x-3">
            <div className="h-8 w-8 bg-gray-200 dark:bg-gray-700 rounded" />
            <div className="flex-1 space-y-2">
              <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-32" />
              <div className="h-1 bg-gray-200 dark:bg-gray-700 rounded" />
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
```

### WebSocket Hook for Real-time Updates
```typescript
// src/hooks/useWebSocket.tsx
import { useEffect, useRef, useState } from 'react'
import { supabase } from '@/services/supabase'

interface UseWebSocketOptions {
  onMessage?: (data: any) => void
  onConnect?: () => void
  onDisconnect?: () => void
  reconnectInterval?: number
}

export function useWebSocket(url: string, options: UseWebSocketOptions = {}) {
  const [isConnected, setIsConnected] = useState(false)
  const [lastMessage, setLastMessage] = useState<any>(null)
  const wsRef = useRef<WebSocket | null>(null)
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null)

  const {
    onMessage,
    onConnect,
    onDisconnect,
    reconnectInterval = 5000
  } = options

  const connect = async () => {
    try {
      // Get auth token
      const { data: { session } } = await supabase.auth.getSession()
      const token = session?.access_token

      // Build WebSocket URL
      const wsUrl = url.startsWith('ws') 
        ? url 
        : `${import.meta.env.VITE_WS_URL || 'ws://localhost:8088'}${url}`
      
      const ws = new WebSocket(`${wsUrl}${token ? `?token=${token}` : ''}`)
      
      ws.onopen = () => {
        setIsConnected(true)
        onConnect?.()
        
        // Clear any pending reconnection
        if (reconnectTimeoutRef.current) {
          clearTimeout(reconnectTimeoutRef.current)
          reconnectTimeoutRef.current = null
        }
      }

      ws.onmessage = (event) => {
        const data = JSON.parse(event.data)
        setLastMessage(data)
        onMessage?.(data)
      }

      ws.onclose = () => {
        setIsConnected(false)
        onDisconnect?.()
        
        // Schedule reconnection
        reconnectTimeoutRef.current = setTimeout(() => {
          connect()
        }, reconnectInterval)
      }

      ws.onerror = (error) => {
        console.error('WebSocket error:', error)
        setIsConnected(false)
      }

      wsRef.current = ws
    } catch (error) {
      console.error('Failed to connect WebSocket:', error)
      setIsConnected(false)
      
      // Schedule reconnection
      reconnectTimeoutRef.current = setTimeout(() => {
        connect()
      }, reconnectInterval)
    }
  }

  const disconnect = () => {
    if (wsRef.current) {
      wsRef.current.close()
      wsRef.current = null
    }
    
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current)
      reconnectTimeoutRef.current = null
    }
    
    setIsConnected(false)
  }

  const sendMessage = (data: any) => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(data))
    }
  }

  useEffect(() => {
    connect()

    return () => {
      disconnect()
    }
  }, [url])

  return {
    isConnected,
    lastMessage,
    sendMessage,
    disconnect,
    reconnect: connect
  }
}
```

**Success Criteria:**
- Real-time pipeline execution monitoring with WebSocket updates
- 5-agent workflow visualization with progress indicators
- Cost tracking during execution with budget warnings
- Individual agent configuration and status monitoring
- Searchable execution history with detailed logs
- Pipeline start/stop controls with proper error handling
- Mobile-responsive design with collapsible agent details
- Integration with existing authentication and API systems

This pipeline management system provides comprehensive control and visibility over the Blog-Poster's content generation workflow, enabling efficient monitoring and management of the 5-agent orchestration process.
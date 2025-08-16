# Lovable Prompt: Pipeline Management System (Revised - Works with Existing Infrastructure)

## Business Context:
The pipeline management system is the orchestration center for Blog-Poster's 5-agent content generation workflow. This implementation extends the existing database schema and components rather than replacing them.

## User Story:
"As a content manager, I want to initiate, monitor, and manage the 5-agent content generation pipeline in real-time, with the ability to configure agents, track costs, view execution logs, and intervene when necessary to ensure quality output."

## Prompt for Lovable:

Create a comprehensive pipeline management system that extends the existing infrastructure. The database already has a `pipelines` table with all necessary fields. Build upon the existing `PipelineStatus` component and use the current authentication context.

**First, extend the existing types if needed:**

### Update Types (if not already present)
```typescript
// Add to src/types/index.ts (only if these don't exist)

export interface PipelineConfig {
  topic: string
  targetKeywords: string[]
  competitorUrls: string[]
  wordCountMin: number
  wordCountMax: number
  seoOptimization: boolean
  legalReview: boolean
  autoPublish: boolean
  wordpressSiteId?: string | null
  budgetLimit: number
}

export interface AgentStatus {
  name: string
  status: 'pending' | 'running' | 'completed' | 'failed'
  progress: number
  startedAt?: string
  completedAt?: string
  cost?: number
  output?: any
  error?: string
}
```

**Create the missing component files:**

### Pipeline Configuration Component
```typescript
// src/components/pipeline/PipelineConfiguration.tsx
import { useState } from 'react'
import { supabase } from '@/lib/supabase'
import { useAuth } from '@/contexts/AuthContext'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Switch } from '@/components/ui/switch'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Loader2, AlertCircle } from 'lucide-react'
import toast from 'react-hot-toast'

interface PipelineConfigurationProps {
  onStart: (config: any) => void
  isStarting: boolean
  disabled?: boolean
  organizationId?: string
}

export function PipelineConfiguration({ 
  onStart, 
  isStarting, 
  disabled,
  organizationId 
}: PipelineConfigurationProps) {
  const { user } = useAuth()
  const [config, setConfig] = useState({
    topic: '',
    targetKeywords: [] as string[],
    competitorUrls: [] as string[],
    wordCountMin: 1500,
    wordCountMax: 2500,
    seoOptimization: true,
    legalReview: true,
    autoPublish: false,
    budgetLimit: 5.00
  })
  const [keywordInput, setKeywordInput] = useState('')
  const [urlInput, setUrlInput] = useState('')

  const handleAddKeyword = () => {
    if (keywordInput.trim() && !config.targetKeywords.includes(keywordInput.trim())) {
      setConfig(prev => ({
        ...prev,
        targetKeywords: [...prev.targetKeywords, keywordInput.trim()]
      }))
      setKeywordInput('')
    }
  }

  const handleAddUrl = () => {
    if (urlInput.trim() && !config.competitorUrls.includes(urlInput.trim())) {
      setConfig(prev => ({
        ...prev,
        competitorUrls: [...prev.competitorUrls, urlInput.trim()]
      }))
      setUrlInput('')
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!config.topic) {
      toast.error('Please enter a topic')
      return
    }

    if (config.targetKeywords.length === 0) {
      toast.error('Please add at least one target keyword')
      return
    }

    onStart(config)
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Pipeline Configuration</CardTitle>
        <CardDescription>
          Configure your content generation pipeline settings
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Topic Input */}
          <div className="space-y-2">
            <Label htmlFor="topic">Content Topic *</Label>
            <Input
              id="topic"
              value={config.topic}
              onChange={(e) => setConfig(prev => ({ ...prev, topic: e.target.value }))}
              placeholder="e.g., Service Dog Training Tips"
              disabled={disabled || isStarting}
            />
          </div>

          {/* Target Keywords */}
          <div className="space-y-2">
            <Label>Target Keywords *</Label>
            <div className="flex gap-2">
              <Input
                value={keywordInput}
                onChange={(e) => setKeywordInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), handleAddKeyword())}
                placeholder="Add a keyword"
                disabled={disabled || isStarting}
              />
              <Button 
                type="button" 
                onClick={handleAddKeyword}
                disabled={disabled || isStarting}
              >
                Add
              </Button>
            </div>
            <div className="flex flex-wrap gap-2 mt-2">
              {config.targetKeywords.map((keyword, index) => (
                <span
                  key={index}
                  className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm"
                >
                  {keyword}
                  <button
                    type="button"
                    onClick={() => setConfig(prev => ({
                      ...prev,
                      targetKeywords: prev.targetKeywords.filter((_, i) => i !== index)
                    }))}
                    className="ml-2 text-blue-500 hover:text-blue-700"
                    disabled={disabled || isStarting}
                  >
                    ×
                  </button>
                </span>
              ))}
            </div>
          </div>

          {/* Competitor URLs */}
          <div className="space-y-2">
            <Label>Competitor URLs (Optional)</Label>
            <div className="flex gap-2">
              <Input
                value={urlInput}
                onChange={(e) => setUrlInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), handleAddUrl())}
                placeholder="https://competitor.com/article"
                disabled={disabled || isStarting}
              />
              <Button 
                type="button" 
                onClick={handleAddUrl}
                disabled={disabled || isStarting}
              >
                Add
              </Button>
            </div>
            <div className="space-y-1 mt-2">
              {config.competitorUrls.map((url, index) => (
                <div key={index} className="flex items-center gap-2 text-sm">
                  <span className="text-gray-600 truncate flex-1">{url}</span>
                  <button
                    type="button"
                    onClick={() => setConfig(prev => ({
                      ...prev,
                      competitorUrls: prev.competitorUrls.filter((_, i) => i !== index)
                    }))}
                    className="text-red-500 hover:text-red-700"
                    disabled={disabled || isStarting}
                  >
                    Remove
                  </button>
                </div>
              ))}
            </div>
          </div>

          {/* Word Count */}
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="wordCountMin">Min Word Count</Label>
              <Input
                id="wordCountMin"
                type="number"
                value={config.wordCountMin}
                onChange={(e) => setConfig(prev => ({ 
                  ...prev, 
                  wordCountMin: parseInt(e.target.value) || 0 
                }))}
                disabled={disabled || isStarting}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="wordCountMax">Max Word Count</Label>
              <Input
                id="wordCountMax"
                type="number"
                value={config.wordCountMax}
                onChange={(e) => setConfig(prev => ({ 
                  ...prev, 
                  wordCountMax: parseInt(e.target.value) || 0 
                }))}
                disabled={disabled || isStarting}
              />
            </div>
          </div>

          {/* Options */}
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <Label htmlFor="seo">SEO Optimization</Label>
              <Switch
                id="seo"
                checked={config.seoOptimization}
                onCheckedChange={(checked) => setConfig(prev => ({ 
                  ...prev, 
                  seoOptimization: checked 
                }))}
                disabled={disabled || isStarting}
              />
            </div>
            <div className="flex items-center justify-between">
              <Label htmlFor="legal">Legal Review</Label>
              <Switch
                id="legal"
                checked={config.legalReview}
                onCheckedChange={(checked) => setConfig(prev => ({ 
                  ...prev, 
                  legalReview: checked 
                }))}
                disabled={disabled || isStarting}
              />
            </div>
            <div className="flex items-center justify-between">
              <Label htmlFor="autoPublish">Auto-Publish</Label>
              <Switch
                id="autoPublish"
                checked={config.autoPublish}
                onCheckedChange={(checked) => setConfig(prev => ({ 
                  ...prev, 
                  autoPublish: checked 
                }))}
                disabled={disabled || isStarting}
              />
            </div>
          </div>

          {/* Budget Limit */}
          <div className="space-y-2">
            <Label htmlFor="budget">Budget Limit ($)</Label>
            <Input
              id="budget"
              type="number"
              step="0.01"
              value={config.budgetLimit}
              onChange={(e) => setConfig(prev => ({ 
                ...prev, 
                budgetLimit: parseFloat(e.target.value) || 0 
              }))}
              disabled={disabled || isStarting}
            />
            <p className="text-sm text-gray-500">
              Estimated cost will be calculated based on configuration
            </p>
          </div>

          {/* Submit Button */}
          <Button
            type="submit"
            className="w-full"
            disabled={disabled || isStarting}
          >
            {isStarting ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Starting Pipeline...
              </>
            ) : (
              'Start Pipeline'
            )}
          </Button>
        </form>
      </CardContent>
    </Card>
  )
}
```

### Execution Monitor Component
```typescript
// src/components/pipeline/ExecutionMonitor.tsx
import { useState, useEffect } from 'react'
import { supabase } from '@/lib/supabase'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'
import { Badge } from '@/components/ui/badge'
import { ScrollArea } from '@/components/ui/scroll-area'
import { 
  Play, 
  CheckCircle2, 
  XCircle, 
  Clock, 
  Loader2,
  AlertTriangle,
  ChevronDown,
  ChevronRight
} from 'lucide-react'
import { formatDistanceToNow } from 'date-fns'
import { cn } from '@/lib/utils'

const AGENTS = [
  { 
    id: 'competitor_monitoring', 
    name: 'Competitor Monitor', 
    icon: '🔍',
    description: 'Analyzes competitor content and identifies gaps'
  },
  { 
    id: 'topic_analysis', 
    name: 'Topic Analyzer', 
    icon: '📊',
    description: 'Extracts SEO opportunities and content structure'
  },
  { 
    id: 'article_generation', 
    name: 'Article Generator', 
    icon: '✍️',
    description: 'Creates SEO-optimized content'
  },
  { 
    id: 'legal_fact_checker', 
    name: 'Legal Fact Checker', 
    icon: '⚖️',
    description: 'Verifies ADA compliance claims and legal accuracy'
  },
  { 
    id: 'wordpress_publishing', 
    name: 'WordPress Publisher', 
    icon: '🚀',
    description: 'Publishes content with proper formatting and SEO'
  },
]

interface ExecutionMonitorProps {
  execution: any
  isLoading?: boolean
}

export function ExecutionMonitor({ execution, isLoading }: ExecutionMonitorProps) {
  const [expandedAgent, setExpandedAgent] = useState<string | null>(null)
  const [agentStatuses, setAgentStatuses] = useState<Record<string, any>>({})

  useEffect(() => {
    if (execution?.agent_status) {
      setAgentStatuses(execution.agent_status)
    }
  }, [execution])

  if (isLoading) {
    return (
      <Card>
        <CardContent className="p-6">
          <div className="flex items-center justify-center">
            <Loader2 className="h-8 w-8 animate-spin text-gray-400" />
          </div>
        </CardContent>
      </Card>
    )
  }

  if (!execution) {
    return (
      <Card>
        <CardContent className="p-8">
          <div className="text-center">
            <Play className="h-16 w-16 text-gray-300 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              No Active Pipeline
            </h3>
            <p className="text-gray-600">
              Start a new pipeline to begin generating content
            </p>
          </div>
        </CardContent>
      </Card>
    )
  }

  const getProgress = () => {
    const completedAgents = execution.agents_completed || []
    return Math.round((completedAgents.length / AGENTS.length) * 100)
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle2 className="h-4 w-4 text-green-500" />
      case 'running':
        return <Loader2 className="h-4 w-4 text-blue-500 animate-spin" />
      case 'failed':
        return <XCircle className="h-4 w-4 text-red-500" />
      default:
        return <Clock className="h-4 w-4 text-gray-400" />
    }
  }

  const getStatusBadge = (status: string) => {
    const variants: Record<string, string> = {
      pending: 'secondary',
      running: 'default',
      completed: 'success',
      failed: 'destructive',
      cancelled: 'outline'
    }
    
    return (
      <Badge variant={variants[status] as any}>
        {status.toUpperCase()}
      </Badge>
    )
  }

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle>{execution.name || 'Pipeline Execution'}</CardTitle>
            <CardDescription>
              Started {formatDistanceToNow(new Date(execution.created_at), { addSuffix: true })}
            </CardDescription>
          </div>
          {getStatusBadge(execution.status)}
        </div>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Progress Bar */}
        <div>
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium">Overall Progress</span>
            <span className="text-sm text-gray-600">{getProgress()}%</span>
          </div>
          <Progress value={getProgress()} />
        </div>

        {/* Agent List */}
        <div className="space-y-2">
          {AGENTS.map((agent) => {
            const isCompleted = execution.agents_completed?.includes(agent.id)
            const isCurrent = execution.current_agent === agent.id
            const agentStatus = agentStatuses[agent.id] || {}
            const isExpanded = expandedAgent === agent.id

            return (
              <div
                key={agent.id}
                className={cn(
                  "border rounded-lg transition-colors",
                  isCurrent && "border-blue-500 bg-blue-50",
                  isCompleted && "bg-green-50"
                )}
              >
                <button
                  onClick={() => setExpandedAgent(isExpanded ? null : agent.id)}
                  className="w-full p-4 flex items-center gap-3 text-left hover:bg-gray-50"
                >
                  <span className="text-2xl">{agent.icon}</span>
                  <div className="flex-1">
                    <div className="flex items-center gap-2">
                      <h4 className="font-medium">{agent.name}</h4>
                      {isCompleted && getStatusIcon('completed')}
                      {isCurrent && getStatusIcon('running')}
                    </div>
                    <p className="text-sm text-gray-600">{agent.description}</p>
                  </div>
                  {isExpanded ? <ChevronDown /> : <ChevronRight />}
                </button>

                {/* Expanded Agent Details */}
                {isExpanded && (
                  <div className="px-4 pb-4 border-t">
                    <div className="grid grid-cols-2 gap-4 mt-4">
                      <div>
                        <p className="text-xs font-medium text-gray-600 mb-1">
                          Status
                        </p>
                        <p className="text-sm">
                          {isCompleted ? 'Completed' : isCurrent ? 'Running' : 'Pending'}
                        </p>
                      </div>
                      {agentStatus.cost && (
                        <div>
                          <p className="text-xs font-medium text-gray-600 mb-1">
                            Cost
                          </p>
                          <p className="text-sm">${agentStatus.cost.toFixed(4)}</p>
                        </div>
                      )}
                    </div>
                    
                    {agentStatus.output && (
                      <div className="mt-3">
                        <p className="text-xs font-medium text-gray-600 mb-2">
                          Output Preview
                        </p>
                        <ScrollArea className="h-24 w-full rounded border p-2">
                          <pre className="text-xs">{JSON.stringify(agentStatus.output, null, 2)}</pre>
                        </ScrollArea>
                      </div>
                    )}
                  </div>
                )}
              </div>
            )
          })}
        </div>

        {/* Error Message */}
        {execution.error_message && (
          <Alert variant="destructive">
            <AlertTriangle className="h-4 w-4" />
            <AlertDescription>{execution.error_message}</AlertDescription>
          </Alert>
        )}
      </CardContent>
    </Card>
  )
}
```

### Main Pipeline Page (Extending Existing Components)
```typescript
// src/pages/Pipeline.tsx
import { useState, useEffect } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { motion, AnimatePresence } from 'framer-motion'
import { supabase } from '@/lib/supabase'
import { useAuth } from '@/contexts/AuthContext'
import { PipelineConfiguration } from '@/components/pipeline/PipelineConfiguration'
import { ExecutionMonitor } from '@/components/pipeline/ExecutionMonitor'
import { PipelineStatus } from '@/components/dashboard/PipelineStatus'
import { Button } from '@/components/ui/button'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Play, Square, Settings, History, DollarSign } from 'lucide-react'
import toast from 'react-hot-toast'

export default function Pipeline() {
  const { user, organization } = useAuth()
  const [currentExecution, setCurrentExecution] = useState<any>(null)
  const queryClient = useQueryClient()

  // Set up Supabase real-time subscription
  useEffect(() => {
    if (!organization?.id) return

    // Subscribe to pipeline updates for this organization
    const channel = supabase
      .channel(`pipelines:${organization.id}`)
      .on(
        'postgres_changes',
        {
          event: '*',
          schema: 'public',
          table: 'pipelines',
          filter: `organization_id=eq.${organization.id}`
        },
        (payload) => {
          // Handle real-time updates
          if (payload.eventType === 'UPDATE' || payload.eventType === 'INSERT') {
            const pipeline = payload.new
            
            if (pipeline.status === 'running' || pipeline.status === 'queued') {
              setCurrentExecution(pipeline)
            }
            
            // Show notifications for status changes
            if (payload.eventType === 'UPDATE' && payload.old.status !== pipeline.status) {
              if (pipeline.status === 'completed') {
                toast.success('Pipeline completed successfully!')
              } else if (pipeline.status === 'failed') {
                toast.error(`Pipeline failed: ${pipeline.error_message}`)
              }
            }
            
            // Refresh queries
            queryClient.invalidateQueries({ queryKey: ['pipelines'] })
          }
        }
      )
      .subscribe()

    return () => {
      supabase.removeChannel(channel)
    }
  }, [organization?.id, queryClient])

  // Query current/recent pipeline
  const { data: activePipeline, isLoading } = useQuery({
    queryKey: ['pipelines', 'active', organization?.id],
    queryFn: async () => {
      const { data, error } = await supabase
        .from('pipelines')
        .select('*')
        .eq('organization_id', organization!.id)
        .in('status', ['running', 'queued', 'pending'])
        .order('created_at', { ascending: false })
        .limit(1)
        .maybeSingle()
      
      if (error) throw error
      return data
    },
    enabled: !!organization?.id,
    refetchInterval: currentExecution?.status === 'running' ? 5000 : false,
  })

  // Start pipeline mutation
  const startPipelineMutation = useMutation({
    mutationFn: async (config: any) => {
      const { data, error } = await supabase
        .from('pipelines')
        .insert({
          organization_id: organization!.id,
          user_id: user!.id,
          name: `Pipeline: ${config.topic}`,
          description: `Generate article about "${config.topic}"`,
          status: 'pending',
          config: config,
          estimated_cost: estimateCost(config),
          priority: 5
        })
        .select()
        .single()
      
      if (error) throw error
      
      // TODO: Trigger backend processing via API or Edge Function
      
      return data
    },
    onSuccess: (data) => {
      setCurrentExecution(data)
      toast.success('Pipeline started successfully!')
    },
    onError: (error: any) => {
      toast.error(`Failed to start pipeline: ${error.message}`)
    }
  })

  // Stop pipeline mutation
  const stopPipelineMutation = useMutation({
    mutationFn: async (pipelineId: string) => {
      const { data, error } = await supabase
        .from('pipelines')
        .update({
          status: 'cancelled',
          cancelled_by: user!.id,
          cancellation_reason: 'User requested cancellation',
          completed_at: new Date().toISOString()
        })
        .eq('id', pipelineId)
        .select()
        .single()
      
      if (error) throw error
      return data
    },
    onSuccess: () => {
      toast.success('Pipeline stopped')
      setCurrentExecution(null)
    }
  })

  // Estimate cost helper
  const estimateCost = (config: any): number => {
    const baseCosts = {
      competitor_monitoring: 0.05,
      topic_analysis: 0.03,
      article_generation: 0.15,
      legal_fact_checker: 0.08,
      wordpress_publishing: 0.02,
    }
    
    const wordCountMultiplier = (config.wordCountMax || 2000) / 1500
    let totalCost = Object.values(baseCosts).reduce((sum: number, cost: number) => sum + cost, 0)
    totalCost *= wordCountMultiplier
    
    return Math.round(totalCost * 100) / 100
  }

  const execution = currentExecution || activePipeline
  const isRunning = execution?.status === 'running' || execution?.status === 'queued'

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Content Pipeline</h1>
          <p className="text-gray-600 mt-1">
            Orchestrate 5 AI agents to generate SEO-optimized articles
          </p>
        </div>

        {/* Pipeline Controls */}
        <div className="flex items-center gap-2">
          {isRunning ? (
            <Button
              variant="destructive"
              onClick={() => execution && stopPipelineMutation.mutate(execution.id)}
              disabled={stopPipelineMutation.isPending}
            >
              <Square className="h-4 w-4 mr-2" />
              Stop Pipeline
            </Button>
          ) : (
            <Button
              onClick={() => {
                // Switch to config tab if needed
                const tabsElement = document.querySelector('[role="tablist"]')
                const configTab = tabsElement?.querySelector('[value="config"]') as HTMLElement
                configTab?.click()
              }}
            >
              <Play className="h-4 w-4 mr-2" />
              Start Pipeline
            </Button>
          )}
        </div>
      </div>

      {/* Main Content */}
      <Tabs defaultValue="monitor" className="space-y-6">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="monitor">
            <Play className="h-4 w-4 mr-2" />
            Monitor
          </TabsTrigger>
          <TabsTrigger value="config">
            <Settings className="h-4 w-4 mr-2" />
            Configuration
          </TabsTrigger>
          <TabsTrigger value="history">
            <History className="h-4 w-4 mr-2" />
            History
          </TabsTrigger>
          <TabsTrigger value="costs">
            <DollarSign className="h-4 w-4 mr-2" />
            Costs
          </TabsTrigger>
        </TabsList>

        <TabsContent value="monitor" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2">
              <ExecutionMonitor execution={execution} isLoading={isLoading} />
            </div>
            <div>
              <PipelineStatus />
            </div>
          </div>
        </TabsContent>

        <TabsContent value="config">
          <PipelineConfiguration
            onStart={(config) => startPipelineMutation.mutate(config)}
            isStarting={startPipelineMutation.isPending}
            disabled={isRunning}
            organizationId={organization?.id}
          />
        </TabsContent>

        <TabsContent value="history">
          <PipelineHistory organizationId={organization?.id} />
        </TabsContent>

        <TabsContent value="costs">
          <CostTracker organizationId={organization?.id} />
        </TabsContent>
      </Tabs>
    </div>
  )
}
```

### Pipeline History Component
```typescript
// src/components/pipeline/PipelineHistory.tsx
import { useQuery } from '@tanstack/react-query'
import { supabase } from '@/lib/supabase'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { formatDistanceToNow } from 'date-fns'
import { Eye, Download } from 'lucide-react'

interface PipelineHistoryProps {
  organizationId?: string
}

export function PipelineHistory({ organizationId }: PipelineHistoryProps) {
  const { data: pipelines, isLoading } = useQuery({
    queryKey: ['pipelines', 'history', organizationId],
    queryFn: async () => {
      const { data, error } = await supabase
        .from('pipelines')
        .select('*')
        .eq('organization_id', organizationId)
        .order('created_at', { ascending: false })
        .limit(50)
      
      if (error) throw error
      return data
    },
    enabled: !!organizationId
  })

  if (isLoading) {
    return <div>Loading pipeline history...</div>
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Pipeline History</CardTitle>
        <CardDescription>
          View and manage your past pipeline executions
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {pipelines?.map((pipeline) => (
            <div
              key={pipeline.id}
              className="flex items-center justify-between p-4 border rounded-lg"
            >
              <div className="flex-1">
                <h4 className="font-medium">{pipeline.name}</h4>
                <p className="text-sm text-gray-600">
                  {formatDistanceToNow(new Date(pipeline.created_at), { addSuffix: true })}
                </p>
              </div>
              
              <div className="flex items-center gap-4">
                <Badge variant={
                  pipeline.status === 'completed' ? 'success' :
                  pipeline.status === 'failed' ? 'destructive' :
                  pipeline.status === 'running' ? 'default' :
                  'secondary'
                }>
                  {pipeline.status}
                </Badge>
                
                {pipeline.total_cost > 0 && (
                  <span className="text-sm font-medium">
                    ${pipeline.total_cost.toFixed(2)}
                  </span>
                )}
                
                <Button variant="ghost" size="sm">
                  <Eye className="h-4 w-4" />
                </Button>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
```

### Cost Tracker Component
```typescript
// src/components/pipeline/CostTracker.tsx
import { useQuery } from '@tanstack/react-query'
import { supabase } from '@/lib/supabase'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'

interface CostTrackerProps {
  organizationId?: string
}

export function CostTracker({ organizationId }: CostTrackerProps) {
  const { data: costData } = useQuery({
    queryKey: ['costs', organizationId],
    queryFn: async () => {
      // Get current month's costs
      const startOfMonth = new Date()
      startOfMonth.setDate(1)
      startOfMonth.setHours(0, 0, 0, 0)

      const { data, error } = await supabase
        .from('pipelines')
        .select('total_cost')
        .eq('organization_id', organizationId)
        .gte('created_at', startOfMonth.toISOString())
        .not('total_cost', 'is', null)

      if (error) throw error

      const totalCost = data?.reduce((sum, p) => sum + (p.total_cost || 0), 0) || 0
      
      return {
        monthlyTotal: totalCost,
        budget: 100, // TODO: Get from organization settings
        articlesGenerated: data?.length || 0
      }
    },
    enabled: !!organizationId
  })

  const usagePercentage = costData ? (costData.monthlyTotal / costData.budget) * 100 : 0

  return (
    <Card>
      <CardHeader>
        <CardTitle>Cost Tracking</CardTitle>
        <CardDescription>
          Monitor your monthly usage and costs
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <div className="flex justify-between text-sm mb-2">
            <span>Monthly Usage</span>
            <span className="font-medium">
              ${costData?.monthlyTotal.toFixed(2)} / ${costData?.budget.toFixed(2)}
            </span>
          </div>
          <Progress value={usagePercentage} />
        </div>
        
        <div className="grid grid-cols-2 gap-4 pt-4 border-t">
          <div>
            <p className="text-sm text-gray-600">Articles Generated</p>
            <p className="text-2xl font-bold">{costData?.articlesGenerated || 0}</p>
          </div>
          <div>
            <p className="text-sm text-gray-600">Avg Cost per Article</p>
            <p className="text-2xl font-bold">
              ${costData?.articlesGenerated 
                ? (costData.monthlyTotal / costData.articlesGenerated).toFixed(2)
                : '0.00'}
            </p>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
```

**Success Criteria:**
- ✅ Works with existing `pipelines` table structure
- ✅ Uses existing authentication context from `@/contexts/AuthContext`
- ✅ Extends existing `PipelineStatus` component
- ✅ Uses existing Supabase configuration
- ✅ Compatible with existing type definitions
- ✅ Creates only the missing components
- ✅ Real-time updates via Supabase subscriptions
- ✅ No backend API dependency (uses Supabase directly)

This implementation properly extends your existing infrastructure rather than replacing it, ensuring compatibility with what's already built.
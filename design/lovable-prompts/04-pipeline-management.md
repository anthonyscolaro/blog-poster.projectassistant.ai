# Lovable Prompt: Pipeline Management System (Final - Corrected Imports)

## Business Context:
The pipeline management system is the orchestration center for Blog-Poster's 5-agent content generation workflow. This implementation extends the existing database schema and components, using correct import paths and existing UI components.

## User Story:
"As a content manager, I want to initiate, monitor, and manage the 5-agent content generation pipeline in real-time, with the ability to configure agents, track costs, view execution logs, and intervene when necessary to ensure quality output."

## Prompt for Lovable:

Create a comprehensive pipeline management system that extends the existing infrastructure. Use the existing `pipelines` table and authentication context. Import UI components from the shared component library created in phase 1.

**First, add any missing UI components to the shared library:**

### Add Missing UI Components
```typescript
// Add these to src/components/ui/ if they don't exist:

// Badge Component
// src/components/ui/Badge.tsx
import { cn } from '@/utils/cn'

interface BadgeProps {
  variant?: 'default' | 'secondary' | 'success' | 'destructive' | 'outline'
  className?: string
  children: React.ReactNode
}

const badgeVariants = {
  default: 'bg-purple-100 text-purple-700 dark:bg-purple-900 dark:text-purple-300',
  secondary: 'bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300',
  success: 'bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300',
  destructive: 'bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-300',
  outline: 'border border-gray-300 dark:border-gray-600'
}

export function Badge({ variant = 'default', className, children }: BadgeProps) {
  return (
    <span className={cn(
      'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
      badgeVariants[variant],
      className
    )}>
      {children}
    </span>
  )
}

// Alert Component
// src/components/ui/Alert.tsx
import { cn } from '@/utils/cn'
import { AlertTriangle, Info, CheckCircle, XCircle } from 'lucide-react'

interface AlertProps {
  variant?: 'default' | 'destructive' | 'success' | 'warning'
  className?: string
  children: React.ReactNode
}

const alertVariants = {
  default: 'bg-blue-50 text-blue-900 dark:bg-blue-900/20 dark:text-blue-300 border-blue-200',
  destructive: 'bg-red-50 text-red-900 dark:bg-red-900/20 dark:text-red-300 border-red-200',
  success: 'bg-green-50 text-green-900 dark:bg-green-900/20 dark:text-green-300 border-green-200',
  warning: 'bg-yellow-50 text-yellow-900 dark:bg-yellow-900/20 dark:text-yellow-300 border-yellow-200'
}

const alertIcons = {
  default: Info,
  destructive: XCircle,
  success: CheckCircle,
  warning: AlertTriangle
}

export function Alert({ variant = 'default', className, children }: AlertProps) {
  const Icon = alertIcons[variant]
  
  return (
    <div className={cn(
      'relative w-full rounded-lg border p-4 flex items-start gap-3',
      alertVariants[variant],
      className
    )}>
      <Icon className="h-4 w-4 mt-0.5" />
      <div className="flex-1">{children}</div>
    </div>
  )
}

export function AlertDescription({ children, className }: { children: React.ReactNode; className?: string }) {
  return (
    <div className={cn('text-sm', className)}>
      {children}
    </div>
  )
}

// Tabs Component
// src/components/ui/Tabs.tsx
import { useState, createContext, useContext } from 'react'
import { cn } from '@/utils/cn'

const TabsContext = createContext<{
  value: string
  onChange: (value: string) => void
}>({ value: '', onChange: () => {} })

export function Tabs({ 
  defaultValue, 
  value: controlledValue, 
  onValueChange,
  children, 
  className 
}: { 
  defaultValue?: string
  value?: string
  onValueChange?: (value: string) => void
  children: React.ReactNode
  className?: string 
}) {
  const [internalValue, setInternalValue] = useState(defaultValue || '')
  const value = controlledValue !== undefined ? controlledValue : internalValue
  const onChange = onValueChange || setInternalValue

  return (
    <TabsContext.Provider value={{ value, onChange }}>
      <div className={cn('w-full', className)}>
        {children}
      </div>
    </TabsContext.Provider>
  )
}

export function TabsList({ children, className }: { children: React.ReactNode; className?: string }) {
  return (
    <div className={cn(
      'inline-flex h-10 items-center justify-center rounded-lg bg-gray-100 dark:bg-gray-800 p-1',
      className
    )}>
      {children}
    </div>
  )
}

export function TabsTrigger({ 
  value, 
  children, 
  className 
}: { 
  value: string
  children: React.ReactNode
  className?: string 
}) {
  const { value: selectedValue, onChange } = useContext(TabsContext)
  const isSelected = value === selectedValue

  return (
    <button
      onClick={() => onChange(value)}
      className={cn(
        'inline-flex items-center justify-center whitespace-nowrap rounded-md px-3 py-1.5 text-sm font-medium transition-all',
        isSelected 
          ? 'bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-sm' 
          : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white',
        className
      )}
    >
      {children}
    </button>
  )
}

export function TabsContent({ 
  value, 
  children, 
  className 
}: { 
  value: string
  children: React.ReactNode
  className?: string 
}) {
  const { value: selectedValue } = useContext(TabsContext)
  
  if (value !== selectedValue) return null

  return (
    <div className={cn('mt-4', className)}>
      {children}
    </div>
  )
}

// Progress Component
// src/components/ui/Progress.tsx
import { cn } from '@/utils/cn'

interface ProgressProps {
  value: number
  max?: number
  className?: string
}

export function Progress({ value, max = 100, className }: ProgressProps) {
  const percentage = Math.min(Math.max(0, (value / max) * 100), 100)

  return (
    <div className={cn('w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2', className)}>
      <div 
        className="bg-purple-600 h-2 rounded-full transition-all duration-300"
        style={{ width: `${percentage}%` }}
      />
    </div>
  )
}

// ScrollArea Component
// src/components/ui/ScrollArea.tsx
import { cn } from '@/utils/cn'

export function ScrollArea({ 
  children, 
  className 
}: { 
  children: React.ReactNode
  className?: string 
}) {
  return (
    <div className={cn('overflow-auto', className)}>
      {children}
    </div>
  )
}

// Switch Component  
// src/components/ui/Switch.tsx
import { cn } from '@/utils/cn'

interface SwitchProps {
  id?: string
  checked: boolean
  onCheckedChange: (checked: boolean) => void
  disabled?: boolean
  className?: string
}

export function Switch({ id, checked, onCheckedChange, disabled, className }: SwitchProps) {
  return (
    <button
      id={id}
      type="button"
      role="switch"
      aria-checked={checked}
      onClick={() => !disabled && onCheckedChange(!checked)}
      disabled={disabled}
      className={cn(
        'relative inline-flex h-6 w-11 items-center rounded-full transition-colors',
        checked ? 'bg-purple-600' : 'bg-gray-200 dark:bg-gray-700',
        disabled && 'opacity-50 cursor-not-allowed',
        className
      )}
    >
      <span
        className={cn(
          'inline-block h-4 w-4 transform rounded-full bg-white transition-transform',
          checked ? 'translate-x-6' : 'translate-x-1'
        )}
      />
    </button>
  )
}

// Label Component
// src/components/ui/Label.tsx
import { cn } from '@/utils/cn'

export function Label({ 
  htmlFor, 
  children, 
  className 
}: { 
  htmlFor?: string
  children: React.ReactNode
  className?: string 
}) {
  return (
    <label 
      htmlFor={htmlFor}
      className={cn('text-sm font-medium text-gray-700 dark:text-gray-300', className)}
    >
      {children}
    </label>
  )
}
```

**Now create the Pipeline components with correct imports:**

### Pipeline Configuration Component
```typescript
// src/components/pipeline/PipelineConfiguration.tsx
import { useState } from 'react'
import { supabase } from '@/services/supabase' // Correct import path
import { useAuth } from '@/contexts/AuthContext' // Correct auth context
import { Button } from '@/components/ui/Button' // From shared components
import { Input } from '@/components/ui/Input' // From shared components
import { Label } from '@/components/ui/Label'
import { Textarea } from '@/components/ui/Input' // Textarea is exported from Input.tsx
import { Switch } from '@/components/ui/Switch'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card'
import { Alert, AlertDescription } from '@/components/ui/Alert'
import { Loader2, AlertCircle } from 'lucide-react'
import { useToast } from '@/components/ui/Toast' // Use the toast hook from shared components

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
  const { showToast } = useToast()
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
      showToast('Please enter a topic', 'error')
      return
    }

    if (config.targetKeywords.length === 0) {
      showToast('Please add at least one target keyword', 'error')
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
          <Input
            label="Content Topic *"
            value={config.topic}
            onChange={(e) => setConfig(prev => ({ ...prev, topic: e.target.value }))}
            placeholder="e.g., Service Dog Training Tips"
            disabled={disabled || isStarting}
          />

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
                  className="px-3 py-1 bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300 rounded-full text-sm"
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
                  <span className="text-gray-600 dark:text-gray-400 truncate flex-1">{url}</span>
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
            <Input
              label="Min Word Count"
              type="number"
              value={config.wordCountMin}
              onChange={(e) => setConfig(prev => ({ 
                ...prev, 
                wordCountMin: parseInt(e.target.value) || 0 
              }))}
              disabled={disabled || isStarting}
            />
            <Input
              label="Max Word Count"
              type="number"
              value={config.wordCountMax}
              onChange={(e) => setConfig(prev => ({ 
                ...prev, 
                wordCountMax: parseInt(e.target.value) || 0 
              }))}
              disabled={disabled || isStarting}
            />
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
          <Input
            label="Budget Limit ($)"
            type="number"
            step="0.01"
            value={config.budgetLimit}
            onChange={(e) => setConfig(prev => ({ 
              ...prev, 
              budgetLimit: parseFloat(e.target.value) || 0 
            }))}
            hint="Estimated cost will be calculated based on configuration"
            disabled={disabled || isStarting}
          />

          {/* Submit Button */}
          <Button
            type="submit"
            fullWidth
            loading={isStarting}
            loadingText="Starting Pipeline..."
            disabled={disabled || isStarting}
          >
            Start Pipeline
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
import { supabase } from '@/services/supabase'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card'
import { Progress } from '@/components/ui/Progress'
import { Badge } from '@/components/ui/Badge'
import { ScrollArea } from '@/components/ui/ScrollArea'
import { Alert, AlertDescription } from '@/components/ui/Alert'
import { Skeleton, CardSkeleton } from '@/components/ui/Skeleton' // Use existing skeleton
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
import { cn } from '@/utils/cn'

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
    return <CardSkeleton />
  }

  if (!execution) {
    return (
      <Card>
        <CardContent className="p-8">
          <div className="text-center">
            <Play className="h-16 w-16 text-gray-300 dark:text-gray-600 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              No Active Pipeline
            </h3>
            <p className="text-gray-600 dark:text-gray-400">
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
    const variants: Record<string, any> = {
      pending: 'secondary',
      running: 'default',
      completed: 'success',
      failed: 'destructive',
      cancelled: 'outline'
    }
    
    return <Badge variant={variants[status]}>{status.toUpperCase()}</Badge>
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
            <span className="text-sm text-gray-600 dark:text-gray-400">{getProgress()}%</span>
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
                  isCurrent && "border-blue-500 bg-blue-50 dark:bg-blue-900/20",
                  isCompleted && "bg-green-50 dark:bg-green-900/20"
                )}
              >
                <button
                  onClick={() => setExpandedAgent(isExpanded ? null : agent.id)}
                  className="w-full p-4 flex items-center gap-3 text-left hover:bg-gray-50 dark:hover:bg-gray-800/50"
                >
                  <span className="text-2xl">{agent.icon}</span>
                  <div className="flex-1">
                    <div className="flex items-center gap-2">
                      <h4 className="font-medium">{agent.name}</h4>
                      {isCompleted && getStatusIcon('completed')}
                      {isCurrent && getStatusIcon('running')}
                    </div>
                    <p className="text-sm text-gray-600 dark:text-gray-400">{agent.description}</p>
                  </div>
                  {isExpanded ? <ChevronDown className="h-4 w-4" /> : <ChevronRight className="h-4 w-4" />}
                </button>

                {/* Expanded Agent Details */}
                {isExpanded && (
                  <div className="px-4 pb-4 border-t">
                    <div className="grid grid-cols-2 gap-4 mt-4">
                      <div>
                        <p className="text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">
                          Status
                        </p>
                        <p className="text-sm">
                          {isCompleted ? 'Completed' : isCurrent ? 'Running' : 'Pending'}
                        </p>
                      </div>
                      {agentStatus.cost && (
                        <div>
                          <p className="text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">
                            Cost
                          </p>
                          <p className="text-sm">${agentStatus.cost.toFixed(4)}</p>
                        </div>
                      )}
                    </div>
                    
                    {agentStatus.output && (
                      <div className="mt-3">
                        <p className="text-xs font-medium text-gray-600 dark:text-gray-400 mb-2">
                          Output Preview
                        </p>
                        <ScrollArea className="h-24 w-full rounded border p-2 bg-gray-50 dark:bg-gray-900">
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
            <AlertDescription>{execution.error_message}</AlertDescription>
          </Alert>
        )}
      </CardContent>
    </Card>
  )
}
```

### Main Pipeline Page
```typescript
// src/pages/Pipeline.tsx
import { useState, useEffect } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { motion } from 'framer-motion'
import { supabase } from '@/services/supabase'
import { useAuth } from '@/contexts/AuthContext'
import { PipelineConfiguration } from '@/components/pipeline/PipelineConfiguration'
import { ExecutionMonitor } from '@/components/pipeline/ExecutionMonitor'
import { PipelineStatus } from '@/components/dashboard/PipelineStatus' // Existing component
import { PipelineHistory } from '@/components/pipeline/PipelineHistory'
import { CostTracker } from '@/components/pipeline/CostTracker'
import { Button } from '@/components/ui/Button'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/Tabs'
import { useToast } from '@/components/ui/Toast'
import { Play, Square, Settings, History, DollarSign } from 'lucide-react'

export default function Pipeline() {
  const { user, organization } = useAuth()
  const [currentExecution, setCurrentExecution] = useState<any>(null)
  const queryClient = useQueryClient()
  const { showToast } = useToast()

  // Set up Supabase real-time subscription
  useEffect(() => {
    if (!organization?.id) return

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
          if (payload.eventType === 'UPDATE' || payload.eventType === 'INSERT') {
            const pipeline = payload.new
            
            if (pipeline.status === 'running' || pipeline.status === 'queued') {
              setCurrentExecution(pipeline)
            }
            
            // Show notifications
            if (payload.eventType === 'UPDATE' && payload.old.status !== pipeline.status) {
              if (pipeline.status === 'completed') {
                showToast('Pipeline completed successfully!', 'success')
              } else if (pipeline.status === 'failed') {
                showToast(`Pipeline failed: ${pipeline.error_message}`, 'error')
              }
            }
            
            queryClient.invalidateQueries({ queryKey: ['pipelines'] })
          }
        }
      )
      .subscribe()

    return () => {
      supabase.removeChannel(channel)
    }
  }, [organization?.id, queryClient, showToast])

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
      
      // TODO: Trigger backend processing
      // This would normally call an Edge Function or API endpoint
      
      return data
    },
    onSuccess: (data) => {
      setCurrentExecution(data)
      showToast('Pipeline started successfully!', 'success')
    },
    onError: (error: any) => {
      showToast(`Failed to start pipeline: ${error.message}`, 'error')
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
      showToast('Pipeline stopped', 'success')
      setCurrentExecution(null)
    }
  })

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
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="container mx-auto px-4 py-8"
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Content Pipeline</h1>
          <p className="text-gray-600 dark:text-gray-400 mt-1">
            Orchestrate 5 AI agents to generate SEO-optimized articles
          </p>
        </div>

        {/* Pipeline Controls */}
        <div className="flex items-center gap-2">
          {isRunning ? (
            <Button
              variant="danger"
              onClick={() => execution && stopPipelineMutation.mutate(execution.id)}
              loading={stopPipelineMutation.isPending}
              leftIcon={<Square className="h-4 w-4" />}
            >
              Stop Pipeline
            </Button>
          ) : (
            <Button
              variant="primary"
              onClick={() => {
                const tabsElement = document.querySelector('[role="tablist"]')
                const configTab = tabsElement?.querySelector('[value="config"]') as HTMLElement
                configTab?.click()
              }}
              leftIcon={<Play className="h-4 w-4" />}
            >
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
              <PipelineStatus /> {/* Existing component from dashboard */}
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
    </motion.div>
  )
}
```

### Pipeline History Component (simplified to use existing components)
```typescript
// src/components/pipeline/PipelineHistory.tsx
import { useQuery } from '@tanstack/react-query'
import { supabase } from '@/services/supabase'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card'
import { Badge } from '@/components/ui/Badge'
import { Button } from '@/components/ui/Button'
import { DataTable } from '@/components/ui/DataTable' // Use existing DataTable
import { formatDistanceToNow } from 'date-fns'
import { formatCurrency } from '@/utils/cn' // Existing utility
import { Eye } from 'lucide-react'

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
      return data || []
    },
    enabled: !!organizationId
  })

  const columns = [
    {
      key: 'name',
      label: 'Pipeline Name',
      render: (pipeline: any) => (
        <div>
          <p className="font-medium">{pipeline.name}</p>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            {formatDistanceToNow(new Date(pipeline.created_at), { addSuffix: true })}
          </p>
        </div>
      )
    },
    {
      key: 'status',
      label: 'Status',
      render: (pipeline: any) => (
        <Badge variant={
          pipeline.status === 'completed' ? 'success' :
          pipeline.status === 'failed' ? 'destructive' :
          pipeline.status === 'running' ? 'default' :
          'secondary'
        }>
          {pipeline.status}
        </Badge>
      )
    },
    {
      key: 'cost',
      label: 'Cost',
      render: (pipeline: any) => (
        <span className="font-medium">
          {pipeline.total_cost ? formatCurrency(pipeline.total_cost) : '-'}
        </span>
      )
    },
    {
      key: 'actions',
      label: 'Actions',
      render: (pipeline: any) => (
        <Button variant="ghost" size="sm">
          <Eye className="h-4 w-4" />
        </Button>
      )
    }
  ]

  return (
    <Card>
      <CardHeader>
        <CardTitle>Pipeline History</CardTitle>
        <CardDescription>
          View and manage your past pipeline executions
        </CardDescription>
      </CardHeader>
      <CardContent>
        <DataTable
          data={pipelines || []}
          columns={columns}
          loading={isLoading}
          emptyMessage="No pipeline executions yet"
        />
      </CardContent>
    </Card>
  )
}
```

### Cost Tracker Component
```typescript
// src/components/pipeline/CostTracker.tsx
import { useQuery } from '@tanstack/react-query'
import { supabase } from '@/services/supabase'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card'
import { Progress } from '@/components/ui/Progress'
import { formatCurrency } from '@/utils/cn'

interface CostTrackerProps {
  organizationId?: string
}

export function CostTracker({ organizationId }: CostTrackerProps) {
  const { data: costData } = useQuery({
    queryKey: ['costs', organizationId],
    queryFn: async () => {
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
      
      // TODO: Get budget from organization settings
      return {
        monthlyTotal: totalCost,
        budget: 100,
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
              {formatCurrency(costData?.monthlyTotal || 0)} / {formatCurrency(costData?.budget || 0)}
            </span>
          </div>
          <Progress value={usagePercentage} />
        </div>
        
        <div className="grid grid-cols-2 gap-4 pt-4 border-t">
          <div>
            <p className="text-sm text-gray-600 dark:text-gray-400">Articles Generated</p>
            <p className="text-2xl font-bold">{costData?.articlesGenerated || 0}</p>
          </div>
          <div>
            <p className="text-sm text-gray-600 dark:text-gray-400">Avg Cost per Article</p>
            <p className="text-2xl font-bold">
              {costData?.articlesGenerated 
                ? formatCurrency(costData.monthlyTotal / costData.articlesGenerated)
                : formatCurrency(0)}
            </p>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
```

**Success Criteria:**
- ✅ Uses `@/services/supabase` (correct import path)
- ✅ Uses `@/contexts/AuthContext` (correct auth context)
- ✅ Extends existing `PipelineStatus` component from dashboard
- ✅ Uses existing shared UI components (Button, Input, Card, etc.)
- ✅ Uses existing utility functions (cn, formatCurrency, etc.)
- ✅ Uses existing Toast system from shared components
- ✅ Creates missing UI components (Badge, Alert, Tabs, Progress, etc.)
- ✅ Works with existing `pipelines` table structure
- ✅ Real-time updates via Supabase subscriptions
- ✅ No backend API dependency

This final version corrects all import paths and uses the existing shared component library while creating only the missing components needed for the pipeline management system.
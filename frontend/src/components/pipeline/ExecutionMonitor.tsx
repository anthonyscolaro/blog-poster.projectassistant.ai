import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'
import { Badge } from '@/components/ui/badge'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Skeleton } from '@/components/ui/skeleton'
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
        <CardHeader>
          <Skeleton className="h-6 w-32" />
          <Skeleton className="h-4 w-48" />
        </CardHeader>
        <CardContent className="space-y-4">
          <Skeleton className="h-6 w-full" />
          <div className="space-y-2">
            {Array.from({ length: 5 }).map((_, i) => (
              <Skeleton key={i} className="h-16 w-full" />
            ))}
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
            <Play className="h-16 w-16 text-muted-foreground mx-auto mb-4" />
            <h3 className="text-lg font-semibold mb-2">
              No Active Pipeline
            </h3>
            <p className="text-muted-foreground">
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
        return <XCircle className="h-4 w-4 text-destructive" />
      default:
        return <Clock className="h-4 w-4 text-muted-foreground" />
    }
  }

  const getStatusVariant = (status: string) => {
    switch (status) {
      case 'pending':
        return 'secondary'
      case 'running':
        return 'default'
      case 'completed':
        return 'outline'
      case 'failed':
        return 'destructive'
      case 'cancelled':
        return 'outline'
      default:
        return 'secondary'
    }
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
          <Badge variant={getStatusVariant(execution.status)}>
            {execution.status.toUpperCase()}
          </Badge>
        </div>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Progress Bar */}
        <div>
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium">Overall Progress</span>
            <span className="text-sm text-muted-foreground">{getProgress()}%</span>
          </div>
          <Progress value={getProgress()} className="h-2" />
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
                  isCurrent && "border-primary bg-primary/5",
                  isCompleted && "bg-muted/50"
                )}
              >
                <button
                  onClick={() => setExpandedAgent(isExpanded ? null : agent.id)}
                  className="w-full p-4 flex items-center gap-3 text-left hover:bg-muted/50 rounded-lg transition-colors"
                >
                  <span className="text-2xl">{agent.icon}</span>
                  <div className="flex-1">
                    <div className="flex items-center gap-2">
                      <h4 className="font-medium">{agent.name}</h4>
                      {isCompleted && getStatusIcon('completed')}
                      {isCurrent && getStatusIcon('running')}
                    </div>
                    <p className="text-sm text-muted-foreground">{agent.description}</p>
                  </div>
                  {isExpanded ? <ChevronDown className="h-4 w-4" /> : <ChevronRight className="h-4 w-4" />}
                </button>

                {/* Expanded Agent Details */}
                {isExpanded && (
                  <div className="px-4 pb-4 border-t">
                    <div className="grid grid-cols-2 gap-4 mt-4">
                      <div>
                        <p className="text-xs font-medium text-muted-foreground mb-1">
                          Status
                        </p>
                        <p className="text-sm">
                          {isCompleted ? 'Completed' : isCurrent ? 'Running' : 'Pending'}
                        </p>
                      </div>
                      {agentStatus.cost && (
                        <div>
                          <p className="text-xs font-medium text-muted-foreground mb-1">
                            Cost
                          </p>
                          <p className="text-sm">${agentStatus.cost.toFixed(4)}</p>
                        </div>
                      )}
                    </div>
                    
                    {agentStatus.output && (
                      <div className="mt-3">
                        <p className="text-xs font-medium text-muted-foreground mb-2">
                          Output Preview
                        </p>
                        <ScrollArea className="h-24 w-full">
                          <div className="rounded border p-2 bg-muted text-xs">
                            <pre className="whitespace-pre-wrap">{JSON.stringify(agentStatus.output, null, 2)}</pre>
                          </div>
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
import { useQuery } from '@tanstack/react-query'
import { supabase } from '@/services/supabase'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { formatDistanceToNow } from 'date-fns'
import { formatCurrency } from '@/utils/formatters'
import { Eye, Clock, CheckCircle2, XCircle, AlertCircle } from 'lucide-react'

interface PipelineHistoryProps {
  organizationId?: string
}

interface Pipeline {
  id: string
  name: string
  status: string
  total_cost: number
  created_at: string
  completed_at?: string
  error_message?: string
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

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle2 className="h-4 w-4 text-green-500" />
      case 'failed':
        return <XCircle className="h-4 w-4 text-destructive" />
      case 'running':
        return <Clock className="h-4 w-4 text-blue-500" />
      default:
        return <AlertCircle className="h-4 w-4 text-muted-foreground" />
    }
  }

  const getStatusVariant = (status: string) => {
    switch (status) {
      case 'completed':
        return 'outline'
      case 'failed':
        return 'destructive'
      case 'running':
        return 'default'
      default:
        return 'secondary'
    }
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
        {isLoading ? (
          <div className="space-y-4">
            {Array.from({ length: 5 }).map((_, i) => (
              <div key={i} className="flex items-center justify-between p-4 border rounded-lg">
                <div className="space-y-2">
                  <div className="h-4 bg-muted rounded w-32 animate-pulse" />
                  <div className="h-3 bg-muted rounded w-24 animate-pulse" />
                </div>
                <div className="h-6 bg-muted rounded w-16 animate-pulse" />
              </div>
            ))}
          </div>
        ) : pipelines && pipelines.length > 0 ? (
          <div className="space-y-4">
            {pipelines.map((pipeline: Pipeline) => (
              <div key={pipeline.id} className="flex items-center justify-between p-4 border rounded-lg hover:bg-muted/50 transition-colors">
                <div className="flex-1 space-y-1">
                  <div className="flex items-center gap-3">
                    {getStatusIcon(pipeline.status)}
                    <h3 className="font-medium">{pipeline.name}</h3>
                    <Badge variant={getStatusVariant(pipeline.status)}>
                      {pipeline.status}
                    </Badge>
                  </div>
                  <p className="text-sm text-muted-foreground">
                    Started {formatDistanceToNow(new Date(pipeline.created_at), { addSuffix: true })}
                    {pipeline.completed_at && ` • Completed ${formatDistanceToNow(new Date(pipeline.completed_at), { addSuffix: true })}`}
                  </p>
                  {pipeline.error_message && (
                    <p className="text-sm text-destructive truncate">
                      Error: {pipeline.error_message}
                    </p>
                  )}
                </div>
                <div className="flex items-center gap-4">
                  {pipeline.total_cost > 0 && (
                    <span className="font-medium text-sm">
                      {formatCurrency(pipeline.total_cost)}
                    </span>
                  )}
                  <Button variant="ghost" size="sm">
                    <Eye className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-8">
            <Clock className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
            <h3 className="text-lg font-medium mb-2">No pipeline executions yet</h3>
            <p className="text-muted-foreground">
              Your pipeline history will appear here once you start generating content.
            </p>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
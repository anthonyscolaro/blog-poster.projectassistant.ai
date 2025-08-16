import { useQuery } from '@tanstack/react-query'
import { supabase } from '@/services/supabase'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'
import { formatCurrency } from '@/utils/formatters'
import { TrendingUp, DollarSign, FileText } from 'lucide-react'

interface CostTrackerProps {
  organizationId?: string
}

export function CostTracker({ organizationId }: CostTrackerProps) {
  const { data: costData, isLoading } = useQuery({
    queryKey: ['costs', organizationId],
    queryFn: async () => {
      const startOfMonth = new Date()
      startOfMonth.setDate(1)
      startOfMonth.setHours(0, 0, 0, 0)

      // Get pipelines data for cost calculation
      const { data: pipelineData, error: pipelineError } = await supabase
        .from('pipelines')
        .select('total_cost, status')
        .eq('organization_id', organizationId)
        .gte('created_at', startOfMonth.toISOString())
        .not('total_cost', 'is', null)

      if (pipelineError) throw pipelineError

      // Get organization budget
      const { data: orgData, error: orgError } = await supabase
        .from('organizations')
        .select('monthly_budget')
        .eq('id', organizationId)
        .single()

      if (orgError) throw orgError

      const totalCost = pipelineData?.reduce((sum, p) => sum + (p.total_cost || 0), 0) || 0
      const completedPipelines = pipelineData?.filter(p => p.status === 'completed').length || 0
      
      return {
        monthlyTotal: totalCost,
        budget: orgData?.monthly_budget || 100,
        articlesGenerated: completedPipelines,
        totalPipelines: pipelineData?.length || 0
      }
    },
    enabled: !!organizationId
  })

  const usagePercentage = costData ? Math.min((costData.monthlyTotal / costData.budget) * 100, 100) : 0
  const avgCostPerArticle = costData && costData.articlesGenerated > 0 
    ? costData.monthlyTotal / costData.articlesGenerated 
    : 0

  if (isLoading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Cost Tracking</CardTitle>
          <CardDescription>
            Monitor your monthly usage and costs
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="animate-pulse space-y-4">
            <div className="h-4 bg-muted rounded w-full" />
            <div className="h-6 bg-muted rounded w-full" />
            <div className="grid grid-cols-2 gap-4">
              <div className="h-16 bg-muted rounded" />
              <div className="h-16 bg-muted rounded" />
            </div>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <DollarSign className="h-5 w-5" />
          Cost Tracking
        </CardTitle>
        <CardDescription>
          Monitor your monthly usage and costs
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Budget Usage */}
        <div className="space-y-3">
          <div className="flex justify-between items-center">
            <span className="text-sm font-medium">Monthly Usage</span>
            <span className="text-sm font-medium">
              {formatCurrency(costData?.monthlyTotal || 0)} / {formatCurrency(costData?.budget || 0)}
            </span>
          </div>
          <Progress value={usagePercentage} className="h-2" />
          <div className="flex justify-between text-xs text-muted-foreground">
            <span>{usagePercentage.toFixed(1)}% used</span>
            <span>{formatCurrency((costData?.budget || 0) - (costData?.monthlyTotal || 0))} remaining</span>
          </div>
        </div>
        
        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-4 border-t">
          <div className="space-y-1">
            <div className="flex items-center gap-2 text-muted-foreground">
              <FileText className="h-4 w-4" />
              <span className="text-sm">Articles Generated</span>
            </div>
            <p className="text-2xl font-bold">{costData?.articlesGenerated || 0}</p>
          </div>
          
          <div className="space-y-1">
            <div className="flex items-center gap-2 text-muted-foreground">
              <TrendingUp className="h-4 w-4" />
              <span className="text-sm">Avg Cost/Article</span>
            </div>
            <p className="text-2xl font-bold">
              {formatCurrency(avgCostPerArticle)}
            </p>
          </div>

          <div className="space-y-1">
            <div className="flex items-center gap-2 text-muted-foreground">
              <DollarSign className="h-4 w-4" />
              <span className="text-sm">Total Pipelines</span>
            </div>
            <p className="text-2xl font-bold">{costData?.totalPipelines || 0}</p>
          </div>
        </div>

        {/* Budget Alert */}
        {usagePercentage > 80 && (
          <div className="p-3 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg">
            <p className="text-sm text-yellow-800 dark:text-yellow-200">
              <strong>Budget Alert:</strong> You've used {usagePercentage.toFixed(1)}% of your monthly budget.
            </p>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
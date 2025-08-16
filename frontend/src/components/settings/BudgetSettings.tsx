import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Switch } from '@/components/ui/switch'
import { Progress } from '@/components/ui/progress'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { 
  DollarSign, 
  TrendingUp, 
  AlertTriangle, 
  Target,
  PauseCircle,
  Activity,
  Calendar,
  CreditCard
} from 'lucide-react'

interface BudgetConfig {
  id?: string
  name?: string
  slug?: string
  plan?: 'free' | 'starter' | 'professional' | 'enterprise'
  subscription_status?: string
  trial_ends_at?: string | null
  articles_limit: number
  articles_used: number
  monthly_budget: number
  current_month_cost: number
  budget_alert_threshold?: number
}

interface BudgetSettingsProps {
  budget: BudgetConfig
  onChange: (updates: Partial<BudgetConfig>) => void
}

export function BudgetSettings({ budget, onChange }: BudgetSettingsProps) {
  const budgetUsagePercentage = (budget.current_month_cost / budget.monthly_budget) * 100
  const articlesUsagePercentage = (budget.articles_used / budget.articles_limit) * 100
  
  const remainingBudget = Math.max(0, budget.monthly_budget - budget.current_month_cost)
  const remainingArticles = Math.max(0, budget.articles_limit - budget.articles_used)
  
  const isOverBudget = budget.current_month_cost >= budget.monthly_budget
  const isNearLimit = budgetUsagePercentage >= (budget.budget_alert_threshold || 80)

  const handleInputChange = (field: keyof BudgetConfig, value: number) => {
    onChange({ [field]: value })
  }

  const getProgressColor = (percentage: number) => {
    if (percentage >= 100) return 'bg-destructive'
    if (percentage >= 80) return 'bg-amber-500'
    return 'bg-primary'
  }

  return (
    <div className="space-y-6">
      {/* Current Usage Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Monthly Budget</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">${budget.current_month_cost.toFixed(2)} / ${budget.monthly_budget.toFixed(2)}</div>
            <Progress 
              value={Math.min(budgetUsagePercentage, 100)} 
              className="mt-2"
            />
            <p className="text-xs text-muted-foreground mt-2">
              {budgetUsagePercentage.toFixed(1)}% used • ${remainingBudget.toFixed(2)} remaining
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Articles Limit</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{budget.articles_used} / {budget.articles_limit}</div>
            <Progress 
              value={Math.min(articlesUsagePercentage, 100)} 
              className="mt-2"
            />
            <p className="text-xs text-muted-foreground mt-2">
              {articlesUsagePercentage.toFixed(1)}% used • {remainingArticles} remaining
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Alerts */}
      {isOverBudget && (
        <Alert variant="destructive">
          <AlertTriangle className="h-4 w-4" />
          <AlertDescription>
            <strong>Budget Exceeded:</strong> You've exceeded your monthly budget limit. 
            Article generation has been paused. Consider upgrading your plan or increasing your budget.
          </AlertDescription>
        </Alert>
      )}

      {isNearLimit && !isOverBudget && (
        <Alert>
          <AlertTriangle className="h-4 w-4" />
          <AlertDescription>
            <strong>Budget Alert:</strong> You've reached {budgetUsagePercentage.toFixed(1)}% of your monthly budget. 
            Consider monitoring your usage or adjusting your limits.
          </AlertDescription>
        </Alert>
      )}

      {/* Budget Configuration */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Target className="h-5 w-5" />
            Budget Limits
          </CardTitle>
          <CardDescription>
            Set monthly spending limits and article quotas to control costs
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-2">
              <Label htmlFor="monthly_budget">
                <DollarSign className="h-4 w-4 inline mr-1" />
                Monthly Budget ($)
              </Label>
              <Input
                id="monthly_budget"
                type="number"
                min={10}
                max={10000}
                step={5}
                value={budget.monthly_budget}
                onChange={(e) => handleInputChange('monthly_budget', parseFloat(e.target.value) || 0)}
              />
              <p className="text-sm text-muted-foreground">
                Maximum amount to spend on content generation per month
              </p>
            </div>

            <div className="space-y-2">
              <Label htmlFor="articles_limit">
                <Activity className="h-4 w-4 inline mr-1" />
                Articles Limit
              </Label>
              <Input
                id="articles_limit"
                type="number"
                min={1}
                max={1000}
                value={budget.articles_limit}
                onChange={(e) => handleInputChange('articles_limit', parseInt(e.target.value) || 0)}
              />
              <p className="text-sm text-muted-foreground">
                Maximum number of articles to generate per month
              </p>
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="budget_alert_threshold">
              Alert Threshold ({budget.budget_alert_threshold || 80}%)
            </Label>
            <Input
              id="budget_alert_threshold"
              type="range"
              min={50}
              max={95}
              step={5}
              value={budget.budget_alert_threshold || 80}
              onChange={(e) => handleInputChange('budget_alert_threshold', parseInt(e.target.value))}
              className="w-full"
            />
            <div className="flex justify-between text-sm text-muted-foreground">
              <span>50%</span>
              <span>Current: {budget.budget_alert_threshold || 80}%</span>
              <span>95%</span>
            </div>
            <p className="text-sm text-muted-foreground">
              Get notified when you reach this percentage of your budget
            </p>
          </div>
        </CardContent>
      </Card>

      {/* Advanced Settings */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <PauseCircle className="h-5 w-5" />
            Advanced Controls
          </CardTitle>
          <CardDescription>
            Additional budget management and safety features
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <Label htmlFor="auto_pause">Auto-pause on budget limit</Label>
              <p className="text-sm text-muted-foreground">
                Automatically pause article generation when budget is exceeded
              </p>
            </div>
            <Switch
              id="auto_pause"
              checked={true}
              disabled
            />
          </div>

          <div className="flex items-center justify-between">
            <div>
              <Label htmlFor="email_alerts">Email budget alerts</Label>
              <p className="text-sm text-muted-foreground">
                Send email notifications when reaching budget thresholds
              </p>
            </div>
            <Switch
              id="email_alerts"
              checked={true}
              disabled
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="cost_per_article_limit">
              Maximum cost per article ($)
            </Label>
            <Input
              id="cost_per_article_limit"
              type="number"
              min={0.10}
              max={10.00}
              step={0.10}
              value={2.00}
              disabled
            />
            <p className="text-sm text-muted-foreground">
              Stop generation if a single article exceeds this cost
            </p>
          </div>
        </CardContent>
      </Card>

      {/* Budget History */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingUp className="h-5 w-5" />
            Usage Trends
          </CardTitle>
          <CardDescription>
            Track your spending patterns over time
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-center justify-between py-2 border-b">
              <span className="text-sm font-medium">This Month</span>
              <span className="text-sm">${budget.current_month_cost.toFixed(2)}</span>
            </div>
            <div className="flex items-center justify-between py-2 border-b">
              <span className="text-sm font-medium">Articles Generated</span>
              <span className="text-sm">{budget.articles_used}</span>
            </div>
            <div className="flex items-center justify-between py-2 border-b">
              <span className="text-sm font-medium">Average Cost per Article</span>
              <span className="text-sm">
                ${budget.articles_used > 0 ? (budget.current_month_cost / budget.articles_used).toFixed(2) : '0.00'}
              </span>
            </div>
            <div className="flex items-center justify-between py-2">
              <span className="text-sm font-medium">Projected Monthly Total</span>
              <span className="text-sm font-bold">
                ${((budget.current_month_cost / new Date().getDate()) * 30).toFixed(2)}
              </span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
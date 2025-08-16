import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { 
  FileText, 
  TrendingUp, 
  DollarSign, 
  Workflow,
  PlusCircle,
  Activity
} from 'lucide-react'
import { useNotificationsWebSocket } from '@/hooks/useWebSocket'
import type { DashboardStats, WebSocketMessage } from '@/types'

export function DashboardPage() {
  const [stats, setStats] = useState<DashboardStats>({
    total_articles: 0,
    published_articles: 0,
    draft_articles: 0,
    active_pipelines: 0,
    monthly_cost: 0,
    budget_percentage: 0,
  })

  const { isConnected } = useNotificationsWebSocket()

  // Simulate loading stats
  useEffect(() => {
    const timer = setTimeout(() => {
      setStats({
        total_articles: 24,
        published_articles: 18,
        draft_articles: 6,
        active_pipelines: 3,
        monthly_cost: 89.50,
        budget_percentage: 59.7,
      })
    }, 1000)
    return () => clearTimeout(timer)
  }, [])

  const statCards = [
    {
      title: 'Total Articles',
      value: stats.total_articles.toString(),
      description: 'Articles generated this month',
      icon: FileText,
      trend: '+12%',
      color: 'text-blue-600'
    },
    {
      title: 'Published',
      value: stats.published_articles.toString(),
      description: 'Live on WordPress',
      icon: TrendingUp,
      trend: '+8%',
      color: 'text-green-600'
    },
    {
      title: 'Active Pipelines',
      value: stats.active_pipelines.toString(),
      description: 'Currently running',
      icon: Workflow,
      trend: '3 running',
      color: 'text-purple-600'
    },
    {
      title: 'Monthly Cost',
      value: `$${stats.monthly_cost.toFixed(2)}`,
      description: `${stats.budget_percentage}% of budget`,
      icon: DollarSign,
      trend: '+5%',
      color: 'text-orange-600'
    },
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
          <p className="text-muted-foreground">
            Welcome to your Blog-Poster SEO content generation dashboard
          </p>
        </div>
        <div className="flex items-center space-x-3">
          <div className="flex items-center space-x-2 text-sm">
            <Activity className={`h-4 w-4 ${isConnected ? 'text-green-500' : 'text-red-500'}`} />
            <span className="text-muted-foreground">
              {isConnected ? 'Connected' : 'Disconnected'}
            </span>
          </div>
          <Button className="bg-purple-gradient hover:opacity-90">
            <PlusCircle className="mr-2 h-4 w-4" />
            New Pipeline
          </Button>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {statCards.map((stat) => (
          <Card key={stat.title} className="hover:shadow-md transition-shadow">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                {stat.title}
              </CardTitle>
              <stat.icon className={`h-4 w-4 ${stat.color}`} />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stat.value}</div>
              <p className="text-xs text-muted-foreground">
                {stat.description}
              </p>
              <div className="text-xs text-green-600 mt-1">
                {stat.trend}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Recent Activity */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-7">
        <Card className="col-span-4">
          <CardHeader>
            <CardTitle>Recent Pipeline Activity</CardTitle>
            <CardDescription>
              Latest content generation pipelines and their status
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {[1, 2, 3].map((i) => (
                <div key={i} className="flex items-center justify-between p-3 border rounded-lg">
                  <div className="flex items-center space-x-3">
                    <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                    <div>
                      <p className="font-medium">Service Dog Training Article #{i}</p>
                      <p className="text-sm text-muted-foreground">Completed 2 hours ago</p>
                    </div>
                  </div>
                  <div className="text-sm text-green-600">
                    ✓ Published
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card className="col-span-3">
          <CardHeader>
            <CardTitle>Quick Actions</CardTitle>
            <CardDescription>
              Common tasks and shortcuts
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            <Button variant="outline" className="w-full justify-start">
              <FileText className="mr-2 h-4 w-4" />
              Create Article
            </Button>
            <Button variant="outline" className="w-full justify-start">
              <Workflow className="mr-2 h-4 w-4" />
              New Pipeline
            </Button>
            <Button variant="outline" className="w-full justify-start">
              <TrendingUp className="mr-2 h-4 w-4" />
              View Analytics
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
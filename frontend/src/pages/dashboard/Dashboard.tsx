import { MetricsGrid } from '@/components/dashboard/MetricsGrid'
import { PipelineStatus } from '@/components/dashboard/PipelineStatus'
import { RecentArticles } from '@/components/dashboard/RecentArticles'
import { AgentPerformance } from '@/components/dashboard/AgentPerformance'
import { QuickActions } from '@/components/dashboard/QuickActions'
import { useAuth } from '@/contexts/AuthContext'

export default function Dashboard() {
  const { user } = useAuth()
  const firstName = user?.user_metadata?.full_name?.split(' ')[0] || 'there'

  return (
    <div className="max-w-7xl mx-auto p-6">
      {/* Welcome Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-foreground mb-2">
          Welcome back, {firstName}! 👋
        </h1>
        <p className="text-muted-foreground">
          Monitor your content generation pipeline and track performance metrics.
        </p>
      </div>

      {/* Quick Actions */}
      <QuickActions />

      {/* Metrics Grid */}
      <MetricsGrid />

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* Pipeline Status */}
        <PipelineStatus />
        
        {/* Agent Performance */}
        <AgentPerformance />
      </div>

      {/* Recent Articles */}
      <RecentArticles />
    </div>
  )
}
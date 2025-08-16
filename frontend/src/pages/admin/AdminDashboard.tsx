import { useState, useEffect } from 'react'
import { useQuery } from '@tanstack/react-query'
import { supabase } from '@/integrations/supabase/client'
import { useAuth } from '@/contexts/AuthContext'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Progress } from '@/components/ui/progress'
import { 
  Users, 
  Building, 
  DollarSign, 
  FileText, 
  Activity,
  TrendingUp,
  AlertTriangle,
  CheckCircle,
  Clock,
  Server,
  Database,
  Zap,
  HardDrive,
  BarChart3,
  Shield,
  Bell,
  Settings,
  LifeBuoy,
  Pause,
  Lock,
  Eye,
  RotateCcw,
  Cpu,
  Globe,
  Timer
} from 'lucide-react'
import { AdminMetricsCard } from '@/components/admin/AdminMetricsCard'
import { SystemStatusGrid } from '@/components/admin/SystemStatusGrid'
import { ActivityFeed } from '@/components/admin/ActivityFeed'
import { AlertManager } from '@/components/admin/AlertManager'

interface PlatformMetrics {
  users: {
    total: number
    active_today: number
    new_signups: number
    growth_rate: number
  }
  organizations: {
    total: number
    active: number
    enterprise: number
  }
  revenue: {
    mrr: number
    today_revenue: number
    churn_rate: number
    ltv: number
  }
  content: {
    articles_today: number
    api_calls: number
    storage_used: number
    storage_total: number
    avg_processing_time: number
  }
  system: {
    uptime: number
    system_load: number
    active_users_now: number
  }
}

interface SystemHealth {
  api_gateway: { status: 'healthy' | 'degraded' | 'down', response_time: number }
  database: { status: 'healthy' | 'degraded' | 'down', connections: number, max_connections: number }
  ai_services: { status: 'healthy' | 'degraded' | 'down', note?: string }
  storage: { status: 'healthy' | 'degraded' | 'down', availability: number }
  queue_system: { status: 'healthy' | 'degraded' | 'down', pending_jobs: number }
  monitoring: { status: 'healthy' | 'degraded' | 'down' }
}

interface EmergencyControls {
  maintenanceMode: boolean
  readOnlyMode: boolean
  disablePayments: boolean
  pauseAgents: boolean
}

interface PerformanceMetrics {
  apiLatency: { p50: number, p95: number, p99: number }
  databaseQueries: { slow_queries: number, avg_query_time: number }
  memoryUsage: { heap_mb: number, rss_mb: number }
  errorRates: { rate_5xx: number, rate_4xx: number }
}

interface AdminAuditLog {
  admin_id: string
  action: string
  target_type: 'user' | 'organization' | 'system'
  target_id: string
  details: Record<string, unknown>
  ip_address: string
  timestamp: string
}

export default function AdminDashboard() {
  const { user, profile } = useAuth()
  const [selectedTimeRange, setSelectedTimeRange] = useState('30d')
  const [emergencyControls, setEmergencyControls] = useState<EmergencyControls>({
    maintenanceMode: false,
    readOnlyMode: false,
    disablePayments: false,
    pauseAgents: false
  })

  // Load platform metrics
  const { data: metrics, isLoading: metricsLoading } = useQuery({
    queryKey: ['admin-platform-metrics', selectedTimeRange],
    queryFn: async (): Promise<PlatformMetrics> => {
      // In a real app, this would call admin APIs
      // For now, we'll simulate the data
      return {
        users: {
          total: 12456,
          active_today: 2843,
          new_signups: 34,
          growth_rate: 12
        },
        organizations: {
          total: 3247,
          active: 2891,
          enterprise: 124
        },
        revenue: {
          mrr: 28350,
          today_revenue: 1240,
          churn_rate: 3.2,
          ltv: 340
        },
        content: {
          articles_today: 847,
          api_calls: 12400,
          storage_used: 2.3,
          storage_total: 5.0,
          avg_processing_time: 2.1
        },
        system: {
          uptime: 99.97,
          system_load: 42,
          active_users_now: 1247
        }
      }
    },
    enabled: !!user
  })

  // Load system health
  const { data: systemHealth } = useQuery({
    queryKey: ['admin-system-health'],
    queryFn: async (): Promise<SystemHealth> => {
      return {
        api_gateway: { status: 'healthy', response_time: 120 },
        database: { status: 'healthy', connections: 45, max_connections: 100 },
        ai_services: { status: 'degraded', note: 'Anthropic API slower than usual' },
        storage: { status: 'healthy', availability: 89 },
        queue_system: { status: 'healthy', pending_jobs: 12 },
        monitoring: { status: 'healthy' }
      }
    },
    refetchInterval: 30000 // Refresh every 30 seconds
  })

  // Load performance metrics
  const { data: performanceMetrics } = useQuery({
    queryKey: ['admin-performance-metrics'],
    queryFn: async (): Promise<PerformanceMetrics> => {
      return {
        apiLatency: { p50: 120, p95: 450, p99: 800 },
        databaseQueries: { slow_queries: 3, avg_query_time: 85 },
        memoryUsage: { heap_mb: 1250, rss_mb: 1800 },
        errorRates: { rate_5xx: 0.02, rate_4xx: 1.5 }
      }
    },
    refetchInterval: 10000 // Refresh every 10 seconds
  })

  // Emergency control handlers
  const handleEmergencyToggle = async (control: keyof EmergencyControls) => {
    const newValue = !emergencyControls[control]
    setEmergencyControls(prev => ({ ...prev, [control]: newValue }))
    
    // Log the admin action
    await logAdminAction({
      action: `emergency_${control}_${newValue ? 'enabled' : 'disabled'}`,
      target_type: 'system',
      target_id: 'platform',
      details: { [control]: newValue }
    })
  }

  // Admin audit logging function
  const logAdminAction = async (action: Omit<AdminAuditLog, 'admin_id' | 'ip_address' | 'timestamp'>) => {
    try {
      await supabase.from('audit_logs').insert({
        organization_id: profile?.organization_id,
        user_id: user?.id,
        action: action.action,
        resource_type: action.target_type,
        resource_id: action.target_id,
        details: JSON.stringify(action.details)
      })
    } catch (error) {
      console.error('Failed to log admin action:', error)
    }
  }

  // Calculate overall system status
  const getOverallSystemStatus = () => {
    if (!systemHealth) return 'unknown'
    
    const statuses = Object.values(systemHealth).map(service => service.status)
    
    if (statuses.includes('down')) return 'critical'
    if (statuses.includes('degraded')) return 'warning'
    return 'healthy'
  }

  const overallStatus = getOverallSystemStatus()

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'healthy': return 'text-green-600'
      case 'warning': return 'text-yellow-600'
      case 'critical': return 'text-red-600'
      default: return 'text-gray-600'
    }
  }

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'healthy':
        return <Badge className="bg-green-100 text-green-800 hover:bg-green-100">All Systems Operational</Badge>
      case 'warning':
        return <Badge className="bg-yellow-100 text-yellow-800 hover:bg-yellow-100">Minor Issues</Badge>
      case 'critical':
        return <Badge className="bg-red-100 text-red-800 hover:bg-red-100">Critical Issues</Badge>
      default:
        return <Badge variant="outline">Unknown Status</Badge>
    }
  }

  if (metricsLoading) {
    return (
      <div className="container mx-auto py-8">
        <div className="animate-pulse space-y-6">
          <div className="h-8 bg-muted rounded w-64"></div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="h-32 bg-muted rounded"></div>
            ))}
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="container mx-auto py-8 space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Platform Administration</h1>
          <p className="text-muted-foreground">
            System health and platform overview
          </p>
        </div>
        
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <span className="text-sm text-muted-foreground">Admin:</span>
            <Badge variant="destructive" className="flex items-center gap-1">
              <Shield className="h-3 w-3" />
              Platform Admin
            </Badge>
          </div>
          
          <div className="flex gap-2">
            <Button variant="outline" size="sm">
              <Bell className="h-4 w-4 mr-2" />
              Support Queue
            </Button>
            <Button variant="outline" size="sm">
              <Activity className="h-4 w-4 mr-2" />
              System Status
            </Button>
          </div>
        </div>
      </div>

      {/* System Status Alert */}
      {overallStatus !== 'healthy' && (
        <Alert variant={overallStatus === 'critical' ? 'destructive' : 'default'}>
          <AlertTriangle className="h-4 w-4" />
          <AlertDescription>
            {overallStatus === 'critical' 
              ? 'Critical system issues detected. Immediate attention required.'
              : 'Some system components are experiencing degraded performance.'
            }
            <Button variant="link" className="ml-2 p-0 h-auto">
              View Details →
            </Button>
          </AlertDescription>
        </Alert>
      )}

      {/* Key Metrics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {/* Platform Health */}
        <AdminMetricsCard
          title="Platform Health"
          value={getStatusBadge(overallStatus)}
          description={`${metrics?.system.uptime}% uptime (30 days)`}
          icon={<Activity className="h-4 w-4" />}
          details={[
            `${metrics?.system.active_users_now} users online`,
            `${metrics?.system.system_load}% system load`
          ]}
          actionLabel="View System Status"
        />

        {/* User Growth */}
        <AdminMetricsCard
          title="User Growth"
          value={`${metrics?.users.total.toLocaleString()} users`}
          description={`+${metrics?.users.new_signups} signups today`}
          icon={<Users className="h-4 w-4" />}
          details={[
            `${metrics?.users.active_today.toLocaleString()} active today`,
            `+${metrics?.users.growth_rate}% this month`
          ]}
          actionLabel="View User Analytics"
          trend={metrics?.users.growth_rate}
        />

        {/* Revenue Overview */}
        <AdminMetricsCard
          title="Revenue Overview"
          value={`$${metrics?.revenue.mrr.toLocaleString()} MRR`}
          description={`+$${metrics?.revenue.today_revenue} today`}
          icon={<DollarSign className="h-4 w-4" />}
          details={[
            `${metrics?.revenue.churn_rate}% churn rate`,
            `$${metrics?.revenue.ltv} avg LTV`
          ]}
          actionLabel="View Billing Dashboard"
          trend={5.2} // Simulated growth
        />

        {/* Content Activity */}
        <AdminMetricsCard
          title="Content Activity"
          value={`${metrics?.content.articles_today} articles today`}
          description={`${(metrics?.content.api_calls / 1000).toFixed(1)}K API calls`}
          icon={<FileText className="h-4 w-4" />}
          details={[
            `${metrics?.content.storage_used}TB / ${metrics?.content.storage_total}TB storage`,
            `${metrics?.content.avg_processing_time}s avg processing`
          ]}
          actionLabel="View Content Analytics"
        />
      </div>

      {/* System Status & Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* System Status Grid */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Server className="h-5 w-5" />
              System Status
            </CardTitle>
            <CardDescription>
              Real-time status of all platform services
            </CardDescription>
          </CardHeader>
          <CardContent>
            <SystemStatusGrid systemHealth={systemHealth} />
          </CardContent>
        </Card>

        {/* Recent Activity */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Clock className="h-5 w-5" />
              Recent Platform Activity
            </CardTitle>
            <CardDescription>
              Live feed of significant platform events
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ActivityFeed />
          </CardContent>
        </Card>
      </div>

      {/* Emergency Controls & Performance */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Emergency Controls */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <AlertTriangle className="h-5 w-5" />
              Emergency Controls
            </CardTitle>
            <CardDescription>
              Critical system-wide controls for emergency situations
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <Button
                variant={emergencyControls.maintenanceMode ? "destructive" : "outline"}
                size="sm"
                onClick={() => handleEmergencyToggle('maintenanceMode')}
                className="justify-start"
              >
                <Settings className="h-4 w-4 mr-2" />
                Maintenance Mode
              </Button>
              <Button
                variant={emergencyControls.readOnlyMode ? "destructive" : "outline"}
                size="sm"
                onClick={() => handleEmergencyToggle('readOnlyMode')}
                className="justify-start"
              >
                <Eye className="h-4 w-4 mr-2" />
                Read-Only Mode
              </Button>
              <Button
                variant={emergencyControls.disablePayments ? "destructive" : "outline"}
                size="sm"
                onClick={() => handleEmergencyToggle('disablePayments')}
                className="justify-start"
              >
                <Lock className="h-4 w-4 mr-2" />
                Disable Payments
              </Button>
              <Button
                variant={emergencyControls.pauseAgents ? "destructive" : "outline"}
                size="sm"
                onClick={() => handleEmergencyToggle('pauseAgents')}
                className="justify-start"
              >
                <Pause className="h-4 w-4 mr-2" />
                Pause AI Agents
              </Button>
            </div>
            
            <div className="pt-4 border-t space-y-2">
              <h4 className="font-medium text-sm">Rate Limiting Status</h4>
              <div className="text-xs text-muted-foreground space-y-1">
                <div>Impersonate: 5/hour per admin</div>
                <div>Bulk Operations: 10/hour</div>
                <div>Data Export: 20/day</div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Performance Monitoring */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Cpu className="h-5 w-5" />
              Performance Metrics
            </CardTitle>
            <CardDescription>
              Real-time system performance indicators
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <Globe className="h-4 w-4" />
                  <span className="text-sm font-medium">API Latency</span>
                </div>
                <div className="text-xs text-muted-foreground">
                  <div>p50: {performanceMetrics?.apiLatency.p50}ms</div>
                  <div>p95: {performanceMetrics?.apiLatency.p95}ms</div>
                  <div>p99: {performanceMetrics?.apiLatency.p99}ms</div>
                </div>
              </div>
              
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <Database className="h-4 w-4" />
                  <span className="text-sm font-medium">Database</span>
                </div>
                <div className="text-xs text-muted-foreground">
                  <div>Slow queries: {performanceMetrics?.databaseQueries.slow_queries}</div>
                  <div>Avg time: {performanceMetrics?.databaseQueries.avg_query_time}ms</div>
                </div>
              </div>
              
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <HardDrive className="h-4 w-4" />
                  <span className="text-sm font-medium">Memory</span>
                </div>
                <div className="text-xs text-muted-foreground">
                  <div>Heap: {performanceMetrics?.memoryUsage.heap_mb}MB</div>
                  <div>RSS: {performanceMetrics?.memoryUsage.rss_mb}MB</div>
                </div>
              </div>
              
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <AlertTriangle className="h-4 w-4" />
                  <span className="text-sm font-medium">Error Rates</span>
                </div>
                <div className="text-xs text-muted-foreground">
                  <div>5xx: {performanceMetrics?.errorRates.rate_5xx}%</div>
                  <div>4xx: {performanceMetrics?.errorRates.rate_4xx}%</div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Alert Management & Quick Actions */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Alert Management */}
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <AlertTriangle className="h-5 w-5" />
              Active Alerts
            </CardTitle>
            <CardDescription>
              System alerts and notifications requiring attention
            </CardDescription>
          </CardHeader>
          <CardContent>
            <AlertManager />
          </CardContent>
        </Card>

        {/* Quick Actions */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Zap className="h-5 w-5" />
              Quick Actions
            </CardTitle>
            <CardDescription>
              Common administrative tasks
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            <Button variant="outline" className="w-full justify-start">
              <LifeBuoy className="h-4 w-4 mr-2" />
              Create Support Ticket
            </Button>
            <Button variant="outline" className="w-full justify-start">
              <Bell className="h-4 w-4 mr-2" />
              Send Platform Notification
            </Button>
            <Button variant="outline" className="w-full justify-start">
              <BarChart3 className="h-4 w-4 mr-2" />
              Generate Platform Report
            </Button>
            <Button variant="outline" className="w-full justify-start">
              <Users className="h-4 w-4 mr-2" />
              Broadcast System Message
            </Button>
            <Button variant="outline" className="w-full justify-start">
              <Timer className="h-4 w-4 mr-2" />
              View Audit Logs
            </Button>
          </CardContent>
        </Card>
      </div>

      {/* Platform Analytics Summary */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingUp className="h-5 w-5" />
            Platform Analytics Summary
          </CardTitle>
          <CardDescription>
            Key performance indicators and trends
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="space-y-2">
              <h4 className="font-medium">Daily Active Users</h4>
              <div className="h-24 bg-muted rounded flex items-center justify-center">
                <span className="text-sm text-muted-foreground">Chart placeholder</span>
              </div>
            </div>
            <div className="space-y-2">
              <h4 className="font-medium">Revenue Trend</h4>
              <div className="h-24 bg-muted rounded flex items-center justify-center">
                <span className="text-sm text-muted-foreground">Chart placeholder</span>
              </div>
            </div>
            <div className="space-y-2">
              <h4 className="font-medium">API Usage</h4>
              <div className="h-24 bg-muted rounded flex items-center justify-center">
                <span className="text-sm text-muted-foreground">Chart placeholder</span>
              </div>
            </div>
            <div className="space-y-2">
              <h4 className="font-medium">User Distribution</h4>
              <div className="h-24 bg-muted rounded flex items-center justify-center">
                <span className="text-sm text-muted-foreground">Chart placeholder</span>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
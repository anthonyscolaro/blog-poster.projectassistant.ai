# Lovable Prompt: Monitoring & Analytics Dashboard

## Business Context:
The monitoring and analytics system provides comprehensive visibility into Blog-Poster's performance, cost efficiency, and system health. It tracks the 5-agent pipeline performance, budget management, error monitoring, and content analytics to ensure optimal operation and ROI.

## User Story:
"As a content manager, I want comprehensive monitoring of system performance, cost tracking, agent reliability, and content analytics so I can optimize our content generation strategy, manage budgets effectively, and quickly identify and resolve issues."

## Monitoring Requirements:
- **System Health**: Real-time service monitoring and uptime tracking
- **Cost Analytics**: Detailed cost breakdowns and budget management
- **Agent Performance**: Success rates, execution times, and error tracking
- **Content Analytics**: Article performance, SEO metrics, and engagement
- **Alert Management**: Configurable alerts for issues and thresholds
- **Historical Reporting**: Trends and performance over time

## Prompt for Lovable:

Create a comprehensive monitoring and analytics dashboard for the Blog-Poster platform that provides real-time insights into system health, cost efficiency, agent performance, and content analytics with intelligent alerting and historical trend analysis.

**Monitoring Components:**

### Main Monitoring Page
```typescript
// src/pages/Monitoring.tsx
import { useState, useEffect } from 'react'
import { useQuery } from '@tanstack/react-query'
import { apiClient } from '@/services/api'
import { SystemHealth } from '@/components/monitoring/SystemHealth'
import { CostAnalytics } from '@/components/monitoring/CostAnalytics'
import { AgentPerformance } from '@/components/monitoring/AgentPerformance'
import { ContentAnalytics } from '@/components/monitoring/ContentAnalytics'
import { AlertsPanel } from '@/components/monitoring/AlertsPanel'
import { PerformanceCharts } from '@/components/monitoring/PerformanceCharts'
import { ErrorTracker } from '@/components/monitoring/ErrorTracker'
import { 
  Activity, 
  DollarSign, 
  Users, 
  TrendingUp, 
  AlertTriangle,
  BarChart3,
  Shield,
  Zap
} from 'lucide-react'
import { useWebSocket } from '@/hooks/useWebSocket'

interface MonitoringData {
  systemHealth: SystemHealthData
  costMetrics: CostMetricsData
  agentMetrics: AgentMetricsData
  contentMetrics: ContentMetricsData
  alerts: AlertData[]
  errors: ErrorData[]
}

interface SystemHealthData {
  uptime: number
  responseTime: number
  memoryUsage: number
  cpuUsage: number
  diskUsage: number
  activeConnections: number
  services: ServiceStatus[]
}

interface ServiceStatus {
  name: string
  status: 'healthy' | 'degraded' | 'down'
  lastCheck: string
  responseTime: number
  uptime: number
}

interface CostMetricsData {
  currentMonth: number
  previousMonth: number
  budget: number
  dailyCosts: DailyCost[]
  costByAgent: AgentCost[]
  projectedCost: number
  costPerArticle: number
}

interface DailyCost {
  date: string
  cost: number
  articles: number
}

interface AgentCost {
  agent: string
  cost: number
  executions: number
  avgCostPerExecution: number
}

interface AgentMetricsData {
  agents: AgentMetric[]
  totalExecutions: number
  successRate: number
  avgExecutionTime: number
  failureReasons: FailureReason[]
}

interface AgentMetric {
  name: string
  executions: number
  successRate: number
  avgExecutionTime: number
  totalCost: number
  lastExecution: string
  errors: number
}

interface FailureReason {
  reason: string
  count: number
  percentage: number
}

interface ContentMetricsData {
  totalArticles: number
  publishedThisMonth: number
  avgSeoScore: number
  topPerformingArticles: TopArticle[]
  seoScoreDistribution: ScoreDistribution[]
  engagementMetrics: EngagementData
}

interface TopArticle {
  id: string
  title: string
  views: number
  seoScore: number
  publishedAt: string
  engagementRate: number
}

interface AlertData {
  id: string
  type: 'warning' | 'error' | 'info'
  title: string
  message: string
  timestamp: string
  acknowledged: boolean
  source: string
}

export default function Monitoring() {
  const [timeRange, setTimeRange] = useState<'1h' | '24h' | '7d' | '30d'>('24h')
  const [activeTab, setActiveTab] = useState<'overview' | 'costs' | 'agents' | 'content' | 'errors'>('overview')
  const [alerts, setAlerts] = useState<AlertData[]>([])

  // Real-time monitoring data
  const { data: monitoringData, isLoading, error } = useQuery({
    queryKey: ['monitoring-data', timeRange],
    queryFn: () => apiClient.get<MonitoringData>(`/api/monitoring/dashboard?range=${timeRange}`),
    refetchInterval: 30000, // Refresh every 30 seconds
  })

  // WebSocket for real-time alerts
  const { isConnected } = useWebSocket('/ws/monitoring', {
    onMessage: (data) => {
      if (data.type === 'alert') {
        setAlerts(prev => [data.alert, ...prev.slice(0, 49)]) // Keep last 50 alerts
      } else if (data.type === 'system_update') {
        // Handle real-time system updates
      }
    }
  })

  const tabs = [
    { id: 'overview', label: 'Overview', icon: Activity },
    { id: 'costs', label: 'Cost Analytics', icon: DollarSign },
    { id: 'agents', label: 'Agent Performance', icon: Users },
    { id: 'content', label: 'Content Analytics', icon: TrendingUp },
    { id: 'errors', label: 'Error Tracking', icon: AlertTriangle },
  ]

  if (isLoading) {
    return <MonitoringSkeleton />
  }

  if (error) {
    return (
      <div className="max-w-7xl mx-auto">
        <div className="text-center py-12">
          <AlertTriangle className="h-16 w-16 text-red-500 mx-auto mb-4" />
          <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-2">
            Monitoring Unavailable
          </h2>
          <p className="text-gray-600 dark:text-gray-400">
            Unable to load monitoring data. Please check system health.
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            Monitoring & Analytics
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            System health, performance metrics, and cost analytics
          </p>
        </div>

        {/* Time Range Selector */}
        <div className="flex items-center gap-2">
          <span className="text-sm text-gray-600 dark:text-gray-400">Time Range:</span>
          <select
            value={timeRange}
            onChange={(e) => setTimeRange(e.target.value as any)}
            className="px-3 py-2 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg text-sm"
          >
            <option value="1h">Last Hour</option>
            <option value="24h">Last 24 Hours</option>
            <option value="7d">Last 7 Days</option>
            <option value="30d">Last 30 Days</option>
          </select>
        </div>
      </div>

      {/* Connection Status */}
      <div className="flex items-center gap-2 mb-6">
        <div className={`h-2 w-2 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`} />
        <span className="text-sm text-gray-600 dark:text-gray-400">
          {isConnected ? 'Real-time monitoring active' : 'Real-time monitoring disconnected'}
        </span>
      </div>

      {/* Active Alerts */}
      {alerts.filter(a => !a.acknowledged).length > 0 && (
        <div className="mb-8">
          <AlertsPanel 
            alerts={alerts.filter(a => !a.acknowledged)} 
            onAcknowledge={(alertId) => {
              setAlerts(prev => prev.map(a => 
                a.id === alertId ? { ...a, acknowledged: true } : a
              ))
            }}
          />
        </div>
      )}

      {/* Tab Navigation */}
      <div className="flex space-x-1 mb-6">
        {tabs.map((tab) => (
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
        {activeTab === 'overview' && (
          <>
            {/* System Health Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
              <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
                <div className="flex items-center justify-between mb-4">
                  <Shield className="h-8 w-8 text-green-500" />
                  <span className="text-2xl font-bold text-gray-900 dark:text-white">
                    {(monitoringData?.systemHealth.uptime || 0).toFixed(1)}%
                  </span>
                </div>
                <p className="text-sm text-gray-600 dark:text-gray-400">System Uptime</p>
              </div>

              <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
                <div className="flex items-center justify-between mb-4">
                  <Zap className="h-8 w-8 text-blue-500" />
                  <span className="text-2xl font-bold text-gray-900 dark:text-white">
                    {monitoringData?.systemHealth.responseTime || 0}ms
                  </span>
                </div>
                <p className="text-sm text-gray-600 dark:text-gray-400">Avg Response Time</p>
              </div>

              <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
                <div className="flex items-center justify-between mb-4">
                  <DollarSign className="h-8 w-8 text-purple-500" />
                  <span className="text-2xl font-bold text-gray-900 dark:text-white">
                    ${(monitoringData?.costMetrics.currentMonth || 0).toFixed(2)}
                  </span>
                </div>
                <p className="text-sm text-gray-600 dark:text-gray-400">Monthly Spend</p>
              </div>

              <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
                <div className="flex items-center justify-between mb-4">
                  <TrendingUp className="h-8 w-8 text-orange-500" />
                  <span className="text-2xl font-bold text-gray-900 dark:text-white">
                    {(monitoringData?.agentMetrics.successRate || 0).toFixed(1)}%
                  </span>
                </div>
                <p className="text-sm text-gray-600 dark:text-gray-400">Success Rate</p>
              </div>
            </div>

            {/* Overview Charts */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <SystemHealth data={monitoringData?.systemHealth} />
              <PerformanceCharts 
                data={{
                  executions: monitoringData?.agentMetrics.totalExecutions || 0,
                  costs: monitoringData?.costMetrics.dailyCosts || [],
                  successRate: monitoringData?.agentMetrics.successRate || 0
                }} 
                timeRange={timeRange}
              />
            </div>
          </>
        )}

        {activeTab === 'costs' && (
          <CostAnalytics 
            data={monitoringData?.costMetrics} 
            timeRange={timeRange} 
          />
        )}

        {activeTab === 'agents' && (
          <AgentPerformance 
            data={monitoringData?.agentMetrics}
            timeRange={timeRange}
          />
        )}

        {activeTab === 'content' && (
          <ContentAnalytics 
            data={monitoringData?.contentMetrics}
            timeRange={timeRange}
          />
        )}

        {activeTab === 'errors' && (
          <ErrorTracker 
            errors={monitoringData?.errors || []}
            timeRange={timeRange}
          />
        )}
      </div>
    </div>
  )
}
```

### System Health Component
```typescript
// src/components/monitoring/SystemHealth.tsx
import { useState } from 'react'
import { 
  Server, 
  Database, 
  Wifi, 
  HardDrive,
  Cpu,
  MemoryStick,
  CheckCircle,
  AlertTriangle,
  XCircle
} from 'lucide-react'

interface SystemHealthProps {
  data?: {
    uptime: number
    responseTime: number
    memoryUsage: number
    cpuUsage: number
    diskUsage: number
    activeConnections: number
    services: {
      name: string
      status: 'healthy' | 'degraded' | 'down'
      lastCheck: string
      responseTime: number
      uptime: number
    }[]
  }
}

export function SystemHealth({ data }: SystemHealthProps) {
  const [expandedService, setExpandedService] = useState<string | null>(null)

  if (!data) return <SystemHealthSkeleton />

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'healthy':
        return <CheckCircle className="h-4 w-4 text-green-500" />
      case 'degraded':
        return <AlertTriangle className="h-4 w-4 text-yellow-500" />
      case 'down':
        return <XCircle className="h-4 w-4 text-red-500" />
      default:
        return <AlertTriangle className="h-4 w-4 text-gray-500" />
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'healthy':
        return 'text-green-600'
      case 'degraded':
        return 'text-yellow-600'
      case 'down':
        return 'text-red-600'
      default:
        return 'text-gray-600'
    }
  }

  const getUsageColor = (usage: number) => {
    if (usage >= 90) return 'bg-red-500'
    if (usage >= 75) return 'bg-yellow-500'
    return 'bg-green-500'
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
          System Health
        </h3>
        <div className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400">
          <div className="h-2 w-2 bg-green-500 rounded-full animate-pulse" />
          Live monitoring
        </div>
      </div>

      {/* Resource Usage */}
      <div className="grid grid-cols-2 gap-4 mb-6">
        <div className="flex items-center gap-3">
          <Cpu className="h-5 w-5 text-gray-400" />
          <div className="flex-1">
            <div className="flex items-center justify-between mb-1">
              <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                CPU Usage
              </span>
              <span className="text-sm text-gray-600 dark:text-gray-400">
                {data.cpuUsage.toFixed(1)}%
              </span>
            </div>
            <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
              <div 
                className={`h-2 rounded-full transition-all ${getUsageColor(data.cpuUsage)}`}
                style={{ width: `${Math.min(data.cpuUsage, 100)}%` }}
              />
            </div>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <MemoryStick className="h-5 w-5 text-gray-400" />
          <div className="flex-1">
            <div className="flex items-center justify-between mb-1">
              <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                Memory Usage
              </span>
              <span className="text-sm text-gray-600 dark:text-gray-400">
                {data.memoryUsage.toFixed(1)}%
              </span>
            </div>
            <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
              <div 
                className={`h-2 rounded-full transition-all ${getUsageColor(data.memoryUsage)}`}
                style={{ width: `${Math.min(data.memoryUsage, 100)}%` }}
              />
            </div>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <HardDrive className="h-5 w-5 text-gray-400" />
          <div className="flex-1">
            <div className="flex items-center justify-between mb-1">
              <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                Disk Usage
              </span>
              <span className="text-sm text-gray-600 dark:text-gray-400">
                {data.diskUsage.toFixed(1)}%
              </span>
            </div>
            <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
              <div 
                className={`h-2 rounded-full transition-all ${getUsageColor(data.diskUsage)}`}
                style={{ width: `${Math.min(data.diskUsage, 100)}%` }}
              />
            </div>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <Wifi className="h-5 w-5 text-gray-400" />
          <div className="flex-1">
            <div className="flex items-center justify-between mb-1">
              <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                Connections
              </span>
              <span className="text-sm text-gray-600 dark:text-gray-400">
                {data.activeConnections}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Services Status */}
      <div>
        <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
          Service Status
        </h4>
        <div className="space-y-2">
          {data.services.map((service) => (
            <div 
              key={service.name}
              className="p-3 bg-gray-50 dark:bg-gray-900 rounded-lg cursor-pointer"
              onClick={() => setExpandedService(
                expandedService === service.name ? null : service.name
              )}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  {getStatusIcon(service.status)}
                  <div>
                    <p className="font-medium text-gray-900 dark:text-white">
                      {service.name}
                    </p>
                    <p className="text-xs text-gray-600 dark:text-gray-400">
                      Last check: {new Date(service.lastCheck).toLocaleTimeString()}
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <p className={`text-sm font-medium capitalize ${getStatusColor(service.status)}`}>
                    {service.status}
                  </p>
                  <p className="text-xs text-gray-600 dark:text-gray-400">
                    {service.responseTime}ms
                  </p>
                </div>
              </div>
              
              {expandedService === service.name && (
                <div className="mt-3 pt-3 border-t border-gray-200 dark:border-gray-700">
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <p className="text-gray-600 dark:text-gray-400">Uptime</p>
                      <p className="font-medium text-gray-900 dark:text-white">
                        {service.uptime.toFixed(2)}%
                      </p>
                    </div>
                    <div>
                      <p className="text-gray-600 dark:text-gray-400">Response Time</p>
                      <p className="font-medium text-gray-900 dark:text-white">
                        {service.responseTime}ms
                      </p>
                    </div>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

function SystemHealthSkeleton() {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
      <div className="animate-pulse space-y-6">
        <div className="flex items-center justify-between">
          <div className="h-6 bg-gray-200 dark:bg-gray-700 rounded w-32" />
          <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-24" />
        </div>
        
        <div className="grid grid-cols-2 gap-4">
          {Array.from({ length: 4 }).map((_, i) => (
            <div key={i} className="space-y-2">
              <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-20" />
              <div className="h-2 bg-gray-200 dark:bg-gray-700 rounded" />
            </div>
          ))}
        </div>
        
        <div className="space-y-3">
          <div className="h-5 bg-gray-200 dark:bg-gray-700 rounded w-24" />
          {Array.from({ length: 5 }).map((_, i) => (
            <div key={i} className="h-12 bg-gray-200 dark:bg-gray-700 rounded" />
          ))}
        </div>
      </div>
    </div>
  )
}
```

### Cost Analytics Component
```typescript
// src/components/monitoring/CostAnalytics.tsx
import { useState } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell } from 'recharts'
import { DollarSign, TrendingUp, TrendingDown, AlertTriangle, Target } from 'lucide-react'

interface CostAnalyticsProps {
  data?: {
    currentMonth: number
    previousMonth: number
    budget: number
    dailyCosts: { date: string; cost: number; articles: number }[]
    costByAgent: { agent: string; cost: number; executions: number; avgCostPerExecution: number }[]
    projectedCost: number
    costPerArticle: number
  }
  timeRange: string
}

const AGENT_COLORS = [
  '#8b5cf6', // purple
  '#3b82f6', // blue
  '#10b981', // green
  '#f59e0b', // yellow
  '#ef4444', // red
]

export function CostAnalytics({ data, timeRange }: CostAnalyticsProps) {
  const [chartType, setChartType] = useState<'daily' | 'agent' | 'trend'>('daily')

  if (!data) return <CostAnalyticsSkeleton />

  const budgetUsage = (data.currentMonth / data.budget) * 100
  const monthOverMonth = ((data.currentMonth - data.previousMonth) / data.previousMonth) * 100
  const isOverBudget = budgetUsage > 100
  const isProjectedOverBudget = (data.projectedCost / data.budget) * 100 > 100

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(amount)
  }

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr)
    if (timeRange === '1h' || timeRange === '24h') {
      return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
    }
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
  }

  return (
    <div className="space-y-6">
      {/* Cost Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
          <div className="flex items-center justify-between mb-4">
            <DollarSign className="h-8 w-8 text-purple-500" />
            <span className={`text-sm font-medium px-2 py-1 rounded-full ${
              isOverBudget 
                ? 'bg-red-100 text-red-700 dark:bg-red-900/20 dark:text-red-400' 
                : 'bg-green-100 text-green-700 dark:bg-green-900/20 dark:text-green-400'
            }`}>
              {budgetUsage.toFixed(0)}%
            </span>
          </div>
          <div>
            <p className="text-2xl font-bold text-gray-900 dark:text-white">
              {formatCurrency(data.currentMonth)}
            </p>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              of {formatCurrency(data.budget)} budget
            </p>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
          <div className="flex items-center justify-between mb-4">
            <Target className="h-8 w-8 text-blue-500" />
            <span className={`text-sm font-medium px-2 py-1 rounded-full ${
              isProjectedOverBudget 
                ? 'bg-red-100 text-red-700 dark:bg-red-900/20 dark:text-red-400' 
                : 'bg-blue-100 text-blue-700 dark:bg-blue-900/20 dark:text-blue-400'
            }`}>
              Projected
            </span>
          </div>
          <div>
            <p className="text-2xl font-bold text-gray-900 dark:text-white">
              {formatCurrency(data.projectedCost)}
            </p>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              End of month estimate
            </p>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
          <div className="flex items-center justify-between mb-4">
            {monthOverMonth >= 0 ? (
              <TrendingUp className="h-8 w-8 text-red-500" />
            ) : (
              <TrendingDown className="h-8 w-8 text-green-500" />
            )}
            <span className={`text-sm font-medium px-2 py-1 rounded-full ${
              monthOverMonth >= 0 
                ? 'bg-red-100 text-red-700 dark:bg-red-900/20 dark:text-red-400' 
                : 'bg-green-100 text-green-700 dark:bg-green-900/20 dark:text-green-400'
            }`}>
              {monthOverMonth >= 0 ? '+' : ''}{monthOverMonth.toFixed(1)}%
            </span>
          </div>
          <div>
            <p className="text-2xl font-bold text-gray-900 dark:text-white">
              {formatCurrency(Math.abs(data.currentMonth - data.previousMonth))}
            </p>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              vs previous month
            </p>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
          <div className="flex items-center justify-between mb-4">
            <DollarSign className="h-8 w-8 text-green-500" />
            <span className="text-sm font-medium px-2 py-1 rounded-full bg-gray-100 text-gray-700 dark:bg-gray-900/20 dark:text-gray-400">
              Per Article
            </span>
          </div>
          <div>
            <p className="text-2xl font-bold text-gray-900 dark:text-white">
              {formatCurrency(data.costPerArticle)}
            </p>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Average cost per article
            </p>
          </div>
        </div>
      </div>

      {/* Budget Warning */}
      {(isOverBudget || isProjectedOverBudget) && (
        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-xl p-4">
          <div className="flex items-start gap-3">
            <AlertTriangle className="h-5 w-5 text-red-500 mt-0.5" />
            <div>
              <h4 className="font-medium text-red-700 dark:text-red-300">
                Budget Alert
              </h4>
              <p className="text-sm text-red-600 dark:text-red-400 mt-1">
                {isOverBudget 
                  ? `Current spending has exceeded the monthly budget by ${formatCurrency(data.currentMonth - data.budget)}.`
                  : `Projected spending will exceed the monthly budget by ${formatCurrency(data.projectedCost - data.budget)}.`
                }
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Chart Controls */}
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
          Cost Analytics
        </h3>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setChartType('daily')}
            className={`px-3 py-2 rounded-lg text-sm font-medium ${
              chartType === 'daily'
                ? 'bg-purple-100 dark:bg-purple-900 text-purple-700 dark:text-purple-300'
                : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800'
            }`}
          >
            Daily Trend
          </button>
          <button
            onClick={() => setChartType('agent')}
            className={`px-3 py-2 rounded-lg text-sm font-medium ${
              chartType === 'agent'
                ? 'bg-purple-100 dark:bg-purple-900 text-purple-700 dark:text-purple-300'
                : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800'
            }`}
          >
            By Agent
          </button>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Chart */}
        <div className="lg:col-span-2 bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
          {chartType === 'daily' ? (
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={data.dailyCosts}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis 
                  dataKey="date" 
                  tickFormatter={formatDate}
                  stroke="#6b7280"
                  fontSize={12}
                />
                <YAxis 
                  tickFormatter={(value) => `$${value}`}
                  stroke="#6b7280"
                  fontSize={12}
                />
                <Tooltip 
                  formatter={(value: number) => [formatCurrency(value), 'Cost']}
                  labelFormatter={formatDate}
                  contentStyle={{
                    backgroundColor: '#1f2937',
                    border: '1px solid #374151',
                    borderRadius: '8px'
                  }}
                />
                <Line 
                  type="monotone" 
                  dataKey="cost" 
                  stroke="#8b5cf6" 
                  strokeWidth={2}
                  dot={{ fill: '#8b5cf6', strokeWidth: 2, r: 4 }}
                  activeDot={{ r: 6 }}
                />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={data.costByAgent}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis 
                  dataKey="agent" 
                  stroke="#6b7280"
                  fontSize={12}
                />
                <YAxis 
                  tickFormatter={(value) => `$${value}`}
                  stroke="#6b7280"
                  fontSize={12}
                />
                <Tooltip 
                  formatter={(value: number) => [formatCurrency(value), 'Cost']}
                  contentStyle={{
                    backgroundColor: '#1f2937',
                    border: '1px solid #374151',
                    borderRadius: '8px'
                  }}
                />
                <Bar dataKey="cost" fill="#8b5cf6" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          )}
        </div>

        {/* Cost Distribution Pie Chart */}
        <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
          <h4 className="font-medium text-gray-900 dark:text-white mb-4">
            Cost Distribution
          </h4>
          <ResponsiveContainer width="100%" height={200}>
            <PieChart>
              <Pie
                data={data.costByAgent}
                cx="50%"
                cy="50%"
                innerRadius={40}
                outerRadius={80}
                dataKey="cost"
                nameKey="agent"
              >
                {data.costByAgent.map((entry, index) => (
                  <Cell 
                    key={`cell-${index}`} 
                    fill={AGENT_COLORS[index % AGENT_COLORS.length]} 
                  />
                ))}
              </Pie>
              <Tooltip formatter={(value: number) => formatCurrency(value)} />
            </PieChart>
          </ResponsiveContainer>

          {/* Legend */}
          <div className="mt-4 space-y-2">
            {data.costByAgent.map((agent, index) => (
              <div key={agent.agent} className="flex items-center justify-between text-sm">
                <div className="flex items-center gap-2">
                  <div 
                    className="w-3 h-3 rounded-full"
                    style={{ backgroundColor: AGENT_COLORS[index % AGENT_COLORS.length] }}
                  />
                  <span className="text-gray-700 dark:text-gray-300">
                    {agent.agent}
                  </span>
                </div>
                <span className="font-medium text-gray-900 dark:text-white">
                  {formatCurrency(agent.cost)}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Agent Cost Details */}
      <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
        <h4 className="font-medium text-gray-900 dark:text-white mb-4">
          Agent Cost Breakdown
        </h4>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="text-left text-sm text-gray-600 dark:text-gray-400">
                <th className="pb-3">Agent</th>
                <th className="pb-3">Total Cost</th>
                <th className="pb-3">Executions</th>
                <th className="pb-3">Avg Cost/Execution</th>
                <th className="pb-3">Share</th>
              </tr>
            </thead>
            <tbody className="text-sm">
              {data.costByAgent.map((agent, index) => (
                <tr key={agent.agent} className="border-t border-gray-200 dark:border-gray-700">
                  <td className="py-3">
                    <div className="flex items-center gap-3">
                      <div 
                        className="w-3 h-3 rounded-full"
                        style={{ backgroundColor: AGENT_COLORS[index % AGENT_COLORS.length] }}
                      />
                      <span className="font-medium text-gray-900 dark:text-white">
                        {agent.agent}
                      </span>
                    </div>
                  </td>
                  <td className="py-3 font-medium text-gray-900 dark:text-white">
                    {formatCurrency(agent.cost)}
                  </td>
                  <td className="py-3 text-gray-600 dark:text-gray-400">
                    {agent.executions.toLocaleString()}
                  </td>
                  <td className="py-3 text-gray-600 dark:text-gray-400">
                    {formatCurrency(agent.avgCostPerExecution)}
                  </td>
                  <td className="py-3 text-gray-600 dark:text-gray-400">
                    {((agent.cost / data.currentMonth) * 100).toFixed(1)}%
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}

function CostAnalyticsSkeleton() {
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {Array.from({ length: 4 }).map((_, i) => (
          <div key={i} className="animate-pulse bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-between mb-4">
              <div className="h-8 w-8 bg-gray-200 dark:bg-gray-700 rounded" />
              <div className="h-6 w-12 bg-gray-200 dark:bg-gray-700 rounded-full" />
            </div>
            <div className="space-y-2">
              <div className="h-8 bg-gray-200 dark:bg-gray-700 rounded w-20" />
              <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-32" />
            </div>
          </div>
        ))}
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
          <div className="h-80 bg-gray-200 dark:bg-gray-700 rounded animate-pulse" />
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
          <div className="h-60 bg-gray-200 dark:bg-gray-700 rounded animate-pulse" />
        </div>
      </div>
    </div>
  )
}
```

**Success Criteria:**
- Real-time system health monitoring with service status tracking
- Comprehensive cost analytics with budget management and alerts
- Agent performance tracking with success rates and execution times
- Content analytics showing SEO scores and engagement metrics
- Error tracking and debugging with detailed logs and trends
- Historical reporting with customizable time ranges
- Alert management with configurable thresholds and notifications
- Mobile-responsive charts and data visualization
- WebSocket integration for real-time updates
- Integration with existing authentication and API systems

This monitoring and analytics system provides comprehensive visibility into the Blog-Poster platform's performance, enabling proactive management and optimization of the content generation workflow.
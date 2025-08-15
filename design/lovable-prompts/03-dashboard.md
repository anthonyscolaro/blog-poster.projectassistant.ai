# Lovable Prompt: Main Dashboard

## Business Context:
The main dashboard is the command center for ServiceDogUS's content generation pipeline. It provides real-time visibility into the 5-agent orchestration system, showing pipeline status, article generation metrics, cost tracking, and system health.

## User Story:
"As a content manager, I want to see real-time metrics on article generation, costs, and pipeline performance so I can optimize our SEO content strategy and manage our budget effectively."

## Dashboard Metrics:
- **Pipeline Status**: Current and recent executions
- **Article Metrics**: Generated, published, scheduled
- **Cost Tracking**: Daily, monthly, per-article costs
- **Agent Performance**: Success rates, execution times
- **SEO Scores**: Average article quality metrics

## Prompt for Lovable:

Create a comprehensive dashboard for the Blog-Poster platform that displays real-time metrics from the 5-agent content generation pipeline. The dashboard should provide immediate insights into system performance, cost efficiency, and content quality.

**Dashboard Components:**

### Animated Key Metrics Grid
```typescript
// src/components/dashboard/MetricsGrid.tsx
import { useQuery } from '@tanstack/react-query'
import { motion } from 'framer-motion'
import { apiClient } from '@/services/api'
import { StaggerContainer, AnimatedCounter, FadeInSection } from '@/components/ui/AnimatedComponents'
import {
  FileText,
  DollarSign,
  TrendingUp,
  Clock,
  CheckCircle,
  AlertCircle
} from 'lucide-react'

interface DashboardMetrics {
  todayArticles: number
  monthlyArticles: number
  todayCost: number
  monthlyCost: number
  monthlyBudget: number
  avgSeoScore: number
  pipelineSuccessRate: number
  avgGenerationTime: number
}

export function MetricsGrid() {
  const { data: metrics, isLoading } = useQuery({
    queryKey: ['dashboard-metrics'],
    queryFn: () => apiClient.get<DashboardMetrics>('/api/metrics/dashboard'),
    refetchInterval: 30000, // Refresh every 30 seconds
  })

  if (isLoading) {
    return <MetricsGridSkeleton />
  }

  const costPercentage = ((metrics?.monthlyCost || 0) / (metrics?.monthlyBudget || 1)) * 100
  const isOverBudget = costPercentage > 80

  const cards = [
    {
      title: "Today's Articles",
      value: metrics?.todayArticles || 0,
      subtitle: `${metrics?.monthlyArticles || 0} this month`,
      icon: FileText,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100',
    },
    {
      title: 'Monthly Cost',
      value: `$${(metrics?.monthlyCost || 0).toFixed(2)}`,
      subtitle: `of $${metrics?.monthlyBudget} budget`,
      icon: DollarSign,
      color: isOverBudget ? 'text-red-600' : 'text-green-600',
      bgColor: isOverBudget ? 'bg-red-100' : 'bg-green-100',
      badge: costPercentage > 0 ? `${costPercentage.toFixed(0)}%` : null,
    },
    {
      title: 'SEO Score',
      value: `${metrics?.avgSeoScore || 0}/100`,
      subtitle: 'Average quality',
      icon: TrendingUp,
      color: 'text-purple-600',
      bgColor: 'bg-purple-100',
    },
    {
      title: 'Success Rate',
      value: `${(metrics?.pipelineSuccessRate || 0).toFixed(1)}%`,
      subtitle: `~${Math.floor(metrics?.avgGenerationTime || 0)}s per article`,
      icon: CheckCircle,
      color: 'text-emerald-600',
      bgColor: 'bg-emerald-100',
    },
  ]

  return (
    <StaggerContainer className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      {cards.map((card, index) => (
        <motion.div
          key={index}
          className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700 hover:shadow-lg transition-shadow duration-200"
          whileHover={{ y: -2 }}
          transition={{ type: "spring", stiffness: 300 }}
        >
          <div className="flex items-center justify-between mb-4">
            <motion.div 
              className={`p-3 rounded-lg ${card.bgColor} dark:bg-opacity-20`}
              whileHover={{ scale: 1.1, rotate: 5 }}
              transition={{ type: "spring", stiffness: 400 }}
            >
              <card.icon className={`h-6 w-6 ${card.color}`} />
            </motion.div>
            {card.badge && (
              <motion.span 
                className={`text-sm font-medium px-2 py-1 rounded-full ${
                  isOverBudget ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'
                }`}
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ delay: index * 0.1 + 0.3, type: "spring" }}
              >
                {card.badge}
              </motion.span>
            )}
          </div>
          <div>
            <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
              {card.title}
            </p>
            <div className="text-2xl font-bold text-gray-900 dark:text-white mt-1">
              {card.title === 'Monthly Articles' || card.title === 'Today\'s Articles' ? (
                <AnimatedCounter 
                  value={parseInt(card.value)} 
                  duration={1.5} 
                />
              ) : card.title === 'Monthly Cost' || card.title === 'Today\'s Cost' ? (
                <AnimatedCounter 
                  value={parseFloat(card.value.replace('$', ''))} 
                  prefix="$" 
                  decimals={2}
                  duration={1.5}
                />
              ) : (
                card.value
              )}
            </div>
            <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
              {card.subtitle}
            </p>
          </div>
        </motion.div>
      ))}
    </StaggerContainer>
  )
}
```

### Animated Pipeline Status Component
```typescript
// src/components/dashboard/PipelineStatus.tsx
import { useQuery } from '@tanstack/react-query'
import { motion, AnimatePresence } from 'framer-motion'
import { apiClient } from '@/services/api'
import { FadeInSection, PulseEffect } from '@/components/ui/AnimatedComponents'
import { Workflow, Circle, CheckCircle2, XCircle, Loader2 } from 'lucide-react'

interface PipelineExecution {
  id: string
  status: 'pending' | 'running' | 'completed' | 'failed'
  agentsCompleted: string[]
  currentAgent: string | null
  startedAt: string
  completedAt: string | null
  articleTitle: string | null
  totalCost: number
  errorMessage: string | null
}

const AGENTS = [
  { id: 'competitor', name: 'Competitor Monitor', icon: '🔍' },
  { id: 'topic', name: 'Topic Analyzer', icon: '📊' },
  { id: 'article', name: 'Article Generator', icon: '✍️' },
  { id: 'legal', name: 'Legal Checker', icon: '⚖️' },
  { id: 'wordpress', name: 'WordPress Publisher', icon: '🚀' },
]

export function PipelineStatus() {
  const { data: executions, isLoading } = useQuery({
    queryKey: ['pipeline-executions'],
    queryFn: () => apiClient.get<PipelineExecution[]>('/pipeline/history?limit=5'),
    refetchInterval: 5000, // Refresh every 5 seconds
  })

  const currentExecution = executions?.[0]
  const isRunning = currentExecution?.status === 'running'

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <Workflow className="h-5 w-5 text-purple-600" />
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
            Pipeline Status
          </h2>
        </div>
        {isRunning && (
          <div className="flex items-center gap-2 text-sm text-green-600">
            <Circle className="h-2 w-2 fill-current animate-pulse" />
            <span>Active</span>
          </div>
        )}
      </div>

      {/* Current Execution Progress */}
      {currentExecution && (
        <div className="mb-6">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-gray-600 dark:text-gray-400">
              Current Pipeline
            </span>
            <span className="text-xs text-gray-500">
              Started {new Date(currentExecution.startedAt).toLocaleTimeString()}
            </span>
          </div>
          
          {/* Animated Agent Progress */}
          <motion.div 
            className="space-y-3"
            initial="hidden"
            animate="visible"
            variants={{
              hidden: { opacity: 1 },
              visible: {
                opacity: 1,
                transition: {
                  staggerChildren: 0.1
                }
              }
            }}
          >
            {AGENTS.map((agent, index) => {
              const isCompleted = currentExecution.agentsCompleted.includes(agent.id)
              const isCurrent = currentExecution.currentAgent === agent.id
              const isFailed = currentExecution.status === 'failed' && isCurrent
              
              return (
                <motion.div 
                  key={agent.id} 
                  className="flex items-center gap-3"
                  variants={{
                    hidden: { x: -20, opacity: 0 },
                    visible: { x: 0, opacity: 1 }
                  }}
                  transition={{ duration: 0.3 }}
                >
                  <motion.span 
                    className="text-lg"
                    animate={isCurrent ? { 
                      scale: [1, 1.2, 1],
                      rotate: [0, 10, -10, 0]
                    } : { scale: 1 }}
                    transition={{ 
                      duration: isCurrent ? 2 : 0.3, 
                      repeat: isCurrent ? Infinity : 0 
                    }}
                  >
                    {agent.icon}
                  </motion.span>
                  <div className="flex-1">
                    <div className="flex items-center justify-between mb-1">
                      <span className={`text-sm font-medium transition-colors duration-300 ${
                        isCurrent ? 'text-blue-600 dark:text-blue-400' : 
                        isCompleted ? 'text-green-600 dark:text-green-400' :
                        'text-gray-700 dark:text-gray-300'
                      }`}>
                        {agent.name}
                      </span>
                      <AnimatePresence mode="wait">
                        {isCompleted && (
                          <motion.div
                            key="completed"
                            initial={{ scale: 0, rotate: -180 }}
                            animate={{ scale: 1, rotate: 0 }}
                            exit={{ scale: 0, rotate: 180 }}
                            transition={{ type: "spring", stiffness: 300 }}
                          >
                            <CheckCircle2 className="h-4 w-4 text-green-500" />
                          </motion.div>
                        )}
                        {isCurrent && !isFailed && (
                          <motion.div
                            key="current"
                            initial={{ scale: 0 }}
                            animate={{ scale: 1 }}
                            exit={{ scale: 0 }}
                          >
                            <Loader2 className="h-4 w-4 text-blue-500 animate-spin" />
                          </motion.div>
                        )}
                        {isFailed && (
                          <motion.div
                            key="failed"
                            initial={{ scale: 0 }}
                            animate={{ scale: 1 }}
                            exit={{ scale: 0 }}
                          >
                            <XCircle className="h-4 w-4 text-red-500" />
                          </motion.div>
                        )}
                      </AnimatePresence>
                    </div>
                    <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 overflow-hidden">
                      <motion.div
                        className={`h-2 rounded-full ${
                          isCompleted
                            ? 'bg-green-500'
                            : isCurrent
                            ? 'bg-blue-500'
                            : isFailed
                            ? 'bg-red-500'
                            : 'bg-gray-300'
                        }`}
                        initial={{ width: '0%' }}
                        animate={{ 
                          width: isCompleted ? '100%' : 
                                isCurrent ? '50%' : 
                                isFailed ? '50%' : '0%'
                        }}
                        transition={{ 
                          duration: 0.5,
                          ease: "easeOut"
                        }}
                      />
                    </div>
                  </div>
                </motion.div>
              )
            })}
          </motion.div>

          {/* Animated Error Message */}
          <AnimatePresence>
            {currentExecution.errorMessage && (
              <motion.div 
                className="mt-4 p-3 bg-red-50 dark:bg-red-900/20 rounded-lg border border-red-200 dark:border-red-800"
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: "auto" }}
                exit={{ opacity: 0, height: 0 }}
                transition={{ duration: 0.3 }}
              >
                <motion.p 
                  className="text-sm text-red-600 dark:text-red-400"
                  initial={{ x: -10 }}
                  animate={{ x: 0 }}
                  transition={{ delay: 0.1 }}
                >
                  {currentExecution.errorMessage}
                </motion.p>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      )}

      {/* Recent Executions */}
      <div>
        <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-3">
          Recent Executions
        </h3>
        <div className="space-y-2">
          {executions?.slice(1, 4).map((execution) => (
            <div
              key={execution.id}
              className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-900 rounded-lg"
            >
              <div className="flex items-center gap-3">
                <div className={`h-2 w-2 rounded-full ${
                  execution.status === 'completed' ? 'bg-green-500' :
                  execution.status === 'failed' ? 'bg-red-500' :
                  execution.status === 'running' ? 'bg-blue-500 animate-pulse' :
                  'bg-gray-400'
                }`} />
                <div>
                  <p className="text-sm font-medium text-gray-900 dark:text-white">
                    {execution.articleTitle || 'Pipeline Execution'}
                  </p>
                  <p className="text-xs text-gray-500">
                    {new Date(execution.startedAt).toLocaleString()}
                  </p>
                </div>
              </div>
              <span className="text-sm text-gray-600 dark:text-gray-400">
                ${execution.totalCost.toFixed(2)}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
```

### Recent Articles Component
```typescript
// src/components/dashboard/RecentArticles.tsx
import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { apiClient } from '@/services/api'
import { FileText, ExternalLink, Clock, TrendingUp } from 'lucide-react'

interface Article {
  id: string
  title: string
  slug: string
  status: 'draft' | 'published' | 'scheduled'
  seoScore: number
  generationCost: number
  wordCount: number
  createdAt: string
  publishedAt: string | null
}

export function RecentArticles() {
  const { data: articles, isLoading } = useQuery({
    queryKey: ['recent-articles'],
    queryFn: () => apiClient.get<Article[]>('/api/articles?limit=5'),
  })

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'published':
        return 'bg-green-100 text-green-700 dark:bg-green-900/20 dark:text-green-400'
      case 'scheduled':
        return 'bg-blue-100 text-blue-700 dark:bg-blue-900/20 dark:text-blue-400'
      default:
        return 'bg-gray-100 text-gray-700 dark:bg-gray-900/20 dark:text-gray-400'
    }
  }

  const getSeoScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600'
    if (score >= 60) return 'text-yellow-600'
    return 'text-red-600'
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <FileText className="h-5 w-5 text-purple-600" />
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
            Recent Articles
          </h2>
        </div>
        <Link
          to="/articles"
          className="text-sm text-purple-600 hover:text-purple-700 dark:text-purple-400 font-medium"
        >
          View all →
        </Link>
      </div>

      <div className="space-y-4">
        {articles?.map((article) => (
          <div
            key={article.id}
            className="p-4 bg-gray-50 dark:bg-gray-900 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
          >
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-2">
                  <Link
                    to={`/articles/${article.id}`}
                    className="font-medium text-gray-900 dark:text-white hover:text-purple-600 dark:hover:text-purple-400"
                  >
                    {article.title}
                  </Link>
                  <ExternalLink className="h-3 w-3 text-gray-400" />
                </div>
                
                <div className="flex items-center gap-4 text-sm text-gray-600 dark:text-gray-400">
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(article.status)}`}>
                    {article.status}
                  </span>
                  <div className="flex items-center gap-1">
                    <TrendingUp className="h-3 w-3" />
                    <span className={`font-medium ${getSeoScoreColor(article.seoScore)}`}>
                      {article.seoScore}/100
                    </span>
                  </div>
                  <div className="flex items-center gap-1">
                    <Clock className="h-3 w-3" />
                    <span>{article.wordCount} words</span>
                  </div>
                  <span>${article.generationCost.toFixed(2)}</span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {(!articles || articles.length === 0) && !isLoading && (
        <div className="text-center py-8">
          <FileText className="h-12 w-12 text-gray-300 dark:text-gray-600 mx-auto mb-3" />
          <p className="text-gray-500 dark:text-gray-400">No articles yet</p>
          <Link
            to="/pipeline"
            className="mt-4 inline-flex items-center px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700"
          >
            Generate First Article
          </Link>
        </div>
      )}
    </div>
  )
}
```

### Main Dashboard Page
```typescript
// src/pages/Dashboard.tsx
import { MetricsGrid } from '@/components/dashboard/MetricsGrid'
import { PipelineStatus } from '@/components/dashboard/PipelineStatus'
import { RecentArticles } from '@/components/dashboard/RecentArticles'
import { CostChart } from '@/components/dashboard/CostChart'
import { AgentPerformance } from '@/components/dashboard/AgentPerformance'
import { QuickActions } from '@/components/dashboard/QuickActions'
import { useAuth } from '@/contexts/AuthContext'

export default function Dashboard() {
  const { user } = useAuth()
  const firstName = user?.user_metadata?.full_name?.split(' ')[0] || 'there'

  return (
    <div className="max-w-7xl mx-auto">
      {/* Welcome Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          Welcome back, {firstName}! 👋
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
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

      {/* Cost Tracking Chart */}
      <div className="mb-8">
        <CostChart />
      </div>

      {/* Recent Articles */}
      <RecentArticles />
    </div>
  )
}
```

### Quick Actions Component
```typescript
// src/components/dashboard/QuickActions.tsx
import { useNavigate } from 'react-router-dom'
import { Play, FileText, Settings, TrendingUp } from 'lucide-react'

export function QuickActions() {
  const navigate = useNavigate()

  const actions = [
    {
      label: 'Start Pipeline',
      icon: Play,
      color: 'bg-purple-gradient',
      onClick: () => navigate('/pipeline'),
    },
    {
      label: 'New Article',
      icon: FileText,
      color: 'bg-blue-500',
      onClick: () => navigate('/articles/new'),
    },
    {
      label: 'View Analytics',
      icon: TrendingUp,
      color: 'bg-green-500',
      onClick: () => navigate('/monitoring'),
    },
    {
      label: 'Settings',
      icon: Settings,
      color: 'bg-gray-500',
      onClick: () => navigate('/settings'),
    },
  ]

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
      {actions.map((action, index) => (
        <button
          key={index}
          onClick={action.onClick}
          className="group relative overflow-hidden rounded-xl p-6 text-white transition-transform hover:scale-105"
        >
          <div className={`absolute inset-0 ${action.color} opacity-90`} />
          <div className="relative z-10">
            <action.icon className="h-8 w-8 mb-3" />
            <p className="font-medium">{action.label}</p>
          </div>
        </button>
      ))}
    </div>
  )
}
```

**Success Criteria:**
- Real-time metrics updating every 30 seconds
- Pipeline execution progress visualization
- Cost tracking with budget warnings
- Recent articles with SEO scores
- Quick action buttons for common tasks
- Mobile-responsive grid layout
- Dark mode support throughout

This dashboard provides comprehensive visibility into the Blog-Poster platform's performance, enabling efficient content generation management.
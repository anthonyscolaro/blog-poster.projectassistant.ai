import { useQuery } from '@tanstack/react-query'
import { motion } from 'framer-motion'
import { StaggerContainer, AnimatedCounter } from '@/components/ui/AnimatedComponents'
import { Skeleton } from '@/components/ui/skeleton'
import {
  FileText,
  DollarSign,
  TrendingUp,
  CheckCircle
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

// Mock data for now - replace with actual API call
const mockMetrics: DashboardMetrics = {
  todayArticles: 8,
  monthlyArticles: 142,
  todayCost: 24.50,
  monthlyCost: 387.20,
  monthlyBudget: 500,
  avgSeoScore: 94,
  pipelineSuccessRate: 96.2,
  avgGenerationTime: 45
}

function MetricsGridSkeleton() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      {Array.from({ length: 4 }).map((_, i) => (
        <div key={i} className="bg-card rounded-xl p-6 shadow-sm border">
          <div className="flex items-center justify-between mb-4">
            <Skeleton className="h-12 w-12 rounded-lg" />
            <Skeleton className="h-6 w-12 rounded-full" />
          </div>
          <Skeleton className="h-4 w-24 mb-2" />
          <Skeleton className="h-8 w-16 mb-1" />
          <Skeleton className="h-3 w-20" />
        </div>
      ))}
    </div>
  )
}

export function MetricsGrid() {
  const { data: metrics, isLoading } = useQuery({
    queryKey: ['dashboard-metrics'],
    queryFn: async () => {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000))
      return mockMetrics
    },
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
      color: 'text-blue-600 dark:text-blue-400',
      bgColor: 'bg-blue-100 dark:bg-blue-900/20',
    },
    {
      title: 'Monthly Cost',
      value: `$${(metrics?.monthlyCost || 0).toFixed(2)}`,
      subtitle: `of $${metrics?.monthlyBudget} budget`,
      icon: DollarSign,
      color: isOverBudget ? 'text-red-600 dark:text-red-400' : 'text-green-600 dark:text-green-400',
      bgColor: isOverBudget ? 'bg-red-100 dark:bg-red-900/20' : 'bg-green-100 dark:bg-green-900/20',
      badge: costPercentage > 0 ? `${costPercentage.toFixed(0)}%` : null,
    },
    {
      title: 'SEO Score',
      value: `${metrics?.avgSeoScore || 0}/100`,
      subtitle: 'Average quality',
      icon: TrendingUp,
      color: 'text-purple-600 dark:text-purple-400',
      bgColor: 'bg-purple-100 dark:bg-purple-900/20',
    },
    {
      title: 'Success Rate',
      value: `${(metrics?.pipelineSuccessRate || 0).toFixed(1)}%`,
      subtitle: `~${Math.floor(metrics?.avgGenerationTime || 0)}s per article`,
      icon: CheckCircle,
      color: 'text-emerald-600 dark:text-emerald-400',
      bgColor: 'bg-emerald-100 dark:bg-emerald-900/20',
    },
  ]

  return (
    <StaggerContainer className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      {cards.map((card, index) => (
        <motion.div
          key={index}
          className="bg-card rounded-xl p-6 shadow-sm border hover:shadow-lg transition-shadow duration-200"
          whileHover={{ y: -2 }}
          transition={{ type: "spring", stiffness: 300 }}
        >
          <div className="flex items-center justify-between mb-4">
            <motion.div 
              className={`p-3 rounded-lg ${card.bgColor}`}
              whileHover={{ scale: 1.1, rotate: 5 }}
              transition={{ type: "spring", stiffness: 400 }}
            >
              <card.icon className={`h-6 w-6 ${card.color}`} />
            </motion.div>
            {card.badge && (
              <motion.span 
                className={`text-sm font-medium px-2 py-1 rounded-full ${
                  isOverBudget ? 'bg-red-100 text-red-700 dark:bg-red-900/20 dark:text-red-400' : 'bg-green-100 text-green-700 dark:bg-green-900/20 dark:text-green-400'
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
            <p className="text-sm font-medium text-muted-foreground">
              {card.title}
            </p>
            <div className="text-2xl font-bold text-foreground mt-1">
              {card.title === 'Monthly Articles' || card.title === "Today's Articles" ? (
                <AnimatedCounter 
                  value={parseInt(card.value.toString())} 
                  duration={1.5} 
                />
              ) : card.title === 'Monthly Cost' ? (
                <AnimatedCounter 
                  value={parseFloat(card.value.toString().replace('$', ''))} 
                  prefix="$" 
                  decimals={2}
                  duration={1.5}
                />
              ) : (
                card.value
              )}
            </div>
            <p className="text-sm text-muted-foreground mt-1">
              {card.subtitle}
            </p>
          </div>
        </motion.div>
      ))}
    </StaggerContainer>
  )
}
import { useQuery } from '@tanstack/react-query'
import { motion } from 'framer-motion'
import { Activity, CheckCircle, Clock, AlertCircle } from 'lucide-react'

interface AgentStats {
  name: string
  icon: string
  successRate: number
  avgTime: number
  lastRun: string
  status: 'healthy' | 'warning' | 'error'
}

// Mock data for now
const mockAgentStats: AgentStats[] = [
  {
    name: 'Competitor Monitor',
    icon: '🔍',
    successRate: 98.5,
    avgTime: 12,
    lastRun: new Date(Date.now() - 1000 * 60 * 5).toISOString(),
    status: 'healthy'
  },
  {
    name: 'Topic Analyzer',
    icon: '📊',
    successRate: 96.2,
    avgTime: 8,
    lastRun: new Date(Date.now() - 1000 * 60 * 3).toISOString(),
    status: 'healthy'
  },
  {
    name: 'Article Generator',
    icon: '✍️',
    successRate: 94.8,
    avgTime: 45,
    lastRun: new Date(Date.now() - 1000 * 60 * 1).toISOString(),
    status: 'healthy'
  },
  {
    name: 'Legal Checker',
    icon: '⚖️',
    successRate: 89.3,
    avgTime: 15,
    lastRun: new Date(Date.now() - 1000 * 60 * 10).toISOString(),
    status: 'warning'
  },
  {
    name: 'WordPress Publisher',
    icon: '🚀',
    successRate: 92.1,
    avgTime: 6,
    lastRun: new Date(Date.now() - 1000 * 60 * 2).toISOString(),
    status: 'healthy'
  }
]

export function AgentPerformance() {
  const { data: agentStats, isLoading } = useQuery({
    queryKey: ['agent-performance'],
    queryFn: async () => {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 500))
      return mockAgentStats
    },
    refetchInterval: 30000,
  })

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'healthy':
        return <CheckCircle className="h-4 w-4 text-green-500" />
      case 'warning':
        return <AlertCircle className="h-4 w-4 text-yellow-500" />
      case 'error':
        return <AlertCircle className="h-4 w-4 text-red-500" />
      default:
        return <Clock className="h-4 w-4 text-gray-500" />
    }
  }

  const getSuccessRateColor = (rate: number) => {
    if (rate >= 95) return 'text-green-600 dark:text-green-400'
    if (rate >= 90) return 'text-yellow-600 dark:text-yellow-400'
    return 'text-red-600 dark:text-red-400'
  }

  return (
    <div className="bg-card rounded-xl p-6 shadow-sm border">
      <div className="flex items-center gap-3 mb-6">
        <Activity className="h-5 w-5 text-purple-600 dark:text-purple-400" />
        <h2 className="text-lg font-semibold text-foreground">
          Agent Performance
        </h2>
      </div>

      <div className="space-y-4">
        {agentStats?.map((agent, index) => (
          <motion.div
            key={agent.name}
            className="p-4 bg-muted/50 rounded-lg"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.1 }}
          >
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-3">
                <span className="text-lg">{agent.icon}</span>
                <span className="font-medium text-foreground">{agent.name}</span>
                {getStatusIcon(agent.status)}
              </div>
              <span className={`text-sm font-medium ${getSuccessRateColor(agent.successRate)}`}>
                {agent.successRate}%
              </span>
            </div>
            
            <div className="flex items-center justify-between text-sm text-muted-foreground">
              <span>Avg: {agent.avgTime}s</span>
              <span>Last: {new Date(agent.lastRun).toLocaleTimeString()}</span>
            </div>
            
            {/* Success Rate Bar */}
            <div className="mt-2 w-full bg-muted rounded-full h-1.5">
              <motion.div
                className={`h-1.5 rounded-full ${
                  agent.successRate >= 95 ? 'bg-green-500' :
                  agent.successRate >= 90 ? 'bg-yellow-500' :
                  'bg-red-500'
                }`}
                initial={{ width: '0%' }}
                animate={{ width: `${agent.successRate}%` }}
                transition={{ duration: 1, delay: index * 0.1 }}
              />
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  )
}
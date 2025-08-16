import { useQuery } from '@tanstack/react-query'
import { motion, AnimatePresence } from 'framer-motion'
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

// Mock data for now
const mockExecutions: PipelineExecution[] = [
  {
    id: '1',
    status: 'running',
    agentsCompleted: ['competitor', 'topic'],
    currentAgent: 'article',
    startedAt: new Date(Date.now() - 1000 * 60 * 5).toISOString(),
    completedAt: null,
    articleTitle: 'AI Content Strategy 2024',
    totalCost: 2.45,
    errorMessage: null,
  },
  {
    id: '2',
    status: 'completed',
    agentsCompleted: ['competitor', 'topic', 'article', 'legal', 'wordpress'],
    currentAgent: null,
    startedAt: new Date(Date.now() - 1000 * 60 * 60 * 2).toISOString(),
    completedAt: new Date(Date.now() - 1000 * 60 * 60 * 1.5).toISOString(),
    articleTitle: 'WordPress SEO Best Practices',
    totalCost: 3.20,
    errorMessage: null,
  }
]

export function PipelineStatus() {
  const { data: executions, isLoading } = useQuery({
    queryKey: ['pipeline-executions'],
    queryFn: async () => {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 500))
      return mockExecutions
    },
    refetchInterval: 5000, // Refresh every 5 seconds
  })

  const currentExecution = executions?.[0]
  const isRunning = currentExecution?.status === 'running'

  return (
    <div className="bg-card rounded-xl p-6 shadow-sm border">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <Workflow className="h-5 w-5 text-purple-600 dark:text-purple-400" />
          <h2 className="text-lg font-semibold text-foreground">
            Pipeline Status
          </h2>
        </div>
        {isRunning && (
          <div className="flex items-center gap-2 text-sm text-green-600 dark:text-green-400">
            <Circle className="h-2 w-2 fill-current animate-pulse" />
            <span>Active</span>
          </div>
        )}
      </div>

      {/* Current Execution Progress */}
      {currentExecution && (
        <div className="mb-6">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-muted-foreground">
              Current Pipeline
            </span>
            <span className="text-xs text-muted-foreground">
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
                        'text-foreground'
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
                    <div className="w-full bg-muted rounded-full h-2 overflow-hidden">
                      <motion.div
                        className={`h-2 rounded-full ${
                          isCompleted
                            ? 'bg-green-500'
                            : isCurrent
                            ? 'bg-blue-500'
                            : isFailed
                            ? 'bg-red-500'
                            : 'bg-muted-foreground/30'
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
        <h3 className="text-sm font-medium text-muted-foreground mb-3">
          Recent Executions
        </h3>
        <div className="space-y-2">
          {executions?.slice(1, 4).map((execution) => (
            <div
              key={execution.id}
              className="flex items-center justify-between p-3 bg-muted/50 rounded-lg"
            >
              <div className="flex items-center gap-3">
                <div className={`h-2 w-2 rounded-full ${
                  execution.status === 'completed' ? 'bg-green-500' :
                  execution.status === 'failed' ? 'bg-red-500' :
                  execution.status === 'running' ? 'bg-blue-500 animate-pulse' :
                  'bg-muted-foreground'
                }`} />
                <div>
                  <p className="text-sm font-medium text-foreground">
                    {execution.articleTitle || 'Pipeline Execution'}
                  </p>
                  <p className="text-xs text-muted-foreground">
                    {new Date(execution.startedAt).toLocaleString()}
                  </p>
                </div>
              </div>
              <span className="text-sm text-muted-foreground">
                ${execution.totalCost.toFixed(2)}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
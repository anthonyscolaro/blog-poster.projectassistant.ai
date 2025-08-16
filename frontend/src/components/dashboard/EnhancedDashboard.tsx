import React, { useState } from 'react'
import { motion, LayoutGroup, AnimatePresence, useScroll, useTransform } from 'framer-motion'
import { X, Users, DollarSign, FileText, Activity, TrendingUp } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { ScrollProgress, AnimatedProgress, PulsingIndicator } from '@/components/ui/AnimatedComponents'
import { fadeInUpVariants, staggerContainerVariants, cardHoverVariants } from '@/utils/animationVariants'

interface MetricCard {
  id: string
  icon: React.ComponentType<{ className?: string }>
  label: string
  value: string
  change: number
  trend: 'up' | 'down' | 'neutral'
  details: string[]
}

interface Pipeline {
  id: string
  name: string
  status: 'active' | 'pending' | 'completed'
  progress: number
  x: number
  y: number
}

const metrics: MetricCard[] = [
  {
    id: 'users',
    icon: Users,
    label: 'Active Users',
    value: '2,847',
    change: 12.5,
    trend: 'up',
    details: ['Daily active: 1,234', 'Weekly growth: +8%', 'Retention: 85%']
  },
  {
    id: 'revenue',
    icon: DollarSign,
    label: 'Monthly Revenue',
    value: '$28,350',
    change: 8.2,
    trend: 'up',
    details: ['MRR growth: +15%', 'ARPU: $87.50', 'Churn: 3.2%']
  },
  {
    id: 'articles',
    icon: FileText,
    label: 'Articles Generated',
    value: '847',
    change: -2.1,
    trend: 'down',
    details: ['Today: 67 articles', 'Quality score: 89%', 'Auto-published: 78%']
  },
  {
    id: 'performance',
    icon: Activity,
    label: 'System Health',
    value: '99.97%',
    change: 0.1,
    trend: 'up',
    details: ['API latency: 120ms', 'Uptime: 99.97%', 'Error rate: 0.02%']
  }
]

const pipelines: Pipeline[] = [
  { id: '1', name: 'Content Pipeline A', status: 'active', progress: 65, x: 50, y: 50 },
  { id: '2', name: 'SEO Optimizer', status: 'pending', progress: 30, x: 200, y: 100 },
  { id: '3', name: 'Social Publisher', status: 'active', progress: 90, x: 150, y: 150 },
  { id: '4', name: 'Analytics Tracker', status: 'completed', progress: 100, x: 300, y: 80 }
]

export function EnhancedDashboard() {
  const [selectedCard, setSelectedCard] = useState<string | null>(null)
  const [expandedSection, setExpandedSection] = useState<string | null>(null)

  const selectedMetric = metrics.find(m => m.id === selectedCard)

  return (
    <>
      <ScrollProgress />
      
      <LayoutGroup>
        <motion.div 
          className="p-6 space-y-8"
          initial="hidden"
          animate="visible"
          variants={staggerContainerVariants}
        >
          {/* Header */}
          <motion.div variants={fadeInUpVariants}>
            <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
            <p className="text-muted-foreground">
              Monitor your content pipeline and platform performance
            </p>
          </motion.div>

          {/* Metric Cards with Layout Animations */}
          <motion.div 
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
            variants={staggerContainerVariants}
          >
            {metrics.map((metric) => (
              <motion.div
                key={metric.id}
                layout
                layoutId={`metric-${metric.id}`}
                onClick={() => setSelectedCard(metric.id)}
                variants={fadeInUpVariants}
                whileHover="hover"
                whileTap={{ scale: 0.98 }}
                className="cursor-pointer"
              >
                <Card className="h-full transition-shadow hover:shadow-lg">
                  <CardContent className="p-6">
                    <motion.div layout="position" className="flex items-center justify-between">
                      <metric.icon className="h-8 w-8 text-primary" />
                      <PulsingIndicator 
                        status={metric.trend === 'up' ? 'active' : metric.trend === 'down' ? 'pending' : 'inactive'}
                        size="sm"
                      />
                    </motion.div>
                    <motion.h3 layout="position" className="text-sm font-medium text-muted-foreground mt-4">
                      {metric.label}
                    </motion.h3>
                    <motion.p layout="position" className="text-2xl font-bold mt-2">
                      {metric.value}
                    </motion.p>
                    <motion.div layout="position" className="flex items-center mt-2">
                      <TrendingUp className={`h-4 w-4 mr-1 ${
                        metric.trend === 'up' ? 'text-green-500' : 
                        metric.trend === 'down' ? 'text-red-500' : 'text-gray-500'
                      }`} />
                      <span className={`text-sm ${
                        metric.trend === 'up' ? 'text-green-600' : 
                        metric.trend === 'down' ? 'text-red-600' : 'text-gray-600'
                      }`}>
                        {metric.change > 0 ? '+' : ''}{metric.change}%
                      </span>
                    </motion.div>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </motion.div>

          {/* Enhanced Pipeline Visualization */}
          <motion.div variants={fadeInUpVariants}>
            <Card>
              <CardHeader>
                <CardTitle>Active Pipelines</CardTitle>
                <CardDescription>
                  Real-time view of your content generation pipelines
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="relative h-[400px] bg-muted/30 rounded-xl overflow-hidden">
                  <svg className="absolute inset-0 w-full h-full">
                    {/* Connection paths between pipelines */}
                    <motion.path
                      d="M100,100 Q200,50 300,130"
                      stroke="hsl(var(--primary))"
                      strokeWidth="2"
                      fill="none"
                      strokeDasharray="5,5"
                      initial={{ pathLength: 0, opacity: 0 }}
                      animate={{ pathLength: 1, opacity: 0.6 }}
                      transition={{ duration: 2, ease: "easeInOut" }}
                    />
                  </svg>

                  {/* Pipeline Nodes */}
                  {pipelines.map((pipeline) => (
                    <DraggablePipelineCard key={pipeline.id} pipeline={pipeline} />
                  ))}
                  
                  {/* Data Flow Particles */}
                  <DataFlowParticles />
                </div>
              </CardContent>
            </Card>
          </motion.div>

          {/* Recent Activity */}
          <motion.div variants={fadeInUpVariants}>
            <Card>
              <CardHeader>
                <CardTitle>Recent Activity</CardTitle>
              </CardHeader>
              <CardContent>
                <motion.div 
                  className="space-y-4"
                  variants={staggerContainerVariants}
                  initial="hidden"
                  animate="visible"
                >
                  {[1, 2, 3, 4].map((item) => (
                    <motion.div
                      key={item}
                      variants={fadeInUpVariants}
                      className="flex items-center space-x-4 p-3 rounded-lg hover:bg-muted/50 transition-colors"
                    >
                      <div className="w-2 h-2 bg-primary rounded-full" />
                      <div className="flex-1">
                        <p className="text-sm">Article "AI in Marketing" published successfully</p>
                        <p className="text-xs text-muted-foreground">2 minutes ago</p>
                      </div>
                    </motion.div>
                  ))}
                </motion.div>
              </CardContent>
            </Card>
          </motion.div>
        </motion.div>

        {/* Expanded Card Modal */}
        <AnimatePresence>
          {selectedCard && selectedMetric && (
            <>
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="fixed inset-0 bg-black/50 z-40"
                onClick={() => setSelectedCard(null)}
              />
              <motion.div
                layoutId={`metric-${selectedCard}`}
                className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-background border rounded-2xl p-8 z-50 w-[500px] max-h-[80vh] overflow-auto"
              >
                <motion.button
                  className="absolute top-4 right-4 text-muted-foreground hover:text-foreground"
                  onClick={() => setSelectedCard(null)}
                  whileHover={{ rotate: 90, scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                >
                  <X className="w-6 h-6" />
                </motion.button>
                
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.2 }}
                  className="space-y-6"
                >
                  <div className="flex items-center gap-4">
                    <selectedMetric.icon className="w-12 h-12 text-primary" />
                    <div>
                      <h2 className="text-2xl font-bold">{selectedMetric.label}</h2>
                      <p className="text-3xl font-bold text-primary">{selectedMetric.value}</p>
                    </div>
                  </div>
                  
                  <div className="space-y-4">
                    <h3 className="text-lg font-semibold">Detailed Insights</h3>
                    {selectedMetric.details.map((detail, index) => (
                      <motion.div
                        key={index}
                        initial={{ x: -20, opacity: 0 }}
                        animate={{ x: 0, opacity: 1 }}
                        transition={{ delay: 0.3 + index * 0.1 }}
                        className="p-3 bg-muted rounded-lg"
                      >
                        <p className="text-sm">{detail}</p>
                      </motion.div>
                    ))}
                  </div>
                  
                  <AnimatedProgress 
                    value={Math.abs(selectedMetric.change) * 10} 
                    showLabel 
                    variant="gradient"
                  />
                </motion.div>
              </motion.div>
            </>
          )}
        </AnimatePresence>
      </LayoutGroup>
    </>
  )
}

function DraggablePipelineCard({ pipeline }: { pipeline: Pipeline }) {
  const [isDragging, setIsDragging] = useState(false)
  
  return (
    <motion.div
      drag
      dragConstraints={{ left: 20, right: 320, top: 20, bottom: 320 }}
      dragElastic={0.1}
      dragTransition={{ bounceStiffness: 600, bounceDamping: 20 }}
      whileDrag={{ 
        scale: 1.1,
        zIndex: 10,
        filter: "drop-shadow(0 20px 25px rgba(0,0,0,0.15))",
        cursor: "grabbing"
      }}
      onDragStart={() => setIsDragging(true)}
      onDragEnd={() => setIsDragging(false)}
      className="absolute bg-background border rounded-lg p-4 w-48 cursor-move shadow-md"
      style={{ 
        left: pipeline.x, 
        top: pipeline.y,
        willChange: isDragging ? 'transform' : 'auto'
      }}
      layout
      transition={{
        layout: { type: "spring", stiffness: 350, damping: 25 }
      }}
    >
      <div className="flex items-center justify-between mb-2">
        <h4 className="font-semibold text-sm">{pipeline.name}</h4>
        <PulsingIndicator 
          status={pipeline.status === 'completed' ? 'inactive' : pipeline.status} 
          size="sm" 
        />
      </div>
      
      <p className="text-xs text-muted-foreground mb-3">
        Status: {pipeline.status}
      </p>
      
      <AnimatedProgress 
        value={pipeline.progress}
        className="mb-2"
      />
      
      <p className="text-xs text-muted-foreground">
        {pipeline.progress}% complete
      </p>
    </motion.div>
  )
}

function DataFlowParticles() {
  return (
    <>
      {[...Array(3)].map((_, i) => (
        <motion.div
          key={i}
          className="absolute w-2 h-2 bg-primary rounded-full opacity-60"
          initial={{ x: 100, y: 100 }}
          animate={{
            x: [100, 150, 200, 250, 300],
            y: [100, 80, 90, 110, 130],
          }}
          transition={{
            duration: 4,
            delay: i * 1.5,
            repeat: Infinity,
            ease: "linear"
          }}
        />
      ))}
    </>
  )
}
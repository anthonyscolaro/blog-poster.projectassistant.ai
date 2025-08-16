import React, { useState } from 'react'
import { Reorder, useDragControls, motion } from 'framer-motion'
import { GripVertical, Play, Pause, Settings, CheckCircle, Clock, AlertTriangle } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { PulsingIndicator, AnimatedProgress } from '@/components/ui/AnimatedComponents'

interface Agent {
  id: string
  name: string
  status: 'active' | 'pending' | 'completed' | 'error'
  description: string
  icon: string
  estimatedTime: string
  progress?: number
}

const initialAgents: Agent[] = [
  { 
    id: '1', 
    name: 'Competitor Monitor', 
    status: 'completed',
    description: 'Analyze competitor content and identify opportunities',
    icon: '🔍',
    estimatedTime: '2-3 min',
    progress: 100
  },
  { 
    id: '2', 
    name: 'Topic Analyzer', 
    status: 'active',
    description: 'Research trending topics and keywords',
    icon: '📊',
    estimatedTime: '3-5 min',
    progress: 65
  },
  { 
    id: '3', 
    name: 'Article Generator', 
    status: 'pending',
    description: 'Generate high-quality, SEO-optimized content',
    icon: '✍️',
    estimatedTime: '5-8 min'
  },
  { 
    id: '4', 
    name: 'Legal Checker', 
    status: 'pending',
    description: 'Verify compliance and fact-check content',
    icon: '⚖️',
    estimatedTime: '2-4 min'
  },
  { 
    id: '5', 
    name: 'WordPress Publisher', 
    status: 'pending',
    description: 'Format and publish to WordPress sites',
    icon: '🚀',
    estimatedTime: '1-2 min'
  }
]

export function ReorderableAgentPipeline() {
  const [agents, setAgents] = useState(initialAgents)
  const [isRunning, setIsRunning] = useState(false)

  const handleStartPipeline = () => {
    setIsRunning(true)
    // Simulate pipeline execution
    setTimeout(() => setIsRunning(false), 10000)
  }

  const getStatusIcon = (status: Agent['status']) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="w-4 h-4 text-green-500" />
      case 'active':
        return <Play className="w-4 h-4 text-blue-500" />
      case 'error':
        return <AlertTriangle className="w-4 h-4 text-red-500" />
      default:
        return <Clock className="w-4 h-4 text-gray-400" />
    }
  }

  const getStatusBadge = (status: Agent['status']) => {
    const variants = {
      completed: 'default',
      active: 'default',
      pending: 'secondary',
      error: 'destructive'
    } as const

    return (
      <Badge variant={variants[status]} className="text-xs">
        {status.charAt(0).toUpperCase() + status.slice(1)}
      </Badge>
    )
  }

  return (
    <Card className="w-full max-w-4xl mx-auto">
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="flex items-center gap-2">
              <span>Agent Pipeline</span>
              <PulsingIndicator 
                status={isRunning ? 'active' : 'inactive'} 
                size="sm" 
              />
            </CardTitle>
            <p className="text-sm text-muted-foreground">
              Drag to reorder agents in your content generation pipeline
            </p>
          </div>
          <Button 
            onClick={handleStartPipeline}
            disabled={isRunning}
            className="min-w-[120px]"
          >
            {isRunning ? (
              <motion.div
                className="flex items-center gap-2"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
              >
                <motion.div
                  className="w-4 h-4 border-2 border-current border-t-transparent rounded-full"
                  animate={{ rotate: 360 }}
                  transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                />
                Running...
              </motion.div>
            ) : (
              <div className="flex items-center gap-2">
                <Play className="w-4 h-4" />
                Start Pipeline
              </div>
            )}
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <Reorder.Group 
          axis="y" 
          values={agents} 
          onReorder={setAgents}
          className="space-y-3"
        >
          {agents.map((agent, index) => (
            <AgentItem 
              key={agent.id} 
              agent={agent} 
              index={index}
              total={agents.length}
              isRunning={isRunning}
            />
          ))}
        </Reorder.Group>
        
        {/* Pipeline Flow Visualization */}
        <motion.div 
          className="mt-6 p-4 bg-muted/30 rounded-lg"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
        >
          <h4 className="font-medium mb-3">Pipeline Flow</h4>
          <div className="flex items-center justify-between">
            {agents.map((agent, index) => (
              <React.Fragment key={agent.id}>
                <motion.div
                  className="flex flex-col items-center"
                  whileHover={{ scale: 1.05 }}
                >
                  <motion.div
                    className={`
                      w-10 h-10 rounded-full flex items-center justify-center text-lg
                      ${agent.status === 'completed' ? 'bg-green-100' : 
                        agent.status === 'active' ? 'bg-blue-100' : 
                        agent.status === 'error' ? 'bg-red-100' : 'bg-gray-100'}
                    `}
                    whileHover={{ rotateY: 180 }}
                    transition={{ duration: 0.4 }}
                  >
                    {agent.icon}
                  </motion.div>
                  <span className="text-xs mt-1 text-center max-w-[60px] truncate">
                    {agent.name.split(' ')[0]}
                  </span>
                </motion.div>
                
                {index < agents.length - 1 && (
                  <motion.div
                    className="flex-1 h-0.5 bg-gray-300 mx-2"
                    initial={{ scaleX: 0 }}
                    animate={{ scaleX: agent.status === 'completed' ? 1 : 0.3 }}
                    transition={{ duration: 0.8, delay: index * 0.2 }}
                    style={{ originX: 0 }}
                  />
                )}
              </React.Fragment>
            ))}
          </div>
        </motion.div>
      </CardContent>
    </Card>
  )
}

function AgentItem({ 
  agent, 
  index, 
  total, 
  isRunning 
}: { 
  agent: Agent
  index: number
  total: number
  isRunning: boolean
}) {
  const controls = useDragControls()
  const [isDragging, setIsDragging] = useState(false)

  const getStatusIcon = (status: Agent['status']) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="w-4 h-4 text-green-500" />
      case 'active':
        return <Play className="w-4 h-4 text-blue-500" />
      case 'error':
        return <AlertTriangle className="w-4 h-4 text-red-500" />
      default:
        return <Clock className="w-4 h-4 text-gray-400" />
    }
  }

  const getStatusBadge = (status: Agent['status']) => {
    const variants = {
      completed: 'default',
      active: 'default', 
      pending: 'secondary',
      error: 'destructive'
    } as const

    return (
      <Badge variant={variants[status]} className="text-xs">
        {status.charAt(0).toUpperCase() + status.slice(1)}
      </Badge>
    )
  }

  return (
    <Reorder.Item
      value={agent}
      id={agent.id}
      dragListener={false}
      dragControls={controls}
      onDragStart={() => setIsDragging(true)}
      onDragEnd={() => setIsDragging(false)}
      className={`
        bg-background border rounded-lg p-4 transition-all duration-200
        ${isDragging ? 'shadow-2xl z-10 rotate-2' : 'shadow-sm hover:shadow-md'}
      `}
      whileDrag={{
        scale: 1.02,
        filter: "drop-shadow(0 20px 25px rgba(0,0,0,0.15))",
        cursor: "grabbing"
      }}
      layout
      transition={{
        layout: { type: "spring", stiffness: 350, damping: 25 }
      }}
    >
      <div className="flex items-center gap-4">
        {/* Drag Handle */}
        <motion.div
          className="cursor-grab active:cursor-grabbing text-gray-400 hover:text-gray-600"
          onPointerDown={(e) => controls.start(e)}
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.95 }}
        >
          <GripVertical className="w-5 h-5" />
        </motion.div>
        
        {/* Agent Icon */}
        <motion.div
          className="text-2xl"
          whileHover={{ scale: 1.2, rotate: 10 }}
          transition={{ type: "spring", stiffness: 300 }}
        >
          {agent.icon}
        </motion.div>
        
        {/* Agent Info */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <h4 className="font-medium truncate">{agent.name}</h4>
            {getStatusBadge(agent.status)}
          </div>
          <p className="text-sm text-muted-foreground truncate mb-2">
            {agent.description}
          </p>
          
          {/* Progress Bar (if active) */}
          {agent.status === 'active' && agent.progress !== undefined && (
            <motion.div
              className="w-full bg-gray-200 rounded-full h-1.5 mb-2"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
            >
              <motion.div
                className="bg-blue-500 h-1.5 rounded-full"
                initial={{ width: 0 }}
                animate={{ width: `${agent.progress}%` }}
                transition={{ duration: 0.5 }}
              />
            </motion.div>
          )}
          
          <div className="flex items-center justify-between text-xs text-muted-foreground">
            <span>Est. time: {agent.estimatedTime}</span>
            <span>Position: {index + 1}/{total}</span>
          </div>
        </div>
        
        {/* Status Icon */}
        <div className="flex items-center gap-2">
          {getStatusIcon(agent.status)}
          <Button variant="ghost" size="sm" className="h-8 w-8 p-0">
            <Settings className="w-4 h-4" />
          </Button>
        </div>
      </div>
    </Reorder.Item>
  )
}
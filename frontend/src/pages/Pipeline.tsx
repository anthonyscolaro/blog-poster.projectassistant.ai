import { useState, useEffect } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { motion } from 'framer-motion'
import { supabase } from '@/services/supabase'
import { useAuth } from '@/contexts/AuthContext'
import apiService from '@/services/api'
import { PipelineConfiguration } from '@/components/pipeline/PipelineConfiguration'
import { ExecutionMonitor } from '@/components/pipeline/ExecutionMonitor'
import { PipelineStatus } from '@/components/dashboard/PipelineStatus'
import { PipelineHistory } from '@/components/pipeline/PipelineHistory'
import { CostTracker } from '@/components/pipeline/CostTracker'
import { Button } from '@/components/ui/button'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { toast } from 'react-hot-toast'
import { Play, Square, Settings, History, DollarSign } from 'lucide-react'

export default function Pipeline() {
  const { user, organization } = useAuth()
  const [currentExecution, setCurrentExecution] = useState<any>(null)
  const [backendStatus, setBackendStatus] = useState<'checking' | 'online' | 'offline' | 'mock'>('checking')
  const queryClient = useQueryClient()

  // Check backend status
  useEffect(() => {
    const checkBackend = async () => {
      const health = await apiService.getHealth()
      setBackendStatus(health.status as any)
    }
    
    checkBackend()
    const interval = setInterval(checkBackend, 30000) // Check every 30 seconds
    
    return () => clearInterval(interval)
  }, [])

  // Set up Supabase real-time subscription
  useEffect(() => {
    if (!organization?.id) return

    const channel = supabase
      .channel(`pipelines:${organization.id}`)
      .on(
        'postgres_changes',
        {
          event: '*',
          schema: 'public',
          table: 'pipelines',
          filter: `organization_id=eq.${organization.id}`
        },
        (payload) => {
          if (payload.eventType === 'UPDATE' || payload.eventType === 'INSERT') {
            const pipeline = payload.new
            
            if (pipeline.status === 'running' || pipeline.status === 'queued') {
              setCurrentExecution(pipeline)
            }
            
            // Show notifications
            if (payload.eventType === 'UPDATE' && payload.old.status !== pipeline.status) {
              if (pipeline.status === 'completed') {
                toast.success('Pipeline completed successfully!')
              } else if (pipeline.status === 'failed') {
                toast.error(`Pipeline failed: ${pipeline.error_message}`)
              }
            }
            
            queryClient.invalidateQueries({ queryKey: ['pipelines'] })
          }
        }
      )
      .subscribe()

    return () => {
      supabase.removeChannel(channel)
    }
  }, [organization?.id, queryClient])

  // Query current/recent pipeline
  const { data: activePipeline, isLoading } = useQuery({
    queryKey: ['pipelines', 'active', organization?.id],
    queryFn: async () => {
      const { data, error } = await supabase
        .from('pipelines')
        .select('*')
        .eq('organization_id', organization!.id)
        .in('status', ['running', 'queued', 'pending'])
        .order('created_at', { ascending: false })
        .limit(1)
        .maybeSingle()
      
      if (error) throw error
      return data
    },
    enabled: !!organization?.id,
    refetchInterval: currentExecution?.status === 'running' ? 5000 : false,
  })

  // Start pipeline mutation
  const startPipelineMutation = useMutation({
    mutationFn: async (config: any) => {
      const { data, error } = await supabase
        .from('pipelines')
        .insert({
          organization_id: organization!.id,
          user_id: user!.id,
          name: `Pipeline: ${config.topic}`,
          description: `Generate article about "${config.topic}"`,
          status: 'pending',
          config: config,
          estimated_cost: estimateCost(config),
          priority: 5
        })
        .select()
        .single()
      
      if (error) throw error

      // Pipeline created in database - backend will pick it up via webhook
      if (data) {
        console.log('Pipeline created in database:', data.id)
        toast('Pipeline created successfully!', { icon: '🚀' })
      }

      return data
    },
    onSuccess: (data) => {
      setCurrentExecution(data)
      toast.success('Pipeline started successfully!')
    },
    onError: (error: any) => {
      toast.error(`Failed to start pipeline: ${error.message}`)
    }
  })

  // Stop pipeline mutation
  const stopPipelineMutation = useMutation({
    mutationFn: async (pipelineId: string) => {
      const { data, error } = await supabase
        .from('pipelines')
        .update({
          status: 'cancelled',
          cancelled_by: user!.id,
          cancellation_reason: 'User requested cancellation',
          completed_at: new Date().toISOString()
        })
        .eq('id', pipelineId)
        .select()
        .single()
      
      if (error) throw error
      return data
    },
    onSuccess: () => {
      toast.success('Pipeline stopped')
      setCurrentExecution(null)
    }
  })

  const estimateCost = (config: any): number => {
    const baseCosts = {
      competitor_monitoring: 0.05,
      topic_analysis: 0.03,
      article_generation: 0.15,
      legal_fact_checker: 0.08,
      wordpress_publishing: 0.02,
    }
    
    const wordCountMultiplier = (config.wordCountMax || 2000) / 1500
    let totalCost = Object.values(baseCosts).reduce((sum: number, cost: number) => sum + cost, 0)
    totalCost *= wordCountMultiplier
    
    return Math.round(totalCost * 100) / 100
  }

  const execution = currentExecution || activePipeline
  const isRunning = execution?.status === 'running' || execution?.status === 'queued'

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="container mx-auto px-4 py-8"
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold">Content Pipeline</h1>
          <p className="text-muted-foreground mt-1">
            Orchestrate 5 AI agents to generate SEO-optimized articles
          </p>
          {/* Backend Status Indicator */}
          <div className="flex items-center gap-2 text-sm mt-2">
            <div className={`h-2 w-2 rounded-full ${
              backendStatus === 'online' ? 'bg-green-500' : 
              backendStatus === 'offline' ? 'bg-red-500' : 
              backendStatus === 'mock' ? 'bg-yellow-500' :
              'bg-gray-500'
            }`} />
            <span className="text-muted-foreground">
              Backend: {
                backendStatus === 'online' ? 'Connected' : 
                backendStatus === 'offline' ? 'Offline (Mock Mode)' : 
                backendStatus === 'mock' ? 'Mock Mode' :
                'Checking...'
              }
            </span>
          </div>
        </div>

        {/* Pipeline Controls */}
        <div className="flex items-center gap-2">
          {isRunning ? (
            <Button
              variant="destructive"
              onClick={() => execution && stopPipelineMutation.mutate(execution.id)}
              disabled={stopPipelineMutation.isPending}
            >
              <Square className="h-4 w-4 mr-2" />
              Stop Pipeline
            </Button>
          ) : (
            <Button
              onClick={() => {
                // Focus on configuration tab
                const configTab = document.querySelector('[value="config"]') as HTMLElement
                configTab?.click()
              }}
            >
              <Play className="h-4 w-4 mr-2" />
              Start Pipeline
            </Button>
          )}
        </div>
      </div>

      {/* Main Content */}
      <Tabs defaultValue="monitor" className="space-y-6">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="monitor">
            <Play className="h-4 w-4 mr-2" />
            Monitor
          </TabsTrigger>
          <TabsTrigger value="config">
            <Settings className="h-4 w-4 mr-2" />
            Configuration
          </TabsTrigger>
          <TabsTrigger value="history">
            <History className="h-4 w-4 mr-2" />
            History
          </TabsTrigger>
          <TabsTrigger value="costs">
            <DollarSign className="h-4 w-4 mr-2" />
            Costs
          </TabsTrigger>
        </TabsList>

        <TabsContent value="monitor" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2">
              <ExecutionMonitor execution={execution} isLoading={isLoading} />
            </div>
            <div>
              <PipelineStatus />
            </div>
          </div>
        </TabsContent>

        <TabsContent value="config">
          <PipelineConfiguration
            onStart={(config) => startPipelineMutation.mutate(config)}
            isStarting={startPipelineMutation.isPending}
            disabled={isRunning}
            organizationId={organization?.id}
          />
        </TabsContent>

        <TabsContent value="history">
          <PipelineHistory organizationId={organization?.id} />
        </TabsContent>

        <TabsContent value="costs">
          <CostTracker organizationId={organization?.id} />
        </TabsContent>
      </Tabs>
    </motion.div>
  )
}
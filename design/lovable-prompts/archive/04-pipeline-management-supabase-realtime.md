# Lovable Prompt: Pipeline Management System (Supabase-Integrated)

## Business Context:
The pipeline management system is the orchestration center for Blog-Poster's 5-agent content generation workflow. It provides real-time monitoring, configuration, and control over the automated content creation process using Supabase's real-time capabilities, ensuring quality SEO content while managing costs and tracking performance.

## User Story:
"As a content manager, I want to initiate, monitor, and manage the 5-agent content generation pipeline in real-time, with the ability to configure agents, track costs, view execution logs, and intervene when necessary to ensure quality output."

## Pipeline Requirements:
- **5-Agent Orchestration**: Sequential execution of Competitor Monitoring → Topic Analysis → Article Generation → Legal Fact Checker → WordPress Publishing
- **Supabase Real-time Updates**: Live progress tracking using Supabase subscriptions
- **Cost Monitoring**: Per-execution cost tracking with budget controls via RPC functions
- **Agent Configuration**: Individual agent parameters and settings
- **Execution History**: Searchable log of past pipeline runs with RLS

## Prompt for Lovable:

Create a comprehensive pipeline management system for the Blog-Poster platform that orchestrates 5 AI agents in sequence to generate legally-compliant, SEO-optimized articles. The system uses Supabase for real-time updates, data persistence, and Row Level Security.

**First, create the Supabase database schema:**

### Database Migration Script
```sql
-- Create pipeline executions table
CREATE TABLE IF NOT EXISTS pipeline_executions (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  organization_id UUID REFERENCES organizations(id) NOT NULL,
  status TEXT CHECK (status IN ('pending', 'running', 'completed', 'failed', 'cancelled')) DEFAULT 'pending',
  current_agent TEXT,
  agents_completed TEXT[] DEFAULT '{}',
  started_at TIMESTAMPTZ DEFAULT NOW(),
  completed_at TIMESTAMPTZ,
  total_cost DECIMAL(10,2) DEFAULT 0,
  estimated_cost DECIMAL(10,2) DEFAULT 0,
  configuration JSONB,
  article_id UUID REFERENCES articles(id),
  error_message TEXT,
  created_by UUID REFERENCES auth.users(id),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create pipeline logs table
CREATE TABLE IF NOT EXISTS pipeline_logs (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  execution_id UUID REFERENCES pipeline_executions(id) ON DELETE CASCADE,
  agent_name TEXT NOT NULL,
  level TEXT CHECK (level IN ('info', 'warning', 'error', 'debug')) DEFAULT 'info',
  message TEXT NOT NULL,
  metadata JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create pipeline configurations table
CREATE TABLE IF NOT EXISTS pipeline_configs (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  organization_id UUID REFERENCES organizations(id) NOT NULL,
  name TEXT NOT NULL,
  description TEXT,
  configuration JSONB NOT NULL,
  is_default BOOLEAN DEFAULT false,
  created_by UUID REFERENCES auth.users(id),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE pipeline_executions ENABLE ROW LEVEL SECURITY;
ALTER TABLE pipeline_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE pipeline_configs ENABLE ROW LEVEL SECURITY;

-- RLS Policies for pipeline_executions
CREATE POLICY "Users can view organization pipeline executions" ON pipeline_executions
  FOR SELECT USING (
    organization_id IN (
      SELECT organization_id FROM profiles 
      WHERE profiles.id = auth.uid()
    )
  );

CREATE POLICY "Users can create pipeline executions" ON pipeline_executions
  FOR INSERT WITH CHECK (
    organization_id IN (
      SELECT organization_id FROM profiles 
      WHERE profiles.id = auth.uid()
    )
  );

CREATE POLICY "Users can update organization pipeline executions" ON pipeline_executions
  FOR UPDATE USING (
    organization_id IN (
      SELECT organization_id FROM profiles 
      WHERE profiles.id = auth.uid()
    )
  );

-- RLS Policies for pipeline_logs (inherit from execution)
CREATE POLICY "Users can view logs for organization pipelines" ON pipeline_logs
  FOR SELECT USING (
    execution_id IN (
      SELECT id FROM pipeline_executions 
      WHERE organization_id IN (
        SELECT organization_id FROM profiles 
        WHERE profiles.id = auth.uid()
      )
    )
  );

-- RLS Policies for pipeline_configs
CREATE POLICY "Users can view organization pipeline configs" ON pipeline_configs
  FOR ALL USING (
    organization_id IN (
      SELECT organization_id FROM profiles 
      WHERE profiles.id = auth.uid()
    )
  );

-- Create indexes for performance
CREATE INDEX idx_pipeline_executions_org_id ON pipeline_executions(organization_id);
CREATE INDEX idx_pipeline_executions_status ON pipeline_executions(status);
CREATE INDEX idx_pipeline_executions_created_at ON pipeline_executions(created_at DESC);
CREATE INDEX idx_pipeline_logs_execution_id ON pipeline_logs(execution_id);
CREATE INDEX idx_pipeline_configs_org_id ON pipeline_configs(organization_id);

-- Function to update pipeline execution status
CREATE OR REPLACE FUNCTION update_pipeline_status(
  p_execution_id UUID,
  p_status TEXT,
  p_current_agent TEXT DEFAULT NULL,
  p_error_message TEXT DEFAULT NULL
)
RETURNS pipeline_executions AS $$
DECLARE
  v_execution pipeline_executions;
BEGIN
  UPDATE pipeline_executions
  SET 
    status = p_status,
    current_agent = COALESCE(p_current_agent, current_agent),
    error_message = p_error_message,
    completed_at = CASE WHEN p_status IN ('completed', 'failed', 'cancelled') THEN NOW() ELSE NULL END,
    updated_at = NOW()
  WHERE id = p_execution_id
  RETURNING * INTO v_execution;
  
  RETURN v_execution;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to add agent to completed list
CREATE OR REPLACE FUNCTION complete_pipeline_agent(
  p_execution_id UUID,
  p_agent_name TEXT,
  p_cost DECIMAL DEFAULT 0
)
RETURNS pipeline_executions AS $$
DECLARE
  v_execution pipeline_executions;
BEGIN
  UPDATE pipeline_executions
  SET 
    agents_completed = array_append(agents_completed, p_agent_name),
    total_cost = total_cost + p_cost,
    updated_at = NOW()
  WHERE id = p_execution_id
  RETURNING * INTO v_execution;
  
  RETURN v_execution;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

**Now create the Supabase service for the frontend:**

### Supabase Service
```typescript
// src/services/supabase.ts
import { createClient } from '@supabase/supabase-js'
import type { Database } from '@/types/database'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY

if (!supabaseUrl || !supabaseAnonKey) {
  throw new Error('Missing Supabase environment variables')
}

export const supabase = createClient<Database>(supabaseUrl, supabaseAnonKey, {
  auth: {
    persistSession: true,
    autoRefreshToken: true,
  },
  realtime: {
    params: {
      eventsPerSecond: 10
    }
  }
})

// Type definitions for pipeline tables
export interface PipelineExecution {
  id: string
  organization_id: string
  status: 'pending' | 'running' | 'completed' | 'failed' | 'cancelled'
  current_agent: string | null
  agents_completed: string[]
  started_at: string
  completed_at: string | null
  total_cost: number
  estimated_cost: number
  configuration: PipelineConfig
  article_id: string | null
  error_message: string | null
  created_by: string
  created_at: string
  updated_at: string
}

export interface PipelineConfig {
  topic: string
  targetKeywords: string[]
  competitorUrls: string[]
  wordCountMin: number
  wordCountMax: number
  seoOptimization: boolean
  legalReview: boolean
  autoPublish: boolean
  wordpressSiteId: string | null
  budgetLimit: number
}

export interface PipelineLog {
  id: string
  execution_id: string
  agent_name: string
  level: 'info' | 'warning' | 'error' | 'debug'
  message: string
  metadata: Record<string, any>
  created_at: string
}
```

**Main Pipeline Page with Supabase Real-time:**

### Pipeline Management Page
```typescript
// src/pages/Pipeline.tsx
import { useState, useEffect } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { motion, AnimatePresence } from 'framer-motion'
import { supabase, type PipelineExecution, type PipelineConfig } from '@/services/supabase'
import { PipelineConfiguration } from '@/components/pipeline/PipelineConfiguration'
import { ExecutionMonitor } from '@/components/pipeline/ExecutionMonitor'
import { PipelineHistory } from '@/components/pipeline/PipelineHistory'
import { AgentStatus } from '@/components/pipeline/AgentStatus'
import { CostTracker } from '@/components/pipeline/CostTracker'
import { ExecutionLogs } from '@/components/pipeline/ExecutionLogs'
import { PageTransition, FadeInSection, PulseEffect } from '@/components/ui/AnimatedComponents'
import { Play, Square, Settings, History, DollarSign } from 'lucide-react'
import { useAuth } from '@/hooks/useAuth'
import toast from 'react-hot-toast'

export default function Pipeline() {
  const [activeTab, setActiveTab] = useState<'monitor' | 'config' | 'history' | 'logs'>('monitor')
  const [currentExecution, setCurrentExecution] = useState<PipelineExecution | null>(null)
  const [isConnected, setIsConnected] = useState(false)
  const queryClient = useQueryClient()
  const { user, organization } = useAuth()

  // Set up Supabase real-time subscription
  useEffect(() => {
    if (!organization?.id) return

    // Subscribe to pipeline executions for this organization
    const channel = supabase
      .channel(`pipeline:${organization.id}`)
      .on(
        'postgres_changes',
        {
          event: '*',
          schema: 'public',
          table: 'pipeline_executions',
          filter: `organization_id=eq.${organization.id}`
        },
        (payload) => {
          // Handle real-time updates
          if (payload.eventType === 'UPDATE' || payload.eventType === 'INSERT') {
            const execution = payload.new as PipelineExecution
            
            // Update current execution if it matches
            if (execution.status === 'running' || 
                (currentExecution?.id === execution.id)) {
              setCurrentExecution(execution)
              
              // Show toast notifications for status changes
              if (payload.eventType === 'UPDATE') {
                const oldStatus = (payload.old as PipelineExecution).status
                if (oldStatus !== execution.status) {
                  if (execution.status === 'completed') {
                    toast.success('Pipeline completed successfully!')
                  } else if (execution.status === 'failed') {
                    toast.error(`Pipeline failed: ${execution.error_message}`)
                  }
                }
              }
            }
            
            // Invalidate queries to refresh data
            queryClient.invalidateQueries({ queryKey: ['pipeline-executions'] })
          }
        }
      )
      .on(
        'postgres_changes',
        {
          event: 'INSERT',
          schema: 'public',
          table: 'pipeline_logs',
        },
        (payload) => {
          // Handle new log entries
          const log = payload.new
          queryClient.invalidateQueries({ queryKey: ['pipeline-logs', log.execution_id] })
          
          // Show important log messages as toasts
          if (log.level === 'error') {
            toast.error(`${log.agent_name}: ${log.message}`)
          } else if (log.level === 'warning') {
            toast(`${log.agent_name}: ${log.message}`, { icon: '⚠️' })
          }
        }
      )
      .subscribe((status) => {
        setIsConnected(status === 'SUBSCRIBED')
      })

    return () => {
      supabase.removeChannel(channel)
    }
  }, [organization?.id, currentExecution?.id, queryClient])

  // Query current/recent execution
  const { data: execution, isLoading } = useQuery({
    queryKey: ['pipeline-execution', 'current', organization?.id],
    queryFn: async () => {
      const { data, error } = await supabase
        .from('pipeline_executions')
        .select('*')
        .eq('organization_id', organization!.id)
        .in('status', ['running', 'pending'])
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
    mutationFn: async (config: PipelineConfig) => {
      // First check budget limit
      const { data: canProceed } = await supabase
        .rpc('check_budget_limit', { p_organization_id: organization!.id })
      
      if (!canProceed) {
        throw new Error('Monthly budget limit reached. Please increase your budget to continue.')
      }
      
      // Create new pipeline execution
      const { data, error } = await supabase
        .from('pipeline_executions')
        .insert({
          organization_id: organization!.id,
          status: 'pending',
          configuration: config,
          estimated_cost: estimateCost(config),
          created_by: user!.id,
        })
        .select()
        .single()
      
      if (error) throw error
      
      // Trigger backend to start processing
      // The backend will update status to 'running' and manage the workflow
      await triggerBackendPipeline(data.id)
      
      return data
    },
    onSuccess: (data) => {
      setCurrentExecution(data)
      toast.success('Pipeline started successfully!')
      setActiveTab('monitor')
    },
    onError: (error: any) => {
      toast.error(`Failed to start pipeline: ${error.message}`)
    }
  })

  // Stop pipeline mutation
  const stopPipelineMutation = useMutation({
    mutationFn: async (executionId: string) => {
      const { data, error } = await supabase
        .rpc('update_pipeline_status', {
          p_execution_id: executionId,
          p_status: 'cancelled',
          p_error_message: 'Cancelled by user'
        })
      
      if (error) throw error
      return data
    },
    onSuccess: () => {
      toast.success('Pipeline stopped')
      setCurrentExecution(null)
    }
  })

  // Helper function to estimate cost
  const estimateCost = (config: PipelineConfig): number => {
    // Base costs per agent (in dollars)
    const agentCosts = {
      competitor_monitoring: 0.05,
      topic_analysis: 0.03,
      article_generation: 0.15, // Claude 3.5 Sonnet
      legal_fact_checker: 0.08,
      wordpress_publishing: 0.02,
    }
    
    // Adjust for word count
    const wordCountMultiplier = config.wordCountMax / 1500
    
    let totalCost = Object.values(agentCosts).reduce((sum, cost) => sum + cost, 0)
    totalCost *= wordCountMultiplier
    
    return Math.round(totalCost * 100) / 100
  }

  // Trigger backend pipeline via API
  const triggerBackendPipeline = async (executionId: string) => {
    // This calls our FastAPI backend which will orchestrate the agents
    const response = await fetch(`${import.meta.env.VITE_API_URL}/api/v1/pipeline/execute`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${(await supabase.auth.getSession()).data.session?.access_token}`
      },
      body: JSON.stringify({ execution_id: executionId })
    })
    
    if (!response.ok) {
      throw new Error('Failed to trigger pipeline execution')
    }
  }

  const isRunning = currentExecution?.status === 'running'
  const canStart = !isRunning && isConnected && !!organization

  return (
    <PageTransition>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Animated Header */}
        <FadeInSection className="flex items-center justify-between mb-8">
          <motion.div
            initial={{ x: -20, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ delay: 0.1 }}
          >
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
              Content Pipeline
            </h1>
            <p className="text-gray-600 dark:text-gray-400">
              Orchestrate 5 AI agents to generate SEO-optimized articles
            </p>
          </motion.div>

          {/* Connection Status & Controls */}
          <motion.div 
            className="flex items-center gap-4"
            initial={{ x: 20, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ delay: 0.2 }}
          >
            <div className="flex items-center gap-2">
              <motion.div 
                className={`h-2 w-2 rounded-full ${
                  isConnected ? 'bg-green-500' : 'bg-red-500'
                }`}
                animate={isConnected ? {
                  scale: [1, 1.2, 1],
                  opacity: [1, 0.7, 1]
                } : {
                  scale: 1,
                  opacity: 0.7
                }}
                transition={{
                  duration: 2,
                  repeat: Infinity,
                  ease: "easeInOut"
                }}
              />
              <span className="text-sm text-gray-600 dark:text-gray-400">
                {isConnected ? 'Real-time Connected' : 'Connecting...'}
              </span>
            </div>

            {/* Pipeline Controls */}
            <div className="flex items-center gap-2">
              <AnimatePresence mode="wait">
                {isRunning ? (
                  <motion.button
                    key="stop"
                    onClick={() => currentExecution && stopPipelineMutation.mutate(currentExecution.id)}
                    className="inline-flex items-center px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
                    disabled={stopPipelineMutation.isPending}
                    initial={{ scale: 0, rotate: -180 }}
                    animate={{ scale: 1, rotate: 0 }}
                    exit={{ scale: 0, rotate: 180 }}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                  >
                    <Square className="h-4 w-4 mr-2" />
                    Stop Pipeline
                  </motion.button>
                ) : (
                  <motion.button
                    key="start"
                    onClick={() => setActiveTab('config')}
                    className="inline-flex items-center px-4 py-2 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-lg hover:opacity-90 transition-opacity disabled:opacity-50"
                    disabled={!canStart}
                    initial={{ scale: 0, rotate: 180 }}
                    animate={{ scale: 1, rotate: 0 }}
                    exit={{ scale: 0, rotate: -180 }}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                  >
                    <Play className="h-4 w-4 mr-2" />
                    Start Pipeline
                  </motion.button>
                )}
              </AnimatePresence>
            </div>
          </motion.div>
        </FadeInSection>

        {/* Tab Navigation */}
        <div className="flex space-x-1 mb-6 border-b border-gray-200 dark:border-gray-700">
          {[
            { id: 'monitor', label: 'Monitor', icon: Play },
            { id: 'config', label: 'Configuration', icon: Settings },
            { id: 'history', label: 'History', icon: History },
            { id: 'logs', label: 'Logs', icon: DollarSign },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`flex items-center px-4 py-2 font-medium transition-colors ${
                activeTab === tab.id
                  ? 'text-purple-600 dark:text-purple-400 border-b-2 border-purple-600 dark:border-purple-400'
                  : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200'
              }`}
            >
              <tab.icon className="h-4 w-4 mr-2" />
              {tab.label}
            </button>
          ))}
        </div>

        {/* Tab Content */}
        <AnimatePresence mode="wait">
          <motion.div
            key={activeTab}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.2 }}
            className="space-y-6"
          >
            {activeTab === 'monitor' && (
              <>
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                  {/* Execution Monitor */}
                  <div className="lg:col-span-2">
                    <ExecutionMonitor 
                      execution={currentExecution || execution} 
                      isLoading={isLoading} 
                    />
                  </div>

                  {/* Cost Tracker */}
                  <div>
                    <CostTracker 
                      execution={currentExecution || execution}
                      organizationId={organization?.id}
                    />
                  </div>
                </div>

                {/* Agent Status Grid */}
                <AgentStatus 
                  execution={currentExecution || execution}
                  isConnected={isConnected}
                />
              </>
            )}

            {activeTab === 'config' && (
              <PipelineConfiguration
                onStart={(config) => startPipelineMutation.mutate(config)}
                isStarting={startPipelineMutation.isPending}
                disabled={isRunning}
                organizationId={organization?.id}
              />
            )}

            {activeTab === 'history' && (
              <PipelineHistory organizationId={organization?.id} />
            )}

            {activeTab === 'logs' && (
              <ExecutionLogs 
                executionId={currentExecution?.id || execution?.id}
                isLive={isRunning}
              />
            )}
          </motion.div>
        </AnimatePresence>
      </div>
    </PageTransition>
  )
}
```

**Success Criteria:**
- ✅ Supabase real-time subscriptions for live updates
- ✅ Row Level Security for multi-tenant data isolation
- ✅ Cost tracking with budget validation via RPC functions
- ✅ Proper organization-based filtering
- ✅ Database schema with indexes for performance
- ✅ Integration with existing authentication system
- ✅ Toast notifications for important events
- ✅ Mobile-responsive design with animations
- ✅ Error handling and loading states

This implementation properly integrates with Lovable's expected patterns and Supabase's capabilities, providing a robust pipeline management system.
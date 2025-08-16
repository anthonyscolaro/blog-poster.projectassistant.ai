import { useEffect, useCallback, useState } from 'react'
import { useQueryClient } from '@tanstack/react-query'
import { toast } from 'sonner'
import wsService from '@/services/websocket'

export function usePipelineWebSocket(pipelineId?: string) {
  const queryClient = useQueryClient()
  const [isConnected, setIsConnected] = useState(false)

  useEffect(() => {
    if (!pipelineId) return

    // Connect to pipeline-specific WebSocket
    wsService.connect(pipelineId)

    // Handle connection events
    const handleConnected = () => setIsConnected(true)
    const handleDisconnected = () => setIsConnected(false)

    // Handle pipeline progress
    const handlePipelineProgress = (progress: any) => {
      // Update cache with real-time progress
      queryClient.setQueryData(['pipeline', pipelineId], (oldData: any) => {
        if (oldData) {
          return {
            ...oldData,
            progress_percentage: progress.percentage,
            current_agent: progress.current_agent,
            agents_completed: progress.agents_completed,
            status: progress.status || oldData.status,
          }
        }
        return oldData
      })

      // Show progress notifications
      if (progress.percentage === 100) {
        toast.success(`Pipeline completed successfully!`)
        queryClient.invalidateQueries({ queryKey: ['pipeline', 'history'] })
      } else if (progress.message) {
        toast.info(progress.message)
      }
    }

    // Handle errors
    const handleError = (error: any) => {
      toast.error(error.message || 'Pipeline error occurred')
      queryClient.invalidateQueries({ queryKey: ['pipeline', pipelineId] })
    }

    // Handle article completion
    const handleArticleComplete = (article: any) => {
      toast.success(`Article "${article.title}" has been generated!`)
      queryClient.invalidateQueries({ queryKey: ['articles'] })
    }

    // Register event listeners
    wsService.on('connected', handleConnected)
    wsService.on('disconnected', handleDisconnected)
    wsService.on('pipeline_progress', handlePipelineProgress)
    wsService.on('error', handleError)
    wsService.on('article_complete', handleArticleComplete)

    // Cleanup
    return () => {
      wsService.off('connected', handleConnected)
      wsService.off('disconnected', handleDisconnected)
      wsService.off('pipeline_progress', handlePipelineProgress)
      wsService.off('error', handleError)
      wsService.off('article_complete', handleArticleComplete)
      wsService.disconnect()
    }
  }, [pipelineId, queryClient])

  const pausePipeline = useCallback(() => {
    if (pipelineId) {
      wsService.pausePipeline(pipelineId)
    }
  }, [pipelineId])

  const resumePipeline = useCallback(() => {
    if (pipelineId) {
      wsService.resumePipeline(pipelineId)
    }
  }, [pipelineId])

  const cancelPipeline = useCallback(() => {
    if (pipelineId) {
      wsService.cancelPipeline(pipelineId)
    }
  }, [pipelineId])

  return {
    isConnected,
    pausePipeline,
    resumePipeline,
    cancelPipeline,
  }
}

// General notifications WebSocket
export function useNotificationsWebSocket() {
  const queryClient = useQueryClient()
  const [isConnected, setIsConnected] = useState(false)

  useEffect(() => {
    // Connect to general notifications
    wsService.connect()

    const handleConnected = () => setIsConnected(true)
    const handleDisconnected = () => setIsConnected(false)

    const handleAgentStatus = (status: any) => {
      queryClient.invalidateQueries({ queryKey: ['monitoring', 'agents'] })
      
      if (status.status === 'error' || status.status === 'offline') {
        toast.error(`Agent ${status.name} is ${status.status}`)
      }
    }

    wsService.on('connected', handleConnected)
    wsService.on('disconnected', handleDisconnected)
    wsService.on('agent_status', handleAgentStatus)

    return () => {
      wsService.off('connected', handleConnected)
      wsService.off('disconnected', handleDisconnected)
      wsService.off('agent_status', handleAgentStatus)
      wsService.disconnect()
    }
  }, [queryClient])

  return { isConnected }
}
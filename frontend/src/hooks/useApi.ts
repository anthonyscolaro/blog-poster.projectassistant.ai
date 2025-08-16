import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { toast } from 'sonner'
import apiService from '@/services/api'
import { PipelineRequest, PipelineResult, ArticleGenerationRequest, SEOAnalysisRequest, WordPressPublishRequest } from '@/types/api'

// Pipeline hooks - CORRECTED
export function usePipelineHistory() {
  return useQuery({
    queryKey: ['pipeline', 'history'],
    queryFn: () => apiService.getPipelineHistory(),
    refetchInterval: 30000,
    staleTime: 10000,
  })
}

export function usePipelineStatus(pipelineId: string) {
  return useQuery({
    queryKey: ['pipeline', pipelineId],
    queryFn: () => apiService.getPipelineStatus(pipelineId),
    enabled: !!pipelineId,
    refetchInterval: 5000, // Poll every 5 seconds while running
  })
}

export function useRunPipeline() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: (request: PipelineRequest) => apiService.runPipeline(request),
    onSuccess: (result) => {
      queryClient.invalidateQueries({ queryKey: ['pipeline'] })
      toast.success('Pipeline started successfully!')
    },
    onError: (error: Error) => {
      console.error('Failed to start pipeline:', error)
      toast.error(error.message || 'Failed to start pipeline')
    },
  })
}

export function useCancelPipeline() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: (pipelineId: string) => apiService.cancelPipeline(pipelineId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['pipeline'] })
      toast.success('Pipeline cancelled successfully')
    },
    onError: (error: Error) => {
      console.error('Failed to cancel pipeline:', error)
      toast.error(error.message || 'Failed to cancel pipeline')
    },
  })
}

// Monitoring hooks - CORRECTED
export function useAgentsStatus() {
  return useQuery({
    queryKey: ['monitoring', 'agents'],
    queryFn: () => apiService.getAgentsStatus(),
    refetchInterval: 10000,
  })
}

export function useSystemMetrics() {
  return useQuery({
    queryKey: ['monitoring', 'metrics'],
    queryFn: () => apiService.getSystemMetrics(),
    refetchInterval: 30000,
  })
}

export function useDependencyHealth() {
  return useQuery({
    queryKey: ['monitoring', 'dependencies'],
    queryFn: () => apiService.checkDependencies(),
    refetchInterval: 30000,
  })
}

// Cost tracking
export function useCostMetrics() {
  return useQuery({
    queryKey: ['costs'],
    queryFn: () => apiService.getCosts(),
    refetchInterval: 60000, // Update every minute
  })
}

// Health check with organization context
export function useHealthCheck() {
  return useQuery({
    queryKey: ['health'],
    queryFn: () => apiService.getHealth(),
    refetchInterval: 60000,
    retry: 3,
  })
}

// Article operations
export function useGenerateArticle() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: (request: ArticleGenerationRequest) => apiService.generateArticle(request),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['articles'] })
      toast.success('Article generation started!')
    },
    onError: (error: Error) => {
      console.error('Failed to generate article:', error)
      toast.error(error.message || 'Failed to generate article')
    },
  })
}

export function useDeleteArticle() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: (articleId: string) => apiService.deleteArticle(articleId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['articles'] })
      toast.success('Article deleted successfully')
    },
    onError: (error: Error) => {
      console.error('Failed to delete article:', error)
      toast.error(error.message || 'Failed to delete article')
    },
  })
}

// SEO operations
export function useAnalyzeSEO() {
  return useMutation({
    mutationFn: (request: SEOAnalysisRequest) => apiService.analyzeSEO(request),
    onError: (error: Error) => {
      console.error('SEO analysis failed:', error)
      toast.error(error.message || 'SEO analysis failed')
    },
  })
}

export function useLintSEO() {
  return useMutation({
    mutationFn: (content: string) => apiService.lintSEO(content),
    onError: (error: Error) => {
      console.error('SEO linting failed:', error)
      toast.error(error.message || 'SEO linting failed')
    },
  })
}

// WordPress operations
export function usePublishToWordPress() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: (request: WordPressPublishRequest) => apiService.publishToWordPress(request),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['articles'] })
      toast.success('Article published to WordPress!')
    },
    onError: (error: Error) => {
      console.error('WordPress publish failed:', error)
      toast.error(error.message || 'Failed to publish to WordPress')
    },
  })
}
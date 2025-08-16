import { useState, useEffect } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Link, useNavigate } from 'react-router-dom'
import { supabase } from '@/integrations/supabase/client'
import { useAuth } from '@/contexts/AuthContext'
import { ArticleCard } from '@/components/articles/ArticleCard'
import { ArticleFilters } from '@/components/articles/ArticleFilters'
import { ArticleSearch } from '@/components/articles/ArticleSearch'
import { Button } from '@/components/ui/button'
import { 
  FileText, 
  Plus, 
  Filter, 
  Grid, 
  List,
  TrendingUp,
  Clock,
  CheckCircle,
  AlertCircle,
  Loader2
} from 'lucide-react'
import toast from 'react-hot-toast'

interface Article {
  id: string
  organization_id: string
  title: string
  slug: string
  excerpt: string
  content: string
  meta_title: string
  meta_description: string
  status: 'draft' | 'published' | 'scheduled' | 'archived'
  seo_score: number
  word_count: number
  reading_time: number
  generation_cost: number
  published_at: string | null
  scheduled_for: string | null
  created_at: string
  updated_at: string
  keywords: string[]
  featured_image: string | null
  wordpress_id: string | null
  wordpress_url: string | null
  user_id: string
}

export default function Articles() {
  const { organization } = useAuth()
  const [filters, setFilters] = useState<any>({})
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid')
  const [showFilters, setShowFilters] = useState(false)
  const [searchTerm, setSearchTerm] = useState('')
  const navigate = useNavigate()
  const queryClient = useQueryClient()

  // Set up real-time subscription
  useEffect(() => {
    if (!organization?.id) return

    const channel = supabase
      .channel(`articles:${organization.id}`)
      .on(
        'postgres_changes',
        {
          event: '*',
          schema: 'public',
          table: 'articles',
          filter: `organization_id=eq.${organization.id}`
        },
        (payload) => {
          queryClient.invalidateQueries({ queryKey: ['articles'] })
          
          if (payload.eventType === 'INSERT') {
            toast.success('New article created')
          } else if (payload.eventType === 'UPDATE') {
            const article = payload.new as Article
            if (article.status === 'published') {
              toast.success(`Article "${article.title}" published!`)
            }
          }
        }
      )
      .subscribe()

    return () => {
      supabase.removeChannel(channel)
    }
  }, [organization?.id, queryClient])

  // Query articles from Supabase
  const { data: articles, isLoading, error } = useQuery({
    queryKey: ['articles', organization?.id, filters, searchTerm],
    queryFn: async () => {
      let query = supabase
        .from('articles')
        .select('*')
        .eq('organization_id', organization!.id)
        .order('created_at', { ascending: false })

      if (filters.status) {
        query = query.eq('status', filters.status)
      }
      if (filters.seoScoreMin) {
        query = query.gte('seo_score', filters.seoScoreMin)
      }
      if (searchTerm) {
        query = query.or(`title.ilike.%${searchTerm}%,content.ilike.%${searchTerm}%`)
      }

      const { data, error } = await query

      if (error) throw error
      return data as Article[]
    },
    enabled: !!organization?.id
  })

  // Query article stats
  const { data: stats } = useQuery({
    queryKey: ['article-stats', organization?.id],
    queryFn: async () => {
      const { data: articles, error } = await supabase
        .from('articles')
        .select('status, seo_score')
        .eq('organization_id', organization!.id)

      if (error) throw error

      return {
        totalArticles: articles?.length || 0,
        publishedArticles: articles?.filter(a => a.status === 'published').length || 0,
        draftArticles: articles?.filter(a => a.status === 'draft').length || 0,
        scheduledArticles: articles?.filter(a => a.status === 'scheduled').length || 0,
        avgSeoScore: articles?.length 
          ? Math.round(articles.reduce((sum, a) => sum + (a.seo_score || 0), 0) / articles.length)
          : 0
      }
    },
    enabled: !!organization?.id
  })

  // Delete article mutation
  const deleteArticleMutation = useMutation({
    mutationFn: async (articleId: string) => {
      const { error } = await supabase
        .from('articles')
        .delete()
        .eq('id', articleId)
        .eq('organization_id', organization!.id)

      if (error) throw error
    },
    onSuccess: () => {
      toast.success('Article deleted')
      queryClient.invalidateQueries({ queryKey: ['articles'] })
    },
    onError: (error: any) => {
      toast.error(`Failed to delete: ${error.message}`)
    }
  })

  const handleSearch = (value: string) => {
    setSearchTerm(value)
  }

  const handleFilterChange = (newFilters: any) => {
    setFilters(prev => ({ ...prev, ...newFilters }))
  }

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-foreground mb-2">
            Articles
          </h1>
          <p className="text-muted-foreground">
            Manage your SEO-optimized content library
          </p>
        </div>

        <div className="flex items-center gap-3">
          {/* View Mode Toggle */}
          <div className="flex items-center bg-background rounded-lg border border-border">
            <button
              onClick={() => setViewMode('grid')}
              className={`p-2 rounded-l-lg transition-colors ${
                viewMode === 'grid' 
                  ? 'bg-accent text-accent-foreground' 
                  : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground'
              }`}
            >
              <Grid className="h-4 w-4" />
            </button>
            <button
              onClick={() => setViewMode('list')}
              className={`p-2 rounded-r-lg transition-colors ${
                viewMode === 'list' 
                  ? 'bg-accent text-accent-foreground' 
                  : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground'
              }`}
            >
              <List className="h-4 w-4" />
            </button>
          </div>

          <Button
            variant="outline"
            onClick={() => setShowFilters(!showFilters)}
          >
            <Filter className="h-4 w-4 mr-2" />
            Filters
          </Button>

          <Button
            onClick={() => navigate('/articles/new')}
          >
            <Plus className="h-4 w-4 mr-2" />
            New Article
          </Button>
        </div>
      </div>

      {/* Stats Cards */}
      {stats && (
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-8">
          <div className="bg-card rounded-lg p-4 border border-border">
            <div className="flex items-center justify-between">
              <FileText className="h-5 w-5 text-muted-foreground" />
              <span className="text-2xl font-bold text-foreground">
                {stats.totalArticles}
              </span>
            </div>
            <p className="text-sm text-muted-foreground mt-1">Total</p>
          </div>
          
          <div className="bg-card rounded-lg p-4 border border-border">
            <div className="flex items-center justify-between">
              <CheckCircle className="h-5 w-5 text-green-500" />
              <span className="text-2xl font-bold text-foreground">
                {stats.publishedArticles}
              </span>
            </div>
            <p className="text-sm text-muted-foreground mt-1">Published</p>
          </div>

          <div className="bg-card rounded-lg p-4 border border-border">
            <div className="flex items-center justify-between">
              <FileText className="h-5 w-5 text-muted-foreground" />
              <span className="text-2xl font-bold text-foreground">
                {stats.draftArticles}
              </span>
            </div>
            <p className="text-sm text-muted-foreground mt-1">Drafts</p>
          </div>

          <div className="bg-card rounded-lg p-4 border border-border">
            <div className="flex items-center justify-between">
              <Clock className="h-5 w-5 text-blue-500" />
              <span className="text-2xl font-bold text-foreground">
                {stats.scheduledArticles}
              </span>
            </div>
            <p className="text-sm text-muted-foreground mt-1">Scheduled</p>
          </div>

          <div className="bg-card rounded-lg p-4 border border-border">
            <div className="flex items-center justify-between">
              <TrendingUp className="h-5 w-5 text-purple-500" />
              <span className="text-2xl font-bold text-foreground">
                {stats.avgSeoScore}
              </span>
            </div>
            <p className="text-sm text-muted-foreground mt-1">Avg SEO</p>
          </div>
        </div>
      )}

      {/* Search and Filters */}
      <div className="mb-6">
        <ArticleSearch onSearch={handleSearch} />
        
        {showFilters && (
          <div className="mt-4">
            <ArticleFilters 
              filters={filters}
              onChange={handleFilterChange}
            />
          </div>
        )}
      </div>

      {/* Articles Grid/List */}
      {isLoading ? (
        <div className="flex items-center justify-center py-12">
          <Loader2 className="h-8 w-8 animate-spin text-primary" />
        </div>
      ) : error ? (
        <div className="text-center py-8">
          <AlertCircle className="h-12 w-12 text-destructive mx-auto mb-3" />
          <p className="text-muted-foreground">
            Failed to load articles. Please try again.
          </p>
        </div>
      ) : !articles?.length ? (
        <div className="text-center py-12">
          <FileText className="h-16 w-16 text-muted-foreground mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-foreground mb-2">
            No articles found
          </h3>
          <p className="text-muted-foreground mb-6">
            Get started by creating your first article or running the content pipeline.
          </p>
          <div className="flex items-center justify-center gap-3">
            <Button onClick={() => navigate('/articles/new')}>
              Create Article
            </Button>
            <Button variant="outline" onClick={() => navigate('/pipeline')}>
              Run Pipeline
            </Button>
          </div>
        </div>
      ) : (
        <div className={
          viewMode === 'grid' 
            ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6'
            : 'space-y-4'
        }>
          {articles.map((article) => (
            <ArticleCard 
              key={article.id} 
              article={article} 
              viewMode={viewMode}
              onDelete={() => deleteArticleMutation.mutate(article.id)}
            />
          ))}
        </div>
      )}
    </div>
  )
}
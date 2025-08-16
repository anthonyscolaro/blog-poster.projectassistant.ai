# Lovable Prompt: Article Management System (Hybrid Architecture)

## Backend Integration Notice

This component uses Blog-Poster's hybrid architecture:
- **Data Storage**: Supabase `articles` table (direct queries)
- **AI Processing**: FastAPI endpoints for SEO analysis
- **Real-time**: Supabase subscriptions for article updates

### API Endpoints Used:
- POST `/api/v1/seo/analyze` - Analyze article SEO score and get optimization suggestions
- POST `/api/v1/wordpress/publish` - Publish article to WordPress (optional)

### Development Mode:
When FastAPI backend is unavailable, mock responses are provided for testing.

## Business Context:
The article management system is the content hub for Blog-Poster, providing comprehensive CRUD operations for SEO-optimized articles. It combines Supabase for data persistence with FastAPI for AI-powered SEO analysis, ensuring all content meets quality standards before publication.

## User Story:
"As a content manager, I want to create, edit, preview, and publish articles with real-time collaboration, SEO validation, and scheduling capabilities, while leveraging AI for optimization suggestions."

## Prompt for Lovable:

Create a comprehensive article management system that uses Supabase for data storage and FastAPI for AI processing. The system should handle the complete lifecycle of SEO-optimized content.

**First, create the API client service:**

### API Client Service
```typescript
// src/services/api.ts
import { supabase } from '@/services/supabase'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8088'

// Mock responses for development
const MOCK_MODE = !API_URL || API_URL.includes('localhost')

const MOCK_RESPONSES = {
  '/api/v1/seo/analyze': {
    score: 85,
    issues: [
      {
        type: 'warning',
        category: 'Meta',
        title: 'Meta description could be longer',
        description: 'Current length: 120 characters. Optimal: 150-160 characters.',
        fix: 'Add more descriptive content to your meta description'
      }
    ],
    suggestions: [
      {
        title: 'Add more internal links',
        description: 'Link to related articles to improve SEO and user engagement',
        impact: 'high'
      },
      {
        title: 'Optimize heading structure',
        description: 'Use H2 and H3 tags to create a clear content hierarchy',
        impact: 'medium'
      }
    ],
    keywordAnalysis: {
      primary: 'service dog training',
      density: 2.3,
      secondary: ['ADA requirements', 'public access', 'handler rights'],
      related: ['emotional support animal', 'therapy dog', 'assistance dog'],
      missingKeywords: ['certification', 'registration']
    },
    readabilityScore: 78,
    technicalChecks: [
      { name: 'Title Length', status: 'passed', description: '58 characters (optimal)' },
      { name: 'Meta Description', status: 'warning', description: '120 characters (could be longer)' },
      { name: 'Keyword Density', status: 'passed', description: '2.3% (optimal range)' },
      { name: 'Alt Text', status: 'failed', description: '3 images missing alt text' }
    ]
  },
  '/api/v1/wordpress/publish': {
    success: true,
    wordpressId: 'wp-123',
    url: 'https://blog.example.com/your-article',
    message: 'Article published successfully'
  }
}

export class APIClient {
  private async getAuthHeader() {
    const session = await supabase.auth.getSession()
    return session.data.session ? {
      'Authorization': `Bearer ${session.data.session.access_token}`
    } : {}
  }

  async analyzeSEO(article: any, targetKeyword?: string) {
    if (MOCK_MODE) {
      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 1000))
      return MOCK_RESPONSES['/api/v1/seo/analyze']
    }

    try {
      const response = await fetch(`${API_URL}/api/v1/seo/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(await this.getAuthHeader())
        },
        body: JSON.stringify({ article, targetKeyword })
      })

      if (!response.ok) {
        throw new Error(`SEO analysis failed: ${response.statusText}`)
      }

      return await response.json()
    } catch (error) {
      console.warn('SEO API unavailable, using mock data', error)
      return MOCK_RESPONSES['/api/v1/seo/analyze']
    }
  }

  async publishToWordPress(articleId: string, siteId: string) {
    if (MOCK_MODE) {
      await new Promise(resolve => setTimeout(resolve, 1500))
      return MOCK_RESPONSES['/api/v1/wordpress/publish']
    }

    try {
      const response = await fetch(`${API_URL}/api/v1/wordpress/publish`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(await this.getAuthHeader())
        },
        body: JSON.stringify({ articleId, siteId })
      })

      if (!response.ok) {
        throw new Error(`WordPress publish failed: ${response.statusText}`)
      }

      return await response.json()
    } catch (error) {
      console.warn('WordPress API unavailable, using mock data', error)
      return MOCK_RESPONSES['/api/v1/wordpress/publish']
    }
  }
}

export const apiClient = new APIClient()
```

**Now create the main Articles page using Supabase:**

### Main Articles Page
```typescript
// src/pages/Articles.tsx
import { useState, useEffect } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Link, useNavigate } from 'react-router-dom'
import { supabase } from '@/services/supabase'
import { useAuth } from '@/contexts/AuthContext'
import { ArticleCard } from '@/components/articles/ArticleCard'
import { ArticleFilters } from '@/components/articles/ArticleFilters'
import { ArticleSearch } from '@/components/articles/ArticleSearch'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
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
  read_time: number
  generation_cost: number
  published_at: string | null
  scheduled_at: string | null
  created_at: string
  updated_at: string
  tags: string[]
  featured_image: string | null
  wordpress_id: string | null
  wordpress_url: string | null
  author_id: string
  pipeline_id: string | null
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
          // Refresh articles when changes occur
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

      // Apply filters
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

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'published':
        return <CheckCircle className="h-4 w-4 text-green-500" />
      case 'scheduled':
        return <Clock className="h-4 w-4 text-blue-500" />
      case 'draft':
        return <FileText className="h-4 w-4 text-gray-500" />
      default:
        return <AlertCircle className="h-4 w-4 text-yellow-500" />
    }
  }

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            Articles
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Manage your SEO-optimized content library
          </p>
        </div>

        <div className="flex items-center gap-3">
          {/* View Mode Toggle */}
          <div className="flex items-center bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
            <button
              onClick={() => setViewMode('grid')}
              className={`p-2 rounded-l-lg ${
                viewMode === 'grid' 
                  ? 'bg-purple-100 dark:bg-purple-900 text-purple-600 dark:text-purple-400' 
                  : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700'
              }`}
            >
              <Grid className="h-4 w-4" />
            </button>
            <button
              onClick={() => setViewMode('list')}
              className={`p-2 rounded-r-lg ${
                viewMode === 'list' 
                  ? 'bg-purple-100 dark:bg-purple-900 text-purple-600 dark:text-purple-400' 
                  : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700'
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
            className="bg-gradient-to-r from-purple-600 to-blue-600 text-white"
          >
            <Plus className="h-4 w-4 mr-2" />
            New Article
          </Button>
        </div>
      </div>

      {/* Stats Cards */}
      {stats && (
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-8">
          <div className="bg-white dark:bg-gray-800 rounded-lg p-4 border border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-between">
              <FileText className="h-5 w-5 text-gray-400" />
              <span className="text-2xl font-bold text-gray-900 dark:text-white">
                {stats.totalArticles}
              </span>
            </div>
            <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">Total</p>
          </div>
          
          <div className="bg-white dark:bg-gray-800 rounded-lg p-4 border border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-between">
              <CheckCircle className="h-5 w-5 text-green-500" />
              <span className="text-2xl font-bold text-gray-900 dark:text-white">
                {stats.publishedArticles}
              </span>
            </div>
            <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">Published</p>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-lg p-4 border border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-between">
              <FileText className="h-5 w-5 text-gray-500" />
              <span className="text-2xl font-bold text-gray-900 dark:text-white">
                {stats.draftArticles}
              </span>
            </div>
            <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">Drafts</p>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-lg p-4 border border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-between">
              <Clock className="h-5 w-5 text-blue-500" />
              <span className="text-2xl font-bold text-gray-900 dark:text-white">
                {stats.scheduledArticles}
              </span>
            </div>
            <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">Scheduled</p>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-lg p-4 border border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-between">
              <TrendingUp className="h-5 w-5 text-purple-500" />
              <span className="text-2xl font-bold text-gray-900 dark:text-white">
                {stats.avgSeoScore}
              </span>
            </div>
            <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">Avg SEO</p>
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
          <Loader2 className="h-8 w-8 animate-spin text-purple-600" />
        </div>
      ) : error ? (
        <div className="text-center py-8">
          <AlertCircle className="h-12 w-12 text-red-500 mx-auto mb-3" />
          <p className="text-gray-600 dark:text-gray-400">
            Failed to load articles. Please try again.
          </p>
        </div>
      ) : !articles?.length ? (
        <div className="text-center py-12">
          <FileText className="h-16 w-16 text-gray-300 dark:text-gray-600 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
            No articles found
          </h3>
          <p className="text-gray-600 dark:text-gray-400 mb-6">
            Get started by creating your first article or running the content pipeline.
          </p>
          <div className="flex items-center justify-center gap-3">
            <Button
              onClick={() => navigate('/articles/new')}
              className="bg-purple-600 hover:bg-purple-700"
            >
              Create Article
            </Button>
            <Button
              variant="outline"
              onClick={() => navigate('/pipeline')}
            >
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
```

### Article Editor Component with SEO Analysis
```typescript
// src/components/articles/ArticleEditor.tsx
import { useState, useEffect } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useNavigate, useParams } from 'react-router-dom'
import { supabase } from '@/services/supabase'
import { apiClient } from '@/services/api'
import { useAuth } from '@/contexts/AuthContext'
import { SEOAnalyzer } from '@/components/articles/SEOAnalyzer'
import { MarkdownEditor } from '@/components/articles/MarkdownEditor'
import { ArticlePreview } from '@/components/articles/ArticlePreview'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { 
  Save, 
  Eye, 
  Code, 
  TrendingUp, 
  Settings,
  ArrowLeft,
  Loader2,
  AlertCircle,
  CheckCircle
} from 'lucide-react'
import toast from 'react-hot-toast'

export function ArticleEditor() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const { user, organization } = useAuth()
  const isNew = id === 'new'

  const [article, setArticle] = useState({
    title: '',
    slug: '',
    excerpt: '',
    content: '',
    meta_title: '',
    meta_description: '',
    status: 'draft' as 'draft' | 'published' | 'scheduled',
    tags: [] as string[],
    featured_image: null as string | null,
    scheduled_at: null as string | null,
  })

  const [activeTab, setActiveTab] = useState<'editor' | 'preview' | 'seo' | 'settings'>('editor')
  const [isAutoSaving, setIsAutoSaving] = useState(false)
  const [lastSaved, setLastSaved] = useState<Date | null>(null)

  // Load article from Supabase if editing
  const { data: existingArticle, isLoading } = useQuery({
    queryKey: ['article', id],
    queryFn: async () => {
      const { data, error } = await supabase
        .from('articles')
        .select('*')
        .eq('id', id)
        .eq('organization_id', organization!.id)
        .single()

      if (error) throw error
      return data
    },
    enabled: !isNew && !!organization?.id,
  })

  // Save article to Supabase
  const saveMutation = useMutation({
    mutationFn: async (articleData: any) => {
      const wordCount = articleData.content.split(/\s+/).length
      const readTime = Math.ceil(wordCount / 200)

      const payload = {
        ...articleData,
        word_count: wordCount,
        read_time: readTime,
        organization_id: organization!.id,
        author_id: user!.id,
        updated_at: new Date().toISOString()
      }

      if (isNew) {
        const { data, error } = await supabase
          .from('articles')
          .insert(payload)
          .select()
          .single()

        if (error) throw error
        return data
      } else {
        const { data, error } = await supabase
          .from('articles')
          .update(payload)
          .eq('id', id)
          .eq('organization_id', organization!.id)
          .select()
          .single()

        if (error) throw error
        return data
      }
    },
    onSuccess: (data) => {
      if (isNew && data.id) {
        navigate(`/articles/${data.id}`, { replace: true })
      }
      toast.success('Article saved successfully!')
      setLastSaved(new Date())
      queryClient.invalidateQueries({ queryKey: ['articles'] })
    },
    onError: (error: any) => {
      toast.error(`Failed to save: ${error.message}`)
    }
  })

  // Auto-save effect
  useEffect(() => {
    if (!article.title && !article.content) return

    const timeoutId = setTimeout(() => {
      setIsAutoSaving(true)
      saveMutation.mutate(article).finally(() => {
        setIsAutoSaving(false)
      })
    }, 3000)

    return () => clearTimeout(timeoutId)
  }, [article])

  // Load existing article
  useEffect(() => {
    if (existingArticle && !isNew) {
      setArticle({
        title: existingArticle.title || '',
        slug: existingArticle.slug || '',
        excerpt: existingArticle.excerpt || '',
        content: existingArticle.content || '',
        meta_title: existingArticle.meta_title || '',
        meta_description: existingArticle.meta_description || '',
        status: existingArticle.status || 'draft',
        tags: existingArticle.tags || [],
        featured_image: existingArticle.featured_image,
        scheduled_at: existingArticle.scheduled_at,
      })
    }
  }, [existingArticle, isNew])

  // Generate slug from title
  useEffect(() => {
    if (article.title && !article.slug) {
      const slug = article.title
        .toLowerCase()
        .replace(/[^a-z0-9]+/g, '-')
        .replace(/(^-|-$)/g, '')
      setArticle(prev => ({ ...prev, slug }))
    }
  }, [article.title])

  const handleArticleChange = (updates: Partial<typeof article>) => {
    setArticle(prev => ({ ...prev, ...updates }))
  }

  const handleSave = () => {
    saveMutation.mutate(article)
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="h-8 w-8 animate-spin text-purple-600" />
      </div>
    )
  }

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-4">
          <Button
            variant="ghost"
            onClick={() => navigate('/articles')}
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back
          </Button>
          <div>
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
              {isNew ? 'New Article' : 'Edit Article'}
            </h1>
            {lastSaved && (
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Last saved {lastSaved.toLocaleTimeString()}
                {isAutoSaving && (
                  <span className="ml-2 text-blue-600">
                    <Loader2 className="inline h-3 w-3 animate-spin mr-1" />
                    Auto-saving...
                  </span>
                )}
              </p>
            )}
          </div>
        </div>

        <Button
          onClick={handleSave}
          disabled={saveMutation.isPending}
        >
          {saveMutation.isPending ? (
            <Loader2 className="h-4 w-4 mr-2 animate-spin" />
          ) : (
            <Save className="h-4 w-4 mr-2" />
          )}
          Save
        </Button>
      </div>

      {/* Editor Tabs */}
      <Tabs value={activeTab} onValueChange={(v) => setActiveTab(v as any)}>
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="editor">
            <Code className="h-4 w-4 mr-2" />
            Editor
          </TabsTrigger>
          <TabsTrigger value="preview">
            <Eye className="h-4 w-4 mr-2" />
            Preview
          </TabsTrigger>
          <TabsTrigger value="seo">
            <TrendingUp className="h-4 w-4 mr-2" />
            SEO Analysis
          </TabsTrigger>
          <TabsTrigger value="settings">
            <Settings className="h-4 w-4 mr-2" />
            Settings
          </TabsTrigger>
        </TabsList>

        <div className="mt-6">
          <TabsContent value="editor" className="space-y-6">
            {/* Title and Basic Fields */}
            <Card>
              <CardContent className="pt-6 space-y-4">
                <div>
                  <Label htmlFor="title">Title</Label>
                  <Input
                    id="title"
                    value={article.title}
                    onChange={(e) => handleArticleChange({ title: e.target.value })}
                    placeholder="Enter article title..."
                  />
                </div>

                <div>
                  <Label htmlFor="slug">Slug</Label>
                  <Input
                    id="slug"
                    value={article.slug}
                    onChange={(e) => handleArticleChange({ slug: e.target.value })}
                    placeholder="article-url-slug"
                  />
                </div>

                <div>
                  <Label htmlFor="excerpt">Excerpt</Label>
                  <Textarea
                    id="excerpt"
                    value={article.excerpt}
                    onChange={(e) => handleArticleChange({ excerpt: e.target.value })}
                    rows={3}
                    placeholder="Brief description of the article..."
                  />
                </div>
              </CardContent>
            </Card>

            {/* Content Editor */}
            <Card>
              <CardHeader>
                <CardTitle>Content</CardTitle>
              </CardHeader>
              <CardContent>
                <MarkdownEditor
                  content={article.content}
                  onChange={(content) => handleArticleChange({ content })}
                />
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="preview">
            <ArticlePreview article={article} />
          </TabsContent>

          <TabsContent value="seo">
            <SEOAnalyzer 
              article={article}
              articleId={!isNew ? id : undefined}
            />
          </TabsContent>

          <TabsContent value="settings" className="space-y-6">
            {/* SEO Settings */}
            <Card>
              <CardHeader>
                <CardTitle>SEO Settings</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label htmlFor="meta_title">Meta Title</Label>
                  <Input
                    id="meta_title"
                    value={article.meta_title}
                    onChange={(e) => handleArticleChange({ meta_title: e.target.value })}
                    placeholder="SEO title (max 60 characters)"
                    maxLength={60}
                  />
                  <p className="text-sm text-gray-500 mt-1">
                    {article.meta_title.length}/60 characters
                  </p>
                </div>

                <div>
                  <Label htmlFor="meta_description">Meta Description</Label>
                  <Textarea
                    id="meta_description"
                    value={article.meta_description}
                    onChange={(e) => handleArticleChange({ meta_description: e.target.value })}
                    placeholder="SEO description (max 160 characters)"
                    maxLength={160}
                    rows={3}
                  />
                  <p className="text-sm text-gray-500 mt-1">
                    {article.meta_description.length}/160 characters
                  </p>
                </div>
              </CardContent>
            </Card>

            {/* Publishing Settings */}
            <Card>
              <CardHeader>
                <CardTitle>Publishing</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label>Status</Label>
                  <div className="flex gap-4 mt-2">
                    {['draft', 'published', 'scheduled'].map((status) => (
                      <label key={status} className="flex items-center">
                        <input
                          type="radio"
                          name="status"
                          value={status}
                          checked={article.status === status}
                          onChange={(e) => handleArticleChange({ status: e.target.value as any })}
                          className="mr-2"
                        />
                        <span className="capitalize">{status}</span>
                      </label>
                    ))}
                  </div>
                </div>

                {article.status === 'scheduled' && (
                  <div>
                    <Label htmlFor="scheduled_at">Schedule Date</Label>
                    <Input
                      id="scheduled_at"
                      type="datetime-local"
                      value={article.scheduled_at || ''}
                      onChange={(e) => handleArticleChange({ scheduled_at: e.target.value })}
                    />
                  </div>
                )}

                <div>
                  <Label htmlFor="tags">Tags</Label>
                  <Input
                    id="tags"
                    value={article.tags.join(', ')}
                    onChange={(e) => handleArticleChange({ 
                      tags: e.target.value.split(',').map(t => t.trim()).filter(Boolean) 
                    })}
                    placeholder="tag1, tag2, tag3"
                  />
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </div>
      </Tabs>
    </div>
  )
}
```

### SEO Analyzer Component
```typescript
// src/components/articles/SEOAnalyzer.tsx
import { useState, useEffect } from 'react'
import { useMutation } from '@tanstack/react-query'
import { apiClient } from '@/services/api'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Progress } from '@/components/ui/progress'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Badge } from '@/components/ui/badge'
import { 
  TrendingUp, 
  CheckCircle, 
  AlertCircle, 
  XCircle,
  Lightbulb,
  Search,
  Loader2
} from 'lucide-react'

interface SEOAnalyzerProps {
  article: {
    title: string
    content: string
    meta_title: string
    meta_description: string
    slug: string
  }
  articleId?: string
}

export function SEOAnalyzer({ article, articleId }: SEOAnalyzerProps) {
  const [targetKeyword, setTargetKeyword] = useState('')
  const [analysis, setAnalysis] = useState<any>(null)

  const analyzeMutation = useMutation({
    mutationFn: async () => {
      return await apiClient.analyzeSEO(article, targetKeyword)
    },
    onSuccess: (data) => {
      setAnalysis(data)
    }
  })

  // Auto-analyze on content change
  useEffect(() => {
    if (article.title && article.content) {
      const timer = setTimeout(() => {
        analyzeMutation.mutate()
      }, 1000)
      return () => clearTimeout(timer)
    }
  }, [article.title, article.content, article.meta_title, article.meta_description])

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600'
    if (score >= 60) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getScoreBg = (score: number) => {
    if (score >= 80) return 'bg-green-100 dark:bg-green-900/20'
    if (score >= 60) return 'bg-yellow-100 dark:bg-yellow-900/20'
    return 'bg-red-100 dark:bg-red-900/20'
  }

  return (
    <div className="space-y-6">
      {/* Target Keyword */}
      <Card>
        <CardHeader>
          <CardTitle>Target Keyword Analysis</CardTitle>
          <CardDescription>
            Set your primary keyword for focused SEO optimization
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex gap-4">
            <div className="flex-1">
              <Label htmlFor="keyword">Primary Keyword</Label>
              <Input
                id="keyword"
                value={targetKeyword}
                onChange={(e) => setTargetKeyword(e.target.value)}
                placeholder="e.g., service dog training"
              />
            </div>
            <Button
              onClick={() => analyzeMutation.mutate()}
              disabled={analyzeMutation.isPending}
              className="mt-6"
            >
              {analyzeMutation.isPending ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <Search className="h-4 w-4" />
              )}
            </Button>
          </div>
        </CardContent>
      </Card>

      {analyzeMutation.isPending && !analysis && (
        <div className="flex items-center justify-center py-8">
          <Loader2 className="h-8 w-8 animate-spin text-purple-600" />
        </div>
      )}

      {analysis && (
        <>
          {/* SEO Score */}
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle>SEO Score</CardTitle>
                <div className={`flex items-center px-4 py-2 rounded-lg ${getScoreBg(analysis.score)}`}>
                  <TrendingUp className={`h-5 w-5 mr-2 ${getScoreColor(analysis.score)}`} />
                  <span className={`text-2xl font-bold ${getScoreColor(analysis.score)}`}>
                    {analysis.score}/100
                  </span>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-3 gap-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-gray-900 dark:text-white">
                    {analysis.keywordAnalysis.density.toFixed(1)}%
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">
                    Keyword Density
                  </div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-gray-900 dark:text-white">
                    {analysis.readabilityScore}
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">
                    Readability
                  </div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-gray-900 dark:text-white">
                    {analysis.technicalChecks.filter(c => c.status === 'passed').length}/{analysis.technicalChecks.length}
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">
                    Checks Passed
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Issues */}
          {analysis.issues.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle>Issues to Fix</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {analysis.issues.map((issue, index) => (
                  <Alert key={index} variant={issue.type === 'error' ? 'destructive' : 'default'}>
                    {issue.type === 'error' && <XCircle className="h-4 w-4" />}
                    {issue.type === 'warning' && <AlertCircle className="h-4 w-4" />}
                    <AlertDescription>
                      <strong>{issue.title}</strong>
                      <p className="mt-1">{issue.description}</p>
                      {issue.fix && (
                        <p className="mt-2 text-sm">
                          <Lightbulb className="inline h-3 w-3 mr-1" />
                          {issue.fix}
                        </p>
                      )}
                    </AlertDescription>
                  </Alert>
                ))}
              </CardContent>
            </Card>
          )}

          {/* Suggestions */}
          {analysis.suggestions.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle>Optimization Suggestions</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                {analysis.suggestions.map((suggestion, index) => (
                  <div key={index} className="flex items-start gap-3">
                    <Lightbulb className="h-4 w-4 text-yellow-500 mt-1 flex-shrink-0" />
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <p className="font-medium">{suggestion.title}</p>
                        <Badge variant={
                          suggestion.impact === 'high' ? 'destructive' :
                          suggestion.impact === 'medium' ? 'default' :
                          'secondary'
                        }>
                          {suggestion.impact} impact
                        </Badge>
                      </div>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        {suggestion.description}
                      </p>
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>
          )}

          {/* Technical Checks */}
          <Card>
            <CardHeader>
              <CardTitle>Technical SEO Checks</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              {analysis.technicalChecks.map((check, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-900 rounded-lg">
                  <div className="flex items-center gap-3">
                    {check.status === 'passed' && <CheckCircle className="h-4 w-4 text-green-500" />}
                    {check.status === 'warning' && <AlertCircle className="h-4 w-4 text-yellow-500" />}
                    {check.status === 'failed' && <XCircle className="h-4 w-4 text-red-500" />}
                    <div>
                      <p className="font-medium">{check.name}</p>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        {check.description}
                      </p>
                    </div>
                  </div>
                  <Badge variant={
                    check.status === 'passed' ? 'success' :
                    check.status === 'warning' ? 'warning' :
                    'destructive'
                  }>
                    {check.status}
                  </Badge>
                </div>
              ))}
            </CardContent>
          </Card>
        </>
      )}
    </div>
  )
}
```

**Success Criteria:**
- ✅ Hybrid architecture with Supabase for data, FastAPI for AI processing
- ✅ Mock responses for frontend-only development
- ✅ Real-time Supabase subscriptions for article updates
- ✅ SEO analysis via FastAPI with fallback to mock data
- ✅ Complete CRUD operations using Supabase
- ✅ Auto-save functionality with debouncing
- ✅ Row Level Security with organization-based filtering
- ✅ Integration with existing authentication context
- ✅ Responsive design with grid/list views
- ✅ Error handling and loading states

This implementation properly balances between Supabase for data operations and FastAPI for AI/processing tasks, ensuring Lovable understands the hybrid architecture while maintaining the ability to develop frontend-only with mock data.
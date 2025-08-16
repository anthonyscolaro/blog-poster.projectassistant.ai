# Lovable Prompt: Article Management System

## Business Context:
The article management system is the content hub for Blog-Poster, providing comprehensive CRUD operations for SEO-optimized articles. It includes content editing, SEO validation, WordPress publishing, scheduling, and performance tracking - essential for managing high-quality service dog industry content.

## User Story:
"As a content manager, I want to create, edit, preview, and publish articles with built-in SEO validation, WordPress integration, and scheduling capabilities, ensuring all content meets our quality standards before publication."

## Article Management Requirements:
- **Content CRUD**: Full create, read, update, delete operations
- **Rich Text Editor**: Markdown support with live preview
- **SEO Validation**: Real-time scoring and optimization suggestions
- **WordPress Publishing**: Direct publishing to configured WordPress sites
- **Article Scheduling**: Future publication scheduling
- **Performance Tracking**: Views, engagement, and SEO metrics

## Prompt for Lovable:

Create a comprehensive article management system for the Blog-Poster platform that handles the complete lifecycle of SEO-optimized content from creation to publication and performance tracking.

**Article Management Components:**

### Main Articles Page
```typescript
// src/pages/Articles.tsx
import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Link, useNavigate } from 'react-router-dom'
import { apiClient } from '@/services/api'
import { ArticleCard } from '@/components/articles/ArticleCard'
import { ArticleFilters } from '@/components/articles/ArticleFilters'
import { ArticleSearch } from '@/components/articles/ArticleSearch'
import { 
  FileText, 
  Plus, 
  Filter, 
  Grid, 
  List,
  TrendingUp,
  Clock,
  CheckCircle,
  AlertCircle
} from 'lucide-react'

interface Article {
  id: string
  title: string
  slug: string
  excerpt: string
  content: string
  metaTitle: string
  metaDescription: string
  status: 'draft' | 'published' | 'scheduled' | 'archived'
  seoScore: number
  wordCount: number
  readTime: number
  generationCost: number
  publishedAt: string | null
  scheduledAt: string | null
  createdAt: string
  updatedAt: string
  tags: string[]
  featuredImage: string | null
  wordpressId: string | null
  wordpressSite: string | null
  performance: {
    views: number
    clickThroughRate: number
    avgTimeOnPage: number
    bounceRate: number
  }
}

interface ArticleFilters {
  status?: string
  tags?: string[]
  seoScoreMin?: number
  dateFrom?: string
  dateTo?: string
  search?: string
}

export default function Articles() {
  const [filters, setFilters] = useState<ArticleFilters>({})
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid')
  const [showFilters, setShowFilters] = useState(false)
  const navigate = useNavigate()

  // Query articles with filters
  const { data: articles, isLoading, error } = useQuery({
    queryKey: ['articles', filters],
    queryFn: () => apiClient.get<{
      articles: Article[]
      total: number
      page: number
      limit: number
    }>('/api/articles', { params: filters }),
  })

  // Article stats
  const { data: stats } = useQuery({
    queryKey: ['article-stats'],
    queryFn: () => apiClient.get<{
      totalArticles: number
      publishedArticles: number
      draftArticles: number
      scheduledArticles: number
      avgSeoScore: number
      totalViews: number
    }>('/api/articles/stats'),
  })

  const handleFilterChange = (newFilters: Partial<ArticleFilters>) => {
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
    <div className="max-w-7xl mx-auto">
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

          <button
            onClick={() => setShowFilters(!showFilters)}
            className="inline-flex items-center px-4 py-2 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700"
          >
            <Filter className="h-4 w-4 mr-2" />
            Filters
          </button>

          <Link
            to="/articles/new"
            className="inline-flex items-center px-4 py-2 bg-purple-gradient text-white rounded-lg hover:opacity-90"
          >
            <Plus className="h-4 w-4 mr-2" />
            New Article
          </Link>
        </div>
      </div>

      {/* Stats Cards */}
      {stats && (
        <div className="grid grid-cols-2 md:grid-cols-6 gap-4 mb-8">
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

          <div className="bg-white dark:bg-gray-800 rounded-lg p-4 border border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-between">
              <TrendingUp className="h-5 w-5 text-green-500" />
              <span className="text-2xl font-bold text-gray-900 dark:text-white">
                {stats.totalViews.toLocaleString()}
              </span>
            </div>
            <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">Views</p>
          </div>
        </div>
      )}

      {/* Search and Filters */}
      <div className="mb-6">
        <ArticleSearch 
          onSearch={(search) => handleFilterChange({ search })} 
        />
        
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
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {Array.from({ length: 6 }).map((_, i) => (
            <div key={i} className="animate-pulse">
              <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border border-gray-200 dark:border-gray-700">
                <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-3/4 mb-4" />
                <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded w-full mb-2" />
                <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded w-2/3" />
              </div>
            </div>
          ))}
        </div>
      ) : error ? (
        <div className="text-center py-8">
          <AlertCircle className="h-12 w-12 text-red-500 mx-auto mb-3" />
          <p className="text-gray-600 dark:text-gray-400">
            Failed to load articles. Please try again.
          </p>
        </div>
      ) : !articles?.articles.length ? (
        <div className="text-center py-12">
          <FileText className="h-16 w-16 text-gray-300 dark:text-gray-600 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
            No articles found
          </h3>
          <p className="text-gray-600 dark:text-gray-400 mb-6">
            Get started by creating your first article or running the content pipeline.
          </p>
          <div className="flex items-center justify-center gap-3">
            <Link
              to="/articles/new"
              className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700"
            >
              Create Article
            </Link>
            <Link
              to="/pipeline"
              className="px-4 py-2 bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-700"
            >
              Run Pipeline
            </Link>
          </div>
        </div>
      ) : (
        <div className={
          viewMode === 'grid' 
            ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6'
            : 'space-y-4'
        }>
          {articles.articles.map((article) => (
            <ArticleCard 
              key={article.id} 
              article={article} 
              viewMode={viewMode}
            />
          ))}
        </div>
      )}
    </div>
  )
}
```

### Article Editor Component
```typescript
// src/components/articles/ArticleEditor.tsx
import { useState, useEffect } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useNavigate, useParams } from 'react-router-dom'
import { apiClient } from '@/services/api'
import { SEOAnalyzer } from '@/components/articles/SEOAnalyzer'
import { MarkdownEditor } from '@/components/articles/MarkdownEditor'
import { ArticlePreview } from '@/components/articles/ArticlePreview'
import { PublishingPanel } from '@/components/articles/PublishingPanel'
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

interface ArticleData {
  id?: string
  title: string
  slug: string
  excerpt: string
  content: string
  metaTitle: string
  metaDescription: string
  status: 'draft' | 'published' | 'scheduled'
  tags: string[]
  featuredImage: string | null
  scheduledAt: string | null
  wordpressSiteId: string | null
}

export function ArticleEditor() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const isNew = id === 'new'

  const [article, setArticle] = useState<ArticleData>({
    title: '',
    slug: '',
    excerpt: '',
    content: '',
    metaTitle: '',
    metaDescription: '',
    status: 'draft',
    tags: [],
    featuredImage: null,
    scheduledAt: null,
    wordpressSiteId: null,
  })

  const [activeTab, setActiveTab] = useState<'editor' | 'preview' | 'seo' | 'publish'>('editor')
  const [isAutoSaving, setIsAutoSaving] = useState(false)
  const [lastSaved, setLastSaved] = useState<Date | null>(null)

  // Load article data if editing
  const { data: existingArticle, isLoading } = useQuery({
    queryKey: ['article', id],
    queryFn: () => apiClient.get<Article>(`/api/articles/${id}`),
    enabled: !isNew,
  })

  // Auto-save mutation
  const autoSaveMutation = useMutation({
    mutationFn: (data: Partial<ArticleData>) => 
      isNew 
        ? apiClient.post('/api/articles', { ...article, ...data, status: 'draft' })
        : apiClient.put(`/api/articles/${id}`, { ...article, ...data }),
    onSuccess: (data) => {
      if (isNew && data.id) {
        navigate(`/articles/${data.id}`, { replace: true })
      }
      setLastSaved(new Date())
      setIsAutoSaving(false)
      queryClient.invalidateQueries({ queryKey: ['article', id] })
    },
    onError: () => {
      setIsAutoSaving(false)
      toast.error('Failed to auto-save changes')
    }
  })

  // Manual save mutation
  const saveMutation = useMutation({
    mutationFn: () => 
      isNew 
        ? apiClient.post('/api/articles', article)
        : apiClient.put(`/api/articles/${id}`, article),
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
    const timeoutId = setTimeout(() => {
      if (article.title || article.content) {
        setIsAutoSaving(true)
        autoSaveMutation.mutate(article)
      }
    }, 2000)

    return () => clearTimeout(timeoutId)
  }, [article])

  // Load existing article
  useEffect(() => {
    if (existingArticle && !isNew) {
      setArticle(existingArticle)
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

  const handleArticleChange = (updates: Partial<ArticleData>) => {
    setArticle(prev => ({ ...prev, ...updates }))
  }

  const handleSave = () => {
    saveMutation.mutate()
  }

  const handleStatusChange = (status: 'draft' | 'published' | 'scheduled') => {
    setArticle(prev => ({ ...prev, status }))
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="h-8 w-8 animate-spin text-purple-600" />
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-4">
          <button
            onClick={() => navigate('/articles')}
            className="p-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white"
          >
            <ArrowLeft className="h-5 w-5" />
          </button>
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

        <div className="flex items-center gap-3">
          <button
            onClick={handleSave}
            disabled={saveMutation.isPending}
            className="inline-flex items-center px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50"
          >
            {saveMutation.isPending ? (
              <Loader2 className="h-4 w-4 mr-2 animate-spin" />
            ) : (
              <Save className="h-4 w-4 mr-2" />
            )}
            Save
          </button>
        </div>
      </div>

      {/* Tab Navigation */}
      <div className="flex space-x-1 mb-6">
        {[
          { id: 'editor', label: 'Editor', icon: Code },
          { id: 'preview', label: 'Preview', icon: Eye },
          { id: 'seo', label: 'SEO Analysis', icon: TrendingUp },
          { id: 'publish', label: 'Publishing', icon: Settings },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`flex items-center px-4 py-2 rounded-lg font-medium transition-colors ${
              activeTab === tab.id
                ? 'bg-purple-100 dark:bg-purple-900 text-purple-700 dark:text-purple-300'
                : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800'
            }`}
          >
            <tab.icon className="h-4 w-4 mr-2" />
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Main Content Area */}
        <div className="lg:col-span-3">
          {activeTab === 'editor' && (
            <div className="space-y-6">
              {/* Title and Basic Fields */}
              <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Title
                    </label>
                    <input
                      type="text"
                      value={article.title}
                      onChange={(e) => handleArticleChange({ title: e.target.value })}
                      className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                      placeholder="Enter article title..."
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Slug
                    </label>
                    <input
                      type="text"
                      value={article.slug}
                      onChange={(e) => handleArticleChange({ slug: e.target.value })}
                      className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                      placeholder="article-url-slug"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Excerpt
                    </label>
                    <textarea
                      value={article.excerpt}
                      onChange={(e) => handleArticleChange({ excerpt: e.target.value })}
                      rows={3}
                      className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                      placeholder="Brief description of the article..."
                    />
                  </div>
                </div>
              </div>

              {/* Content Editor */}
              <MarkdownEditor
                content={article.content}
                onChange={(content) => handleArticleChange({ content })}
              />
            </div>
          )}

          {activeTab === 'preview' && (
            <ArticlePreview article={article} />
          )}

          {activeTab === 'seo' && (
            <SEOAnalyzer article={article} />
          )}

          {activeTab === 'publish' && (
            <PublishingPanel 
              article={article}
              onStatusChange={handleStatusChange}
              onUpdate={handleArticleChange}
            />
          )}
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Article Status */}
          <div className="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700">
            <h3 className="font-medium text-gray-900 dark:text-white mb-3">Status</h3>
            <div className="space-y-2">
              {['draft', 'published', 'scheduled'].map((status) => (
                <label key={status} className="flex items-center">
                  <input
                    type="radio"
                    name="status"
                    value={status}
                    checked={article.status === status}
                    onChange={(e) => handleStatusChange(e.target.value as any)}
                    className="h-4 w-4 text-purple-600 focus:ring-purple-500 border-gray-300"
                  />
                  <span className="ml-2 text-sm text-gray-700 dark:text-gray-300 capitalize">
                    {status}
                  </span>
                </label>
              ))}
            </div>
          </div>

          {/* Tags */}
          <div className="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700">
            <h3 className="font-medium text-gray-900 dark:text-white mb-3">Tags</h3>
            <input
              type="text"
              value={article.tags.join(', ')}
              onChange={(e) => handleArticleChange({ 
                tags: e.target.value.split(',').map(t => t.trim()).filter(Boolean) 
              })}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent dark:bg-gray-700 dark:text-white text-sm"
              placeholder="tag1, tag2, tag3"
            />
          </div>

          {/* Article Stats */}
          <div className="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700">
            <h3 className="font-medium text-gray-900 dark:text-white mb-3">Statistics</h3>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-600 dark:text-gray-400">Words:</span>
                <span className="text-gray-900 dark:text-white">
                  {article.content.split(/\s+/).length}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600 dark:text-gray-400">Characters:</span>
                <span className="text-gray-900 dark:text-white">
                  {article.content.length}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600 dark:text-gray-400">Read time:</span>
                <span className="text-gray-900 dark:text-white">
                  {Math.ceil(article.content.split(/\s+/).length / 200)} min
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
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
import { 
  TrendingUp, 
  CheckCircle, 
  AlertCircle, 
  XCircle,
  Lightbulb,
  Target,
  Search,
  Link
} from 'lucide-react'

interface SEOAnalysis {
  score: number
  issues: SEOIssue[]
  suggestions: SEOSuggestion[]
  keywordAnalysis: KeywordAnalysis
  readabilityScore: number
  technicalChecks: TechnicalCheck[]
}

interface SEOIssue {
  type: 'error' | 'warning' | 'info'
  category: string
  title: string
  description: string
  fix?: string
}

interface SEOSuggestion {
  title: string
  description: string
  impact: 'high' | 'medium' | 'low'
}

interface KeywordAnalysis {
  primary: string
  density: number
  secondary: string[]
  related: string[]
  missingKeywords: string[]
}

interface TechnicalCheck {
  name: string
  status: 'passed' | 'failed' | 'warning'
  description: string
}

interface SEOAnalyzerProps {
  article: {
    title: string
    content: string
    metaTitle: string
    metaDescription: string
    slug: string
  }
}

export function SEOAnalyzer({ article }: SEOAnalyzerProps) {
  const [analysis, setAnalysis] = useState<SEOAnalysis | null>(null)
  const [targetKeyword, setTargetKeyword] = useState('')

  const analyzeMutation = useMutation({
    mutationFn: (data: { article: any, targetKeyword?: string }) =>
      apiClient.post<SEOAnalysis>('/api/seo/analyze', data),
    onSuccess: (data) => {
      setAnalysis(data)
    }
  })

  useEffect(() => {
    if (article.title && article.content) {
      analyzeMutation.mutate({ article, targetKeyword })
    }
  }, [article.title, article.content, article.metaTitle, article.metaDescription])

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

  const getIssueIcon = (type: string) => {
    switch (type) {
      case 'error':
        return <XCircle className="h-4 w-4 text-red-500" />
      case 'warning':
        return <AlertCircle className="h-4 w-4 text-yellow-500" />
      default:
        return <CheckCircle className="h-4 w-4 text-blue-500" />
    }
  }

  return (
    <div className="space-y-6">
      {/* Target Keyword */}
      <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          Target Keyword Analysis
        </h3>
        <div className="flex items-center gap-4">
          <div className="flex-1">
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Primary Keyword
            </label>
            <input
              type="text"
              value={targetKeyword}
              onChange={(e) => setTargetKeyword(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
              placeholder="service dog training"
            />
          </div>
          <button
            onClick={() => analyzeMutation.mutate({ article, targetKeyword })}
            disabled={analyzeMutation.isPending}
            className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50"
          >
            <Search className="h-4 w-4" />
          </button>
        </div>
      </div>

      {analysis && (
        <>
          {/* SEO Score */}
          <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                SEO Score
              </h3>
              <div className={`flex items-center px-4 py-2 rounded-lg ${getScoreBg(analysis.score)}`}>
                <TrendingUp className={`h-5 w-5 mr-2 ${getScoreColor(analysis.score)}`} />
                <span className={`text-2xl font-bold ${getScoreColor(analysis.score)}`}>
                  {analysis.score}/100
                </span>
              </div>
            </div>

            {/* Score Breakdown */}
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
                  {analysis.technicalChecks.filter(c => c.status === 'passed').length}
                </div>
                <div className="text-sm text-gray-600 dark:text-gray-400">
                  Checks Passed
                </div>
              </div>
            </div>
          </div>

          {/* Issues */}
          {analysis.issues.length > 0 && (
            <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                Issues to Fix
              </h3>
              <div className="space-y-4">
                {analysis.issues.map((issue, index) => (
                  <div key={index} className="flex items-start gap-3 p-4 bg-gray-50 dark:bg-gray-900 rounded-lg">
                    {getIssueIcon(issue.type)}
                    <div className="flex-1">
                      <h4 className="font-medium text-gray-900 dark:text-white">
                        {issue.title}
                      </h4>
                      <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                        {issue.description}
                      </p>
                      {issue.fix && (
                        <p className="text-sm text-purple-600 dark:text-purple-400 mt-2">
                          💡 {issue.fix}
                        </p>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Suggestions */}
          {analysis.suggestions.length > 0 && (
            <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                Optimization Suggestions
              </h3>
              <div className="space-y-3">
                {analysis.suggestions.map((suggestion, index) => (
                  <div key={index} className="flex items-start gap-3">
                    <Lightbulb className="h-4 w-4 text-yellow-500 mt-1 flex-shrink-0" />
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <h4 className="font-medium text-gray-900 dark:text-white">
                          {suggestion.title}
                        </h4>
                        <span className={`text-xs px-2 py-1 rounded-full ${
                          suggestion.impact === 'high' 
                            ? 'bg-red-100 text-red-700 dark:bg-red-900/20 dark:text-red-400'
                            : suggestion.impact === 'medium'
                            ? 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/20 dark:text-yellow-400'
                            : 'bg-green-100 text-green-700 dark:bg-green-900/20 dark:text-green-400'
                        }`}>
                          {suggestion.impact} impact
                        </span>
                      </div>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        {suggestion.description}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Technical Checks */}
          <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Technical SEO Checks
            </h3>
            <div className="space-y-3">
              {analysis.technicalChecks.map((check, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-900 rounded-lg">
                  <div className="flex items-center gap-3">
                    {check.status === 'passed' && <CheckCircle className="h-4 w-4 text-green-500" />}
                    {check.status === 'warning' && <AlertCircle className="h-4 w-4 text-yellow-500" />}
                    {check.status === 'failed' && <XCircle className="h-4 w-4 text-red-500" />}
                    <div>
                      <p className="font-medium text-gray-900 dark:text-white">
                        {check.name}
                      </p>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        {check.description}
                      </p>
                    </div>
                  </div>
                  <span className={`text-sm font-medium capitalize ${
                    check.status === 'passed' ? 'text-green-600' :
                    check.status === 'warning' ? 'text-yellow-600' :
                    'text-red-600'
                  }`}>
                    {check.status}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Keyword Analysis */}
          <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Keyword Analysis
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h4 className="font-medium text-gray-900 dark:text-white mb-3">
                  Secondary Keywords
                </h4>
                <div className="flex flex-wrap gap-2">
                  {analysis.keywordAnalysis.secondary.map((keyword, index) => (
                    <span
                      key={index}
                      className="px-3 py-1 bg-blue-100 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300 text-sm rounded-full"
                    >
                      {keyword}
                    </span>
                  ))}
                </div>
              </div>
              
              <div>
                <h4 className="font-medium text-gray-900 dark:text-white mb-3">
                  Missing Keywords
                </h4>
                <div className="flex flex-wrap gap-2">
                  {analysis.keywordAnalysis.missingKeywords.map((keyword, index) => (
                    <span
                      key={index}
                      className="px-3 py-1 bg-red-100 dark:bg-red-900/20 text-red-700 dark:text-red-300 text-sm rounded-full"
                    >
                      {keyword}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  )
}
```

**Success Criteria:**
- Complete article CRUD with rich text markdown editor
- Real-time SEO analysis and optimization suggestions
- WordPress publishing integration with multiple site support
- Article scheduling and status management
- Performance tracking with engagement metrics
- Responsive design with grid and list view modes
- Auto-save functionality with manual save override
- Tag management and article categorization
- Live preview with proper formatting
- Integration with existing authentication and API systems

This article management system provides comprehensive content lifecycle management for the Blog-Poster platform, enabling efficient creation, optimization, and publishing of SEO-focused articles.
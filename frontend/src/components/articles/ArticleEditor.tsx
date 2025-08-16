import { useState, useEffect } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useNavigate, useParams } from 'react-router-dom'
import { supabase } from '@/integrations/supabase/client'
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
  Loader2
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
    keywords: [] as string[],
    featured_image: null as string | null,
    scheduled_for: null as string | null,
  })

  const [activeTab, setActiveTab] = useState<'editor' | 'preview' | 'seo' | 'settings'>('editor')
  const [isAutoSaving, setIsAutoSaving] = useState(false)
  const [lastSaved, setLastSaved] = useState<Date | null>(null)

  // Load article from Supabase if editing
  const { data: existingArticle, isLoading, error: articleError } = useQuery({
    queryKey: ['article', id],
    queryFn: async () => {
      const { data, error } = await supabase
        .from('articles')
        .select('*')
        .eq('id', id)
        .eq('organization_id', organization!.id)
        .maybeSingle()

      if (error) throw error
      return data
    },
    enabled: !isNew && !!organization?.id,
  })

  // Save article to Supabase
  const saveMutation = useMutation({
    mutationFn: async (articleData: any) => {
      const wordCount = articleData.content.split(/\s+/).filter(Boolean).length
      const readingTime = Math.ceil(wordCount / 200)

      const payload = {
        ...articleData,
        word_count: wordCount,
        reading_time: readingTime,
        organization_id: organization!.id,
        user_id: user!.id,
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
      saveMutation.mutate(article)
      setTimeout(() => setIsAutoSaving(false), 500)
    }, 3000)

    return () => clearTimeout(timeoutId)
  }, [article])

  // Load existing article
  useEffect(() => {
    if (existingArticle && !isNew) {
      // Ensure status is one of the valid types
      const validStatus = ['draft', 'published', 'scheduled'].includes(existingArticle.status) 
        ? existingArticle.status as 'draft' | 'published' | 'scheduled'
        : 'draft'
      
      setArticle({
        title: existingArticle.title || '',
        slug: existingArticle.slug || '',
        excerpt: existingArticle.excerpt || '',
        content: existingArticle.content || '',
        meta_title: existingArticle.meta_title || '',
        meta_description: existingArticle.meta_description || '',
        status: validStatus,
        keywords: existingArticle.keywords || [],
        featured_image: existingArticle.featured_image,
        scheduled_for: existingArticle.scheduled_for,
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
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    )
  }

  if (articleError || (!isNew && existingArticle === null)) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-foreground mb-4">Article Not Found</h1>
          <p className="text-muted-foreground mb-6">
            The article you're looking for doesn't exist or you don't have permission to view it.
          </p>
          <Button onClick={() => navigate('/articles')}>
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Articles
          </Button>
        </div>
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
            <h1 className="text-2xl font-bold text-foreground">
              {isNew ? 'New Article' : 'Edit Article'}
            </h1>
            {lastSaved && (
              <p className="text-sm text-muted-foreground">
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
                  <p className="text-sm text-muted-foreground mt-1">
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
                  <p className="text-sm text-muted-foreground mt-1">
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
                          onChange={(e) => {
                            const newStatus = e.target.value as 'draft' | 'published' | 'scheduled'
                            handleArticleChange({ status: newStatus })
                          }}
                          className="mr-2"
                        />
                        <span className="capitalize">{status}</span>
                      </label>
                    ))}
                  </div>
                </div>

                {article.status === 'scheduled' && (
                  <div>
                    <Label htmlFor="scheduled_for">Schedule Date</Label>
                    <Input
                      id="scheduled_for"
                      type="datetime-local"
                      value={article.scheduled_for || ''}
                      onChange={(e) => handleArticleChange({ scheduled_for: e.target.value })}
                    />
                  </div>
                )}

                <div>
                  <Label htmlFor="keywords">Keywords</Label>
                  <Input
                    id="keywords"
                    value={article.keywords.join(', ')}
                    onChange={(e) => handleArticleChange({ 
                      keywords: e.target.value.split(',').map(t => t.trim()).filter(Boolean) 
                    })}
                    placeholder="keyword1, keyword2, keyword3"
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
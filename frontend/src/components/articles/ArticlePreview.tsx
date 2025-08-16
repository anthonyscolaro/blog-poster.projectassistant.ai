import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Calendar, Clock, TrendingUp } from 'lucide-react'

interface ArticlePreviewProps {
  article: {
    title: string
    excerpt: string
    content: string
    meta_title: string
    meta_description: string
    status: string
    keywords: string[]
  }
}

export function ArticlePreview({ article }: ArticlePreviewProps) {
  const formatContent = (text: string) => {
    // Simple markdown to HTML conversion
    return text
      .replace(/^### (.*$)/gim, '<h3 class="text-xl font-semibold mt-6 mb-3">$1</h3>')
      .replace(/^## (.*$)/gim, '<h2 class="text-2xl font-semibold mt-8 mb-4">$1</h2>')
      .replace(/^# (.*$)/gim, '<h1 class="text-3xl font-bold mt-8 mb-6">$1</h1>')
      .replace(/\*\*(.*?)\*\*/gim, '<strong class="font-semibold">$1</strong>')
      .replace(/\*(.*?)\*/gim, '<em class="italic">$1</em>')
      .replace(/\[([^\]]*)\]\(([^\)]*)\)/gim, '<a href="$2" class="text-primary hover:underline">$1</a>')
      .replace(/^- (.*$)/gim, '<li class="ml-4">$1</li>')
      .replace(/^> (.*$)/gim, '<blockquote class="border-l-4 border-accent pl-4 italic my-4">$1</blockquote>')
      .replace(/`([^`]*)`/gim, '<code class="bg-accent px-1 py-0.5 rounded text-sm">$1</code>')
      .replace(/\n\n/gim, '</p><p class="mb-4">')
      .replace(/\n/gim, '<br>')
  }

  const wordCount = article.content.split(/\s+/).filter(Boolean).length
  const readingTime = Math.ceil(wordCount / 200)

  return (
    <div className="space-y-6">
      {/* Article Meta */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle>Article Preview</CardTitle>
            <Badge variant="outline">{article.status}</Badge>
          </div>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-3 gap-4 text-sm">
            <div className="flex items-center gap-2">
              <Clock className="h-4 w-4 text-muted-foreground" />
              <span>{readingTime} min read</span>
            </div>
            <div className="flex items-center gap-2">
              <TrendingUp className="h-4 w-4 text-muted-foreground" />
              <span>{wordCount} words</span>
            </div>
            <div className="flex items-center gap-2">
              <Calendar className="h-4 w-4 text-muted-foreground" />
              <span>Draft</span>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* SEO Preview */}
      <Card>
        <CardHeader>
          <CardTitle>SEO Preview</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <h3 className="text-sm font-medium text-muted-foreground mb-2">Search Result Preview</h3>
              <div className="border border-border rounded-lg p-4 bg-background">
                <h4 className="text-blue-600 text-lg font-medium hover:underline cursor-pointer">
                  {article.meta_title || article.title}
                </h4>
                <p className="text-green-600 text-sm mt-1">example.com/articles/your-slug</p>
                <p className="text-gray-600 dark:text-gray-400 text-sm mt-2">
                  {article.meta_description || article.excerpt}
                </p>
              </div>
            </div>
            
            {article.keywords.length > 0 && (
              <div>
                <h3 className="text-sm font-medium text-muted-foreground mb-2">Keywords</h3>
                <div className="flex flex-wrap gap-2">
                  {article.keywords.map((keyword, index) => (
                    <Badge key={index} variant="secondary">
                      {keyword}
                    </Badge>
                  ))}
                </div>
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Article Content */}
      <Card>
        <CardHeader>
          <CardTitle>{article.title || 'Untitled Article'}</CardTitle>
          {article.excerpt && (
            <p className="text-muted-foreground">{article.excerpt}</p>
          )}
        </CardHeader>
        <CardContent>
          <div 
            className="prose prose-sm max-w-none dark:prose-invert"
            dangerouslySetInnerHTML={{ 
              __html: `<p class="mb-4">${formatContent(article.content)}</p>` 
            }}
          />
          {!article.content && (
            <p className="text-muted-foreground italic">No content yet...</p>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { FileText, ExternalLink, Clock, TrendingUp } from 'lucide-react'

interface Article {
  id: string
  title: string
  slug: string
  status: 'draft' | 'published' | 'scheduled'
  seoScore: number
  generationCost: number
  wordCount: number
  createdAt: string
  publishedAt: string | null
}

// Mock data for now
const mockArticles: Article[] = [
  {
    id: '1',
    title: 'AI Content Strategy 2024: Complete Guide',
    slug: 'ai-content-strategy-2024',
    status: 'published',
    seoScore: 94,
    generationCost: 3.20,
    wordCount: 2400,
    createdAt: new Date(Date.now() - 1000 * 60 * 60 * 2).toISOString(),
    publishedAt: new Date(Date.now() - 1000 * 60 * 60 * 1).toISOString(),
  },
  {
    id: '2',
    title: 'WordPress SEO Best Practices for 2024',
    slug: 'wordpress-seo-best-practices',
    status: 'published',
    seoScore: 87,
    generationCost: 2.80,
    wordCount: 1800,
    createdAt: new Date(Date.now() - 1000 * 60 * 60 * 4).toISOString(),
    publishedAt: new Date(Date.now() - 1000 * 60 * 60 * 3).toISOString(),
  },
  {
    id: '3',
    title: 'Content Marketing Automation Tools',
    slug: 'content-marketing-automation-tools',
    status: 'scheduled',
    seoScore: 91,
    generationCost: 2.45,
    wordCount: 2100,
    createdAt: new Date(Date.now() - 1000 * 60 * 60 * 6).toISOString(),
    publishedAt: null,
  },
  {
    id: '4',
    title: 'Advanced SEO Techniques for Blog Posts',
    slug: 'advanced-seo-techniques',
    status: 'draft',
    seoScore: 76,
    generationCost: 1.90,
    wordCount: 1500,
    createdAt: new Date(Date.now() - 1000 * 60 * 60 * 8).toISOString(),
    publishedAt: null,
  }
]

export function RecentArticles() {
  const { data: articles, isLoading } = useQuery({
    queryKey: ['recent-articles'],
    queryFn: async () => {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 500))
      return mockArticles
    },
  })

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'published':
        return 'bg-green-100 text-green-700 dark:bg-green-900/20 dark:text-green-400'
      case 'scheduled':
        return 'bg-blue-100 text-blue-700 dark:bg-blue-900/20 dark:text-blue-400'
      default:
        return 'bg-gray-100 text-gray-700 dark:bg-gray-900/20 dark:text-gray-400'
    }
  }

  const getSeoScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600 dark:text-green-400'
    if (score >= 60) return 'text-yellow-600 dark:text-yellow-400'
    return 'text-red-600 dark:text-red-400'
  }

  return (
    <div className="bg-card rounded-xl p-6 shadow-sm border">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <FileText className="h-5 w-5 text-purple-600 dark:text-purple-400" />
          <h2 className="text-lg font-semibold text-foreground">
            Recent Articles
          </h2>
        </div>
        <Link
          to="/articles"
          className="text-sm text-purple-600 hover:text-purple-700 dark:text-purple-400 font-medium"
        >
          View all →
        </Link>
      </div>

      <div className="space-y-4">
        {articles?.map((article) => (
          <div
            key={article.id}
            className="p-4 bg-muted/50 rounded-lg hover:bg-muted/70 transition-colors"
          >
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-2">
                  <Link
                    to={`/articles/${article.id}`}
                    className="font-medium text-foreground hover:text-purple-600 dark:hover:text-purple-400"
                  >
                    {article.title}
                  </Link>
                  <ExternalLink className="h-3 w-3 text-muted-foreground" />
                </div>
                
                <div className="flex items-center gap-4 text-sm text-muted-foreground">
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(article.status)}`}>
                    {article.status}
                  </span>
                  <div className="flex items-center gap-1">
                    <TrendingUp className="h-3 w-3" />
                    <span className={`font-medium ${getSeoScoreColor(article.seoScore)}`}>
                      {article.seoScore}/100
                    </span>
                  </div>
                  <div className="flex items-center gap-1">
                    <Clock className="h-3 w-3" />
                    <span>{article.wordCount} words</span>
                  </div>
                  <span>${article.generationCost.toFixed(2)}</span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {(!articles || articles.length === 0) && !isLoading && (
        <div className="text-center py-8">
          <FileText className="h-12 w-12 text-muted-foreground mx-auto mb-3" />
          <p className="text-muted-foreground">No articles yet</p>
          <Link
            to="/pipeline"
            className="mt-4 inline-flex items-center px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700"
          >
            Generate First Article
          </Link>
        </div>
      )}
    </div>
  )
}
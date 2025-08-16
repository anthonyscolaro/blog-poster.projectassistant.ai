import { Link } from 'react-router-dom'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardFooter, CardHeader } from '@/components/ui/card'
import { 
  MoreHorizontal, 
  Edit, 
  Trash2, 
  Calendar,
  TrendingUp,
  Clock,
  User,
  ExternalLink
} from 'lucide-react'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'

interface Article {
  id: string
  title: string
  excerpt: string
  status: 'draft' | 'published' | 'scheduled' | 'archived'
  seo_score: number
  word_count: number
  reading_time: number
  published_at: string | null
  scheduled_for: string | null
  created_at: string
  wordpress_url: string | null
}

interface ArticleCardProps {
  article: Article
  viewMode: 'grid' | 'list'
  onDelete: () => void
}

export function ArticleCard({ article, viewMode, onDelete }: ArticleCardProps) {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'published':
        return 'bg-green-500/10 text-green-700 dark:text-green-400'
      case 'scheduled':
        return 'bg-blue-500/10 text-blue-700 dark:text-blue-400'
      case 'draft':
        return 'bg-gray-500/10 text-gray-700 dark:text-gray-400'
      default:
        return 'bg-yellow-500/10 text-yellow-700 dark:text-yellow-400'
    }
  }

  const getSeoScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600 dark:text-green-400'
    if (score >= 60) return 'text-yellow-600 dark:text-yellow-400'
    return 'text-red-600 dark:text-red-400'
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    })
  }

  if (viewMode === 'list') {
    return (
      <Card className="hover:shadow-md transition-shadow">
        <CardContent className="p-6">
          <div className="flex items-start justify-between">
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-3 mb-2">
                <Badge className={getStatusColor(article.status)}>
                  {article.status}
                </Badge>
                <div className="flex items-center gap-1 text-sm text-muted-foreground">
                  <TrendingUp className="h-4 w-4" />
                  <span className={getSeoScoreColor(article.seo_score)}>
                    {article.seo_score}/100
                  </span>
                </div>
                <div className="flex items-center gap-1 text-sm text-muted-foreground">
                  <Clock className="h-4 w-4" />
                  {article.reading_time} min read
                </div>
              </div>
              
              <Link 
                to={`/articles/${article.id}`}
                className="block group"
              >
                <h3 className="text-lg font-semibold text-foreground group-hover:text-primary transition-colors mb-2 truncate">
                  {article.title}
                </h3>
                <p className="text-muted-foreground text-sm line-clamp-2">
                  {article.excerpt}
                </p>
              </Link>
              
              <div className="flex items-center gap-4 mt-3 text-xs text-muted-foreground">
                <span>{article.word_count} words</span>
                <span>Created {formatDate(article.created_at)}</span>
                {article.published_at && (
                  <span>Published {formatDate(article.published_at)}</span>
                )}
              </div>
            </div>
            
            <div className="flex items-center gap-2 ml-4">
              {article.wordpress_url && (
                <Button size="sm" variant="ghost" asChild>
                  <a href={article.wordpress_url} target="_blank" rel="noopener noreferrer">
                    <ExternalLink className="h-4 w-4" />
                  </a>
                </Button>
              )}
              
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button size="sm" variant="ghost">
                    <MoreHorizontal className="h-4 w-4" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end">
                  <DropdownMenuItem asChild>
                    <Link to={`/articles/${article.id}`}>
                      <Edit className="h-4 w-4 mr-2" />
                      Edit
                    </Link>
                  </DropdownMenuItem>
                  <DropdownMenuItem 
                    onClick={onDelete}
                    className="text-destructive focus:text-destructive"
                  >
                    <Trash2 className="h-4 w-4 mr-2" />
                    Delete
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </div>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between">
          <Badge className={getStatusColor(article.status)}>
            {article.status}
          </Badge>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button size="sm" variant="ghost">
                <MoreHorizontal className="h-4 w-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuItem asChild>
                <Link to={`/articles/${article.id}`}>
                  <Edit className="h-4 w-4 mr-2" />
                  Edit
                </Link>
              </DropdownMenuItem>
              <DropdownMenuItem 
                onClick={onDelete}
                className="text-destructive focus:text-destructive"
              >
                <Trash2 className="h-4 w-4 mr-2" />
                Delete
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </CardHeader>
      
      <CardContent className="pb-4">
        <Link 
          to={`/articles/${article.id}`}
          className="block group"
        >
          <h3 className="text-lg font-semibold text-foreground group-hover:text-primary transition-colors mb-2 line-clamp-2">
            {article.title}
          </h3>
          <p className="text-muted-foreground text-sm line-clamp-3 mb-4">
            {article.excerpt}
          </p>
        </Link>
        
        <div className="flex items-center justify-between text-sm">
          <div className="flex items-center gap-1">
            <TrendingUp className="h-4 w-4" />
            <span className={getSeoScoreColor(article.seo_score)}>
              {article.seo_score}/100
            </span>
          </div>
          
          <div className="flex items-center gap-1 text-muted-foreground">
            <Clock className="h-4 w-4" />
            {article.reading_time} min
          </div>
        </div>
      </CardContent>
      
      <CardFooter className="pt-0 text-xs text-muted-foreground">
        <div className="flex items-center justify-between w-full">
          <span>{article.word_count} words</span>
          <span>{formatDate(article.created_at)}</span>
        </div>
      </CardFooter>
    </Card>
  )
}
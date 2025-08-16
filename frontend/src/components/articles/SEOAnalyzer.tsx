import { useState, useEffect } from 'react'
import { useMutation } from '@tanstack/react-query'
import apiService from '@/services/api'
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
      return await apiService.analyzeSEO({ content: article.content, target_keyword: targetKeyword })
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
    if (score >= 80) return 'text-green-600 dark:text-green-400'
    if (score >= 60) return 'text-yellow-600 dark:text-yellow-400'
    return 'text-red-600 dark:text-red-400'
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
          <Loader2 className="h-8 w-8 animate-spin text-primary" />
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
                  <div className="text-2xl font-bold text-foreground">
                    {analysis.keywordAnalysis.density.toFixed(1)}%
                  </div>
                  <div className="text-sm text-muted-foreground">
                    Keyword Density
                  </div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-foreground">
                    {analysis.readabilityScore}
                  </div>
                  <div className="text-sm text-muted-foreground">
                    Readability
                  </div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-foreground">
                    {analysis.technicalChecks.filter(c => c.status === 'passed').length}/{analysis.technicalChecks.length}
                  </div>
                  <div className="text-sm text-muted-foreground">
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
                      <p className="text-sm text-muted-foreground">
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
                <div key={index} className="flex items-center justify-between p-3 bg-accent/50 rounded-lg">
                  <div className="flex items-center gap-3">
                    {check.status === 'passed' && <CheckCircle className="h-4 w-4 text-green-500" />}
                    {check.status === 'warning' && <AlertCircle className="h-4 w-4 text-yellow-500" />}
                    {check.status === 'failed' && <XCircle className="h-4 w-4 text-red-500" />}
                    <div>
                      <p className="font-medium">{check.name}</p>
                      <p className="text-sm text-muted-foreground">
                        {check.description}
                      </p>
                    </div>
                  </div>
                  <Badge variant={
                    check.status === 'passed' ? 'default' :
                    check.status === 'warning' ? 'secondary' :
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
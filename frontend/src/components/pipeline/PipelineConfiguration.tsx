import { useState } from 'react'
import { supabase } from '@/services/supabase'
import { useAuth } from '@/contexts/AuthContext'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Switch } from '@/components/ui/switch'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Badge } from '@/components/ui/badge'
import { Loader2, AlertCircle, Plus, X } from 'lucide-react'
import { toast } from 'react-hot-toast'

interface PipelineConfigurationProps {
  onStart: (config: any) => void
  isStarting: boolean
  disabled?: boolean
  organizationId?: string
}

export function PipelineConfiguration({ 
  onStart, 
  isStarting, 
  disabled,
  organizationId 
}: PipelineConfigurationProps) {
  const { user } = useAuth()
  const [config, setConfig] = useState({
    topic: '',
    targetKeywords: [] as string[],
    competitorUrls: [] as string[],
    wordCountMin: 1500,
    wordCountMax: 2500,
    seoOptimization: true,
    legalReview: true,
    autoPublish: false,
    budgetLimit: 5.00
  })
  const [keywordInput, setKeywordInput] = useState('')
  const [urlInput, setUrlInput] = useState('')

  const handleAddKeyword = () => {
    if (keywordInput.trim() && !config.targetKeywords.includes(keywordInput.trim())) {
      setConfig(prev => ({
        ...prev,
        targetKeywords: [...prev.targetKeywords, keywordInput.trim()]
      }))
      setKeywordInput('')
    }
  }

  const handleRemoveKeyword = (index: number) => {
    setConfig(prev => ({
      ...prev,
      targetKeywords: prev.targetKeywords.filter((_, i) => i !== index)
    }))
  }

  const handleAddUrl = () => {
    if (urlInput.trim() && !config.competitorUrls.includes(urlInput.trim())) {
      setConfig(prev => ({
        ...prev,
        competitorUrls: [...prev.competitorUrls, urlInput.trim()]
      }))
      setUrlInput('')
    }
  }

  const handleRemoveUrl = (index: number) => {
    setConfig(prev => ({
      ...prev,
      competitorUrls: prev.competitorUrls.filter((_, i) => i !== index)
    }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!config.topic) {
      toast.error('Please enter a topic')
      return
    }

    if (config.targetKeywords.length === 0) {
      toast.error('Please add at least one target keyword')
      return
    }

    onStart(config)
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Pipeline Configuration</CardTitle>
        <CardDescription>
          Configure your content generation pipeline settings
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Topic Input */}
          <div className="space-y-2">
            <Label htmlFor="topic">Content Topic *</Label>
            <Input
              id="topic"
              value={config.topic}
              onChange={(e) => setConfig(prev => ({ ...prev, topic: e.target.value }))}
              placeholder="e.g., Service Dog Training Tips"
              disabled={disabled || isStarting}
            />
          </div>

          {/* Target Keywords */}
          <div className="space-y-2">
            <Label>Target Keywords *</Label>
            <div className="flex gap-2">
              <Input
                value={keywordInput}
                onChange={(e) => setKeywordInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), handleAddKeyword())}
                placeholder="Add a keyword"
                disabled={disabled || isStarting}
              />
              <Button 
                type="button" 
                onClick={handleAddKeyword}
                disabled={disabled || isStarting}
                size="sm"
              >
                <Plus className="h-4 w-4" />
              </Button>
            </div>
            <div className="flex flex-wrap gap-2 mt-2">
              {config.targetKeywords.map((keyword, index) => (
                <Badge key={index} variant="secondary" className="flex items-center gap-1">
                  {keyword}
                  <button
                    type="button"
                    onClick={() => handleRemoveKeyword(index)}
                    className="ml-1 hover:text-destructive"
                    disabled={disabled || isStarting}
                  >
                    <X className="h-3 w-3" />
                  </button>
                </Badge>
              ))}
            </div>
          </div>

          {/* Competitor URLs */}
          <div className="space-y-2">
            <Label>Competitor URLs (Optional)</Label>
            <div className="flex gap-2">
              <Input
                value={urlInput}
                onChange={(e) => setUrlInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), handleAddUrl())}
                placeholder="https://competitor.com/article"
                disabled={disabled || isStarting}
              />
              <Button 
                type="button" 
                onClick={handleAddUrl}
                disabled={disabled || isStarting}
                size="sm"
              >
                <Plus className="h-4 w-4" />
              </Button>
            </div>
            <div className="space-y-1 mt-2">
              {config.competitorUrls.map((url, index) => (
                <div key={index} className="flex items-center gap-2 text-sm p-2 bg-muted rounded">
                  <span className="text-muted-foreground truncate flex-1">{url}</span>
                  <button
                    type="button"
                    onClick={() => handleRemoveUrl(index)}
                    className="text-destructive hover:text-destructive/80"
                    disabled={disabled || isStarting}
                  >
                    <X className="h-4 w-4" />
                  </button>
                </div>
              ))}
            </div>
          </div>

          {/* Word Count */}
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="wordCountMin">Min Word Count</Label>
              <Input
                id="wordCountMin"
                type="number"
                value={config.wordCountMin}
                onChange={(e) => setConfig(prev => ({ 
                  ...prev, 
                  wordCountMin: parseInt(e.target.value) || 0 
                }))}
                disabled={disabled || isStarting}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="wordCountMax">Max Word Count</Label>
              <Input
                id="wordCountMax"
                type="number"
                value={config.wordCountMax}
                onChange={(e) => setConfig(prev => ({ 
                  ...prev, 
                  wordCountMax: parseInt(e.target.value) || 0 
                }))}
                disabled={disabled || isStarting}
              />
            </div>
          </div>

          {/* Options */}
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <Label htmlFor="seo">SEO Optimization</Label>
              <Switch
                id="seo"
                checked={config.seoOptimization}
                onCheckedChange={(checked) => setConfig(prev => ({ 
                  ...prev, 
                  seoOptimization: checked 
                }))}
                disabled={disabled || isStarting}
              />
            </div>
            <div className="flex items-center justify-between">
              <Label htmlFor="legal">Legal Review</Label>
              <Switch
                id="legal"
                checked={config.legalReview}
                onCheckedChange={(checked) => setConfig(prev => ({ 
                  ...prev, 
                  legalReview: checked 
                }))}
                disabled={disabled || isStarting}
              />
            </div>
            <div className="flex items-center justify-between">
              <Label htmlFor="autoPublish">Auto-Publish</Label>
              <Switch
                id="autoPublish"
                checked={config.autoPublish}
                onCheckedChange={(checked) => setConfig(prev => ({ 
                  ...prev, 
                  autoPublish: checked 
                }))}
                disabled={disabled || isStarting}
              />
            </div>
          </div>

          {/* Budget Limit */}
          <div className="space-y-2">
            <Label htmlFor="budget">Budget Limit ($)</Label>
            <Input
              id="budget"
              type="number"
              step="0.01"
              value={config.budgetLimit}
              onChange={(e) => setConfig(prev => ({ 
                ...prev, 
                budgetLimit: parseFloat(e.target.value) || 0 
              }))}
              disabled={disabled || isStarting}
            />
            <p className="text-sm text-muted-foreground">
              Estimated cost will be calculated based on configuration
            </p>
          </div>

          {/* Submit Button */}
          <Button
            type="submit"
            className="w-full"
            disabled={disabled || isStarting}
          >
            {isStarting && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
            {isStarting ? 'Starting Pipeline...' : 'Start Pipeline'}
          </Button>
        </form>
      </CardContent>
    </Card>
  )
}
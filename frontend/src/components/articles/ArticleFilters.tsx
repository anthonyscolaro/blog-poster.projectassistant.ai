import { Card, CardContent } from '@/components/ui/card'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Slider } from '@/components/ui/slider'

interface ArticleFiltersProps {
  filters: {
    status?: string
    seoScoreMin?: number
  }
  onChange: (filters: any) => void
}

export function ArticleFilters({ filters, onChange }: ArticleFiltersProps) {
  return (
    <Card>
      <CardContent className="pt-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <Label htmlFor="status-filter">Status</Label>
            <Select
              value={filters.status || ''}
              onValueChange={(value) => onChange({ status: value || undefined })}
            >
              <SelectTrigger>
                <SelectValue placeholder="All statuses" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="">All statuses</SelectItem>
                <SelectItem value="draft">Draft</SelectItem>
                <SelectItem value="published">Published</SelectItem>
                <SelectItem value="scheduled">Scheduled</SelectItem>
                <SelectItem value="archived">Archived</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div>
            <Label>Minimum SEO Score: {filters.seoScoreMin || 0}</Label>
            <div className="mt-2">
              <Slider
                value={[filters.seoScoreMin || 0]}
                onValueChange={([value]) => onChange({ seoScoreMin: value })}
                max={100}
                step={10}
                className="w-full"
              />
            </div>
          </div>

          <div className="flex items-end">
            <button
              onClick={() => onChange({ status: undefined, seoScoreMin: undefined })}
              className="text-sm text-muted-foreground hover:text-foreground transition-colors"
            >
              Clear filters
            </button>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
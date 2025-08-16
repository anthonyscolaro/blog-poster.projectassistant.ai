import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { TrendingUp, TrendingDown, ArrowRight } from 'lucide-react'

interface AdminMetricsCardProps {
  title: string
  value: string | React.ReactNode
  description: string
  icon: React.ReactNode
  details: string[]
  actionLabel: string
  trend?: number
  onClick?: () => void
}

export function AdminMetricsCard({
  title,
  value,
  description,
  icon,
  details,
  actionLabel,
  trend,
  onClick
}: AdminMetricsCardProps) {
  const getTrendColor = (trend: number) => {
    if (trend > 0) return 'text-green-600'
    if (trend < 0) return 'text-red-600'
    return 'text-muted-foreground'
  }

  const getTrendIcon = (trend: number) => {
    if (trend > 0) return <TrendingUp className="h-3 w-3" />
    if (trend < 0) return <TrendingDown className="h-3 w-3" />
    return null
  }

  return (
    <Card className="transition-all hover:shadow-md">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium flex items-center gap-2">
          {icon}
          {title}
        </CardTitle>
        {trend !== undefined && (
          <Badge variant="outline" className={`${getTrendColor(trend)} border-current`}>
            {getTrendIcon(trend)}
            {Math.abs(trend)}%
          </Badge>
        )}
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          <div>
            <div className="text-2xl font-bold">
              {typeof value === 'string' ? value : value}
            </div>
            <p className="text-xs text-muted-foreground">
              {description}
            </p>
          </div>
          
          <div className="space-y-1">
            {details.map((detail, index) => (
              <p key={index} className="text-xs text-muted-foreground">
                • {detail}
              </p>
            ))}
          </div>
          
          <Button 
            variant="ghost" 
            size="sm" 
            className="w-full justify-between p-2 h-8"
            onClick={onClick}
          >
            <span className="text-xs">{actionLabel}</span>
            <ArrowRight className="h-3 w-3" />
          </Button>
        </div>
      </CardContent>
    </Card>
  )
}
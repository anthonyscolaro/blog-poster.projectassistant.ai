import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { Badge } from '@/components/ui/badge'
import { 
  FileText, 
  UserPlus, 
  Settings, 
  Trash2, 
  Edit, 
  Eye, 
  MessageCircle,
  CheckCircle,
  Clock,
  AlertCircle
} from 'lucide-react'

interface ActivityTimelineProps {
  activities: Array<{
    id: string
    action: string
    resource_type: string | null
    details: any
    created_at: string
    profiles?: {
      full_name: string | null
      avatar_url: string | null
    } | null
  }>
  limit?: number
}

export function ActivityTimeline({ activities, limit }: ActivityTimelineProps) {
  const displayedActivities = limit ? activities.slice(0, limit) : activities

  const getActionIcon = (action: string, resourceType: string | null) => {
    if (action.includes('create')) return FileText
    if (action.includes('invite') || action.includes('join')) return UserPlus
    if (action.includes('update') || action.includes('edit')) return Edit
    if (action.includes('delete') || action.includes('remove')) return Trash2
    if (action.includes('publish')) return CheckCircle
    if (action.includes('view')) return Eye
    if (action.includes('comment')) return MessageCircle
    if (action.includes('settings')) return Settings
    return AlertCircle
  }

  const getActionColor = (action: string) => {
    if (action.includes('create') || action.includes('publish')) return 'text-green-600'
    if (action.includes('update') || action.includes('edit')) return 'text-blue-600'
    if (action.includes('delete') || action.includes('remove')) return 'text-red-600'
    if (action.includes('invite') || action.includes('join')) return 'text-purple-600'
    return 'text-gray-600'
  }

  const formatTimeAgo = (date: string) => {
    const now = new Date()
    const activityDate = new Date(date)
    const diffInMinutes = Math.floor((now.getTime() - activityDate.getTime()) / (1000 * 60))

    if (diffInMinutes < 1) return 'Just now'
    if (diffInMinutes < 60) return `${diffInMinutes}m ago`
    if (diffInMinutes < 1440) return `${Math.floor(diffInMinutes / 60)}h ago`
    if (diffInMinutes < 10080) return `${Math.floor(diffInMinutes / 1440)}d ago`
    return activityDate.toLocaleDateString()
  }

  const formatAction = (action: string, details: any) => {
    switch (action) {
      case 'article.created':
        return `created article "${details?.title || 'Untitled'}"`
      case 'article.published':
        return `published article "${details?.title || 'Untitled'}"`
      case 'article.updated':
        return `updated article "${details?.title || 'Untitled'}"`
      case 'article.deleted':
        return `deleted article "${details?.title || 'Untitled'}"`
      case 'member.invited':
        return `invited ${details?.email || 'new member'} to the team`
      case 'member.joined':
        return `joined the team`
      case 'member.role_changed':
        return `changed role to ${details?.new_role || 'member'}`
      case 'pipeline.created':
        return `created new content pipeline`
      case 'pipeline.completed':
        return `completed content pipeline`
      case 'organization.settings_updated':
        return `updated organization settings`
      default:
        return action.replace(/_/g, ' ').replace(/\./g, ' ')
    }
  }

  if (!displayedActivities.length) {
    return (
      <div className="text-center py-8">
        <Clock className="h-12 w-12 text-muted-foreground mx-auto mb-3" />
        <p className="text-muted-foreground">No recent activity</p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {displayedActivities.map((activity, index) => {
        const Icon = getActionIcon(activity.action, activity.resource_type)
        const iconColor = getActionColor(activity.action)
        
        return (
          <div key={activity.id} className="flex items-start gap-3">
            {/* Activity Icon */}
            <div className={`flex-shrink-0 w-8 h-8 rounded-full bg-muted flex items-center justify-center ${iconColor}`}>
              <Icon className="h-4 w-4" />
            </div>

            {/* Activity Content */}
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 mb-1">
                {activity.profiles && (
                  <Avatar className="h-5 w-5">
                    <AvatarImage src={activity.profiles.avatar_url || undefined} />
                    <AvatarFallback className="text-xs">
                      {activity.profiles.full_name?.split(' ').map(n => n[0]).join('') || 'U'}
                    </AvatarFallback>
                  </Avatar>
                )}
                
                <p className="text-sm">
                  <span className="font-medium">
                    {activity.profiles?.full_name || 'System'}
                  </span>{' '}
                  {formatAction(activity.action, activity.details)}
                </p>
              </div>

              <div className="flex items-center gap-2">
                <span className="text-xs text-muted-foreground">
                  {formatTimeAgo(activity.created_at)}
                </span>

                {activity.resource_type && (
                  <Badge variant="outline" className="text-xs">
                    {activity.resource_type}
                  </Badge>
                )}
              </div>

              {/* Activity Details */}
              {activity.details && Object.keys(activity.details).length > 0 && (
                <div className="mt-2 p-2 bg-muted rounded text-xs">
                  {activity.details.seo_score && (
                    <span>SEO Score: {activity.details.seo_score}/100</span>
                  )}
                  {activity.details.word_count && (
                    <span className="ml-3">Words: {activity.details.word_count}</span>
                  )}
                  {activity.details.cost && (
                    <span className="ml-3">Cost: ${activity.details.cost}</span>
                  )}
                </div>
              )}
            </div>

            {/* Timeline Connector */}
            {index < displayedActivities.length - 1 && (
              <div className="absolute left-4 top-10 w-px h-8 bg-border" style={{ marginLeft: '15px' }} />
            )}
          </div>
        )
      })}

      {limit && activities.length > limit && (
        <div className="text-center pt-4">
          <p className="text-sm text-muted-foreground">
            +{activities.length - limit} more activities
          </p>
        </div>
      )}
    </div>
  )
}
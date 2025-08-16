import { Badge } from '@/components/ui/badge'
import { ScrollArea } from '@/components/ui/scroll-area'
import { 
  Building, 
  CreditCard, 
  TrendingUp, 
  AlertTriangle, 
  Shield, 
  Users,
  FileText,
  CheckCircle,
  XCircle
} from 'lucide-react'

interface ActivityItem {
  id: string
  type: 'upgrade' | 'payment' | 'usage' | 'support' | 'security' | 'system'
  title: string
  description: string
  timestamp: string
  severity: 'info' | 'warning' | 'critical' | 'success'
  organization?: string
  user?: string
}

const mockActivities: ActivityItem[] = [
  {
    id: '1',
    type: 'upgrade',
    title: 'Plan Upgrade',
    description: "Organization 'TechCorp' upgraded to Professional plan",
    timestamp: '2 minutes ago',
    severity: 'success',
    organization: 'TechCorp'
  },
  {
    id: '2',
    type: 'payment',
    title: 'Payment Failed',
    description: 'Payment failed for user@domain.com - retry scheduled',
    timestamp: '5 minutes ago',
    severity: 'warning',
    user: 'user@domain.com'
  },
  {
    id: '3',
    type: 'usage',
    title: 'High API Usage',
    description: "High API usage detected from organization 'ContentAgency'",
    timestamp: '12 minutes ago',
    severity: 'warning',
    organization: 'ContentAgency'
  },
  {
    id: '4',
    type: 'support',
    title: 'Support Escalation',
    description: 'Support ticket #1247 escalated to technical team',
    timestamp: '18 minutes ago',
    severity: 'info'
  },
  {
    id: '5',
    type: 'security',
    title: 'Security Alert',
    description: 'Multiple failed login attempts from IP 192.168.1.1',
    timestamp: '25 minutes ago',
    severity: 'critical'
  },
  {
    id: '6',
    type: 'system',
    title: 'System Recovery',
    description: 'Anthropic API service restored to normal operation',
    timestamp: '32 minutes ago',
    severity: 'success'
  },
  {
    id: '7',
    type: 'upgrade',
    title: 'New Enterprise Customer',
    description: "Organization 'MegaCorp' signed enterprise contract",
    timestamp: '1 hour ago',
    severity: 'success',
    organization: 'MegaCorp'
  },
  {
    id: '8',
    type: 'payment',
    title: 'Payment Recovered',
    description: 'Failed payment successfully recovered for StartupXYZ',
    timestamp: '1 hour ago',
    severity: 'success',
    organization: 'StartupXYZ'
  }
]

export function ActivityFeed() {
  const getActivityIcon = (type: string, severity: string) => {
    const iconClass = `h-4 w-4 ${getSeverityColor(severity)}`
    
    switch (type) {
      case 'upgrade':
        return <TrendingUp className={iconClass} />
      case 'payment':
        return severity === 'warning' || severity === 'critical' 
          ? <XCircle className={iconClass} />
          : <CheckCircle className={iconClass} />
      case 'usage':
        return <BarChart3 className={iconClass} />
      case 'support':
        return <Users className={iconClass} />
      case 'security':
        return <Shield className={iconClass} />
      case 'system':
        return <AlertTriangle className={iconClass} />
      default:
        return <FileText className={iconClass} />
    }
  }

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'success':
        return 'text-green-600'
      case 'warning':
        return 'text-yellow-600'
      case 'critical':
        return 'text-red-600'
      default:
        return 'text-blue-600'
    }
  }

  const getSeverityBadge = (severity: string) => {
    switch (severity) {
      case 'success':
        return <Badge className="bg-green-100 text-green-800 hover:bg-green-100">Success</Badge>
      case 'warning':
        return <Badge className="bg-yellow-100 text-yellow-800 hover:bg-yellow-100">Warning</Badge>
      case 'critical':
        return <Badge className="bg-red-100 text-red-800 hover:bg-red-100">Critical</Badge>
      default:
        return <Badge className="bg-blue-100 text-blue-800 hover:bg-blue-100">Info</Badge>
    }
  }

  return (
    <ScrollArea className="h-[400px]">
      <div className="space-y-3">
        {mockActivities.map((activity) => (
          <div 
            key={activity.id} 
            className="flex items-start gap-3 p-3 border rounded-lg hover:bg-muted/50 transition-colors"
          >
            <div className="mt-0.5">
              {getActivityIcon(activity.type, activity.severity)}
            </div>
            
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 mb-1">
                <h4 className="font-medium text-sm">{activity.title}</h4>
                {getSeverityBadge(activity.severity)}
              </div>
              <p className="text-xs text-muted-foreground mb-2">
                {activity.description}
              </p>
              <div className="flex items-center gap-2 text-xs text-muted-foreground">
                <span>{activity.timestamp}</span>
                {activity.organization && (
                  <>
                    <span>•</span>
                    <span className="flex items-center gap-1">
                      <Building className="h-3 w-3" />
                      {activity.organization}
                    </span>
                  </>
                )}
                {activity.user && (
                  <>
                    <span>•</span>
                    <span className="flex items-center gap-1">
                      <Users className="h-3 w-3" />
                      {activity.user}
                    </span>
                  </>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </ScrollArea>
  )
}

// Import BarChart3 since it was missing
import { BarChart3 } from 'lucide-react'
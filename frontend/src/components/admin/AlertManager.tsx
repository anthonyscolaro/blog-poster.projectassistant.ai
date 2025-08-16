import { useState } from 'react'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { ScrollArea } from '@/components/ui/scroll-area'
import { 
  AlertTriangle, 
  XCircle, 
  CheckCircle, 
  Clock, 
  DollarSign,
  Server,
  Shield,
  Users,
  Eye,
  Check,
  X
} from 'lucide-react'

interface Alert {
  id: string
  type: 'system' | 'billing' | 'security' | 'performance' | 'user'
  severity: 'critical' | 'warning' | 'info'
  title: string
  description: string
  timestamp: string
  acknowledged: boolean
  resolved: boolean
  assignee?: string
  escalated: boolean
}

const mockAlerts: Alert[] = [
  {
    id: '1',
    type: 'system',
    severity: 'warning',
    title: 'Anthropic API Degraded',
    description: 'Response times increased by 40% over the last 15 minutes',
    timestamp: '5 minutes ago',
    acknowledged: false,
    resolved: false,
    escalated: false
  },
  {
    id: '2',
    type: 'billing',
    severity: 'critical',
    title: 'Payment Processing Error',
    description: 'Stripe webhook failures causing payment delays',
    timestamp: '12 minutes ago',
    acknowledged: true,
    resolved: false,
    assignee: 'billing-team',
    escalated: true
  },
  {
    id: '3',
    type: 'security',
    severity: 'warning',
    title: 'Suspicious Login Pattern',
    description: 'Multiple failed login attempts from new IP ranges',
    timestamp: '1 hour ago',
    acknowledged: true,
    resolved: false,
    assignee: 'security-team',
    escalated: false
  },
  {
    id: '4',
    type: 'performance',
    severity: 'info',
    title: 'Database Connection Pool',
    description: 'Connection usage approaching 85% of capacity',
    timestamp: '2 hours ago',
    acknowledged: false,
    resolved: false,
    escalated: false
  },
  {
    id: '5',
    type: 'user',
    severity: 'warning',
    title: 'Support Ticket Backlog',
    description: '15 tickets pending response beyond SLA',
    timestamp: '3 hours ago',
    acknowledged: true,
    resolved: false,
    assignee: 'support-team',
    escalated: false
  }
]

export function AlertManager() {
  const [alerts, setAlerts] = useState(mockAlerts)
  const [filter, setFilter] = useState<'all' | 'unacknowledged' | 'critical'>('unacknowledged')

  const getAlertIcon = (type: string, severity: string) => {
    const iconClass = `h-4 w-4 ${getSeverityColor(severity)}`
    
    switch (type) {
      case 'system':
        return <Server className={iconClass} />
      case 'billing':
        return <DollarSign className={iconClass} />
      case 'security':
        return <Shield className={iconClass} />
      case 'performance':
        return <AlertTriangle className={iconClass} />
      case 'user':
        return <Users className={iconClass} />
      default:
        return <AlertTriangle className={iconClass} />
    }
  }

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical':
        return 'text-red-600'
      case 'warning':
        return 'text-yellow-600'
      case 'info':
        return 'text-blue-600'
      default:
        return 'text-gray-600'
    }
  }

  const getSeverityBadge = (severity: string) => {
    switch (severity) {
      case 'critical':
        return <Badge className="bg-red-100 text-red-800 hover:bg-red-100">Critical</Badge>
      case 'warning':
        return <Badge className="bg-yellow-100 text-yellow-800 hover:bg-yellow-100">Warning</Badge>
      case 'info':
        return <Badge className="bg-blue-100 text-blue-800 hover:bg-blue-100">Info</Badge>
      default:
        return <Badge variant="outline">Unknown</Badge>
    }
  }

  const handleAcknowledge = (alertId: string) => {
    setAlerts(alerts.map(alert => 
      alert.id === alertId ? { ...alert, acknowledged: true } : alert
    ))
  }

  const handleResolve = (alertId: string) => {
    setAlerts(alerts.map(alert => 
      alert.id === alertId ? { ...alert, resolved: true } : alert
    ))
  }

  const filteredAlerts = alerts.filter(alert => {
    if (!alert.resolved) { // Never show resolved alerts
      switch (filter) {
        case 'unacknowledged':
          return !alert.acknowledged
        case 'critical':
          return alert.severity === 'critical'
        case 'all':
        default:
          return true
      }
    }
    return false
  })

  const criticalCount = alerts.filter(a => !a.resolved && a.severity === 'critical').length
  const unacknowledgedCount = alerts.filter(a => !a.resolved && !a.acknowledged).length

  return (
    <div className="space-y-4">
      {/* Alert Summary */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <XCircle className="h-4 w-4 text-red-600" />
            <span className="text-sm font-medium">{criticalCount} Critical</span>
          </div>
          <div className="flex items-center gap-2">
            <Clock className="h-4 w-4 text-yellow-600" />
            <span className="text-sm font-medium">{unacknowledgedCount} Unacknowledged</span>
          </div>
        </div>
        
        <div className="flex gap-2">
          <Button
            variant={filter === 'unacknowledged' ? 'default' : 'outline'}
            size="sm"
            onClick={() => setFilter('unacknowledged')}
          >
            Unacked
          </Button>
          <Button
            variant={filter === 'critical' ? 'default' : 'outline'}
            size="sm"
            onClick={() => setFilter('critical')}
          >
            Critical
          </Button>
          <Button
            variant={filter === 'all' ? 'default' : 'outline'}
            size="sm"
            onClick={() => setFilter('all')}
          >
            All
          </Button>
        </div>
      </div>

      {/* Alerts List */}
      <ScrollArea className="h-[300px]">
        <div className="space-y-2">
          {filteredAlerts.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-8 text-center">
              <CheckCircle className="h-8 w-8 text-green-600 mb-2" />
              <span className="text-sm text-muted-foreground">
                {filter === 'unacknowledged' 
                  ? 'No unacknowledged alerts'
                  : filter === 'critical'
                  ? 'No critical alerts'
                  : 'No active alerts'
                }
              </span>
            </div>
          ) : (
            filteredAlerts.map((alert) => (
              <div 
                key={alert.id} 
                className={`flex items-start gap-3 p-3 border rounded-lg transition-colors ${
                  alert.severity === 'critical' ? 'border-red-200 bg-red-50/50' : 
                  alert.severity === 'warning' ? 'border-yellow-200 bg-yellow-50/50' : 
                  'border-border'
                }`}
              >
                <div className="mt-0.5">
                  {getAlertIcon(alert.type, alert.severity)}
                </div>
                
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <h4 className="font-medium text-sm">{alert.title}</h4>
                    {getSeverityBadge(alert.severity)}
                    {alert.escalated && (
                      <Badge variant="destructive" className="text-xs">Escalated</Badge>
                    )}
                  </div>
                  <p className="text-xs text-muted-foreground mb-2">
                    {alert.description}
                  </p>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2 text-xs text-muted-foreground">
                      <span>{alert.timestamp}</span>
                      {alert.assignee && (
                        <>
                          <span>•</span>
                          <span>Assigned to {alert.assignee}</span>
                        </>
                      )}
                    </div>
                    
                    <div className="flex gap-1">
                      {!alert.acknowledged && (
                        <Button
                          variant="ghost"
                          size="sm"
                          className="h-6 px-2"
                          onClick={() => handleAcknowledge(alert.id)}
                        >
                          <Eye className="h-3 w-3 mr-1" />
                          Ack
                        </Button>
                      )}
                      <Button
                        variant="ghost"
                        size="sm"
                        className="h-6 px-2"
                        onClick={() => handleResolve(alert.id)}
                      >
                        <Check className="h-3 w-3 mr-1" />
                        Resolve
                      </Button>
                    </div>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </ScrollArea>
    </div>
  )
}
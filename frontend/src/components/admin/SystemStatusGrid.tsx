import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { 
  Server, 
  Database, 
  Zap, 
  HardDrive, 
  BarChart3, 
  Shield,
  CheckCircle,
  AlertTriangle,
  XCircle
} from 'lucide-react'

interface SystemHealth {
  api_gateway: { status: 'healthy' | 'degraded' | 'down', response_time: number }
  database: { status: 'healthy' | 'degraded' | 'down', connections: number, max_connections: number }
  ai_services: { status: 'healthy' | 'degraded' | 'down', note?: string }
  storage: { status: 'healthy' | 'degraded' | 'down', availability: number }
  queue_system: { status: 'healthy' | 'degraded' | 'down', pending_jobs: number }
  monitoring: { status: 'healthy' | 'degraded' | 'down' }
}

interface SystemStatusGridProps {
  systemHealth?: SystemHealth
}

export function SystemStatusGrid({ systemHealth }: SystemStatusGridProps) {
  if (!systemHealth) {
    return (
      <div className="space-y-3">
        {[...Array(6)].map((_, i) => (
          <div key={i} className="animate-pulse flex items-center gap-3">
            <div className="h-8 w-8 bg-muted rounded"></div>
            <div className="flex-1 h-4 bg-muted rounded"></div>
            <div className="h-6 w-16 bg-muted rounded"></div>
          </div>
        ))}
      </div>
    )
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'healthy':
        return <CheckCircle className="h-4 w-4 text-green-600" />
      case 'degraded':
        return <AlertTriangle className="h-4 w-4 text-yellow-600" />
      case 'down':
        return <XCircle className="h-4 w-4 text-red-600" />
      default:
        return <AlertTriangle className="h-4 w-4 text-gray-600" />
    }
  }

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'healthy':
        return <Badge className="bg-green-100 text-green-800 hover:bg-green-100">Healthy</Badge>
      case 'degraded':
        return <Badge className="bg-yellow-100 text-yellow-800 hover:bg-yellow-100">Degraded</Badge>
      case 'down':
        return <Badge className="bg-red-100 text-red-800 hover:bg-red-100">Down</Badge>
      default:
        return <Badge variant="outline">Unknown</Badge>
    }
  }

  const services = [
    {
      name: 'API Gateway',
      icon: <Server className="h-4 w-4" />,
      status: systemHealth.api_gateway.status,
      details: `${systemHealth.api_gateway.response_time}ms response time`
    },
    {
      name: 'Database',
      icon: <Database className="h-4 w-4" />,
      status: systemHealth.database.status,
      details: `${systemHealth.database.connections}/${systemHealth.database.max_connections} connections`
    },
    {
      name: 'AI Services',
      icon: <Zap className="h-4 w-4" />,
      status: systemHealth.ai_services.status,
      details: systemHealth.ai_services.note || 'All models operational'
    },
    {
      name: 'Storage',
      icon: <HardDrive className="h-4 w-4" />,
      status: systemHealth.storage.status,
      details: `${systemHealth.storage.availability}% available`
    },
    {
      name: 'Queue System',
      icon: <BarChart3 className="h-4 w-4" />,
      status: systemHealth.queue_system.status,
      details: `${systemHealth.queue_system.pending_jobs} jobs pending`
    },
    {
      name: 'Monitoring',
      icon: <Shield className="h-4 w-4" />,
      status: systemHealth.monitoring.status,
      details: 'All alerts active'
    }
  ]

  return (
    <div className="space-y-4">
      {services.map((service) => (
        <div key={service.name} className="flex items-center justify-between p-3 border rounded-lg">
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2">
              {service.icon}
              {getStatusIcon(service.status)}
            </div>
            <div>
              <div className="font-medium text-sm">{service.name}</div>
              <div className="text-xs text-muted-foreground">{service.details}</div>
            </div>
          </div>
          <div className="flex items-center gap-2">
            {getStatusBadge(service.status)}
          </div>
        </div>
      ))}
      
      {/* Database Connection Usage */}
      <div className="mt-4 p-3 bg-muted/50 rounded-lg">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm font-medium">Database Connections</span>
          <span className="text-xs text-muted-foreground">
            {systemHealth.database.connections}/{systemHealth.database.max_connections}
          </span>
        </div>
        <Progress 
          value={(systemHealth.database.connections / systemHealth.database.max_connections) * 100} 
          className="h-2"
        />
      </div>
      
      {/* Storage Usage */}
      <div className="p-3 bg-muted/50 rounded-lg">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm font-medium">Storage Availability</span>
          <span className="text-xs text-muted-foreground">
            {systemHealth.storage.availability}%
          </span>
        </div>
        <Progress 
          value={systemHealth.storage.availability} 
          className="h-2"
        />
      </div>
    </div>
  )
}
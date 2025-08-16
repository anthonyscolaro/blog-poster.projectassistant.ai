import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Plug, ExternalLink } from 'lucide-react'

interface IntegrationSettingsProps {
  integrations: any
  onChange: (updates: any) => void
}

const AVAILABLE_INTEGRATIONS = [
  {
    id: 'google_analytics',
    name: 'Google Analytics',
    description: 'Track content performance and user engagement',
    icon: '📊',
    status: 'available'
  },
  {
    id: 'hubspot',
    name: 'HubSpot',
    description: 'Sync content with your CRM and marketing automation',
    icon: '🚀',
    status: 'available'
  },
  {
    id: 'zapier',
    name: 'Zapier',
    description: 'Connect with 5000+ apps and automate workflows',
    icon: '⚡',
    status: 'available'
  },
  {
    id: 'make',
    name: 'Make',
    description: 'Advanced automation and integration platform',
    icon: '🔧',
    status: 'available'
  }
]

export function IntegrationSettings({ integrations, onChange }: IntegrationSettingsProps) {
  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Plug className="h-5 w-5" />
            Third-Party Integrations
          </CardTitle>
          <CardDescription>
            Connect Blog-Poster with your favorite tools and services
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {AVAILABLE_INTEGRATIONS.map((integration) => (
              <div key={integration.id} className="flex items-center justify-between p-4 border rounded-lg">
                <div className="flex items-center gap-3">
                  <span className="text-2xl">{integration.icon}</span>
                  <div>
                    <h4 className="font-medium">{integration.name}</h4>
                    <p className="text-sm text-muted-foreground">{integration.description}</p>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <Badge variant="outline">Coming Soon</Badge>
                  <Button variant="outline" size="sm" disabled>
                    <ExternalLink className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
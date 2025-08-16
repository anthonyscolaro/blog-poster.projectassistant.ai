import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Plus, Globe, Settings } from 'lucide-react'

interface WordPressConfig {
  id: string
  name: string
  url: string
  username: string
  app_password: string | null
  is_default: boolean
  is_active: boolean
  verify_ssl: boolean
  last_sync: string | null
  categories: string[]
  default_author: string | null
}

interface WordPressSettingsProps {
  wordpressConfigs: WordPressConfig[]
  onChange: (configs: WordPressConfig[]) => void
}

export function WordPressSettings({ wordpressConfigs, onChange }: WordPressSettingsProps) {
  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Globe className="h-5 w-5" />
            WordPress Connections
          </CardTitle>
          <CardDescription>
            Manage WordPress site connections for content publishing
          </CardDescription>
        </CardHeader>
        <CardContent>
          {wordpressConfigs.length > 0 ? (
            <div className="space-y-4">
              {wordpressConfigs.map((site) => (
                <div key={site.id} className="flex items-center justify-between p-4 border rounded-lg">
                  <div>
                    <h4 className="font-medium">{site.name}</h4>
                    <p className="text-sm text-muted-foreground">{site.url}</p>
                    {site.last_sync && (
                      <p className="text-xs text-muted-foreground">
                        Last sync: {new Date(site.last_sync).toLocaleDateString()}
                      </p>
                    )}
                  </div>
                  <div className="flex items-center gap-2">
                    {site.is_default && (
                      <Badge variant="secondary">Default</Badge>
                    )}
                    <Badge variant={site.is_active ? 'default' : 'secondary'}>
                      {site.is_active ? 'Connected' : 'Inactive'}
                    </Badge>
                    <Button variant="outline" size="sm">
                      <Settings className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8">
              <Globe className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
              <p className="text-muted-foreground mb-4">No WordPress sites connected</p>
              <Button variant="outline">
                <Plus className="h-4 w-4 mr-2" />
                Add WordPress Site
              </Button>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
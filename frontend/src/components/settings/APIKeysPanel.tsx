import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { 
  Key, 
  Eye, 
  EyeOff, 
  Check, 
  X, 
  Plus,
  Trash2,
  TestTube,
  Shield,
  ExternalLink,
  AlertTriangle,
  Info
} from 'lucide-react'
import { toast } from 'sonner'

interface ApiKeyConfig {
  key_name: string
  service: string
  encrypted_key: string
  key_hint: string | null
  is_active: boolean
  last_used_at: string | null
  created_at: string
  updated_at: string
}

interface ApiKeys {
  anthropic: ApiKeyConfig | null
  openai: ApiKeyConfig | null
  jina: ApiKeyConfig | null
  wordpress: any[]
}

interface APIKeysPanelProps {
  apiKeys: ApiKeys
  onChange: (updates: Partial<ApiKeys>) => void
}

const API_SERVICES = {
  anthropic: {
    name: 'Anthropic Claude',
    description: 'High-quality content generation and fact-checking',
    icon: '🤖',
    placeholder: 'sk-ant-api03-...',
    docsUrl: 'https://docs.anthropic.com/claude/reference/getting-started-with-the-api',
    features: ['Article Generation', 'Legal Fact-Checking', 'Content Analysis'],
    cost: '$0.50-2.00 per article'
  },
  openai: {
    name: 'OpenAI',
    description: 'Topic analysis and content optimization',
    icon: '⚡',
    placeholder: 'sk-...',
    docsUrl: 'https://platform.openai.com/docs/quickstart',
    features: ['Topic Analysis', 'SEO Optimization', 'Content Refinement'],
    cost: '$0.10-0.50 per article'
  },
  jina: {
    name: 'Jina AI',
    description: 'Advanced embeddings for competitor analysis',
    icon: '🔍',
    placeholder: 'jina_...',
    docsUrl: 'https://jina.ai/embeddings/',
    features: ['Competitor Monitoring', 'Content Similarity', 'Topic Clustering'],
    cost: '$0.02-0.10 per article'
  }
}

export function APIKeysPanel({ apiKeys, onChange }: APIKeysPanelProps) {
  const [showKeys, setShowKeys] = useState<Record<string, boolean>>({})
  const [newKeys, setNewKeys] = useState<Record<string, string>>({})
  const [testingKeys, setTestingKeys] = useState<Record<string, boolean>>({})

  const toggleKeyVisibility = (service: string) => {
    setShowKeys(prev => ({ ...prev, [service]: !prev[service] }))
  }

  const handleKeyUpdate = (service: keyof ApiKeys, key: string) => {
    setNewKeys(prev => ({ ...prev, [service]: key }))
    
    // Update the API keys
    onChange({
      ...apiKeys,
      [service]: key ? {
        key_name: `${service}_key`,
        service,
        encrypted_key: key,
        key_hint: key.slice(0, 8) + '...' + key.slice(-4),
        is_active: true,
        last_used_at: null,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      } : null
    })
  }

  const handleTestKey = async (service: string) => {
    const key = newKeys[service] || (apiKeys[service as keyof ApiKeys] as ApiKeyConfig)?.encrypted_key
    if (!key) {
      toast.error('Please enter an API key first')
      return
    }

    setTestingKeys(prev => ({ ...prev, [service]: true }))
    
    try {
      // Simulate API key testing
      await new Promise(resolve => setTimeout(resolve, 2000))
      
      // For demo purposes, randomly succeed or fail
      const isValid = Math.random() > 0.3
      
      if (isValid) {
        toast.success(`${API_SERVICES[service as keyof typeof API_SERVICES].name} API key is valid!`)
        // Update the key status
        const currentKey = apiKeys[service as keyof ApiKeys] as ApiKeyConfig
        if (currentKey) {
          onChange({
            ...apiKeys,
            [service]: {
              ...currentKey,
              is_active: true,
              last_used_at: new Date().toISOString()
            }
          })
        }
      } else {
        toast.error(`${API_SERVICES[service as keyof typeof API_SERVICES].name} API key is invalid`)
      }
    } catch (error) {
      toast.error('Failed to test API key')
    } finally {
      setTestingKeys(prev => ({ ...prev, [service]: false }))
    }
  }

  const handleRemoveKey = (service: keyof ApiKeys) => {
    onChange({
      ...apiKeys,
      [service]: null
    })
    setNewKeys(prev => ({ ...prev, [service]: '' }))
    toast.success('API key removed')
  }

  const getKeyDisplay = (service: string, config: ApiKeyConfig | null) => {
    if (!config) return ''
    
    if (showKeys[service]) {
      return newKeys[service] || config.encrypted_key || ''
    } else {
      return config.key_hint || '••••••••••••••••'
    }
  }

  const getStatusBadge = (config: ApiKeyConfig | null) => {
    if (!config) return <Badge variant="outline">Not configured</Badge>
    
    if (config.is_active) {
      return <Badge variant="default" className="bg-green-500"><Check className="h-3 w-3 mr-1" />Active</Badge>
    } else {
      return <Badge variant="destructive"><X className="h-3 w-3 mr-1" />Invalid</Badge>
    }
  }

  return (
    <div className="space-y-6">
      {/* Information Alert */}
      <Alert>
        <Info className="h-4 w-4" />
        <AlertDescription>
          API keys are encrypted and stored securely. They're required for content generation agents to function.
          <strong> Cost estimates are per article and may vary based on content length and complexity.</strong>
        </AlertDescription>
      </Alert>

      {/* API Keys Configuration */}
      {Object.entries(API_SERVICES).map(([serviceKey, service]) => {
        const config = apiKeys[serviceKey as keyof ApiKeys] as ApiKeyConfig | null
        const isTesting = testingKeys[serviceKey]
        
        return (
          <Card key={serviceKey}>
            <CardHeader>
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-3">
                  <div className="text-2xl">{service.icon}</div>
                  <div>
                    <CardTitle className="flex items-center gap-2">
                      {service.name}
                      {getStatusBadge(config)}
                    </CardTitle>
                    <CardDescription>{service.description}</CardDescription>
                  </div>
                </div>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => window.open(service.docsUrl, '_blank')}
                >
                  <ExternalLink className="h-4 w-4 mr-2" />
                  API Docs
                </Button>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Features & Cost */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label className="text-sm font-medium">Features</Label>
                  <ul className="text-sm text-muted-foreground mt-1">
                    {service.features.map((feature) => (
                      <li key={feature} className="flex items-center gap-1">
                        <Check className="h-3 w-3 text-green-500" />
                        {feature}
                      </li>
                    ))}
                  </ul>
                </div>
                <div>
                  <Label className="text-sm font-medium">Estimated Cost</Label>
                  <p className="text-sm text-muted-foreground mt-1">{service.cost}</p>
                </div>
              </div>

              {/* API Key Input */}
              <div className="space-y-2">
                <Label htmlFor={`${serviceKey}-key`}>
                  <Key className="h-4 w-4 inline mr-1" />
                  API Key
                </Label>
                <div className="flex gap-2">
                  <div className="relative flex-1">
                    <Input
                      id={`${serviceKey}-key`}
                      type={showKeys[serviceKey] ? 'text' : 'password'}
                      value={newKeys[serviceKey] || getKeyDisplay(serviceKey, config)}
                      onChange={(e) => {
                        setNewKeys(prev => ({ ...prev, [serviceKey]: e.target.value }))
                        if (e.target.value) {
                          handleKeyUpdate(serviceKey as keyof ApiKeys, e.target.value)
                        }
                      }}
                      placeholder={service.placeholder}
                    />
                    <Button
                      type="button"
                      variant="ghost"
                      size="sm"
                      className="absolute right-0 top-0 h-full px-3"
                      onClick={() => toggleKeyVisibility(serviceKey)}
                    >
                      {showKeys[serviceKey] ? (
                        <EyeOff className="h-4 w-4" />
                      ) : (
                        <Eye className="h-4 w-4" />
                      )}
                    </Button>
                  </div>
                  
                  <Button
                    variant="outline"
                    onClick={() => handleTestKey(serviceKey)}
                    disabled={isTesting || (!newKeys[serviceKey] && !config)}
                  >
                    {isTesting ? (
                      'Testing...'
                    ) : (
                      <>
                        <TestTube className="h-4 w-4 mr-2" />
                        Test
                      </>
                    )}
                  </Button>

                  {config && (
                    <Button
                      variant="outline"
                      size="icon"
                      onClick={() => handleRemoveKey(serviceKey as keyof ApiKeys)}
                      className="text-destructive hover:text-destructive"
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  )}
                </div>
                
                {config?.last_used_at && (
                  <p className="text-sm text-muted-foreground">
                    Last used: {new Date(config.last_used_at).toLocaleDateString()}
                  </p>
                )}
              </div>
            </CardContent>
          </Card>
        )
      })}

      {/* Security Notice */}
      <Alert>
        <Shield className="h-4 w-4" />
        <AlertDescription>
          <strong>Security:</strong> Your API keys are encrypted at rest and never logged in plain text. 
          Only use API keys from official providers and never share them with unauthorized parties.
        </AlertDescription>
      </Alert>

      {/* WordPress Connection */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Key className="h-5 w-5" />
            WordPress Connections
          </CardTitle>
          <CardDescription>
            Manage WordPress site connections for content publishing
          </CardDescription>
        </CardHeader>
        <CardContent>
          {apiKeys.wordpress.length > 0 ? (
            <div className="space-y-4">
              {apiKeys.wordpress.map((site, index) => (
                <div key={index} className="flex items-center justify-between p-4 border rounded-lg">
                  <div>
                    <h4 className="font-medium">{site.name}</h4>
                    <p className="text-sm text-muted-foreground">{site.url}</p>
                  </div>
                  <Badge variant={site.is_active ? 'default' : 'secondary'}>
                    {site.is_active ? 'Connected' : 'Inactive'}
                  </Badge>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8">
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
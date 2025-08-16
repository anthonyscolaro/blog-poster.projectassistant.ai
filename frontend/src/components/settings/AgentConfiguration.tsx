import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Label } from '@/components/ui/label'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Switch } from '@/components/ui/switch'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Slider } from '@/components/ui/slider'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Button } from '@/components/ui/button'
import { 
  Bot, 
  Settings, 
  AlertCircle, 
  RefreshCw,
  DollarSign,
  Clock,
  Zap,
  FileText,
  Shield,
  Globe,
  Target,
  Brain
} from 'lucide-react'

interface AgentConfig {
  enabled: boolean
  timeout_seconds: number
  max_retries: number
  config: Record<string, unknown>
}

interface AgentSettings {
  competitor: AgentConfig
  topic: AgentConfig
  article: AgentConfig
  legal: AgentConfig
  wordpress: AgentConfig
}

interface AgentConfigurationProps {
  agents: AgentSettings
  onChange: (updates: Partial<AgentSettings>) => void
}

const AGENT_DETAILS = {
  competitor: {
    name: 'Competitor Monitoring Agent',
    icon: Globe,
    description: 'Tracks industry content and identifies opportunities',
    defaultModel: 'jina-embeddings-v2',
    supportsCustomPrompts: true,
    costEstimate: 0.02,
    features: ['Content Discovery', 'Trend Analysis', 'Gap Identification']
  },
  topic: {
    name: 'Topic Analysis Agent',
    icon: FileText,
    description: 'Analyzes topics for SEO opportunities and content gaps',
    defaultModel: 'gpt-4-turbo',
    supportsCustomPrompts: true,
    costEstimate: 0.01,
    features: ['Keyword Research', 'SEO Analysis', 'Content Planning']
  },
  article: {
    name: 'Article Generation Agent',
    icon: Zap,
    description: 'Creates SEO-optimized content with Claude 3.5 Sonnet',
    defaultModel: 'claude-3-5-sonnet-20241022',
    supportsCustomPrompts: true,
    costEstimate: 0.20,
    features: ['Content Creation', 'SEO Optimization', 'Brand Voice']
  },
  legal: {
    name: 'Legal Fact Checker Agent',
    icon: Shield,
    description: 'Verifies ADA compliance claims and legal accuracy',
    defaultModel: 'claude-3-5-sonnet-20241022',
    supportsCustomPrompts: true,
    costEstimate: 0.02,
    features: ['Compliance Check', 'Fact Verification', 'Legal Review']
  },
  wordpress: {
    name: 'WordPress Publisher Agent',
    icon: Bot,
    description: 'Handles content deployment via WPGraphQL',
    defaultModel: null,
    supportsCustomPrompts: false,
    costEstimate: 0,
    features: ['Content Publishing', 'Meta Management', 'Category Assignment']
  }
}

const AVAILABLE_MODELS = [
  { value: 'claude-3-5-sonnet-20241022', label: 'Claude 3.5 Sonnet (Latest)', cost: 'High' },
  { value: 'claude-3-opus-20240229', label: 'Claude 3 Opus', cost: 'High' },
  { value: 'gpt-4-turbo', label: 'GPT-4 Turbo', cost: 'Medium' },
  { value: 'gpt-4', label: 'GPT-4', cost: 'Medium' },
  { value: 'gpt-3.5-turbo', label: 'GPT-3.5 Turbo', cost: 'Low' }
]

export function AgentConfiguration({ agents, onChange }: AgentConfigurationProps) {
  const [selectedAgent, setSelectedAgent] = useState<keyof AgentSettings>('competitor')
  const [testingAgent, setTestingAgent] = useState<string | null>(null)

  const currentAgent = agents[selectedAgent]
  const agentDetails = AGENT_DETAILS[selectedAgent]

  const handleAgentChange = (field: keyof AgentConfig | string, value: any) => {
    if (field === 'model_override' || field === 'temperature' || field === 'max_tokens' || field === 'custom_prompts') {
      onChange({
        ...agents,
        [selectedAgent]: {
          ...currentAgent,
          config: {
            ...currentAgent.config,
            [field]: value
          }
        }
      })
    } else {
      onChange({
        ...agents,
        [selectedAgent]: {
          ...currentAgent,
          [field]: value
        }
      })
    }
  }

  const handleTestAgent = async (agentKey: keyof AgentSettings) => {
    setTestingAgent(agentKey)
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 2000))
    setTestingAgent(null)
  }

  const calculateMonthlyEstimate = () => {
    let totalCost = 0
    Object.entries(agents).forEach(([key, config]) => {
      if (config.enabled) {
        const details = AGENT_DETAILS[key as keyof AgentSettings]
        totalCost += details.costEstimate * 100 // Assuming 100 articles/month
      }
    })
    return totalCost
  }

  const getConfigValue = (key: string, defaultValue: any = '') => {
    return currentAgent.config?.[key] ?? defaultValue
  }

  return (
    <div className="space-y-6">
      {/* Agent Selector */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Settings className="h-5 w-5" />
            Agent Configuration
          </CardTitle>
          <CardDescription>
            Customize behavior and parameters for each content generation agent
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 mb-6">
            {Object.entries(AGENT_DETAILS).map(([key, details]) => {
              const Icon = details.icon
              const agent = agents[key as keyof AgentSettings]
              return (
                <button
                  key={key}
                  onClick={() => setSelectedAgent(key as keyof AgentSettings)}
                  className={`p-4 border rounded-lg text-left transition-colors ${
                    selectedAgent === key
                      ? 'border-primary bg-primary/5'
                      : 'border-border hover:border-muted-foreground'
                  }`}
                >
                  <div className="flex items-center justify-between mb-2">
                    <Icon className="h-5 w-5" />
                    {agent.enabled && (
                      <span className="h-2 w-2 bg-green-500 rounded-full" />
                    )}
                  </div>
                  <h4 className="font-medium text-sm">{details.name}</h4>
                  <p className="text-xs text-muted-foreground mt-1">
                    ~${details.costEstimate}/article
                  </p>
                </button>
              )
            })}
          </div>

          {/* Selected Agent Configuration */}
          <div className="space-y-6">
            <div className="flex items-start justify-between">
              <div>
                <h3 className="text-lg font-semibold flex items-center gap-2">
                  <agentDetails.icon className="h-5 w-5" />
                  {agentDetails.name}
                </h3>
                <p className="text-sm text-muted-foreground mt-1">
                  {agentDetails.description}
                </p>
                <div className="flex flex-wrap gap-2 mt-2">
                  {agentDetails.features.map((feature) => (
                    <span
                      key={feature}
                      className="inline-flex items-center px-2 py-1 rounded-md text-xs bg-muted text-muted-foreground"
                    >
                      {feature}
                    </span>
                  ))}
                </div>
              </div>
              <Button
                variant="outline"
                size="sm"
                onClick={() => handleTestAgent(selectedAgent)}
                disabled={!!testingAgent || !currentAgent.enabled}
              >
                {testingAgent === selectedAgent ? (
                  <>
                    <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
                    Testing...
                  </>
                ) : (
                  <>
                    <Brain className="h-4 w-4 mr-2" />
                    Test Agent
                  </>
                )}
              </Button>
            </div>

            {/* Enable/Disable Toggle */}
            <div className="flex items-center justify-between p-4 bg-muted/50 rounded-lg">
              <div>
                <Label htmlFor="agent-enabled" className="font-medium">Enable Agent</Label>
                <p className="text-sm text-muted-foreground">
                  Turn this agent on or off in the content generation pipeline
                </p>
              </div>
              <Switch
                id="agent-enabled"
                checked={currentAgent.enabled}
                onCheckedChange={(checked) => handleAgentChange('enabled', checked)}
              />
            </div>

            {/* Configuration Options (only show if enabled) */}
            {currentAgent.enabled && (
              <>
                {/* Model Override */}
                {agentDetails.defaultModel && (
                  <div className="space-y-2">
                    <Label htmlFor="model-override">
                      <Brain className="h-4 w-4 inline mr-1" />
                      AI Model
                    </Label>
                    <Select
                      value={getConfigValue('model_override', agentDetails.defaultModel)}
                      onValueChange={(value) => handleAgentChange('model_override', value)}
                    >
                      <SelectTrigger id="model-override">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {AVAILABLE_MODELS.map(model => (
                          <SelectItem key={model.value} value={model.value}>
                            <div className="flex items-center justify-between w-full">
                              <span>{model.label}</span>
                              <span className="text-xs text-muted-foreground ml-2">
                                {model.cost} cost
                              </span>
                            </div>
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    <p className="text-sm text-muted-foreground">
                      Override the default model for this agent
                    </p>
                  </div>
                )}

                {/* Temperature */}
                {agentDetails.supportsCustomPrompts && (
                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <Label htmlFor="temperature">
                        <Target className="h-4 w-4 inline mr-1" />
                        Temperature
                      </Label>
                      <span className="text-sm text-muted-foreground">
                        {getConfigValue('temperature', 0.7)}
                      </span>
                    </div>
                    <Slider
                      id="temperature"
                      min={0}
                      max={1}
                      step={0.1}
                      value={[getConfigValue('temperature', 0.7)]}
                      onValueChange={([value]) => handleAgentChange('temperature', value)}
                      className="w-full"
                    />
                    <p className="text-sm text-muted-foreground">
                      Controls randomness: 0 = focused, 1 = creative
                    </p>
                  </div>
                )}

                {/* Timeout and Retries */}
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="timeout">
                      <Clock className="h-4 w-4 inline mr-1" />
                      Timeout (seconds)
                    </Label>
                    <Input
                      id="timeout"
                      type="number"
                      min={10}
                      max={600}
                      value={currentAgent.timeout_seconds}
                      onChange={(e) => handleAgentChange('timeout_seconds', parseInt(e.target.value))}
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="retries">
                      <RefreshCw className="h-4 w-4 inline mr-1" />
                      Max Retries
                    </Label>
                    <Input
                      id="retries"
                      type="number"
                      min={0}
                      max={10}
                      value={currentAgent.max_retries}
                      onChange={(e) => handleAgentChange('max_retries', parseInt(e.target.value))}
                    />
                  </div>
                </div>

                {/* Max Tokens */}
                {agentDetails.supportsCustomPrompts && (
                  <div className="space-y-2">
                    <Label htmlFor="max-tokens">Max Output Tokens (Optional)</Label>
                    <Input
                      id="max-tokens"
                      type="number"
                      min={100}
                      max={8000}
                      value={getConfigValue('max_tokens', '')}
                      placeholder="Default: Model maximum"
                      onChange={(e) => handleAgentChange('max_tokens', e.target.value ? parseInt(e.target.value) : null)}
                    />
                    <p className="text-sm text-muted-foreground">
                      Limit output length (leave empty for model default)
                    </p>
                  </div>
                )}

                {/* Custom Prompts */}
                {agentDetails.supportsCustomPrompts && (
                  <div className="space-y-2">
                    <Label htmlFor="custom-prompts">Custom System Prompt (Optional)</Label>
                    <Textarea
                      id="custom-prompts"
                      rows={6}
                      value={getConfigValue('custom_prompts', '')}
                      placeholder="Enter custom instructions for this agent..."
                      onChange={(e) => handleAgentChange('custom_prompts', e.target.value || null)}
                    />
                    <p className="text-sm text-muted-foreground">
                      Override default prompts with custom instructions for this agent
                    </p>
                  </div>
                )}
              </>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Cost Estimation */}
      <Alert>
        <DollarSign className="h-4 w-4" />
        <AlertDescription>
          <strong>Estimated Monthly Cost:</strong> ${calculateMonthlyEstimate().toFixed(2)} 
          (based on 100 articles/month with current agent configuration)
        </AlertDescription>
      </Alert>

      {/* Agent Status Summary */}
      <Card>
        <CardHeader>
          <CardTitle>Pipeline Status</CardTitle>
          <CardDescription>
            Overview of all agents in your content generation pipeline
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {Object.entries(AGENT_DETAILS).map(([key, details]) => {
              const agent = agents[key as keyof AgentSettings]
              const Icon = details.icon
              
              return (
                <div key={key} className="flex items-center justify-between py-2 border-b last:border-b-0">
                  <div className="flex items-center gap-3">
                    <Icon className="h-4 w-4" />
                    <div>
                      <span className="font-medium text-sm">{details.name}</span>
                      <p className="text-xs text-muted-foreground">${details.costEstimate}/article</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    {agent.enabled ? (
                      <span className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-green-100 text-green-800">
                        <span className="h-1.5 w-1.5 bg-green-500 rounded-full mr-1"></span>
                        Active
                      </span>
                    ) : (
                      <span className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-gray-100 text-gray-800">
                        <span className="h-1.5 w-1.5 bg-gray-500 rounded-full mr-1"></span>
                        Disabled
                      </span>
                    )}
                  </div>
                </div>
              )
            })}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
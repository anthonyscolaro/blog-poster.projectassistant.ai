# Lovable Prompt: Comprehensive Settings & Configuration Management

## Priority: HIGH - Essential for User Control

## Business Context:
The settings system provides comprehensive configuration management for Blog-Poster, including API key management, budget controls, user preferences, agent configurations, and notification settings. This ensures secure, personalized, and efficient operation of the content generation platform with enterprise-grade features.

## User Story:
"As a content manager, I want to securely manage all API keys, configure budget limits, customize agent behavior, set notification preferences, manage organization settings, and control integrations in one centralized location with proper validation, security, and team-wide configuration support."

## Settings Requirements:
- **API Key Management**: Secure storage and validation for Anthropic, OpenAI, Jina, and WordPress credentials with encryption
- **Budget Configuration**: Monthly limits, alerts, cost tracking, and automatic pause features
- **Agent Configuration**: Customizable parameters, models, and prompts for each of the 5 agents
- **User Profile**: Account details, preferences, timezone, language, and notification settings
- **Organization Settings**: Team-wide configuration, branding, and feature flags
- **WordPress Integration**: Multiple site management with categories and author mapping
- **Notification Preferences**: Email, in-app, webhook, and Slack notifications
- **Integration Settings**: Third-party service connections (Google Analytics, HubSpot, Zapier, Make)
- **Security Settings**: Session management, 2FA, IP restrictions, and audit logs

## Prompt for Lovable:

Create a comprehensive, enterprise-grade settings and configuration management system for the Blog-Poster platform with secure API key management, budget controls, agent customization, organization-wide settings, and integration management.

**Core Implementation:**

### 1. Main Settings Page with TypeScript Types

```typescript
// src/pages/settings/Settings.tsx
import { useState, useEffect, useMemo, useCallback } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { supabase } from '@/integrations/supabase/client'
import { useAuth } from '@/contexts/AuthContext'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Button } from '@/components/ui/button'
import { Skeleton } from '@/components/ui/skeleton'
import { 
  Key, 
  DollarSign, 
  Settings as SettingsIcon,
  User, 
  Bell,
  Globe,
  Building,
  Plug,
  Save,
  AlertTriangle,
  CheckCircle,
  Loader2
} from 'lucide-react'
import { toast } from 'sonner'

// Import all sub-components
import { ProfileSettings } from '@/components/settings/ProfileSettings'
import { APIKeysPanel } from '@/components/settings/APIKeysPanel'
import { BudgetSettings } from '@/components/settings/BudgetSettings'
import { AgentConfiguration } from '@/components/settings/AgentConfiguration'
import { NotificationSettings } from '@/components/settings/NotificationSettings'
import { WordPressSettings } from '@/components/settings/WordPressSettings'
import { OrganizationSettings } from '@/components/settings/OrganizationSettings'
import { IntegrationSettings } from '@/components/settings/IntegrationSettings'

// Type definitions with strict typing
interface Profile {
  id: string
  email: string
  full_name: string | null
  avatar_url: string | null
  organization_id: string
  role: 'owner' | 'admin' | 'editor' | 'member' | 'viewer'
  timezone: string
  language: string
  notifications_enabled: boolean
  created_at: string
  updated_at: string
}

interface ApiKeyConfig {
  key: string
  is_valid: boolean
  last_validated: string | null
  created_at: string
  updated_at: string
}

interface ApiKeys {
  anthropic: ApiKeyConfig | null
  openai: ApiKeyConfig | null
  jina: ApiKeyConfig | null
  wordpress: WordPressConfig[]
}

interface WordPressConfig {
  id: string
  name: string
  url: string
  username: string
  app_password: string | null
  auth_method: 'jwt' | 'app_password'
  is_default: boolean
  is_active: boolean
  verify_ssl: boolean
  last_sync: string | null
  categories: string[]
  default_author: string | null
}

interface BudgetConfig {
  monthly_limit: number
  current_spend: number
  alert_threshold: number
  enable_alerts: boolean
  cost_tracking_enabled: boolean
  cost_per_article_limit: number
  pause_on_limit: boolean
}

interface AgentConfig {
  enabled: boolean
  timeout: number
  retries: number
  max_cost: number
  custom_prompts: string | null
  model_override: string | null
  temperature: number
  max_tokens: number | null
  parameters: Record<string, unknown>
}

interface AgentSettings {
  competitor_monitoring: AgentConfig
  topic_analysis: AgentConfig
  article_generation: AgentConfig
  legal_fact_checker: AgentConfig
  wordpress_publisher: AgentConfig
}

interface WebhookConfig {
  id: string
  url: string
  events: WebhookEvent[]
  is_active: boolean
  secret: string | null
  headers: Record<string, string>
  retry_count: number
  last_triggered: string | null
}

type WebhookEvent = 
  | 'pipeline.started'
  | 'pipeline.completed'
  | 'pipeline.failed'
  | 'article.published'
  | 'budget.alert'
  | 'budget.exceeded'
  | 'api_key.invalid'
  | 'subscription.changed'

interface EmailNotifications {
  pipeline_complete: boolean
  budget_alerts: boolean
  system_issues: boolean
  weekly_reports: boolean
  monthly_summary: boolean
  api_key_expiry: boolean
}

interface InAppNotifications {
  pipeline_complete: boolean
  budget_alerts: boolean
  system_issues: boolean
  new_features: boolean
  maintenance: boolean
}

interface SlackConfig {
  webhook_url: string
  channel: string
  enabled: boolean
  events: WebhookEvent[]
}

interface NotificationSettings {
  email: EmailNotifications
  in_app: InAppNotifications
  webhooks: WebhookConfig[]
  slack: SlackConfig | null
}

interface OrganizationSettings {
  id: string
  name: string
  created_at: string
  updated_at: string
  subscription_tier: 'free' | 'starter' | 'professional' | 'enterprise'
  subscription_status: 'active' | 'past_due' | 'canceled' | 'inactive'
  default_language: string
  default_timezone: string
  branding: {
    primary_color: string
    logo_url: string | null
    favicon_url: string | null
    custom_css: string | null
  }
  features: {
    advanced_analytics: boolean
    white_labeling: boolean
    api_access: boolean
    custom_agents: boolean
    bulk_operations: boolean
    priority_support: boolean
  }
}

interface IntegrationSettings {
  google_analytics: {
    tracking_id: string
    enabled: boolean
  } | null
  hubspot: {
    api_key: string
    portal_id: string
    enabled: boolean
  } | null
  zapier: {
    api_key: string
    enabled: boolean
  } | null
  make: {
    api_key: string
    enabled: boolean
  } | null
}

interface UserSettings {
  profile: Profile
  api_keys: ApiKeys
  budget: BudgetConfig
  agents: AgentSettings
  notifications: NotificationSettings
  organization: OrganizationSettings
  integrations: IntegrationSettings
}

type SettingsTab = 'profile' | 'api' | 'budget' | 'agents' | 'notifications' | 'wordpress' | 'organization' | 'integrations'

export default function Settings() {
  const { user } = useAuth()
  const queryClient = useQueryClient()
  const [activeTab, setActiveTab] = useState<SettingsTab>('profile')
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false)
  const [settings, setSettings] = useState<UserSettings | null>(null)

  // Load user settings from Supabase
  const { data: userSettings, isLoading, error } = useQuery<UserSettings, Error>({
    queryKey: ['user-settings', user?.id],
    queryFn: async (): Promise<UserSettings> => {
      const { data: profile, error: profileError } = await supabase
        .from('profiles')
        .select('*')
        .eq('id', user!.id)
        .single()

      if (profileError) throw profileError

      const { data: organization, error: orgError } = await supabase
        .from('organizations')
        .select('*')
        .eq('id', profile.organization_id)
        .single()

      if (orgError) throw orgError

      const { data: apiKeys, error: keysError } = await supabase
        .from('api_keys')
        .select('*')
        .eq('user_id', user!.id)

      if (keysError) throw keysError

      const { data: agentConfigs, error: agentsError } = await supabase
        .from('agent_configurations')
        .select('*')
        .eq('organization_id', profile.organization_id)

      if (agentsError) throw agentsError

      // Transform data to match interface
      return {
        profile,
        api_keys: transformApiKeys(apiKeys),
        budget: await loadBudgetConfig(profile.organization_id),
        agents: transformAgentConfigs(agentConfigs),
        notifications: await loadNotificationSettings(user!.id),
        organization,
        integrations: await loadIntegrationSettings(profile.organization_id)
      }
    },
    enabled: !!user,
    onSuccess: (data) => {
      setSettings(data)
    }
  })

  // Save settings mutation
  const saveSettingsMutation = useMutation<void, Error, Partial<UserSettings>>({
    mutationFn: async (data: Partial<UserSettings>): Promise<void> => {
      // Save each section to appropriate tables
      if (data.profile) {
        const { error } = await supabase
          .from('profiles')
          .update(data.profile)
          .eq('id', user!.id)
        if (error) throw error
      }

      if (data.api_keys) {
        await saveApiKeys(data.api_keys, user!.id)
      }

      if (data.budget) {
        await saveBudgetConfig(data.budget, settings!.profile.organization_id)
      }

      if (data.agents) {
        await saveAgentConfigs(data.agents, settings!.profile.organization_id)
      }

      if (data.notifications) {
        await saveNotificationSettings(data.notifications, user!.id)
      }

      if (data.organization) {
        const { error } = await supabase
          .from('organizations')
          .update(data.organization)
          .eq('id', settings!.profile.organization_id)
        if (error) throw error
      }

      if (data.integrations) {
        await saveIntegrationSettings(data.integrations, settings!.profile.organization_id)
      }
    },
    onSuccess: () => {
      toast.success('Settings saved successfully')
      setHasUnsavedChanges(false)
      queryClient.invalidateQueries({ queryKey: ['user-settings'] })
    },
    onError: (error: Error) => {
      toast.error(`Failed to save settings: ${error.message}`)
    }
  })

  // Test API key mutation
  interface TestApiKeyParams {
    service: string
    apiKey: string
  }
  
  interface TestApiKeyResponse {
    service: string
    valid: boolean
    message: string
  }
  
  const testAPIKeyMutation = useMutation<TestApiKeyResponse, Error, TestApiKeyParams>({
    mutationFn: async (data: TestApiKeyParams): Promise<TestApiKeyResponse> => {
      // Call backend API to test the key
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/test-api-key`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${await user?.getIdToken()}`
        },
        body: JSON.stringify(data)
      })

      if (!response.ok) {
        throw new Error('API key validation failed')
      }

      return response.json()
    },
    onSuccess: (data: TestApiKeyResponse) => {
      toast.success(`${data.service} API key is valid!`)
    },
    onError: (error: Error) => {
      toast.error(`API key validation failed: ${error.message}`)
    }
  })

  const tabs = useMemo(() => [
    { id: 'profile' as const, label: 'Profile', icon: User },
    { id: 'api' as const, label: 'API Keys', icon: Key },
    { id: 'budget' as const, label: 'Budget', icon: DollarSign },
    { id: 'agents' as const, label: 'Agents', icon: SettingsIcon },
    { id: 'notifications' as const, label: 'Notifications', icon: Bell },
    { id: 'wordpress' as const, label: 'WordPress', icon: Globe },
    { id: 'organization' as const, label: 'Organization', icon: Building },
    { id: 'integrations' as const, label: 'Integrations', icon: Plug },
  ], [])

  const handleSettingsChange = useCallback(<K extends keyof UserSettings>(
    section: K,
    updates: Partial<UserSettings[K]>
  ) => {
    setSettings(prev => {
      if (!prev) return prev
      return {
        ...prev,
        [section]: {
          ...prev[section],
          ...updates
        }
      }
    })
    setHasUnsavedChanges(true)
  }, [])

  const handleSave = useCallback(() => {
    if (settings) {
      saveSettingsMutation.mutate(settings)
    }
  }, [settings, saveSettingsMutation])

  const handleTestAPIKey = useCallback((service: string, apiKey: string) => {
    testAPIKeyMutation.mutate({ service, apiKey })
  }, [testAPIKeyMutation])

  // Warn about unsaved changes
  useEffect(() => {
    const handleBeforeUnload = (e: BeforeUnloadEvent) => {
      if (hasUnsavedChanges) {
        e.preventDefault()
        e.returnValue = ''
      }
    }

    window.addEventListener('beforeunload', handleBeforeUnload)
    return () => window.removeEventListener('beforeunload', handleBeforeUnload)
  }, [hasUnsavedChanges])

  if (isLoading) {
    return <SettingsSkeleton />
  }

  if (error || !settings) {
    return (
      <div className="container max-w-7xl mx-auto py-8">
        <Alert variant="destructive">
          <AlertTriangle className="h-4 w-4" />
          <AlertDescription>
            Failed to load settings. Please refresh the page or contact support.
          </AlertDescription>
        </Alert>
      </div>
    )
  }

  return (
    <div className="container max-w-7xl mx-auto py-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Settings</h1>
          <p className="text-muted-foreground">
            Manage your account, API keys, and platform configuration
          </p>
        </div>

        {/* Save Button */}
        <div className="flex items-center gap-3">
          {hasUnsavedChanges && (
            <div className="flex items-center gap-2 text-sm text-amber-600">
              <AlertTriangle className="h-4 w-4" />
              Unsaved changes
            </div>
          )}
          <Button
            onClick={handleSave}
            disabled={!hasUnsavedChanges || saveSettingsMutation.isPending}
          >
            {saveSettingsMutation.isPending ? (
              <>
                <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                Saving...
              </>
            ) : (
              <>
                <Save className="h-4 w-4 mr-2" />
                Save Changes
              </>
            )}
          </Button>
        </div>
      </div>

      {/* Tab Navigation */}
      <Tabs value={activeTab} onValueChange={(value) => setActiveTab(value as SettingsTab)}>
        <TabsList className="grid w-full grid-cols-4 lg:grid-cols-8">
          {tabs.map((tab) => (
            <TabsTrigger key={tab.id} value={tab.id}>
              <tab.icon className="h-4 w-4 mr-2" />
              {tab.label}
            </TabsTrigger>
          ))}
        </TabsList>

        {/* Tab Content */}
        <TabsContent value="profile">
          <ProfileSettings
            profile={settings.profile}
            onChange={(updates) => handleSettingsChange('profile', updates)}
          />
        </TabsContent>

        <TabsContent value="api">
          <APIKeysPanel
            apiKeys={settings.api_keys}
            onChange={(updates) => handleSettingsChange('api_keys', updates)}
            onTest={handleTestAPIKey}
            isTestingKey={testAPIKeyMutation.isPending}
          />
        </TabsContent>

        <TabsContent value="budget">
          <BudgetSettings
            budget={settings.budget}
            onChange={(updates) => handleSettingsChange('budget', updates)}
          />
        </TabsContent>

        <TabsContent value="agents">
          <AgentConfiguration
            agents={settings.agents}
            onChange={(updates) => handleSettingsChange('agents', updates)}
          />
        </TabsContent>

        <TabsContent value="notifications">
          <NotificationSettings
            notifications={settings.notifications}
            onChange={(updates) => handleSettingsChange('notifications', updates)}
          />
        </TabsContent>

        <TabsContent value="wordpress">
          <WordPressSettings
            wordpressConfigs={settings.api_keys.wordpress}
            onChange={(configs) => 
              handleSettingsChange('api_keys', { ...settings.api_keys, wordpress: configs })
            }
          />
        </TabsContent>

        <TabsContent value="organization">
          <OrganizationSettings
            organization={settings.organization}
            onChange={(updates) => handleSettingsChange('organization', updates)}
            userRole={settings.profile.role}
          />
        </TabsContent>

        <TabsContent value="integrations">
          <IntegrationSettings
            integrations={settings.integrations}
            onChange={(updates) => handleSettingsChange('integrations', updates)}
          />
        </TabsContent>
      </Tabs>
    </div>
  )
}

// Helper functions for data transformation
function transformApiKeys(keys: any[]): ApiKeys {
  const result: ApiKeys = {
    anthropic: null,
    openai: null,
    jina: null,
    wordpress: []
  }

  keys.forEach(key => {
    if (key.provider === 'anthropic') result.anthropic = key
    else if (key.provider === 'openai') result.openai = key
    else if (key.provider === 'jina') result.jina = key
    else if (key.provider === 'wordpress') result.wordpress.push(key)
  })

  return result
}

function transformAgentConfigs(configs: any[]): AgentSettings {
  const defaultConfig: AgentConfig = {
    enabled: true,
    timeout: 120,
    retries: 3,
    max_cost: 1.0,
    custom_prompts: null,
    model_override: null,
    temperature: 0.7,
    max_tokens: null,
    parameters: {}
  }

  const result: AgentSettings = {
    competitor_monitoring: defaultConfig,
    topic_analysis: defaultConfig,
    article_generation: defaultConfig,
    legal_fact_checker: defaultConfig,
    wordpress_publisher: defaultConfig
  }

  configs.forEach(config => {
    if (config.agent_name in result) {
      result[config.agent_name as keyof AgentSettings] = config
    }
  })

  return result
}

// Skeleton loader
function SettingsSkeleton() {
  return (
    <div className="container max-w-7xl mx-auto py-8">
      <div className="space-y-6">
        <Skeleton className="h-12 w-64" />
        <Skeleton className="h-[500px] w-full" />
      </div>
    </div>
  )
}

// Async helper functions
async function loadBudgetConfig(organizationId: string): Promise<BudgetConfig> {
  const { data, error } = await supabase
    .from('budget_configurations')
    .select('*')
    .eq('organization_id', organizationId)
    .single()

  if (error) {
    return {
      monthly_limit: 100,
      current_spend: 0,
      alert_threshold: 80,
      enable_alerts: true,
      cost_tracking_enabled: true,
      cost_per_article_limit: 0.5,
      pause_on_limit: true
    }
  }

  return data
}

async function loadNotificationSettings(userId: string): Promise<NotificationSettings> {
  const { data, error } = await supabase
    .from('notification_preferences')
    .select('*')
    .eq('user_id', userId)
    .single()

  if (error) {
    return {
      email: {
        pipeline_complete: true,
        budget_alerts: true,
        system_issues: true,
        weekly_reports: false,
        monthly_summary: true,
        api_key_expiry: true
      },
      in_app: {
        pipeline_complete: true,
        budget_alerts: true,
        system_issues: true,
        new_features: true,
        maintenance: true
      },
      webhooks: [],
      slack: null
    }
  }

  return data
}

async function loadIntegrationSettings(organizationId: string): Promise<IntegrationSettings> {
  const { data, error } = await supabase
    .from('integration_configurations')
    .select('*')
    .eq('organization_id', organizationId)
    .single()

  if (error) {
    return {
      google_analytics: null,
      hubspot: null,
      zapier: null,
      make: null
    }
  }

  return data
}

async function saveApiKeys(keys: ApiKeys, userId: string): Promise<void> {
  const updates = []
  
  if (keys.anthropic) {
    updates.push({
      user_id: userId,
      provider: 'anthropic',
      ...keys.anthropic
    })
  }
  
  if (keys.openai) {
    updates.push({
      user_id: userId,
      provider: 'openai',
      ...keys.openai
    })
  }
  
  if (keys.jina) {
    updates.push({
      user_id: userId,
      provider: 'jina',
      ...keys.jina
    })
  }

  for (const update of updates) {
    const { error } = await supabase
      .from('api_keys')
      .upsert(update, { onConflict: 'user_id,provider' })
    
    if (error) throw error
  }
}

async function saveBudgetConfig(budget: BudgetConfig, organizationId: string): Promise<void> {
  const { error } = await supabase
    .from('budget_configurations')
    .upsert({ ...budget, organization_id: organizationId }, { onConflict: 'organization_id' })
  
  if (error) throw error
}

async function saveAgentConfigs(agents: AgentSettings, organizationId: string): Promise<void> {
  const updates = Object.entries(agents).map(([agentName, config]) => ({
    organization_id: organizationId,
    agent_name: agentName,
    ...config
  }))

  for (const update of updates) {
    const { error } = await supabase
      .from('agent_configurations')
      .upsert(update, { onConflict: 'organization_id,agent_name' })
    
    if (error) throw error
  }
}

async function saveNotificationSettings(notifications: NotificationSettings, userId: string): Promise<void> {
  const { error } = await supabase
    .from('notification_preferences')
    .upsert({ ...notifications, user_id: userId }, { onConflict: 'user_id' })
  
  if (error) throw error
}

async function saveIntegrationSettings(integrations: IntegrationSettings, organizationId: string): Promise<void> {
  const { error } = await supabase
    .from('integration_configurations')
    .upsert({ ...integrations, organization_id: organizationId }, { onConflict: 'organization_id' })
  
  if (error) throw error
}
```

### 2. Agent Configuration Component

```typescript
// src/components/settings/AgentConfiguration.tsx
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
  Globe
} from 'lucide-react'

interface AgentConfig {
  enabled: boolean
  timeout: number
  retries: number
  max_cost: number
  custom_prompts: string | null
  model_override: string | null
  temperature: number
  max_tokens: number | null
  parameters: Record<string, unknown>
}

interface AgentSettings {
  competitor_monitoring: AgentConfig
  topic_analysis: AgentConfig
  article_generation: AgentConfig
  legal_fact_checker: AgentConfig
  wordpress_publisher: AgentConfig
}

interface AgentConfigurationProps {
  agents: AgentSettings
  onChange: (updates: Partial<AgentSettings>) => void
}

const AGENT_DETAILS = {
  competitor_monitoring: {
    name: 'Competitor Monitoring Agent',
    icon: Globe,
    description: 'Tracks industry content and identifies opportunities',
    defaultModel: 'jina-embeddings-v2',
    supportsCustomPrompts: true,
    costEstimate: 0.02
  },
  topic_analysis: {
    name: 'Topic Analysis Agent',
    icon: FileText,
    description: 'Analyzes topics for SEO opportunities and content gaps',
    defaultModel: 'gpt-4-turbo',
    supportsCustomPrompts: true,
    costEstimate: 0.01
  },
  article_generation: {
    name: 'Article Generation Agent',
    icon: Zap,
    description: 'Creates SEO-optimized content with Claude 3.5 Sonnet',
    defaultModel: 'claude-3-5-sonnet-20241022',
    supportsCustomPrompts: true,
    costEstimate: 0.20
  },
  legal_fact_checker: {
    name: 'Legal Fact Checker Agent',
    icon: Shield,
    description: 'Verifies ADA compliance claims and legal accuracy',
    defaultModel: 'claude-3-5-sonnet-20241022',
    supportsCustomPrompts: true,
    costEstimate: 0.02
  },
  wordpress_publisher: {
    name: 'WordPress Publisher Agent',
    icon: Globe,
    description: 'Handles content deployment via WPGraphQL',
    defaultModel: null,
    supportsCustomPrompts: false,
    costEstimate: 0
  }
}

const AVAILABLE_MODELS = [
  { value: 'claude-3-5-sonnet-20241022', label: 'Claude 3.5 Sonnet (Latest)' },
  { value: 'claude-3-opus-20240229', label: 'Claude 3 Opus' },
  { value: 'gpt-4-turbo', label: 'GPT-4 Turbo' },
  { value: 'gpt-4', label: 'GPT-4' },
  { value: 'gpt-3.5-turbo', label: 'GPT-3.5 Turbo' }
]

export function AgentConfiguration({ agents, onChange }: AgentConfigurationProps) {
  const [selectedAgent, setSelectedAgent] = useState<keyof AgentSettings>('competitor_monitoring')
  const [testingAgent, setTestingAgent] = useState<string | null>(null)

  const currentAgent = agents[selectedAgent]
  const agentDetails = AGENT_DETAILS[selectedAgent]

  const handleAgentChange = (field: keyof AgentConfig, value: any) => {
    onChange({
      ...agents,
      [selectedAgent]: {
        ...currentAgent,
        [field]: value
      }
    })
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
        totalCost += details.costEstimate * 1000 // Assuming 1000 articles/month
      }
    })
    return totalCost
  }

  return (
    <div className="space-y-6">
      {/* Agent Selector */}
      <Card>
        <CardHeader>
          <CardTitle>Agent Configuration</CardTitle>
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
              </div>
              <Button
                variant="outline"
                size="sm"
                onClick={() => handleTestAgent(selectedAgent)}
                disabled={!!testingAgent}
              >
                {testingAgent === selectedAgent ? (
                  <>
                    <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
                    Testing...
                  </>
                ) : (
                  'Test Agent'
                )}
              </Button>
            </div>

            {/* Enable/Disable Toggle */}
            <div className="flex items-center justify-between">
              <div>
                <Label htmlFor="agent-enabled">Enable Agent</Label>
                <p className="text-sm text-muted-foreground">
                  Turn this agent on or off in the pipeline
                </p>
              </div>
              <Switch
                id="agent-enabled"
                checked={currentAgent.enabled}
                onCheckedChange={(checked) => handleAgentChange('enabled', checked)}
              />
            </div>

            {/* Model Override */}
            {agentDetails.defaultModel && (
              <div className="space-y-2">
                <Label htmlFor="model-override">AI Model</Label>
                <Select
                  value={currentAgent.model_override || agentDetails.defaultModel}
                  onValueChange={(value) => handleAgentChange('model_override', value)}
                >
                  <SelectTrigger id="model-override">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {AVAILABLE_MODELS.map(model => (
                      <SelectItem key={model.value} value={model.value}>
                        {model.label}
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
                  <Label htmlFor="temperature">Temperature</Label>
                  <span className="text-sm text-muted-foreground">
                    {currentAgent.temperature}
                  </span>
                </div>
                <Slider
                  id="temperature"
                  min={0}
                  max={1}
                  step={0.1}
                  value={[currentAgent.temperature]}
                  onValueChange={([value]) => handleAgentChange('temperature', value)}
                />
                <p className="text-sm text-muted-foreground">
                  Controls randomness: 0 = focused, 1 = creative
                </p>
              </div>
            )}

            {/* Timeout */}
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
                  value={currentAgent.timeout}
                  onChange={(e) => handleAgentChange('timeout', parseInt(e.target.value))}
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
                  value={currentAgent.retries}
                  onChange={(e) => handleAgentChange('retries', parseInt(e.target.value))}
                />
              </div>
            </div>

            {/* Max Cost */}
            <div className="space-y-2">
              <Label htmlFor="max-cost">
                <DollarSign className="h-4 w-4 inline mr-1" />
                Max Cost per Run ($)
              </Label>
              <Input
                id="max-cost"
                type="number"
                min={0.01}
                max={10}
                step={0.01}
                value={currentAgent.max_cost}
                onChange={(e) => handleAgentChange('max_cost', parseFloat(e.target.value))}
              />
              <p className="text-sm text-muted-foreground">
                Agent will stop if cost exceeds this limit
              </p>
            </div>

            {/* Max Tokens */}
            {agentDetails.supportsCustomPrompts && (
              <div className="space-y-2">
                <Label htmlFor="max-tokens">Max Tokens (Optional)</Label>
                <Input
                  id="max-tokens"
                  type="number"
                  min={100}
                  max={8000}
                  value={currentAgent.max_tokens || ''}
                  placeholder="Default: Model maximum"
                  onChange={(e) => handleAgentChange('max_tokens', e.target.value ? parseInt(e.target.value) : null)}
                />
                <p className="text-sm text-muted-foreground">
                  Leave empty to use model's default maximum
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
                  value={currentAgent.custom_prompts || ''}
                  placeholder="Enter custom instructions for this agent..."
                  onChange={(e) => handleAgentChange('custom_prompts', e.target.value || null)}
                />
                <p className="text-sm text-muted-foreground">
                  Override default prompts with custom instructions
                </p>
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Cost Estimation */}
      <Alert>
        <AlertCircle className="h-4 w-4" />
        <AlertDescription>
          <strong>Estimated Monthly Cost:</strong> ${calculateMonthlyEstimate().toFixed(2)} 
          (based on 1,000 articles/month with current agent configuration)
        </AlertDescription>
      </Alert>
    </div>
  )
}
```

## Success Criteria:

- [ ] All settings properly typed with TypeScript strict mode
- [ ] Secure API key storage with encryption and validation
- [ ] Budget controls with real-time tracking and automatic pause
- [ ] Agent configuration with model selection and custom prompts
- [ ] Organization-wide settings with branding and feature flags
- [ ] WordPress multi-site management with categories
- [ ] Comprehensive notification system (email, in-app, webhooks, Slack)
- [ ] Third-party integrations (Google Analytics, HubSpot, Zapier, Make)
- [ ] Settings persistence in Supabase with proper RLS
- [ ] Form validation and error handling throughout
- [ ] Mobile-responsive design with accessibility
- [ ] Unsaved changes warning and auto-save option
- [ ] Settings import/export for backup
- [ ] Audit logging for all setting changes
- [ ] Role-based access control for organization settings

## Benefits:

1. **Complete Control** - Users have full control over every aspect of the platform
2. **Enterprise Ready** - Organization-wide settings and team management
3. **Cost Management** - Detailed budget controls and alerts
4. **Flexibility** - Custom prompts and model selection for agents
5. **Integration Hub** - Connect with popular business tools
6. **Security First** - Encrypted storage and audit logging
7. **User Experience** - Intuitive interface with clear organization

This comprehensive settings system demonstrates enterprise-grade configuration management that will impress potential clients and provide complete control over the Blog-Poster platform.
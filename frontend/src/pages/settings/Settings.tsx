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

// Use the actual Profile type from Auth context and extend it
interface ExtendedProfile {
  id: string
  email: string
  full_name: string | null
  avatar_url: string | null
  organization_id: string
  role: 'owner' | 'admin' | 'editor' | 'member'
  onboarding_completed: boolean
  two_factor_enabled: boolean
  timezone?: string
  notification_preferences?: Record<string, boolean>
  created_at?: string
  updated_at?: string
}

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
  wordpress: WordPressConfig[]
}

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

interface ExtendedOrganization {
  id: string
  name: string
  slug: string
  plan: 'free' | 'starter' | 'professional' | 'enterprise'
  subscription_status: string
  trial_ends_at: string | null
  articles_limit: number
  articles_used: number
  monthly_budget: number
  current_month_cost: number
  budget_alert_threshold?: number
}

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

interface NotificationConfig {
  email: boolean
  browser: boolean
  webhook: boolean
  slack: boolean
}

interface UserSettings {
  profile: ExtendedProfile
  api_keys: ApiKeys
  budget: ExtendedOrganization
  agents: AgentSettings
  notifications: NotificationConfig
  organization: ExtendedOrganization
}

type SettingsTab = 'profile' | 'api' | 'budget' | 'agents' | 'notifications' | 'wordpress' | 'organization' | 'integrations'

export default function Settings() {
  const { user, profile, organization } = useAuth()
  const queryClient = useQueryClient()
  const [activeTab, setActiveTab] = useState<SettingsTab>('profile')
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false)
  const [settings, setSettings] = useState<UserSettings | null>(null)

  // Load user settings from Supabase
  const { data: userSettings, isLoading, error } = useQuery({
    queryKey: ['user-settings', user?.id],
    queryFn: async (): Promise<UserSettings> => {
      if (!user || !profile) throw new Error('User not authenticated')

      // Load API keys
      const { data: apiKeysData, error: keysError } = await supabase
        .from('organization_api_keys')
        .select('*')
        .eq('organization_id', profile.organization_id)

      if (keysError) throw keysError

      // Load agent configs
      const { data: agentConfigsData, error: agentsError } = await supabase
        .from('agent_configs')
        .select('*')
        .eq('organization_id', profile.organization_id)

      if (agentsError) throw agentsError

      // Transform data to match interface
      return {
        profile: {
          ...profile,
          timezone: (profile as any).timezone || 'America/New_York',
          notification_preferences: (profile as any).notification_preferences || {},
          created_at: (profile as any).created_at || new Date().toISOString(),
          updated_at: (profile as any).updated_at || new Date().toISOString()
        } as ExtendedProfile,
        api_keys: transformApiKeys(apiKeysData || []),
        budget: {
          ...organization,
          budget_alert_threshold: (organization as any)?.budget_alert_threshold || 80
        } as ExtendedOrganization,
        agents: transformAgentConfigs(agentConfigsData || []),
        notifications: ((profile as any).notification_preferences as NotificationConfig) || {
          email: true,
          browser: true,
          webhook: false,
          slack: false
        },
        organization: {
          ...organization,
          budget_alert_threshold: (organization as any)?.budget_alert_threshold || 80
        } as ExtendedOrganization
      }
    },
    enabled: !!user && !!profile
  })

  // Set settings when data changes
  useEffect(() => {
    if (userSettings) {
      setSettings(userSettings)
    }
  }, [userSettings])

  // Save settings mutation
  const saveSettingsMutation = useMutation({
    mutationFn: async (data: Partial<UserSettings>): Promise<void> => {
      if (!user || !profile) throw new Error('User not authenticated')

      // Save profile updates
      if (data.profile) {
        const { error } = await supabase
          .from('profiles')
          .update({
            full_name: data.profile.full_name,
            timezone: data.profile.timezone,
            notification_preferences: data.profile.notification_preferences,
            updated_at: new Date().toISOString()
          })
          .eq('id', user.id)
        if (error) throw error
      }

      // Save API keys
      if (data.api_keys) {
        await saveApiKeys(data.api_keys, profile.organization_id)
      }

      // Save agent configs
      if (data.agents) {
        await saveAgentConfigs(data.agents, profile.organization_id)
      }

      // Save budget settings (organization level)
      if (data.budget) {
        const { error } = await supabase
          .from('organizations')
          .update({
            monthly_budget: data.budget.monthly_budget,
            budget_alert_threshold: data.budget.budget_alert_threshold,
            articles_limit: data.budget.articles_limit,
            updated_at: new Date().toISOString()
          })
          .eq('id', profile.organization_id)
        if (error) throw error
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
            integrations={{}}
            onChange={() => {}}
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
    if (key.service === 'anthropic') result.anthropic = key
    else if (key.service === 'openai') result.openai = key
    else if (key.service === 'jina') result.jina = key
    else if (key.service === 'wordpress') result.wordpress.push(key)
  })

  return result
}

function transformAgentConfigs(configs: any[]): AgentSettings {
  const defaultConfig: AgentConfig = {
    enabled: true,
    timeout_seconds: 120,
    max_retries: 3,
    config: {}
  }

  const result: AgentSettings = {
    competitor: defaultConfig,
    topic: defaultConfig,
    article: defaultConfig,
    legal: defaultConfig,
    wordpress: defaultConfig
  }

  configs.forEach(config => {
    if (config.agent_name in result) {
      result[config.agent_name as keyof AgentSettings] = {
        enabled: config.enabled,
        timeout_seconds: config.timeout_seconds,
        max_retries: config.max_retries,
        config: config.config
      }
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
async function saveApiKeys(keys: ApiKeys, organizationId: string): Promise<void> {
  const updates = []
  
  if (keys.anthropic) {
    updates.push({
      organization_id: organizationId,
      service: 'anthropic',
      ...keys.anthropic
    })
  }
  
  if (keys.openai) {
    updates.push({
      organization_id: organizationId,
      service: 'openai',
      ...keys.openai
    })
  }
  
  if (keys.jina) {
    updates.push({
      organization_id: organizationId,
      service: 'jina',
      ...keys.jina
    })
  }

  for (const update of updates) {
    const { error } = await supabase
      .from('organization_api_keys')
      .upsert(update, { onConflict: 'organization_id,service' })
    
    if (error) throw error
  }
}

async function saveAgentConfigs(agents: AgentSettings, organizationId: string): Promise<void> {
  const updates = Object.entries(agents).map(([agentName, config]) => ({
    organization_id: organizationId,
    agent_name: agentName,
    enabled: config.enabled,
    timeout_seconds: config.timeout_seconds,
    max_retries: config.max_retries,
    config: config.config
  }))

  for (const update of updates) {
    const { error } = await supabase
      .from('agent_configs')
      .upsert(update, { onConflict: 'organization_id,agent_name' })
    
    if (error) throw error
  }
}
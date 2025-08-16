# Lovable Prompt: Settings & Configuration Management

## Business Context:
The settings system provides comprehensive configuration management for Blog-Poster, including API key management, budget controls, user preferences, agent configurations, and notification settings. This ensures secure, personalized, and efficient operation of the content generation platform.

## User Story:
"As a content manager, I want to securely manage all API keys, configure budget limits, customize agent behavior, set notification preferences, and manage my profile settings in one centralized location with proper validation and security."

## Settings Requirements:
- **API Key Management**: Secure storage and validation for Anthropic, OpenAI, Jina, and WordPress credentials
- **Budget Configuration**: Monthly limits, alerts, and cost tracking settings
- **Agent Configuration**: Customizable parameters for each of the 5 agents
- **User Profile**: Account details, preferences, and security settings
- **Notification Preferences**: Email, in-app, and webhook notification controls
- **WordPress Integration**: Multiple site management and publishing settings

## Prompt for Lovable:

Create a comprehensive settings and configuration management system for the Blog-Poster platform that provides secure API key management, budget controls, agent customization, and user preferences with proper validation and encryption.

**Settings Components:**

### Main Settings Page
```typescript
// src/pages/Settings.tsx
import { useState, useEffect } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { apiClient } from '@/services/api'
import { APIKeysPanel } from '@/components/settings/APIKeysPanel'
import { BudgetSettings } from '@/components/settings/BudgetSettings'
import { AgentConfiguration } from '@/components/settings/AgentConfiguration'
import { UserProfile } from '@/components/settings/UserProfile'
import { NotificationSettings } from '@/components/settings/NotificationSettings'
import { WordPressSettings } from '@/components/settings/WordPressSettings'
import { SecuritySettings } from '@/components/settings/SecuritySettings'
import { 
  Key, 
  DollarSign, 
  Settings as SettingsIcon,
  User, 
  Bell,
  Globe,
  Shield,
  Save,
  AlertTriangle,
  CheckCircle
} from 'lucide-react'
import toast from 'react-hot-toast'

interface UserSettings {
  profile: {
    id: string
    email: string
    fullName: string
    company: string | null
    timezone: string
    language: string
    avatar: string | null
  }
  apiKeys: {
    anthropic: string | null
    openai: string | null
    jina: string | null
    wordpress: WordPressConfig[]
  }
  budget: {
    monthlyLimit: number
    currentSpend: number
    alertThreshold: number
    enableAlerts: boolean
    costTrackingEnabled: boolean
  }
  agents: {
    [key: string]: AgentConfig
  }
  notifications: {
    email: {
      pipelineComplete: boolean
      budgetAlerts: boolean
      systemIssues: boolean
      weeklyReports: boolean
    }
    inApp: {
      pipelineComplete: boolean
      budgetAlerts: boolean
      systemIssues: boolean
    }
    webhooks: WebhookConfig[]
  }
  security: {
    twoFactorEnabled: boolean
    sessionTimeout: number
    allowedIPs: string[]
    lastPasswordChange: string
  }
}

interface WordPressConfig {
  id: string
  name: string
  url: string
  username: string
  password: string | null
  authMethod: 'jwt' | 'app_password'
  isDefault: boolean
  isActive: boolean
}

interface AgentConfig {
  enabled: boolean
  timeout: number
  retries: number
  customPrompts: string | null
  parameters: { [key: string]: any }
}

interface WebhookConfig {
  id: string
  url: string
  events: string[]
  isActive: boolean
  secret: string | null
}

export default function Settings() {
  const [activeTab, setActiveTab] = useState<'profile' | 'api' | 'budget' | 'agents' | 'notifications' | 'wordpress' | 'security'>('profile')
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false)
  const [settings, setSettings] = useState<UserSettings | null>(null)
  const queryClient = useQueryClient()

  // Load user settings
  const { data: userSettings, isLoading, error } = useQuery({
    queryKey: ['user-settings'],
    queryFn: () => apiClient.get<UserSettings>('/api/user/settings'),
    onSuccess: (data) => {
      setSettings(data)
    }
  })

  // Save settings mutation
  const saveSettingsMutation = useMutation({
    mutationFn: (data: Partial<UserSettings>) =>
      apiClient.put('/api/user/settings', data),
    onSuccess: () => {
      toast.success('Settings saved successfully!')
      setHasUnsavedChanges(false)
      queryClient.invalidateQueries({ queryKey: ['user-settings'] })
    },
    onError: (error: any) => {
      toast.error(`Failed to save settings: ${error.message}`)
    }
  })

  // Test API key mutation
  const testAPIKeyMutation = useMutation({
    mutationFn: (data: { service: string, apiKey: string }) =>
      apiClient.post('/api/user/test-api-key', data),
    onSuccess: (data) => {
      toast.success(`${data.service} API key is valid!`)
    },
    onError: (error: any) => {
      toast.error(`API key validation failed: ${error.message}`)
    }
  })

  const tabs = [
    { id: 'profile', label: 'Profile', icon: User },
    { id: 'api', label: 'API Keys', icon: Key },
    { id: 'budget', label: 'Budget', icon: DollarSign },
    { id: 'agents', label: 'Agents', icon: SettingsIcon },
    { id: 'notifications', label: 'Notifications', icon: Bell },
    { id: 'wordpress', label: 'WordPress', icon: Globe },
    { id: 'security', label: 'Security', icon: Shield },
  ]

  const handleSettingsChange = (section: keyof UserSettings, updates: any) => {
    if (!settings) return
    
    setSettings(prev => ({
      ...prev!,
      [section]: {
        ...prev![section],
        ...updates
      }
    }))
    setHasUnsavedChanges(true)
  }

  const handleSave = () => {
    if (settings) {
      saveSettingsMutation.mutate(settings)
    }
  }

  const handleTestAPIKey = (service: string, apiKey: string) => {
    testAPIKeyMutation.mutate({ service, apiKey })
  }

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
      <div className="max-w-7xl mx-auto">
        <div className="text-center py-12">
          <AlertTriangle className="h-16 w-16 text-red-500 mx-auto mb-4" />
          <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-2">
            Failed to Load Settings
          </h2>
          <p className="text-gray-600 dark:text-gray-400">
            Unable to load your settings. Please refresh the page or contact support.
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            Settings
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Manage your account, API keys, and platform configuration
          </p>
        </div>

        {/* Save Button */}
        <div className="flex items-center gap-3">
          {hasUnsavedChanges && (
            <div className="flex items-center gap-2 text-sm text-yellow-600 dark:text-yellow-400">
              <AlertTriangle className="h-4 w-4" />
              Unsaved changes
            </div>
          )}
          <button
            onClick={handleSave}
            disabled={!hasUnsavedChanges || saveSettingsMutation.isPending}
            className="inline-flex items-center px-4 py-2 bg-purple-gradient text-white rounded-lg hover:opacity-90 disabled:opacity-50"
          >
            {saveSettingsMutation.isPending ? (
              <>
                <div className="animate-spin h-4 w-4 mr-2 border-2 border-white border-t-transparent rounded-full" />
                Saving...
              </>
            ) : (
              <>
                <Save className="h-4 w-4 mr-2" />
                Save Changes
              </>
            )}
          </button>
        </div>
      </div>

      {/* Tab Navigation */}
      <div className="flex space-x-1 mb-6 overflow-x-auto">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`flex items-center px-4 py-2 rounded-lg font-medium transition-colors whitespace-nowrap ${
              activeTab === tab.id
                ? 'bg-purple-100 dark:bg-purple-900 text-purple-700 dark:text-purple-300'
                : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800'
            }`}
          >
            <tab.icon className="h-4 w-4 mr-2" />
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div className="space-y-6">
        {activeTab === 'profile' && (
          <UserProfile
            profile={settings.profile}
            onChange={(updates) => handleSettingsChange('profile', updates)}
          />
        )}

        {activeTab === 'api' && (
          <APIKeysPanel
            apiKeys={settings.apiKeys}
            onChange={(updates) => handleSettingsChange('apiKeys', updates)}
            onTest={handleTestAPIKey}
            isTestingKey={testAPIKeyMutation.isPending}
          />
        )}

        {activeTab === 'budget' && (
          <BudgetSettings
            budget={settings.budget}
            onChange={(updates) => handleSettingsChange('budget', updates)}
          />
        )}

        {activeTab === 'agents' && (
          <AgentConfiguration
            agents={settings.agents}
            onChange={(updates) => handleSettingsChange('agents', updates)}
          />
        )}

        {activeTab === 'notifications' && (
          <NotificationSettings
            notifications={settings.notifications}
            onChange={(updates) => handleSettingsChange('notifications', updates)}
          />
        )}

        {activeTab === 'wordpress' && (
          <WordPressSettings
            wordpressConfigs={settings.apiKeys.wordpress}
            onChange={(updates) => 
              handleSettingsChange('apiKeys', { wordpress: updates })
            }
          />
        )}

        {activeTab === 'security' && (
          <SecuritySettings
            security={settings.security}
            onChange={(updates) => handleSettingsChange('security', updates)}
          />
        )}
      </div>
    </div>
  )
}
```

### API Keys Management Panel
```typescript
// src/components/settings/APIKeysPanel.tsx
import { useState } from 'react'
import { 
  Key, 
  Eye, 
  EyeOff, 
  TestTube, 
  CheckCircle, 
  XCircle,
  Info,
  ExternalLink
} from 'lucide-react'

interface APIKeysPanelProps {
  apiKeys: {
    anthropic: string | null
    openai: string | null
    jina: string | null
    wordpress: any[]
  }
  onChange: (updates: any) => void
  onTest: (service: string, apiKey: string) => void
  isTestingKey: boolean
}

const API_SERVICES = [
  {
    key: 'anthropic',
    name: 'Anthropic Claude',
    description: 'Required for article generation with Claude 3.5 Sonnet',
    placeholder: 'sk-ant-api03-...',
    required: true,
    docsUrl: 'https://docs.anthropic.com/claude/docs/getting-access-to-claude',
    format: /^sk-ant-api03-/,
    agent: 'Article Generation Agent'
  },
  {
    key: 'openai',
    name: 'OpenAI GPT',
    description: 'Fallback for article generation and topic analysis',
    placeholder: 'sk-...',
    required: false,
    docsUrl: 'https://platform.openai.com/api-keys',
    format: /^sk-/,
    agent: 'Article Generation Agent (Fallback)'
  },
  {
    key: 'jina',
    name: 'Jina AI',
    description: 'Required for competitor monitoring and web scraping',
    placeholder: 'jina_...',
    required: true,
    docsUrl: 'https://jina.ai/api',
    format: /^jina_/,
    agent: 'Competitor Monitoring Agent'
  }
]

export function APIKeysPanel({ apiKeys, onChange, onTest, isTestingKey }: APIKeysPanelProps) {
  const [visibleKeys, setVisibleKeys] = useState<{ [key: string]: boolean }>({})
  const [testResults, setTestResults] = useState<{ [key: string]: 'success' | 'error' | null }>({})

  const toggleVisibility = (serviceKey: string) => {
    setVisibleKeys(prev => ({
      ...prev,
      [serviceKey]: !prev[serviceKey]
    }))
  }

  const handleKeyChange = (serviceKey: string, value: string) => {
    onChange({
      ...apiKeys,
      [serviceKey]: value || null
    })
    // Clear test result when key changes
    setTestResults(prev => ({
      ...prev,
      [serviceKey]: null
    }))
  }

  const handleTestKey = async (service: any) => {
    const apiKey = apiKeys[service.key as keyof typeof apiKeys] as string
    if (!apiKey) return

    try {
      await onTest(service.key, apiKey)
      setTestResults(prev => ({
        ...prev,
        [service.key]: 'success'
      }))
    } catch (error) {
      setTestResults(prev => ({
        ...prev,
        [service.key]: 'error'
      }))
    }
  }

  const validateKeyFormat = (service: any, value: string) => {
    if (!value) return true
    return service.format.test(value)
  }

  const getRequiredMissingKeys = () => {
    return API_SERVICES
      .filter(service => service.required)
      .filter(service => !apiKeys[service.key as keyof typeof apiKeys])
  }

  const requiredMissingKeys = getRequiredMissingKeys()

  return (
    <div className="space-y-6">
      {/* Overview */}
      <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
        <div className="flex items-start gap-4">
          <div className="p-3 bg-purple-100 dark:bg-purple-900/20 rounded-lg">
            <Key className="h-6 w-6 text-purple-600 dark:text-purple-400" />
          </div>
          <div className="flex-1">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              API Keys Configuration
            </h3>
            <p className="text-gray-600 dark:text-gray-400 mb-4">
              Securely store your API keys for the 5-agent content generation pipeline. 
              All keys are encrypted and stored securely.
            </p>
            
            {requiredMissingKeys.length > 0 && (
              <div className="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-4">
                <div className="flex items-start gap-3">
                  <Info className="h-5 w-5 text-yellow-600 dark:text-yellow-400 mt-0.5" />
                  <div>
                    <h4 className="font-medium text-yellow-800 dark:text-yellow-300">
                      Missing Required API Keys
                    </h4>
                    <p className="text-sm text-yellow-700 dark:text-yellow-400 mt-1">
                      The following required API keys are missing: {requiredMissingKeys.map(k => k.name).join(', ')}. 
                      Content generation will not work without these keys.
                    </p>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* API Key Forms */}
      <div className="grid grid-cols-1 gap-6">
        {API_SERVICES.map((service) => {
          const currentKey = apiKeys[service.key as keyof typeof apiKeys] as string
          const isVisible = visibleKeys[service.key]
          const testResult = testResults[service.key]
          const isValidFormat = validateKeyFormat(service, currentKey || '')

          return (
            <div 
              key={service.key}
              className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700"
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <h4 className="text-lg font-medium text-gray-900 dark:text-white">
                      {service.name}
                    </h4>
                    {service.required && (
                      <span className="text-xs px-2 py-1 bg-red-100 text-red-700 dark:bg-red-900/20 dark:text-red-400 rounded-full">
                        Required
                      </span>
                    )}
                    {testResult === 'success' && (
                      <CheckCircle className="h-4 w-4 text-green-500" />
                    )}
                    {testResult === 'error' && (
                      <XCircle className="h-4 w-4 text-red-500" />
                    )}
                  </div>
                  <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                    {service.description}
                  </p>
                  <p className="text-xs text-purple-600 dark:text-purple-400">
                    Used by: {service.agent}
                  </p>
                </div>
                <a
                  href={service.docsUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                >
                  <ExternalLink className="h-4 w-4" />
                </a>
              </div>

              <div className="space-y-3">
                {/* API Key Input */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    API Key
                  </label>
                  <div className="relative">
                    <input
                      type={isVisible ? 'text' : 'password'}
                      value={currentKey || ''}
                      onChange={(e) => handleKeyChange(service.key, e.target.value)}
                      className={`w-full px-4 py-2 pr-20 border rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent dark:bg-gray-700 dark:text-white font-mono text-sm ${
                        currentKey && !isValidFormat
                          ? 'border-red-300 dark:border-red-600'
                          : 'border-gray-300 dark:border-gray-600'
                      }`}
                      placeholder={service.placeholder}
                    />
                    <div className="absolute inset-y-0 right-0 flex items-center gap-1 pr-3">
                      <button
                        type="button"
                        onClick={() => toggleVisibility(service.key)}
                        className="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                      >
                        {isVisible ? (
                          <EyeOff className="h-4 w-4" />
                        ) : (
                          <Eye className="h-4 w-4" />
                        )}
                      </button>
                      <button
                        type="button"
                        onClick={() => handleTestKey(service)}
                        disabled={!currentKey || !isValidFormat || isTestingKey}
                        className="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 disabled:opacity-50"
                        title="Test API Key"
                      >
                        <TestTube className="h-4 w-4" />
                      </button>
                    </div>
                  </div>
                  
                  {currentKey && !isValidFormat && (
                    <p className="text-sm text-red-600 dark:text-red-400 mt-1">
                      Invalid API key format. Expected format: {service.placeholder}
                    </p>
                  )}
                  
                  {testResult === 'success' && (
                    <p className="text-sm text-green-600 dark:text-green-400 mt-1">
                      ✓ API key is valid and working
                    </p>
                  )}
                  
                  {testResult === 'error' && (
                    <p className="text-sm text-red-600 dark:text-red-400 mt-1">
                      ✗ API key validation failed. Please check your key.
                    </p>
                  )}
                </div>

                {/* Status */}
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-600 dark:text-gray-400">
                    Status:
                  </span>
                  <span className={`font-medium ${
                    currentKey 
                      ? 'text-green-600 dark:text-green-400'
                      : service.required
                      ? 'text-red-600 dark:text-red-400'
                      : 'text-gray-600 dark:text-gray-400'
                  }`}>
                    {currentKey 
                      ? 'Configured'
                      : service.required
                      ? 'Required - Not Set'
                      : 'Optional - Not Set'
                    }
                  </span>
                </div>
              </div>
            </div>
          )
        })}
      </div>

      {/* Security Notice */}
      <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-xl p-4">
        <div className="flex items-start gap-3">
          <Info className="h-5 w-5 text-blue-600 dark:text-blue-400 mt-0.5" />
          <div>
            <h4 className="font-medium text-blue-800 dark:text-blue-300 mb-1">
              Security Information
            </h4>
            <ul className="text-sm text-blue-700 dark:text-blue-400 space-y-1">
              <li>• All API keys are encrypted at rest using AES-256 encryption</li>
              <li>• Keys are transmitted securely over HTTPS</li>
              <li>• Only you can view and modify your API keys</li>
              <li>• API usage is monitored and logged for cost tracking</li>
              <li>• Keys can be rotated at any time without service interruption</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}
```

### Budget Settings Component
```typescript
// src/components/settings/BudgetSettings.tsx
import { useState } from 'react'
import { 
  DollarSign, 
  TrendingUp, 
  AlertTriangle, 
  Bell,
  Target,
  BarChart3
} from 'lucide-react'

interface BudgetSettingsProps {
  budget: {
    monthlyLimit: number
    currentSpend: number
    alertThreshold: number
    enableAlerts: boolean
    costTrackingEnabled: boolean
  }
  onChange: (updates: any) => void
}

const BUDGET_PRESETS = [
  { label: 'Starter', amount: 50, description: '~100-200 articles/month' },
  { label: 'Professional', amount: 200, description: '~400-800 articles/month' },
  { label: 'Enterprise', amount: 500, description: '~1000-2000 articles/month' },
  { label: 'Custom', amount: 0, description: 'Set your own limit' },
]

export function BudgetSettings({ budget, onChange }: BudgetSettingsProps) {
  const [selectedPreset, setSelectedPreset] = useState<string>(() => {
    const preset = BUDGET_PRESETS.find(p => p.amount === budget.monthlyLimit)
    return preset?.label || 'Custom'
  })

  const budgetUsage = (budget.currentSpend / budget.monthlyLimit) * 100
  const isNearLimit = budgetUsage >= budget.alertThreshold
  const isOverBudget = budgetUsage > 100

  const handlePresetChange = (preset: typeof BUDGET_PRESETS[0]) => {
    setSelectedPreset(preset.label)
    if (preset.amount > 0) {
      onChange({
        ...budget,
        monthlyLimit: preset.amount
      })
    }
  }

  const handleCustomLimitChange = (value: number) => {
    onChange({
      ...budget,
      monthlyLimit: value
    })
  }

  const handleAlertThresholdChange = (value: number) => {
    onChange({
      ...budget,
      alertThreshold: value
    })
  }

  const handleToggleChange = (field: string, value: boolean) => {
    onChange({
      ...budget,
      [field]: value
    })
  }

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(amount)
  }

  const estimateArticles = (amount: number) => {
    const avgCostPerArticle = 0.25 // Estimate
    return Math.floor(amount / avgCostPerArticle)
  }

  return (
    <div className="space-y-6">
      {/* Current Budget Status */}
      <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
        <div className="flex items-start gap-4 mb-6">
          <div className="p-3 bg-purple-100 dark:bg-purple-900/20 rounded-lg">
            <DollarSign className="h-6 w-6 text-purple-600 dark:text-purple-400" />
          </div>
          <div className="flex-1">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              Budget Management
            </h3>
            <p className="text-gray-600 dark:text-gray-400">
              Control your content generation costs with budget limits and alerts
            </p>
          </div>
        </div>

        {/* Budget Usage Overview */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
          <div className="text-center">
            <div className={`text-2xl font-bold mb-1 ${
              isOverBudget ? 'text-red-600' : 'text-gray-900 dark:text-white'
            }`}>
              {formatCurrency(budget.currentSpend)}
            </div>
            <div className="text-sm text-gray-600 dark:text-gray-400">
              Current Month Spend
            </div>
          </div>
          
          <div className="text-center">
            <div className="text-2xl font-bold text-gray-900 dark:text-white mb-1">
              {formatCurrency(budget.monthlyLimit)}
            </div>
            <div className="text-sm text-gray-600 dark:text-gray-400">
              Monthly Budget
            </div>
          </div>
          
          <div className="text-center">
            <div className="text-2xl font-bold text-gray-900 dark:text-white mb-1">
              {formatCurrency(budget.monthlyLimit - budget.currentSpend)}
            </div>
            <div className="text-sm text-gray-600 dark:text-gray-400">
              Remaining Budget
            </div>
          </div>
        </div>

        {/* Budget Usage Bar */}
        <div className="mb-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
              Budget Usage
            </span>
            <span className={`text-sm font-medium ${
              isOverBudget ? 'text-red-600' :
              isNearLimit ? 'text-yellow-600' :
              'text-green-600'
            }`}>
              {budgetUsage.toFixed(1)}%
            </span>
          </div>
          <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3">
            <div 
              className={`h-3 rounded-full transition-all duration-500 ${
                isOverBudget ? 'bg-red-500' :
                isNearLimit ? 'bg-yellow-500' :
                'bg-green-500'
              }`}
              style={{ width: `${Math.min(budgetUsage, 100)}%` }}
            />
            {budget.alertThreshold < 100 && (
              <div 
                className="absolute w-0.5 h-3 bg-orange-500 transform -translate-x-0.5"
                style={{ 
                  left: `${budget.alertThreshold}%`,
                  marginTop: '-12px'
                }}
                title={`Alert threshold: ${budget.alertThreshold}%`}
              />
            )}
          </div>
        </div>

        {/* Alert if over budget or near limit */}
        {(isOverBudget || isNearLimit) && (
          <div className={`p-4 rounded-lg border ${
            isOverBudget 
              ? 'bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800' 
              : 'bg-yellow-50 dark:bg-yellow-900/20 border-yellow-200 dark:border-yellow-800'
          }`}>
            <div className="flex items-start gap-3">
              <AlertTriangle className={`h-5 w-5 mt-0.5 ${
                isOverBudget ? 'text-red-600' : 'text-yellow-600'
              }`} />
              <div>
                <h4 className={`font-medium ${
                  isOverBudget ? 'text-red-800 dark:text-red-300' : 'text-yellow-800 dark:text-yellow-300'
                }`}>
                  {isOverBudget ? 'Budget Exceeded' : 'Budget Alert'}
                </h4>
                <p className={`text-sm mt-1 ${
                  isOverBudget ? 'text-red-700 dark:text-red-400' : 'text-yellow-700 dark:text-yellow-400'
                }`}>
                  {isOverBudget 
                    ? `You've exceeded your monthly budget by ${formatCurrency(budget.currentSpend - budget.monthlyLimit)}. Consider increasing your limit or reducing usage.`
                    : `You've reached ${budgetUsage.toFixed(1)}% of your monthly budget. New content generation may be limited.`
                  }
                </p>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Budget Configuration */}
      <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
        <h4 className="text-lg font-medium text-gray-900 dark:text-white mb-4">
          Budget Configuration
        </h4>

        {/* Preset Budgets */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
            Choose a Budget Plan
          </label>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {BUDGET_PRESETS.map((preset) => (
              <button
                key={preset.label}
                onClick={() => handlePresetChange(preset)}
                className={`p-4 border-2 rounded-lg text-left transition-colors ${
                  selectedPreset === preset.label
                    ? 'border-purple-500 bg-purple-50 dark:bg-purple-900/20'
                    : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600'
                }`}
              >
                <div className="flex items-center justify-between mb-2">
                  <h5 className="font-medium text-gray-900 dark:text-white">
                    {preset.label}
                  </h5>
                  <Target className={`h-4 w-4 ${
                    selectedPreset === preset.label ? 'text-purple-600' : 'text-gray-400'
                  }`} />
                </div>
                {preset.amount > 0 && (
                  <div className="text-2xl font-bold text-gray-900 dark:text-white mb-1">
                    {formatCurrency(preset.amount)}
                  </div>
                )}
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  {preset.description}
                </p>
              </button>
            ))}
          </div>
        </div>

        {/* Custom Budget Amount */}
        {selectedPreset === 'Custom' && (
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Custom Monthly Budget
            </label>
            <div className="relative">
              <span className="absolute left-3 top-2 text-gray-500 dark:text-gray-400">$</span>
              <input
                type="number"
                min="10"
                max="10000"
                step="10"
                value={budget.monthlyLimit}
                onChange={(e) => handleCustomLimitChange(Number(e.target.value))}
                className="w-full pl-8 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                placeholder="Enter amount"
              />
            </div>
            <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
              Estimated {estimateArticles(budget.monthlyLimit)} articles per month at $0.25 average cost
            </p>
          </div>
        )}

        {/* Alert Settings */}
        <div className="space-y-4">
          <div className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-900 rounded-lg">
            <div className="flex items-center gap-3">
              <Bell className="h-5 w-5 text-gray-600 dark:text-gray-400" />
              <div>
                <p className="font-medium text-gray-900 dark:text-white">
                  Budget Alerts
                </p>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Receive notifications when approaching budget limit
                </p>
              </div>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={budget.enableAlerts}
                onChange={(e) => handleToggleChange('enableAlerts', e.target.checked)}
                className="sr-only peer"
              />
              <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-purple-300 dark:peer-focus:ring-purple-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-purple-600" />
            </label>
          </div>

          {budget.enableAlerts && (
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Alert Threshold ({budget.alertThreshold}% of budget)
              </label>
              <input
                type="range"
                min="50"
                max="95"
                step="5"
                value={budget.alertThreshold}
                onChange={(e) => handleAlertThresholdChange(Number(e.target.value))}
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer dark:bg-gray-700 slider"
              />
              <div className="flex justify-between text-xs text-gray-600 dark:text-gray-400 mt-1">
                <span>50%</span>
                <span>75%</span>
                <span>95%</span>
              </div>
              <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">
                Alert when monthly spending reaches {formatCurrency(budget.monthlyLimit * budget.alertThreshold / 100)}
              </p>
            </div>
          )}

          <div className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-900 rounded-lg">
            <div className="flex items-center gap-3">
              <BarChart3 className="h-5 w-5 text-gray-600 dark:text-gray-400" />
              <div>
                <p className="font-medium text-gray-900 dark:text-white">
                  Cost Tracking
                </p>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Track detailed cost analytics and usage patterns
                </p>
              </div>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={budget.costTrackingEnabled}
                onChange={(e) => handleToggleChange('costTrackingEnabled', e.target.checked)}
                className="sr-only peer"
              />
              <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-purple-300 dark:peer-focus:ring-purple-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-purple-600" />
            </label>
          </div>
        </div>
      </div>

      {/* Cost Estimation */}
      <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-xl p-4">
        <div className="flex items-start gap-3">
          <TrendingUp className="h-5 w-5 text-blue-600 dark:text-blue-400 mt-0.5" />
          <div>
            <h4 className="font-medium text-blue-800 dark:text-blue-300 mb-2">
              Cost Estimation Guide
            </h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-blue-700 dark:text-blue-400">
              <div>
                <p className="font-medium mb-1">Average Costs per Agent:</p>
                <ul className="space-y-1">
                  <li>• Competitor Monitoring: ~$0.02</li>
                  <li>• Topic Analysis: ~$0.01</li>
                  <li>• Article Generation: ~$0.20</li>
                  <li>• Legal Fact Checking: ~$0.02</li>
                  <li>• WordPress Publishing: Free</li>
                </ul>
              </div>
              <div>
                <p className="font-medium mb-1">Estimated Articles by Budget:</p>
                <ul className="space-y-1">
                  <li>• $50/month: ~200 articles</li>
                  <li>• $200/month: ~800 articles</li>
                  <li>• $500/month: ~2,000 articles</li>
                  <li>• Costs vary by article length and complexity</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
```

**Success Criteria:**
- Secure API key management with encryption and validation
- Comprehensive budget controls with real-time tracking and alerts
- Agent configuration with customizable parameters and timeouts
- User profile management with timezone and preference settings
- Notification controls for email, in-app, and webhook alerts
- WordPress integration with multiple site support and authentication
- Security settings with 2FA, session management, and IP restrictions
- Form validation and error handling throughout
- Mobile-responsive design with proper accessibility
- Integration with existing authentication and API systems

This settings and configuration system provides comprehensive control over all aspects of the Blog-Poster platform, ensuring secure operation and personalized user experience.
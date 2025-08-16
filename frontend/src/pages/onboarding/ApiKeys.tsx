import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { OnboardingLayout } from '@/components/onboarding/OnboardingLayout'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Eye, EyeOff, Key, Shield, ExternalLink, CheckCircle, AlertCircle, DollarSign } from 'lucide-react'
import { cn } from '@/lib/utils'

export default function ApiKeys() {
  const navigate = useNavigate()
  const [apiKeys, setApiKeys] = useState({
    anthropic: '',
    openai: '',
    jina: ''
  })
  const [showKeys, setShowKeys] = useState({
    anthropic: false,
    openai: false,
    jina: false
  })
  const [testResults, setTestResults] = useState({
    anthropic: null as 'testing' | 'success' | 'error' | null,
    openai: null as 'testing' | 'success' | 'error' | null,
    jina: null as 'testing' | 'success' | 'error' | null
  })

  const handleKeyChange = (service: string, value: string) => {
    setApiKeys(prev => ({ ...prev, [service]: value }))
    setTestResults(prev => ({ ...prev, [service]: null }))
  }

  const toggleShowKey = (service: string) => {
    setShowKeys(prev => ({ ...prev, [service]: !prev[service] }))
  }

  const testApiKey = async (service: string) => {
    if (!apiKeys[service as keyof typeof apiKeys]) return

    setTestResults(prev => ({ ...prev, [service]: 'testing' }))
    
    // Simulate API test
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // For demo purposes, assume success if key is not empty
    const isValid = apiKeys[service as keyof typeof apiKeys].length > 10
    setTestResults(prev => ({ 
      ...prev, 
      [service]: isValid ? 'success' : 'error' 
    }))
  }

  const handleContinue = () => {
    navigate('/onboarding/wordpress')
  }

  const handleBack = () => {
    navigate('/onboarding/profile')
  }

  const handleSkip = () => {
    navigate('/onboarding/wordpress')
  }

  const canContinue = Boolean(apiKeys.anthropic && apiKeys.jina)
  const hasRequiredKeys = testResults.anthropic === 'success' && testResults.jina === 'success'

  const apiServices = [
    {
      key: 'anthropic',
      name: 'Anthropic (Claude)',
      required: true,
      description: 'Powers the main content generation agent',
      helpUrl: 'https://console.anthropic.com',
      cost: '$0.10-0.50 per article',
      features: ['High-quality content', 'SEO optimization', 'Fact checking']
    },
    {
      key: 'openai', 
      name: 'OpenAI (GPT)',
      required: false,
      description: 'Fallback when Anthropic is unavailable',
      helpUrl: 'https://platform.openai.com',
      cost: '$0.15-0.75 per article',
      features: ['Reliable backup', 'Multiple models', 'Fast generation']
    },
    {
      key: 'jina',
      name: 'Jina AI Reader',
      required: true,
      description: 'Powers competitor monitoring and web scraping',
      helpUrl: 'https://jina.ai/reader',
      cost: '$0.01-0.05 per article',
      features: ['Web scraping', 'Content analysis', 'Competitor tracking']
    }
  ]

  return (
    <OnboardingLayout
      currentStep={3}
      totalSteps={5}
      stepName="Connect your AI services"
      onBack={handleBack}
      onSkip={handleSkip}
      onContinue={handleContinue}
      canContinue={canContinue}
    >
      <div className="space-y-8">
        {/* Header */}
        <div className="text-center space-y-2">
          <Key className="w-12 h-12 text-primary mx-auto" />
          <h1 className="text-2xl font-bold text-foreground">
            Connect Your AI Services
          </h1>
          <p className="text-muted-foreground">
            Use your own API keys for full control and cost transparency
          </p>
        </div>

        {/* Why Section */}
        <Card className="bg-gradient-to-r from-primary/5 to-primary/10 border-primary/20">
          <CardContent className="p-6">
            <h3 className="font-semibold text-foreground mb-4 flex items-center">
              <DollarSign className="w-5 h-5 mr-2 text-primary" />
              Why Your Own Keys?
            </h3>
            <div className="grid md:grid-cols-2 gap-4 text-sm">
              <div className="space-y-2">
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-primary rounded-full" />
                  <span>Full cost control - pay AI providers directly</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-primary rounded-full" />
                  <span>No markup on API usage</span>
                </div>
              </div>
              <div className="space-y-2">
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-primary rounded-full" />
                  <span>Higher rate limits and priority access</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-primary rounded-full" />
                  <span>Your data stays between you and AI providers</span>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* API Keys */}
        <div className="space-y-6">
          {apiServices.map((service) => (
            <Card key={service.key} className={cn(
              "transition-all duration-200",
              testResults[service.key as keyof typeof testResults] === 'success' && "border-green-200 bg-green-50/50"
            )}>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <span>{service.name}</span>
                    {service.required ? (
                      <Badge variant="destructive">Required</Badge>
                    ) : (
                      <Badge variant="secondary">Optional</Badge>
                    )}
                  </div>
                  {testResults[service.key as keyof typeof testResults] === 'success' && (
                    <CheckCircle className="w-5 h-5 text-green-600" />
                  )}
                </CardTitle>
                <p className="text-sm text-muted-foreground">{service.description}</p>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor={service.key}>API Key</Label>
                  <div className="flex space-x-2">
                    <div className="relative flex-1">
                      <Input
                        id={service.key}
                        type={showKeys[service.key as keyof typeof showKeys] ? 'text' : 'password'}
                        value={apiKeys[service.key as keyof typeof apiKeys]}
                        onChange={(e) => handleKeyChange(service.key, e.target.value)}
                        placeholder={`Enter your ${service.name} API key`}
                        className="pr-10"
                      />
                      <Button
                        type="button"
                        variant="ghost"
                        size="sm"
                        className="absolute right-0 top-0 h-full px-3"
                        onClick={() => toggleShowKey(service.key)}
                      >
                        {showKeys[service.key as keyof typeof showKeys] ? (
                          <EyeOff className="w-4 h-4" />
                        ) : (
                          <Eye className="w-4 h-4" />
                        )}
                      </Button>
                    </div>
                    <Button
                      onClick={() => testApiKey(service.key)}
                      disabled={!apiKeys[service.key as keyof typeof apiKeys] || testResults[service.key as keyof typeof testResults] === 'testing'}
                      variant="outline"
                    >
                      {testResults[service.key as keyof typeof testResults] === 'testing' ? (
                        'Testing...'
                      ) : testResults[service.key as keyof typeof testResults] === 'success' ? (
                        'Connected ✓'
                      ) : (
                        'Test'
                      )}
                    </Button>
                  </div>
                  
                  {testResults[service.key as keyof typeof testResults] === 'error' && (
                    <div className="flex items-center space-x-2 text-red-600 text-sm">
                      <AlertCircle className="w-4 h-4" />
                      <span>Invalid API key. Please check and try again.</span>
                    </div>
                  )}
                  
                  <div className="flex items-center justify-between text-sm">
                    <a 
                      href={service.helpUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-primary hover:underline flex items-center space-x-1"
                    >
                      <span>Get your API key</span>
                      <ExternalLink className="w-3 h-3" />
                    </a>
                    <span className="text-muted-foreground">{service.cost}</span>
                  </div>
                </div>

                <div className="text-sm">
                  <p className="text-muted-foreground mb-2">Features:</p>
                  <div className="flex flex-wrap gap-2">
                    {service.features.map((feature) => (
                      <Badge key={feature} variant="outline" className="text-xs">
                        {feature}
                      </Badge>
                    ))}
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Security Note */}
        <Card className="bg-muted/50">
          <CardContent className="p-6">
            <div className="flex items-start space-x-3">
              <Shield className="w-5 h-5 text-primary mt-0.5" />
              <div>
                <h3 className="font-semibold text-foreground mb-2">Security & Privacy</h3>
                <ul className="text-sm text-muted-foreground space-y-1">
                  <li>🔒 Your API keys are encrypted and stored securely</li>
                  <li>🔒 We never see or log your actual keys</li>
                  <li>🔒 You can update or remove keys anytime in settings</li>
                  <li>🔒 Keys are only used for your content generation</li>
                </ul>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Cost Calculator */}
        <Card>
          <CardContent className="p-6">
            <h3 className="font-semibold text-foreground mb-4">Estimated Monthly Costs</h3>
            <div className="grid md:grid-cols-3 gap-4 text-center">
              <div className="space-y-2">
                <div className="text-2xl font-bold text-foreground">$15-30</div>
                <div className="text-sm text-muted-foreground">10 articles/month</div>
              </div>
              <div className="space-y-2">
                <div className="text-2xl font-bold text-foreground">$25-60</div>
                <div className="text-sm text-muted-foreground">20 articles/month</div>
              </div>
              <div className="space-y-2">
                <div className="text-2xl font-bold text-foreground">$50-150</div>
                <div className="text-sm text-muted-foreground">50 articles/month</div>
              </div>
            </div>
            <p className="text-xs text-muted-foreground text-center mt-4">
              Costs may vary based on article length and complexity
            </p>
          </CardContent>
        </Card>
      </div>
    </OnboardingLayout>
  )
}
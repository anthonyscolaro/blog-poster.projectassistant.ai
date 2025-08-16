import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { OnboardingLayout } from '@/components/onboarding/OnboardingLayout'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Badge } from '@/components/ui/badge'
import { Eye, EyeOff, Globe, CheckCircle, AlertCircle, Plus, Trash2, ExternalLink, Shield } from 'lucide-react'

export default function WordPress() {
  const navigate = useNavigate()
  const [sites, setSites] = useState([
    {
      id: '1',
      url: '',
      username: '',
      password: '',
      status: 'disconnected' as 'disconnected' | 'testing' | 'connected' | 'error',
      siteInfo: null as any,
      settings: {
        defaultStatus: 'draft',
        defaultAuthor: '',
        defaultCategory: '',
        featuredImage: 'auto-generate'
      }
    }
  ])
  const [showPasswords, setShowPasswords] = useState<Record<string, boolean>>({})

  const updateSite = (id: string, updates: any) => {
    setSites(prev => prev.map(site => 
      site.id === id ? { ...site, ...updates } : site
    ))
  }

  const togglePassword = (siteId: string) => {
    setShowPasswords(prev => ({ ...prev, [siteId]: !prev[siteId] }))
  }

  const testConnection = async (siteId: string) => {
    const site = sites.find(s => s.id === siteId)
    if (!site?.url || !site?.username || !site?.password) return

    updateSite(siteId, { status: 'testing' })
    
    // Simulate connection test
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // For demo purposes, assume success if all fields are filled
    const isValid = site.url.includes('http') && site.username && site.password.length > 5
    
    if (isValid) {
      updateSite(siteId, { 
        status: 'connected',
        siteInfo: {
          siteName: 'My Awesome Blog',
          wpVersion: '6.3.2',
          theme: 'Twenty Twenty-Three',
          postTypes: ['post', 'page'],
          categories: ['Uncategorized', 'Technology', 'Business'],
          users: ['admin', 'editor']
        }
      })
    } else {
      updateSite(siteId, { status: 'error' })
    }
  }

  const addSite = () => {
    const newSite = {
      id: Date.now().toString(),
      url: '',
      username: '',
      password: '',
      status: 'disconnected' as const,
      siteInfo: null,
      settings: {
        defaultStatus: 'draft',
        defaultAuthor: '',
        defaultCategory: '',
        featuredImage: 'auto-generate'
      }
    }
    setSites(prev => [...prev, newSite])
  }

  const removeSite = (id: string) => {
    setSites(prev => prev.filter(site => site.id !== id))
  }

  const handleContinue = () => {
    navigate('/onboarding/team')
  }

  const handleBack = () => {
    navigate('/onboarding/api-keys')
  }

  const handleSkip = () => {
    navigate('/onboarding/team')
  }

  const hasConnectedSite = sites.some(site => site.status === 'connected')

  return (
    <OnboardingLayout
      currentStep={4}
      totalSteps={5}
      stepName="Connect your WordPress site"
      onBack={handleBack}
      onSkip={handleSkip}
      onContinue={handleContinue}
      canContinue={true}
    >
      <div className="space-y-8">
        {/* Header */}
        <div className="text-center space-y-2">
          <Globe className="w-12 h-12 text-primary mx-auto" />
          <h1 className="text-2xl font-bold text-foreground">
            Connect Your WordPress Site
          </h1>
          <p className="text-muted-foreground">
            Automatically publish articles with perfect formatting
          </p>
        </div>

        {/* WordPress Sites */}
        <div className="space-y-6">
          {sites.map((site, index) => (
            <Card key={site.id} className="relative">
              {sites.length > 1 && (
                <Button
                  variant="ghost"
                  size="sm"
                  className="absolute top-4 right-4 text-muted-foreground hover:text-destructive"
                  onClick={() => removeSite(site.id)}
                >
                  <Trash2 className="w-4 h-4" />
                </Button>
              )}
              
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span>WordPress Site {index + 1}</span>
                  {site.status === 'connected' && (
                    <Badge variant="default" className="bg-green-500">
                      <CheckCircle className="w-3 h-3 mr-1" />
                      Connected
                    </Badge>
                  )}
                  {site.status === 'error' && (
                    <Badge variant="destructive">
                      <AlertCircle className="w-3 h-3 mr-1" />
                      Error
                    </Badge>
                  )}
                </CardTitle>
              </CardHeader>

              <CardContent>
                <Tabs defaultValue="basic" className="space-y-4">
                  <TabsList className="grid w-full grid-cols-2">
                    <TabsTrigger value="basic">Basic Setup</TabsTrigger>
                    <TabsTrigger value="settings" disabled={site.status !== 'connected'}>
                      Publishing Settings
                    </TabsTrigger>
                  </TabsList>

                  <TabsContent value="basic" className="space-y-4">
                    <div className="grid md:grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <Label htmlFor={`url-${site.id}`}>WordPress URL</Label>
                        <Input
                          id={`url-${site.id}`}
                          value={site.url}
                          onChange={(e) => updateSite(site.id, { url: e.target.value })}
                          placeholder="https://yoursite.com"
                        />
                      </div>

                      <div className="space-y-2">
                        <Label htmlFor={`username-${site.id}`}>Username</Label>
                        <Input
                          id={`username-${site.id}`}
                          value={site.username}
                          onChange={(e) => updateSite(site.id, { username: e.target.value })}
                          placeholder="Your WordPress username"
                        />
                      </div>

                      <div className="space-y-2 md:col-span-2">
                        <Label htmlFor={`password-${site.id}`}>Application Password</Label>
                        <div className="flex space-x-2">
                          <div className="relative flex-1">
                            <Input
                              id={`password-${site.id}`}
                              type={showPasswords[site.id] ? 'text' : 'password'}
                              value={site.password}
                              onChange={(e) => updateSite(site.id, { password: e.target.value })}
                              placeholder="Generated application password"
                              className="pr-10"
                            />
                            <Button
                              type="button"
                              variant="ghost"
                              size="sm"
                              className="absolute right-0 top-0 h-full px-3"
                              onClick={() => togglePassword(site.id)}
                            >
                              {showPasswords[site.id] ? (
                                <EyeOff className="w-4 h-4" />
                              ) : (
                                <Eye className="w-4 h-4" />
                              )}
                            </Button>
                          </div>
                          <Button
                            onClick={() => testConnection(site.id)}
                            disabled={!site.url || !site.username || !site.password || site.status === 'testing'}
                            variant="outline"
                          >
                            {site.status === 'testing' ? 'Testing...' : 'Test Connection'}
                          </Button>
                        </div>
                      </div>
                    </div>

                    {site.status === 'error' && (
                      <div className="flex items-center space-x-2 text-red-600 text-sm">
                        <AlertCircle className="w-4 h-4" />
                        <span>Connection failed. Please check your credentials and try again.</span>
                      </div>
                    )}

                    {site.status === 'connected' && site.siteInfo && (
                      <Card className="bg-green-50 border-green-200">
                        <CardContent className="p-4">
                          <h4 className="font-semibold text-green-800 mb-2">Connection Successful!</h4>
                          <div className="grid md:grid-cols-2 gap-2 text-sm text-green-700">
                            <div>Site: {site.siteInfo.siteName}</div>
                            <div>WordPress: {site.siteInfo.wpVersion}</div>
                            <div>Theme: {site.siteInfo.theme}</div>
                            <div>Categories: {site.siteInfo.categories.length}</div>
                          </div>
                        </CardContent>
                      </Card>
                    )}

                    {/* Instructions */}
                    <Card className="bg-muted/50">
                      <CardContent className="p-4">
                        <h4 className="font-semibold mb-2">How to get an Application Password:</h4>
                        <ol className="text-sm text-muted-foreground space-y-1 list-decimal list-inside">
                          <li>Go to Users → Profile in your WordPress admin</li>
                          <li>Scroll to &apos;Application Passwords&apos;</li>
                          <li>Enter &apos;Blog-Poster&apos; as the name</li>
                          <li>Click &apos;Add New Application Password&apos;</li>
                          <li>Copy the generated password above</li>
                        </ol>
                        <a 
                          href="https://wordpress.org/support/article/application-passwords/"
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-primary hover:underline flex items-center space-x-1 text-sm mt-2"
                        >
                          <span>Learn more about Application Passwords</span>
                          <ExternalLink className="w-3 h-3" />
                        </a>
                      </CardContent>
                    </Card>
                  </TabsContent>

                  <TabsContent value="settings" className="space-y-4">
                    {site.status === 'connected' && (
                      <div className="grid md:grid-cols-2 gap-4">
                        <div className="space-y-2">
                          <Label>Default Post Status</Label>
                          <Select 
                            value={site.settings.defaultStatus} 
                            onValueChange={(value) => updateSite(site.id, { 
                              settings: { ...site.settings, defaultStatus: value } 
                            })}
                          >
                            <SelectTrigger>
                              <SelectValue />
                            </SelectTrigger>
                            <SelectContent>
                              <SelectItem value="draft">Draft</SelectItem>
                              <SelectItem value="pending">Pending Review</SelectItem>
                              <SelectItem value="publish">Published</SelectItem>
                            </SelectContent>
                          </Select>
                        </div>

                        <div className="space-y-2">
                          <Label>Default Author</Label>
                          <Select 
                            value={site.settings.defaultAuthor} 
                            onValueChange={(value) => updateSite(site.id, { 
                              settings: { ...site.settings, defaultAuthor: value } 
                            })}
                          >
                            <SelectTrigger>
                              <SelectValue placeholder="Select author" />
                            </SelectTrigger>
                            <SelectContent>
                              {site.siteInfo?.users.map((user: string) => (
                                <SelectItem key={user} value={user}>{user}</SelectItem>
                              ))}
                            </SelectContent>
                          </Select>
                        </div>

                        <div className="space-y-2">
                          <Label>Default Category</Label>
                          <Select 
                            value={site.settings.defaultCategory} 
                            onValueChange={(value) => updateSite(site.id, { 
                              settings: { ...site.settings, defaultCategory: value } 
                            })}
                          >
                            <SelectTrigger>
                              <SelectValue placeholder="Select category" />
                            </SelectTrigger>
                            <SelectContent>
                              {site.siteInfo?.categories.map((category: string) => (
                                <SelectItem key={category} value={category}>{category}</SelectItem>
                              ))}
                            </SelectContent>
                          </Select>
                        </div>

                        <div className="space-y-2">
                          <Label>Featured Image</Label>
                          <Select 
                            value={site.settings.featuredImage} 
                            onValueChange={(value) => updateSite(site.id, { 
                              settings: { ...site.settings, featuredImage: value } 
                            })}
                          >
                            <SelectTrigger>
                              <SelectValue />
                            </SelectTrigger>
                            <SelectContent>
                              <SelectItem value="auto-generate">Auto-generate</SelectItem>
                              <SelectItem value="placeholder">Use placeholder</SelectItem>
                              <SelectItem value="skip">Skip featured image</SelectItem>
                            </SelectContent>
                          </Select>
                        </div>
                      </div>
                    )}
                  </TabsContent>
                </Tabs>
              </CardContent>
            </Card>
          ))}

          <Button
            onClick={addSite}
            variant="outline"
            className="w-full border-dashed"
          >
            <Plus className="w-4 h-4 mr-2" />
            Add Another WordPress Site
          </Button>
        </div>

        {/* Security & Permissions */}
        <Card className="bg-muted/50">
          <CardContent className="p-6">
            <div className="flex items-start space-x-3">
              <Shield className="w-5 h-5 text-primary mt-0.5" />
              <div>
                <h3 className="font-semibold text-foreground mb-2">Security & Permissions</h3>
                <div className="grid md:grid-cols-2 gap-4 text-sm">
                  <div className="space-y-1">
                    <div className="flex items-center space-x-2 text-green-600">
                      <CheckCircle className="w-4 h-4" />
                      <span>SSL verification enabled</span>
                    </div>
                    <div className="flex items-center space-x-2 text-green-600">
                      <CheckCircle className="w-4 h-4" />
                      <span>Read-only access to site info</span>
                    </div>
                  </div>
                  <div className="space-y-1">
                    <div className="flex items-center space-x-2 text-green-600">
                      <CheckCircle className="w-4 h-4" />
                      <span>Write access only to posts</span>
                    </div>
                    <div className="flex items-center space-x-2 text-red-600">
                      <AlertCircle className="w-4 h-4" />
                      <span>No access to plugins, themes, or users</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </OnboardingLayout>
  )
}
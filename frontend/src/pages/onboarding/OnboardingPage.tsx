import { useState } from 'react'
import { useAuth } from '@/contexts/AuthContext'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { CheckCircle, Shield } from 'lucide-react'

export default function OnboardingPage() {
  const { user, profile, updateProfile } = useAuth()
  const [loading, setLoading] = useState(false)
  const [step, setStep] = useState(1)
  const [formData, setFormData] = useState({
    full_name: profile?.full_name || '',
    avatar_url: profile?.avatar_url || '',
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      await updateProfile({
        ...formData,
        onboarding_completed: true
      })
      // Redirect will happen automatically via AuthContext
    } catch (error) {
      console.error('Failed to complete onboarding:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }))
  }

  if (!user || !profile) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="spinner"></div>
      </div>
    )
  }

  return (
    <div className="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        {/* Header */}
        <div className="text-center">
          <div className="flex justify-center">
            <div className="w-16 h-16 bg-purple-gradient rounded-xl flex items-center justify-center">
              <Shield className="w-8 h-8 text-white" />
            </div>
          </div>
          <h2 className="mt-6 text-3xl font-bold text-gray-900 dark:text-white">
            Welcome to Blog-Poster!
          </h2>
          <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
            Let's set up your profile to get started
          </p>
        </div>

        {/* Onboarding Form */}
        <Card>
          <CardHeader>
            <CardTitle>Complete Your Profile</CardTitle>
            <CardDescription>
              Help us personalize your experience
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="space-y-4">
                <div>
                  <Label htmlFor="full_name">Full Name</Label>
                  <Input
                    id="full_name"
                    name="full_name"
                    type="text"
                    required
                    className="mt-1"
                    placeholder="Your full name"
                    value={formData.full_name}
                    onChange={(e) => handleInputChange('full_name', e.target.value)}
                  />
                </div>

                <div>
                  <Label htmlFor="avatar_url">Profile Picture URL (Optional)</Label>
                  <Input
                    id="avatar_url"
                    name="avatar_url"
                    type="url"
                    className="mt-1"
                    placeholder="https://example.com/your-photo.jpg"
                    value={formData.avatar_url}
                    onChange={(e) => handleInputChange('avatar_url', e.target.value)}
                  />
                </div>
              </div>

              <div className="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg">
                <div className="flex items-start space-x-3">
                  <CheckCircle className="h-5 w-5 text-blue-600 mt-0.5" />
                  <div>
                    <h3 className="text-sm font-medium text-blue-900 dark:text-blue-100">
                      Organization Created
                    </h3>
                    <p className="text-sm text-blue-700 dark:text-blue-200 mt-1">
                      Your organization "{profile.organization_id}" has been set up. 
                      You can invite team members and manage settings later.
                    </p>
                  </div>
                </div>
              </div>

              <Button
                type="submit"
                className="w-full bg-purple-gradient hover:opacity-90"
                disabled={loading}
              >
                {loading ? (
                  <div className="flex items-center space-x-2">
                    <div className="spinner"></div>
                    <span>Setting up...</span>
                  </div>
                ) : (
                  'Complete Setup'
                )}
              </Button>
            </form>
          </CardContent>
        </Card>

        {/* Footer */}
        <div className="text-center text-xs text-gray-500">
          <p>© 2024 ServiceDogUS. All rights reserved.</p>
        </div>
      </div>
    </div>
  )
}
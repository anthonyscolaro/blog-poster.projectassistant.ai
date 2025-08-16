import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Button } from '@/components/ui/button'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { Badge } from '@/components/ui/badge'
import { Switch } from '@/components/ui/switch'
import { Upload, User, Clock, Mail, Shield } from 'lucide-react'

interface Profile {
  id: string
  email: string
  full_name: string | null
  avatar_url: string | null
  organization_id: string
  role: 'owner' | 'admin' | 'editor' | 'member'
  onboarding_completed?: boolean
  two_factor_enabled?: boolean
  timezone?: string
  notification_preferences?: Record<string, boolean>
  created_at?: string
  updated_at?: string
}

interface ProfileSettingsProps {
  profile: Profile
  onChange: (updates: Partial<Profile>) => void
}

const TIMEZONES = [
  { value: 'America/New_York', label: 'Eastern Time (ET)' },
  { value: 'America/Chicago', label: 'Central Time (CT)' },
  { value: 'America/Denver', label: 'Mountain Time (MT)' },
  { value: 'America/Los_Angeles', label: 'Pacific Time (PT)' },
  { value: 'America/Phoenix', label: 'Arizona Time (MST)' },
  { value: 'America/Anchorage', label: 'Alaska Time (AKST)' },
  { value: 'Pacific/Honolulu', label: 'Hawaii Time (HST)' },
  { value: 'Europe/London', label: 'London (GMT)' },
  { value: 'Europe/Paris', label: 'Paris (CET)' },
  { value: 'Europe/Berlin', label: 'Berlin (CET)' },
  { value: 'Asia/Tokyo', label: 'Tokyo (JST)' },
  { value: 'Asia/Shanghai', label: 'Shanghai (CST)' },
  { value: 'Asia/Kolkata', label: 'Mumbai (IST)' },
  { value: 'Australia/Sydney', label: 'Sydney (AEDT)' }
]

const ROLE_DESCRIPTIONS = {
  owner: 'Full access to all features and settings',
  admin: 'Manage users, settings, and content',
  editor: 'Create and edit content',
  member: 'View and create content'
}

const ROLE_COLORS = {
  owner: 'destructive',
  admin: 'default',
  editor: 'secondary',
  member: 'outline'
} as const

export function ProfileSettings({ profile, onChange }: ProfileSettingsProps) {
  const [isUploadingAvatar, setIsUploadingAvatar] = useState(false)

  const handleInputChange = (field: keyof Profile, value: any) => {
    onChange({ [field]: value })
  }

  const handleNotificationChange = (key: string, enabled: boolean) => {
    const updatedPreferences = {
      ...profile.notification_preferences,
      [key]: enabled
    }
    onChange({ notification_preferences: updatedPreferences })
  }

  const handleAvatarUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (!file) return

    setIsUploadingAvatar(true)
    try {
      // Implement avatar upload logic here
      // For now, just simulate the upload
      await new Promise(resolve => setTimeout(resolve, 2000))
      
      // Update avatar URL after successful upload
      onChange({ avatar_url: URL.createObjectURL(file) })
    } catch (error) {
      console.error('Avatar upload failed:', error)
    } finally {
      setIsUploadingAvatar(false)
    }
  }

  const getInitials = (name: string | null) => {
    if (!name) return profile.email.charAt(0).toUpperCase()
    return name
      .split(' ')
      .map(part => part.charAt(0))
      .join('')
      .toUpperCase()
      .slice(0, 2)
  }

  return (
    <div className="space-y-6">
      {/* Profile Information */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <User className="h-5 w-5" />
            Profile Information
          </CardTitle>
          <CardDescription>
            Update your personal information and preferences
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Avatar Upload */}
          <div className="flex items-center gap-6">
            <Avatar className="h-20 w-20">
              <AvatarImage src={profile.avatar_url || ''} />
              <AvatarFallback className="text-lg">
                {getInitials(profile.full_name)}
              </AvatarFallback>
            </Avatar>
            <div className="space-y-2">
              <Label htmlFor="avatar-upload" className="cursor-pointer">
                <Button
                  variant="outline"
                  size="sm"
                  disabled={isUploadingAvatar}
                  asChild
                >
                  <span>
                    <Upload className="h-4 w-4 mr-2" />
                    {isUploadingAvatar ? 'Uploading...' : 'Change Avatar'}
                  </span>
                </Button>
              </Label>
              <input
                id="avatar-upload"
                type="file"
                accept="image/*"
                className="hidden"
                onChange={handleAvatarUpload}
                disabled={isUploadingAvatar}
              />
              <p className="text-sm text-muted-foreground">
                Upload a square image, max 2MB
              </p>
            </div>
          </div>

          {/* Basic Information */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-2">
              <Label htmlFor="full_name">Full Name</Label>
              <Input
                id="full_name"
                value={profile.full_name || ''}
                onChange={(e) => handleInputChange('full_name', e.target.value)}
                placeholder="Enter your full name"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="email">
                <Mail className="h-4 w-4 inline mr-1" />
                Email Address
              </Label>
              <Input
                id="email"
                value={profile.email}
                disabled
                className="bg-muted"
              />
              <p className="text-sm text-muted-foreground">
                Contact support to change your email address
              </p>
            </div>
          </div>

          {/* Role and Timezone */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-2">
              <Label>
                <Shield className="h-4 w-4 inline mr-1" />
                Role
              </Label>
              <div className="flex items-center gap-2">
                <Badge variant={ROLE_COLORS[profile.role]}>
                  {profile.role.charAt(0).toUpperCase() + profile.role.slice(1)}
                </Badge>
              </div>
              <p className="text-sm text-muted-foreground">
                {ROLE_DESCRIPTIONS[profile.role]}
              </p>
            </div>

            <div className="space-y-2">
              <Label htmlFor="timezone">
                <Clock className="h-4 w-4 inline mr-1" />
                Timezone
              </Label>
              <Select
                value={profile.timezone}
                onValueChange={(value) => handleInputChange('timezone', value)}
              >
                <SelectTrigger id="timezone">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {TIMEZONES.map((tz) => (
                    <SelectItem key={tz.value} value={tz.value}>
                      {tz.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Notification Preferences */}
      <Card>
        <CardHeader>
          <CardTitle>Quick Notification Settings</CardTitle>
          <CardDescription>
            Basic notification preferences (detailed settings in Notifications tab)
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <Label htmlFor="email-notifications">Email Notifications</Label>
              <p className="text-sm text-muted-foreground">
                Receive important updates via email
              </p>
            </div>
            <Switch
              id="email-notifications"
              checked={profile.notification_preferences?.email !== false}
              onCheckedChange={(checked) => handleNotificationChange('email', checked)}
            />
          </div>

          <div className="flex items-center justify-between">
            <div>
              <Label htmlFor="browser-notifications">Browser Notifications</Label>
              <p className="text-sm text-muted-foreground">
                Show notifications in your browser
              </p>
            </div>
            <Switch
              id="browser-notifications"
              checked={profile.notification_preferences?.browser !== false}
              onCheckedChange={(checked) => handleNotificationChange('browser', checked)}
            />
          </div>
        </CardContent>
      </Card>

      {/* Account Information */}
      <Card>
        <CardHeader>
          <CardTitle>Account Information</CardTitle>
          <CardDescription>
            View your account details and activity
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <Label>Member Since</Label>
              <p className="text-sm font-medium">
                {new Date(profile.created_at).toLocaleDateString('en-US', {
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric'
                })}
              </p>
            </div>

            <div>
              <Label>Last Updated</Label>
              <p className="text-sm font-medium">
                {new Date(profile.updated_at).toLocaleDateString('en-US', {
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric'
                })}
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Label } from '@/components/ui/label'
import { Switch } from '@/components/ui/switch'
import { Bell, Mail, Globe, Webhook, Slack } from 'lucide-react'

interface NotificationConfig {
  email: boolean
  browser: boolean
  webhook: boolean
  slack: boolean
}

interface NotificationSettingsProps {
  notifications: NotificationConfig
  onChange: (updates: Partial<NotificationConfig>) => void
}

export function NotificationSettings({ notifications, onChange }: NotificationSettingsProps) {
  const handleToggle = (key: keyof NotificationConfig, value: boolean) => {
    onChange({ [key]: value })
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Bell className="h-5 w-5" />
            Notification Preferences
          </CardTitle>
          <CardDescription>
            Choose how you want to be notified about important events
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Email Notifications */}
          <div className="flex items-center justify-between">
            <div className="space-y-1">
              <Label htmlFor="email-notifications" className="flex items-center gap-2">
                <Mail className="h-4 w-4" />
                Email Notifications
              </Label>
              <p className="text-sm text-muted-foreground">
                Receive important updates and alerts via email
              </p>
            </div>
            <Switch
              id="email-notifications"
              checked={notifications.email}
              onCheckedChange={(checked) => handleToggle('email', checked)}
            />
          </div>

          {/* Browser Notifications */}
          <div className="flex items-center justify-between">
            <div className="space-y-1">
              <Label htmlFor="browser-notifications" className="flex items-center gap-2">
                <Globe className="h-4 w-4" />
                Browser Notifications
              </Label>
              <p className="text-sm text-muted-foreground">
                Show notifications in your browser when the app is open
              </p>
            </div>
            <Switch
              id="browser-notifications"
              checked={notifications.browser}
              onCheckedChange={(checked) => handleToggle('browser', checked)}
            />
          </div>

          {/* Webhook Notifications */}
          <div className="flex items-center justify-between">
            <div className="space-y-1">
              <Label htmlFor="webhook-notifications" className="flex items-center gap-2">
                <Webhook className="h-4 w-4" />
                Webhook Notifications
              </Label>
              <p className="text-sm text-muted-foreground">
                Send notifications to external services via webhooks
              </p>
            </div>
            <Switch
              id="webhook-notifications"
              checked={notifications.webhook}
              onCheckedChange={(checked) => handleToggle('webhook', checked)}
            />
          </div>

          {/* Slack Notifications */}
          <div className="flex items-center justify-between">
            <div className="space-y-1">
              <Label htmlFor="slack-notifications" className="flex items-center gap-2">
                <Slack className="h-4 w-4" />
                Slack Notifications
              </Label>
              <p className="text-sm text-muted-foreground">
                Send notifications to your Slack workspace
              </p>
            </div>
            <Switch
              id="slack-notifications"
              checked={notifications.slack}
              onCheckedChange={(checked) => handleToggle('slack', checked)}
            />
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
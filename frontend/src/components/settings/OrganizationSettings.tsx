import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Badge } from '@/components/ui/badge'
import { Building, Crown, Shield } from 'lucide-react'

interface OrganizationSettingsProps {
  organization: any
  onChange: (updates: any) => void
  userRole: string
}

export function OrganizationSettings({ organization, onChange, userRole }: OrganizationSettingsProps) {
  const canEdit = userRole === 'owner' || userRole === 'admin'

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Building className="h-5 w-5" />
            Organization Details
          </CardTitle>
          <CardDescription>
            Manage your organization settings and subscription
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-2">
              <Label htmlFor="org-name">Organization Name</Label>
              <Input
                id="org-name"
                value={organization?.name || ''}
                onChange={(e) => onChange({ name: e.target.value })}
                disabled={!canEdit}
              />
            </div>

            <div className="space-y-2">
              <Label>Subscription Plan</Label>
              <div className="flex items-center gap-2">
                <Badge variant="default" className="flex items-center gap-1">
                  <Crown className="h-3 w-3" />
                  {organization?.plan || 'Free'}
                </Badge>
                <Badge variant="outline">
                  {organization?.subscription_status || 'Active'}
                </Badge>
              </div>
            </div>
          </div>

          <div className="space-y-2">
            <Label>Your Role</Label>
            <div className="flex items-center gap-2">
              <Badge variant="secondary" className="flex items-center gap-1">
                <Shield className="h-3 w-3" />
                {userRole.charAt(0).toUpperCase() + userRole.slice(1)}
              </Badge>
            </div>
          </div>

          {!canEdit && (
            <p className="text-sm text-muted-foreground">
              You need admin or owner permissions to modify organization settings.
            </p>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
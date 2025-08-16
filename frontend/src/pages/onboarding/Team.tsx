import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { OnboardingLayout } from '@/components/onboarding/OnboardingLayout'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Badge } from '@/components/ui/badge'
import { Users, Mail, Plus, Trash2, Check, Clock, X, Shield, Star } from 'lucide-react'

export default function Team() {
  const navigate = useNavigate()
  const [invites, setInvites] = useState([
    { id: '1', email: '', role: 'editor', status: 'draft' }
  ])
  const [message, setMessage] = useState('Join me on Blog-Poster to streamline our content creation!')
  const [sentInvites, setSentInvites] = useState([
    { id: 'sent1', email: 'sarah@company.com', role: 'admin', status: 'sent', sentAt: '2024-01-15' },
    { id: 'sent2', email: 'mike@company.com', role: 'editor', status: 'accepted', sentAt: '2024-01-15' }
  ])

  const addInvite = () => {
    const newInvite = {
      id: Date.now().toString(),
      email: '',
      role: 'editor',
      status: 'draft'
    }
    setInvites(prev => [...prev, newInvite])
  }

  const removeInvite = (id: string) => {
    setInvites(prev => prev.filter(invite => invite.id !== id))
  }

  const updateInvite = (id: string, field: string, value: string) => {
    setInvites(prev => prev.map(invite => 
      invite.id === id ? { ...invite, [field]: value } : invite
    ))
  }

  const sendInvites = () => {
    const validInvites = invites.filter(invite => invite.email)
    // Simulate sending invites
    const newSentInvites = validInvites.map(invite => ({
      ...invite,
      status: 'sent',
      sentAt: new Date().toISOString().split('T')[0]
    }))
    setSentInvites(prev => [...prev, ...newSentInvites])
    setInvites([{ id: Date.now().toString(), email: '', role: 'editor', status: 'draft' }])
  }

  const handleContinue = () => {
    navigate('/onboarding/complete')
  }

  const handleBack = () => {
    navigate('/onboarding/wordpress')
  }

  const handleSkip = () => {
    navigate('/onboarding/complete')
  }

  const roles = [
    {
      value: 'owner',
      label: 'Owner',
      description: 'Full access to everything',
      icon: Star,
      permissions: ['Everything', 'Billing', 'Team Management', 'API Keys']
    },
    {
      value: 'admin', 
      label: 'Admin',
      description: 'Manage team, settings, and content',
      icon: Shield,
      permissions: ['Team Management', 'Settings', 'All Content', 'Analytics']
    },
    {
      value: 'editor',
      label: 'Editor', 
      description: 'Create and edit content',
      icon: Users,
      permissions: ['Create Content', 'Edit All Content', 'Publish', 'Analytics']
    },
    {
      value: 'member',
      label: 'Member',
      description: 'Create content, limited editing',
      icon: Users,
      permissions: ['Create Content', 'Edit Own Content', 'View Analytics']
    },
    {
      value: 'viewer',
      label: 'Viewer',
      description: 'Read-only access to content',
      icon: Users,
      permissions: ['View Content', 'View Analytics']
    }
  ]

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'sent':
        return <Clock className="w-4 h-4 text-yellow-500" />
      case 'accepted':
        return <Check className="w-4 h-4 text-green-500" />
      case 'declined':
        return <X className="w-4 h-4 text-red-500" />
      default:
        return null
    }
  }

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'sent':
        return <Badge variant="secondary">Sent</Badge>
      case 'accepted':
        return <Badge variant="default" className="bg-green-500">Accepted</Badge>
      case 'declined':
        return <Badge variant="destructive">Declined</Badge>
      default:
        return null
    }
  }

  const hasValidInvites = invites.some(invite => invite.email)

  return (
    <OnboardingLayout
      currentStep={5}
      totalSteps={5}
      stepName="Invite your team"
      onBack={handleBack}
      onSkip={handleSkip}
      onContinue={handleContinue}
      canContinue={true}
    >
      <div className="space-y-8">
        {/* Header */}
        <div className="text-center space-y-2">
          <Users className="w-12 h-12 text-primary mx-auto" />
          <h1 className="text-2xl font-bold text-foreground">
            Invite Your Team
          </h1>
          <p className="text-muted-foreground">
            Collaborate on content creation and management
          </p>
        </div>

        {/* Team Benefits */}
        <Card className="bg-gradient-to-r from-primary/5 to-primary/10 border-primary/20">
          <CardContent className="p-6">
            <h3 className="font-semibold text-foreground mb-4">With team collaboration you can:</h3>
            <div className="grid md:grid-cols-2 gap-4 text-sm">
              <div className="space-y-2">
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-primary rounded-full" />
                  <span>Assign content creation to team members</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-primary rounded-full" />
                  <span>Set up approval workflows</span>
                </div>
              </div>
              <div className="space-y-2">
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-primary rounded-full" />
                  <span>Track team productivity and costs</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-primary rounded-full" />
                  <span>Share API keys across the organization</span>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Invite Form */}
        <Card>
          <CardHeader>
            <CardTitle>Send Invitations</CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Invite List */}
            <div className="space-y-4">
              {invites.map((invite, index) => (
                <div key={invite.id} className="flex items-center space-x-4 p-4 border border-border rounded-lg">
                  <div className="flex-1 grid md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor={`email-${invite.id}`}>Email Address</Label>
                      <Input
                        id={`email-${invite.id}`}
                        type="email"
                        value={invite.email}
                        onChange={(e) => updateInvite(invite.id, 'email', e.target.value)}
                        placeholder="colleague@company.com"
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor={`role-${invite.id}`}>Role</Label>
                      <Select 
                        value={invite.role} 
                        onValueChange={(value) => updateInvite(invite.id, 'role', value)}
                      >
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          {roles.slice(1).map(role => (
                            <SelectItem key={role.value} value={role.value}>
                              <div className="flex items-center space-x-2">
                                <role.icon className="w-4 h-4" />
                                <span>{role.label}</span>
                              </div>
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                  </div>
                  {invites.length > 1 && (
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => removeInvite(invite.id)}
                      className="text-muted-foreground hover:text-destructive"
                    >
                      <Trash2 className="w-4 h-4" />
                    </Button>
                  )}
                </div>
              ))}
              
              <Button
                onClick={addInvite}
                variant="outline"
                className="w-full border-dashed"
              >
                <Plus className="w-4 h-4 mr-2" />
                Add Another Invitation
              </Button>
            </div>

            {/* Personal Message */}
            <div className="space-y-2">
              <Label htmlFor="message">Personal Message (Optional)</Label>
              <Textarea
                id="message"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder="Add a personal note to your invitation..."
                rows={3}
              />
            </div>

            {/* Send Button */}
            <Button
              onClick={sendInvites}
              disabled={!hasValidInvites}
              className="w-full"
            >
              <Mail className="w-4 h-4 mr-2" />
              Send Invitations
            </Button>
          </CardContent>
        </Card>

        {/* Pending Invitations */}
        {sentInvites.length > 0 && (
          <Card>
            <CardHeader>
              <CardTitle>Pending Invitations</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {sentInvites.map((invite) => (
                  <div key={invite.id} className="flex items-center justify-between p-3 border border-border rounded-lg">
                    <div className="flex items-center space-x-3">
                      {getStatusIcon(invite.status)}
                      <div>
                        <div className="font-medium">{invite.email}</div>
                        <div className="text-sm text-muted-foreground">
                          {roles.find(r => r.value === invite.role)?.label} • Sent {invite.sentAt}
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      {getStatusBadge(invite.status)}
                      {invite.status === 'sent' && (
                        <Button variant="ghost" size="sm" className="text-xs">
                          Resend
                        </Button>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}

        {/* Role Explanations */}
        <Card>
          <CardHeader>
            <CardTitle>Role Permissions</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid gap-4">
              {roles.slice(1).map((role) => (
                <div key={role.value} className="flex items-start space-x-3 p-3 border border-border rounded-lg">
                  <role.icon className="w-5 h-5 text-primary mt-0.5" />
                  <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-1">
                      <span className="font-semibold">{role.label}</span>
                      <span className="text-sm text-muted-foreground">- {role.description}</span>
                    </div>
                    <div className="flex flex-wrap gap-2">
                      {role.permissions.map((permission) => (
                        <Badge key={permission} variant="outline" className="text-xs">
                          {permission}
                        </Badge>
                      ))}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Skip Option */}
        <Card className="text-center bg-muted/50">
          <CardContent className="p-6">
            <h3 className="font-semibold text-foreground mb-2">Working solo? No problem!</h3>
            <p className="text-sm text-muted-foreground mb-4">
              You can invite team members anytime from your organization settings.
            </p>
            <Button onClick={handleSkip} variant="outline" size="lg">
              Skip Team Setup
            </Button>
          </CardContent>
        </Card>

        {/* Billing Note */}
        <Card className="bg-muted/50">
          <CardContent className="p-4">
            <h4 className="font-semibold text-foreground mb-2">💡 Billing Information</h4>
            <ul className="text-sm text-muted-foreground space-y-1">
              <li>• Team members don&apos;t affect your billing</li>
              <li>• You pay per article generated, not per user</li>
              <li>• API costs are shared across your organization</li>
              <li>• Only owners can manage billing and subscriptions</li>
            </ul>
          </CardContent>
        </Card>
      </div>
    </OnboardingLayout>
  )
}
import { useState } from 'react'
import { Card, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { 
  MoreHorizontal, 
  MessageCircle, 
  UserCheck, 
  UserX,
  Calendar,
  TrendingUp,
  Clock
} from 'lucide-react'
import { RoleBadge } from './RoleBadge'

interface TeamMemberCardProps {
  member: {
    id: string
    full_name: string | null
    email: string
    avatar_url: string | null
    role: string
    created_at: string
    last_activity_at: string | null
  }
  canManage: boolean
  onRoleChange: (newRole: string) => void
  onRemove: () => void
}

export function TeamMemberCard({ member, canManage, onRoleChange, onRemove }: TeamMemberCardProps) {
  const [showActions, setShowActions] = useState(false)

  const formatLastActive = (date: string | null) => {
    if (!date) return 'Never'
    const now = new Date()
    const lastActive = new Date(date)
    const diffInMinutes = Math.floor((now.getTime() - lastActive.getTime()) / (1000 * 60))

    if (diffInMinutes < 60) return `${diffInMinutes}m ago`
    if (diffInMinutes < 1440) return `${Math.floor(diffInMinutes / 60)}h ago`
    return `${Math.floor(diffInMinutes / 1440)}d ago`
  }

  const isOnline = member.last_activity_at && 
    new Date().getTime() - new Date(member.last_activity_at).getTime() < 5 * 60 * 1000

  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardContent className="p-6">
        <div className="flex items-start justify-between mb-4">
          <div className="flex items-center gap-3">
            <div className="relative">
              <Avatar className="h-12 w-12">
                <AvatarImage src={member.avatar_url || undefined} />
                <AvatarFallback>
                  {member.full_name?.split(' ').map(n => n[0]).join('') || 'U'}
                </AvatarFallback>
              </Avatar>
              {isOnline && (
                <div className="absolute -bottom-1 -right-1 w-4 h-4 bg-green-500 border-2 border-white rounded-full"></div>
              )}
            </div>
            
            <div className="flex-1 min-w-0">
              <h3 className="font-semibold text-sm truncate">
                {member.full_name || member.email}
              </h3>
              <p className="text-xs text-muted-foreground truncate">
                {member.email}
              </p>
            </div>
          </div>

          <RoleBadge role={member.role} />
        </div>

        {/* Member Stats */}
        <div className="space-y-2 mb-4">
          <div className="flex items-center justify-between text-xs">
            <span className="text-muted-foreground">Member since</span>
            <span>{new Date(member.created_at).toLocaleDateString()}</span>
          </div>
          
          <div className="flex items-center justify-between text-xs">
            <span className="text-muted-foreground">Last active</span>
            <span>{formatLastActive(member.last_activity_at)}</span>
          </div>

          <div className="flex items-center justify-between text-xs">
            <span className="text-muted-foreground">Articles</span>
            <span>12 this month</span>
          </div>

          <div className="flex items-center justify-between text-xs">
            <span className="text-muted-foreground">Quality score</span>
            <span className="flex items-center gap-1">
              <TrendingUp className="h-3 w-3 text-green-500" />
              95%
            </span>
          </div>
        </div>

        {/* Actions */}
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm" className="flex-1">
            <MessageCircle className="h-3 w-3 mr-1" />
            Message
          </Button>
          
          {canManage && (
            <div className="flex items-center gap-1">
              <Select
                value={member.role}
                onValueChange={onRoleChange}
              >
                <SelectTrigger className="w-20 h-8 text-xs">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="admin">Admin</SelectItem>
                  <SelectItem value="editor">Editor</SelectItem>
                  <SelectItem value="member">Member</SelectItem>
                  <SelectItem value="viewer">Viewer</SelectItem>
                </SelectContent>
              </Select>
              
              <Button
                variant="ghost"
                size="sm"
                className="h-8 w-8 p-0 text-red-600 hover:text-red-700"
                onClick={onRemove}
              >
                <UserX className="h-3 w-3" />
              </Button>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  )
}
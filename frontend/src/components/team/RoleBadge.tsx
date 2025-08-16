import { Badge } from '@/components/ui/badge'
import { Crown, Shield, Edit, User, Eye } from 'lucide-react'

interface RoleBadgeProps {
  role: string
  size?: 'sm' | 'md' | 'lg'
  showIcon?: boolean
}

export function RoleBadge({ role, size = 'sm', showIcon = true }: RoleBadgeProps) {
  const getRoleConfig = (role: string) => {
    switch (role) {
      case 'owner':
        return {
          label: 'Owner',
          variant: 'default' as const,
          className: 'bg-purple-100 text-purple-800 hover:bg-purple-100 dark:bg-purple-900 dark:text-purple-300',
          icon: Crown
        }
      case 'admin':
        return {
          label: 'Admin',
          variant: 'default' as const,
          className: 'bg-blue-100 text-blue-800 hover:bg-blue-100 dark:bg-blue-900 dark:text-blue-300',
          icon: Shield
        }
      case 'editor':
        return {
          label: 'Editor',
          variant: 'default' as const,
          className: 'bg-green-100 text-green-800 hover:bg-green-100 dark:bg-green-900 dark:text-green-300',
          icon: Edit
        }
      case 'member':
        return {
          label: 'Member',
          variant: 'default' as const,
          className: 'bg-gray-100 text-gray-800 hover:bg-gray-100 dark:bg-gray-700 dark:text-gray-300',
          icon: User
        }
      case 'viewer':
        return {
          label: 'Viewer',
          variant: 'default' as const,
          className: 'bg-gray-100 text-gray-600 hover:bg-gray-100 dark:bg-gray-800 dark:text-gray-400',
          icon: Eye
        }
      default:
        return {
          label: role,
          variant: 'default' as const,
          className: 'bg-gray-100 text-gray-800 hover:bg-gray-100 dark:bg-gray-700 dark:text-gray-300',
          icon: User
        }
    }
  }

  const config = getRoleConfig(role)
  const Icon = config.icon

  const sizeClasses = {
    sm: 'text-xs px-2 py-1',
    md: 'text-sm px-3 py-1',
    lg: 'text-base px-4 py-2'
  }

  return (
    <Badge 
      variant={config.variant}
      className={`${config.className} ${sizeClasses[size]} flex items-center gap-1`}
    >
      {showIcon && <Icon className={`${size === 'sm' ? 'h-3 w-3' : size === 'md' ? 'h-4 w-4' : 'h-5 w-5'}`} />}
      {config.label}
    </Badge>
  )
}
import React from 'react'
import { motion } from 'framer-motion'
import { 
  FileText, 
  Workflow, 
  Users, 
  BarChart3, 
  Package, 
  AlertCircle,
  Search,
  Filter,
  Plus,
  Settings,
  CreditCard,
  Mail
} from 'lucide-react'
import { Button } from './button'

interface EmptyStateProps {
  icon: React.ComponentType<{ className?: string }>
  title: string
  description: string
  action?: {
    label: string
    onClick: () => void
    variant?: 'default' | 'outline'
  }
  secondaryAction?: {
    label: string
    onClick: () => void
  }
  className?: string
}

export function EmptyState({
  icon: Icon,
  title,
  description,
  action,
  secondaryAction,
  className
}: EmptyStateProps) {
  return (
    <motion.div 
      className={`flex flex-col items-center justify-center py-12 px-4 text-center ${className}`}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <motion.div 
        className="w-16 h-16 bg-muted rounded-full flex items-center justify-center mb-6"
        initial={{ scale: 0.8 }}
        animate={{ scale: 1 }}
        transition={{ delay: 0.2 }}
      >
        <Icon className="w-8 h-8 text-muted-foreground" />
      </motion.div>
      
      <motion.h3 
        className="text-lg font-semibold text-foreground mb-2"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3 }}
      >
        {title}
      </motion.h3>
      
      <motion.p 
        className="text-muted-foreground mb-6 max-w-sm"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.4 }}
      >
        {description}
      </motion.p>
      
      {(action || secondaryAction) && (
        <motion.div 
          className="flex flex-col sm:flex-row gap-3"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
        >
          {action && (
            <Button
              onClick={action.onClick}
              variant={action.variant || 'default'}
              className="min-w-[140px]"
            >
              {action.label}
            </Button>
          )}
          {secondaryAction && (
            <Button
              onClick={secondaryAction.onClick}
              variant="outline"
              className="min-w-[140px]"
            >
              {secondaryAction.label}
            </Button>
          )}
        </motion.div>
      )}
    </motion.div>
  )
}

// Predefined empty states for common scenarios
export const EmptyStates = {
  articles: {
    icon: FileText,
    title: "No articles yet",
    description: "Start generating your first SEO-optimized article with our 5-agent pipeline.",
    action: {
      label: "Generate First Article",
      onClick: () => window.location.href = '/pipeline'
    }
  },
  
  pipelines: {
    icon: Workflow,
    title: "No active pipelines",
    description: "Configure and start a pipeline to begin generating content automatically.",
    action: {
      label: "Start Pipeline", 
      onClick: () => window.location.href = '/pipeline'
    }
  },
  
  team: {
    icon: Users,
    title: "No team members",
    description: "Invite team members to collaborate on content generation and management.",
    action: {
      label: "Invite Team Member",
      onClick: () => {} // Will be provided by parent component
    }
  },

  analytics: {
    icon: BarChart3,
    title: "No analytics data",
    description: "Analytics will appear here once you start generating and publishing articles.",
    action: {
      label: "Generate Content",
      onClick: () => window.location.href = '/pipeline'
    }
  },

  search: {
    icon: Search,
    title: "No results found",
    description: "Try adjusting your search terms or filters to find what you're looking for.",
    action: {
      label: "Clear Filters",
      onClick: () => {},
      variant: 'outline' as const
    }
  },

  filtered: {
    icon: Filter,
    title: "No items match your filters",
    description: "Try removing some filters or adjusting your criteria to see more results.",
    action: {
      label: "Reset Filters",
      onClick: () => {},
      variant: 'outline' as const
    }
  },

  settings: {
    icon: Settings,
    title: "Configure your settings",
    description: "Complete your configuration to start using all platform features.",
    action: {
      label: "Configure Now",
      onClick: () => {}
    }
  },

  billing: {
    icon: CreditCard,
    title: "No billing history",
    description: "Your billing transactions and invoices will appear here.",
    action: {
      label: "View Plans",
      onClick: () => window.location.href = '/billing'
    }
  },

  notifications: {
    icon: Mail,
    title: "No notifications",
    description: "You're all caught up! New notifications will appear here.",
  }
}

// Specialized empty states for specific use cases
export function SearchEmptyState({ 
  query, 
  onClearSearch 
}: { 
  query: string
  onClearSearch: () => void 
}) {
  return (
    <EmptyState
      icon={Search}
      title={`No results for "${query}"`}
      description="Try searching with different keywords or check your spelling."
      action={{
        label: "Clear Search",
        onClick: onClearSearch,
        variant: 'outline'
      }}
    />
  )
}

export function ErrorEmptyState({ 
  title = "Something went wrong",
  description = "We encountered an error loading this data.",
  onRetry 
}: {
  title?: string
  description?: string 
  onRetry: () => void
}) {
  return (
    <EmptyState
      icon={AlertCircle}
      title={title}
      description={description}
      action={{
        label: "Try Again",
        onClick: onRetry
      }}
    />
  )
}

export function FirstTimeEmptyState({
  title,
  description,
  primaryAction,
  secondaryAction
}: {
  title: string
  description: string
  primaryAction: { label: string; onClick: () => void }
  secondaryAction?: { label: string; onClick: () => void }
}) {
  return (
    <EmptyState
      icon={Package}
      title={title}
      description={description}
      action={primaryAction}
      secondaryAction={secondaryAction}
      className="py-20"
    />
  )
}
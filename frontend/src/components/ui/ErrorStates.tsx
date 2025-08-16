import React from 'react'
import { motion } from 'framer-motion'
import { AlertTriangle, AlertCircle, WifiOff, Server, RefreshCw, Home } from 'lucide-react'
import { Button } from './button'

interface ErrorStateProps {
  error?: Error | string
  title?: string
  description?: string
  retry?: () => void
  showDetails?: boolean
  variant?: 'error' | 'warning' | 'offline' | 'server'
  className?: string
}

export function ErrorState({
  error,
  title,
  description,
  retry,
  showDetails = false,
  variant = 'error',
  className
}: ErrorStateProps) {
  const errorMessage = typeof error === 'string' ? error : error?.message || 'An unexpected error occurred'
  
  const variants = {
    error: {
      icon: AlertCircle,
      bgColor: 'bg-destructive/10',
      iconColor: 'text-destructive',
      title: title || 'Something went wrong',
      description: description || errorMessage
    },
    warning: {
      icon: AlertTriangle,
      bgColor: 'bg-yellow-100 dark:bg-yellow-900/20',
      iconColor: 'text-yellow-600 dark:text-yellow-400',
      title: title || 'Warning',
      description: description || errorMessage
    },
    offline: {
      icon: WifiOff,
      bgColor: 'bg-gray-100 dark:bg-gray-800',
      iconColor: 'text-gray-500',
      title: title || 'You\'re offline',
      description: description || 'Check your internet connection and try again.'
    },
    server: {
      icon: Server,
      bgColor: 'bg-destructive/10',
      iconColor: 'text-destructive',
      title: title || 'Server error',
      description: description || 'Our servers are experiencing issues. Please try again later.'
    }
  }

  const config = variants[variant]
  const Icon = config.icon

  return (
    <motion.div 
      className={`rounded-lg p-6 text-center ${config.bgColor} ${className}`}
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.3 }}
    >
      <motion.div
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{ delay: 0.1, type: "spring", stiffness: 200 }}
      >
        <Icon className={`w-12 h-12 mx-auto mb-4 ${config.iconColor}`} />
      </motion.div>
      
      <motion.h3 
        className="text-lg font-semibold text-foreground mb-2"
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
      >
        {config.title}
      </motion.h3>
      
      <motion.p 
        className="text-muted-foreground mb-4"
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
      >
        {config.description}
      </motion.p>

      {showDetails && error && typeof error !== 'string' && (
        <motion.details 
          className="text-left mb-4 p-3 bg-muted rounded text-sm"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
        >
          <summary className="cursor-pointer font-medium mb-2">Error Details</summary>
          <pre className="text-xs overflow-auto text-muted-foreground">
            {error.stack || error.message}
          </pre>
        </motion.details>
      )}
      
      {retry && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
        >
          <Button 
            onClick={retry}
            variant="default"
            leftIcon={<RefreshCw className="w-4 h-4" />}
          >
            Try Again
          </Button>
        </motion.div>
      )}
    </motion.div>
  )
}

// Specialized error components
export function NetworkErrorState({ retry }: { retry: () => void }) {
  return (
    <ErrorState
      variant="offline"
      title="Connection lost"
      description="Please check your internet connection and try again."
      retry={retry}
    />
  )
}

export function ServerErrorState({ retry }: { retry: () => void }) {
  return (
    <ErrorState
      variant="server"
      title="Server unavailable"
      description="We're experiencing technical difficulties. Please try again in a few moments."
      retry={retry}
    />
  )
}

export function NotFoundErrorState({ onGoHome }: { onGoHome: () => void }) {
  return (
    <div className="flex flex-col items-center justify-center py-20 text-center">
      <motion.div 
        className="text-6xl font-bold text-muted-foreground mb-4"
        initial={{ opacity: 0, scale: 0.5 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
      >
        404
      </motion.div>
      
      <motion.h1 
        className="text-2xl font-semibold text-foreground mb-2"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
      >
        Page Not Found
      </motion.h1>
      
      <motion.p 
        className="text-muted-foreground mb-6 max-w-sm"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
      >
        The page you're looking for doesn't exist or has been moved.
      </motion.p>
      
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
      >
        <Button 
          onClick={onGoHome}
          leftIcon={<Home className="w-4 h-4" />}
        >
          Go to Dashboard
        </Button>
      </motion.div>
    </div>
  )
}

export function UnauthorizedErrorState({ onLogin }: { onLogin: () => void }) {
  return (
    <ErrorState
      variant="warning"
      title="Access denied"
      description="You don't have permission to view this page. Please sign in or contact your administrator."
      retry={onLogin}
    />
  )
}

// Error boundary fallback component
export function ErrorBoundaryFallback({ 
  error, 
  resetErrorBoundary 
}: { 
  error: Error
  resetErrorBoundary: () => void 
}) {
  return (
    <div className="min-h-[400px] flex items-center justify-center p-8">
      <ErrorState
        error={error}
        title="Application Error"
        description="Something went wrong with the application. Please try refreshing the page."
        retry={resetErrorBoundary}
        showDetails={process.env.NODE_ENV === 'development'}
        className="max-w-md w-full"
      />
    </div>
  )
}
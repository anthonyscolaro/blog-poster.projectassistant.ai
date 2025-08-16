import React from 'react'
import { AlertTriangle, RefreshCw } from 'lucide-react'
import { Button } from './button'

interface ErrorBoundaryState {
  hasError: boolean
  error?: Error
}

interface ErrorBoundaryProps {
  children: React.ReactNode
  fallback?: React.ComponentType<{ error?: Error; resetError: () => void }>
  onError?: (error: Error, errorInfo: React.ErrorInfo) => void
}

export class ErrorBoundary extends React.Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props)
    this.state = { hasError: false }
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error }
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('ErrorBoundary caught an error:', error, errorInfo)
    this.props.onError?.(error, errorInfo)
  }

  resetError = () => {
    this.setState({ hasError: false, error: undefined })
  }

  render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        const FallbackComponent = this.props.fallback
        return <FallbackComponent error={this.state.error} resetError={this.resetError} />
      }

      return <DefaultErrorFallback error={this.state.error} resetError={this.resetError} />
    }

    return this.props.children
  }
}

function DefaultErrorFallback({ error, resetError }: { error?: Error; resetError: () => void }) {
  return (
    <div className="min-h-[400px] flex items-center justify-center p-8">
      <div className="text-center max-w-md">
        <div className="mb-6">
          <AlertTriangle className="h-16 w-16 text-destructive mx-auto mb-4" />
          <h2 className="text-2xl font-semibold text-foreground mb-2">
            Something went wrong
          </h2>
          <p className="text-muted-foreground mb-4">
            An unexpected error occurred. Please try refreshing the page or contact support if the problem persists.
          </p>
          
          {error && import.meta.env.DEV && (
            <details className="text-left mb-4 p-4 bg-muted rounded-lg">
              <summary className="cursor-pointer font-medium text-foreground mb-2">
                Error Details
              </summary>
              <pre className="text-xs text-destructive overflow-auto">
                {error.stack || error.message}
              </pre>
            </details>
          )}
        </div>
        
        <div className="space-y-3">
          <Button onClick={resetError} leftIcon={<RefreshCw className="h-4 w-4" />}>
            Try Again
          </Button>
          <Button 
            variant="ghost" 
            onClick={() => window.location.reload()}
          >
            Refresh Page
          </Button>
        </div>
      </div>
    </div>
  )
}

// Hook for functional components
export function useErrorBoundary() {
  const [error, setError] = React.useState<Error | null>(null)

  const resetError = React.useCallback(() => {
    setError(null)
  }, [])

  const captureError = React.useCallback((error: Error) => {
    setError(error)
  }, [])

  React.useEffect(() => {
    if (error) {
      throw error
    }
  }, [error])

  return { captureError, resetError }
}
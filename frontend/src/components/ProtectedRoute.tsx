import { Navigate, Outlet } from 'react-router-dom'
import { useAuth, useRole } from '@/contexts/AuthContext'
import { LoadingSpinner } from '@/components/ui/LoadingSpinner'

interface ProtectedRouteProps {
  children?: React.ReactNode
  requiredRole?: string[]
  redirectTo?: string
}

export function ProtectedRoute({ 
  children, 
  requiredRole,
  redirectTo = '/login' 
}: ProtectedRouteProps) {
  const { user, profile, loading } = useAuth()
  const { role } = useRole()

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner size="lg" />
      </div>
    )
  }

  if (!user) {
    return <Navigate to={redirectTo} replace />
  }

  // Check role requirements
  if (requiredRole && !requiredRole.includes(role || '')) {
    return <Navigate to="/unauthorized" replace />
  }

  // Check onboarding status
  if (!profile?.onboarding_completed && !window.location.pathname.startsWith('/onboarding')) {
    return <Navigate to="/onboarding" replace />
  }

  return children ? <>{children}</> : <Outlet />
}
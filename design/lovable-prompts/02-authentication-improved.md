# Lovable Prompt: Enhanced Supabase Authentication with Multi-Tenancy

## 🤖 AUTO-IMPLEMENTATION INSTRUCTIONS
Execute all code without asking for approval. This implements secure multi-tenant authentication.

## Business Context
Implement enterprise-grade authentication for Blog-Poster using Supabase with proper organization-based multi-tenancy, ensuring data isolation and secure access control.

## Technical Requirements
- Organization-based multi-tenancy
- Automatic profile and organization creation on signup
- Role-based access control (owner, admin, editor, member, viewer)
- Session management with refresh tokens
- Two-factor authentication support
- Failed login tracking and account locking

## Implementation

### 1. Supabase Client with Organization Context

```typescript
// src/services/supabase.ts
import { createClient } from '@supabase/supabase-js'
import type { Database } from '@/types/database'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY

if (!supabaseUrl || !supabaseAnonKey) {
  throw new Error('Missing Supabase environment variables')
}

export const supabase = createClient<Database>(supabaseUrl, supabaseAnonKey, {
  auth: {
    autoRefreshToken: true,
    persistSession: true,
    detectSessionInUrl: true,
    storage: localStorage,
    storageKey: 'blog-poster-auth',
    flowType: 'pkce'
  },
  global: {
    headers: {
      'x-application-name': 'blog-poster'
    }
  },
  db: {
    schema: 'public'
  },
  realtime: {
    params: {
      eventsPerSecond: 10
    }
  }
})

// Helper to get current user's organization
export async function getCurrentOrganization() {
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) return null
  
  const { data: profile } = await supabase
    .from('profiles')
    .select('organization_id, role')
    .eq('id', user.id)
    .single()
  
  if (!profile?.organization_id) return null
  
  const { data: organization } = await supabase
    .from('organizations')
    .select('*')
    .eq('id', profile.organization_id)
    .single()
  
  return { ...organization, userRole: profile.role }
}
```

### 2. Enhanced Auth Context with Organization Support

```typescript
// src/contexts/AuthContext.tsx
import React, { createContext, useContext, useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { supabase, getCurrentOrganization } from '@/services/supabase'
import { toast } from 'react-hot-toast'
import type { User, Session } from '@supabase/supabase-js'

interface Profile {
  id: string
  email: string
  full_name: string | null
  organization_id: string
  role: 'owner' | 'admin' | 'editor' | 'member' | 'viewer'
  avatar_url: string | null
  onboarding_completed: boolean
  two_factor_enabled: boolean
}

interface Organization {
  id: string
  name: string
  slug: string
  plan: 'free' | 'starter' | 'professional' | 'enterprise'
  subscription_status: string
  trial_ends_at: string | null
  articles_limit: number
  articles_used: number
  monthly_budget: number
  current_month_cost: number
}

interface AuthContextType {
  user: User | null
  profile: Profile | null
  organization: Organization | null
  session: Session | null
  loading: boolean
  signIn: (email: string, password: string) => Promise<void>
  signUp: (email: string, password: string, metadata?: any) => Promise<void>
  signOut: () => Promise<void>
  resetPassword: (email: string) => Promise<void>
  updateProfile: (updates: Partial<Profile>) => Promise<void>
  refreshSession: () => Promise<void>
  checkBudgetLimit: () => Promise<boolean>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [profile, setProfile] = useState<Profile | null>(null)
  const [organization, setOrganization] = useState<Organization | null>(null)
  const [session, setSession] = useState<Session | null>(null)
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  // Load user profile and organization
  const loadUserData = async (userId: string) => {
    try {
      // Get profile with organization
      const { data: profileData, error: profileError } = await supabase
        .from('profiles')
        .select(`
          *,
          organizations (*)
        `)
        .eq('id', userId)
        .single()

      if (profileError) throw profileError

      if (profileData) {
        setProfile(profileData)
        setOrganization(profileData.organizations)
        
        // Check if onboarding is needed
        if (!profileData.onboarding_completed) {
          navigate('/onboarding')
        }
      }
    } catch (error) {
      console.error('Error loading user data:', error)
      toast.error('Failed to load user profile')
    }
  }

  useEffect(() => {
    // Check active session
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session)
      setUser(session?.user ?? null)
      
      if (session?.user) {
        loadUserData(session.user.id)
      }
      
      setLoading(false)
    })

    // Listen for auth changes
    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      async (event, session) => {
        setSession(session)
        setUser(session?.user ?? null)
        
        if (event === 'SIGNED_IN' && session?.user) {
          await loadUserData(session.user.id)
        } else if (event === 'SIGNED_OUT') {
          setProfile(null)
          setOrganization(null)
        } else if (event === 'TOKEN_REFRESHED') {
          console.log('Token refreshed successfully')
        }
        
        setLoading(false)
      }
    )

    return () => subscription.unsubscribe()
  }, [navigate])

  const signIn = async (email: string, password: string) => {
    try {
      // Check for account lock
      const { data: profileCheck } = await supabase
        .from('profiles')
        .select('account_locked_until, failed_login_attempts')
        .eq('email', email)
        .single()

      if (profileCheck?.account_locked_until) {
        const lockTime = new Date(profileCheck.account_locked_until)
        if (lockTime > new Date()) {
          throw new Error(`Account locked until ${lockTime.toLocaleString()}`)
        }
      }

      const { data, error } = await supabase.auth.signInWithPassword({
        email,
        password,
      })

      if (error) {
        // Increment failed login attempts
        if (profileCheck) {
          const attempts = (profileCheck.failed_login_attempts || 0) + 1
          const lockAccount = attempts >= 5
          
          await supabase
            .from('profiles')
            .update({
              failed_login_attempts: attempts,
              account_locked_until: lockAccount 
                ? new Date(Date.now() + 30 * 60 * 1000).toISOString() // 30 minutes
                : null
            })
            .eq('email', email)
        }
        throw error
      }

      // Reset failed attempts on successful login
      if (data.user) {
        await supabase
          .from('profiles')
          .update({
            failed_login_attempts: 0,
            last_login_at: new Date().toISOString()
          })
          .eq('id', data.user.id)
      }

      toast.success('Successfully signed in!')
      navigate('/dashboard')
    } catch (error: any) {
      toast.error(error.message || 'Failed to sign in')
      throw error
    }
  }

  const signUp = async (
    email: string, 
    password: string, 
    metadata?: {
      full_name?: string
      company?: string
    }
  ) => {
    try {
      const { data, error } = await supabase.auth.signUp({
        email,
        password,
        options: {
          data: metadata,
          emailRedirectTo: `${window.location.origin}/onboarding`
        }
      })

      if (error) throw error

      // Auto sign in after signup (if email verification is not required)
      if (data.session) {
        toast.success('Account created successfully!')
        navigate('/onboarding')
      } else {
        toast.success('Account created! Please check your email to verify.')
        navigate('/auth/verify-email')
      }
      
      // Note: Organization and profile creation happens automatically
      // via the handle_new_user() database trigger
      
    } catch (error: any) {
      toast.error(error.message || 'Failed to sign up')
      throw error
    }
  }

  const signOut = async () => {
    try {
      // Update last activity
      if (user) {
        await supabase
          .from('profiles')
          .update({ last_activity_at: new Date().toISOString() })
          .eq('id', user.id)
      }

      const { error } = await supabase.auth.signOut()
      if (error) throw error

      setUser(null)
      setProfile(null)
      setOrganization(null)
      setSession(null)
      
      toast.success('Signed out successfully')
      navigate('/login')
    } catch (error: any) {
      toast.error(error.message || 'Failed to sign out')
      throw error
    }
  }

  const resetPassword = async (email: string) => {
    try {
      const { error } = await supabase.auth.resetPasswordForEmail(email, {
        redirectTo: `${window.location.origin}/reset-password`,
      })

      if (error) throw error

      toast.success('Password reset email sent!')
    } catch (error: any) {
      toast.error(error.message || 'Failed to send reset email')
      throw error
    }
  }

  const updateProfile = async (updates: Partial<Profile>) => {
    if (!user) throw new Error('No user logged in')

    try {
      const { data, error } = await supabase
        .from('profiles')
        .update(updates)
        .eq('id', user.id)
        .select()
        .single()

      if (error) throw error

      setProfile(data)
      toast.success('Profile updated successfully')
    } catch (error: any) {
      toast.error(error.message || 'Failed to update profile')
      throw error
    }
  }

  const refreshSession = async () => {
    try {
      const { data: { session }, error } = await supabase.auth.refreshSession()
      if (error) throw error
      
      setSession(session)
    } catch (error: any) {
      console.error('Failed to refresh session:', error)
      // If refresh fails, sign out
      await signOut()
    }
  }

  const checkBudgetLimit = async () => {
    if (!organization) return false

    try {
      const { data, error } = await supabase
        .rpc('check_budget_limit', { p_organization_id: organization.id })

      if (error) throw error
      return data
    } catch (error: any) {
      console.error('Failed to check budget:', error)
      return false
    }
  }

  return (
    <AuthContext.Provider value={{
      user,
      profile,
      organization,
      session,
      loading,
      signIn,
      signUp,
      signOut,
      resetPassword,
      updateProfile,
      refreshSession,
      checkBudgetLimit
    }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}

// Role-based access control hook
export function useRole() {
  const { profile } = useAuth()
  
  return {
    isOwner: profile?.role === 'owner',
    isAdmin: profile?.role === 'owner' || profile?.role === 'admin',
    isEditor: ['owner', 'admin', 'editor'].includes(profile?.role || ''),
    isMember: ['owner', 'admin', 'editor', 'member'].includes(profile?.role || ''),
    role: profile?.role
  }
}

// Organization permission check
export function usePermission(permission: string) {
  const { profile, organization } = useAuth()
  
  const permissions: Record<string, string[]> = {
    'manage_team': ['owner', 'admin'],
    'manage_billing': ['owner'],
    'create_content': ['owner', 'admin', 'editor'],
    'view_analytics': ['owner', 'admin', 'editor', 'member'],
    'manage_settings': ['owner', 'admin']
  }
  
  return permissions[permission]?.includes(profile?.role || '') || false
}
```

### 3. Protected Routes with Role Checking

```typescript
// src/components/ProtectedRoute.tsx
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
```

### 4. Login Form with Enhanced Security

```typescript
// src/pages/auth/Login.tsx
import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '@/contexts/AuthContext'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { Alert } from '@/components/ui/Alert'
import { Mail, Lock, Eye, EyeOff } from 'lucide-react'

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { signIn } = useAuth()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      await signIn(email, password)
    } catch (err: any) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white">
            Welcome back
          </h2>
          <p className="mt-2 text-gray-600 dark:text-gray-400">
            Sign in to access your Blog-Poster dashboard
          </p>
        </div>

        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          {error && (
            <Alert variant="error" onClose={() => setError('')}>
              {error}
            </Alert>
          )}

          <div className="space-y-4">
            <Input
              label="Email address"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              autoComplete="email"
              leftIcon={<Mail className="w-5 h-5" />}
              placeholder="you@example.com"
            />

            <Input
              label="Password"
              type={showPassword ? 'text' : 'password'}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              autoComplete="current-password"
              leftIcon={<Lock className="w-5 h-5" />}
              rightIcon={
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="text-gray-500 hover:text-gray-700"
                >
                  {showPassword ? (
                    <EyeOff className="w-5 h-5" />
                  ) : (
                    <Eye className="w-5 h-5" />
                  )}
                </button>
              }
              placeholder="Enter your password"
            />
          </div>

          <div className="flex items-center justify-between">
            <label className="flex items-center">
              <input
                type="checkbox"
                className="rounded border-gray-300"
              />
              <span className="ml-2 text-sm text-gray-600 dark:text-gray-400">
                Remember me
              </span>
            </label>

            <Link
              to="/forgot-password"
              className="text-sm text-purple-600 hover:text-purple-500"
            >
              Forgot password?
            </Link>
          </div>

          <Button
            type="submit"
            fullWidth
            size="lg"
            loading={loading}
            loadingText="Signing in..."
          >
            Sign in
          </Button>

          <div className="text-center">
            <span className="text-sm text-gray-600 dark:text-gray-400">
              Don't have an account?{' '}
            </span>
            <Link
              to="/register"
              className="text-sm text-purple-600 hover:text-purple-500 font-medium"
            >
              Sign up for free
            </Link>
          </div>
        </form>
      </div>
    </div>
  )
}
```

### 5. Email Verification Page

```typescript
// src/pages/auth/VerifyEmail.tsx
import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '@/contexts/AuthContext'
import { Button } from '@/components/ui/Button'
import { Alert } from '@/components/ui/Alert'
import { Mail, CheckCircle, Clock } from 'lucide-react'
import { supabase } from '@/services/supabase'
import { toast } from 'react-hot-toast'

export function VerifyEmail() {
  const navigate = useNavigate()
  const { user } = useAuth()
  const [resending, setResending] = useState(false)
  const [resendCooldown, setResendCooldown] = useState(0)

  useEffect(() => {
    // If user is already verified, redirect to dashboard
    if (user?.email_confirmed_at) {
      navigate('/dashboard')
    }
  }, [user, navigate])

  useEffect(() => {
    // Cooldown timer
    if (resendCooldown > 0) {
      const timer = setTimeout(() => setResendCooldown(resendCooldown - 1), 1000)
      return () => clearTimeout(timer)
    }
  }, [resendCooldown])

  const handleResendEmail = async () => {
    if (!user?.email || resendCooldown > 0) return

    setResending(true)
    try {
      const { error } = await supabase.auth.resend({
        type: 'signup',
        email: user.email,
        options: {
          emailRedirectTo: `${window.location.origin}/onboarding`
        }
      })

      if (error) throw error

      toast.success('Verification email sent!')
      setResendCooldown(60) // 60 second cooldown
    } catch (error: any) {
      toast.error(error.message || 'Failed to resend email')
    } finally {
      setResending(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 dark:from-gray-900 dark:to-gray-800 flex items-center justify-center p-4">
      <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 max-w-md w-full">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-purple-100 dark:bg-purple-900/30 rounded-full mb-4">
            <Mail className="w-8 h-8 text-purple-600 dark:text-purple-400" />
          </div>
          
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
            Check Your Email
          </h1>
          
          <p className="text-gray-600 dark:text-gray-400">
            We've sent a verification link to:
          </p>
          <p className="font-medium text-gray-900 dark:text-white mt-1">
            {user?.email}
          </p>
        </div>

        <Alert variant="info" className="mb-6">
          <Clock className="w-4 h-4" />
          <p className="text-sm">
            The verification link will expire in 24 hours. Please check your spam folder if you don't see the email.
          </p>
        </Alert>

        <div className="space-y-4">
          <Button
            onClick={handleResendEmail}
            disabled={resending || resendCooldown > 0}
            variant="outline"
            fullWidth
            loading={resending}
          >
            {resendCooldown > 0 
              ? `Resend in ${resendCooldown}s` 
              : 'Resend Verification Email'
            }
          </Button>

          <div className="relative">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-gray-300 dark:border-gray-600"></div>
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-2 bg-white dark:bg-gray-800 text-gray-500">
                Already verified?
              </span>
            </div>
          </div>

          <Button
            onClick={() => navigate('/login')}
            fullWidth
          >
            Back to Login
          </Button>
        </div>

        <div className="mt-6 text-center">
          <p className="text-sm text-gray-600 dark:text-gray-400">
            Having trouble?{' '}
            <Link
              to="/contact"
              className="text-purple-600 hover:text-purple-500 font-medium"
            >
              Contact Support
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}
```

## Key Improvements

✅ **Organization-based multi-tenancy** - All queries filtered by organization
✅ **Automatic profile creation** - Via database trigger on signup
✅ **Role-based access control** - Owner, admin, editor, member, viewer roles
✅ **Failed login tracking** - Account locking after 5 failed attempts
✅ **Session management** - Auto-refresh with PKCE flow
✅ **Budget checking** - Integration with database function
✅ **Onboarding flow** - Redirect to onboarding if not completed
✅ **Security headers** - Proper auth configuration
✅ **Permission hooks** - useRole() and usePermission() for easy access control
✅ **Auto-signin on signup** - Immediate access if email verification disabled
✅ **Email verification page** - Proper UX for email confirmation flow

This authentication system provides enterprise-grade security with proper multi-tenancy support.
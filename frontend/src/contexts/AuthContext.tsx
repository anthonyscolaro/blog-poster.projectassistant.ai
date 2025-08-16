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
  const loadUserData = async (userId: string, retryCount = 0) => {
    try {
      // Get profile with organization
      const { data: profileData, error: profileError } = await supabase
        .from('profiles')
        .select(`
          *,
          organizations (*)
        `)
        .eq('id', userId)
        .maybeSingle()

      // If profile doesn't exist yet (new user), wait and retry
      if (!profileData && retryCount < 3) {
        console.log(`Profile not found, retrying in ${(retryCount + 1) * 1000}ms...`)
        setTimeout(() => {
          loadUserData(userId, retryCount + 1)
        }, (retryCount + 1) * 1000)
        return
      }

      if (profileError) {
        throw profileError
      }

      if (profileData) {
        setProfile(profileData as Profile)
        setOrganization(profileData.organizations as any)
        
        // Check if onboarding is needed
        if (!profileData.onboarding_completed) {
          navigate('/onboarding')
        }
      } else if (retryCount >= 3) {
        // After max retries, redirect to onboarding to let user complete setup
        console.warn('Profile not found after retries, redirecting to onboarding')
        navigate('/onboarding')
      }
    } catch (error) {
      console.error('Error loading user data:', error)
      if (retryCount < 3) {
        // Retry on error for new users
        setTimeout(() => {
          loadUserData(userId, retryCount + 1)
        }, (retryCount + 1) * 1000)
      } else {
        toast.error('Unable to load profile. Please try refreshing the page.')
      }
    }
  }

  useEffect(() => {
    // Check active session
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session)
      setUser(session?.user ?? null)
      
      if (session?.user) {
        setTimeout(() => {
          loadUserData(session.user.id)
        }, 0)
      }
      
      setLoading(false)
    })

    // Listen for auth changes
    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      async (event, session) => {
        setSession(session)
        setUser(session?.user ?? null)
        
        if (event === 'SIGNED_IN' && session?.user) {
          setTimeout(() => {
            loadUserData(session.user.id)
          }, 0)
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

      setProfile(data as Profile)
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
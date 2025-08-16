import { supabase } from '@/integrations/supabase/client'

// Get JWT token for API calls
export async function getAuthToken(): Promise<string | null> {
  const { data: { session } } = await supabase.auth.getSession()
  return session?.access_token || null
}

// Add organization context to headers
export async function getAuthHeaders(): Promise<Record<string, string>> {
  const token = await getAuthToken()
  
  // Get organization ID from current user's profile
  let organizationId = ''
  try {
    const { data: { user } } = await supabase.auth.getUser()
    if (user) {
      const { data: profile } = await supabase
        .from('profiles')
        .select('organization_id')
        .eq('id', user.id)
        .single()
      
      organizationId = profile?.organization_id || ''
    }
  } catch (error) {
    console.warn('Failed to get organization ID:', error)
  }
  
  return {
    'Authorization': token ? `Bearer ${token}` : '',
    'X-Organization-ID': organizationId,
    'Content-Type': 'application/json'
  }
}

// Check if user is authenticated
export async function isAuthenticated(): Promise<boolean> {
  const token = await getAuthToken()
  return !!token
}

// Get current user ID
export async function getCurrentUserId(): Promise<string | null> {
  const { data: { user } } = await supabase.auth.getUser()
  return user?.id || null
}
import { createClient } from '@supabase/supabase-js'
import type { Database } from '@/integrations/supabase/types'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL || "https://epftkydwdqerdlhvqili.supabase.co"
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY || "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVwZnRreWR3ZHFlcmRsaHZxaWxpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTUyODQ1NDAsImV4cCI6MjA3MDg2MDU0MH0.Mn9Re4itgw0w7Qi2RyD4V0vmGx8tLtJPNdbNtpP0-Ng"

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
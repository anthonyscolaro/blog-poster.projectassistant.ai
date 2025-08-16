import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Toaster } from 'react-hot-toast'
import { ThemeProvider } from '@/contexts/ThemeContext'
import { AuthProvider } from '@/contexts/AuthContext'
import { PublicLayout } from '@/components/layout/PublicLayout'
import { AppLayout } from '@/components/layout/AppLayout'
import { ProtectedRoute } from '@/components/ProtectedRoute'
import { AdminRoute } from '@/components/AdminRoute'

// Public Pages
import Landing from '@/pages/public/Landing'
import Pricing from '@/pages/public/Pricing'
import Features from '@/pages/public/Features'
import About from '@/pages/public/About'
import Contact from '@/pages/public/Contact'
import Privacy from '@/pages/public/Privacy'
import Terms from '@/pages/public/Terms'

// Auth Pages
import Login from '@/pages/auth/Login'
import Register from '@/pages/auth/Register'
import { VerifyEmail } from '@/pages/auth/VerifyEmail'

// Onboarding Pages
import Welcome from '@/pages/onboarding/Welcome'
import Profile from '@/pages/onboarding/Profile'
import ApiKeys from '@/pages/onboarding/ApiKeys'
import WordPress from '@/pages/onboarding/WordPress'
import OnboardingTeam from '@/pages/onboarding/Team'
import Complete from '@/pages/onboarding/Complete'

// Team Management Pages
import Team from '@/pages/team/Team'
import TeamMembers from '@/pages/team/TeamMembers'

// Dashboard Pages
import Dashboard from '@/pages/dashboard/Dashboard'
import Pipeline from '@/pages/Pipeline'
import Articles from '@/pages/Articles'
import { ArticleEditor } from '@/components/articles/ArticleEditor'
import Settings from '@/pages/settings/Settings'

// Admin Pages
import AdminDashboard from '@/pages/admin/AdminDashboard'
import UserManagement from '@/pages/admin/UserManagement'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60 * 1000,
      refetchOnWindowFocus: false,
    },
  },
})

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider>
        <Router>
          <AuthProvider>
            <Routes>
              {/* Public Routes */}
              <Route element={<PublicLayout />}>
                <Route path="/" element={<Landing />} />
                <Route path="/pricing" element={<Pricing />} />
                <Route path="/features" element={<Features />} />
                <Route path="/about" element={<About />} />
                <Route path="/contact" element={<Contact />} />
                <Route path="/privacy" element={<Privacy />} />
                <Route path="/terms" element={<Terms />} />
              </Route>

              {/* Auth Routes */}
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/auth/verify-email" element={<VerifyEmail />} />

              {/* Onboarding Routes */}
              <Route path="/onboarding" element={<Welcome />} />
              <Route path="/onboarding/profile" element={<Profile />} />
              <Route path="/onboarding/api-keys" element={<ApiKeys />} />
              <Route path="/onboarding/wordpress" element={<WordPress />} />
              <Route path="/onboarding/team" element={<OnboardingTeam />} />
              <Route path="/onboarding/complete" element={<Complete />} />

              {/* Protected App Routes */}
              <Route
                element={
                  <ProtectedRoute>
                    <AppLayout />
                  </ProtectedRoute>
                }
              >
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/pipeline" element={<Pipeline />} />
                <Route path="/articles" element={<Articles />} />
                <Route path="/articles/:id" element={<ArticleEditor />} />
                <Route path="/team" element={<Team />} />
                <Route path="/team/members" element={<TeamMembers />} />
                <Route path="/team/invite" element={<div className="p-6"><h1 className="text-2xl font-bold">Invite Team</h1><p className="text-gray-600 mt-2">Team invitation features coming soon...</p></div>} />
                <Route path="/team/roles" element={<div className="p-6"><h1 className="text-2xl font-bold">Team Roles</h1><p className="text-gray-600 mt-2">Role management coming soon...</p></div>} />
                <Route path="/team/activity" element={<div className="p-6"><h1 className="text-2xl font-bold">Team Activity</h1><p className="text-gray-600 mt-2">Activity tracking coming soon...</p></div>} />
                <Route path="/team/settings" element={<div className="p-6"><h1 className="text-2xl font-bold">Team Settings</h1><p className="text-gray-600 mt-2">Team settings coming soon...</p></div>} />
                <Route path="/analytics" element={<div className="p-6"><h1 className="text-2xl font-bold">Analytics</h1><p className="text-gray-600 mt-2">Analytics dashboard coming soon...</p></div>} />
                <Route path="/billing" element={<div className="p-6"><h1 className="text-2xl font-bold">Billing</h1><p className="text-gray-600 mt-2">Billing management coming soon...</p></div>} />
                <Route path="/monitoring" element={<div className="p-6"><h1 className="text-2xl font-bold">Monitoring</h1><p className="text-gray-600 mt-2">System monitoring coming soon...</p></div>} />
                 <Route path="/settings" element={<Settings />} />
                 
                 {/* Admin Routes */}
                 <Route path="/admin" element={<AdminRoute><AdminDashboard /></AdminRoute>} />
                 <Route path="/admin/users" element={<AdminRoute><UserManagement /></AdminRoute>} />
              </Route>

              {/* Catch all route */}
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
            <Toaster
              position="top-right"
              toastOptions={{
                duration: 4000,
                style: {
                  background: 'var(--background)',
                  color: 'var(--foreground)',
                  border: '1px solid var(--border)',
                },
              }}
            />
          </AuthProvider>
        </Router>
      </ThemeProvider>
    </QueryClientProvider>
  )
}

export default App;

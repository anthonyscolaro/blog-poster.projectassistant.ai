# Lovable Prompt: Complete Routing & Pages Setup

## Overview:
This file contains the complete routing configuration and ALL page components for the Blog-Poster dashboard. Every route will work without 404 errors, and all pages include proper TypeScript, responsive design, and the purple gradient theme.

## Router Configuration:

### Main App Component with Complete Router Setup
```typescript
// src/App.tsx
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
import { Toaster } from 'react-hot-toast'
import { ThemeProvider } from '@/contexts/ThemeContext'
import { AuthProvider } from '@/contexts/AuthContext'
import { PublicLayout } from '@/components/layout/PublicLayout'
import { AppLayout } from '@/components/layout/AppLayout'
import { AdminLayout } from '@/components/layout/AdminLayout'
import { ProtectedRoute } from '@/components/ProtectedRoute'
import { AdminRoute } from '@/components/AdminRoute'

// Public Pages
import Landing from '@/pages/public/Landing'
import Pricing from '@/pages/public/Pricing'
import Features from '@/pages/public/Features'
import About from '@/pages/public/About'
import Blog from '@/pages/public/Blog'
import BlogPost from '@/pages/public/BlogPost'
import Contact from '@/pages/public/Contact'
import Privacy from '@/pages/public/Privacy'
import Terms from '@/pages/public/Terms'

// Auth Pages
import Login from '@/pages/auth/Login'
import Register from '@/pages/auth/Register'
import ForgotPassword from '@/pages/auth/ForgotPassword'
import ResetPassword from '@/pages/auth/ResetPassword'

// Onboarding Pages
import Welcome from '@/pages/onboarding/Welcome'
import ProfileSetup from '@/pages/onboarding/Profile'
import ApiKeysSetup from '@/pages/onboarding/ApiKeys'
import WordPressSetup from '@/pages/onboarding/WordPress'
import TeamSetup from '@/pages/onboarding/Team'
import OnboardingComplete from '@/pages/onboarding/Complete'

// Dashboard Pages
import Dashboard from '@/pages/dashboard/Dashboard'
import QuickStart from '@/pages/dashboard/QuickStart'

// Pipeline Pages
import Pipeline from '@/pages/pipeline/Pipeline'
import NewPipeline from '@/pages/pipeline/NewPipeline'
import PipelineDetails from '@/pages/pipeline/PipelineDetails'
import PipelineLogs from '@/pages/pipeline/PipelineLogs'
import PipelineHistory from '@/pages/pipeline/PipelineHistory'
import PipelineTemplates from '@/pages/pipeline/PipelineTemplates'

// Article Pages
import Articles from '@/pages/articles/Articles'
import NewArticle from '@/pages/articles/NewArticle'
import ArticleDetail from '@/pages/articles/ArticleDetail'
import EditArticle from '@/pages/articles/EditArticle'
import ArticleSEO from '@/pages/articles/ArticleSEO'
import ArticlePreview from '@/pages/articles/ArticlePreview'
import DraftArticles from '@/pages/articles/DraftArticles'
import PublishedArticles from '@/pages/articles/PublishedArticles'
import ScheduledArticles from '@/pages/articles/ScheduledArticles'

// Team Pages
import Team from '@/pages/team/Team'
import TeamMembers from '@/pages/team/TeamMembers'
import InviteTeam from '@/pages/team/InviteTeam'
import TeamRoles from '@/pages/team/TeamRoles'
import TeamActivity from '@/pages/team/TeamActivity'
import TeamSettings from '@/pages/team/TeamSettings'

// Billing Pages
import Billing from '@/pages/billing/Billing'
import Subscription from '@/pages/billing/Subscription'
import UpgradePlan from '@/pages/billing/UpgradePlan'
import Usage from '@/pages/billing/Usage'
import Invoices from '@/pages/billing/Invoices'
import PaymentMethods from '@/pages/billing/PaymentMethods'
import PaymentHistory from '@/pages/billing/PaymentHistory'

// Settings Pages
import Settings from '@/pages/settings/Settings'
import ProfileSettings from '@/pages/settings/ProfileSettings'
import OrganizationSettings from '@/pages/settings/OrganizationSettings'
import ApiKeysSettings from '@/pages/settings/ApiKeysSettings'
import WordPressSettings from '@/pages/settings/WordPressSettings'
import NotificationSettings from '@/pages/settings/NotificationSettings'
import SecuritySettings from '@/pages/settings/SecuritySettings'
import IntegrationSettings from '@/pages/settings/IntegrationSettings'
import WebhookSettings from '@/pages/settings/WebhookSettings'
import BrandingSettings from '@/pages/settings/BrandingSettings'

// Analytics Pages
import Analytics from '@/pages/analytics/Analytics'
import ContentAnalytics from '@/pages/analytics/ContentAnalytics'
import SEOAnalytics from '@/pages/analytics/SEOAnalytics'
import CostAnalytics from '@/pages/analytics/CostAnalytics'
import TeamAnalytics from '@/pages/analytics/TeamAnalytics'
import ExportData from '@/pages/analytics/ExportData'

// Monitoring Pages
import Monitoring from '@/pages/monitoring/Monitoring'
import AgentMonitoring from '@/pages/monitoring/AgentMonitoring'
import ErrorTracking from '@/pages/monitoring/ErrorTracking'
import ApiUsage from '@/pages/monitoring/ApiUsage'
import WebhookLogs from '@/pages/monitoring/WebhookLogs'

// Admin Pages
import AdminDashboard from '@/pages/admin/AdminDashboard'
import UserManagement from '@/pages/admin/UserManagement'
import OrganizationManagement from '@/pages/admin/OrganizationManagement'
import BillingManagement from '@/pages/admin/BillingManagement'
import ContentModeration from '@/pages/admin/ContentModeration'
import SystemSettings from '@/pages/admin/SystemSettings'
import SystemLogs from '@/pages/admin/SystemLogs'
import PlatformMetrics from '@/pages/admin/PlatformMetrics'
import SupportTickets from '@/pages/admin/SupportTickets'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60 * 1000, // 1 minute
      refetchOnWindowFocus: false,
    },
  },
})

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider>
        <AuthProvider>
          <Router>
            <Routes>
              {/* Public Routes */}
              <Route element={<PublicLayout />}>
                <Route path="/" element={<Landing />} />
                <Route path="/pricing" element={<Pricing />} />
                <Route path="/features" element={<Features />} />
                <Route path="/about" element={<About />} />
                <Route path="/blog" element={<Blog />} />
                <Route path="/blog/:slug" element={<BlogPost />} />
                <Route path="/contact" element={<Contact />} />
                <Route path="/privacy" element={<Privacy />} />
                <Route path="/terms" element={<Terms />} />
              </Route>

              {/* Auth Routes */}
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/forgot-password" element={<ForgotPassword />} />
              <Route path="/reset-password" element={<ResetPassword />} />

              {/* Onboarding Routes */}
              <Route
                path="/onboarding"
                element={
                  <ProtectedRoute>
                    <Welcome />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/onboarding/profile"
                element={
                  <ProtectedRoute>
                    <ProfileSetup />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/onboarding/api-keys"
                element={
                  <ProtectedRoute>
                    <ApiKeysSetup />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/onboarding/wordpress"
                element={
                  <ProtectedRoute>
                    <WordPressSetup />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/onboarding/team"
                element={
                  <ProtectedRoute>
                    <TeamSetup />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/onboarding/complete"
                element={
                  <ProtectedRoute>
                    <OnboardingComplete />
                  </ProtectedRoute>
                }
              />

              {/* App Routes */}
              <Route
                element={
                  <ProtectedRoute>
                    <AppLayout />
                  </ProtectedRoute>
                }
              >
                {/* Dashboard */}
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/dashboard/quick-start" element={<QuickStart />} />

                {/* Pipeline Management */}
                <Route path="/pipeline" element={<Pipeline />} />
                <Route path="/pipeline/new" element={<NewPipeline />} />
                <Route path="/pipeline/:id" element={<PipelineDetails />} />
                <Route path="/pipeline/:id/logs" element={<PipelineLogs />} />
                <Route path="/pipeline/history" element={<PipelineHistory />} />
                <Route path="/pipeline/templates" element={<PipelineTemplates />} />

                {/* Article Management */}
                <Route path="/articles" element={<Articles />} />
                <Route path="/articles/new" element={<NewArticle />} />
                <Route path="/articles/:id" element={<ArticleDetail />} />
                <Route path="/articles/:id/edit" element={<EditArticle />} />
                <Route path="/articles/:id/seo" element={<ArticleSEO />} />
                <Route path="/articles/:id/preview" element={<ArticlePreview />} />
                <Route path="/articles/drafts" element={<DraftArticles />} />
                <Route path="/articles/published" element={<PublishedArticles />} />
                <Route path="/articles/scheduled" element={<ScheduledArticles />} />

                {/* Team Management */}
                <Route path="/team" element={<Team />} />
                <Route path="/team/members" element={<TeamMembers />} />
                <Route path="/team/invite" element={<InviteTeam />} />
                <Route path="/team/roles" element={<TeamRoles />} />
                <Route path="/team/activity" element={<TeamActivity />} />
                <Route path="/team/settings" element={<TeamSettings />} />

                {/* Billing */}
                <Route path="/billing" element={<Billing />} />
                <Route path="/billing/subscription" element={<Subscription />} />
                <Route path="/billing/upgrade" element={<UpgradePlan />} />
                <Route path="/billing/usage" element={<Usage />} />
                <Route path="/billing/invoices" element={<Invoices />} />
                <Route path="/billing/payment" element={<PaymentMethods />} />
                <Route path="/billing/history" element={<PaymentHistory />} />

                {/* Settings */}
                <Route path="/settings" element={<Settings />} />
                <Route path="/settings/profile" element={<ProfileSettings />} />
                <Route path="/settings/organization" element={<OrganizationSettings />} />
                <Route path="/settings/api-keys" element={<ApiKeysSettings />} />
                <Route path="/settings/wordpress" element={<WordPressSettings />} />
                <Route path="/settings/notifications" element={<NotificationSettings />} />
                <Route path="/settings/security" element={<SecuritySettings />} />
                <Route path="/settings/integrations" element={<IntegrationSettings />} />
                <Route path="/settings/webhooks" element={<WebhookSettings />} />
                <Route path="/settings/branding" element={<BrandingSettings />} />

                {/* Analytics */}
                <Route path="/analytics" element={<Analytics />} />
                <Route path="/analytics/content" element={<ContentAnalytics />} />
                <Route path="/analytics/seo" element={<SEOAnalytics />} />
                <Route path="/analytics/costs" element={<CostAnalytics />} />
                <Route path="/analytics/team" element={<TeamAnalytics />} />
                <Route path="/analytics/export" element={<ExportData />} />

                {/* Monitoring */}
                <Route path="/monitoring" element={<Monitoring />} />
                <Route path="/monitoring/agents" element={<AgentMonitoring />} />
                <Route path="/monitoring/errors" element={<ErrorTracking />} />
                <Route path="/monitoring/api" element={<ApiUsage />} />
                <Route path="/monitoring/webhooks" element={<WebhookLogs />} />
              </Route>

              {/* Admin Routes */}
              <Route
                element={
                  <AdminRoute>
                    <AdminLayout />
                  </AdminRoute>
                }
              >
                <Route path="/admin" element={<AdminDashboard />} />
                <Route path="/admin/users" element={<UserManagement />} />
                <Route path="/admin/organizations" element={<OrganizationManagement />} />
                <Route path="/admin/billing" element={<BillingManagement />} />
                <Route path="/admin/content" element={<ContentModeration />} />
                <Route path="/admin/system" element={<SystemSettings />} />
                <Route path="/admin/logs" element={<SystemLogs />} />
                <Route path="/admin/metrics" element={<PlatformMetrics />} />
                <Route path="/admin/support" element={<SupportTickets />} />
              </Route>

              {/* Catch all route */}
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </Router>
          <Toaster
            position="top-right"
            toastOptions={{
              duration: 4000,
              style: {
                background: '#363636',
                color: '#fff',
              },
            }}
          />
        </AuthProvider>
      </ThemeProvider>
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  )
}

export default App
```

### Layout Components with Sidebar Navigation

```typescript
// src/components/layout/AppLayout.tsx
import { Outlet, NavLink } from 'react-router-dom'
import { useState } from 'react'
import {
  LayoutDashboard,
  Workflow,
  FileText,
  Activity,
  Settings,
  Menu,
  X,
  Moon,
  Sun,
  LogOut,
  Users,
  CreditCard,
  BarChart3
} from 'lucide-react'
import { useTheme } from '@/contexts/ThemeContext'
import { useAuth } from '@/contexts/AuthContext'

const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
  { name: 'Pipeline', href: '/pipeline', icon: Workflow },
  { name: 'Articles', href: '/articles', icon: FileText },
  { name: 'Team', href: '/team', icon: Users },
  { name: 'Analytics', href: '/analytics', icon: BarChart3 },
  { name: 'Billing', href: '/billing', icon: CreditCard },
  { name: 'Monitoring', href: '/monitoring', icon: Activity },
  { name: 'Settings', href: '/settings', icon: Settings },
]

export function AppLayout() {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const { theme, toggleTheme } = useTheme()
  const { user, signOut } = useAuth()

  return (
    <div className="min-h-screen bg-dashboard-bg dark:bg-dashboard-dark">
      {/* Mobile sidebar backdrop */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 z-40 bg-black bg-opacity-50 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <div
        className={`fixed inset-y-0 left-0 z-50 w-64 bg-white dark:bg-gray-900 transform transition-transform lg:translate-x-0 ${
          sidebarOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <div className="flex h-full flex-col">
          {/* Logo */}
          <div className="flex h-16 items-center justify-between px-4 bg-purple-gradient">
            <h1 className="text-xl font-bold text-white">Blog-Poster</h1>
            <button
              onClick={() => setSidebarOpen(false)}
              className="text-white lg:hidden"
            >
              <X className="h-6 w-6" />
            </button>
          </div>

          {/* Navigation */}
          <nav className="flex-1 space-y-1 px-2 py-4">
            {navigation.map((item) => (
              <NavLink
                key={item.name}
                to={item.href}
                className={({ isActive }) =>
                  `group flex items-center px-2 py-2 text-sm font-medium rounded-md transition-colors ${
                    isActive
                      ? 'bg-primary-100 dark:bg-primary-900 text-primary-700 dark:text-primary-200'
                      : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800'
                  }`
                }
              >
                <item.icon className="mr-3 h-5 w-5" />
                {item.name}
              </NavLink>
            ))}
          </nav>

          {/* User section */}
          <div className="border-t border-gray-200 dark:border-gray-700 p-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <div className="h-8 w-8 rounded-full bg-primary-500 flex items-center justify-center text-white">
                  {user?.email?.[0].toUpperCase() || 'U'}
                </div>
                <div className="ml-3">
                  <p className="text-sm font-medium text-gray-700 dark:text-gray-300">
                    {user?.email || 'user@example.com'}
                  </p>
                </div>
              </div>
              <button
                onClick={signOut}
                className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
              >
                <LogOut className="h-5 w-5" />
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Main content */}
      <div className="lg:pl-64">
        {/* Top bar */}
        <div className="sticky top-0 z-30 flex h-16 items-center gap-4 border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 px-4">
          <button
            onClick={() => setSidebarOpen(true)}
            className="text-gray-500 lg:hidden"
          >
            <Menu className="h-6 w-6" />
          </button>
          
          <div className="flex flex-1 items-center justify-end gap-4">
            {/* Theme toggle */}
            <button
              onClick={toggleTheme}
              className="p-2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
            >
              {theme === 'dark' ? (
                <Sun className="h-5 w-5" />
              ) : (
                <Moon className="h-5 w-5" />
              )}
            </button>
          </div>
        </div>

        {/* Page content */}
        <main className="p-4 md:p-6 lg:p-8">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
```

### Public Layout
```typescript
// src/components/layout/PublicLayout.tsx
import { Outlet, Link } from 'react-router-dom'
import { useTheme } from '@/contexts/ThemeContext'
import { Moon, Sun } from 'lucide-react'

export function PublicLayout() {
  const { theme, toggleTheme } = useTheme()

  return (
    <div className="min-h-screen bg-white dark:bg-gray-900">
      {/* Navigation */}
      <nav className="border-b border-gray-200 dark:border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <Link to="/" className="flex items-center space-x-2">
                <div className="h-8 w-8 rounded bg-purple-gradient flex items-center justify-center">
                  <span className="text-white font-bold text-sm">BP</span>
                </div>
                <span className="text-xl font-bold text-gray-900 dark:text-white">
                  Blog-Poster
                </span>
              </Link>
            </div>

            <div className="flex items-center space-x-8">
              <Link
                to="/features"
                className="text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white"
              >
                Features
              </Link>
              <Link
                to="/pricing"
                className="text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white"
              >
                Pricing
              </Link>
              <Link
                to="/about"
                className="text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white"
              >
                About
              </Link>
              <Link
                to="/contact"
                className="text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white"
              >
                Contact
              </Link>
              <button
                onClick={toggleTheme}
                className="p-2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
              >
                {theme === 'dark' ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
              </button>
              <Link
                to="/login"
                className="text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white"
              >
                Sign in
              </Link>
              <Link
                to="/register"
                className="bg-purple-gradient text-white px-4 py-2 rounded-md hover:opacity-90"
              >
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </nav>

      <Outlet />

      {/* Footer */}
      <footer className="bg-gray-50 dark:bg-gray-800">
        <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            <div>
              <h3 className="text-sm font-semibold text-gray-400 tracking-wider uppercase">
                Product
              </h3>
              <ul className="mt-4 space-y-4">
                <li>
                  <Link to="/features" className="text-base text-gray-500 hover:text-gray-900">
                    Features
                  </Link>
                </li>
                <li>
                  <Link to="/pricing" className="text-base text-gray-500 hover:text-gray-900">
                    Pricing
                  </Link>
                </li>
              </ul>
            </div>
            <div>
              <h3 className="text-sm font-semibold text-gray-400 tracking-wider uppercase">
                Company
              </h3>
              <ul className="mt-4 space-y-4">
                <li>
                  <Link to="/about" className="text-base text-gray-500 hover:text-gray-900">
                    About
                  </Link>
                </li>
                <li>
                  <Link to="/contact" className="text-base text-gray-500 hover:text-gray-900">
                    Contact
                  </Link>
                </li>
              </ul>
            </div>
            <div>
              <h3 className="text-sm font-semibold text-gray-400 tracking-wider uppercase">
                Legal
              </h3>
              <ul className="mt-4 space-y-4">
                <li>
                  <Link to="/privacy" className="text-base text-gray-500 hover:text-gray-900">
                    Privacy
                  </Link>
                </li>
                <li>
                  <Link to="/terms" className="text-base text-gray-500 hover:text-gray-900">
                    Terms
                  </Link>
                </li>
              </ul>
            </div>
          </div>
          <div className="mt-8 border-t border-gray-200 pt-8">
            <p className="text-base text-gray-400 text-center">
              &copy; 2024 Blog-Poster. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}
```

### Admin Layout
```typescript
// src/components/layout/AdminLayout.tsx
import { Outlet } from 'react-router-dom'
import { AppLayout } from './AppLayout'

export function AdminLayout() {
  return <AppLayout />
}
```

### Protected Route Component
```typescript
// src/components/ProtectedRoute.tsx
import { useAuth } from '@/contexts/AuthContext'
import { Navigate } from 'react-router-dom'

interface ProtectedRouteProps {
  children: React.ReactNode
}

export function ProtectedRoute({ children }: ProtectedRouteProps) {
  const { user, loading } = useAuth()

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="spinner"></div>
      </div>
    )
  }

  if (!user) {
    return <Navigate to="/login" replace />
  }

  return <>{children}</>
}
```

### Admin Route Component
```typescript
// src/components/AdminRoute.tsx
import { useAuth } from '@/contexts/AuthContext'
import { Navigate } from 'react-router-dom'

interface AdminRouteProps {
  children: React.ReactNode
}

export function AdminRoute({ children }: AdminRouteProps) {
  const { user, loading } = useAuth()

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="spinner"></div>
      </div>
    )
  }

  if (!user || user.role !== 'admin') {
    return <Navigate to="/dashboard" replace />
  }

  return <>{children}</>
}
```

### Auth Context Provider (React 19 Enhanced)
```typescript
// src/contexts/AuthContext.tsx
import { createContext, useContext, useEffect, useState, use } from 'react'

interface User {
  id: string
  email: string
  name: string
  role: 'user' | 'admin'
}

interface AuthContextType {
  user: User | null
  loading: boolean
  signIn: (email: string, password: string) => Promise<void>
  signUp: (email: string, password: string, name: string) => Promise<void>
  signOut: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Simulate checking for existing session
    const checkAuth = () => {
      const savedUser = localStorage.getItem('user')
      if (savedUser) {
        setUser(JSON.parse(savedUser))
      }
      setLoading(false)
    }

    checkAuth()
  }, [])

  const signIn = async (email: string, password: string) => {
    // React 19 Actions can be used for form submissions with automatic pending states
    // Simulate API call
    const mockUser: User = {
      id: '1',
      email,
      name: 'Test User',
      role: 'user'
    }
    setUser(mockUser)
    localStorage.setItem('user', JSON.stringify(mockUser))
  }

  const signUp = async (email: string, password: string, name: string) => {
    // Simulate API call
    const mockUser: User = {
      id: '1',
      email,
      name,
      role: 'user'
    }
    setUser(mockUser)
    localStorage.setItem('user', JSON.stringify(mockUser))
  }

  const signOut = () => {
    setUser(null)
    localStorage.removeItem('user')
  }

  return (
    <AuthContext.Provider value={{ user, loading, signIn, signUp, signOut }}>
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
```

## Instructions for Lovable:

1. **Create all the layout components above** - These handle the main navigation and page structure
2. **Create ALL page components** listed in the routing configuration (see the imports in App.tsx)
3. **Each page should be a simple placeholder** with:
   - Proper TypeScript export
   - A heading with the page name
   - Basic responsive layout using Tailwind
   - Purple gradient theme for primary buttons
   - Dark mode support
4. **Page Template Example**:
```typescript
// src/pages/[category]/[PageName].tsx
export default function PageName() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Page Name</h1>
        <button className="bg-purple-gradient text-white px-4 py-2 rounded-md hover:opacity-90">
          Primary Action
        </button>
      </div>
      
      <div className="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
        <p className="text-gray-600 dark:text-gray-400">
          This is the Page Name page. Content will be implemented here.
        </p>
      </div>
    </div>
  )
}
```

5. **Create ALL these page files** (every single one from the imports):
   - Public pages: Landing, Pricing, Features, About, Blog, BlogPost, Contact, Privacy, Terms
   - Auth pages: Login, Register, ForgotPassword, ResetPassword
   - Onboarding pages: Welcome, Profile, ApiKeys, WordPress, Team, Complete
   - Dashboard pages: Dashboard, QuickStart
   - Pipeline pages: Pipeline, NewPipeline, PipelineDetails, PipelineLogs, PipelineHistory, PipelineTemplates
   - Article pages: Articles, NewArticle, ArticleDetail, EditArticle, ArticleSEO, ArticlePreview, DraftArticles, PublishedArticles, ScheduledArticles
   - Team pages: Team, TeamMembers, InviteTeam, TeamRoles, TeamActivity, TeamSettings
   - Billing pages: Billing, Subscription, UpgradePlan, Usage, Invoices, PaymentMethods, PaymentHistory
   - Settings pages: Settings, ProfileSettings, OrganizationSettings, ApiKeysSettings, WordPressSettings, NotificationSettings, SecuritySettings, IntegrationSettings, WebhookSettings, BrandingSettings
   - Analytics pages: Analytics, ContentAnalytics, SEOAnalytics, CostAnalytics, TeamAnalytics, ExportData
   - Monitoring pages: Monitoring, AgentMonitoring, ErrorTracking, ApiUsage, WebhookLogs
   - Admin pages: AdminDashboard, UserManagement, OrganizationManagement, BillingManagement, ContentModeration, SystemSettings, SystemLogs, PlatformMetrics, SupportTickets

**Success Criteria:**
- All routes work without 404 errors
- Every page has proper TypeScript
- Navigation sidebar works on all screen sizes
- Dark/light mode toggle works everywhere
- Purple gradient theme applied consistently
- All placeholder pages show correctly
- Mobile responsive design works
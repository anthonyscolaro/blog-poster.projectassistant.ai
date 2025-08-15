# Lovable Prompt: Project Setup & Configuration

## Business Context:
Setting up the Blog-Poster dashboard as a professional SEO content generation platform for ServiceDogUS. This React + Vite application will manage a 5-agent orchestration system that automates content creation while maintaining legal accuracy for service dog industry content.

## User Story:
"As a content manager, I want a modern, responsive dashboard that lets me monitor and control the entire content generation pipeline from competitor research to WordPress publishing."

## Technical Requirements:
- React 18+ with Vite 5+ build system
- TailwindCSS with custom purple gradient theme
- Dark/light mode toggle
- Responsive design (mobile-first)
- WebSocket support for real-time updates

## Prompt for Lovable:

🚨 CRITICAL REQUIREMENT: Use React + Vite ONLY
- This MUST be a React application with Vite build system (Lovable's default)
- Use standard React components and hooks
- Use React Router for navigation
- Ensure package.json includes "react": "^18.0.0" and "vite": "^5.0.0"

Create a React + Vite project setup for the Blog-Poster SEO content generation dashboard. This is a professional content automation platform that orchestrates 5 AI agents to generate legally-compliant, SEO-optimized articles for the service dog industry.

**Project Configuration:**

### Package.json Setup
```json
{
  "name": "blog-poster-dashboard",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0"
  },
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "react-router-dom": "^6.22.0",
    "@tanstack/react-query": "^5.17.0",
    "@supabase/supabase-js": "^2.39.0",
    "zustand": "^4.5.0",
    "recharts": "^2.10.0",
    "lucide-react": "^0.303.0",
    "clsx": "^2.1.0",
    "date-fns": "^3.3.0",
    "socket.io-client": "^4.6.0",
    "@stripe/stripe-js": "^2.4.0",
    "@stripe/react-stripe-js": "^2.4.0",
    "react-hot-toast": "^2.4.1",
    "framer-motion": "^10.18.0",
    "react-hook-form": "^7.48.2",
    "@hookform/resolvers": "^3.3.2",
    "zod": "^3.22.4",
    "react-markdown": "^9.0.1",
    "react-syntax-highlighter": "^15.5.0",
    "react-countup": "^6.5.0",
    "react-intersection-observer": "^9.5.3"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "@typescript-eslint/eslint-plugin": "^6.0.0",
    "@typescript-eslint/parser": "^6.0.0",
    "@vitejs/plugin-react": "^4.2.0",
    "autoprefixer": "^10.4.0",
    "eslint": "^8.56.0",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.0",
    "postcss": "^8.4.0",
    "tailwindcss": "^3.4.0",
    "typescript": "^5.3.0",
    "vite": "^5.0.0"
  }
}
```

### TailwindCSS Configuration with Custom Theme
```typescript
// tailwind.config.js
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f5f3ff',
          100: '#ede9fe',
          200: '#ddd6fe',
          300: '#c4b5fd',
          400: '#a78bfa',
          500: '#8b5cf6',
          600: '#7c3aed',
          700: '#6d28d9',
          800: '#5b21b6',
          900: '#4c1d95',
          950: '#2e1065',
        },
        dashboard: {
          bg: '#f8fafc',
          dark: '#0f172a',
          card: '#ffffff',
          'card-dark': '#1e293b',
        }
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'slide-in': 'slideIn 0.3s ease-out',
        'fade-in': 'fadeIn 0.5s ease-out',
      },
      keyframes: {
        slideIn: {
          '0%': { transform: 'translateX(-100%)' },
          '100%': { transform: 'translateX(0)' },
        },
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
      },
      backgroundImage: {
        'purple-gradient': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'success-gradient': 'linear-gradient(135deg, #667eea 0%, #48bb78 100%)',
      },
    },
  },
  plugins: [],
}
```

### Vite Configuration
```typescript
// vite.config.ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@components': path.resolve(__dirname, './src/components'),
      '@pages': path.resolve(__dirname, './src/pages'),
      '@services': path.resolve(__dirname, './src/services'),
      '@hooks': path.resolve(__dirname, './src/hooks'),
      '@types': path.resolve(__dirname, './src/types'),
      '@utils': path.resolve(__dirname, './src/utils'),
    },
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8088',
        changeOrigin: true,
      },
      '/ws': {
        target: 'ws://localhost:8088',
        ws: true,
      },
    },
  },
})
```

### TypeScript Configuration
```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"],
      "@components/*": ["./src/components/*"],
      "@pages/*": ["./src/pages/*"],
      "@services/*": ["./src/services/*"],
      "@hooks/*": ["./src/hooks/*"],
      "@types/*": ["./src/types/*"],
      "@utils/*": ["./src/utils/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

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

### Layout Component with Sidebar Navigation
```typescript
// src/components/Layout.tsx
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
  LogOut
} from 'lucide-react'
import { useTheme } from '@/contexts/ThemeContext'
import { useAuth } from '@/contexts/AuthContext'

const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
  { name: 'Pipeline', href: '/pipeline', icon: Workflow },
  { name: 'Articles', href: '/articles', icon: FileText },
  { name: 'Monitoring', href: '/monitoring', icon: Activity },
  { name: 'Settings', href: '/settings', icon: Settings },
]

export function Layout() {
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
                  {user?.email?.[0].toUpperCase()}
                </div>
                <div className="ml-3">
                  <p className="text-sm font-medium text-gray-700 dark:text-gray-300">
                    {user?.email}
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

### Theme Context Provider
```typescript
// src/contexts/ThemeContext.tsx
import { createContext, useContext, useEffect, useState } from 'react'

interface ThemeContextType {
  theme: 'light' | 'dark'
  toggleTheme: () => void
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined)

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<'light' | 'dark'>(() => {
    const saved = localStorage.getItem('theme')
    return (saved as 'light' | 'dark') || 'light'
  })

  useEffect(() => {
    localStorage.setItem('theme', theme)
    document.documentElement.classList.toggle('dark', theme === 'dark')
  }, [theme])

  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light')
  }

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  )
}

export function useTheme() {
  const context = useContext(ThemeContext)
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider')
  }
  return context
}
```

### Global Styles
```css
/* src/index.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
  }
}

@layer utilities {
  .animate-slide-in {
    animation: slideIn 0.3s ease-out;
  }

  .animate-fade-in {
    animation: fadeIn 0.5s ease-out;
  }

  .scrollbar-thin {
    scrollbar-width: thin;
    scrollbar-color: rgb(203 213 225) transparent;
  }

  .dark .scrollbar-thin {
    scrollbar-color: rgb(51 65 85) transparent;
  }
}

/* Custom scrollbar styles */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background-color: rgb(203 213 225);
  border-radius: 4px;
}

.dark ::-webkit-scrollbar-thumb {
  background-color: rgb(51 65 85);
}

/* Loading spinner */
.spinner {
  border: 2px solid rgba(139, 92, 246, 0.1);
  border-left-color: rgb(139, 92, 246);
  border-radius: 50%;
  width: 20px;
  height: 20px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
```

### Placeholder Page Components

Create all page components with proper TypeScript and responsive design:

```typescript
// src/pages/Login.tsx
import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { Mail, Lock, Eye, EyeOff } from 'lucide-react'
import { useAuth } from '@/contexts/AuthContext'

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const navigate = useNavigate()
  const { signIn } = useAuth()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    try {
      await signIn(email, password)
      navigate('/dashboard')
    } catch (error) {
      console.error('Login error:', error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <div className="mx-auto h-12 w-12 rounded-full bg-purple-gradient flex items-center justify-center">
            <span className="text-white font-bold text-xl">BP</span>
          </div>
          <h2 className="mt-6 text-center text-3xl font-bold text-gray-900 dark:text-white">
            Sign in to your account
          </h2>
        </div>
        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div className="space-y-4">
            <div>
              <label htmlFor="email" className="sr-only">Email address</label>
              <div className="relative">
                <Mail className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
                <input
                  id="email"
                  name="email"
                  type="email"
                  autoComplete="email"
                  required
                  className="pl-10 appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 dark:border-gray-700 placeholder-gray-500 dark:placeholder-gray-400 text-gray-900 dark:text-white bg-white dark:bg-gray-800 focus:outline-none focus:ring-primary-500 focus:border-primary-500 focus:z-10 sm:text-sm"
                  placeholder="Email address"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </div>
            </div>
            <div>
              <label htmlFor="password" className="sr-only">Password</label>
              <div className="relative">
                <Lock className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
                <input
                  id="password"
                  name="password"
                  type={showPassword ? 'text' : 'password'}
                  autoComplete="current-password"
                  required
                  className="pl-10 pr-10 appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 dark:border-gray-700 placeholder-gray-500 dark:placeholder-gray-400 text-gray-900 dark:text-white bg-white dark:bg-gray-800 focus:outline-none focus:ring-primary-500 focus:border-primary-500 focus:z-10 sm:text-sm"
                  placeholder="Password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
                <button
                  type="button"
                  className="absolute right-3 top-3 text-gray-400 hover:text-gray-600"
                  onClick={() => setShowPassword(!showPassword)}
                >
                  {showPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                </button>
              </div>
            </div>
          </div>

          <div>
            <button
              type="submit"
              disabled={isLoading}
              className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-purple-gradient hover:opacity-90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50"
            >
              {isLoading ? (
                <div className="spinner" />
              ) : (
                'Sign in'
              )}
            </button>
          </div>

          <div className="text-center">
            <Link
              to="/register"
              className="font-medium text-primary-600 hover:text-primary-500 dark:text-primary-400"
            >
              Don't have an account? Sign up
            </Link>
          </div>
        </form>
      </div>
    </div>
  )
}
```

```typescript
// src/pages/Register.tsx
import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { Mail, Lock, Eye, EyeOff, User } from 'lucide-react'
import { useAuth } from '@/contexts/AuthContext'

export default function Register() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: ''
  })
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const navigate = useNavigate()
  const { signUp } = useAuth()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (formData.password !== formData.confirmPassword) {
      alert('Passwords do not match')
      return
    }
    setIsLoading(true)
    try {
      await signUp(formData.email, formData.password, formData.name)
      navigate('/dashboard')
    } catch (error) {
      console.error('Registration error:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }))
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <div className="mx-auto h-12 w-12 rounded-full bg-purple-gradient flex items-center justify-center">
            <span className="text-white font-bold text-xl">BP</span>
          </div>
          <h2 className="mt-6 text-center text-3xl font-bold text-gray-900 dark:text-white">
            Create your account
          </h2>
        </div>
        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div className="space-y-4">
            <div>
              <label htmlFor="name" className="sr-only">Full name</label>
              <div className="relative">
                <User className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
                <input
                  id="name"
                  name="name"
                  type="text"
                  required
                  className="pl-10 appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 dark:border-gray-700 placeholder-gray-500 dark:placeholder-gray-400 text-gray-900 dark:text-white bg-white dark:bg-gray-800 focus:outline-none focus:ring-primary-500 focus:border-primary-500 focus:z-10 sm:text-sm"
                  placeholder="Full name"
                  value={formData.name}
                  onChange={handleInputChange}
                />
              </div>
            </div>
            <div>
              <label htmlFor="email" className="sr-only">Email address</label>
              <div className="relative">
                <Mail className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
                <input
                  id="email"
                  name="email"
                  type="email"
                  autoComplete="email"
                  required
                  className="pl-10 appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 dark:border-gray-700 placeholder-gray-500 dark:placeholder-gray-400 text-gray-900 dark:text-white bg-white dark:bg-gray-800 focus:outline-none focus:ring-primary-500 focus:border-primary-500 focus:z-10 sm:text-sm"
                  placeholder="Email address"
                  value={formData.email}
                  onChange={handleInputChange}
                />
              </div>
            </div>
            <div>
              <label htmlFor="password" className="sr-only">Password</label>
              <div className="relative">
                <Lock className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
                <input
                  id="password"
                  name="password"
                  type={showPassword ? 'text' : 'password'}
                  required
                  className="pl-10 pr-10 appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 dark:border-gray-700 placeholder-gray-500 dark:placeholder-gray-400 text-gray-900 dark:text-white bg-white dark:bg-gray-800 focus:outline-none focus:ring-primary-500 focus:border-primary-500 focus:z-10 sm:text-sm"
                  placeholder="Password"
                  value={formData.password}
                  onChange={handleInputChange}
                />
                <button
                  type="button"
                  className="absolute right-3 top-3 text-gray-400 hover:text-gray-600"
                  onClick={() => setShowPassword(!showPassword)}
                >
                  {showPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                </button>
              </div>
            </div>
            <div>
              <label htmlFor="confirmPassword" className="sr-only">Confirm password</label>
              <div className="relative">
                <Lock className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
                <input
                  id="confirmPassword"
                  name="confirmPassword"
                  type={showConfirmPassword ? 'text' : 'password'}
                  required
                  className="pl-10 pr-10 appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 dark:border-gray-700 placeholder-gray-500 dark:placeholder-gray-400 text-gray-900 dark:text-white bg-white dark:bg-gray-800 focus:outline-none focus:ring-primary-500 focus:border-primary-500 focus:z-10 sm:text-sm"
                  placeholder="Confirm password"
                  value={formData.confirmPassword}
                  onChange={handleInputChange}
                />
                <button
                  type="button"
                  className="absolute right-3 top-3 text-gray-400 hover:text-gray-600"
                  onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                >
                  {showConfirmPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                </button>
              </div>
            </div>
          </div>

          <div>
            <button
              type="submit"
              disabled={isLoading}
              className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-purple-gradient hover:opacity-90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50"
            >
              {isLoading ? (
                <div className="spinner" />
              ) : (
                'Sign up'
              )}
            </button>
          </div>

          <div className="text-center">
            <Link
              to="/login"
              className="font-medium text-primary-600 hover:text-primary-500 dark:text-primary-400"
            >
              Already have an account? Sign in
            </Link>
          </div>
        </form>
      </div>
    </div>
  )
}
```

```typescript
// src/pages/Dashboard.tsx
import { BarChart, TrendingUp, FileText, Clock, Activity } from 'lucide-react'

export default function Dashboard() {
  const stats = [
    { name: 'Articles Generated', value: '24', icon: FileText, change: '+12%' },
    { name: 'Success Rate', value: '96%', icon: TrendingUp, change: '+2.3%' },
    { name: 'Processing Time', value: '3.2m', icon: Clock, change: '-15%' },
    { name: 'Active Pipelines', value: '5', icon: Activity, change: '+1' },
  ]

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Dashboard</h1>
        <button className="bg-purple-gradient text-white px-4 py-2 rounded-md hover:opacity-90 transition-opacity">
          New Pipeline
        </button>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat) => (
          <div
            key={stat.name}
            className="bg-white dark:bg-gray-800 overflow-hidden shadow rounded-lg p-6"
          >
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <stat.icon className="h-6 w-6 text-primary-600" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 dark:text-gray-400 truncate">
                    {stat.name}
                  </dt>
                  <dd className="flex items-baseline">
                    <div className="text-2xl font-semibold text-gray-900 dark:text-white">
                      {stat.value}
                    </div>
                    <div className="ml-2 flex items-baseline text-sm font-semibold text-green-600">
                      {stat.change}
                    </div>
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Recent Activity */}
      <div className="bg-white dark:bg-gray-800 shadow rounded-lg">
        <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
          <h2 className="text-lg font-medium text-gray-900 dark:text-white">Recent Activity</h2>
        </div>
        <div className="p-6">
          <div className="space-y-4">
            {[1, 2, 3, 4, 5].map((item) => (
              <div key={item} className="flex items-center space-x-4">
                <div className="h-2 w-2 bg-primary-500 rounded-full"></div>
                <div className="flex-1">
                  <p className="text-sm text-gray-900 dark:text-white">
                    Pipeline completed: "Service Dog Training Methods"
                  </p>
                  <p className="text-xs text-gray-500 dark:text-gray-400">2 minutes ago</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
```

```typescript
// src/pages/Pipeline.tsx
import { Play, Pause, Square, Settings, Plus } from 'lucide-react'
import { Link } from 'react-router-dom'

export default function Pipeline() {
  const pipelines = [
    { id: 1, name: 'Service Dog Training', status: 'running', progress: 65 },
    { id: 2, name: 'ADA Compliance Guide', status: 'completed', progress: 100 },
    { id: 3, name: 'ESA vs Service Dog', status: 'paused', progress: 30 },
    { id: 4, name: 'Certification Process', status: 'pending', progress: 0 },
  ]

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'running': return 'text-green-600 bg-green-100'
      case 'completed': return 'text-blue-600 bg-blue-100'
      case 'paused': return 'text-yellow-600 bg-yellow-100'
      case 'pending': return 'text-gray-600 bg-gray-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Pipeline Management</h1>
        <button className="bg-purple-gradient text-white px-4 py-2 rounded-md hover:opacity-90 transition-opacity flex items-center space-x-2">
          <Plus className="h-4 w-4" />
          <span>New Pipeline</span>
        </button>
      </div>

      <div className="bg-white dark:bg-gray-800 shadow rounded-lg overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
          <h2 className="text-lg font-medium text-gray-900 dark:text-white">Active Pipelines</h2>
        </div>
        <div className="divide-y divide-gray-200 dark:divide-gray-700">
          {pipelines.map((pipeline) => (
            <div key={pipeline.id} className="p-6">
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-3">
                    <h3 className="text-lg font-medium text-gray-900 dark:text-white">
                      {pipeline.name}
                    </h3>
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(pipeline.status)}`}>
                      {pipeline.status}
                    </span>
                  </div>
                  <div className="mt-2">
                    <div className="flex items-center justify-between text-sm text-gray-600 dark:text-gray-400">
                      <span>Progress</span>
                      <span>{pipeline.progress}%</span>
                    </div>
                    <div className="mt-1 w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                      <div
                        className="bg-primary-600 h-2 rounded-full transition-all duration-300"
                        style={{ width: `${pipeline.progress}%` }}
                      ></div>
                    </div>
                  </div>
                </div>
                <div className="flex items-center space-x-2 ml-4">
                  <button className="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
                    <Play className="h-4 w-4" />
                  </button>
                  <button className="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
                    <Pause className="h-4 w-4" />
                  </button>
                  <button className="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
                    <Square className="h-4 w-4" />
                  </button>
                  <button className="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
                    <Settings className="h-4 w-4" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
```

```typescript
// src/pages/Articles.tsx
import { FileText, ExternalLink, Edit, Trash2, Calendar } from 'lucide-react'
import { Link } from 'react-router-dom'

export default function Articles() {
  const articles = [
    {
      id: 1,
      title: 'Complete Guide to Service Dog Training Methods',
      status: 'published',
      wordCount: 2150,
      publishedAt: '2024-01-15',
      views: 1240
    },
    {
      id: 2,
      title: 'ADA Compliance Requirements for Service Dogs',
      status: 'draft',
      wordCount: 1890,
      publishedAt: null,
      views: 0
    },
    {
      id: 3,
      title: 'Understanding ESA vs Service Dog Differences',
      status: 'published',
      wordCount: 1675,
      publishedAt: '2024-01-12',
      views: 890
    }
  ]

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'published': return 'text-green-600 bg-green-100'
      case 'draft': return 'text-yellow-600 bg-yellow-100'
      case 'pending': return 'text-blue-600 bg-blue-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Articles</h1>
        <button className="bg-purple-gradient text-white px-4 py-2 rounded-md hover:opacity-90 transition-opacity">
          Generate Article
        </button>
      </div>

      <div className="bg-white dark:bg-gray-800 shadow rounded-lg overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
          <h2 className="text-lg font-medium text-gray-900 dark:text-white">All Articles</h2>
        </div>
        <div className="divide-y divide-gray-200 dark:divide-gray-700">
          {articles.map((article) => (
            <div key={article.id} className="p-6">
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-3">
                    <FileText className="h-5 w-5 text-gray-400" />
                    <Link
                      to={`/articles/${article.id}`}
                      className="text-lg font-medium text-gray-900 dark:text-white hover:text-primary-600 dark:hover:text-primary-400"
                    >
                      {article.title}
                    </Link>
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(article.status)}`}>
                      {article.status}
                    </span>
                  </div>
                  <div className="mt-2 flex items-center space-x-6 text-sm text-gray-500 dark:text-gray-400">
                    <span>{article.wordCount} words</span>
                    {article.publishedAt && (
                      <span className="flex items-center space-x-1">
                        <Calendar className="h-4 w-4" />
                        <span>{article.publishedAt}</span>
                      </span>
                    )}
                    <span>{article.views} views</span>
                  </div>
                </div>
                <div className="flex items-center space-x-2 ml-4">
                  <Link
                    to={`/articles/${article.id}`}
                    className="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                  >
                    <ExternalLink className="h-4 w-4" />
                  </Link>
                  <button className="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
                    <Edit className="h-4 w-4" />
                  </button>
                  <button className="p-2 text-gray-400 hover:text-red-600 dark:hover:text-red-400">
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
```

```typescript
// src/pages/ArticleDetail.tsx
import { useParams, Link } from 'react-router-dom'
import { ArrowLeft, ExternalLink, Edit, Calendar, Eye, Clock } from 'lucide-react'

export default function ArticleDetail() {
  const { id } = useParams<{ id: string }>()
  
  // Mock article data - in real app, fetch from API
  const article = {
    id: parseInt(id || '1'),
    title: 'Complete Guide to Service Dog Training Methods',
    content: `# Complete Guide to Service Dog Training Methods

Service dogs are specially trained animals that perform specific tasks for individuals with disabilities. This comprehensive guide covers the essential training methods, legal requirements, and best practices for service dog preparation.

## Understanding Service Dog Requirements

Under the Americans with Disabilities Act (ADA), service dogs are defined as dogs that are individually trained to do work or perform tasks for people with disabilities. The work or task a dog has been trained to provide must be directly related to the person's disability.

## Training Methodologies

### 1. Positive Reinforcement Training
This method focuses on rewarding desired behaviors rather than punishing unwanted ones. It's the most effective and humane approach to service dog training.

### 2. Task-Specific Training
Each service dog must be trained for specific tasks related to their handler's disability:
- Guide dogs for the blind
- Hearing dogs for the deaf
- Mobility assistance dogs
- Medical alert dogs
- Psychiatric service dogs

## Legal Compliance and ADA Requirements

Service dogs are protected under federal law and have access rights that other animals do not possess. Key legal points include:

- Only dogs (and in some cases miniature horses) can be service animals
- No registration, certification, or special ID required
- Allowed in all public accommodations
- Cannot be charged pet fees
- Must be individually trained for disability-related tasks

## Training Timeline and Expectations

Service dog training typically takes 1-2 years and involves multiple phases:
1. Basic obedience (3-6 months)
2. Public access training (6-12 months)
3. Task-specific training (6-12 months)
4. Advanced proofing and refinement (ongoing)

## Conclusion

Proper service dog training requires patience, consistency, and expertise. Always work with qualified trainers and understand your legal rights and responsibilities as a handler.`,
    status: 'published',
    wordCount: 2150,
    publishedAt: '2024-01-15T10:30:00Z',
    views: 1240,
    readTime: 8,
    seoScore: 95,
    tags: ['Service Dogs', 'ADA Compliance', 'Training', 'Disability Rights']
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Link
            to="/articles"
            className="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
          >
            <ArrowLeft className="h-5 w-5" />
          </Link>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            {article.title}
          </h1>
        </div>
        <div className="flex items-center space-x-2">
          <button className="flex items-center space-x-2 px-4 py-2 text-sm text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 rounded-md hover:bg-gray-200 dark:hover:bg-gray-600">
            <Edit className="h-4 w-4" />
            <span>Edit</span>
          </button>
          <button className="flex items-center space-x-2 px-4 py-2 text-sm text-white bg-purple-gradient rounded-md hover:opacity-90">
            <ExternalLink className="h-4 w-4" />
            <span>Publish</span>
          </button>
        </div>
      </div>

      {/* Article Metadata */}
      <div className="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
          <div className="flex items-center space-x-3">
            <Eye className="h-5 w-5 text-gray-400" />
            <div>
              <p className="text-sm text-gray-500 dark:text-gray-400">Views</p>
              <p className="text-lg font-semibold text-gray-900 dark:text-white">{article.views}</p>
            </div>
          </div>
          <div className="flex items-center space-x-3">
            <Clock className="h-5 w-5 text-gray-400" />
            <div>
              <p className="text-sm text-gray-500 dark:text-gray-400">Read Time</p>
              <p className="text-lg font-semibold text-gray-900 dark:text-white">{article.readTime} min</p>
            </div>
          </div>
          <div className="flex items-center space-x-3">
            <Calendar className="h-5 w-5 text-gray-400" />
            <div>
              <p className="text-sm text-gray-500 dark:text-gray-400">Published</p>
              <p className="text-lg font-semibold text-gray-900 dark:text-white">
                {new Date(article.publishedAt).toLocaleDateString()}
              </p>
            </div>
          </div>
          <div className="flex items-center space-x-3">
            <div className="h-5 w-5 bg-green-500 rounded-full flex items-center justify-center">
              <span className="text-xs text-white font-bold">S</span>
            </div>
            <div>
              <p className="text-sm text-gray-500 dark:text-gray-400">SEO Score</p>
              <p className="text-lg font-semibold text-green-600">{article.seoScore}/100</p>
            </div>
          </div>
        </div>
      </div>

      {/* Article Content */}
      <div className="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
        <div className="prose dark:prose-invert max-w-none">
          <div dangerouslySetInnerHTML={{ __html: article.content.replace(/\n/g, '<br />') }} />
        </div>
      </div>

      {/* Tags */}
      <div className="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
        <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">Tags</h3>
        <div className="flex flex-wrap gap-2">
          {article.tags.map((tag) => (
            <span
              key={tag}
              className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-primary-100 text-primary-800 dark:bg-primary-900 dark:text-primary-200"
            >
              {tag}
            </span>
          ))}
        </div>
      </div>
    </div>
  )
}
```

```typescript
// src/pages/Monitoring.tsx
import { Activity, AlertTriangle, CheckCircle, XCircle, Clock } from 'lucide-react'

export default function Monitoring() {
  const systemStatus = [
    { name: 'Competitor Monitoring Agent', status: 'healthy', lastCheck: '2 minutes ago' },
    { name: 'Topic Analysis Agent', status: 'healthy', lastCheck: '3 minutes ago' },
    { name: 'Article Generation Agent', status: 'warning', lastCheck: '5 minutes ago' },
    { name: 'Legal Fact Checker Agent', status: 'healthy', lastCheck: '1 minute ago' },
    { name: 'WordPress Publishing Agent', status: 'error', lastCheck: '10 minutes ago' },
  ]

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'healthy': return <CheckCircle className="h-5 w-5 text-green-500" />
      case 'warning': return <AlertTriangle className="h-5 w-5 text-yellow-500" />
      case 'error': return <XCircle className="h-5 w-5 text-red-500" />
      default: return <Clock className="h-5 w-5 text-gray-500" />
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'healthy': return 'text-green-600 bg-green-100'
      case 'warning': return 'text-yellow-600 bg-yellow-100'
      case 'error': return 'text-red-600 bg-red-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">System Monitoring</h1>
        <button className="bg-purple-gradient text-white px-4 py-2 rounded-md hover:opacity-90 transition-opacity">
          Refresh Status
        </button>
      </div>

      {/* System Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white dark:bg-gray-800 overflow-hidden shadow rounded-lg p-6">
          <div className="flex items-center">
            <CheckCircle className="h-6 w-6 text-green-500" />
            <div className="ml-4">
              <h3 className="text-lg font-medium text-gray-900 dark:text-white">Healthy</h3>
              <p className="text-2xl font-semibold text-green-600">3</p>
            </div>
          </div>
        </div>
        <div className="bg-white dark:bg-gray-800 overflow-hidden shadow rounded-lg p-6">
          <div className="flex items-center">
            <AlertTriangle className="h-6 w-6 text-yellow-500" />
            <div className="ml-4">
              <h3 className="text-lg font-medium text-gray-900 dark:text-white">Warning</h3>
              <p className="text-2xl font-semibold text-yellow-600">1</p>
            </div>
          </div>
        </div>
        <div className="bg-white dark:bg-gray-800 overflow-hidden shadow rounded-lg p-6">
          <div className="flex items-center">
            <XCircle className="h-6 w-6 text-red-500" />
            <div className="ml-4">
              <h3 className="text-lg font-medium text-gray-900 dark:text-white">Error</h3>
              <p className="text-2xl font-semibold text-red-600">1</p>
            </div>
          </div>
        </div>
      </div>

      {/* Agent Status */}
      <div className="bg-white dark:bg-gray-800 shadow rounded-lg overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
          <h2 className="text-lg font-medium text-gray-900 dark:text-white">Agent Status</h2>
        </div>
        <div className="divide-y divide-gray-200 dark:divide-gray-700">
          {systemStatus.map((agent) => (
            <div key={agent.name} className="p-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  {getStatusIcon(agent.status)}
                  <div>
                    <h3 className="text-lg font-medium text-gray-900 dark:text-white">
                      {agent.name}
                    </h3>
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                      Last check: {agent.lastCheck}
                    </p>
                  </div>
                </div>
                <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(agent.status)}`}>
                  {agent.status}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Recent Logs */}
      <div className="bg-white dark:bg-gray-800 shadow rounded-lg">
        <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
          <h2 className="text-lg font-medium text-gray-900 dark:text-white">Recent Logs</h2>
        </div>
        <div className="p-6">
          <div className="space-y-3 font-mono text-sm">
            <div className="text-green-600">[INFO] Article generation completed successfully</div>
            <div className="text-yellow-600">[WARN] API rate limit approaching (80% used)</div>
            <div className="text-red-600">[ERROR] WordPress connection failed - timeout</div>
            <div className="text-gray-600 dark:text-gray-400">[INFO] Competitor monitoring scan initiated</div>
            <div className="text-green-600">[INFO] Legal fact checking passed</div>
          </div>
        </div>
      </div>
    </div>
  )
}
```

```typescript
// src/pages/Settings.tsx
import { Save, Key, Globe, Bell, Shield } from 'lucide-react'
import { useState } from 'react'

export default function Settings() {
  const [settings, setSettings] = useState({
    wordpress_url: 'https://wp.servicedogus.test',
    wp_username: 'admin',
    anthropic_api_key: '••••••••••••••••',
    jina_api_key: '••••••••••••••••',
    max_cost_per_article: '0.50',
    max_monthly_cost: '100.00',
    notifications_email: true,
    notifications_slack: false,
    auto_publish: false,
    seo_optimization: true,
  })

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target
    setSettings(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }))
  }

  const handleSave = () => {
    // Save settings logic here
    console.log('Saving settings:', settings)
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Settings</h1>
        <button
          onClick={handleSave}
          className="bg-purple-gradient text-white px-4 py-2 rounded-md hover:opacity-90 transition-opacity flex items-center space-x-2"
        >
          <Save className="h-4 w-4" />
          <span>Save Changes</span>
        </button>
      </div>

      {/* API Configuration */}
      <div className="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
        <div className="flex items-center space-x-2 mb-4">
          <Key className="h-5 w-5 text-gray-400" />
          <h2 className="text-lg font-medium text-gray-900 dark:text-white">API Configuration</h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Anthropic API Key
            </label>
            <input
              type="password"
              name="anthropic_api_key"
              value={settings.anthropic_api_key}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Jina AI API Key
            </label>
            <input
              type="password"
              name="jina_api_key"
              value={settings.jina_api_key}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
            />
          </div>
        </div>
      </div>

      {/* WordPress Configuration */}
      <div className="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
        <div className="flex items-center space-x-2 mb-4">
          <Globe className="h-5 w-5 text-gray-400" />
          <h2 className="text-lg font-medium text-gray-900 dark:text-white">WordPress Configuration</h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              WordPress URL
            </label>
            <input
              type="url"
              name="wordpress_url"
              value={settings.wordpress_url}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Username
            </label>
            <input
              type="text"
              name="wp_username"
              value={settings.wp_username}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
            />
          </div>
        </div>
      </div>

      {/* Cost Management */}
      <div className="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
        <div className="flex items-center space-x-2 mb-4">
          <Shield className="h-5 w-5 text-gray-400" />
          <h2 className="text-lg font-medium text-gray-900 dark:text-white">Cost Management</h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Max Cost Per Article ($)
            </label>
            <input
              type="number"
              step="0.01"
              name="max_cost_per_article"
              value={settings.max_cost_per_article}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Max Monthly Cost ($)
            </label>
            <input
              type="number"
              step="0.01"
              name="max_monthly_cost"
              value={settings.max_monthly_cost}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
            />
          </div>
        </div>
      </div>

      {/* Notifications */}
      <div className="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
        <div className="flex items-center space-x-2 mb-4">
          <Bell className="h-5 w-5 text-gray-400" />
          <h2 className="text-lg font-medium text-gray-900 dark:text-white">Notifications</h2>
        </div>
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-sm font-medium text-gray-900 dark:text-white">Email Notifications</h3>
              <p className="text-sm text-gray-500 dark:text-gray-400">Receive email alerts for pipeline events</p>
            </div>
            <input
              type="checkbox"
              name="notifications_email"
              checked={settings.notifications_email}
              onChange={handleInputChange}
              className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
            />
          </div>
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-sm font-medium text-gray-900 dark:text-white">Slack Notifications</h3>
              <p className="text-sm text-gray-500 dark:text-gray-400">Send alerts to Slack channel</p>
            </div>
            <input
              type="checkbox"
              name="notifications_slack"
              checked={settings.notifications_slack}
              onChange={handleInputChange}
              className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
            />
          </div>
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-sm font-medium text-gray-900 dark:text-white">Auto-Publish</h3>
              <p className="text-sm text-gray-500 dark:text-gray-400">Automatically publish approved articles</p>
            </div>
            <input
              type="checkbox"
              name="auto_publish"
              checked={settings.auto_publish}
              onChange={handleInputChange}
              className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
            />
          </div>
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-sm font-medium text-gray-900 dark:text-white">SEO Optimization</h3>
              <p className="text-sm text-gray-500 dark:text-gray-400">Enable advanced SEO features</p>
            </div>
            <input
              type="checkbox"
              name="seo_optimization"
              checked={settings.seo_optimization}
              onChange={handleInputChange}
              className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
            />
          </div>
        </div>
      </div>
    </div>
  )
}
```

**Success Criteria:**
- Project scaffolding complete with all dependencies
- All routes defined and working with no 404 errors
- Complete placeholder pages for all navigation items
- Dark/light mode toggle working
- Responsive sidebar navigation
- Purple gradient theme applied consistently
- TypeScript properly configured
- API proxy setup for backend integration
- Every button and link has a working destination

This setup creates a professional foundation for the Blog-Poster dashboard with complete routing and working placeholder pages for all features. All navigation will work from the start, ensuring no 404 errors and a complete user experience.
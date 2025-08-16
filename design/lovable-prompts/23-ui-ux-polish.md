# Lovable Prompt: UI/UX Polish Components

## Business Context
Add essential UI polish components including loading states, empty states, error handling, and mobile responsiveness to create a professional, production-ready experience for the Blog-Poster platform.

## User Story
"As a user, I want clear feedback for all interactions, helpful guidance when there's no data, and a smooth experience on any device size."

## Prompt for Lovable:

Create comprehensive UI polish components including loading states, empty states, error handling, and mobile navigation for the Blog-Poster platform. These components ensure a professional user experience with proper feedback for all interactions.

### 1. Design System & Tokens
```typescript
// src/styles/design-tokens.ts
export const colors = {
  // Primary - Purple Gradient (Keep as is - it's our signature)
  primary: {
    gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    50: '#f5f3ff',
    100: '#ede9fe',
    500: '#8b5cf6',
    600: '#7c3aed',
    700: '#6d28d9',
  },
  
  // Semantic Colors - Ensure consistency
  success: {
    light: '#10b981',
    DEFAULT: '#059669',
    dark: '#047857',
  },
  
  warning: {
    light: '#f59e0b',
    DEFAULT: '#d97706',
    dark: '#b45309',
  },
  
  error: {
    light: '#ef4444',
    DEFAULT: '#dc2626',
    dark: '#b91c1c',
  },
  
  // Neutrals - Clean grays
  gray: {
    50: '#f9fafb',
    100: '#f3f4f6',
    200: '#e5e7eb',
    300: '#d1d5db',
    400: '#9ca3af',
    500: '#6b7280',
    600: '#4b5563',
    700: '#374151',
    800: '#1f2937',
    900: '#111827',
  }
}

// Consistent spacing system
export const spacing = {
  xs: '0.5rem',   // 8px
  sm: '0.75rem',  // 12px
  md: '1rem',     // 16px
  lg: '1.5rem',   // 24px
  xl: '2rem',     // 32px
  '2xl': '3rem',  // 48px
  '3xl': '4rem',  // 64px
}

// Typography scale
export const typography = {
  xs: '0.75rem',    // 12px
  sm: '0.875rem',   // 14px
  base: '1rem',     // 16px
  lg: '1.125rem',   // 18px
  xl: '1.25rem',    // 20px
  '2xl': '1.5rem',  // 24px
  '3xl': '1.875rem', // 30px
  '4xl': '2.25rem',  // 36px
  '5xl': '3rem',     // 48px
}
```

### 2. Loading State Components
```typescript
// src/components/ui/LoadingStates.tsx
import { motion } from 'framer-motion'

// Skeleton Loader for Content
export function ContentSkeleton() {
  return (
    <div className="animate-pulse">
      <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-3/4 mb-4" />
      <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/2 mb-4" />
      <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-5/6" />
    </div>
  )
}

// Table Skeleton
export function TableSkeleton({ rows = 5 }) {
  return (
    <div className="space-y-3">
      {[...Array(rows)].map((_, i) => (
        <div key={i} className="flex gap-4 animate-pulse">
          <div className="h-10 bg-gray-200 dark:bg-gray-700 rounded flex-1" />
          <div className="h-10 bg-gray-200 dark:bg-gray-700 rounded w-32" />
          <div className="h-10 bg-gray-200 dark:bg-gray-700 rounded w-24" />
        </div>
      ))}
    </div>
  )
}

// Card Grid Skeleton
export function CardGridSkeleton({ cards = 4 }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {[...Array(cards)].map((_, i) => (
        <div key={i} className="bg-white dark:bg-gray-800 rounded-xl p-6 animate-pulse">
          <div className="h-8 w-8 bg-gray-200 dark:bg-gray-700 rounded mb-4" />
          <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/2 mb-2" />
          <div className="h-6 bg-gray-200 dark:bg-gray-700 rounded w-3/4" />
        </div>
      ))}
    </div>
  )
}
```

### 3. Empty State Components
```typescript
// src/components/ui/EmptyStates.tsx
import { motion } from 'framer-motion'
import { FileText, Workflow, Users, BarChart, Package, AlertCircle } from 'lucide-react'
import { useNavigate } from 'react-router-dom'

export function EmptyState({
  icon: Icon,
  title,
  description,
  action
}: {
  icon: React.ComponentType<{ className?: string }>
  title: string
  description: string
  action?: {
    label: string
    onClick: () => void
  }
}) {
  return (
    <motion.div 
      className="flex flex-col items-center justify-center py-12 px-4 text-center"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="w-20 h-20 bg-gray-100 dark:bg-gray-800 rounded-full flex items-center justify-center mb-6">
        <Icon className="w-10 h-10 text-gray-400" />
      </div>
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
        {title}
      </h3>
      <p className="text-gray-600 dark:text-gray-400 mb-6 max-w-sm">
        {description}
      </p>
      {action && (
        <motion.button
          onClick={action.onClick}
          className="px-6 py-2 bg-purple-gradient text-white rounded-lg font-medium"
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
        >
          {action.label}
        </motion.button>
      )}
    </motion.div>
  )
}

// Specific empty states for different sections
export const EmptyStates = {
  articles: {
    icon: FileText,
    title: "No articles yet",
    description: "Start generating your first SEO-optimized article with our 5-agent pipeline.",
    action: {
      label: "Generate First Article",
      onClick: () => navigate('/pipeline')
    }
  },
  
  pipelines: {
    icon: Workflow,
    title: "No active pipelines",
    description: "Configure and start a pipeline to begin generating content.",
    action: {
      label: "Start Pipeline",
      onClick: () => navigate('/pipeline')
    }
  },
  
  team: {
    icon: Users,
    title: "No team members",
    description: "Invite team members to collaborate on content generation.",
    action: {
      label: "Invite Team Member",
      onClick: () => openInviteModal()
    }
  }
}
```

### 4. Error State Components
```typescript
// src/components/ui/ErrorStates.tsx
import { AlertCircle } from 'lucide-react'
import { motion } from 'framer-motion'
export function ErrorState({
  error,
  retry
}: {
  error: Error | string
  retry?: () => void
}) {
  return (
    <div className="bg-red-50 dark:bg-red-900/20 rounded-lg p-6 text-center">
      <AlertCircle className="w-12 h-12 text-red-500 mx-auto mb-4" />
      <h3 className="text-lg font-semibold text-red-700 dark:text-red-300 mb-2">
        Something went wrong
      </h3>
      <p className="text-red-600 dark:text-red-400 mb-4">
        {typeof error === 'string' ? error : error.message}
      </p>
      {retry && (
        <button
          onClick={retry}
          className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
        >
          Try Again
        </button>
      )}
    </div>
  )
}
```

### 5. Mobile Navigation Component
```typescript
// Ensure all components follow this pattern
<div className="
  px-4 sm:px-6 lg:px-8           // Responsive padding
  grid-cols-1 sm:grid-cols-2 lg:grid-cols-4  // Responsive grid
  text-base sm:text-lg lg:text-xl // Responsive typography
  flex-col sm:flex-row            // Responsive flex direction
">
```

```typescript
// src/components/layout/MobileNav.tsx
import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Menu, X, Home, BarChart3, Workflow, FileText, Settings, Users, CreditCard } from 'lucide-react'
import { useNavigate, useLocation } from 'react-router-dom'
export function MobileNav() {
  const [isOpen, setIsOpen] = useState(false)
  const navigate = useNavigate()
  const location = useLocation()
  
  const navItems = [
    { path: '/dashboard', label: 'Dashboard', icon: Home },
    { path: '/pipeline', label: 'Pipeline', icon: Workflow },
    { path: '/articles', label: 'Articles', icon: FileText },
    { path: '/analytics', label: 'Analytics', icon: BarChart3 },
    { path: '/team', label: 'Team', icon: Users },
    { path: '/billing', label: 'Billing', icon: CreditCard },
    { path: '/settings', label: 'Settings', icon: Settings },
  ]
  
  return (
    <>
      {/* Mobile menu button - only visible on small screens */}
      <motion.button
        className="sm:hidden fixed bottom-4 right-4 z-50 p-4 bg-purple-gradient rounded-full shadow-lg"
        onClick={() => setIsOpen(!isOpen)}
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
      >
        <AnimatePresence mode="wait">
          {isOpen ? (
            <motion.div
              key="close"
              initial={{ rotate: -90, opacity: 0 }}
              animate={{ rotate: 0, opacity: 1 }}
              exit={{ rotate: 90, opacity: 0 }}
            >
              <X className="w-6 h-6 text-white" />
            </motion.div>
          ) : (
            <motion.div
              key="menu"
              initial={{ rotate: 90, opacity: 0 }}
              animate={{ rotate: 0, opacity: 1 }}
              exit={{ rotate: -90, opacity: 0 }}
            >
              <Menu className="w-6 h-6 text-white" />
            </motion.div>
          )}
        </AnimatePresence>
      </motion.button>
      
      {/* Overlay */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50 z-30 sm:hidden"
            onClick={() => setIsOpen(false)}
          />
        )}
      </AnimatePresence>
      
      {/* Slide-out menu */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ x: '100%' }}
            animate={{ x: 0 }}
            exit={{ x: '100%' }}
            transition={{ type: 'spring', damping: 25, stiffness: 200 }}
            className="fixed inset-y-0 right-0 w-72 bg-white dark:bg-gray-900 shadow-xl z-40 sm:hidden"
          >
            {/* Header */}
            <div className="p-6 border-b border-gray-200 dark:border-gray-700">
              <h2 className="text-xl font-bold text-gray-900 dark:text-white">Menu</h2>
            </div>
            
            {/* Navigation items */}
            <nav className="p-4">
              {navItems.map((item, index) => (
                <motion.button
                  key={item.path}
                  onClick={() => {
                    navigate(item.path)
                    setIsOpen(false)
                  }}
                  className={`
                    w-full flex items-center gap-3 px-4 py-3 rounded-lg mb-2
                    transition-colors
                    ${location.pathname === item.path
                      ? 'bg-purple-gradient text-white'
                      : 'hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-700 dark:text-gray-300'
                    }
                  `}
                  initial={{ x: 20, opacity: 0 }}
                  animate={{ x: 0, opacity: 1 }}
                  transition={{ delay: index * 0.05 }}
                >
                  <item.icon className="w-5 h-5" />
                  <span className="font-medium">{item.label}</span>
                </motion.button>
              ))}
            </nav>
            
            {/* User section */}
            <div className="absolute bottom-0 left-0 right-0 p-6 border-t border-gray-200 dark:border-gray-700">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-purple-gradient rounded-full" />
                <div>
                  <p className="font-medium text-gray-900 dark:text-white">John Doe</p>
                  <p className="text-sm text-gray-600 dark:text-gray-400">john@example.com</p>
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  )
}
```

### 6. Form Validation Components
```typescript
// Real-time validation with visual feedback
export function FormField({
  label,
  error,
  success,
  ...props
}) {
  return (
    <div>
      <label className="block text-sm font-medium mb-2">{label}</label>
      <div className="relative">
        <input
          className={`
            w-full px-4 py-2 rounded-lg border transition-colors
            ${error ? 'border-red-500 focus:ring-red-500' : ''}
            ${success ? 'border-green-500 focus:ring-green-500' : ''}
            ${!error && !success ? 'border-gray-300 focus:ring-purple-500' : ''}
          `}
          {...props}
        />
        {/* Validation icons */}
        {error && <XCircle className="absolute right-3 top-3 w-5 h-5 text-red-500" />}
        {success && <CheckCircle className="absolute right-3 top-3 w-5 h-5 text-green-500" />}
      </div>
      {/* Error message */}
      {error && (
        <motion.p
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-sm text-red-500 mt-1"
        >
          {error}
        </motion.p>
      )}
    </div>
  )
}
```

### 7. Confirmation Components
```typescript
// src/components/ui/ConfirmButton.tsx
import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
export function ConfirmButton({
  onConfirm,
  children,
  confirmText = "Are you sure?"
}) {
  const [confirming, setConfirming] = useState(false)
  
  if (confirming) {
    return (
      <div className="flex gap-2">
        <span className="text-sm py-2">{confirmText}</span>
        <button
          onClick={() => {
            onConfirm()
            setConfirming(false)
          }}
          className="px-3 py-1 bg-red-600 text-white rounded text-sm"
        >
          Yes
        </button>
        <button
          onClick={() => setConfirming(false)}
          className="px-3 py-1 bg-gray-300 text-gray-700 rounded text-sm"
        >
          Cancel
        </button>
      </div>
    )
  }
  
  return (
    <button
      onClick={() => setConfirming(true)}
      className="text-red-600 hover:text-red-700"
    >
      {children}
    </button>
  )
}
```

### 8. Page Wrapper with Loading States
```typescript
// Smooth page transitions with loading states
export function PageWrapper({ children }) {
  const [isLoading, setIsLoading] = useState(true)
  
  useEffect(() => {
    // Simulate data loading
    setTimeout(() => setIsLoading(false), 500)
  }, [])
  
  if (isLoading) {
    return <PageSkeleton />
  }
  
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.3 }}
    >
      {children}
    </motion.div>
  )
}
```

### 9. Data Visualization Components
```typescript
export function MetricChart({ data, isLoading }) {
  if (isLoading) {
    return (
      <div className="h-64 bg-gray-100 dark:bg-gray-800 rounded-lg animate-pulse" />
    )
  }
  
  if (!data || data.length === 0) {
    return (
      <EmptyState
        icon={BarChart}
        title="No data available"
        description="Data will appear here once you start generating articles"
      />
    )
  }
  
  return (
    <ResponsiveContainer width="100%" height={256}>
      {/* Chart implementation */}
    </ResponsiveContainer>
  )
}
```

### 10. Integration Examples

#### Using Loading States in Dashboard
```typescript
// In Dashboard component
import { CardGridSkeleton } from '@/components/ui/LoadingStates'
import { EmptyStates } from '@/components/ui/EmptyStates'

export default function Dashboard() {
  const { data, isLoading, error } = useQuery(/* ... */)
  
  if (isLoading) return <CardGridSkeleton cards={4} />
  if (error) return <ErrorState error={error} retry={refetch} />
  if (!data || data.length === 0) return <EmptyState {...EmptyStates.articles} />
  
  return <DashboardContent data={data} />
}
```

#### Using Empty States in Article Management
```typescript
// In ArticleManagement component
if (articles.length === 0) {
  return (
    <EmptyState
      icon={FileText}
      title="No articles yet"
      description="Start generating your first SEO-optimized article"
      action={{
        label: "Generate Article",
        onClick: () => navigate('/pipeline')
      }}
    />
  )
}
```

#### Using Form Validation
```typescript
// In Settings or Pipeline Configuration
<FormField
  label="API Key"
  type="password"
  value={apiKey}
  onChange={(e) => setApiKey(e.target.value)}
  error={errors.apiKey}
  success={apiKey && apiKey.length > 20}
/>
```

## Success Criteria

✅ **Loading States**: Skeleton loaders for all data types
✅ **Empty States**: Helpful messages with actionable CTAs
✅ **Error Handling**: User-friendly error messages with retry
✅ **Mobile Navigation**: Responsive hamburger menu
✅ **Form Validation**: Real-time feedback with visual indicators
✅ **Confirmation Dialogs**: Inline confirmation for destructive actions
✅ **Responsive Design**: Mobile-first with proper breakpoints
✅ **Accessibility**: Keyboard navigation and ARIA labels
✅ **Dark Mode Support**: All components work in light/dark themes
✅ **Consistent Design**: Unified colors, spacing, and typography

These polish components complete the Blog-Poster platform's UI/UX, ensuring a professional and delightful user experience across all devices and states.
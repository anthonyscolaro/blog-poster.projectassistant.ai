import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Menu, 
  X, 
  Home, 
  BarChart3, 
  Workflow, 
  FileText, 
  Settings, 
  Users, 
  CreditCard,
  LogOut,
  User
} from 'lucide-react'
import { useNavigate, useLocation } from 'react-router-dom'
import { useAuth } from '@/contexts/AuthContext'
import { Button } from '@/components/ui/button'

export function MobileNav() {
  const [isOpen, setIsOpen] = useState(false)
  const navigate = useNavigate()
  const location = useLocation()
  const { profile, signOut } = useAuth()
  
  const navItems = [
    { path: '/dashboard', label: 'Dashboard', icon: Home },
    { path: '/pipeline', label: 'Pipeline', icon: Workflow },
    { path: '/articles', label: 'Articles', icon: FileText },
    { path: '/analytics', label: 'Analytics', icon: BarChart3 },
    { path: '/team', label: 'Team', icon: Users },
    { path: '/billing', label: 'Billing', icon: CreditCard },
    { path: '/settings', label: 'Settings', icon: Settings },
  ]

  const handleNavigation = (path: string) => {
    navigate(path)
    setIsOpen(false)
  }

  const handleSignOut = async () => {
    try {
      await signOut()
      setIsOpen(false)
    } catch (error) {
      console.error('Error signing out:', error)
    }
  }
  
  return (
    <>
      {/* Mobile menu button - only visible on small screens */}
      <motion.button
        className="lg:hidden fixed bottom-6 right-6 z-50 p-4 bg-purple-gradient rounded-full shadow-lg border-2 border-white/10"
        onClick={() => setIsOpen(!isOpen)}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        style={{ willChange: 'transform' }}
      >
        <AnimatePresence mode="wait">
          {isOpen ? (
            <motion.div
              key="close"
              initial={{ rotate: -90, opacity: 0 }}
              animate={{ rotate: 0, opacity: 1 }}
              exit={{ rotate: 90, opacity: 0 }}
              transition={{ duration: 0.2 }}
            >
              <X className="w-6 h-6 text-white" />
            </motion.div>
          ) : (
            <motion.div
              key="menu"
              initial={{ rotate: 90, opacity: 0 }}
              animate={{ rotate: 0, opacity: 1 }}
              exit={{ rotate: -90, opacity: 0 }}
              transition={{ duration: 0.2 }}
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
            transition={{ duration: 0.2 }}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-30 lg:hidden"
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
            transition={{ 
              type: 'spring', 
              damping: 30, 
              stiffness: 300,
              duration: 0.3
            }}
            className="fixed inset-y-0 right-0 w-80 bg-card border-l border-border shadow-2xl z-40 lg:hidden"
          >
            {/* Header */}
            <div className="p-6 border-b border-border bg-gradient-to-r from-primary/5 to-accent/5">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 bg-purple-gradient rounded-full flex items-center justify-center">
                  <User className="w-6 h-6 text-white" />
                </div>
                <div className="flex-1 min-w-0">
                  <h2 className="font-semibold text-foreground truncate">
                    {profile?.full_name || 'User'}
                  </h2>
                  <p className="text-sm text-muted-foreground truncate">
                    {profile?.email}
                  </p>
                </div>
              </div>
            </div>
            
            {/* Navigation items */}
            <nav className="p-4 space-y-2 flex-1">
              {navItems.map((item, index) => {
                const isActive = location.pathname === item.path
                
                return (
                  <motion.button
                    key={item.path}
                    onClick={() => handleNavigation(item.path)}
                    className={`
                      w-full flex items-center gap-3 px-4 py-3 rounded-lg
                      transition-all duration-200 text-left
                      ${isActive
                        ? 'bg-purple-gradient text-white shadow-lg' 
                        : 'hover:bg-accent/50 text-foreground hover:text-accent-foreground'
                      }
                    `}
                    initial={{ x: 20, opacity: 0 }}
                    animate={{ x: 0, opacity: 1 }}
                    transition={{ delay: index * 0.05 }}
                    whileHover={{ x: 4 }}
                    whileTap={{ scale: 0.98 }}
                  >
                    <item.icon className={`w-5 h-5 ${isActive ? 'text-white' : 'text-muted-foreground'}`} />
                    <span className="font-medium">{item.label}</span>
                  </motion.button>
                )
              })}
            </nav>
            
            {/* Footer actions */}
            <div className="p-4 border-t border-border">
              <Button
                onClick={handleSignOut}
                variant="ghost"
                className="w-full justify-start gap-3 text-destructive hover:text-destructive hover:bg-destructive/10"
                leftIcon={<LogOut className="w-5 h-5" />}
              >
                Sign Out
              </Button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  )
}

// Mobile-first responsive navigation for header
export function MobileNavToggle() {
  return (
    <div className="lg:hidden">
      <MobileNav />
    </div>
  )
}

// Responsive navigation wrapper
export function ResponsiveNav({ children }: { children: React.ReactNode }) {
  return (
    <>
      {/* Desktop navigation */}
      <div className="hidden lg:block">
        {children}
      </div>
      
      {/* Mobile navigation */}
      <div className="lg:hidden">
        <MobileNav />
      </div>
    </>
  )
}
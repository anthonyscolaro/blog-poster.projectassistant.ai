import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { NavLink, useLocation } from 'react-router-dom'
import { 
  Home, 
  FileText, 
  Settings, 
  BarChart3, 
  Users, 
  Zap,
  ChevronDown,
  Bell,
  Search
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { navActiveIndicatorVariants, fadeInUpVariants } from '@/utils/animationVariants'

interface NavItem {
  id: string
  label: string
  icon: React.ComponentType<{ className?: string }>
  to: string
  badge?: number
  submenu?: NavItem[]
}

const navigationItems: NavItem[] = [
  {
    id: 'dashboard',
    label: 'Dashboard',
    icon: Home,
    to: '/dashboard'
  },
  {
    id: 'articles',
    label: 'Articles',
    icon: FileText,
    to: '/articles',
    badge: 3
  },
  {
    id: 'pipeline',
    label: 'Pipeline',
    icon: Zap,
    to: '/pipeline',
    submenu: [
      { id: 'pipeline-active', label: 'Active Pipelines', icon: Zap, to: '/pipeline/active' },
      { id: 'pipeline-templates', label: 'Templates', icon: FileText, to: '/pipeline/templates' },
      { id: 'pipeline-history', label: 'History', icon: BarChart3, to: '/pipeline/history' }
    ]
  },
  {
    id: 'analytics',
    label: 'Analytics',
    icon: BarChart3,
    to: '/analytics'
  },
  {
    id: 'team',
    label: 'Team',
    icon: Users,
    to: '/team'
  },
  {
    id: 'settings',
    label: 'Settings',
    icon: Settings,
    to: '/settings'
  }
]

export function AnimatedNavigation() {
  const location = useLocation()
  const [expandedMenus, setExpandedMenus] = useState<Set<string>>(new Set())
  const [searchQuery, setSearchQuery] = useState('')
  const [notifications] = useState(5)

  const isActiveRoute = (path: string) => {
    return location.pathname === path || location.pathname.startsWith(path + '/')
  }

  const toggleSubmenu = (itemId: string) => {
    setExpandedMenus(prev => {
      const newSet = new Set(prev)
      if (newSet.has(itemId)) {
        newSet.delete(itemId)
      } else {
        newSet.add(itemId)
      }
      return newSet
    })
  }

  const getNavItemClasses = (isActive: boolean) => {
    return `
      relative flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium
      transition-colors duration-200 group
      ${isActive 
        ? 'text-primary bg-primary/10' 
        : 'text-muted-foreground hover:text-foreground hover:bg-muted/50'
      }
    `
  }

  return (
    <nav className="flex flex-col h-full p-4 space-y-6">
      {/* Search Bar */}
      <motion.div 
        className="relative"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
      >
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-muted-foreground" />
        <Input
          type="text"
          placeholder="Search..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="pl-10 pr-4 py-2"
        />
      </motion.div>

      {/* Navigation Items */}
      <motion.div 
        className="flex-1 space-y-2"
        variants={fadeInUpVariants}
        initial="hidden"
        animate="visible"
      >
        {navigationItems.map((item, index) => (
          <motion.div
            key={item.id}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.1 * (index + 1) }}
          >
            {item.submenu ? (
              // Menu with Submenu
              <div>
                <motion.button
                  className={getNavItemClasses(isActiveRoute(item.to))}
                  onClick={() => toggleSubmenu(item.id)}
                  whileHover={{ x: 4 }}
                  whileTap={{ scale: 0.98 }}
                >
                  <item.icon className="w-5 h-5" />
                  <span className="flex-1 text-left">{item.label}</span>
                  {item.badge && (
                    <Badge variant="secondary" className="ml-auto">
                      {item.badge}
                    </Badge>
                  )}
                  <motion.div
                    animate={{ rotate: expandedMenus.has(item.id) ? 180 : 0 }}
                    transition={{ duration: 0.2 }}
                  >
                    <ChevronDown className="w-4 h-4" />
                  </motion.div>
                  
                  {/* Active Indicator */}
                  {isActiveRoute(item.to) && (
                    <motion.div
                      layoutId="activeIndicator"
                      className="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-8 bg-primary rounded-r-full"
                      initial={false}
                      transition={{
                        type: "spring",
                        stiffness: 350,
                        damping: 30
                      }}
                    />
                  )}
                </motion.button>
                
                {/* Submenu */}
                <AnimatePresence>
                  {expandedMenus.has(item.id) && (
                    <motion.div
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: 'auto', opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      transition={{ duration: 0.2 }}
                      className="overflow-hidden ml-4 mt-2 space-y-1"
                    >
                      {item.submenu.map((subItem) => (
                        <motion.div
                          key={subItem.id}
                          initial={{ opacity: 0, x: -10 }}
                          animate={{ opacity: 1, x: 0 }}
                          exit={{ opacity: 0, x: -10 }}
                          transition={{ duration: 0.15 }}
                        >
                          <NavLink
                            to={subItem.to}
                            className={({ isActive }) => getNavItemClasses(isActive)}
                          >
                            <subItem.icon className="w-4 h-4" />
                            <span>{subItem.label}</span>
                            
                            {/* Active Indicator for Submenu */}
                            {isActiveRoute(subItem.to) && (
                              <motion.div
                                layoutId="activeSubIndicator"
                                className="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-6 bg-primary rounded-r-full"
                                initial={false}
                                transition={{
                                  type: "spring",
                                  stiffness: 350,
                                  damping: 30
                                }}
                              />
                            )}
                          </NavLink>
                        </motion.div>
                      ))}
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            ) : (
              // Regular Menu Item
              <NavLink
                to={item.to}
                className={({ isActive }) => getNavItemClasses(isActive)}
              >
                {({ isActive }) => (
                  <motion.div
                    className="flex items-center gap-3 w-full"
                    whileHover={{ x: 4 }}
                    whileTap={{ scale: 0.98 }}
                  >
                    <item.icon className="w-5 h-5" />
                    <span className="flex-1">{item.label}</span>
                    {item.badge && (
                      <Badge variant="secondary">
                        {item.badge}
                      </Badge>
                    )}
                    
                    {/* Active Indicator */}
                    {isActive && (
                      <motion.div
                        layoutId="activeIndicator"
                        className="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-8 bg-primary rounded-r-full"
                        initial={false}
                        transition={{
                          type: "spring",
                          stiffness: 350,
                          damping: 30
                        }}
                      />
                    )}
                  </motion.div>
                )}
              </NavLink>
            )}
          </motion.div>
        ))}
      </motion.div>

      {/* Bottom Actions */}
      <motion.div 
        className="space-y-3 pt-4 border-t"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.8 }}
      >
        <Button
          variant="outline"
          size="sm"
          className="w-full justify-start gap-3"
        >
          <Bell className="w-4 h-4" />
          <span className="flex-1 text-left">Notifications</span>
          {notifications > 0 && (
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              className="w-5 h-5 bg-red-500 text-white text-xs rounded-full flex items-center justify-center"
            >
              {notifications}
            </motion.div>
          )}
        </Button>
      </motion.div>
    </nav>
  )
}

// Horizontal Tab Navigation Component
export function HorizontalTabNavigation() {
  const [activeTab, setActiveTab] = useState('dashboard')
  
  const tabs = [
    { id: 'dashboard', label: 'Dashboard' },
    { id: 'articles', label: 'Articles' },
    { id: 'pipeline', label: 'Pipeline' },
    { id: 'analytics', label: 'Analytics' },
    { id: 'settings', label: 'Settings' }
  ]

  return (
    <nav className="flex space-x-1 p-1 bg-muted rounded-lg">
      {tabs.map((tab) => (
        <motion.button
          key={tab.id}
          onClick={() => setActiveTab(tab.id)}
          className="relative px-4 py-2 text-sm font-medium rounded-md transition-colors"
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
        >
          {activeTab === tab.id && (
            <motion.div
              layoutId="activeTabBackground"
              className="absolute inset-0 bg-background shadow-sm rounded-md"
              transition={{
                type: "spring",
                stiffness: 350,
                damping: 30
              }}
            />
          )}
          <span className={`relative z-10 ${
            activeTab === tab.id ? 'text-foreground' : 'text-muted-foreground'
          }`}>
            {tab.label}
          </span>
        </motion.button>
      ))}
    </nav>
  )
}
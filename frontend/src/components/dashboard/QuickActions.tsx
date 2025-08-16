import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Play, FileText, Settings, TrendingUp } from 'lucide-react'

export function QuickActions() {
  const navigate = useNavigate()

  const actions = [
    {
      label: 'Start Pipeline',
      icon: Play,
      color: 'bg-gradient-to-r from-purple-600 to-purple-700',
      onClick: () => navigate('/pipeline'),
    },
    {
      label: 'New Article',
      icon: FileText,
      color: 'bg-blue-500',
      onClick: () => navigate('/articles/new'),
    },
    {
      label: 'View Analytics',
      icon: TrendingUp,
      color: 'bg-green-500',
      onClick: () => navigate('/monitoring'),
    },
    {
      label: 'Settings',
      icon: Settings,
      color: 'bg-gray-500',
      onClick: () => navigate('/settings'),
    },
  ]

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
      {actions.map((action, index) => (
        <motion.button
          key={index}
          onClick={action.onClick}
          className="group relative overflow-hidden rounded-xl p-6 text-white transition-transform"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.1 }}
        >
          <div className={`absolute inset-0 ${action.color} opacity-90`} />
          <div className="relative z-10">
            <action.icon className="h-8 w-8 mb-3" />
            <p className="font-medium">{action.label}</p>
          </div>
        </motion.button>
      ))}
    </div>
  )
}
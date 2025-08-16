# Lovable Prompt: Shared Components & UI Library

## Business Context:
The shared components library provides reusable, consistent UI elements across the Blog-Poster platform. These components ensure design consistency, improve development efficiency, and provide a cohesive user experience throughout the application while maintaining the purple gradient theme and dark mode support.

## User Story:
"As a user, I want a consistent, intuitive interface across all parts of the Blog-Poster platform with smooth interactions, clear feedback, and accessible design patterns that work seamlessly in both light and dark modes."

## Component Requirements:
- **React 19 Features**: Leverage Server Components, use() hook, and Actions for form handling
- **Design Consistency**: Purple gradient theme with consistent spacing and typography
- **Accessibility**: WCAG 2.1 AA compliant with proper ARIA labels and keyboard navigation
- **Responsive Design**: Mobile-first approach with breakpoint-aware layouts
- **Loading States**: Skeleton loaders and loading indicators for all async operations
- **Error Handling**: Error boundaries and user-friendly error messages
- **Dark Mode**: Full dark mode support with smooth transitions
- **Performance**: Optimized with React 19's concurrent features and Suspense

## Prompt for Lovable:

Create a comprehensive shared component library for the Blog-Poster platform that provides reusable, accessible, and consistent UI elements with proper TypeScript types, loading states, error handling, and theme support. Utilize React 19 features like Actions for form handling, Suspense for async components, and the use() hook where applicable.

**Shared Components:**

### Animated Button Component System
```typescript
// src/components/ui/Button.tsx
import React from 'react'
import { motion } from 'framer-motion'
import { Loader2 } from 'lucide-react'
import { cn } from '@/utils/cn'

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger' | 'success'
  size?: 'sm' | 'md' | 'lg' | 'xl'
  loading?: boolean
  loadingText?: string
  leftIcon?: React.ReactNode
  rightIcon?: React.ReactNode
  fullWidth?: boolean
  animation?: boolean // Enable/disable animations
}

const buttonVariants = {
  primary: 'bg-purple-gradient text-white hover:opacity-90 focus:ring-purple-500',
  secondary: 'bg-gray-600 text-white hover:bg-gray-700 focus:ring-gray-500',
  outline: 'border-2 border-purple-600 text-purple-600 hover:bg-purple-50 dark:hover:bg-purple-900/20 focus:ring-purple-500',
  ghost: 'text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 focus:ring-gray-500',
  danger: 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500',
  success: 'bg-green-600 text-white hover:bg-green-700 focus:ring-green-500',
}

const buttonSizes = {
  sm: 'px-3 py-1.5 text-sm',
  md: 'px-4 py-2 text-sm',
  lg: 'px-6 py-3 text-base',
  xl: 'px-8 py-4 text-lg',
}

export function Button({
  variant = 'primary',
  size = 'md',
  loading = false,
  loadingText,
  leftIcon,
  rightIcon,
  fullWidth = false,
  animation = true,
  className,
  children,
  disabled,
  ...props
}: ButtonProps) {
  const isDisabled = disabled || loading

  const buttonAnimations = animation ? {
    initial: { scale: 1 },
    whileHover: { scale: 1.02 },
    whileTap: { scale: 0.98 },
    transition: { 
      type: "spring", 
      stiffness: 300, 
      damping: 20 
    }
  } : {}

  const ButtonComponent = animation ? motion.button : 'button'

  return (
    <ButtonComponent
      {...buttonAnimations}
      className={cn(
        'relative inline-flex items-center justify-center font-medium rounded-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed',
        buttonVariants[variant],
        buttonSizes[size],
        fullWidth && 'w-full',
        className
      )}
      disabled={isDisabled}
      {...props}
    >
      {loading ? (
        <motion.div
          className="flex items-center"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.3 }}
        >
          <Loader2 className="h-4 w-4 mr-2 animate-spin" />
          {loadingText || 'Loading...'}
        </motion.div>
      ) : (
        <>
          {leftIcon && (
            <motion.span 
              className="mr-2"
              initial={{ x: -5, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              transition={{ duration: 0.2 }}
            >
              {leftIcon}
            </motion.span>
          )}
          {children}
          {rightIcon && (
            <motion.span 
              className="ml-2"
              initial={{ x: 5, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              transition={{ duration: 0.2 }}
            >
              {rightIcon}
            </motion.span>
          )}
        </>
      )}
    </ButtonComponent>
  )
}

// Button group for related actions
export function ButtonGroup({ children, className }: { children: React.ReactNode; className?: string }) {
  return (
    <div className={cn('inline-flex rounded-lg shadow-sm', className)}>
      {React.Children.map(children, (child, index) => {
        if (React.isValidElement(child)) {
          return React.cloneElement(child, {
            className: cn(
              child.props.className,
              index === 0 && 'rounded-r-none border-r-0',
              index === React.Children.count(children) - 1 && 'rounded-l-none',
              index > 0 && index < React.Children.count(children) - 1 && 'rounded-none border-x-0'
            ),
          })
        }
        return child
      })}
    </div>
  )
}
```

### Input Components
```typescript
// src/components/ui/Input.tsx
import React, { forwardRef } from 'react'
import { cn } from '@/utils/cn'

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string
  error?: string
  hint?: string
  leftIcon?: React.ReactNode
  rightIcon?: React.ReactNode
  fullWidth?: boolean
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, hint, leftIcon, rightIcon, fullWidth = true, className, ...props }, ref) => {
    const inputId = props.id || `input-${Math.random().toString(36).substr(2, 9)}`

    return (
      <div className={cn('space-y-2', fullWidth && 'w-full')}>
        {label && (
          <label 
            htmlFor={inputId}
            className="block text-sm font-medium text-gray-700 dark:text-gray-300"
          >
            {label}
            {props.required && <span className="text-red-500 ml-1">*</span>}
          </label>
        )}
        
        <div className="relative">
          {leftIcon && (
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              {leftIcon}
            </div>
          )}
          
          <input
            ref={ref}
            id={inputId}
            className={cn(
              'block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm',
              'focus:ring-2 focus:ring-purple-500 focus:border-transparent',
              'placeholder-gray-400 dark:placeholder-gray-500',
              'bg-white dark:bg-gray-700 text-gray-900 dark:text-white',
              'disabled:bg-gray-50 dark:disabled:bg-gray-800 disabled:cursor-not-allowed',
              error && 'border-red-300 dark:border-red-600 focus:ring-red-500',
              leftIcon && 'pl-10',
              rightIcon && 'pr-10',
              className
            )}
            {...props}
          />
          
          {rightIcon && (
            <div className="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
              {rightIcon}
            </div>
          )}
        </div>

        {error && (
          <p className="text-sm text-red-600 dark:text-red-400" role="alert">
            {error}
          </p>
        )}
        
        {hint && !error && (
          <p className="text-sm text-gray-600 dark:text-gray-400">
            {hint}
          </p>
        )}
      </div>
    )
  }
)

Input.displayName = 'Input'

// Textarea variant
interface TextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string
  error?: string
  hint?: string
  fullWidth?: boolean
}

export const Textarea = forwardRef<HTMLTextAreaElement, TextareaProps>(
  ({ label, error, hint, fullWidth = true, className, ...props }, ref) => {
    const textareaId = props.id || `textarea-${Math.random().toString(36).substr(2, 9)}`

    return (
      <div className={cn('space-y-2', fullWidth && 'w-full')}>
        {label && (
          <label 
            htmlFor={textareaId}
            className="block text-sm font-medium text-gray-700 dark:text-gray-300"
          >
            {label}
            {props.required && <span className="text-red-500 ml-1">*</span>}
          </label>
        )}
        
        <textarea
          ref={ref}
          id={textareaId}
          className={cn(
            'block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm',
            'focus:ring-2 focus:ring-purple-500 focus:border-transparent',
            'placeholder-gray-400 dark:placeholder-gray-500',
            'bg-white dark:bg-gray-700 text-gray-900 dark:text-white',
            'disabled:bg-gray-50 dark:disabled:bg-gray-800 disabled:cursor-not-allowed',
            'resize-vertical min-h-[100px]',
            error && 'border-red-300 dark:border-red-600 focus:ring-red-500',
            className
          )}
          {...props}
        />

        {error && (
          <p className="text-sm text-red-600 dark:text-red-400" role="alert">
            {error}
          </p>
        )}
        
        {hint && !error && (
          <p className="text-sm text-gray-600 dark:text-gray-400">
            {hint}
          </p>
        )}
      </div>
    )
  }
)

Textarea.displayName = 'Textarea'
```

### Card Components
```typescript
// src/components/ui/Card.tsx
import React from 'react'
import { cn } from '@/utils/cn'

interface CardProps {
  children: React.ReactNode
  className?: string
  padding?: 'none' | 'sm' | 'md' | 'lg'
  shadow?: 'none' | 'sm' | 'md' | 'lg'
  border?: boolean
  hover?: boolean
}

const paddingVariants = {
  none: '',
  sm: 'p-4',
  md: 'p-6',
  lg: 'p-8',
}

const shadowVariants = {
  none: '',
  sm: 'shadow-sm',
  md: 'shadow-md',
  lg: 'shadow-lg',
}

export function Card({ 
  children, 
  className, 
  padding = 'md',
  shadow = 'sm',
  border = true,
  hover = false 
}: CardProps) {
  return (
    <div
      className={cn(
        'bg-white dark:bg-gray-800 rounded-xl',
        border && 'border border-gray-200 dark:border-gray-700',
        paddingVariants[padding],
        shadowVariants[shadow],
        hover && 'transition-all duration-200 hover:shadow-lg dark:hover:shadow-gray-900/25',
        className
      )}
    >
      {children}
    </div>
  )
}

export function CardHeader({ children, className }: { children: React.ReactNode; className?: string }) {
  return (
    <div className={cn('mb-4 pb-4 border-b border-gray-200 dark:border-gray-700', className)}>
      {children}
    </div>
  )
}

export function CardTitle({ children, className }: { children: React.ReactNode; className?: string }) {
  return (
    <h3 className={cn('text-lg font-semibold text-gray-900 dark:text-white', className)}>
      {children}
    </h3>
  )
}

export function CardDescription({ children, className }: { children: React.ReactNode; className?: string }) {
  return (
    <p className={cn('text-gray-600 dark:text-gray-400 mt-1', className)}>
      {children}
    </p>
  )
}

export function CardContent({ children, className }: { children: React.ReactNode; className?: string }) {
  return (
    <div className={cn('space-y-4', className)}>
      {children}
    </div>
  )
}

export function CardFooter({ children, className }: { children: React.ReactNode; className?: string }) {
  return (
    <div className={cn('mt-6 pt-4 border-t border-gray-200 dark:border-gray-700', className)}>
      {children}
    </div>
  )
}
```

### Modal Components
```typescript
// src/components/ui/Modal.tsx
import React, { useEffect } from 'react'
import { createPortal } from 'react-dom'
import { X } from 'lucide-react'
import { cn } from '@/utils/cn'

interface ModalProps {
  isOpen: boolean
  onClose: () => void
  title?: string
  children: React.ReactNode
  size?: 'sm' | 'md' | 'lg' | 'xl' | 'full'
  closeOnOverlayClick?: boolean
  closeOnEscape?: boolean
  className?: string
}

const sizeVariants = {
  sm: 'max-w-md',
  md: 'max-w-lg',
  lg: 'max-w-2xl',
  xl: 'max-w-4xl',
  full: 'max-w-full mx-4',
}

export function Modal({
  isOpen,
  onClose,
  title,
  children,
  size = 'md',
  closeOnOverlayClick = true,
  closeOnEscape = true,
  className,
}: ModalProps) {
  useEffect(() => {
    if (!closeOnEscape) return

    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose()
      }
    }

    if (isOpen) {
      document.addEventListener('keydown', handleEscape)
      document.body.style.overflow = 'hidden'
    }

    return () => {
      document.removeEventListener('keydown', handleEscape)
      document.body.style.overflow = 'unset'
    }
  }, [isOpen, onClose, closeOnEscape])

  if (!isOpen) return null

  return createPortal(
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* Overlay */}
      <div
        className="absolute inset-0 bg-black/50 backdrop-blur-sm"
        onClick={closeOnOverlayClick ? onClose : undefined}
      />
      
      {/* Modal */}
      <div
        className={cn(
          'relative bg-white dark:bg-gray-800 rounded-xl shadow-xl',
          'max-h-[90vh] overflow-hidden',
          'animate-fade-in',
          sizeVariants[size],
          className
        )}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        {(title || onClose) && (
          <div className="flex items-center justify-between p-6 border-b border-gray-200 dark:border-gray-700">
            {title && (
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
                {title}
              </h2>
            )}
            <button
              onClick={onClose}
              className="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
            >
              <X className="h-5 w-5" />
            </button>
          </div>
        )}
        
        {/* Content */}
        <div className="p-6 overflow-y-auto max-h-[calc(90vh-120px)]">
          {children}
        </div>
      </div>
    </div>,
    document.body
  )
}

export function ConfirmModal({
  isOpen,
  onClose,
  onConfirm,
  title = 'Confirm Action',
  message,
  confirmText = 'Confirm',
  cancelText = 'Cancel',
  variant = 'danger',
}: {
  isOpen: boolean
  onClose: () => void
  onConfirm: () => void
  title?: string
  message: string
  confirmText?: string
  cancelText?: string
  variant?: 'danger' | 'warning' | 'info'
}) {
  return (
    <Modal isOpen={isOpen} onClose={onClose} title={title} size="sm">
      <div className="space-y-4">
        <p className="text-gray-600 dark:text-gray-400">
          {message}
        </p>
        
        <div className="flex items-center gap-3 justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg"
          >
            {cancelText}
          </button>
          <button
            onClick={() => {
              onConfirm()
              onClose()
            }}
            className={cn(
              'px-4 py-2 text-white rounded-lg font-medium',
              variant === 'danger' && 'bg-red-600 hover:bg-red-700',
              variant === 'warning' && 'bg-yellow-600 hover:bg-yellow-700',
              variant === 'info' && 'bg-blue-600 hover:bg-blue-700'
            )}
          >
            {confirmText}
          </button>
        </div>
      </div>
    </Modal>
  )
}
```

### Toast Notification System
```typescript
// src/components/ui/Toast.tsx
import React, { createContext, useContext, useState, useCallback } from 'react'
import { createPortal } from 'react-dom'
import { CheckCircle, AlertTriangle, XCircle, Info, X } from 'lucide-react'
import { cn } from '@/utils/cn'

interface Toast {
  id: string
  type: 'success' | 'error' | 'warning' | 'info'
  title: string
  message?: string
  duration?: number
  action?: {
    label: string
    onClick: () => void
  }
}

interface ToastContextType {
  toasts: Toast[]
  addToast: (toast: Omit<Toast, 'id'>) => void
  removeToast: (id: string) => void
  success: (title: string, message?: string) => void
  error: (title: string, message?: string) => void
  warning: (title: string, message?: string) => void
  info: (title: string, message?: string) => void
}

const ToastContext = createContext<ToastContextType | undefined>(undefined)

export function ToastProvider({ children }: { children: React.ReactNode }) {
  const [toasts, setToasts] = useState<Toast[]>([])

  const addToast = useCallback((toast: Omit<Toast, 'id'>) => {
    const id = Math.random().toString(36).substr(2, 9)
    const newToast = { ...toast, id }
    
    setToasts(prev => [...prev, newToast])

    // Auto remove after duration
    setTimeout(() => {
      removeToast(id)
    }, toast.duration || 5000)
  }, [])

  const removeToast = useCallback((id: string) => {
    setToasts(prev => prev.filter(toast => toast.id !== id))
  }, [])

  const success = useCallback((title: string, message?: string) => {
    addToast({ type: 'success', title, message })
  }, [addToast])

  const error = useCallback((title: string, message?: string) => {
    addToast({ type: 'error', title, message })
  }, [addToast])

  const warning = useCallback((title: string, message?: string) => {
    addToast({ type: 'warning', title, message })
  }, [addToast])

  const info = useCallback((title: string, message?: string) => {
    addToast({ type: 'info', title, message })
  }, [addToast])

  return (
    <ToastContext.Provider value={{
      toasts,
      addToast,
      removeToast,
      success,
      error,
      warning,
      info,
    }}>
      {children}
      <ToastContainer toasts={toasts} removeToast={removeToast} />
    </ToastContext.Provider>
  )
}

export function useToast() {
  const context = useContext(ToastContext)
  if (!context) {
    throw new Error('useToast must be used within ToastProvider')
  }
  return context
}

function ToastContainer({ toasts, removeToast }: { toasts: Toast[]; removeToast: (id: string) => void }) {
  return createPortal(
    <div className="fixed top-4 right-4 z-50 space-y-2">
      {toasts.map((toast) => (
        <ToastItem key={toast.id} toast={toast} onRemove={removeToast} />
      ))}
    </div>,
    document.body
  )
}

function ToastItem({ toast, onRemove }: { toast: Toast; onRemove: (id: string) => void }) {
  const icons = {
    success: CheckCircle,
    error: XCircle,
    warning: AlertTriangle,
    info: Info,
  }

  const colors = {
    success: 'bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-800 text-green-800 dark:text-green-200',
    error: 'bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800 text-red-800 dark:text-red-200',
    warning: 'bg-yellow-50 dark:bg-yellow-900/20 border-yellow-200 dark:border-yellow-800 text-yellow-800 dark:text-yellow-200',
    info: 'bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-800 text-blue-800 dark:text-blue-200',
  }

  const iconColors = {
    success: 'text-green-500',
    error: 'text-red-500',
    warning: 'text-yellow-500',
    info: 'text-blue-500',
  }

  const Icon = icons[toast.type]

  return (
    <div
      className={cn(
        'flex items-start gap-3 p-4 rounded-lg border shadow-lg min-w-[320px] max-w-md',
        'animate-slide-in',
        colors[toast.type]
      )}
    >
      <Icon className={cn('h-5 w-5 mt-0.5 flex-shrink-0', iconColors[toast.type])} />
      
      <div className="flex-1 min-w-0">
        <h4 className="font-medium">{toast.title}</h4>
        {toast.message && (
          <p className="text-sm opacity-90 mt-1">{toast.message}</p>
        )}
        {toast.action && (
          <button
            onClick={toast.action.onClick}
            className="text-sm font-medium underline mt-2 hover:no-underline"
          >
            {toast.action.label}
          </button>
        )}
      </div>
      
      <button
        onClick={() => onRemove(toast.id)}
        className="p-1 hover:bg-black/5 dark:hover:bg-white/5 rounded"
      >
        <X className="h-4 w-4" />
      </button>
    </div>
  )
}
```

### Data Table Component
```typescript
// src/components/ui/DataTable.tsx
import React, { useState } from 'react'
import { ChevronDown, ChevronUp, ChevronsUpDown, Search } from 'lucide-react'
import { cn } from '@/utils/cn'

interface Column<T> {
  key: keyof T
  label: string
  sortable?: boolean
  render?: (value: T[keyof T], row: T) => React.ReactNode
  width?: string
  align?: 'left' | 'center' | 'right'
}

interface DataTableProps<T> {
  data: T[]
  columns: Column<T>[]
  loading?: boolean
  searchable?: boolean
  searchPlaceholder?: string
  emptyMessage?: string
  rowKey: keyof T
  onRowClick?: (row: T) => void
  className?: string
}

export function DataTable<T extends Record<string, any>>({
  data,
  columns,
  loading = false,
  searchable = true,
  searchPlaceholder = 'Search...',
  emptyMessage = 'No data available',
  rowKey,
  onRowClick,
  className,
}: DataTableProps<T>) {
  const [sortBy, setSortBy] = useState<keyof T | null>(null)
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc')
  const [searchQuery, setSearchQuery] = useState('')

  // Filter data based on search query
  const filteredData = React.useMemo(() => {
    if (!searchQuery) return data
    
    return data.filter(row =>
      columns.some(column => {
        const value = row[column.key]
        return String(value).toLowerCase().includes(searchQuery.toLowerCase())
      })
    )
  }, [data, searchQuery, columns])

  // Sort data
  const sortedData = React.useMemo(() => {
    if (!sortBy) return filteredData

    return [...filteredData].sort((a, b) => {
      const aValue = a[sortBy]
      const bValue = b[sortBy]

      if (aValue < bValue) return sortOrder === 'asc' ? -1 : 1
      if (aValue > bValue) return sortOrder === 'asc' ? 1 : -1
      return 0
    })
  }, [filteredData, sortBy, sortOrder])

  const handleSort = (key: keyof T) => {
    if (sortBy === key) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')
    } else {
      setSortBy(key)
      setSortOrder('asc')
    }
  }

  const getSortIcon = (key: keyof T) => {
    if (sortBy !== key) return <ChevronsUpDown className="h-4 w-4" />
    return sortOrder === 'asc' ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />
  }

  if (loading) {
    return <DataTableSkeleton columns={columns.length} />
  }

  return (
    <div className={cn('space-y-4', className)}>
      {/* Search */}
      {searchable && (
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
          <input
            type="text"
            placeholder={searchPlaceholder}
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
          />
        </div>
      )}

      {/* Table */}
      <div className="overflow-x-auto border border-gray-200 dark:border-gray-700 rounded-lg">
        <table className="w-full">
          <thead className="bg-gray-50 dark:bg-gray-800">
            <tr>
              {columns.map((column) => (
                <th
                  key={String(column.key)}
                  className={cn(
                    'px-4 py-3 text-sm font-medium text-gray-700 dark:text-gray-300',
                    column.align === 'center' && 'text-center',
                    column.align === 'right' && 'text-right',
                    column.sortable && 'cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-700'
                  )}
                  style={{ width: column.width }}
                  onClick={() => column.sortable && handleSort(column.key)}
                >
                  <div className="flex items-center gap-2">
                    {column.label}
                    {column.sortable && getSortIcon(column.key)}
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
            {sortedData.length === 0 ? (
              <tr>
                <td
                  colSpan={columns.length}
                  className="px-4 py-8 text-center text-gray-500 dark:text-gray-400"
                >
                  {emptyMessage}
                </td>
              </tr>
            ) : (
              sortedData.map((row, index) => (
                <tr
                  key={String(row[rowKey]) || index}
                  className={cn(
                    'hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors',
                    onRowClick && 'cursor-pointer'
                  )}
                  onClick={() => onRowClick?.(row)}
                >
                  {columns.map((column) => (
                    <td
                      key={String(column.key)}
                      className={cn(
                        'px-4 py-3 text-sm text-gray-900 dark:text-white',
                        column.align === 'center' && 'text-center',
                        column.align === 'right' && 'text-right'
                      )}
                    >
                      {column.render
                        ? column.render(row[column.key], row)
                        : String(row[column.key] || '')
                      }
                    </td>
                  ))}
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}

function DataTableSkeleton({ columns }: { columns: number }) {
  return (
    <div className="space-y-4">
      <div className="h-10 bg-gray-200 dark:bg-gray-700 rounded animate-pulse" />
      <div className="border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden">
        <div className="bg-gray-50 dark:bg-gray-800">
          <div className="flex">
            {Array.from({ length: columns }).map((_, i) => (
              <div key={i} className="flex-1 p-4">
                <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded animate-pulse" />
              </div>
            ))}
          </div>
        </div>
        {Array.from({ length: 5 }).map((_, i) => (
          <div key={i} className="flex border-t border-gray-200 dark:border-gray-700">
            {Array.from({ length: columns }).map((_, j) => (
              <div key={j} className="flex-1 p-4">
                <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded animate-pulse" />
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  )
}
```

### Loading Skeleton Components
```typescript
// src/components/ui/Skeleton.tsx
import React from 'react'
import { cn } from '@/utils/cn'

interface SkeletonProps {
  className?: string
  width?: string | number
  height?: string | number
  rounded?: boolean
  animate?: boolean
}

export function Skeleton({ 
  className, 
  width, 
  height, 
  rounded = true, 
  animate = true 
}: SkeletonProps) {
  return (
    <div
      className={cn(
        'bg-gray-200 dark:bg-gray-700',
        rounded && 'rounded',
        animate && 'animate-pulse',
        className
      )}
      style={{ width, height }}
    />
  )
}

export function CardSkeleton() {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
      <div className="animate-pulse space-y-4">
        <div className="flex items-center space-x-4">
          <Skeleton className="h-12 w-12 rounded-full" />
          <div className="space-y-2 flex-1">
            <Skeleton className="h-4 w-3/4" />
            <Skeleton className="h-3 w-1/2" />
          </div>
        </div>
        <Skeleton className="h-3 w-full" />
        <Skeleton className="h-3 w-2/3" />
      </div>
    </div>
  )
}

export function TableSkeleton({ rows = 5, columns = 4 }: { rows?: number; columns?: number }) {
  return (
    <div className="space-y-3">
      {/* Header */}
      <div className="flex space-x-4">
        {Array.from({ length: columns }).map((_, i) => (
          <Skeleton key={i} className="h-4 flex-1" />
        ))}
      </div>
      
      {/* Rows */}
      {Array.from({ length: rows }).map((_, i) => (
        <div key={i} className="flex space-x-4">
          {Array.from({ length: columns }).map((_, j) => (
            <Skeleton key={j} className="h-4 flex-1" />
          ))}
        </div>
      ))}
    </div>
  )
}
```

### Error Boundary Component
```typescript
// src/components/ui/ErrorBoundary.tsx
import React from 'react'
import { AlertTriangle, RefreshCw } from 'lucide-react'
import { Button } from './Button'

interface ErrorBoundaryState {
  hasError: boolean
  error?: Error
}

interface ErrorBoundaryProps {
  children: React.ReactNode
  fallback?: React.ComponentType<{ error?: Error; resetError: () => void }>
  onError?: (error: Error, errorInfo: React.ErrorInfo) => void
}

export class ErrorBoundary extends React.Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props)
    this.state = { hasError: false }
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error }
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('ErrorBoundary caught an error:', error, errorInfo)
    this.props.onError?.(error, errorInfo)
  }

  resetError = () => {
    this.setState({ hasError: false, error: undefined })
  }

  render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        const FallbackComponent = this.props.fallback
        return <FallbackComponent error={this.state.error} resetError={this.resetError} />
      }

      return <DefaultErrorFallback error={this.state.error} resetError={this.resetError} />
    }

    return this.props.children
  }
}

function DefaultErrorFallback({ error, resetError }: { error?: Error; resetError: () => void }) {
  return (
    <div className="min-h-[400px] flex items-center justify-center p-8">
      <div className="text-center max-w-md">
        <div className="mb-6">
          <AlertTriangle className="h-16 w-16 text-red-500 mx-auto mb-4" />
          <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-2">
            Something went wrong
          </h2>
          <p className="text-gray-600 dark:text-gray-400 mb-4">
            An unexpected error occurred. Please try refreshing the page or contact support if the problem persists.
          </p>
          
          {error && process.env.NODE_ENV === 'development' && (
            <details className="text-left mb-4 p-4 bg-gray-100 dark:bg-gray-800 rounded-lg">
              <summary className="cursor-pointer font-medium text-gray-900 dark:text-white mb-2">
                Error Details
              </summary>
              <pre className="text-xs text-red-600 dark:text-red-400 overflow-auto">
                {error.stack || error.message}
              </pre>
            </details>
          )}
        </div>
        
        <div className="space-y-3">
          <Button onClick={resetError} leftIcon={<RefreshCw className="h-4 w-4" />}>
            Try Again
          </Button>
          <Button 
            variant="ghost" 
            onClick={() => window.location.reload()}
          >
            Refresh Page
          </Button>
        </div>
      </div>
    </div>
  )
}

// Hook for functional components
export function useErrorBoundary() {
  const [error, setError] = React.useState<Error | null>(null)

  const resetError = React.useCallback(() => {
    setError(null)
  }, [])

  const captureError = React.useCallback((error: Error) => {
    setError(error)
  }, [])

  React.useEffect(() => {
    if (error) {
      throw error
    }
  }, [error])

  return { captureError, resetError }
}
```

### Utility Functions
```typescript
// src/utils/cn.ts
import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

// src/utils/formatters.ts
export function formatCurrency(amount: number, currency = 'USD'): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
  }).format(amount)
}

export function formatDate(date: string | Date, options?: Intl.DateTimeFormatOptions): string {
  const dateObj = typeof date === 'string' ? new Date(date) : date
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    ...options,
  }).format(dateObj)
}

export function formatRelativeTime(date: string | Date): string {
  const dateObj = typeof date === 'string' ? new Date(date) : date
  const now = new Date()
  const diffMs = now.getTime() - dateObj.getTime()
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMs / 3600000)
  const diffDays = Math.floor(diffMs / 86400000)

  if (diffMins < 1) return 'Just now'
  if (diffMins < 60) return `${diffMins}m ago`
  if (diffHours < 24) return `${diffHours}h ago`
  if (diffDays < 7) return `${diffDays}d ago`
  
  return formatDate(dateObj, { month: 'short', day: 'numeric' })
}

export function truncateText(text: string, maxLength: number): string {
  if (text.length <= maxLength) return text
  return text.slice(0, maxLength) + '...'
}

export function formatNumber(num: number, options?: Intl.NumberFormatOptions): string {
  return new Intl.NumberFormat('en-US', options).format(num)
}
```

### Animated Components Library

```typescript
// src/components/ui/AnimatedComponents.tsx
import { motion, useReducedMotion, AnimatePresence } from 'framer-motion'
import { useInView } from 'react-intersection-observer'
import { ReactNode, useEffect, useState } from 'react'

// Fade In Section - For page sections that animate in on scroll
interface FadeInSectionProps {
  children: ReactNode
  delay?: number
  direction?: 'up' | 'down' | 'left' | 'right'
  className?: string
}

export function FadeInSection({ 
  children, 
  delay = 0, 
  direction = 'up', 
  className 
}: FadeInSectionProps) {
  const { ref, inView } = useInView({
    threshold: 0.1,
    triggerOnce: true
  })
  const shouldReduceMotion = useReducedMotion()

  // PERFORMANCE: Use transform strings for hardware acceleration
  const directionVariants = {
    up: { transform: 'translateY(40px)', opacity: 0 },
    down: { transform: 'translateY(-40px)', opacity: 0 },
    left: { transform: 'translateX(40px)', opacity: 0 },
    right: { transform: 'translateX(-40px)', opacity: 0 }
  }

  if (shouldReduceMotion) {
    return <div className={className}>{children}</div>
  }

  return (
    <motion.div
      ref={ref}
      initial={directionVariants[direction]}
      animate={inView ? { transform: 'translate(0px, 0px)', opacity: 1 } : directionVariants[direction]}
      transition={{ duration: 0.6, delay, ease: "easeOut" }}
      className={className}
      // PERFORMANCE: Add will-change for heavy animations
      style={{ willChange: inView ? 'transform, opacity' : 'auto' }}
    >
      {children}
    </motion.div>
  )
}

// Stagger Container - For animating lists with staggered delays
interface StaggerContainerProps {
  children: ReactNode
  staggerDelay?: number
  className?: string
}

export function StaggerContainer({ 
  children, 
  staggerDelay = 0.1, 
  className 
}: StaggerContainerProps) {
  const shouldReduceMotion = useReducedMotion()

  const container = {
    hidden: { opacity: 1 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: shouldReduceMotion ? 0 : staggerDelay
      }
    }
  }

  // PERFORMANCE: Use transform instead of y for hardware acceleration
  const item = {
    hidden: { transform: 'translateY(20px)', opacity: 0 },
    visible: {
      transform: 'translateY(0px)',
      opacity: 1,
      transition: { duration: shouldReduceMotion ? 0 : 0.5 }
    }
  }

  return (
    <motion.div
      variants={container}
      initial="hidden"
      animate="visible"
      className={className}
    >
      {Array.isArray(children) ? 
        children.map((child, index) => (
          <motion.div key={index} variants={item}>
            {child}
          </motion.div>
        )) :
        <motion.div variants={item}>{children}</motion.div>
      }
    </motion.div>
  )
}

// Animated Counter - For numeric displays with count-up animation
interface AnimatedCounterProps {
  value: number
  duration?: number
  prefix?: string
  suffix?: string
  decimals?: number
  className?: string
}

export function AnimatedCounter({ 
  value, 
  duration = 2, 
  prefix = '', 
  suffix = '', 
  decimals = 0,
  className 
}: AnimatedCounterProps) {
  const [count, setCount] = useState(0)
  const { ref, inView } = useInView({ threshold: 0.1, triggerOnce: true })
  const shouldReduceMotion = useReducedMotion()

  useEffect(() => {
    if (!inView) return

    if (shouldReduceMotion) {
      setCount(value)
      return
    }

    let startTime: number | null = null
    const startValue = 0

    const animate = (currentTime: number) => {
      if (startTime === null) startTime = currentTime
      const progress = Math.min((currentTime - startTime) / (duration * 1000), 1)
      
      // Easing function for smooth animation
      const easeOutExpo = 1 - Math.pow(2, -10 * progress)
      const currentValue = startValue + (value - startValue) * easeOutExpo
      
      setCount(currentValue)

      if (progress < 1) {
        requestAnimationFrame(animate)
      } else {
        setCount(value)
      }
    }

    requestAnimationFrame(animate)
  }, [inView, value, duration, shouldReduceMotion])

  return (
    <span ref={ref} className={className}>
      {prefix}{count.toFixed(decimals)}{suffix}
    </span>
  )
}

// Page Transition - For smooth page transitions
export function PageTransition({ children }: { children: ReactNode }) {
  const shouldReduceMotion = useReducedMotion()

  // PERFORMANCE: Use transform strings for hardware acceleration
  const pageVariants = {
    initial: shouldReduceMotion ? {} : { 
      opacity: 0, 
      transform: 'translateX(-20px) scale(0.98)'
    },
    in: { 
      opacity: 1, 
      transform: 'translateX(0px) scale(1)'
    },
    out: shouldReduceMotion ? {} : { 
      opacity: 0, 
      transform: 'translateX(20px) scale(0.98)'
    }
  }

  const pageTransition = {
    type: "tween",
    ease: "anticipate",
    duration: shouldReduceMotion ? 0 : 0.4
  }

  return (
    <motion.div
      initial="initial"
      animate="in"
      exit="out"
      variants={pageVariants}
      transition={pageTransition}
    >
      {children}
    </motion.div>
  )
}

// Animated Modal - Enhanced modal with entrance/exit animations
interface AnimatedModalProps {
  isOpen: boolean
  onClose: () => void
  children: ReactNode
  size?: 'sm' | 'md' | 'lg' | 'xl'
  className?: string
}

export function AnimatedModal({ 
  isOpen, 
  onClose, 
  children, 
  size = 'md',
  className 
}: AnimatedModalProps) {
  const shouldReduceMotion = useReducedMotion()

  const sizeClasses = {
    sm: 'max-w-md',
    md: 'max-w-lg',
    lg: 'max-w-2xl',
    xl: 'max-w-4xl'
  }

  const backdropVariants = {
    hidden: { opacity: 0 },
    visible: { opacity: 1 }
  }

  // PERFORMANCE: Use transform for hardware acceleration
  const modalVariants = {
    hidden: shouldReduceMotion ? { opacity: 0 } : {
      opacity: 0,
      transform: 'scale(0.8) translateY(-50px)'
    },
    visible: {
      opacity: 1,
      transform: 'scale(1) translateY(0px)',
      transition: {
        type: "spring",
        damping: 25,
        stiffness: 500
      }
    }
  }

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          className="fixed inset-0 z-50 flex items-center justify-center p-4"
          initial="hidden"
          animate="visible"
          exit="hidden"
          variants={backdropVariants}
          onClick={onClose}
        >
          {/* Backdrop */}
          <div className="absolute inset-0 bg-black/50" />
          
          {/* Modal */}
          <motion.div
            className={`
              relative bg-white dark:bg-gray-800 rounded-xl shadow-xl 
              w-full ${sizeClasses[size]} max-h-[90vh] overflow-auto
              ${className}
            `}
            variants={modalVariants}
            onClick={(e) => e.stopPropagation()}
          >
            {children}
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}

// Pulse Effect - For highlighting new or important elements
export function PulseEffect({ children, className }: { children: ReactNode; className?: string }) {
  const shouldReduceMotion = useReducedMotion()

  if (shouldReduceMotion) {
    return <div className={className}>{children}</div>
  }

  return (
    <motion.div
      className={className}
      animate={{
        scale: [1, 1.05, 1],
        opacity: [1, 0.8, 1]
      }}
      transition={{
        duration: 2,
        repeat: Infinity,
        ease: "easeInOut"
      }}
    >
      {children}
    </motion.div>
  )
}

// Typing Animation - For text that appears to be typed
interface TypingAnimationProps {
  text: string
  speed?: number
  className?: string
  onComplete?: () => void
}

export function TypingAnimation({ 
  text, 
  speed = 100, 
  className,
  onComplete 
}: TypingAnimationProps) {
  const [displayedText, setDisplayedText] = useState('')
  const [isComplete, setIsComplete] = useState(false)
  const shouldReduceMotion = useReducedMotion()

  useEffect(() => {
    if (shouldReduceMotion) {
      setDisplayedText(text)
      setIsComplete(true)
      onComplete?.()
      return
    }

    let i = 0
    const timer = setInterval(() => {
      if (i < text.length) {
        setDisplayedText(text.slice(0, i + 1))
        i++
      } else {
        setIsComplete(true)
        onComplete?.()
        clearInterval(timer)
      }
    }, speed)

    return () => clearInterval(timer)
  }, [text, speed, shouldReduceMotion, onComplete])

  return (
    <span className={className}>
      {displayedText}
      {!isComplete && !shouldReduceMotion && (
        <motion.span
          animate={{ opacity: [1, 0] }}
          transition={{ duration: 0.8, repeat: Infinity, repeatType: "reverse" }}
        >
          |
        </motion.span>
      )}
    </span>
  )
}
```

**Success Criteria:**
- Consistent design system with purple gradient theme and dark mode support
- Accessible components with proper ARIA labels and keyboard navigation
- Responsive design that works on all screen sizes
- Loading states and skeleton loaders for all async operations
- Comprehensive error handling with user-friendly error messages
- Toast notification system for user feedback
- Modal and dialog components with proper focus management
- Data table with sorting, searching, and pagination capabilities
- Reusable form components with validation support
- TypeScript types for all components and props
- Performance optimized with proper memoization
- Integration with existing styling and theme system
- **Smooth Framer Motion animations** with accessibility support (respects prefers-reduced-motion)
- **Micro-interactions** that enhance user experience without being distracting
- **Page transitions** that provide visual continuity between routes
- **Staggered animations** for lists and grids that create engaging reveals
- **Progress indicators** with smooth animations for better perceived performance

This shared component library provides a solid foundation for building consistent, accessible, and maintainable user interfaces across the Blog-Poster platform.
import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { AlertTriangle, Trash2, LogOut, X, Check } from 'lucide-react'
import { Button } from './button'
import { Modal } from './Modal'

// Inline confirmation button
interface ConfirmButtonProps {
  onConfirm: () => void
  children: React.ReactNode
  confirmText?: string
  cancelText?: string
  className?: string
  variant?: 'danger' | 'warning' | 'info'
  size?: 'sm' | 'md' | 'lg'
}

export function ConfirmButton({
  onConfirm,
  children,
  confirmText = "Are you sure?",
  cancelText = "Cancel",
  className,
  variant = 'danger',
  size = 'md'
}: ConfirmButtonProps) {
  const [confirming, setConfirming] = useState(false)
  
  const variantStyles = {
    danger: 'text-destructive hover:text-destructive',
    warning: 'text-yellow-600 hover:text-yellow-700',
    info: 'text-primary hover:text-primary/80'
  }

  if (confirming) {
    return (
      <motion.div 
        className="flex items-center gap-2"
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.2 }}
      >
        <span className="text-sm text-muted-foreground whitespace-nowrap">
          {confirmText}
        </span>
        <Button
          onClick={() => {
            onConfirm()
            setConfirming(false)
          }}
          variant="destructive"
          size="sm"
          className="h-7"
        >
          <Check className="w-3 h-3" />
        </Button>
        <Button
          onClick={() => setConfirming(false)}
          variant="outline"
          size="sm"
          className="h-7"
        >
          <X className="w-3 h-3" />
        </Button>
      </motion.div>
    )
  }
  
  return (
    <button
      onClick={() => setConfirming(true)}
      className={`${variantStyles[variant]} transition-colors ${className}`}
    >
      {children}
    </button>
  )
}

// Modal confirmation dialog
interface ConfirmDialogProps {
  isOpen: boolean
  onClose: () => void
  onConfirm: () => void
  title: string
  description: string
  confirmText?: string
  cancelText?: string
  variant?: 'danger' | 'warning' | 'info'
  icon?: React.ReactNode
  loading?: boolean
}

export function ConfirmDialog({
  isOpen,
  onClose,
  onConfirm,
  title,
  description,
  confirmText = 'Confirm',
  cancelText = 'Cancel',
  variant = 'danger',
  icon,
  loading = false
}: ConfirmDialogProps) {
  const variantConfig = {
    danger: {
      icon: icon || <AlertTriangle className="w-6 h-6 text-destructive" />,
      buttonClass: 'bg-destructive hover:bg-destructive/90 text-destructive-foreground',
      iconBg: 'bg-destructive/10'
    },
    warning: {
      icon: icon || <AlertTriangle className="w-6 h-6 text-yellow-600" />,
      buttonClass: 'bg-yellow-600 hover:bg-yellow-700 text-white',
      iconBg: 'bg-yellow-100 dark:bg-yellow-900/20'
    },
    info: {
      icon: icon || <AlertTriangle className="w-6 h-6 text-primary" />,
      buttonClass: 'bg-primary hover:bg-primary/90 text-primary-foreground',
      iconBg: 'bg-primary/10'
    }
  }

  const config = variantConfig[variant]

  const handleConfirm = () => {
    onConfirm()
    onClose()
  }

  return (
    <Modal isOpen={isOpen} onClose={onClose} size="sm">
      <div className="p-6">
        <div className="flex items-start gap-4">
          <div className={`p-2 rounded-full ${config.iconBg}`}>
            {config.icon}
          </div>
          <div className="flex-1">
            <h3 className="text-lg font-semibold text-foreground mb-2">
              {title}
            </h3>
            <p className="text-muted-foreground mb-6">
              {description}
            </p>
            
            <div className="flex items-center gap-3 justify-end">
              <Button
                onClick={onClose}
                variant="outline"
                disabled={loading}
              >
                {cancelText}
              </Button>
              <Button
                onClick={handleConfirm}
                className={config.buttonClass}
                loading={loading}
                disabled={loading}
              >
                {confirmText}
              </Button>
            </div>
          </div>
        </div>
      </div>
    </Modal>
  )
}

// Pre-configured confirmation dialogs for common actions
export function DeleteConfirmDialog({
  isOpen,
  onClose,
  onConfirm,
  itemName,
  loading = false
}: {
  isOpen: boolean
  onClose: () => void
  onConfirm: () => void
  itemName: string
  loading?: boolean
}) {
  return (
    <ConfirmDialog
      isOpen={isOpen}
      onClose={onClose}
      onConfirm={onConfirm}
      title="Delete Item"
      description={`Are you sure you want to delete "${itemName}"? This action cannot be undone.`}
      confirmText="Delete"
      cancelText="Cancel"
      variant="danger"
      icon={<Trash2 className="w-6 h-6 text-destructive" />}
      loading={loading}
    />
  )
}

export function SignOutConfirmDialog({
  isOpen,
  onClose,
  onConfirm,
  loading = false
}: {
  isOpen: boolean
  onClose: () => void
  onConfirm: () => void
  loading?: boolean
}) {
  return (
    <ConfirmDialog
      isOpen={isOpen}
      onClose={onClose}
      onConfirm={onConfirm}
      title="Sign Out"
      description="Are you sure you want to sign out? Any unsaved changes will be lost."
      confirmText="Sign Out"
      cancelText="Cancel"
      variant="warning"
      icon={<LogOut className="w-6 h-6 text-yellow-600" />}
      loading={loading}
    />
  )
}

// Hook for managing confirmation dialogs
export function useConfirmDialog() {
  const [isOpen, setIsOpen] = useState(false)
  const [config, setConfig] = useState<{
    title: string
    description: string
    onConfirm: () => void
    variant?: 'danger' | 'warning' | 'info'
    confirmText?: string
    cancelText?: string
  } | null>(null)

  const openDialog = (dialogConfig: typeof config) => {
    setConfig(dialogConfig)
    setIsOpen(true)
  }

  const closeDialog = () => {
    setIsOpen(false)
    setConfig(null)
  }

  const ConfirmDialogComponent = config ? (
    <ConfirmDialog
      isOpen={isOpen}
      onClose={closeDialog}
      {...config}
    />
  ) : null

  return {
    openDialog,
    closeDialog,
    ConfirmDialogComponent
  }
}

// Quick confirmation for destructive actions
export function QuickDeleteButton({
  onDelete,
  itemName,
  className
}: {
  onDelete: () => void
  itemName?: string
  className?: string
}) {
  const [showConfirm, setShowConfirm] = useState(false)

  return (
    <>
      <ConfirmButton
        onConfirm={onDelete}
        confirmText={itemName ? `Delete ${itemName}?` : "Delete?"}
        variant="danger"
        className={className}
      >
        <Trash2 className="w-4 h-4" />
      </ConfirmButton>
    </>
  )
}

// Confirmation with additional context
export function ContextualConfirm({
  children,
  title,
  description,
  context,
  onConfirm,
  variant = 'danger'
}: {
  children: React.ReactNode
  title: string
  description: string
  context?: React.ReactNode
  onConfirm: () => void
  variant?: 'danger' | 'warning' | 'info'
}) {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <>
      <div onClick={() => setIsOpen(true)}>
        {children}
      </div>
      
      <Modal isOpen={isOpen} onClose={() => setIsOpen(false)} size="md">
        <div className="p-6">
          <h3 className="text-lg font-semibold text-foreground mb-2">
            {title}
          </h3>
          <p className="text-muted-foreground mb-4">
            {description}
          </p>
          
          {context && (
            <div className="bg-muted rounded-lg p-4 mb-6">
              {context}
            </div>
          )}
          
          <div className="flex items-center gap-3 justify-end">
            <Button
              onClick={() => setIsOpen(false)}
              variant="outline"
            >
              Cancel
            </Button>
            <Button
              onClick={() => {
                onConfirm()
                setIsOpen(false)
              }}
              variant={variant === 'danger' ? 'destructive' : 'default'}
            >
              Confirm
            </Button>
          </div>
        </div>
      </Modal>
    </>
  )
}
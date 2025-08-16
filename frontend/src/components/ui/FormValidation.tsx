import React from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { CheckCircle, XCircle, AlertCircle, Eye, EyeOff } from 'lucide-react'
import { cn } from '@/lib/utils'
import { Input } from './input'

interface FormFieldProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string
  error?: string
  success?: string | boolean
  hint?: string
  leftIcon?: React.ReactNode
  rightIcon?: React.ReactNode
  loading?: boolean
  showValidation?: boolean
}

export function FormField({
  label,
  error,
  success,
  hint,
  leftIcon,
  rightIcon,
  loading = false,
  showValidation = true,
  className,
  ...props
}: FormFieldProps) {
  const hasError = !!error
  const hasSuccess = !!success && !hasError
  const fieldId = props.id || `field-${Math.random().toString(36).substr(2, 9)}`

  // Determine border and ring colors based on state
  const getBorderClass = () => {
    if (hasError) return 'border-destructive focus:ring-destructive'
    if (hasSuccess) return 'border-green-500 focus:ring-green-500'
    return 'border-input focus:ring-ring'
  }

  return (
    <div className="space-y-2">
      {label && (
        <label 
          htmlFor={fieldId}
          className="block text-sm font-medium text-foreground"
        >
          {label}
          {props.required && <span className="text-destructive ml-1">*</span>}
        </label>
      )}
      
      <div className="relative">
        {leftIcon && (
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <div className={cn(
              "text-muted-foreground",
              hasError && "text-destructive",
              hasSuccess && "text-green-500"
            )}>
              {leftIcon}
            </div>
          </div>
        )}
        
        <input
          id={fieldId}
          className={cn(
            'flex h-10 w-full rounded-md border bg-background px-3 py-2 text-sm',
            'placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-offset-2',
            'disabled:cursor-not-allowed disabled:opacity-50',
            'transition-all duration-200',
            leftIcon && 'pl-10',
            (rightIcon || showValidation) && 'pr-10',
            getBorderClass(),
            className
          )}
          {...props}
        />
        
        {/* Validation icons and loading */}
        <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
          {loading ? (
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
              className="w-4 h-4 border-2 border-muted-foreground border-t-primary rounded-full"
            />
          ) : showValidation ? (
            <AnimatePresence mode="wait">
              {hasError && (
                <motion.div
                  key="error"
                  initial={{ scale: 0, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  exit={{ scale: 0, opacity: 0 }}
                  transition={{ duration: 0.2 }}
                >
                  <XCircle className="w-5 h-5 text-destructive" />
                </motion.div>
              )}
              {hasSuccess && (
                <motion.div
                  key="success"
                  initial={{ scale: 0, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  exit={{ scale: 0, opacity: 0 }}
                  transition={{ duration: 0.2 }}
                >
                  <CheckCircle className="w-5 h-5 text-green-500" />
                </motion.div>
              )}
            </AnimatePresence>
          ) : rightIcon ? (
            <div className="text-muted-foreground">{rightIcon}</div>
          ) : null}
        </div>
      </div>

      {/* Error message */}
      <AnimatePresence>
        {error && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.2 }}
            className="flex items-center gap-2 text-sm text-destructive"
            role="alert"
          >
            <AlertCircle className="w-4 h-4 flex-shrink-0" />
            {error}
          </motion.div>
        )}
      </AnimatePresence>
      
      {/* Success message */}
      <AnimatePresence>
        {hasSuccess && typeof success === 'string' && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.2 }}
            className="flex items-center gap-2 text-sm text-green-600 dark:text-green-400"
          >
            <CheckCircle className="w-4 h-4 flex-shrink-0" />
            {success}
          </motion.div>
        )}
      </AnimatePresence>
      
      {/* Hint text */}
      {hint && !error && (
        <p className="text-sm text-muted-foreground">
          {hint}
        </p>
      )}
    </div>
  )
}

// Password field with toggle visibility
interface PasswordFieldProps extends Omit<FormFieldProps, 'type' | 'rightIcon'> {
  showToggle?: boolean
}

export function PasswordField({ 
  showToggle = true, 
  ...props 
}: PasswordFieldProps) {
  const [showPassword, setShowPassword] = React.useState(false)

  return (
    <FormField
      {...props}
      type={showPassword ? 'text' : 'password'}
      rightIcon={
        showToggle ? (
          <button
            type="button"
            onClick={() => setShowPassword(!showPassword)}
            className="text-muted-foreground hover:text-foreground transition-colors"
          >
            {showPassword ? (
              <EyeOff className="w-4 h-4" />
            ) : (
              <Eye className="w-4 h-4" />
            )}
          </button>
        ) : undefined
      }
      showValidation={!showToggle} // Don't show validation icon if we have toggle
    />
  )
}

// Field with character count
interface TextFieldWithCountProps extends FormFieldProps {
  maxLength?: number
  showCount?: boolean
}

export function TextFieldWithCount({ 
  maxLength, 
  showCount = true, 
  value,
  ...props 
}: TextFieldWithCountProps) {
  const charCount = String(value || '').length
  const isNearLimit = maxLength && charCount > maxLength * 0.8
  const isOverLimit = maxLength && charCount > maxLength

  return (
    <div>
      <FormField
        {...props}
        value={value}
        maxLength={maxLength}
      />
      {showCount && maxLength && (
        <div className="flex justify-end mt-1">
          <span className={cn(
            "text-xs",
            isOverLimit ? "text-destructive" : 
            isNearLimit ? "text-yellow-600 dark:text-yellow-400" : 
            "text-muted-foreground"
          )}>
            {charCount}/{maxLength}
          </span>
        </div>
      )}
    </div>
  )
}

// Real-time validation hook
export function useFieldValidation(
  value: string,
  rules: {
    required?: boolean
    minLength?: number
    maxLength?: number
    pattern?: RegExp
    custom?: (value: string) => string | null
  }
) {
  const [error, setError] = React.useState<string>('')
  const [isValid, setIsValid] = React.useState(false)

  React.useEffect(() => {
    let errorMessage = ''

    if (rules.required && !value.trim()) {
      errorMessage = 'This field is required'
    } else if (value) {
      if (rules.minLength && value.length < rules.minLength) {
        errorMessage = `Must be at least ${rules.minLength} characters`
      } else if (rules.maxLength && value.length > rules.maxLength) {
        errorMessage = `Must be no more than ${rules.maxLength} characters`
      } else if (rules.pattern && !rules.pattern.test(value)) {
        errorMessage = 'Invalid format'
      } else if (rules.custom) {
        errorMessage = rules.custom(value) || ''
      }
    }

    setError(errorMessage)
    setIsValid(!errorMessage && (value.length > 0 || !rules.required))
  }, [value, rules])

  return { error, isValid }
}

// Form validation patterns
export const ValidationPatterns = {
  email: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
  phone: /^\+?[\d\s\-\(\)]+$/,
  url: /^https?:\/\/.+\..+/,
  slug: /^[a-z0-9]+(?:-[a-z0-9]+)*$/,
  apiKey: /^[a-zA-Z0-9]{20,}$/,
}
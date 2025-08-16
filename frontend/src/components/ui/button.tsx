import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva, type VariantProps } from "class-variance-authority"
import { motion } from "framer-motion"
import { Loader2 } from "lucide-react"

import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-lg text-sm font-medium transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:size-4 [&_svg]:shrink-0",
  {
    variants: {
      variant: {
        default: "bg-purple-gradient text-white hover:opacity-90 focus:ring-primary",
        destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        outline: "border-2 border-primary text-primary hover:bg-primary/10 focus:ring-primary",
        secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80",
        ghost: "text-muted-foreground hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
        success: "bg-success-gradient text-white hover:opacity-90 focus:ring-green-500",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 px-3",
        lg: "h-11 px-6 py-3",
        xl: "h-12 px-8 py-4 text-base",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean
  loading?: boolean
  loadingText?: string
  leftIcon?: React.ReactNode
  rightIcon?: React.ReactNode
  fullWidth?: boolean
  animation?: boolean
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ 
    className, 
    variant, 
    size, 
    asChild = false, 
    loading = false,
    loadingText,
    leftIcon,
    rightIcon,
    fullWidth = false,
    animation = true,
    children,
    disabled,
    ...props 
  }, ref) => {
    const isDisabled = disabled || loading
    
    // Filter out motion-specific props to avoid conflicts
    const {
      onDrag,
      onDragEnd,
      onDragStart,
      whileHover,
      whileTap,
      ...filteredProps
    } = props as any

    const baseClassName = cn(
      buttonVariants({ variant, size }),
      fullWidth && "w-full",
      className
    )

    if (asChild) {
      return (
        <Slot
          className={baseClassName}
          ref={ref}
          disabled={isDisabled}
          {...filteredProps}
        >
          {children}
        </Slot>
      )
    }

    if (animation) {
      return (
        <motion.button
          className={baseClassName}
          ref={ref}
          disabled={isDisabled}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          transition={{ type: "spring", stiffness: 300, damping: 20 }}
          {...filteredProps}
        >
          {loading ? (
            <motion.div
              className="flex items-center gap-2"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.3 }}
            >
              <Loader2 className="h-4 w-4 animate-spin" />
              {loadingText || 'Loading...'}
            </motion.div>
          ) : (
            <>
              {leftIcon && (
                <span className="flex items-center">
                  {leftIcon}
                </span>
              )}
              {children}
              {rightIcon && (
                <span className="flex items-center">
                  {rightIcon}
                </span>
              )}
            </>
          )}
        </motion.button>
      )
    }

    return (
      <button
        className={baseClassName}
        ref={ref}
        disabled={isDisabled}
        {...filteredProps}
      >
        {loading ? (
          <div className="flex items-center gap-2">
            <Loader2 className="h-4 w-4 animate-spin" />
            {loadingText || 'Loading...'}
          </div>
        ) : (
          <>
            {leftIcon && (
              <span className="flex items-center">
                {leftIcon}
              </span>
            )}
            {children}
            {rightIcon && (
              <span className="flex items-center">
                {rightIcon}
              </span>
            )}
          </>
        )}
      </button>
    )
  }
)
Button.displayName = "Button"

// Button group for related actions
export function ButtonGroup({ children, className }: { children: React.ReactNode; className?: string }) {
  return (
    <div className={cn('inline-flex rounded-lg shadow-sm', className)}>
      {React.Children.map(children, (child, index) => {
        if (React.isValidElement(child) && typeof child.type !== 'string') {
          return React.cloneElement(child as React.ReactElement<any>, {
            className: cn(
              (child as any).props?.className,
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

export { Button, buttonVariants }

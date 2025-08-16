import { motion, useReducedMotion, AnimatePresence, useScroll, useTransform, useSpring, useMotionValue } from 'framer-motion'
import { useInView } from 'react-intersection-observer'
import { ReactNode, useEffect, useState, useRef } from 'react'

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

  const directionVariants = {
    up: { opacity: 0, y: 40 },
    down: { opacity: 0, y: -40 },
    left: { opacity: 0, x: 40 },
    right: { opacity: 0, x: -40 }
  }

  if (shouldReduceMotion) {
    return <div className={className}>{children}</div>
  }

  return (
    <motion.div
      ref={ref}
      initial={directionVariants[direction]}
      animate={inView ? { opacity: 1, x: 0, y: 0 } : directionVariants[direction]}
      transition={{ duration: 0.6, delay, ease: "easeOut" }}
      className={className}
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

  const item = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
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

  const pageVariants = {
    initial: shouldReduceMotion ? {} : { 
      opacity: 0, 
      x: -20,
      scale: 0.98
    },
    in: { 
      opacity: 1, 
      x: 0,
      scale: 1
    },
    out: shouldReduceMotion ? {} : { 
      opacity: 0, 
      x: 20,
      scale: 0.98
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

// Scale on Hover - Simple hover animation for interactive elements
export function ScaleOnHover({ children, className, scale = 1.05 }: { 
  children: ReactNode
  className?: string
  scale?: number
}) {
  const shouldReduceMotion = useReducedMotion()

  if (shouldReduceMotion) {
    return <div className={className}>{children}</div>
  }

  return (
    <motion.div
      className={className}
      whileHover={{ scale }}
      whileTap={{ scale: scale * 0.95 }}
      transition={{ type: "spring", stiffness: 300, damping: 20 }}
    >
      {children}
    </motion.div>
  )
}

// Scroll Progress Indicator
interface ScrollProgressProps {
  className?: string
}

export function ScrollProgress({ className = '' }: ScrollProgressProps) {
  const { scrollYProgress } = useScroll()
  const scaleX = useSpring(scrollYProgress, {
    stiffness: 100,
    damping: 30,
    restDelta: 0.001
  })

  return (
    <motion.div
      className={`fixed top-0 left-0 right-0 h-1 bg-gradient-to-r from-primary to-primary/60 z-50 origin-left ${className}`}
      style={{ scaleX }}
    />
  )
}

// Animated Progress Bar
interface AnimatedProgressProps {
  value: number
  max?: number
  showLabel?: boolean
  variant?: 'default' | 'gradient'
  className?: string
}

export function AnimatedProgress({ 
  value, 
  max = 100, 
  showLabel = false,
  variant = 'default',
  className = ''
}: AnimatedProgressProps) {
  const percentage = Math.min((value / max) * 100, 100)
  const shouldReduceMotion = useReducedMotion()
  
  const progressClasses = variant === 'gradient'
    ? 'bg-gradient-to-r from-primary to-primary/60'
    : 'bg-primary'

  return (
    <div className={`space-y-2 ${className}`}>
      {showLabel && (
        <div className="flex justify-between text-sm">
          <span>Progress</span>
          <motion.span
            key={value}
            initial={shouldReduceMotion ? {} : { scale: 1.2 }}
            animate={{ scale: 1 }}
            transition={{ type: "spring", stiffness: 300 }}
          >
            {Math.round(percentage)}%
          </motion.span>
        </div>
      )}
      <div className="h-2 bg-muted rounded-full overflow-hidden">
        <motion.div
          className={`h-full rounded-full ${progressClasses}`}
          initial={{ width: 0 }}
          animate={{ width: `${percentage}%` }}
          transition={shouldReduceMotion ? { duration: 0 } : { 
            duration: 1, 
            ease: "easeOut",
            type: "spring",
            stiffness: 100
          }}
        />
      </div>
    </div>
  )
}

// Pulsing Status Indicator
interface PulsingIndicatorProps {
  status: 'active' | 'inactive' | 'pending'
  size?: 'sm' | 'md' | 'lg'
  className?: string
}

export function PulsingIndicator({ status, size = 'md', className = '' }: PulsingIndicatorProps) {
  const shouldReduceMotion = useReducedMotion()
  
  const sizeClasses = {
    sm: 'w-2 h-2',
    md: 'w-3 h-3',
    lg: 'w-4 h-4'
  }

  const statusClasses = {
    active: 'bg-green-500',
    inactive: 'bg-gray-400',
    pending: 'bg-yellow-500'
  }

  return (
    <motion.div
      className={`
        rounded-full ${sizeClasses[size]} ${statusClasses[status]} ${className}
      `}
      animate={!shouldReduceMotion && status === 'active' ? {
        scale: [1, 1.2, 1],
        opacity: [1, 0.6, 1]
      } : {}}
      transition={!shouldReduceMotion && status === 'active' ? {
        duration: 2,
        repeat: Infinity,
        ease: "easeInOut"
      } : {}}
    />
  )
}
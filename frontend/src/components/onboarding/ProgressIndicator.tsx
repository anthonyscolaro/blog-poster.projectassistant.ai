import React from 'react'
import { Check } from 'lucide-react'
import { cn } from '@/lib/utils'

interface ProgressIndicatorProps {
  currentStep: number
  totalSteps: number
  className?: string
}

const stepNames = [
  'Welcome',
  'Profile',
  'API Keys',
  'WordPress',
  'Team',
  'Complete'
]

export function ProgressIndicator({ currentStep, totalSteps, className }: ProgressIndicatorProps) {
  return (
    <div className={cn("flex items-center space-x-2", className)}>
      {Array.from({ length: totalSteps }, (_, index) => {
        const stepNumber = index + 1
        const isCompleted = stepNumber < currentStep
        const isCurrent = stepNumber === currentStep
        const stepName = stepNames[index] || `Step ${stepNumber}`

        return (
          <div key={stepNumber} className="flex items-center">
            <div className="flex flex-col items-center">
              <div
                className={cn(
                  "w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium transition-all duration-200",
                  {
                    "bg-gradient-to-r from-primary to-primary/80 text-white": isCurrent,
                    "bg-primary text-white": isCompleted,
                    "bg-muted text-muted-foreground": !isCurrent && !isCompleted,
                  }
                )}
              >
                {isCompleted ? (
                  <Check className="w-4 h-4" />
                ) : (
                  stepNumber
                )}
              </div>
              <span className={cn(
                "text-xs mt-1 hidden sm:block",
                {
                  "text-primary font-medium": isCurrent,
                  "text-muted-foreground": !isCurrent
                }
              )}>
                {stepName}
              </span>
            </div>
            {stepNumber < totalSteps && (
              <div
                className={cn(
                  "w-8 h-0.5 mx-2 transition-colors duration-200",
                  {
                    "bg-primary": isCompleted,
                    "bg-muted": !isCompleted,
                  }
                )}
              />
            )}
          </div>
        )
      })}
    </div>
  )
}
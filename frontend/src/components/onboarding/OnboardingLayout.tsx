import React from 'react'
import { motion } from 'framer-motion'
import { ProgressIndicator } from './ProgressIndicator'
import { Button } from '@/components/ui/button'
import { ArrowLeft, SkipForward } from 'lucide-react'

interface OnboardingLayoutProps {
  children: React.ReactNode
  currentStep: number
  totalSteps: number
  stepName: string
  onBack?: () => void
  onSkip?: () => void
  onContinue?: () => void
  canContinue?: boolean
  isLoading?: boolean
  showSkip?: boolean
}

export function OnboardingLayout({
  children,
  currentStep,
  totalSteps,
  stepName,
  onBack,
  onSkip,
  onContinue,
  canContinue = true,
  isLoading = false,
  showSkip = true
}: OnboardingLayoutProps) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-primary/5 via-background to-primary/5">
      {/* Header */}
      <div className="border-b border-border/50 bg-background/80 backdrop-blur-sm sticky top-0 z-10">
        <div className="container max-w-4xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="h-8 w-8 rounded bg-gradient-to-r from-primary to-primary/80 flex items-center justify-center">
                <span className="text-white font-bold text-sm">BP</span>
              </div>
              <div>
                <h1 className="text-lg font-semibold text-foreground">Blog-Poster Setup</h1>
                <p className="text-sm text-muted-foreground">{stepName}</p>
              </div>
            </div>
            <ProgressIndicator 
              currentStep={currentStep} 
              totalSteps={totalSteps} 
            />
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="container max-w-4xl mx-auto px-6 py-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="grid lg:grid-cols-3 gap-8"
        >
          {/* Main Content Area */}
          <div className="lg:col-span-2">
            <div className="bg-background border border-border rounded-lg shadow-sm p-8">
              {children}
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Progress Card */}
            <div className="bg-background border border-border rounded-lg p-6">
              <h3 className="font-semibold text-foreground mb-3">Your Progress</h3>
              <div className="space-y-3">
                <div className="flex justify-between text-sm">
                  <span className="text-muted-foreground">Step {currentStep} of {totalSteps}</span>
                  <span className="text-primary font-medium">
                    {Math.round((currentStep / totalSteps) * 100)}% Complete
                  </span>
                </div>
                <div className="w-full bg-muted rounded-full h-2">
                  <div 
                    className="bg-gradient-to-r from-primary to-primary/80 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${(currentStep / totalSteps) * 100}%` }}
                  />
                </div>
                <p className="text-sm text-muted-foreground">
                  About {Math.max(1, totalSteps - currentStep)} minute{totalSteps - currentStep !== 1 ? 's' : ''} remaining
                </p>
              </div>
            </div>

            {/* Help Card */}
            <div className="bg-background border border-border rounded-lg p-6">
              <h3 className="font-semibold text-foreground mb-3">Need Help?</h3>
              <div className="space-y-3 text-sm">
                <div className="flex items-start space-x-2">
                  <div className="w-2 h-2 bg-primary rounded-full mt-2 flex-shrink-0" />
                  <div>
                    <p className="font-medium text-foreground">Documentation</p>
                    <p className="text-muted-foreground">Step-by-step guides</p>
                  </div>
                </div>
                <div className="flex items-start space-x-2">
                  <div className="w-2 h-2 bg-primary rounded-full mt-2 flex-shrink-0" />
                  <div>
                    <p className="font-medium text-foreground">Live Chat</p>
                    <p className="text-muted-foreground">Get instant help</p>
                  </div>
                </div>
                <div className="flex items-start space-x-2">
                  <div className="w-2 h-2 bg-primary rounded-full mt-2 flex-shrink-0" />
                  <div>
                    <p className="font-medium text-foreground">Video Tutorials</p>
                    <p className="text-muted-foreground">Watch and learn</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Navigation */}
        <div className="flex items-center justify-between mt-8 pt-6 border-t border-border">
          <div className="flex items-center space-x-3">
            {onBack && (
              <Button
                variant="outline"
                onClick={onBack}
                className="flex items-center space-x-2"
              >
                <ArrowLeft className="w-4 h-4" />
                <span>Previous</span>
              </Button>
            )}
          </div>

          <div className="flex items-center space-x-3">
            {showSkip && onSkip && (
              <Button
                variant="ghost"
                onClick={onSkip}
                className="flex items-center space-x-2 text-muted-foreground"
              >
                <SkipForward className="w-4 h-4" />
                <span>Skip This Step</span>
              </Button>
            )}
            {onContinue && (
              <Button
                onClick={onContinue}
                disabled={!canContinue || isLoading}
                className="bg-gradient-to-r from-primary to-primary/80 text-white px-6"
              >
                {isLoading ? 'Loading...' : currentStep === totalSteps ? 'Complete Setup' : 'Continue'}
              </Button>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
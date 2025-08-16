import React from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { OnboardingLayout } from '@/components/onboarding/OnboardingLayout'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { CheckCircle, Clock, Rocket, Users, Zap, Settings } from 'lucide-react'

export default function Welcome() {
  const navigate = useNavigate()

  const handleContinue = () => {
    navigate('/onboarding/profile')
  }

  const handleSkip = () => {
    navigate('/dashboard')
  }

  const features = [
    {
      icon: CheckCircle,
      title: "Connect WordPress",
      description: "Automatically publish with perfect formatting"
    },
    {
      icon: Zap,
      title: "Configure AI Agents",
      description: "Set up your API keys for content generation"
    },
    {
      icon: Settings,
      title: "Generate First Article",
      description: "Create SEO-optimized content in minutes"
    },
    {
      icon: Users,
      title: "Team Collaboration",
      description: "Invite team members and set permissions"
    }
  ]

  return (
    <OnboardingLayout
      currentStep={1}
      totalSteps={5}
      stepName="Welcome to Blog-Poster"
      onContinue={handleContinue}
      onSkip={handleSkip}
      showSkip={true}
    >
      <div className="text-center space-y-8">
        {/* Hero Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="space-y-4"
        >
          <div className="text-6xl mb-4">🚀</div>
          <h1 className="text-3xl font-bold text-foreground">
            Welcome to Blog-Poster!
          </h1>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Let&apos;s get you set up in just 5 minutes. We&apos;ll configure everything you need to start generating amazing content.
          </p>
        </motion.div>

        {/* What You'll Accomplish */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="space-y-6"
        >
          <h2 className="text-xl font-semibold text-foreground">
            What You&apos;ll Accomplish:
          </h2>
          
          <div className="grid md:grid-cols-2 gap-4">
            {features.map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 + index * 0.1 }}
              >
                <Card className="h-full hover:shadow-md transition-shadow">
                  <CardContent className="p-6">
                    <div className="flex items-start space-x-4">
                      <div className="bg-gradient-to-r from-primary to-primary/80 p-2 rounded-lg">
                        <feature.icon className="w-5 h-5 text-white" />
                      </div>
                      <div className="text-left">
                        <h3 className="font-semibold text-foreground mb-2">
                          {feature.title}
                        </h3>
                        <p className="text-sm text-muted-foreground">
                          {feature.description}
                        </p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Time Expectation */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="bg-muted/50 rounded-lg p-6"
        >
          <div className="flex items-center justify-center space-x-3">
            <Clock className="w-5 h-5 text-primary" />
            <span className="text-lg font-medium text-foreground">
              About 5 minutes to complete
            </span>
          </div>
          <p className="text-sm text-muted-foreground mt-2">
            You can always skip steps and return later
          </p>
        </motion.div>

        {/* Pipeline Preview */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7 }}
          className="space-y-4"
        >
          <h3 className="text-lg font-semibold text-foreground">
            Your 5-Agent Content Pipeline
          </h3>
          <div className="flex items-center justify-center space-x-2 overflow-x-auto pb-4">
            {[
              { name: 'Competitor', color: 'bg-red-500' },
              { name: 'Topic', color: 'bg-orange-500' },
              { name: 'Article', color: 'bg-blue-500' },
              { name: 'Legal', color: 'bg-green-500' },
              { name: 'WordPress', color: 'bg-purple-500' }
            ].map((agent, index) => (
              <div key={agent.name} className="flex items-center">
                <div className="flex flex-col items-center">
                  <div className={`w-10 h-10 ${agent.color} rounded-full flex items-center justify-center text-white text-xs font-bold`}>
                    {index + 1}
                  </div>
                  <span className="text-xs text-muted-foreground mt-1">
                    {agent.name}
                  </span>
                </div>
                {index < 4 && (
                  <div className="w-8 h-0.5 bg-muted mx-2" />
                )}
              </div>
            ))}
          </div>
        </motion.div>

        {/* CTA Buttons */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8 }}
          className="flex flex-col sm:flex-row items-center justify-center space-y-3 sm:space-y-0 sm:space-x-4 pt-6"
        >
          <Button
            onClick={handleContinue}
            size="lg"
            className="bg-gradient-to-r from-primary to-primary/80 text-white px-8 py-3 text-lg"
          >
            <Rocket className="w-5 h-5 mr-2" />
            Let&apos;s Get Started
          </Button>
          <Button
            onClick={handleSkip}
            variant="outline"
            size="lg"
            className="px-8 py-3"
          >
            Skip Setup for Now
          </Button>
        </motion.div>
      </div>
    </OnboardingLayout>
  )
}
import React from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { OnboardingLayout } from '@/components/onboarding/OnboardingLayout'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Checkbox } from '@/components/ui/checkbox'
import { 
  CheckCircle, 
  Rocket, 
  LayoutDashboard, 
  Settings, 
  FileText, 
  Users, 
  Zap,
  BookOpen,
  MessageCircle,
  Mail,
  Video,
  Trophy,
  ArrowRight,
  Clock
} from 'lucide-react'

export default function Complete() {
  const navigate = useNavigate()

  const handleGenerateArticle = () => {
    navigate('/pipeline/new')
  }

  const handleViewDashboard = () => {
    navigate('/dashboard')
  }

  const handleCustomizeSettings = () => {
    navigate('/settings')
  }

  const setupSummary = [
    { icon: CheckCircle, label: 'Profile', description: 'Content Manager at TechCorp', completed: true },
    { icon: CheckCircle, label: 'API Keys', description: 'Anthropic, Jina AI connected', completed: true },
    { icon: CheckCircle, label: 'WordPress', description: 'blog.techcorp.com connected', completed: true },
    { icon: CheckCircle, label: 'Team', description: '3 invitations sent', completed: true }
  ]

  const nextStepsCards = [
    {
      icon: FileText,
      title: 'Generate Your First Article',
      description: 'Let\'s create your first SEO-optimized article',
      preview: 'Topic suggestions based on your industry',
      action: 'Start First Article',
      time: '~3 minutes',
      onClick: handleGenerateArticle,
      primary: true
    },
    {
      icon: LayoutDashboard,
      title: 'Explore the Dashboard',
      description: 'Take a tour of your new content command center',
      preview: 'Dashboard features overview',
      action: 'View Dashboard',
      time: '~2 minutes',
      onClick: handleViewDashboard
    },
    {
      icon: Settings,
      title: 'Configure Agent Settings',
      description: 'Customize how your AI agents work',
      preview: 'Agent configuration options',
      action: 'Customize Agents',
      time: '~5 minutes',
      onClick: handleCustomizeSettings
    }
  ]

  const checklist = [
    'Generate your first article',
    'Review and publish to WordPress',
    'Invite team members',
    'Set up competitor monitoring',
    'Configure notification preferences'
  ]

  const resources = [
    {
      icon: BookOpen,
      title: 'Documentation & Tutorials',
      description: 'Step-by-step guides and best practices',
      url: '#'
    },
    {
      icon: MessageCircle,
      title: 'Join our Community',
      description: 'Connect with other Blog-Poster users',
      url: '#'
    },
    {
      icon: Mail,
      title: 'Email Support',
      description: 'Get help from our support team',
      url: 'mailto:hello@blog-poster.com'
    },
    {
      icon: Video,
      title: 'Video Walkthrough Series',
      description: 'Watch detailed video tutorials',
      url: '#'
    }
  ]

  return (
    <OnboardingLayout
      currentStep={5}
      totalSteps={5}
      stepName="Setup complete!"
      showSkip={false}
    >
      <div className="space-y-8">
        {/* Celebration Header */}
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5 }}
          className="text-center space-y-4"
        >
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="text-6xl mb-4"
          >
            🎉
          </motion.div>
          <h1 className="text-3xl font-bold text-foreground">
            You&apos;re All Set!
          </h1>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Your Blog-Poster account is ready to generate amazing content. Let&apos;s create something incredible together!
          </p>
          
          {/* Achievement Badge */}
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.4 }}
            className="inline-flex items-center space-x-2 bg-gradient-to-r from-primary to-primary/80 text-white px-6 py-3 rounded-full"
          >
            <Trophy className="w-5 h-5" />
            <span className="font-semibold">Onboarding Complete</span>
          </motion.div>
        </motion.div>

        {/* Setup Summary */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
        >
          <Card>
            <CardHeader>
              <CardTitle>Setup Summary</CardTitle>
              <p className="text-sm text-muted-foreground">Here&apos;s what you&apos;ve configured:</p>
            </CardHeader>
            <CardContent>
              <div className="grid md:grid-cols-2 gap-4">
                {setupSummary.map((item, index) => (
                  <motion.div
                    key={item.label}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.7 + index * 0.1 }}
                    className="flex items-center space-x-3 p-3 border border-border rounded-lg"
                  >
                    <item.icon className="w-5 h-5 text-green-500" />
                    <div>
                      <div className="font-semibold">{item.label}</div>
                      <div className="text-sm text-muted-foreground">{item.description}</div>
                    </div>
                  </motion.div>
                ))}
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* Next Steps */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8 }}
          className="space-y-4"
        >
          <h2 className="text-xl font-semibold text-foreground">What&apos;s Next?</h2>
          <div className="grid gap-4">
            {nextStepsCards.map((card, index) => (
              <motion.div
                key={card.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.9 + index * 0.1 }}
              >
                <Card className={`cursor-pointer transition-all duration-200 hover:shadow-md ${
                  card.primary ? 'border-primary bg-primary/5' : ''
                }`}>
                  <CardContent className="p-6">
                    <div className="flex items-start justify-between">
                      <div className="flex items-start space-x-4 flex-1">
                        <div className={`p-3 rounded-lg ${
                          card.primary 
                            ? 'bg-gradient-to-r from-primary to-primary/80 text-white' 
                            : 'bg-muted'
                        }`}>
                          <card.icon className="w-6 h-6" />
                        </div>
                        <div className="flex-1">
                          <h3 className="font-semibold text-foreground mb-2">
                            {card.title}
                          </h3>
                          <p className="text-sm text-muted-foreground mb-3">
                            {card.description}
                          </p>
                          <p className="text-xs text-muted-foreground mb-4">
                            {card.preview}
                          </p>
                          <div className="flex items-center justify-between">
                            <Button
                              onClick={card.onClick}
                              variant={card.primary ? 'default' : 'outline'}
                              className={card.primary ? 'bg-gradient-to-r from-primary to-primary/80' : ''}
                            >
                              {card.action}
                              <ArrowRight className="w-4 h-4 ml-2" />
                            </Button>
                            <div className="flex items-center space-x-1 text-xs text-muted-foreground">
                              <Clock className="w-3 h-3" />
                              <span>{card.time}</span>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Quick Start Checklist */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.2 }}
        >
          <Card>
            <CardHeader>
              <CardTitle>Quick Start Checklist</CardTitle>
              <p className="text-sm text-muted-foreground">Complete these to get the most from Blog-Poster:</p>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {checklist.map((item, index) => (
                  <div key={item} className="flex items-center space-x-3">
                    <Checkbox id={`checklist-${index}`} />
                    <label 
                      htmlFor={`checklist-${index}`} 
                      className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                    >
                      {item}
                    </label>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* Resources */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.4 }}
        >
          <Card>
            <CardHeader>
              <CardTitle>Need Help? We&apos;ve Got You Covered</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid md:grid-cols-2 gap-4">
                {resources.map((resource, index) => (
                  <a
                    key={resource.title}
                    href={resource.url}
                    className="flex items-start space-x-3 p-3 border border-border rounded-lg hover:border-primary/50 transition-colors"
                  >
                    <resource.icon className="w-5 h-5 text-primary mt-0.5" />
                    <div>
                      <div className="font-semibold text-foreground">{resource.title}</div>
                      <div className="text-sm text-muted-foreground">{resource.description}</div>
                    </div>
                  </a>
                ))}
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* Primary CTA */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.6 }}
          className="text-center pt-6"
        >
          <Button
            onClick={handleGenerateArticle}
            size="lg"
            className="bg-gradient-to-r from-primary to-primary/80 text-white px-8 py-4 text-lg"
          >
            <Rocket className="w-5 h-5 mr-2" />
            Generate My First Article
          </Button>
          <div className="flex items-center justify-center space-x-4 mt-4">
            <Button
              onClick={handleViewDashboard}
              variant="outline"
              size="lg"
            >
              Go to Dashboard
            </Button>
            <Button
              onClick={handleCustomizeSettings}
              variant="ghost"
              size="lg"
              className="text-muted-foreground"
            >
              Customize Settings
            </Button>
          </div>
        </motion.div>
      </div>
    </OnboardingLayout>
  )
}
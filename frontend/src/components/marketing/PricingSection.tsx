import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { CheckCircle, Star, Zap, Crown, Building } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { FadeInSection } from '@/components/ui/AnimatedComponents'

export function PricingSection() {
  const [billingCycle, setBillingCycle] = useState<'monthly' | 'annual'>('monthly')

  const plans = [
    {
      name: 'Free',
      icon: Star,
      price: { monthly: 0, annual: 0 },
      articles: '2 articles/month',
      badge: 'Most Popular for Testing',
      badgeColor: 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300',
      features: [
        'All core features',
        'WordPress publishing',
        'Email support',
        'Basic SEO optimization',
        'Legal fact-checking'
      ],
      cta: 'Start Free',
      ctaVariant: 'outline' as const,
      popular: false
    },
    {
      name: 'Starter',
      icon: Zap,
      price: { monthly: 29, annual: 24 },
      articles: '20 articles/month',
      badge: 'Best for Small Teams',
      badgeColor: 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300',
      features: [
        'Everything in Free',
        'Priority support',
        'Advanced SEO tools',
        'Team collaboration (3 members)',
        'Analytics dashboard',
        'Custom templates'
      ],
      cta: 'Start 14-Day Trial',
      ctaVariant: 'default' as const,
      popular: false
    },
    {
      name: 'Professional',
      icon: Crown,
      price: { monthly: 99, annual: 82 },
      articles: '100 articles/month',
      badge: 'Most Popular',
      badgeColor: 'bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-300',
      features: [
        'Everything in Starter',
        'White-label options',
        'API access',
        'Unlimited team members',
        'Custom AI agents',
        'Advanced analytics',
        'Phone support'
      ],
      cta: 'Start 14-Day Trial',
      ctaVariant: 'default' as const,
      popular: true
    },
    {
      name: 'Enterprise',
      icon: Building,
      price: { monthly: 'Custom', annual: 'Custom' },
      articles: 'Unlimited',
      badge: 'For Large Organizations',
      badgeColor: 'bg-gray-100 text-gray-700 dark:bg-gray-900/30 dark:text-gray-300',
      features: [
        'Everything in Professional',
        'Custom deployment',
        'Dedicated support',
        'Custom integrations',
        'SLA guarantee',
        'Training & onboarding',
        'Custom contracts'
      ],
      cta: 'Contact Sales',
      ctaVariant: 'outline' as const,
      popular: false
    }
  ]

  const calculateSavings = (monthlyPrice: number, annualPrice: number) => {
    if (typeof monthlyPrice !== 'number' || typeof annualPrice !== 'number') return 0
    return Math.round(((monthlyPrice * 12 - annualPrice * 12) / (monthlyPrice * 12)) * 100)
  }

  return (
    <section id="pricing" className="py-20 bg-white dark:bg-gray-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <FadeInSection>
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
              Simple, Transparent Pricing
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto mb-8">
              Use your own API keys - no hidden AI costs. Scale with confidence as your content needs grow.
            </p>

            {/* Billing Toggle */}
            <div className="flex items-center justify-center space-x-4">
              <span className={`text-sm font-medium ${billingCycle === 'monthly' ? 'text-gray-900 dark:text-white' : 'text-gray-500'}`}>
                Monthly
              </span>
              <motion.button
                className="relative inline-flex h-6 w-11 items-center rounded-full bg-gray-200 dark:bg-gray-700 transition-colors"
                onClick={() => setBillingCycle(billingCycle === 'monthly' ? 'annual' : 'monthly')}
                whileTap={{ scale: 0.95 }}
              >
                <motion.span
                  className="inline-block h-4 w-4 transform rounded-full bg-purple-gradient shadow-lg"
                  animate={{ x: billingCycle === 'annual' ? 24 : 4 }}
                  transition={{ type: "spring", stiffness: 300, damping: 30 }}
                />
              </motion.button>
              <span className={`text-sm font-medium ${billingCycle === 'annual' ? 'text-gray-900 dark:text-white' : 'text-gray-500'}`}>
                Annual
              </span>
              {billingCycle === 'annual' && (
                <motion.span
                  className="text-sm text-green-600 dark:text-green-400 font-medium"
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                >
                  Save up to 20%
                </motion.span>
              )}
            </div>
          </div>
        </FadeInSection>

        {/* Pricing Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {plans.map((plan, index) => {
            const Icon = plan.icon
            const currentPrice = plan.price[billingCycle]
            const savings = typeof currentPrice === 'number' && typeof plan.price.monthly === 'number' 
              ? calculateSavings(plan.price.monthly, currentPrice)
              : 0
            
            return (
              <motion.div
                key={plan.name}
                className={`relative bg-white dark:bg-gray-800 rounded-2xl border-2 transition-all duration-300 ${
                  plan.popular 
                    ? 'border-purple-500 shadow-2xl shadow-purple-500/20 scale-105' 
                    : 'border-gray-200 dark:border-gray-700 shadow-lg hover:shadow-xl'
                }`}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                whileHover={{ 
                  y: plan.popular ? -5 : -10,
                  transition: { duration: 0.3 }
                }}
              >
                {/* Popular Badge */}
                {plan.popular && (
                  <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                    <div className="bg-purple-gradient text-white px-4 py-1 rounded-full text-sm font-medium">
                      Most Popular
                    </div>
                  </div>
                )}

                <div className="p-8">
                  {/* Header */}
                  <div className="text-center mb-8">
                    <div className={`w-12 h-12 rounded-xl bg-gradient-to-r ${
                      plan.popular ? 'from-purple-500 to-purple-600' : 'from-gray-400 to-gray-500'
                    } flex items-center justify-center mx-auto mb-4`}>
                      <Icon className="w-6 h-6 text-white" />
                    </div>
                    
                    <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">
                      {plan.name}
                    </h3>
                    
                    <div className="mb-4">
                      <div className="flex items-baseline justify-center">
                        {typeof currentPrice === 'number' ? (
                          <>
                            <span className="text-4xl font-bold text-gray-900 dark:text-white">
                              ${currentPrice}
                            </span>
                            <span className="text-gray-500 ml-1">
                              /{billingCycle === 'monthly' ? 'mo' : 'yr'}
                            </span>
                          </>
                        ) : (
                          <span className="text-4xl font-bold text-gray-900 dark:text-white">
                            {currentPrice}
                          </span>
                        )}
                      </div>
                      
                      {billingCycle === 'annual' && savings > 0 && (
                        <motion.div
                          className="text-green-600 dark:text-green-400 text-sm font-medium mt-1"
                          initial={{ opacity: 0 }}
                          animate={{ opacity: 1 }}
                        >
                          Save {savings}% annually
                        </motion.div>
                      )}
                    </div>
                    
                    <div className="text-gray-600 dark:text-gray-400 font-medium mb-4">
                      {plan.articles}
                    </div>
                    
                    <div className={`inline-block px-3 py-1 rounded-full text-xs font-medium ${plan.badgeColor}`}>
                      {plan.badge}
                    </div>
                  </div>

                  {/* Features */}
                  <div className="space-y-4 mb-8">
                    {plan.features.map((feature, featureIndex) => (
                      <motion.div
                        key={feature}
                        className="flex items-start space-x-3"
                        initial={{ opacity: 0, x: -10 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: index * 0.1 + featureIndex * 0.05 }}
                      >
                        <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" />
                        <span className="text-gray-600 dark:text-gray-400 text-sm">
                          {feature}
                        </span>
                      </motion.div>
                    ))}
                  </div>

                  {/* CTA Button */}
                  <Button
                    variant={plan.ctaVariant}
                    className={`w-full ${
                      plan.popular 
                        ? 'bg-purple-gradient text-white hover:opacity-90' 
                        : ''
                    }`}
                  >
                    {plan.cta}
                  </Button>
                </div>
              </motion.div>
            )
          })}
        </div>

        {/* Bottom Notes */}
        <FadeInSection delay={0.6}>
          <div className="mt-16 text-center space-y-4">
            <div className="flex flex-wrap justify-center gap-8 text-sm text-gray-600 dark:text-gray-400">
              <div className="flex items-center space-x-2">
                <CheckCircle className="w-4 h-4 text-green-500" />
                <span>14-day money-back guarantee</span>
              </div>
              <div className="flex items-center space-x-2">
                <CheckCircle className="w-4 h-4 text-green-500" />
                <span>Bring your own API keys</span>
              </div>
              <div className="flex items-center space-x-2">
                <CheckCircle className="w-4 h-4 text-green-500" />
                <span>No setup or cancellation fees</span>
              </div>
            </div>
            
            <p className="text-gray-500 dark:text-gray-400">
              All plans include access to Anthropic, OpenAI, and Jina API integrations. 
              API costs are separate and billed directly by providers.
            </p>
          </div>
        </FadeInSection>
      </div>
    </section>
  )
}
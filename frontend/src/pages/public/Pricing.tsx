import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { Check, X, Star, Shield, Zap, Users, ArrowRight, Calculator } from 'lucide-react'
import { Link } from 'react-router-dom'

export default function Pricing() {
  const [isAnnual, setIsAnnual] = useState(false)
  const [calculatorArticles, setCalculatorArticles] = useState(50)
  const [calculatorTeam, setCalculatorTeam] = useState(5)

  const plans = [
    {
      name: 'FREE',
      subtitle: 'Perfect for testing',
      price: { monthly: 0, annual: 0 },
      articles: '2 articles/month',
      badge: 'Most Popular for Testing',
      features: [
        'All 5 AI agents',
        'WordPress publishing',
        'SEO optimization',
        'Legal fact-checking',
        'Email support'
      ],
      limitations: [
        'Team collaboration',
        'Advanced analytics',
        'Priority support'
      ],
      cta: 'Get Started Free',
      ctaSubtext: 'No credit card required',
      popular: false
    },
    {
      name: 'STARTER',
      subtitle: 'Best for small teams',
      price: { monthly: 29, annual: 24 },
      articles: '20 articles/month',
      badge: 'Most Popular',
      features: [
        'Everything in Free',
        'Team collaboration (5 members)',
        'Priority email support',
        'Advanced SEO analytics',
        'Custom WordPress templates',
        'Bulk content operations'
      ],
      limitations: [
        'White-label options',
        'API access'
      ],
      cta: 'Start 14-Day Trial',
      ctaSubtext: 'Most popular for small teams',
      popular: true
    },
    {
      name: 'PROFESSIONAL',
      subtitle: 'Perfect for agencies',
      price: { monthly: 99, annual: 85 },
      articles: '100 articles/month',
      badge: 'Best Value',
      features: [
        'Everything in Starter',
        'Unlimited team members',
        'White-label options',
        'API access & webhooks',
        'Advanced analytics',
        'Priority chat support',
        'Custom agent training',
        'Multiple WordPress sites'
      ],
      limitations: [],
      cta: 'Start 14-Day Trial',
      ctaSubtext: 'Perfect for agencies and growing teams',
      popular: false
    },
    {
      name: 'ENTERPRISE',
      subtitle: 'For large organizations',
      price: { monthly: 'Custom', annual: 'Custom' },
      articles: 'Unlimited articles',
      badge: 'Contact Sales',
      features: [
        'Everything in Professional',
        'Custom deployment options',
        'Dedicated account manager',
        'SLA guarantees (99.9% uptime)',
        'Custom integrations',
        'Advanced security features',
        'Training and onboarding',
        '24/7 phone support'
      ],
      limitations: [],
      cta: 'Contact Sales Team',
      ctaSubtext: 'For large organizations and enterprises',
      popular: false
    }
  ]

  const faqs = [
    {
      question: 'What happens when I exceed my article limit?',
      answer: "We'll notify you when you approach your limit. You can upgrade your plan or purchase additional articles at $2.50 each."
    },
    {
      question: 'Can I change plans anytime?',
      answer: "Yes! You can upgrade or downgrade your plan at any time. Changes take effect immediately, and we'll prorate billing accordingly."
    },
    {
      question: 'How does billing work with annual plans?',
      answer: 'Annual plans are billed upfront with a 20% discount. You can switch to monthly billing at any time during your subscription.'
    },
    {
      question: 'What are the actual AI costs I will pay?',
      answer: 'You provide your own API keys for Claude, GPT-4, and Jina AI. Typical cost is $0.15-0.30 per article depending on length and complexity.'
    },
    {
      question: 'Do you offer education or non-profit discounts?',
      answer: 'Yes! We offer 50% discounts for educational institutions and qualifying non-profits. Contact sales for details.'
    },
    {
      question: 'What payment methods do you accept?',
      answer: 'We accept all major credit cards, PayPal, and wire transfers for Enterprise plans. All payments are processed securely by Stripe.'
    }
  ]

  const calculateSavings = () => {
    const manualCost = calculatorArticles * 150 // $150 per article manual
    const teamCost = calculatorTeam * 5000 // $5000 per team member monthly
    const totalManual = manualCost + teamCost
    
    const blogPosterCost = calculatorArticles <= 20 ? 29 : calculatorArticles <= 100 ? 99 : 299
    const aiCost = calculatorArticles * 0.25 // $0.25 per article AI cost
    const totalBlogPoster = blogPosterCost + aiCost
    
    return {
      manual: totalManual,
      blogPoster: totalBlogPoster,
      savings: totalManual - totalBlogPoster,
      percentage: Math.round(((totalManual - totalBlogPoster) / totalManual) * 100)
    }
  }

  const savings = calculateSavings()

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <section className="pt-20 pb-16 bg-white dark:bg-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <h1 className="text-4xl md:text-6xl font-bold text-gray-900 dark:text-white mb-6">
              Simple, Transparent Pricing
            </h1>
            <p className="text-xl text-gray-600 dark:text-gray-400 mb-8 max-w-3xl mx-auto">
              Pay for what you use. Scale as you grow. No hidden fees.
              Use your own API keys - no markup on AI costs.
            </p>
            
            {/* Trust indicators */}
            <div className="flex flex-wrap justify-center items-center gap-6 text-sm text-gray-600 dark:text-gray-400">
              <div className="flex items-center space-x-2">
                <Shield className="w-5 h-5 text-green-500" />
                <span>14-day free trial on all paid plans</span>
              </div>
              <div className="flex items-center space-x-2">
                <Zap className="w-5 h-5 text-blue-500" />
                <span>No setup fees, cancel anytime</span>
              </div>
              <div className="flex items-center space-x-2">
                <Users className="w-5 h-5 text-purple-500" />
                <span>Used by 500+ content teams</span>
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Billing Toggle */}
      <section className="py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-center items-center space-x-4 mb-12">
            <span className={`text-lg ${!isAnnual ? 'text-gray-900 dark:text-white font-semibold' : 'text-gray-600 dark:text-gray-400'}`}>
              Monthly
            </span>
            <motion.button
              className={`relative w-16 h-8 rounded-full ${isAnnual ? 'bg-purple-gradient' : 'bg-gray-300 dark:bg-gray-600'}`}
              onClick={() => setIsAnnual(!isAnnual)}
              whileTap={{ scale: 0.95 }}
            >
              <motion.div
                className="absolute top-1 left-1 w-6 h-6 bg-white rounded-full shadow-lg"
                animate={{ x: isAnnual ? 32 : 0 }}
                transition={{ type: 'spring', stiffness: 500, damping: 30 }}
              />
            </motion.button>
            <span className={`text-lg ${isAnnual ? 'text-gray-900 dark:text-white font-semibold' : 'text-gray-600 dark:text-gray-400'}`}>
              Annual
            </span>
            {isAnnual && (
              <motion.span
                className="bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200 px-3 py-1 rounded-full text-sm font-medium"
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
              >
                Save 20%
              </motion.span>
            )}
          </div>
        </div>
      </section>

      {/* Pricing Cards */}
      <section className="pb-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {plans.map((plan, index) => (
              <motion.div
                key={plan.name}
                className={`relative bg-white dark:bg-gray-800 rounded-2xl shadow-lg border-2 p-8 ${
                  plan.popular 
                    ? 'border-purple-500 ring-2 ring-purple-200 dark:ring-purple-800' 
                    : 'border-gray-200 dark:border-gray-700'
                }`}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                whileHover={{ y: -5 }}
              >
                {plan.popular && (
                  <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                    <span className="bg-purple-gradient text-white px-4 py-2 rounded-full text-sm font-semibold flex items-center space-x-1">
                      <Star className="w-4 h-4" />
                      <span>{plan.badge}</span>
                    </span>
                  </div>
                )}

                <div className="text-center">
                  <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                    {plan.name}
                  </h3>
                  <p className="text-gray-600 dark:text-gray-400 mb-4">{plan.subtitle}</p>
                  
                  <div className="mb-6">
                    {typeof plan.price.monthly === 'number' ? (
                      <div>
                        <span className="text-5xl font-bold text-gray-900 dark:text-white">
                          ${isAnnual ? plan.price.annual : plan.price.monthly}
                        </span>
                        <span className="text-gray-600 dark:text-gray-400">/month</span>
                        {isAnnual && plan.price.monthly > 0 && (
                          <div className="text-sm text-gray-500 dark:text-gray-400 line-through">
                            ${plan.price.monthly}/month billed monthly
                          </div>
                        )}
                      </div>
                    ) : (
                      <span className="text-3xl font-bold text-gray-900 dark:text-white">
                        {plan.price.monthly}
                      </span>
                    )}
                  </div>

                  <p className="text-lg text-purple-600 dark:text-purple-400 font-semibold mb-6">
                    {plan.articles}
                  </p>

                  <motion.button
                    className={`w-full py-3 px-6 rounded-lg font-semibold mb-6 ${
                      plan.popular 
                        ? 'bg-purple-gradient text-white' 
                        : 'border-2 border-purple-500 text-purple-600 hover:bg-purple-50 dark:hover:bg-purple-900/20'
                    }`}
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                  >
                    {plan.cta}
                  </motion.button>

                  <p className="text-sm text-gray-600 dark:text-gray-400 mb-8">
                    {plan.ctaSubtext}
                  </p>
                </div>

                <div className="space-y-3">
                  {plan.features.map((feature, idx) => (
                    <div key={idx} className="flex items-center space-x-3">
                      <Check className="w-5 h-5 text-green-500 flex-shrink-0" />
                      <span className="text-gray-700 dark:text-gray-300">{feature}</span>
                    </div>
                  ))}
                  {plan.limitations.map((limitation, idx) => (
                    <div key={idx} className="flex items-center space-x-3 opacity-60">
                      <X className="w-5 h-5 text-gray-400 flex-shrink-0" />
                      <span className="text-gray-600 dark:text-gray-400">{limitation}</span>
                    </div>
                  ))}
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Cost Calculator */}
      <section className="py-20 bg-white dark:bg-gray-800">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-12"
          >
            <Calculator className="w-12 h-12 text-purple-500 mx-auto mb-4" />
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
              Calculate Your Savings
            </h2>
            <p className="text-gray-600 dark:text-gray-400">
              See how much you can save compared to manual content creation
            </p>
          </motion.div>

          <div className="bg-gray-50 dark:bg-gray-900 rounded-2xl p-8">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Articles per month
                </label>
                <input
                  type="range"
                  min="1"
                  max="200"
                  value={calculatorArticles}
                  onChange={(e) => setCalculatorArticles(Number(e.target.value))}
                  className="w-full"
                />
                <div className="text-center text-2xl font-bold text-purple-600 mt-2">
                  {calculatorArticles} articles
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Team size
                </label>
                <input
                  type="range"
                  min="1"
                  max="20"
                  value={calculatorTeam}
                  onChange={(e) => setCalculatorTeam(Number(e.target.value))}
                  className="w-full"
                />
                <div className="text-center text-2xl font-bold text-purple-600 mt-2">
                  {calculatorTeam} people
                </div>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-center">
              <div className="bg-red-50 dark:bg-red-900/20 p-6 rounded-xl">
                <h3 className="text-lg font-semibold text-red-700 dark:text-red-300 mb-2">
                  Manual Creation
                </h3>
                <div className="text-3xl font-bold text-red-600 dark:text-red-400">
                  ${savings.manual.toLocaleString()}
                </div>
                <p className="text-sm text-red-600 dark:text-red-400 mt-1">per month</p>
              </div>

              <div className="bg-green-50 dark:bg-green-900/20 p-6 rounded-xl">
                <h3 className="text-lg font-semibold text-green-700 dark:text-green-300 mb-2">
                  Blog-Poster
                </h3>
                <div className="text-3xl font-bold text-green-600 dark:text-green-400">
                  ${savings.blogPoster.toLocaleString()}
                </div>
                <p className="text-sm text-green-600 dark:text-green-400 mt-1">per month</p>
              </div>

              <div className="bg-purple-50 dark:bg-purple-900/20 p-6 rounded-xl">
                <h3 className="text-lg font-semibold text-purple-700 dark:text-purple-300 mb-2">
                  You Save
                </h3>
                <div className="text-3xl font-bold text-purple-600 dark:text-purple-400">
                  {savings.percentage}%
                </div>
                <p className="text-sm text-purple-600 dark:text-purple-400 mt-1">
                  ${savings.savings.toLocaleString()}/month
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* FAQ */}
      <section className="py-20">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-12"
          >
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
              Frequently Asked Questions
            </h2>
            <p className="text-gray-600 dark:text-gray-400">
              Everything you need to know about our pricing
            </p>
          </motion.div>

          <div className="space-y-6">
            {faqs.map((faq, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-lg"
              >
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                  {faq.question}
                </h3>
                <p className="text-gray-600 dark:text-gray-400">
                  {faq.answer}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="py-20 bg-purple-gradient">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-white">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <h2 className="text-3xl md:text-4xl font-bold mb-6">
              Ready to Scale Your Content?
            </h2>
            <p className="text-xl mb-8 opacity-90">
              Join 500+ content teams generating SEO articles on autopilot
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/signup"
                className="px-8 py-4 bg-white text-purple-600 rounded-lg font-semibold hover:bg-gray-100 transition-colors inline-flex items-center justify-center space-x-2"
              >
                <span>Start Your Free Trial</span>
                <ArrowRight className="w-5 h-5" />
              </Link>
              <Link
                to="/contact"
                className="px-8 py-4 border-2 border-white text-white rounded-lg font-semibold hover:bg-white hover:text-purple-600 transition-colors"
              >
                Schedule a Demo
              </Link>
            </div>
            
            <p className="text-sm mt-4 opacity-75">
              No credit card required • 14-day money-back guarantee
            </p>
          </motion.div>
        </div>
      </section>
    </div>
  )
}
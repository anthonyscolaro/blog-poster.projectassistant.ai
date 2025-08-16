import React from 'react'
import { motion } from 'framer-motion'
import { ArrowRight, CheckCircle, Shield, Clock, Users } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { FadeInSection } from '@/components/ui/AnimatedComponents'

export function FinalCTASection() {
  const securityBadges = [
    { icon: Shield, label: 'SOC 2 Compliant' },
    { icon: CheckCircle, label: 'GDPR Ready' },
    { icon: Clock, label: '99.9% Uptime' },
    { icon: Users, label: '500+ Customers' }
  ]

  const benefits = [
    'Generate your first 2 articles completely free',
    'No credit card required to start',
    '14-day money-back guarantee on all paid plans',
    'Full access to all 5 AI agents',
    'WordPress integration included',
    'Email support from day one'
  ]

  return (
    <section className="relative py-20 bg-gradient-to-br from-purple-600 via-purple-700 to-indigo-800 overflow-hidden">
      {/* Background Elements */}
      <div className="absolute inset-0">
        <motion.div
          className="absolute top-20 left-10 w-40 h-40 bg-white/10 rounded-full blur-xl"
          animate={{
            scale: [1, 1.2, 1],
            rotate: [0, 180, 360]
          }}
          transition={{
            duration: 10,
            repeat: Infinity,
            ease: "linear"
          }}
        />
        <motion.div
          className="absolute bottom-20 right-10 w-32 h-32 bg-indigo-300/20 rounded-full blur-lg"
          animate={{
            scale: [1.2, 1, 1.2],
            x: [0, 30, 0]
          }}
          transition={{
            duration: 8,
            repeat: Infinity,
            ease: "easeInOut"
          }}
        />
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <FadeInSection>
          <div className="text-center mb-12">
            <motion.h2 
              className="text-4xl md:text-5xl lg:text-6xl font-bold text-white mb-6"
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
            >
              Ready to Scale Your Content?
            </motion.h2>
            
            <motion.p 
              className="text-xl md:text-2xl text-white/90 max-w-3xl mx-auto mb-8"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
            >
              Join 500+ content teams generating SEO articles on autopilot. 
              Start free and experience the power of AI-driven content creation.
            </motion.p>
          </div>
        </FadeInSection>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          {/* Left Side - Benefits */}
          <FadeInSection delay={0.4}>
            <div className="space-y-6">
              <h3 className="text-2xl font-bold text-white mb-6">
                What you get when you start today:
              </h3>
              
              <div className="space-y-4">
                {benefits.map((benefit, index) => (
                  <motion.div
                    key={benefit}
                    className="flex items-start space-x-3"
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.6 + index * 0.1 }}
                  >
                    <CheckCircle className="w-6 h-6 text-green-400 flex-shrink-0 mt-0.5" />
                    <span className="text-white/90 text-lg">{benefit}</span>
                  </motion.div>
                ))}
              </div>
            </div>
          </FadeInSection>

          {/* Right Side - CTA Form */}
          <FadeInSection delay={0.6}>
            <div className="bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/20">
              <div className="text-center mb-8">
                <h3 className="text-2xl font-bold text-white mb-4">
                  Start Your Free Trial Now
                </h3>
                <p className="text-white/80">
                  No commitment. Cancel anytime. Start generating content in under 5 minutes.
                </p>
              </div>

              {/* CTA Buttons */}
              <div className="space-y-4 mb-8">
                <motion.button
                  className="w-full px-8 py-4 bg-white text-purple-700 rounded-lg text-lg font-semibold shadow-xl hover:shadow-2xl transition-all duration-300 flex items-center justify-center space-x-3 group"
                  whileHover={{ 
                    scale: 1.02,
                    boxShadow: "0 25px 50px rgba(255, 255, 255, 0.3)"
                  }}
                  whileTap={{ scale: 0.98 }}
                >
                  <span>Start Free Trial - 2 Articles Free</span>
                  <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                </motion.button>

                <div className="text-center">
                  <span className="text-white/80 text-sm">
                    No credit card required • 14-day money-back guarantee
                  </span>
                </div>
              </div>

              {/* Trial Information */}
              <div className="bg-white/5 rounded-lg p-4 border border-white/10">
                <div className="text-white/90 text-sm space-y-2">
                  <div className="flex items-center justify-between">
                    <span>Free articles included:</span>
                    <span className="font-semibold">2 articles</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span>Setup time:</span>
                    <span className="font-semibold">Under 5 minutes</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span>Credit card required:</span>
                    <span className="font-semibold text-green-400">No</span>
                  </div>
                </div>
              </div>
            </div>
          </FadeInSection>
        </div>

        {/* Security Badges */}
        <FadeInSection delay={0.8}>
          <div className="mt-16 text-center">
            <p className="text-white/80 mb-8 text-lg">
              Trusted by enterprise customers worldwide
            </p>
            
            <div className="flex flex-wrap justify-center items-center gap-8">
              {securityBadges.map((badge, index) => {
                const Icon = badge.icon
                return (
                  <motion.div
                    key={badge.label}
                    className="flex items-center space-x-3 text-white/80 hover:text-white transition-colors"
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: 1 + index * 0.1 }}
                    whileHover={{ scale: 1.05 }}
                  >
                    <Icon className="w-5 h-5" />
                    <span className="font-medium">{badge.label}</span>
                  </motion.div>
                )
              })}
            </div>
          </div>
        </FadeInSection>

        {/* Final Trust Statement */}
        <FadeInSection delay={1.2}>
          <div className="mt-12 text-center">
            <motion.div
              className="inline-flex items-center space-x-2 bg-white/10 backdrop-blur-sm rounded-full px-6 py-3 border border-white/20"
              whileHover={{ scale: 1.05 }}
            >
              <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
              <span className="text-white/90 text-sm font-medium">
                47 people started their free trial in the last 24 hours
              </span>
            </motion.div>
          </div>
        </FadeInSection>
      </div>
    </section>
  )
}
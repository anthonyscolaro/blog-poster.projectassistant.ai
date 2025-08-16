import React from 'react'
import { motion } from 'framer-motion'
import { AnimatedCounter, FadeInSection } from '@/components/ui/AnimatedComponents'

export function SocialProofSection() {
  // Mock company logos - in real implementation, these would be actual client logos
  const companyLogos = [
    { name: 'TechFlow', logo: 'TF' },
    { name: 'GrowthCorp', logo: 'GC' },
    { name: 'ContentPro', logo: 'CP' },
    { name: 'SEOMax', logo: 'SM' },
    { name: 'MarketBuzz', logo: 'MB' },
    { name: 'WriteWell', logo: 'WW' },
    { name: 'BlogBoost', logo: 'BB' },
    { name: 'RankHigh', logo: 'RH' }
  ]

  const metrics = [
    { value: 10847, suffix: '+', label: 'Articles Generated' },
    { value: 94, suffix: '%', label: 'Average SEO Score' },
    { value: 5, suffix: 'x', label: 'Faster Than Manual Writing' }
  ]

  return (
    <section className="py-16 bg-gray-50 dark:bg-gray-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <FadeInSection>
          <div className="text-center mb-12">
            <h2 className="text-2xl md:text-3xl font-bold text-gray-900 dark:text-white mb-4">
              Trusted by Content Teams Worldwide
            </h2>
            <p className="text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
              Join hundreds of marketing teams, agencies, and businesses that have transformed 
              their content strategy with our AI-powered platform.
            </p>
          </div>
        </FadeInSection>

        {/* Company Logos */}
        <FadeInSection delay={0.2}>
          <div className="mb-16">
            <div className="flex flex-wrap justify-center items-center gap-8 md:gap-12">
              {companyLogos.map((company, index) => (
                <motion.div
                  key={company.name}
                  className="flex items-center justify-center"
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: index * 0.1 }}
                  whileHover={{ scale: 1.1 }}
                >
                  <div className="flex items-center space-x-3 group">
                    <div className="w-10 h-10 bg-gradient-to-br from-gray-200 to-gray-300 dark:from-gray-700 dark:to-gray-800 rounded-lg flex items-center justify-center group-hover:from-purple-200 group-hover:to-purple-300 dark:group-hover:from-purple-800 dark:group-hover:to-purple-900 transition-all duration-300">
                      <span className="text-gray-600 dark:text-gray-300 font-bold text-sm group-hover:text-purple-700 dark:group-hover:text-purple-200">
                        {company.logo}
                      </span>
                    </div>
                    <span className="text-gray-500 dark:text-gray-400 font-medium group-hover:text-gray-700 dark:group-hover:text-gray-200 transition-colors duration-300">
                      {company.name}
                    </span>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </FadeInSection>

        {/* Key Metrics */}
        <FadeInSection delay={0.4}>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
            {metrics.map((metric, index) => (
              <motion.div
                key={metric.label}
                className="bg-white dark:bg-gray-800 rounded-2xl p-8 shadow-lg border border-gray-200 dark:border-gray-700"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.6 + index * 0.1 }}
                whileHover={{ 
                  y: -5,
                  boxShadow: "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)"
                }}
              >
                <div className="text-4xl md:text-5xl font-bold text-purple-600 dark:text-purple-400 mb-2">
                  <AnimatedCounter 
                    value={metric.value} 
                    suffix={metric.suffix}
                    duration={2}
                  />
                </div>
                <p className="text-gray-600 dark:text-gray-400 font-medium">
                  {metric.label}
                </p>
              </motion.div>
            ))}
          </div>
        </FadeInSection>

        {/* Additional Trust Indicators */}
        <FadeInSection delay={0.8}>
          <div className="mt-16 text-center">
            <div className="inline-flex items-center space-x-8 text-sm text-gray-500 dark:text-gray-400">
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                <span>SOC 2 Compliant</span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                <span>GDPR Ready</span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                <span>99.9% Uptime</span>
              </div>
            </div>
          </div>
        </FadeInSection>
      </div>
    </section>
  )
}
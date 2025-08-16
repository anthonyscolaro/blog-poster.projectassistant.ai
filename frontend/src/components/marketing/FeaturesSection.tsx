import React from 'react'
import { motion } from 'framer-motion'
import { 
  Search, 
  Shield, 
  Bot, 
  Globe, 
  DollarSign, 
  Users,
  CheckCircle,
  ArrowRight
} from 'lucide-react'
import { FadeInSection, StaggerContainer } from '@/components/ui/AnimatedComponents'

export function FeaturesSection() {
  const features = [
    {
      icon: Search,
      title: 'SEO Optimization',
      description: 'Complete title tags, meta descriptions, schema markup, and internal linking strategies.',
      highlights: ['Title & Meta Tags', 'Schema Markup', 'Internal Linking', 'Keyword Optimization'],
      color: 'from-blue-500 to-blue-600'
    },
    {
      icon: Shield,
      title: 'Legal Compliance',
      description: 'ADA compliance fact-checking with proper citations and claim verification.',
      highlights: ['Fact Verification', 'ADA Compliance', 'Citation Sources', 'Legal Review'],
      color: 'from-red-500 to-red-600'
    },
    {
      icon: Bot,
      title: 'Multi-Agent Pipeline',
      description: '5 specialized AI agents working together for comprehensive content creation.',
      highlights: ['Competitor Analysis', 'Topic Research', 'Content Generation', 'Quality Assurance'],
      color: 'from-purple-500 to-purple-600'
    },
    {
      icon: Globe,
      title: 'WordPress Integration',
      description: 'Direct publishing with perfect formatting, image optimization, and SEO setup.',
      highlights: ['Auto Publishing', 'Image Optimization', 'Format Preservation', 'SEO Tags'],
      color: 'from-green-500 to-green-600'
    },
    {
      icon: DollarSign,
      title: 'Cost Tracking',
      description: 'Monitor AI usage and stay within budget with transparent cost reporting.',
      highlights: ['Usage Analytics', 'Budget Alerts', 'Cost Breakdown', 'ROI Tracking'],
      color: 'from-yellow-500 to-yellow-600'
    },
    {
      icon: Users,
      title: 'Team Collaboration',
      description: 'Invite team members with role-based access and workflow management.',
      highlights: ['Role Management', 'Team Workflows', 'Review Process', 'Access Control'],
      color: 'from-indigo-500 to-indigo-600'
    }
  ]

  return (
    <section className="py-20 bg-gray-50 dark:bg-gray-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <FadeInSection>
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
              Everything You Need for Content Success
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
              From research to publishing, our comprehensive platform handles every aspect 
              of professional content creation with enterprise-grade features.
            </p>
          </div>
        </FadeInSection>

        <StaggerContainer className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => {
            const Icon = feature.icon
            
            return (
              <motion.div
                key={feature.title}
                className="group bg-white dark:bg-gray-800 rounded-2xl p-8 shadow-lg border border-gray-200 dark:border-gray-700 hover:shadow-xl transition-all duration-300"
                whileHover={{ 
                  y: -8,
                  transition: { duration: 0.3 }
                }}
              >
                {/* Icon */}
                <motion.div 
                  className={`w-16 h-16 bg-gradient-to-r ${feature.color} rounded-2xl flex items-center justify-center mb-6`}
                  whileHover={{ 
                    rotate: 5,
                    scale: 1.1
                  }}
                  transition={{ duration: 0.3 }}
                >
                  <Icon className="w-8 h-8 text-white" />
                </motion.div>

                {/* Content */}
                <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4 group-hover:text-purple-600 dark:group-hover:text-purple-400 transition-colors">
                  {feature.title}
                </h3>
                
                <p className="text-gray-600 dark:text-gray-400 mb-6 leading-relaxed">
                  {feature.description}
                </p>

                {/* Feature Highlights */}
                <div className="space-y-2 mb-6">
                  {feature.highlights.map((highlight, highlightIndex) => (
                    <motion.div
                      key={highlight}
                      className="flex items-center space-x-3"
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: index * 0.1 + highlightIndex * 0.05 }}
                    >
                      <CheckCircle className="w-4 h-4 text-green-500 flex-shrink-0" />
                      <span className="text-sm text-gray-600 dark:text-gray-400">
                        {highlight}
                      </span>
                    </motion.div>
                  ))}
                </div>

                {/* Learn More Link */}
                <motion.button
                  className="flex items-center space-x-2 text-purple-600 dark:text-purple-400 font-medium text-sm group-hover:text-purple-700 dark:group-hover:text-purple-300 transition-colors"
                  whileHover={{ x: 5 }}
                  transition={{ duration: 0.2 }}
                >
                  <span>Learn More</span>
                  <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                </motion.button>
              </motion.div>
            )
          })}
        </StaggerContainer>

        {/* Feature Showcase Visual */}
        <FadeInSection delay={0.6}>
          <div className="mt-20">
            <div className="bg-white dark:bg-gray-800 rounded-3xl p-8 shadow-2xl border border-gray-200 dark:border-gray-700">
              <div className="text-center mb-8">
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                  See It All Working Together
                </h3>
                <p className="text-gray-600 dark:text-gray-400">
                  Watch how our features combine to create the perfect content workflow
                </p>
              </div>

              {/* Mock Dashboard Interface */}
              <div className="bg-gray-50 dark:bg-gray-900 rounded-2xl p-6 border border-gray-200 dark:border-gray-700">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {/* SEO Panel */}
                  <div className="bg-white dark:bg-gray-800 p-4 rounded-lg border border-green-200 dark:border-green-800">
                    <div className="flex items-center space-x-2 mb-3">
                      <Search className="w-5 h-5 text-green-500" />
                      <span className="font-medium text-gray-900 dark:text-white">SEO Score</span>
                    </div>
                    <div className="text-2xl font-bold text-green-600">96/100</div>
                    <div className="text-sm text-gray-600 dark:text-gray-400">Excellent optimization</div>
                  </div>

                  {/* Compliance Panel */}
                  <div className="bg-white dark:bg-gray-800 p-4 rounded-lg border border-blue-200 dark:border-blue-800">
                    <div className="flex items-center space-x-2 mb-3">
                      <Shield className="w-5 h-5 text-blue-500" />
                      <span className="font-medium text-gray-900 dark:text-white">Compliance</span>
                    </div>
                    <div className="text-2xl font-bold text-blue-600">✓ Verified</div>
                    <div className="text-sm text-gray-600 dark:text-gray-400">12 facts checked</div>
                  </div>

                  {/* Team Panel */}
                  <div className="bg-white dark:bg-gray-800 p-4 rounded-lg border border-purple-200 dark:border-purple-800">
                    <div className="flex items-center space-x-2 mb-3">
                      <Users className="w-5 h-5 text-purple-500" />
                      <span className="font-medium text-gray-900 dark:text-white">Team Status</span>
                    </div>
                    <div className="text-2xl font-bold text-purple-600">5 Active</div>
                    <div className="text-sm text-gray-600 dark:text-gray-400">Contributors online</div>
                  </div>
                </div>

                {/* Progress Bar */}
                <div className="mt-6">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium text-gray-900 dark:text-white">Article Pipeline</span>
                    <span className="text-sm text-gray-600 dark:text-gray-400">4/5 Complete</span>
                  </div>
                  <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                    <motion.div 
                      className="bg-purple-gradient h-2 rounded-full"
                      initial={{ width: 0 }}
                      animate={{ width: '80%' }}
                      transition={{ duration: 2, ease: "easeOut" }}
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </FadeInSection>
      </div>
    </section>
  )
}
import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  Search, 
  Brain, 
  PenTool, 
  Shield, 
  Globe, 
  Users,
  BarChart3,
  Zap,
  CheckCircle,
  ArrowRight,
  Play,
  Star,
  Clock,
  Target,
  Workflow
} from 'lucide-react'
import { Link } from 'react-router-dom'

export default function Features() {
  const [activeAgent, setActiveAgent] = useState(0)

  const agents = [
    {
      icon: Search,
      name: 'Competitor Monitor',
      title: 'Stay Ahead of Your Competition',
      description: 'Automatically monitors competitor content, identifies gaps, and finds opportunities in your industry.',
      benefits: [
        'Real-time competitor content analysis',
        'Identify content gaps and opportunities',
        'Track industry trends and keywords',
        'Competitive SEO insights'
      ],
      technical: 'Powered by Jina AI for accurate web scraping',
      color: 'from-blue-500 to-blue-600',
      demo: 'Analyzing 50+ competitors in your industry...'
    },
    {
      icon: Brain,
      name: 'Topic Analyzer',
      title: 'Discover High-Value Content Topics',
      description: 'AI-powered topic research that identifies the best keywords and content opportunities for your audience.',
      benefits: [
        'SEO keyword research and analysis',
        'Content gap identification',
        'Search volume and difficulty scoring',
        'Topic clustering and planning'
      ],
      technical: 'Advanced NLP and search data analysis',
      color: 'from-purple-500 to-purple-600',
      demo: 'Found 47 high-value topics with low competition...'
    },
    {
      icon: PenTool,
      name: 'Article Generator',
      title: 'Create SEO-Optimized Articles',
      description: 'Generate comprehensive, well-researched articles that rank on search engines and engage readers.',
      benefits: [
        '1,500+ word comprehensive articles',
        'SEO-optimized titles and meta descriptions',
        'Natural, engaging writing style',
        'Proper heading structure and formatting'
      ],
      technical: 'Powered by Claude 3.5 Sonnet for superior quality',
      color: 'from-green-500 to-green-600',
      demo: 'Generating 1,847 word article on "AI Content Marketing"...'
    },
    {
      icon: Shield,
      name: 'Legal Fact Checker',
      title: 'Ensure Legal Compliance',
      description: 'Specialized AI that verifies ADA compliance claims and ensures all legal statements are accurate.',
      benefits: [
        'ADA compliance verification',
        'Legal claim fact-checking',
        'Proper citation formatting',
        'Industry regulation compliance'
      ],
      technical: 'Trained on legal databases and regulations',
      color: 'from-red-500 to-red-600',
      demo: 'Verified 12 claims, found 2 citations needed...'
    },
    {
      icon: Globe,
      name: 'WordPress Publisher',
      title: 'Seamless WordPress Publishing',
      description: 'Automatically format and publish your articles to WordPress with perfect SEO setup.',
      benefits: [
        'Direct WordPress publishing',
        'Perfect formatting and structure',
        'SEO meta tags and schema markup',
        'Featured image optimization'
      ],
      technical: 'WPGraphQL and REST API integration',
      color: 'from-indigo-500 to-indigo-600',
      demo: 'Published with 96/100 SEO score to WordPress...'
    }
  ]

  const advancedFeatures = [
    {
      icon: Search,
      title: 'Built-in SEO Best Practices',
      description: 'Every article is optimized for search engines with proper title tags, meta descriptions, schema markup, and internal linking strategies.',
      metrics: 'Average 92/100 SEO score',
      color: 'from-blue-500 to-blue-600'
    },
    {
      icon: Users,
      title: 'Team Collaboration',
      description: 'Work together seamlessly with role-based access, review workflows, comments, and team analytics.',
      metrics: 'Scale from 1 to 100+ team members',
      color: 'from-purple-500 to-purple-600'
    },
    {
      icon: BarChart3,
      title: 'Analytics & Reporting',
      description: 'Track content performance with SEO metrics, team productivity insights, cost tracking, and ROI analysis.',
      metrics: 'Data-driven content strategy',
      color: 'from-green-500 to-green-600'
    },
    {
      icon: Zap,
      title: 'Custom Training',
      description: 'Teach AI your brand voice with custom prompts, style guides, and brand voice training for consistent messaging.',
      metrics: 'Consistent brand messaging',
      color: 'from-orange-500 to-orange-600'
    }
  ]

  const useCases = [
    {
      title: 'Content Agencies',
      subtitle: 'Scale your agency with AI-powered content',
      description: 'Manage multiple clients with white-label options, team collaboration tools, and bulk content generation.',
      results: 'AgencyX increased output by 5x while maintaining quality',
      features: ['White-label options', 'Client management', 'Bulk operations', 'Team collaboration'],
      icon: Users,
      color: 'from-blue-500 to-purple-600'
    },
    {
      title: 'E-commerce Brands',
      subtitle: 'Drive more organic traffic to your store',
      description: 'Create product content, buying guides, and SEO-optimized articles that convert visitors into customers.',
      results: 'ShopY increased organic traffic by 200%',
      features: ['Product content', 'Buying guides', 'SEO optimization', 'Conversion focus'],
      icon: Target,
      color: 'from-green-500 to-blue-500'
    },
    {
      title: 'SaaS Companies',
      subtitle: 'Educate prospects and customers at scale',
      description: 'Generate technical content, feature announcements, and thought leadership articles that drive leads.',
      results: 'TechCorp generated 1,000+ qualified leads',
      features: ['Technical content', 'Feature announcements', 'Thought leadership', 'Lead generation'],
      icon: Zap,
      color: 'from-purple-500 to-pink-500'
    },
    {
      title: 'Legal & Healthcare',
      subtitle: 'Compliant content you can trust',
      description: 'Create industry-specific content with fact-checking, proper citations, and compliance verification.',
      results: 'LawFirm maintains 100% compliance',
      features: ['Fact-checking', 'Compliance verification', 'Proper citations', 'Industry regulations'],
      icon: Shield,
      color: 'from-red-500 to-orange-500'
    }
  ]

  const integrations = [
    'WordPress', 'Slack', 'Discord', 'Zapier', 'Webhooks', 'REST API', 'GraphQL', 'Stripe'
  ]

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
              Powerful Features for Content Success
            </h1>
            <p className="text-xl text-gray-600 dark:text-gray-400 mb-8 max-w-3xl mx-auto">
              Everything you need to create, optimize, and publish SEO content at scale
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/signup"
                className="inline-flex items-center px-8 py-4 bg-purple-gradient text-white rounded-lg font-semibold hover:opacity-90 transition-opacity space-x-2"
              >
                <span>Start Free Trial</span>
                <ArrowRight className="w-5 h-5" />
              </Link>
              <button className="inline-flex items-center px-8 py-4 border-2 border-purple-500 text-purple-600 dark:text-purple-400 rounded-lg font-semibold hover:bg-purple-50 dark:hover:bg-purple-900/20 transition-colors space-x-2">
                <Play className="w-5 h-5" />
                <span>Watch Demo</span>
              </button>
            </div>
          </motion.div>
        </div>
      </section>

      {/* 5 AI Agents Pipeline */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
              5 AI Agents Working Together
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
              Our proprietary pipeline handles everything from research to publishing
            </p>
          </motion.div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-start">
            {/* Agent List */}
            <div className="space-y-4">
              {agents.map((agent, index) => (
                <motion.div
                  key={index}
                  className={`p-6 rounded-2xl cursor-pointer transition-all duration-300 ${
                    activeAgent === index 
                      ? 'bg-white dark:bg-gray-800 shadow-lg border-2 border-purple-500' 
                      : 'bg-gray-100 dark:bg-gray-800/50 hover:bg-white dark:hover:bg-gray-800 hover:shadow-md'
                  }`}
                  onClick={() => setActiveAgent(index)}
                  whileHover={{ scale: 1.02 }}
                  initial={{ opacity: 0, x: -20 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: index * 0.1 }}
                >
                  <div className="flex items-start space-x-4">
                    <div className={`w-12 h-12 bg-gradient-to-r ${agent.color} rounded-xl flex items-center justify-center flex-shrink-0`}>
                      <agent.icon className="w-6 h-6 text-white" />
                    </div>
                    <div className="flex-1">
                      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-1">
                        {agent.name}
                      </h3>
                      <p className="text-gray-600 dark:text-gray-400 text-sm">
                        {agent.description}
                      </p>
                      {activeAgent === index && (
                        <motion.div
                          initial={{ opacity: 0, height: 0 }}
                          animate={{ opacity: 1, height: 'auto' }}
                          className="mt-3 text-xs text-purple-600 dark:text-purple-400 font-medium"
                        >
                          {agent.technical}
                        </motion.div>
                      )}
                    </div>
                    <div className="flex items-center space-x-2 text-sm text-gray-500 dark:text-gray-400">
                      <Clock className="w-4 h-4" />
                      <span>~30s</span>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>

            {/* Agent Details */}
            <motion.div
              key={activeAgent}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
              className="bg-white dark:bg-gray-800 rounded-2xl p-8 shadow-lg"
            >
              <div className={`w-16 h-16 bg-gradient-to-r ${agents[activeAgent].color} rounded-2xl flex items-center justify-center mb-6`}>
                {React.createElement(agents[activeAgent].icon, { className: "w-8 h-8 text-white" })}
              </div>

              <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                {agents[activeAgent].title}
              </h3>

              <p className="text-gray-600 dark:text-gray-400 mb-6">
                {agents[activeAgent].description}
              </p>

              <div className="space-y-3 mb-6">
                {agents[activeAgent].benefits.map((benefit, idx) => (
                  <div key={idx} className="flex items-center space-x-3">
                    <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
                    <span className="text-gray-700 dark:text-gray-300">{benefit}</span>
                  </div>
                ))}
              </div>

              {/* Demo Simulation */}
              <div className="bg-gray-50 dark:bg-gray-900 rounded-lg p-4">
                <div className="flex items-center space-x-2 mb-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                  <span className="text-sm font-medium text-gray-600 dark:text-gray-400">Live Demo</span>
                </div>
                <p className="text-sm text-gray-700 dark:text-gray-300 font-mono">
                  {agents[activeAgent].demo}
                </p>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Advanced Features */}
      <section className="py-20 bg-white dark:bg-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
              Advanced Features for Professional Teams
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
              Enterprise-grade capabilities that scale with your business
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {advancedFeatures.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="bg-gray-50 dark:bg-gray-900 rounded-2xl p-8 hover:shadow-lg transition-shadow"
              >
                <div className={`w-12 h-12 bg-gradient-to-r ${feature.color} rounded-xl flex items-center justify-center mb-6`}>
                  <feature.icon className="w-6 h-6 text-white" />
                </div>
                
                <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
                  {feature.title}
                </h3>
                
                <p className="text-gray-600 dark:text-gray-400 mb-4">
                  {feature.description}
                </p>

                <div className="inline-flex items-center px-3 py-1 bg-purple-100 dark:bg-purple-900/30 rounded-full text-sm font-medium text-purple-700 dark:text-purple-300">
                  <Star className="w-4 h-4 mr-2" />
                  {feature.metrics}
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Use Cases */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
              Built for Every Industry
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
              See how teams across industries use Blog-Poster to scale their content
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {useCases.map((useCase, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="bg-white dark:bg-gray-800 rounded-2xl p-8 shadow-lg hover:shadow-xl transition-shadow"
              >
                <div className={`w-16 h-16 bg-gradient-to-r ${useCase.color} rounded-2xl flex items-center justify-center mb-6`}>
                  <useCase.icon className="w-8 h-8 text-white" />
                </div>

                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                  {useCase.title}
                </h3>
                
                <p className="text-purple-600 dark:text-purple-400 font-semibold mb-4">
                  {useCase.subtitle}
                </p>

                <p className="text-gray-600 dark:text-gray-400 mb-6">
                  {useCase.description}
                </p>

                <div className="bg-green-50 dark:bg-green-900/20 rounded-lg p-4 mb-6">
                  <p className="text-green-800 dark:text-green-200 font-semibold text-sm">
                    ✅ Success Story: {useCase.results}
                  </p>
                </div>

                <div className="grid grid-cols-2 gap-2">
                  {useCase.features.map((feature, idx) => (
                    <div key={idx} className="flex items-center space-x-2 text-sm text-gray-600 dark:text-gray-400">
                      <CheckCircle className="w-4 h-4 text-green-500 flex-shrink-0" />
                      <span>{feature}</span>
                    </div>
                  ))}
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Integrations */}
      <section className="py-20 bg-white dark:bg-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
              Connects With Your Favorite Tools
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
              Seamless integrations with the tools you already use
            </p>
          </motion.div>

          <div className="flex flex-wrap justify-center gap-8">
            {integrations.map((integration, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, scale: 0.8 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="bg-gray-50 dark:bg-gray-900 rounded-lg px-6 py-4 text-gray-600 dark:text-gray-400 font-semibold hover:bg-purple-50 dark:hover:bg-purple-900/20 hover:text-purple-600 dark:hover:text-purple-400 transition-colors"
              >
                {integration}
              </motion.div>
            ))}
          </div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mt-12"
          >
            <p className="text-gray-600 dark:text-gray-400 mb-4">
              Need a custom integration?
            </p>
            <Link
              to="/contact"
              className="inline-flex items-center text-purple-600 dark:text-purple-400 font-semibold hover:text-purple-700 dark:hover:text-purple-300"
            >
              Contact our team
              <ArrowRight className="w-4 h-4 ml-2" />
            </Link>
          </motion.div>
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
              Ready to Experience These Features?
            </h2>
            <p className="text-xl mb-8 opacity-90">
              Join 500+ content teams already scaling with Blog-Poster
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/signup"
                className="px-8 py-4 bg-white text-purple-600 rounded-lg font-semibold hover:bg-gray-100 transition-colors inline-flex items-center justify-center space-x-2"
              >
                <span>Start Free Trial</span>
                <ArrowRight className="w-5 h-5" />
              </Link>
              <Link
                to="/pricing"
                className="px-8 py-4 border-2 border-white text-white rounded-lg font-semibold hover:bg-white hover:text-purple-600 transition-colors"
              >
                View Pricing
              </Link>
            </div>
            
            <p className="text-sm mt-4 opacity-75">
              2 free articles • No credit card required • 14-day money-back guarantee
            </p>
          </motion.div>
        </div>
      </section>
    </div>
  )
}
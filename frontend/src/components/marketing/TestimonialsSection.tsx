import React from 'react'
import { motion } from 'framer-motion'
import { Star, Quote } from 'lucide-react'
import { FadeInSection, StaggerContainer } from '@/components/ui/AnimatedComponents'

export function TestimonialsSection() {
  const testimonials = [
    {
      id: 1,
      name: 'Sarah Chen',
      role: 'Content Director',
      company: 'TechFlow',
      avatar: 'SC',
      rating: 5,
      quote: "Blog-Poster reduced our content creation time from 8 hours to 30 minutes per article. The SEO optimization is incredible - we're ranking on page 1 for competitive keywords we never thought possible.",
      metrics: '300% increase in organic traffic'
    },
    {
      id: 2,
      name: 'Marcus Rodriguez',
      role: 'Founder',
      company: 'GrowthAgency',
      avatar: 'MR',
      rating: 5,
      quote: "The legal fact-checking agent is a game-changer for our agency. We can confidently create compliance content for our clients without hiring expensive legal reviewers. ROI was immediate.",
      metrics: '$50K saved on legal reviews'
    },
    {
      id: 3,
      name: 'Emma Thompson',
      role: 'SEO Manager',
      company: 'ServiceCorp',
      avatar: 'ET',
      rating: 5,
      quote: "Best investment we've made this year. Generated 50+ articles last month, all ranking in top 10. The WordPress integration is seamless and the team collaboration features are perfect.",
      metrics: '50+ articles published monthly'
    },
    {
      id: 4,
      name: 'David Park',
      role: 'Marketing Director',
      company: 'FinTech Solutions',
      avatar: 'DP',
      rating: 5,
      quote: "The 5-agent system consistently produces better content than our previous writers. The competitor analysis feature alone has helped us identify dozens of content opportunities.",
      metrics: '400% content output increase'
    }
  ]

  const companyStats = [
    { metric: '95%', label: 'Client Retention Rate' },
    { metric: '4.9/5', label: 'Average Rating' },
    { metric: '500+', label: 'Happy Customers' },
    { metric: '10K+', label: 'Articles Generated' }
  ]

  return (
    <section className="py-20 bg-gray-50 dark:bg-gray-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <FadeInSection>
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
              What Our Customers Say
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
              Join hundreds of content teams who have transformed their workflow 
              and dramatically improved their results with Blog-Poster.
            </p>
          </div>
        </FadeInSection>

        {/* Stats Row */}
        <FadeInSection delay={0.2}>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 mb-16">
            {companyStats.map((stat, index) => (
              <motion.div
                key={stat.label}
                className="text-center"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <div className="text-3xl md:text-4xl font-bold text-purple-600 dark:text-purple-400 mb-2">
                  {stat.metric}
                </div>
                <div className="text-gray-600 dark:text-gray-400 text-sm font-medium">
                  {stat.label}
                </div>
              </motion.div>
            ))}
          </div>
        </FadeInSection>

        {/* Testimonials Grid */}
        <StaggerContainer className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {testimonials.map((testimonial, index) => (
            <motion.div
              key={testimonial.id}
              className="bg-white dark:bg-gray-800 rounded-2xl p-8 shadow-lg border border-gray-200 dark:border-gray-700"
              whileHover={{ 
                y: -5,
                boxShadow: "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)"
              }}
              transition={{ duration: 0.3 }}
            >
              {/* Quote Icon */}
              <div className="flex justify-between items-start mb-6">
                <Quote className="w-8 h-8 text-purple-500 opacity-50" />
                
                {/* Rating */}
                <div className="flex space-x-1">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <Star key={i} className="w-5 h-5 text-yellow-400 fill-current" />
                  ))}
                </div>
              </div>

              {/* Quote */}
              <blockquote className="text-gray-700 dark:text-gray-300 mb-6 leading-relaxed">
                "{testimonial.quote}"
              </blockquote>

              {/* Metrics */}
              <div className="bg-purple-50 dark:bg-purple-900/20 rounded-lg p-4 mb-6">
                <div className="text-purple-700 dark:text-purple-300 font-semibold text-sm">
                  Result: {testimonial.metrics}
                </div>
              </div>

              {/* Author */}
              <div className="flex items-center space-x-4">
                <div className="w-12 h-12 bg-purple-gradient rounded-full flex items-center justify-center">
                  <span className="text-white font-bold text-sm">
                    {testimonial.avatar}
                  </span>
                </div>
                <div>
                  <div className="font-semibold text-gray-900 dark:text-white">
                    {testimonial.name}
                  </div>
                  <div className="text-gray-600 dark:text-gray-400 text-sm">
                    {testimonial.role} at {testimonial.company}
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </StaggerContainer>

        {/* Customer Logos */}
        <FadeInSection delay={0.6}>
          <div className="mt-16 text-center">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-8">
              Trusted by leading companies worldwide
            </h3>
            
            <div className="flex flex-wrap justify-center items-center gap-8 opacity-60">
              {['TechFlow', 'GrowthAgency', 'ServiceCorp', 'FinTech Solutions', 'ContentPro', 'MarketBuzz'].map((company, index) => (
                <motion.div
                  key={company}
                  className="text-gray-500 dark:text-gray-400 font-semibold"
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 0.6, scale: 1 }}
                  transition={{ delay: index * 0.1 }}
                  whileHover={{ opacity: 1, scale: 1.05 }}
                >
                  {company}
                </motion.div>
              ))}
            </div>
          </div>
        </FadeInSection>

        {/* Bottom CTA */}
        <FadeInSection delay={0.8}>
          <div className="mt-16 text-center">
            <div className="bg-white dark:bg-gray-800 rounded-2xl p-8 shadow-lg border border-gray-200 dark:border-gray-700">
              <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                Ready to Join These Success Stories?
              </h3>
              <p className="text-gray-600 dark:text-gray-400 mb-6">
                Start your free trial today and see why content teams choose Blog-Poster
              </p>
              <motion.button
                className="px-8 py-4 bg-purple-gradient text-white rounded-lg font-semibold shadow-lg hover:shadow-xl transition-all duration-300"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                Start Free Trial - 2 Articles Free
              </motion.button>
              <p className="text-gray-500 dark:text-gray-400 text-sm mt-4">
                No credit card required • 14-day money-back guarantee
              </p>
            </div>
          </div>
        </FadeInSection>
      </div>
    </section>
  )
}
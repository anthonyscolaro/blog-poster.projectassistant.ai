import React from 'react'
import { motion } from 'framer-motion'
import { 
  Target, 
  Users, 
  Award, 
  Shield, 
  Lightbulb, 
  Heart,
  MapPin,
  Mail,
  Linkedin,
  Twitter,
  Github,
  ArrowRight,
  Star,
  Rocket,
  Globe
} from 'lucide-react'
import { Link } from 'react-router-dom'

export default function About() {
  const team = [
    {
      name: 'Sarah Chen',
      role: 'CEO & Co-Founder',
      bio: 'Former VP of Content at TechFlow. 10+ years scaling content operations for Fortune 500 companies.',
      image: '/api/placeholder/300/300',
      linkedin: 'https://linkedin.com/in/sarahchen',
      twitter: 'https://twitter.com/sarahchen'
    },
    {
      name: 'Marcus Rodriguez',
      role: 'CTO & Co-Founder', 
      bio: 'Ex-Google AI researcher. PhD in Natural Language Processing from Stanford. Published 40+ papers on AI.',
      image: '/api/placeholder/300/300',
      linkedin: 'https://linkedin.com/in/marcusrodriguez',
      github: 'https://github.com/marcusrodriguez'
    },
    {
      name: 'Emma Thompson',
      role: 'Head of Product',
      bio: 'Former Product Lead at ContentCorp. Expert in content workflows and SEO optimization.',
      image: '/api/placeholder/300/300',
      linkedin: 'https://linkedin.com/in/emmathompson',
      twitter: 'https://twitter.com/emmathompson'
    },
    {
      name: 'David Kim',
      role: 'Head of Engineering',
      bio: 'Full-stack engineer with 8+ years building scalable AI systems. Former tech lead at OpenAI.',
      image: '/api/placeholder/300/300',
      linkedin: 'https://linkedin.com/in/davidkim',
      github: 'https://github.com/davidkim'
    }
  ]

  const values = [
    {
      icon: Target,
      title: 'Quality First',
      description: 'We never compromise on content quality. Every article meets professional editorial standards.',
      color: 'from-blue-500 to-blue-600'
    },
    {
      icon: Shield,
      title: 'Transparency',
      description: "We're open about AI capabilities and limitations. No black boxes, no false promises.",
      color: 'from-green-500 to-green-600'
    },
    {
      icon: Lightbulb,
      title: 'Innovation',
      description: 'We push the boundaries of AI-powered content while maintaining ethical standards.',
      color: 'from-purple-500 to-purple-600'
    },
    {
      icon: Heart,
      title: 'Customer Success',
      description: "Your success is our success. We're here to help you achieve your content goals.",
      color: 'from-red-500 to-red-600'
    }
  ]

  const milestones = [
    {
      year: '2023',
      title: 'Company Founded',
      description: 'Started with a vision to democratize high-quality content creation'
    },
    {
      year: '2023',
      title: 'First 100 Customers',
      description: 'Reached product-market fit with content agencies and SaaS companies'
    },
    {
      year: '2024',
      title: '100,000+ Articles',
      description: 'Generated over 100,000 SEO-optimized articles for customers'
    },
    {
      year: '2024',
      title: 'Series A Funding',
      description: 'Raised $10M to expand our AI research and development team'
    },
    {
      year: '2024',
      title: '500+ Customers',
      description: 'Growing community of content teams scaling with Blog-Poster'
    }
  ]

  const investors = [
    'Sequoia Capital',
    'Andreessen Horowitz',
    'First Round Capital',
    'Y Combinator',
    'OpenAI Fund'
  ]

  const partners = [
    'Anthropic',
    'OpenAI',
    'Jina AI',
    'WordPress',
    'Stripe'
  ]

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <section className="pt-20 pb-16 bg-white dark:bg-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-center mb-16"
          >
            <h1 className="text-4xl md:text-6xl font-bold text-gray-900 dark:text-white mb-6">
              Revolutionizing Content Creation with AI
            </h1>
            <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
              Our mission is to democratize high-quality content creation, making professional-grade 
              articles accessible to teams of all sizes through AI innovation.
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center"
          >
            <div className="bg-purple-50 dark:bg-purple-900/20 rounded-2xl p-8">
              <div className="text-4xl font-bold text-purple-600 dark:text-purple-400 mb-2">500+</div>
              <p className="text-gray-600 dark:text-gray-400">Happy Customers</p>
            </div>
            <div className="bg-green-50 dark:bg-green-900/20 rounded-2xl p-8">
              <div className="text-4xl font-bold text-green-600 dark:text-green-400 mb-2">100K+</div>
              <p className="text-gray-600 dark:text-gray-400">Articles Generated</p>
            </div>
            <div className="bg-blue-50 dark:bg-blue-900/20 rounded-2xl p-8">
              <div className="text-4xl font-bold text-blue-600 dark:text-blue-400 mb-2">92%</div>
              <p className="text-gray-600 dark:text-gray-400">Avg. SEO Score</p>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Problem & Solution */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
            >
              <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-6">
                The Content Creation Challenge
              </h2>
              <div className="space-y-4 text-gray-600 dark:text-gray-400">
                <p>
                  <strong className="text-red-600 dark:text-red-400">3-5 hours per article:</strong> Traditional content creation is time-consuming and expensive.
                </p>
                <p>
                  <strong className="text-red-600 dark:text-red-400">Quality vs. Speed:</strong> Teams struggle to maintain quality while scaling content production.
                </p>
                <p>
                  <strong className="text-red-600 dark:text-red-400">Compliance Risks:</strong> Legal and regulatory compliance checking adds complexity and delays.
                </p>
                <p>
                  <strong className="text-red-600 dark:text-red-400">SEO Expertise:</strong> Creating content that actually ranks requires specialized knowledge.
                </p>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
            >
              <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-6">
                Our Solution
              </h2>
              <div className="space-y-4 text-gray-600 dark:text-gray-400">
                <p>
                  <strong className="text-green-600 dark:text-green-400">3-minute generation:</strong> Our 5-agent AI pipeline reduces creation time by 95%.
                </p>
                <p>
                  <strong className="text-green-600 dark:text-green-400">Consistent quality:</strong> AI maintains professional editorial standards at scale.
                </p>
                <p>
                  <strong className="text-green-600 dark:text-green-400">Built-in compliance:</strong> Legal fact-checking agent ensures accuracy and citations.
                </p>
                <p>
                  <strong className="text-green-600 dark:text-green-400">SEO optimized:</strong> Every article includes proper tags, meta descriptions, and structure.
                </p>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Company Values */}
      <section className="py-20 bg-white dark:bg-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
              What Drives Us
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
              Our core values guide every decision we make and every feature we build
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {values.map((value, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="text-center"
              >
                <div className={`w-16 h-16 bg-gradient-to-r ${value.color} rounded-2xl flex items-center justify-center mx-auto mb-6`}>
                  <value.icon className="w-8 h-8 text-white" />
                </div>
                <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
                  {value.title}
                </h3>
                <p className="text-gray-600 dark:text-gray-400">
                  {value.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Team Section */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
              Meet the Team
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
              AI researchers, content experts, and industry veterans working together to transform content creation
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {team.map((member, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-lg text-center"
              >
                <img
                  src={member.image}
                  alt={member.name}
                  className="w-24 h-24 rounded-full mx-auto mb-4 object-cover"
                />
                <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">
                  {member.name}
                </h3>
                <p className="text-purple-600 dark:text-purple-400 font-semibold mb-3">
                  {member.role}
                </p>
                <p className="text-gray-600 dark:text-gray-400 text-sm mb-4">
                  {member.bio}
                </p>
                <div className="flex justify-center space-x-3">
                  {member.linkedin && (
                    <a
                      href={member.linkedin}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-gray-400 hover:text-blue-600 transition-colors"
                    >
                      <Linkedin className="w-5 h-5" />
                    </a>
                  )}
                  {member.twitter && (
                    <a
                      href={member.twitter}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-gray-400 hover:text-blue-400 transition-colors"
                    >
                      <Twitter className="w-5 h-5" />
                    </a>
                  )}
                  {member.github && (
                    <a
                      href={member.github}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors"
                    >
                      <Github className="w-5 h-5" />
                    </a>
                  )}
                </div>
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
              Want to join our mission?
            </p>
            <Link
              to="/careers"
              className="inline-flex items-center text-purple-600 dark:text-purple-400 font-semibold hover:text-purple-700 dark:hover:text-purple-300"
            >
              View open positions
              <ArrowRight className="w-4 h-4 ml-2" />
            </Link>
          </motion.div>
        </div>
      </section>

      {/* Company Timeline */}
      <section className="py-20 bg-white dark:bg-gray-800">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
              Our Journey
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
              From idea to industry leader - here's how we've grown
            </p>
          </motion.div>

          <div className="relative">
            {/* Timeline line */}
            <div className="absolute left-8 top-0 bottom-0 w-0.5 bg-purple-200 dark:bg-purple-800"></div>

            <div className="space-y-8">
              {milestones.map((milestone, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: -20 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: index * 0.1 }}
                  className="flex items-start space-x-4"
                >
                  <div className="w-16 h-16 bg-purple-gradient rounded-full flex items-center justify-center text-white font-bold text-sm flex-shrink-0">
                    {milestone.year}
                  </div>
                  <div className="flex-1 pb-8">
                    <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">
                      {milestone.title}
                    </h3>
                    <p className="text-gray-600 dark:text-gray-400">
                      {milestone.description}
                    </p>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Investors & Partners */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
              Backed by the Best
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
              We're proud to work with leading investors and technology partners
            </p>
          </motion.div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
            <div>
              <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-8 text-center">
                Investors
              </h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {investors.map((investor, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, scale: 0.8 }}
                    whileInView={{ opacity: 1, scale: 1 }}
                    viewport={{ once: true }}
                    transition={{ delay: index * 0.1 }}
                    className="bg-white dark:bg-gray-800 rounded-lg p-6 text-center shadow-lg"
                  >
                    <p className="font-semibold text-gray-900 dark:text-white">{investor}</p>
                  </motion.div>
                ))}
              </div>
            </div>

            <div>
              <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-8 text-center">
                Technology Partners
              </h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {partners.map((partner, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, scale: 0.8 }}
                    whileInView={{ opacity: 1, scale: 1 }}
                    viewport={{ once: true }}
                    transition={{ delay: index * 0.1 }}
                    className="bg-white dark:bg-gray-800 rounded-lg p-6 text-center shadow-lg"
                  >
                    <p className="font-semibold text-gray-900 dark:text-white">{partner}</p>
                  </motion.div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Contact Information */}
      <section className="py-20 bg-white dark:bg-gray-800">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-6">
              Let's Connect
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-400 mb-12">
              We'd love to hear from you. Reach out for partnerships, press inquiries, or just to say hello.
            </p>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="text-center">
                <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <Mail className="w-6 h-6 text-blue-600 dark:text-blue-400" />
                </div>
                <h3 className="font-semibold text-gray-900 dark:text-white mb-2">General Inquiries</h3>
                <p className="text-gray-600 dark:text-gray-400">hello@blog-poster.com</p>
              </div>

              <div className="text-center">
                <div className="w-12 h-12 bg-purple-100 dark:bg-purple-900/30 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <Users className="w-6 h-6 text-purple-600 dark:text-purple-400" />
                </div>
                <h3 className="font-semibold text-gray-900 dark:text-white mb-2">Press & Media</h3>
                <p className="text-gray-600 dark:text-gray-400">press@blog-poster.com</p>
              </div>

              <div className="text-center">
                <div className="w-12 h-12 bg-green-100 dark:bg-green-900/30 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <MapPin className="w-6 h-6 text-green-600 dark:text-green-400" />
                </div>
                <h3 className="font-semibold text-gray-900 dark:text-white mb-2">Headquarters</h3>
                <p className="text-gray-600 dark:text-gray-400">San Francisco, CA</p>
              </div>
            </div>

            <div className="mt-12">
              <Link
                to="/contact"
                className="inline-flex items-center px-8 py-4 bg-purple-gradient text-white rounded-lg font-semibold hover:opacity-90 transition-opacity space-x-2"
              >
                <span>Get in Touch</span>
                <ArrowRight className="w-5 h-5" />
              </Link>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  )
}
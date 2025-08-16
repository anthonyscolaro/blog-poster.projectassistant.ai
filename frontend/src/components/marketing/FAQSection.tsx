import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { ChevronDown, ChevronUp } from 'lucide-react'
import { FadeInSection } from '@/components/ui/AnimatedComponents'

export function FAQSection() {
  const [openIndex, setOpenIndex] = useState<number | null>(0)

  const faqs = [
    {
      question: "How does the AI content quality compare to human writers?",
      answer: "Our 5-agent system produces content that consistently matches or exceeds human writer quality. The content is researched, fact-checked, and optimized for SEO. Many customers report better performance than their previous human-written content because of the systematic approach and built-in optimization."
    },
    {
      question: "Do I need to provide my own API keys?",
      answer: "Yes, you'll need API keys for Anthropic (Claude), OpenAI (GPT-4), and Jina (for embeddings). This keeps costs transparent and allows you to control your AI spending directly. We provide detailed setup guides and cost estimation tools to help you manage expenses."
    },
    {
      question: "Can I customize the writing style and tone?",
      answer: "Absolutely! You can train the system with your brand voice, provide style guidelines, and create custom templates. The AI learns from your existing content and can match your specific tone, terminology, and formatting preferences across all generated articles."
    },
    {
      question: "How does the legal fact-checking work?",
      answer: "Our Legal Fact-Checker agent cross-references claims against authoritative sources, adds proper citations, and flags potentially problematic statements. It ensures ADA compliance and helps maintain legal accuracy, though we always recommend final review by qualified professionals for sensitive content."
    },
    {
      question: "What WordPress versions are supported?",
      answer: "We support WordPress 5.0+ and WordPress.com sites. The integration works with most popular themes and plugins, including Yoast SEO, RankMath, and Elementor. We automatically handle formatting, featured images, meta tags, and category assignment."
    },
    {
      question: "Can I invite team members to collaborate?",
      answer: "Yes! All paid plans include team collaboration features. You can invite team members, assign roles (Editor, Writer, Reviewer), set up approval workflows, and track contributions. Team members can review, edit, and approve content before publication."
    },
    {
      question: "How accurate is the SEO optimization?",
      answer: "Our SEO optimization averages 94/100 scores across all generated content. We handle keyword density, meta tags, schema markup, internal linking, and readability optimization. The system follows current Google guidelines and adapts to algorithm updates."
    },
    {
      question: "What happens if I exceed my article limit?",
      answer: "You'll receive notifications as you approach your limit. If you exceed it, you can upgrade your plan or purchase additional articles as needed. We never stop your service abruptly - there's always a grace period to upgrade or manage your usage."
    },
    {
      question: "Do you offer refunds?",
      answer: "Yes, we offer a 14-day money-back guarantee on all paid plans. If you're not satisfied with the service for any reason, contact our support team for a full refund. The free plan allows you to test the platform risk-free before upgrading."
    },
    {
      question: "How secure is my data?",
      answer: "We're SOC 2 compliant and follow enterprise-grade security practices. Your content and API keys are encrypted at rest and in transit. We never train AI models on your data, and you maintain full ownership of all generated content."
    }
  ]

  const toggleFAQ = (index: number) => {
    setOpenIndex(openIndex === index ? null : index)
  }

  return (
    <section className="py-20 bg-white dark:bg-gray-900">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <FadeInSection>
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
              Frequently Asked Questions
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-400">
              Get answers to common questions about Blog-Poster's features, pricing, and implementation.
            </p>
          </div>
        </FadeInSection>

        <div className="space-y-4">
          {faqs.map((faq, index) => (
            <motion.div
              key={index}
              className="bg-gray-50 dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 overflow-hidden"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.05 }}
            >
              <button
                className="w-full px-6 py-6 text-left flex items-center justify-between hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors duration-200"
                onClick={() => toggleFAQ(index)}
              >
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white pr-8">
                  {faq.question}
                </h3>
                <motion.div
                  animate={{ rotate: openIndex === index ? 180 : 0 }}
                  transition={{ duration: 0.2 }}
                  className="flex-shrink-0"
                >
                  <ChevronDown className="w-5 h-5 text-gray-500" />
                </motion.div>
              </button>

              <AnimatePresence>
                {openIndex === index && (
                  <motion.div
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: 'auto', opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    transition={{ duration: 0.3, ease: "easeInOut" }}
                    className="overflow-hidden"
                  >
                    <div className="px-6 pb-6">
                      <p className="text-gray-600 dark:text-gray-400 leading-relaxed">
                        {faq.answer}
                      </p>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </motion.div>
          ))}
        </div>

        {/* Contact Support Section */}
        <FadeInSection delay={0.6}>
          <div className="mt-16 text-center">
            <div className="bg-purple-50 dark:bg-purple-900/20 rounded-2xl p-8 border border-purple-200 dark:border-purple-800">
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
                Still have questions?
              </h3>
              <p className="text-gray-600 dark:text-gray-400 mb-6">
                Our support team is here to help you get started and make the most of Blog-Poster.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <motion.button
                  className="px-6 py-3 bg-purple-gradient text-white rounded-lg font-medium"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  Contact Support
                </motion.button>
                <motion.button
                  className="px-6 py-3 border border-purple-300 dark:border-purple-700 text-purple-600 dark:text-purple-400 rounded-lg font-medium hover:bg-purple-50 dark:hover:bg-purple-900/30"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  Schedule Demo
                </motion.button>
              </div>
            </div>
          </div>
        </FadeInSection>
      </div>
    </section>
  )
}
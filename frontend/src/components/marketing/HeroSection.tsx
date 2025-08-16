import React from 'react'
import { motion, useScroll, useTransform } from 'framer-motion'
import { Play, ArrowRight, CheckCircle } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { TypingAnimation, AnimatedCounter } from '@/components/ui/AnimatedComponents'

export function HeroSection() {
  const { scrollY } = useScroll()
  const y1 = useTransform(scrollY, [0, 300], [0, -50])
  const y2 = useTransform(scrollY, [0, 300], [0, -100])

  const trustSignals = [
    'No credit card required',
    '14-day money-back guarantee',
    'Used by 500+ content teams'
  ]

  const keyBenefits = [
    'Generate 1,500+ word articles in 3 minutes',
    'Built-in legal fact-checking for compliance',
    'Automatic WordPress publishing with SEO optimization'
  ]

  return (
    <section className="relative min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-600 via-purple-700 to-indigo-800 overflow-hidden">
      {/* Animated Background Elements */}
      <motion.div 
        style={{ y: y1 }}
        className="absolute top-20 left-10 w-32 h-32 bg-white/10 rounded-full blur-xl"
        animate={{
          scale: [1, 1.2, 1],
          rotate: [0, 180, 360]
        }}
        transition={{
          duration: 8,
          repeat: Infinity,
          ease: "linear"
        }}
      />
      <motion.div 
        style={{ y: y2 }}
        className="absolute bottom-20 right-10 w-24 h-24 bg-indigo-300/20 rounded-full blur-lg"
        animate={{
          scale: [1.2, 1, 1.2],
          x: [0, 20, 0]
        }}
        transition={{
          duration: 6,
          repeat: Infinity,
          ease: "easeInOut"
        }}
      />
      
      {/* Gradient overlay */}
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-black/20" />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
          className="max-w-5xl mx-auto"
        >
          <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold text-white mb-6 leading-tight">
            Generate{' '}
            <span className="relative">
              <TypingAnimation
                text="SEO-Optimized Articles"
                className="text-yellow-300"
                speed={80}
              />
            </span>
            <br />That Actually Rank
          </h1>
        </motion.div>
        
        <motion.p 
          className="text-lg sm:text-xl md:text-2xl text-white/90 mb-8 max-w-4xl mx-auto leading-relaxed"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.3 }}
        >
          Our 5-agent AI system researches competitors, analyzes topics, creates content, 
          fact-checks claims, and publishes to WordPress—all while you sleep.
        </motion.p>

        {/* Key Benefits */}
        <motion.div
          className="mb-8 max-w-3xl mx-auto"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.5 }}
        >
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-left">
            {keyBenefits.map((benefit, index) => (
              <motion.div
                key={index}
                className="flex items-start space-x-3 bg-white/10 backdrop-blur-sm rounded-lg p-4"
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.7 + index * 0.1 }}
              >
                <CheckCircle className="w-5 h-5 text-green-400 flex-shrink-0 mt-0.5" />
                <span className="text-white/90 text-sm font-medium">{benefit}</span>
              </motion.div>
            ))}
          </div>
        </motion.div>
        
        {/* CTAs */}
        <motion.div
          className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-8"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.8 }}
        >
          <motion.button
            className="px-8 py-4 bg-white text-purple-700 rounded-lg text-lg font-semibold shadow-xl hover:shadow-2xl transition-all duration-300 flex items-center space-x-2 group"
            whileHover={{ 
              scale: 1.05,
              boxShadow: "0 25px 50px rgba(255, 255, 255, 0.3)"
            }}
            whileTap={{ scale: 0.95 }}
          >
            <span>Start Free Trial - 2 Articles Free</span>
            <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
          </motion.button>
          
          <motion.button
            className="px-8 py-4 border-2 border-white/30 text-white rounded-lg text-lg font-semibold hover:bg-white/10 hover:border-white/50 transition-all duration-300 flex items-center space-x-2 group backdrop-blur-sm"
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            <Play className="w-5 h-5 group-hover:scale-110 transition-transform" />
            <span>Watch 2-Minute Demo</span>
          </motion.button>
        </motion.div>

        {/* Trust Signals */}
        <motion.div
          className="flex flex-col sm:flex-row justify-center items-center gap-4 sm:gap-8 text-white/80 text-sm"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.8, delay: 1 }}
        >
          {trustSignals.map((signal, index) => (
            <motion.div
              key={index}
              className="flex items-center space-x-2"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 1.2 + index * 0.1 }}
            >
              <CheckCircle className="w-4 h-4 text-green-400" />
              <span>{signal}</span>
            </motion.div>
          ))}
        </motion.div>

        {/* Hero Visual - Dashboard Mockup */}
        <motion.div
          className="mt-16 relative max-w-4xl mx-auto"
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1, delay: 1.2 }}
        >
          <div className="relative">
            <motion.div
              className="bg-white rounded-2xl shadow-2xl overflow-hidden border border-gray-200"
              animate={{ y: [0, -10, 0] }}
              transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
            >
              {/* Mock Dashboard Header */}
              <div className="bg-gray-50 px-6 py-4 border-b border-gray-200">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div className="w-3 h-3 bg-red-400 rounded-full"></div>
                    <div className="w-3 h-3 bg-yellow-400 rounded-full"></div>
                    <div className="w-3 h-3 bg-green-400 rounded-full"></div>
                  </div>
                  <div className="text-gray-600 text-sm font-medium">Blog-Poster Dashboard</div>
                  <div className="w-12"></div>
                </div>
              </div>
              
              {/* Mock Dashboard Content */}
              <div className="p-6">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                  <div className="bg-purple-50 p-4 rounded-lg">
                    <div className="text-purple-600 text-2xl font-bold">
                      <AnimatedCounter value={47} />
                    </div>
                    <div className="text-gray-600 text-sm">Articles Generated</div>
                  </div>
                  <div className="bg-green-50 p-4 rounded-lg">
                    <div className="text-green-600 text-2xl font-bold">
                      <AnimatedCounter value={94} suffix="%" />
                    </div>
                    <div className="text-gray-600 text-sm">Avg SEO Score</div>
                  </div>
                  <div className="bg-blue-50 p-4 rounded-lg">
                    <div className="text-blue-600 text-2xl font-bold">
                      <AnimatedCounter value={12} suffix="h" />
                    </div>
                    <div className="text-gray-600 text-sm">Time Saved</div>
                  </div>
                </div>
                
                {/* Mock Article List */}
                <div className="space-y-3">
                  <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div className="flex items-center space-x-3">
                      <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                      <span className="text-gray-800 font-medium">How to Optimize WordPress for SEO in 2024</span>
                    </div>
                    <div className="text-green-600 text-sm font-medium">Published</div>
                  </div>
                  <div className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
                    <div className="flex items-center space-x-3">
                      <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></div>
                      <span className="text-gray-800 font-medium">Best AI Content Tools for Marketing Teams</span>
                    </div>
                    <div className="text-blue-600 text-sm font-medium">Generating...</div>
                  </div>
                </div>
              </div>
            </motion.div>
            
            {/* Floating notification */}
            <motion.div
              className="absolute -right-4 top-1/2 transform -translate-y-1/2 bg-green-500 text-white px-4 py-2 rounded-lg shadow-lg"
              initial={{ opacity: 0, scale: 0, x: 20 }}
              animate={{ opacity: 1, scale: 1, x: 0 }}
              transition={{ delay: 2, duration: 0.5 }}
            >
              <div className="text-sm font-medium">Article Published!</div>
              <div className="text-xs opacity-90">SEO Score: 96/100</div>
            </motion.div>
          </div>
        </motion.div>
      </div>
    </section>
  )
}
import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Search, 
  Target, 
  FileText, 
  Shield, 
  Send,
  Play,
  CheckCircle
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { FadeInSection, StaggerContainer } from '@/components/ui/AnimatedComponents'

export function HowItWorksSection() {
  const [activeDemo, setActiveDemo] = useState(false)
  const [currentStep, setCurrentStep] = useState(0)

  const agents = [
    {
      id: 1,
      name: 'Competitor Monitor',
      description: 'Scans industry content for opportunities and trending topics',
      icon: Search,
      time: '~30 seconds',
      color: 'from-blue-500 to-blue-600',
      details: 'Analyzes competitor content, identifies content gaps, and finds high-opportunity keywords your competitors are missing.'
    },
    {
      id: 2,
      name: 'Topic Analyzer',
      description: 'Identifies high-value keywords and content gaps',
      icon: Target,
      time: '~45 seconds',
      color: 'from-green-500 to-green-600',
      details: 'Performs keyword research, analyzes search intent, and creates content outlines optimized for search rankings.'
    },
    {
      id: 3,
      name: 'Content Generator',
      description: 'Creates SEO-optimized articles with your brand voice',
      icon: FileText,
      time: '~2 minutes',
      color: 'from-purple-500 to-purple-600',
      details: 'Generates comprehensive, well-structured articles with proper headings, meta descriptions, and internal linking strategies.'
    },
    {
      id: 4,
      name: 'Legal Fact-Checker',
      description: 'Verifies claims and ensures compliance with regulations',
      icon: Shield,
      time: '~15 seconds',
      color: 'from-red-500 to-red-600',
      details: 'Cross-references facts, adds citations, and ensures ADA compliance and legal accuracy for all claims made in the content.'
    },
    {
      id: 5,
      name: 'WordPress Publisher',
      description: 'Publishes with perfect formatting and SEO meta tags',
      icon: Send,
      time: '~5 seconds',
      color: 'from-orange-500 to-orange-600',
      details: 'Automatically formats content, adds meta tags, optimizes images, and publishes directly to your WordPress site.'
    }
  ]

  const startDemo = () => {
    setActiveDemo(true)
    setCurrentStep(0)
    
    // Simulate the demo progression
    agents.forEach((_, index) => {
      setTimeout(() => {
        setCurrentStep(index + 1)
      }, (index + 1) * 1000)
    })
    
    // Reset demo after completion
    setTimeout(() => {
      setActiveDemo(false)
      setCurrentStep(0)
    }, agents.length * 1000 + 2000)
  }

  return (
    <section id="features" className="py-20 bg-white dark:bg-gray-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <FadeInSection>
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
              5 AI Agents Working for You
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto mb-8">
              Our proprietary pipeline handles everything from research to publishing, 
              so you can focus on strategy while we handle execution.
            </p>
            
            <Button
              onClick={startDemo}
              className="bg-purple-gradient text-white hover:opacity-90 flex items-center space-x-2"
              disabled={activeDemo}
            >
              <Play className="w-5 h-5" />
              <span>{activeDemo ? 'Demo Running...' : 'Watch Live Demo'}</span>
            </Button>
          </div>
        </FadeInSection>

        {/* Agent Pipeline - 3 Column Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">
          {/* First Column - 2 Agents */}
          <StaggerContainer className="space-y-6">
            {agents.slice(0, 2).map((agent, index) => {
              const Icon = agent.icon
              const isActive = activeDemo && currentStep === index + 1
              const isCompleted = activeDemo && currentStep > index + 1
              
              return (
                <motion.div
                  key={agent.id}
                  className={`relative p-5 rounded-2xl border-2 transition-all duration-500 ${
                    isActive 
                      ? 'border-purple-500 bg-purple-50 dark:bg-purple-900/20 shadow-lg' 
                      : isCompleted
                      ? 'border-green-500 bg-green-50 dark:bg-green-900/20'
                      : 'border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800'
                  }`}
                  whileHover={{ scale: 1.02 }}
                  transition={{ duration: 0.2 }}
                >
                  {/* Status Indicator */}
                  <div className={`absolute -left-3 top-1/2 transform -translate-y-1/2 w-6 h-6 rounded-full border-4 border-white dark:border-gray-900 flex items-center justify-center ${
                    isCompleted ? 'bg-green-500' : isActive ? 'bg-purple-500' : 'bg-gray-300'
                  }`}>
                    {isCompleted ? (
                      <CheckCircle className="w-4 h-4 text-white" />
                    ) : isActive ? (
                      <motion.div
                        className="w-2 h-2 bg-white rounded-full"
                        animate={{ scale: [1, 1.5, 1] }}
                        transition={{ duration: 1, repeat: Infinity }}
                      />
                    ) : (
                      <span className="text-white text-xs font-bold">{index + 1}</span>
                    )}
                  </div>

                  {/* Automated Badge - Better positioned */}
                  <div className="absolute top-3 right-3">
                    <span className="px-2 py-1 bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300 text-xs font-medium rounded-full">
                      Auto
                    </span>
                  </div>

                  <div className="flex items-start space-x-3 pr-12">
                    <div className={`w-10 h-10 rounded-lg bg-gradient-to-r ${agent.color} flex items-center justify-center flex-shrink-0`}>
                      <Icon className="w-5 h-5 text-white" />
                    </div>
                    
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between mb-2">
                        <h3 className="text-base font-semibold text-gray-900 dark:text-white">
                          {agent.name}
                        </h3>
                        <span className="text-xs text-gray-500 dark:text-gray-400 font-medium">
                          {agent.time}
                        </span>
                      </div>
                      
                      <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                        {agent.description}
                      </p>
                      
                      <p className="text-xs text-gray-500 dark:text-gray-500 leading-relaxed">
                        {agent.details}
                      </p>
                      
                      {isActive && (
                        <motion.div
                          className="mt-3 flex items-center space-x-2 text-purple-600 dark:text-purple-400"
                          initial={{ opacity: 0 }}
                          animate={{ opacity: 1 }}
                        >
                          <motion.div
                            className="w-2 h-2 bg-purple-600 rounded-full"
                            animate={{ scale: [1, 1.5, 1] }}
                            transition={{ duration: 0.5, repeat: Infinity }}
                          />
                          <span className="text-xs font-medium">Processing...</span>
                        </motion.div>
                      )}
                    </div>
                  </div>
                </motion.div>
              )
            })}
          </StaggerContainer>

          {/* Second Column - 3 Agents */}
          <StaggerContainer className="space-y-6" staggerDelay={0.1}>
            {agents.slice(2, 5).map((agent, index) => {
              const actualIndex = index + 2
              const Icon = agent.icon
              const isActive = activeDemo && currentStep === actualIndex + 1
              const isCompleted = activeDemo && currentStep > actualIndex + 1
              
              return (
                <motion.div
                  key={agent.id}
                  className={`relative p-5 rounded-2xl border-2 transition-all duration-500 ${
                    isActive 
                      ? 'border-purple-500 bg-purple-50 dark:bg-purple-900/20 shadow-lg' 
                      : isCompleted
                      ? 'border-green-500 bg-green-50 dark:bg-green-900/20'
                      : 'border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800'
                  }`}
                  whileHover={{ scale: 1.02 }}
                  transition={{ duration: 0.2 }}
                >
                  {/* Status Indicator */}
                  <div className={`absolute -left-3 top-1/2 transform -translate-y-1/2 w-6 h-6 rounded-full border-4 border-white dark:border-gray-900 flex items-center justify-center ${
                    isCompleted ? 'bg-green-500' : isActive ? 'bg-purple-500' : 'bg-gray-300'
                  }`}>
                    {isCompleted ? (
                      <CheckCircle className="w-4 h-4 text-white" />
                    ) : isActive ? (
                      <motion.div
                        className="w-2 h-2 bg-white rounded-full"
                        animate={{ scale: [1, 1.5, 1] }}
                        transition={{ duration: 1, repeat: Infinity }}
                      />
                    ) : (
                      <span className="text-white text-xs font-bold">{actualIndex + 1}</span>
                    )}
                  </div>

                  {/* Automated Badge - Better positioned */}
                  <div className="absolute top-3 right-3">
                    <span className="px-2 py-1 bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300 text-xs font-medium rounded-full">
                      Auto
                    </span>
                  </div>

                  <div className="flex items-start space-x-3 pr-12">
                    <div className={`w-10 h-10 rounded-lg bg-gradient-to-r ${agent.color} flex items-center justify-center flex-shrink-0`}>
                      <Icon className="w-5 h-5 text-white" />
                    </div>
                    
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between mb-2">
                        <h3 className="text-base font-semibold text-gray-900 dark:text-white">
                          {agent.name}
                        </h3>
                        <span className="text-xs text-gray-500 dark:text-gray-400 font-medium">
                          {agent.time}
                        </span>
                      </div>
                      
                      <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                        {agent.description}
                      </p>
                      
                      <p className="text-xs text-gray-500 dark:text-gray-500 leading-relaxed">
                        {agent.details}
                      </p>
                      
                      {isActive && (
                        <motion.div
                          className="mt-3 flex items-center space-x-2 text-purple-600 dark:text-purple-400"
                          initial={{ opacity: 0 }}
                          animate={{ opacity: 1 }}
                        >
                          <motion.div
                            className="w-2 h-2 bg-purple-600 rounded-full"
                            animate={{ scale: [1, 1.5, 1] }}
                            transition={{ duration: 0.5, repeat: Infinity }}
                          />
                          <span className="text-xs font-medium">Processing...</span>
                        </motion.div>
                      )}
                    </div>
                  </div>
                </motion.div>
              )
            })}
          </StaggerContainer>

          {/* Third Column - Enhanced Live Pipeline Demo */}
          <FadeInSection delay={0.3} className="lg:row-span-2">
            <div className="sticky top-8">
              <div className="bg-gradient-to-br from-purple-50 to-indigo-50 dark:from-purple-900/20 dark:to-indigo-900/20 rounded-2xl p-6 border-2 border-purple-200 dark:border-purple-800 shadow-lg">
                <div className="text-center mb-6">
                  <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">
                    Live Pipeline Demo
                  </h3>
                  <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
                    Watch the 5 AI agents work together
                  </p>
                  
                  <Button
                    onClick={startDemo}
                    className="bg-purple-gradient text-white hover:opacity-90 flex items-center space-x-2 mx-auto"
                    disabled={activeDemo}
                  >
                    <Play className="w-4 h-4" />
                    <span>{activeDemo ? 'Running...' : 'Start Demo'}</span>
                  </Button>
                </div>
                
                {/* Progress Bar */}
                {activeDemo && (
                  <div className="mb-6">
                    <div className="flex justify-between text-xs text-gray-600 dark:text-gray-400 mb-2">
                      <span>Progress</span>
                      <span>{Math.round((currentStep / agents.length) * 100)}%</span>
                    </div>
                    <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                      <motion.div
                        className="bg-purple-gradient h-2 rounded-full"
                        initial={{ width: "0%" }}
                        animate={{ width: `${(currentStep / agents.length) * 100}%` }}
                        transition={{ duration: 0.5 }}
                      />
                    </div>
                  </div>
                )}
                
                <div className="space-y-3 min-h-[300px]">
                  <AnimatePresence>
                    {activeDemo && (
                      <>
                        {currentStep >= 1 && (
                          <motion.div
                            initial={{ opacity: 0, scale: 0.95 }}
                            animate={{ opacity: 1, scale: 1 }}
                            className="bg-white dark:bg-gray-800 p-4 rounded-xl border border-blue-200 dark:border-blue-800 shadow-sm"
                          >
                            <div className="flex items-center space-x-3">
                              <div className="w-8 h-8 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center">
                                <Search className="w-4 h-4 text-blue-600" />
                              </div>
                              <div className="flex-1">
                                <div className="font-semibold text-sm text-gray-900 dark:text-white">Analysis Complete</div>
                                <div className="text-xs text-gray-600 dark:text-gray-400">23 opportunities found</div>
                              </div>
                            </div>
                          </motion.div>
                        )}
                        
                        {currentStep >= 2 && (
                          <motion.div
                            initial={{ opacity: 0, scale: 0.95 }}
                            animate={{ opacity: 1, scale: 1 }}
                            className="bg-white dark:bg-gray-800 p-4 rounded-xl border border-green-200 dark:border-green-800 shadow-sm"
                          >
                            <div className="flex items-center space-x-3">
                              <div className="w-8 h-8 bg-green-100 dark:bg-green-900/30 rounded-lg flex items-center justify-center">
                                <Target className="w-4 h-4 text-green-600" />
                              </div>
                              <div className="flex-1">
                                <div className="font-semibold text-sm text-gray-900 dark:text-white">Keywords Analyzed</div>
                                <div className="text-xs text-gray-600 dark:text-gray-400">High-value targets identified</div>
                              </div>
                            </div>
                          </motion.div>
                        )}
                        
                        {currentStep >= 3 && (
                          <motion.div
                            initial={{ opacity: 0, scale: 0.95 }}
                            animate={{ opacity: 1, scale: 1 }}
                            className="bg-white dark:bg-gray-800 p-4 rounded-xl border border-purple-200 dark:border-purple-800 shadow-sm"
                          >
                            <div className="flex items-center space-x-3">
                              <div className="w-8 h-8 bg-purple-100 dark:bg-purple-900/30 rounded-lg flex items-center justify-center">
                                <FileText className="w-4 h-4 text-purple-600" />
                              </div>
                              <div className="flex-1">
                                <div className="font-semibold text-sm text-gray-900 dark:text-white">Article Generated</div>
                                <div className="text-xs text-gray-600 dark:text-gray-400">1,847 words • SEO optimized</div>
                              </div>
                            </div>
                          </motion.div>
                        )}
                        
                        {currentStep >= 4 && (
                          <motion.div
                            initial={{ opacity: 0, scale: 0.95 }}
                            animate={{ opacity: 1, scale: 1 }}
                            className="bg-white dark:bg-gray-800 p-4 rounded-xl border border-red-200 dark:border-red-800 shadow-sm"
                          >
                            <div className="flex items-center space-x-3">
                              <div className="w-8 h-8 bg-red-100 dark:bg-red-900/30 rounded-lg flex items-center justify-center">
                                <Shield className="w-4 h-4 text-red-600" />
                              </div>
                              <div className="flex-1">
                                <div className="font-semibold text-sm text-gray-900 dark:text-white">Facts Verified</div>
                                <div className="text-xs text-gray-600 dark:text-gray-400">12 claims • 3 citations added</div>
                              </div>
                            </div>
                          </motion.div>
                        )}
                        
                        {currentStep >= 5 && (
                          <motion.div
                            initial={{ opacity: 0, scale: 0.95 }}
                            animate={{ opacity: 1, scale: 1 }}
                            className="bg-white dark:bg-gray-800 p-4 rounded-xl border border-orange-200 dark:border-orange-800 shadow-sm"
                          >
                            <div className="flex items-center space-x-3">
                              <div className="w-8 h-8 bg-orange-100 dark:bg-orange-900/30 rounded-lg flex items-center justify-center">
                                <Send className="w-4 h-4 text-orange-600" />
                              </div>
                              <div className="flex-1">
                                <div className="font-semibold text-sm text-gray-900 dark:text-white">Published Successfully</div>
                                <div className="text-xs text-gray-600 dark:text-gray-400">SEO score: 96/100</div>
                              </div>
                            </div>
                          </motion.div>
                        )}
                      </>
                    )}
                  </AnimatePresence>
                  
                  {!activeDemo && (
                    <div className="flex flex-col items-center justify-center py-12 text-center">
                      <div className="w-16 h-16 bg-purple-100 dark:bg-purple-900/30 rounded-full flex items-center justify-center mb-4">
                        <Play className="w-8 h-8 text-purple-600" />
                      </div>
                      <p className="text-sm text-gray-500 dark:text-gray-400 mb-2">Ready to see the magic?</p>
                      <p className="text-xs text-gray-400 dark:text-gray-500">Click the button above to start</p>
                    </div>
                  )}
                </div>

                {activeDemo && currentStep >= 5 && (
                  <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="mt-6 p-4 bg-green-50 dark:bg-green-900/20 rounded-xl border border-green-200 dark:border-green-800"
                  >
                    <div className="text-center">
                      <CheckCircle className="w-8 h-8 text-green-600 mx-auto mb-2" />
                      <div className="font-semibold text-sm text-green-800 dark:text-green-300">Pipeline Complete!</div>
                      <div className="text-xs text-green-600 dark:text-green-400">Article ready for publishing</div>
                    </div>
                  </motion.div>
                )}
              </div>
            </div>
          </FadeInSection>
        </div>

        {/* Bottom CTA */}
        <FadeInSection delay={0.6}>
          <div className="text-center mt-16">
            <Button
              className="bg-purple-gradient text-white hover:opacity-90 text-lg px-8 py-4"
            >
              Start Your Free Trial
            </Button>
            <p className="text-gray-500 dark:text-gray-400 mt-4">
              No credit card required • Generate 2 articles free
            </p>
          </div>
        </FadeInSection>
      </div>
    </section>
  )
}
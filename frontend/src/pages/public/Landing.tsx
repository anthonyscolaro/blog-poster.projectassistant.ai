import React from 'react'
import { motion } from 'framer-motion'
import { HeroSection } from '@/components/marketing/HeroSection'
import { SocialProofSection } from '@/components/marketing/SocialProofSection'
import { HowItWorksSection } from '@/components/marketing/HowItWorksSection'
import { FeaturesSection } from '@/components/marketing/FeaturesSection'
import { PricingSection } from '@/components/marketing/PricingSection'
import { TestimonialsSection } from '@/components/marketing/TestimonialsSection'
import { FAQSection } from '@/components/marketing/FAQSection'
import { FinalCTASection } from '@/components/marketing/FinalCTASection'
import { MarketingHeader } from '@/components/marketing/MarketingHeader'
import { MarketingFooter } from '@/components/marketing/MarketingFooter'
import { PageTransition } from '@/components/ui/AnimatedComponents'

export default function Landing() {
  return (
    <PageTransition>
      <div className="min-h-screen bg-white dark:bg-gray-900">
        <main>
          <HeroSection />
          <SocialProofSection />
          <HowItWorksSection />
          <FeaturesSection />
          <PricingSection />
          <TestimonialsSection />
          <FAQSection />
          <FinalCTASection />
        </main>
        
        <MarketingFooter />
      </div>
    </PageTransition>
  )
}
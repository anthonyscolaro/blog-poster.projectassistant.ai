# Lovable Prompt: Landing Page - Marketing Website

## Business Context
Create a stunning, conversion-optimized landing page for Blog-Poster, a microSaaS platform that automates SEO content generation using a 5-agent AI system. This landing page must immediately communicate value, build trust, and drive signups.

## Target Audience
- Content marketers and agencies
- WordPress site owners
- SEO professionals
- Small to medium businesses needing content

## User Story
"As a visitor, I want to quickly understand what Blog-Poster does, see proof it works, understand pricing, and feel confident enough to sign up for a free trial."

## Design Requirements

### Visual Design
- **Hero Section**: Purple gradient background with compelling headline
- **Consistent Branding**: Purple gradient theme (#667eea to #764ba2)
- **Mobile-First**: Fully responsive on all devices
- **Fast Loading**: Optimized images and smooth animations
- **Professional**: Clean, modern SaaS aesthetic

### Content Strategy
- **Value-First**: Lead with benefits, not features
- **Social Proof**: Testimonials, logos, metrics
- **Clear CTAs**: Multiple conversion points
- **Trust Signals**: Security badges, guarantees

## Prompt for Lovable

Create a beautiful, conversion-optimized landing page for Blog-Poster, an AI-powered SEO content generation platform. This is the main marketing website that converts visitors into paying customers.

### Page Structure & Content

#### 1. Header/Navigation
```typescript
// Header with transparent background over hero
// Sticky navigation that becomes solid on scroll
<Header>
  - Logo: "Blog-Poster" with gradient accent
  - Navigation: Features, Pricing, About, Blog
  - CTA Button: "Start Free Trial" (purple gradient)
  - Login link (subtle)
</Header>
```

#### 2. Hero Section
```typescript
// Full-screen hero with purple gradient background
<HeroSection>
  Headline: "Generate SEO-Optimized Articles That Actually Rank"
  Subheadline: "Our 5-agent AI system researches competitors, analyzes topics, creates content, fact-checks claims, and publishes to WordPress—all while you sleep."
  
  Key Benefits (3 bullet points):
  - "Generate 1,500+ word articles in 3 minutes"
  - "Built-in legal fact-checking for compliance"
  - "Automatic WordPress publishing with SEO optimization"
  
  Primary CTA: "Start Free Trial - 2 Articles Free"
  Secondary CTA: "Watch 2-Minute Demo"
  
  Trust Signals:
  - "No credit card required"
  - "14-day money-back guarantee"
  - "Used by 500+ content teams"
  
  Hero Visual: 
  - Animated dashboard mockup or
  - Split-screen showing "Before: Manual content creation" vs "After: Automated pipeline"
  - Live typing animation showing article generation
</HeroSection>
```

#### 3. Social Proof Section
```typescript
<SocialProofSection>
  Header: "Trusted by Content Teams Worldwide"
  
  Company Logos (6-8 logos):
  - Use placeholder logos for agencies, SaaS companies, etc.
  - Subtle grayscale with hover color effects
  
  Key Metrics (3 metrics):
  - "10,000+ Articles Generated"
  - "95% SEO Score Average"
  - "5x Faster Than Manual Writing"
</SocialProofSection>
```

#### 4. How It Works Section
```typescript
<HowItWorksSection>
  Header: "5 AI Agents Working for You"
  Subheader: "Our proprietary pipeline handles everything from research to publishing"
  
  Agent Steps (5 cards with icons):
  1. "Competitor Monitor" - "Scans industry content for opportunities"
  2. "Topic Analyzer" - "Identifies high-value keywords and gaps"
  3. "Content Generator" - "Creates SEO-optimized articles with your voice"
  4. "Legal Fact-Checker" - "Verifies claims and ensures compliance"
  5. "WordPress Publisher" - "Publishes with perfect formatting and meta tags"
  
  Each card shows:
  - Icon, title, description
  - Time estimate (e.g., "~30 seconds")
  - "Automated" badge
  
  Bottom CTA: "See It In Action - Start Free Trial"
</HowItWorksSection>
```

#### 5. Features Showcase
```typescript
<FeaturesSection>
  Header: "Everything You Need for Content Success"
  
  Feature Grid (6 features):
  1. "SEO Optimization" - "Title tags, meta descriptions, schema markup"
  2. "Legal Compliance" - "ADA compliance fact-checking with citations"
  3. "Multi-Agent Pipeline" - "5 specialized AI agents working together"
  4. "WordPress Integration" - "Direct publishing with perfect formatting"
  5. "Cost Tracking" - "Monitor AI usage and stay within budget"
  6. "Team Collaboration" - "Invite team members with role-based access"
  
  Each feature:
  - Icon, title, description
  - Screenshot or illustration
  - "Learn More" link
</FeaturesSection>
```

#### 6. Pricing Section
```typescript
<PricingSection>
  Header: "Simple, Transparent Pricing"
  Subheader: "Use your own API keys - no hidden AI costs"
  
  Pricing Cards (4 plans):
  
  FREE:
  - Price: "$0/month"
  - Articles: "2 articles/month"
  - Features: "All core features", "WordPress publishing", "Email support"
  - CTA: "Start Free"
  - Badge: "Most Popular for Testing"
  
  STARTER:
  - Price: "$29/month"
  - Articles: "20 articles/month"
  - Features: "Priority support", "Advanced SEO", "Team collaboration (3 members)"
  - CTA: "Start 14-Day Trial"
  - Badge: "Best for Small Teams"
  
  PROFESSIONAL:
  - Price: "$99/month"
  - Articles: "100 articles/month"
  - Features: "White-label options", "API access", "Unlimited team members", "Custom agents"
  - CTA: "Start 14-Day Trial"
  - Badge: "Most Popular"
  
  ENTERPRISE:
  - Price: "Custom"
  - Articles: "Unlimited"
  - Features: "Custom deployment", "Dedicated support", "Custom integrations", "SLA guarantee"
  - CTA: "Contact Sales"
  - Badge: "For Large Organizations"
  
  Bottom Notes:
  - "All plans include 14-day money-back guarantee"
  - "Bring your own API keys (Anthropic, OpenAI, Jina)"
  - "No setup fees or cancellation charges"
</PricingSection>
```

#### 7. Testimonials Section
```typescript
<TestimonialsSection>
  Header: "What Our Customers Say"
  
  Testimonial Cards (3-4 testimonials):
  
  Testimonial 1:
  Name: "Sarah Chen"
  Role: "Content Director at TechFlow"
  Quote: "Blog-Poster reduced our content creation time from 8 hours to 30 minutes per article. The SEO optimization is incredible - we're ranking on page 1 for competitive keywords."
  Avatar: Professional headshot
  
  Testimonial 2:
  Name: "Marcus Rodriguez"
  Role: "Founder, GrowthAgency"
  Quote: "The legal fact-checking agent is a game-changer. We can confidently create compliance content for our clients without hiring expensive legal reviewers."
  Avatar: Professional headshot
  
  Testimonial 3:
  Name: "Emma Thompson"
  Role: "SEO Manager at ServiceCorp"
  Quote: "Best investment we've made. Generated 50+ articles last month, all ranking in top 10. The WordPress integration is seamless."
  Avatar: Professional headshot
  
  Display Format:
  - Card layout with quotes, avatars, names, titles
  - 5-star ratings
  - Company logos where applicable
</TestimonialsSection>
```

#### 8. FAQ Section
```typescript
<FAQSection>
  Header: "Frequently Asked Questions"
  
  Questions (8-10 FAQs):
  1. "How does the AI content quality compare to human writers?"
  2. "Do I need to provide my own API keys?"
  3. "Can I customize the writing style and tone?"
  4. "How does the legal fact-checking work?"
  5. "What WordPress versions are supported?"
  6. "Can I invite team members?"
  7. "How accurate is the SEO optimization?"
  8. "What happens if I exceed my article limit?"
  9. "Do you offer refunds?"
  10. "How secure is my data?"
  
  Format: Expandable accordion with detailed answers
</FAQSection>
```

#### 9. Final CTA Section
```typescript
<FinalCTASection>
  Background: Purple gradient
  Header: "Ready to Scale Your Content?"
  Subheader: "Join 500+ content teams generating SEO articles on autopilot"
  
  CTA Button: "Start Your Free Trial"
  Secondary: "No credit card required • 2 free articles"
  
  Security Badges:
  - "SOC 2 Compliant"
  - "GDPR Ready"
  - "99.9% Uptime"
</FinalCTASection>
```

#### 10. Footer
```typescript
<Footer>
  Company Info:
  - Logo, tagline
  - "AI-powered content generation for modern teams"
  
  Links (4 columns):
  Product: Features, Pricing, API, Integrations
  Company: About, Blog, Careers, Press
  Resources: Help Center, Documentation, Status, Security
  Legal: Privacy Policy, Terms of Service, GDPR, Cookie Policy
  
  Contact:
  - Email: hello@blog-poster.com
  - Social links: Twitter, LinkedIn, GitHub
  
  Bottom:
  - "© 2024 Blog-Poster. All rights reserved."
  - Trust badges, certifications
</Footer>
```

### Interactive Elements

#### Enhanced Animations & Micro-interactions
```typescript
// src/components/marketing/AnimatedLandingComponents.tsx
import { motion, useScroll, useTransform, useInView } from 'framer-motion'
import { TypingAnimation, AnimatedCounter, FadeInSection, StaggerContainer } from '@/components/ui/AnimatedComponents'

// Hero Section with Parallax and Typing Animation
export function AnimatedHeroSection() {
  const { scrollY } = useScroll()
  // PERFORMANCE: Use transform strings for hardware acceleration
  const y1 = useTransform(scrollY, [0, 300], ['translateY(0px)', 'translateY(-50px)'])
  const y2 = useTransform(scrollY, [0, 300], ['translateY(0px)', 'translateY(-100px)'])
  
  return (
    <section className="relative min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-50 to-indigo-100 overflow-hidden">
      {/* Floating Background Elements */}
      <motion.div 
        style={{ transform: y1 }}
        className="absolute top-20 left-10 w-32 h-32 bg-purple-300/20 rounded-full blur-xl"
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
        style={{ transform: y2 }}
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
      
      <div className="max-w-7xl mx-auto px-4 text-center relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
        >
          <h1 className="text-5xl md:text-7xl font-bold text-gray-900 mb-6">
            Generate{' '}
            <TypingAnimation
              text="SEO-Optimized Articles"
              className="bg-purple-gradient bg-clip-text text-transparent"
              speed={80}
            />
            {' '}That Actually Rank
          </h1>
        </motion.div>
        
        <motion.p 
          className="text-xl md:text-2xl text-gray-600 mb-8 max-w-3xl mx-auto leading-relaxed"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.3 }}
        >
          Our 5-agent AI system researches competitors, analyzes topics, creates content, 
          fact-checks claims, and publishes to WordPress—all while you sleep.
        </motion.p>
        
        <motion.div
          className="flex flex-col sm:flex-row gap-4 justify-center items-center"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.6 }}
        >
          <motion.button
            className="px-8 py-4 bg-purple-gradient text-white rounded-lg text-lg font-semibold shadow-lg"
            whileHover={{ 
              scale: 1.05,
              // PERFORMANCE: Use filter instead of boxShadow for better performance
              filter: "drop-shadow(0 20px 25px rgba(139, 92, 246, 0.3))"
            }}
            whileTap={{ scale: 0.95 }}
            animate={{
              filter: [
                "drop-shadow(0 10px 15px rgba(139, 92, 246, 0.3))",
                "drop-shadow(0 20px 25px rgba(139, 92, 246, 0.4))",
                "drop-shadow(0 10px 15px rgba(139, 92, 246, 0.3))"
              ]
            }}
            transition={{
              filter: {
                duration: 2,
                repeat: Infinity,
                ease: "easeInOut"
              }
            }}
            style={{ willChange: 'transform, filter' }}
          >
            Start Free Trial - 2 Articles Free
          </motion.button>
          
          <motion.button
            className="px-8 py-4 border-2 border-gray-300 text-gray-700 rounded-lg text-lg font-semibold hover:border-purple-500 hover:text-purple-600"
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            Watch 2-Minute Demo
          </motion.button>
        </motion.div>
      </div>
    </section>
  )
}

// Animated Feature Cards with Hover Effects
export function AnimatedFeatureCards({ features }) {
  return (
    <StaggerContainer className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      {features.map((feature, index) => (
        <motion.div
          key={index}
          className="bg-white rounded-2xl p-8 shadow-lg border border-gray-100"
          whileHover={{ 
            // PERFORMANCE: Use transform for hardware acceleration
            transform: 'translateY(-10px)',
            filter: 'drop-shadow(0 25px 50px rgba(0, 0, 0, 0.15))'
          }}
          transition={{ type: "spring", stiffness: 300 }}
          style={{ willChange: 'transform, filter' }}
        >
          <motion.div 
            className="w-16 h-16 bg-purple-gradient rounded-2xl flex items-center justify-center mb-6"
            whileHover={{ rotate: 360 }}
            transition={{ duration: 0.6 }}
          >
            <feature.icon className="w-8 h-8 text-white" />
          </motion.div>
          <h3 className="text-2xl font-bold text-gray-900 mb-4">{feature.title}</h3>
          <p className="text-gray-600 leading-relaxed">{feature.description}</p>
        </motion.div>
      ))}
    </StaggerContainer>
  )
}

// Animated Metrics with CountUp
export function AnimatedMetrics() {
  return (
    <motion.div 
      className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center"
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true }}
      variants={{
        hidden: { opacity: 0 },
        visible: {
          opacity: 1,
          transition: {
            staggerChildren: 0.2
          }
        }
      }}
    >
      <motion.div variants={{ hidden: { y: 20, opacity: 0 }, visible: { y: 0, opacity: 1 } }}>
        <AnimatedCounter 
          value={10847} 
          className="text-4xl md:text-5xl font-bold text-purple-600"
          suffix="+"
        />
        <p className="text-gray-600 mt-2">Articles Generated</p>
      </motion.div>
      <motion.div variants={{ hidden: { y: 20, opacity: 0 }, visible: { y: 0, opacity: 1 } }}>
        <AnimatedCounter 
          value={94} 
          className="text-4xl md:text-5xl font-bold text-purple-600"
          suffix="%"
        />
        <p className="text-gray-600 mt-2">Average SEO Score</p>
      </motion.div>
      <motion.div variants={{ hidden: { y: 20, opacity: 0 }, visible: { y: 0, opacity: 1 } }}>
        <AnimatedCounter 
          value={5} 
          className="text-4xl md:text-5xl font-bold text-purple-600"
          suffix="x"
        />
        <p className="text-gray-600 mt-2">Faster Than Manual</p>
      </motion.div>
    </motion.div>
  )
}

// Interactive Demo Component
export function InteractiveDemo() {
  const [currentStep, setCurrentStep] = useState(0)
  const steps = [
    { name: "Competitor Monitor", description: "Scanning industry content...", duration: 2000 },
    { name: "Topic Analyzer", description: "Identifying opportunities...", duration: 1500 },
    { name: "Article Generator", description: "Creating content...", duration: 3000 },
    { name: "Legal Checker", description: "Verifying claims...", duration: 1000 },
    { name: "WordPress Publisher", description: "Publishing article...", duration: 800 }
  ]
  
  return (
    <motion.div 
      className="bg-gray-50 rounded-2xl p-8"
      initial={{ opacity: 0, scale: 0.9 }}
      whileInView={{ opacity: 1, scale: 1 }}
      viewport={{ once: true }}
      transition={{ duration: 0.6 }}
    >
      <h3 className="text-2xl font-bold text-center mb-8">See It In Action</h3>
      
      <div className="space-y-4">
        {steps.map((step, index) => (
          <motion.div
            key={index}
            className={`flex items-center p-4 rounded-lg ${
              index < currentStep ? 'bg-green-100 border-green-200' :
              index === currentStep ? 'bg-blue-100 border-blue-200' :
              'bg-gray-100 border-gray-200'
            } border`}
            animate={index === currentStep ? {
              scale: [1, 1.02, 1]
            } : {}}
            transition={{ duration: 1, repeat: index === currentStep ? Infinity : 0 }}
          >
            <div className={`w-8 h-8 rounded-full flex items-center justify-center mr-4 ${
              index < currentStep ? 'bg-green-500' :
              index === currentStep ? 'bg-blue-500' :
              'bg-gray-300'
            }`}>
              {index < currentStep ? (
                <motion.svg 
                  initial={{ scale: 0 }} 
                  animate={{ scale: 1 }} 
                  className="w-5 h-5 text-white" 
                  fill="currentColor" 
                  viewBox="0 0 20 20"
                >
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </motion.svg>
              ) : index === currentStep ? (
                <div className="w-4 h-4 bg-white rounded-full animate-pulse" />
              ) : (
                <span className="text-white text-sm font-bold">{index + 1}</span>
              )}
            </div>
            <div>
              <p className="font-semibold">{step.name}</p>
              <p className="text-sm text-gray-600">{step.description}</p>
            </div>
          </motion.div>
        ))}
      </div>
    </motion.div>
  )
}
```

#### Demo Features
```typescript
// Optional interactive demo
<InteractiveDemo>
  - "Try it now" button that shows mini pipeline
  - Live preview of article generation (mock)
  - Sample competitor analysis results
  - SEO score calculator
</InteractiveDemo>
```

### Technical Implementation

#### Components Structure
```typescript
// src/pages/public/Landing.tsx
export default function Landing() {
  return (
    <>
      <HeroSection />
      <SocialProofSection />
      <HowItWorksSection />
      <FeaturesSection />
      <PricingSection />
      <TestimonialsSection />
      <FAQSection />
      <FinalCTASection />
    </>
  )
}

// Individual sections as separate components
// src/components/marketing/HeroSection.tsx
// src/components/marketing/PricingSection.tsx
// etc.
```

#### Key Features to Implement
- **Responsive Design**: Mobile-first with breakpoints
- **Performance**: Optimized images, lazy loading
- **SEO**: Meta tags, structured data, Open Graph
- **Analytics**: UTM tracking, conversion events
- **A/B Testing**: Multiple CTA variations

#### Mock Data
```typescript
// Use realistic mock data throughout
const mockMetrics = {
  articlesGenerated: 10847,
  averageSEOScore: 94,
  timesSaved: "5x"
}

const mockTestimonials = [
  // Realistic testimonials with proper attribution
]

const mockCompanyLogos = [
  // Placeholder company logos
]
```

### Success Criteria
✅ **Conversion Optimized**: Clear value prop, multiple CTAs, social proof
✅ **Mobile Responsive**: Perfect on all device sizes
✅ **Fast Loading**: < 3 second load time
✅ **SEO Ready**: Proper meta tags and structure
✅ **Brand Consistent**: Purple gradient theme throughout
✅ **Professional**: SaaS-quality design and copy
✅ **Interactive**: Smooth animations and hover effects
✅ **Trust Building**: Testimonials, guarantees, security badges

This landing page will be the primary driver of signups for the Blog-Poster platform, showcasing the unique value of the 5-agent AI system while building trust and driving conversions.
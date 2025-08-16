# Lovable Prompt: Onboarding Wizard - Complete User Setup

## Business Context
Create a comprehensive onboarding wizard that guides new users through setting up their Blog-Poster account, configuring API keys, connecting WordPress, and inviting team members. This onboarding should be engaging, informative, and ensure users can successfully generate their first article.

## User Journey
1. **Welcome**: Set expectations and show value
2. **Profile Setup**: Complete user and organization information
3. **API Keys**: Configure Anthropic, OpenAI, and Jina API keys
4. **WordPress Connection**: Connect their WordPress site
5. **Team Invites**: Invite team members (optional)
6. **Completion**: Celebrate success and guide to first article

## User Story
"As a new user, I want a guided setup process that helps me configure everything needed to start generating articles, with clear explanations of what each step does and why it's important."

## Prompt for Lovable

Create a beautiful, step-by-step onboarding wizard for Blog-Poster that guides new users through complete account setup. This wizard should be educational, engaging, and ensure users are ready to succeed with the platform.

### Onboarding Flow Structure

#### Route Setup
```typescript
// Onboarding routes in App.tsx
<Route path="/onboarding" element={<Welcome />} />
<Route path="/onboarding/profile" element={<ProfileSetup />} />
<Route path="/onboarding/api-keys" element={<ApiKeysSetup />} />
<Route path="/onboarding/wordpress" element={<WordPressSetup />} />
<Route path="/onboarding/team" element={<TeamSetup />} />
<Route path="/onboarding/complete" element={<OnboardingComplete />} />
```

#### 1. Welcome Screen (/onboarding)
```typescript
// src/pages/onboarding/Welcome.tsx
<WelcomeScreen>
  Header:
    - "Welcome to Blog-Poster! 🚀"
    - "Let's get you set up in 5 minutes"
  
  Value Proposition:
    - "What You'll Accomplish:"
    - "✅ Connect your WordPress site"
    - "✅ Configure AI agents with your API keys"
    - "✅ Generate your first SEO-optimized article"
    - "✅ Set up team collaboration"
  
  Progress Indicator:
    - Step 1 of 5 highlighted
    - Visual progress bar (0/5 complete)
  
  Expected Time:
    - "⏱️ About 5 minutes to complete"
    - "You can always skip steps and return later"
  
  CTA:
    - Primary: "Let's Get Started"
    - Secondary: "Skip Setup for Now"
  
  Visual Elements:
    - Animated illustration of the 5-agent pipeline
    - Purple gradient background
    - Floating dashboard elements
</WelcomeScreen>
```

#### 2. Profile Setup (/onboarding/profile)
```typescript
// src/pages/onboarding/Profile.tsx
<ProfileSetupScreen>
  Header:
    - "Tell Us About Yourself"
    - "This helps us personalize your experience"
  
  Progress: Step 2 of 5 (20% complete)
  
  Form Fields:
    Personal Information:
    - Full Name (pre-filled from signup)
    - Job Title (dropdown + custom)
      Options: "Content Manager", "SEO Specialist", "Marketing Director", "Agency Owner", "Blogger", "Other"
    - Company/Organization (pre-filled if available)
    - Company Size (dropdown)
      Options: "Just me", "2-10 people", "11-50 people", "51-200 people", "200+ people"
    
    Content Goals:
    - "What's your primary content goal?" (multi-select)
      Options: "Increase organic traffic", "Save time on content creation", "Improve SEO rankings", "Scale content production", "Ensure legal compliance"
    
    Current Process:
    - "How do you currently create content?" (single select)
      Options: "Manual writing", "Freelance writers", "Content agencies", "Basic AI tools", "No consistent process"
    
    Blog Information:
    - Industry/Niche (dropdown + custom)
      Options: "Technology", "Healthcare", "Finance", "Legal", "E-commerce", "Education", "Real Estate", "Other"
    - Content Frequency
      Options: "Daily", "Weekly", "Bi-weekly", "Monthly", "As needed"
  
  Sidebar Info:
    - "Why We Ask This"
    - "• Customize agent prompts for your industry"
    - "• Suggest relevant keywords and topics"
    - "• Optimize writing style and tone"
    - "• Provide industry-specific templates"
  
  Navigation:
    - Back: "← Previous"
    - Skip: "Skip This Step"
    - Continue: "Continue →" (purple gradient button)
</ProfileSetupScreen>
```

#### 3. API Keys Setup (/onboarding/api-keys)
```typescript
// src/pages/onboarding/ApiKeys.tsx
<ApiKeysSetupScreen>
  Header:
    - "Connect Your AI Services"
    - "Use your own API keys for full control and cost transparency"
  
  Progress: Step 3 of 5 (40% complete)
  
  Why Section:
    - "🔑 Why Your Own Keys?"
    - "• Full cost control - pay AI providers directly"
    - "• No markup on API usage"
    - "• Your data stays between you and the AI providers"
    - "• Higher rate limits and priority access"
  
  API Key Sections:
  
  1. Anthropic (Claude) - REQUIRED:
    - Label: "Anthropic API Key (Required)"
    - Description: "Powers the main content generation agent"
    - Input: Password field with show/hide toggle
    - Help: "Need an API key? Get one at console.anthropic.com"
    - Status indicator: "Not connected" / "Connected ✓"
    - Test button: "Test Connection"
    - Cost estimate: "~$0.10-0.50 per article"
  
  2. OpenAI (Backup) - OPTIONAL:
    - Label: "OpenAI API Key (Optional Backup)"
    - Description: "Fallback when Anthropic is unavailable"
    - Input: Password field with show/hide toggle
    - Help: "Get your key at platform.openai.com"
    - Status indicator: "Not connected" / "Connected ✓"
    - Test button: "Test Connection"
    - Cost estimate: "~$0.15-0.75 per article"
  
  3. Jina AI - REQUIRED:
    - Label: "Jina AI Reader API Key (Required)"
    - Description: "Powers competitor monitoring and web scraping"
    - Input: Password field with show/hide toggle
    - Help: "Get your free key at jina.ai/reader"
    - Status indicator: "Not connected" / "Connected ✓"
    - Test button: "Test Connection"
    - Cost estimate: "~$0.01-0.05 per article"
  
  Security Note:
    - "🔒 Your API keys are encrypted and stored securely"
    - "We never see or log your actual keys"
    - "You can update or remove keys anytime in settings"
  
  Getting Started Help:
    - Expandable section: "How to Get API Keys"
    - Step-by-step guides with screenshots
    - Expected costs and rate limits
    - Free tier information
  
  Cost Calculator:
    - "Estimated monthly cost for X articles: $Y"
    - Updates based on user's content frequency from previous step
  
  Navigation:
    - Back: "← Previous"
    - Skip: "Skip (Add Later)"
    - Continue: "Continue →" (enabled when at least Anthropic + Jina are connected)
</ApiKeysSetupScreen>
```

#### 4. WordPress Setup (/onboarding/wordpress)
```typescript
// src/pages/onboarding/WordPress.tsx
<WordPressSetupScreen>
  Header:
    - "Connect Your WordPress Site"
    - "Automatically publish articles with perfect formatting"
  
  Progress: Step 4 of 5 (60% complete)
  
  Connection Options Tabs:
  
  Tab 1: "Application Password (Recommended)"
    - WordPress URL field: "https://yoursite.com"
    - Username field: "Your WordPress username"
    - Application Password: "Generated password"
    - Help: "Application passwords are more secure than regular passwords"
    
    Setup Instructions:
    - "1. Go to Users → Profile in your WordPress admin"
    - "2. Scroll to 'Application Passwords'"
    - "3. Enter 'Blog-Poster' as the name"
    - "4. Click 'Add New Application Password'"
    - "5. Copy the generated password below"
    
    Visual Guide:
    - Screenshots showing each step
    - Expandable "Show me how" sections
  
  Tab 2: "WPGraphQL (Advanced)"
    - Description: "For headless WordPress or custom setups"
    - GraphQL Endpoint field
    - JWT Token field
    - Help: "Requires WPGraphQL plugin installed"
  
  Connection Testing:
    - Test Connection button
    - Status: "Not connected" / "Testing..." / "Connected ✓"
    - Site Info Display (when connected):
      - Site name, URL, WordPress version
      - Available post types
      - Theme information
  
  Publishing Settings:
    - Default Post Status: "Draft" / "Pending Review" / "Published"
    - Default Author: Dropdown of site users
    - Default Category: Dropdown of categories
    - Featured Image Handling: "Auto-generate" / "Use placeholder" / "Skip"
  
  Multiple Sites:
    - "Add Another Site" button
    - Support for multiple WordPress installations
    - Site switching in dashboard
  
  Security & Permissions:
    - "✅ SSL verification enabled"
    - "✅ Read-only access to site info"
    - "✅ Write access only to posts"
    - "❌ No access to plugins, themes, or users"
  
  Sidebar Tips:
    - "💡 Pro Tips"
    - "• Use a dedicated user account for Blog-Poster"
    - "• Application passwords can be revoked anytime"
    - "• We recommend starting with 'Draft' status"
    - "• You can publish multiple sites from one account"
  
  Navigation:
    - Back: "← Previous"
    - Skip: "Skip (Connect Later)"
    - Continue: "Continue →" (enabled when at least one site connected)
</WordPressSetupScreen>
```

#### 5. Team Setup (/onboarding/team)
```typescript
// src/pages/onboarding/Team.tsx
<TeamSetupScreen>
  Header:
    - "Invite Your Team"
    - "Collaborate on content creation and management"
  
  Progress: Step 5 of 5 (80% complete)
  
  Team Invitation Section:
    - "Who should join your organization?"
    - "You can always invite more people later"
  
  Invite Form:
    - Email addresses (multiple, comma-separated)
    - Role selection for each invite:
      • Owner: "Full access to everything"
      • Admin: "Manage team, settings, and content"
      • Editor: "Create and edit content"
      • Member: "Create content, limited editing"
      • Viewer: "Read-only access to content"
    
    - Personal message (optional):
      Default: "Join me on Blog-Poster to streamline our content creation!"
    
    - Send invites button: "Send Invitations"
  
  Role Explanations:
    - Visual role matrix showing permissions
    - "What can each role do?"
    - Expandable details for each role
  
  Pending Invitations:
    - List of sent invitations
    - Status: "Sent", "Accepted", "Declined"
    - Resend/Cancel options
  
  Team Size Benefits:
    - "With team collaboration you can:"
    - "• Assign content creation to team members"
    - "• Set up approval workflows"
    - "• Track team productivity and costs"
    - "• Share API keys across the organization"
  
  Skip Option:
    - "Working solo? No problem!"
    - "You can invite team members anytime from settings"
    - Large "Skip Team Setup" button
  
  Billing Note:
    - "Team members don't affect your billing"
    - "You pay per article generated, not per user"
    - "API costs are shared across your organization"
  
  Navigation:
    - Back: "← Previous"
    - Skip: "Skip Team Setup"
    - Continue: "Continue →" (enabled always)
</TeamSetupScreen>
```

#### 6. Completion Screen (/onboarding/complete)
```typescript
// src/pages/onboarding/Complete.tsx
<CompletionScreen>
  Header:
    - "🎉 You're All Set!"
    - "Your Blog-Poster account is ready to generate amazing content"
  
  Progress: Complete! (100%)
  
  Setup Summary:
    - "Here's what you've configured:"
    - ✅ Profile: "Content Manager at [Company]"
    - ✅ API Keys: "Anthropic, Jina AI connected"
    - ✅ WordPress: "[Site name] connected"
    - ✅ Team: "3 invitations sent" (or "Working solo")
  
  Next Steps Cards:
    
    Card 1: "Generate Your First Article"
    - "Let's create your first SEO-optimized article"
    - Preview: Topic suggestions based on their industry
    - CTA: "Start First Article"
    - Time: "~3 minutes"
    
    Card 2: "Explore the Dashboard"
    - "Take a tour of your new content command center"
    - Preview: Dashboard features overview
    - CTA: "View Dashboard"
    - Time: "~2 minutes"
    
    Card 3: "Configure Agent Settings"
    - "Customize how your AI agents work"
    - Preview: Agent configuration options
    - CTA: "Customize Agents"
    - Time: "~5 minutes"
  
  Quick Start Checklist:
    - "Complete these to get the most from Blog-Poster:"
    - ☐ "Generate your first article"
    - ☐ "Review and publish to WordPress"
    - ☐ "Invite team members"
    - ☐ "Set up competitor monitoring"
    - ☐ "Configure notification preferences"
  
  Resources Section:
    - "Need help? We've got you covered:"
    - "📚 Documentation & Tutorials"
    - "💬 Join our Community Slack"
    - "📧 Email Support (hello@blog-poster.com)"
    - "🎥 Video Walkthrough Series"
  
  Achievement Badge:
    - "Onboarding Complete" badge
    - Share option: "Share your achievement"
    - Progress celebration animation
  
  Primary CTA:
    - Large gradient button: "Generate My First Article"
    - Takes user to /pipeline/new with smart defaults
  
  Secondary Actions:
    - "Go to Dashboard" (smaller button)
    - "Customize Settings" (text link)
</CompletionScreen>
```

### Shared Components

#### Progress Indicator
```typescript
// src/components/onboarding/ProgressIndicator.tsx
<ProgressIndicator>
  - Visual progress bar (0-100%)
  - Step indicators (1/5, 2/5, etc.)
  - Step names and icons
  - Estimated time remaining
  - "X% Complete" text
</ProgressIndicator>
```

#### Onboarding Layout
```typescript
// src/components/onboarding/OnboardingLayout.tsx
<OnboardingLayout>
  - Consistent header with logo and progress
  - Sidebar with tips and help
  - Main content area
  - Navigation buttons (Back/Skip/Continue)
  - Purple gradient backgrounds
  - Mobile-responsive design
</OnboardingLayout>
```

#### Help Tooltips
```typescript
// Interactive help throughout
- Hover tooltips for complex terms
- "Why do we need this?" explanations
- Cost estimates and examples
- Security and privacy assurances
- Links to detailed documentation
```

### State Management

#### Onboarding Store
```typescript
// src/stores/onboardingStore.ts
interface OnboardingState {
  currentStep: number
  completedSteps: boolean[]
  profileData: ProfileData
  apiKeys: ApiKeyData
  wordpressConnections: WordPressData[]
  teamInvites: TeamInviteData[]
  canContinue: boolean
  isCompleted: boolean
}
```

#### Data Persistence
```typescript
// Save progress to Supabase
- Auto-save form data as user types
- Resume from last completed step
- Mark onboarding_completed in profiles table
- Update onboarding_step for progress tracking
```

### Technical Features

#### Form Validation
```typescript
// Real-time validation with helpful messages
- API key format validation
- WordPress URL verification
- Email format checking
- Required field indicators
- Inline error messages
```

#### API Testing
```typescript
// Live connection testing
- Test API keys with actual API calls
- WordPress connection verification
- Real-time status indicators
- Error handling with helpful suggestions
```

#### Analytics Tracking
```typescript
// Track onboarding funnel
- Step completion rates
- Drop-off points
- Time spent on each step
- Most common setup configurations
- Support ticket triggers
```

### Success Criteria
✅ **High Completion Rate**: Clear steps with obvious value
✅ **Educational**: Users understand what they're setting up
✅ **Flexible**: Can skip steps and return later
✅ **Mobile Friendly**: Works perfectly on all devices
✅ **Secure**: Safe handling of API keys and credentials
✅ **Fast**: Quick setup with smart defaults
✅ **Helpful**: Tooltips, guides, and support throughout
✅ **Celebratory**: Feels rewarding to complete

This onboarding wizard ensures new users can quickly and confidently set up their Blog-Poster account with all necessary integrations, leading to a higher activation rate and faster time-to-value.
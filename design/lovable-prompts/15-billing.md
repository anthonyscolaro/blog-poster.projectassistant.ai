# Lovable Prompt: Billing System - Complete Subscription Management

## Business Context
Create a comprehensive billing system for Blog-Poster's microSaaS platform with Stripe integration, subscription management, usage tracking, and billing analytics. This system handles the freemium model with clear upgrade paths and transparent usage monitoring.

## Business Model
- **Free**: 2 articles/month, basic features
- **Starter**: $29/month, 20 articles, team collaboration
- **Professional**: $99/month, 100 articles, white-label features
- **Enterprise**: Custom pricing, unlimited articles, dedicated support

## User Stories
- "As a user, I want to see my current usage and billing status clearly"
- "As a user, I want to upgrade/downgrade my plan easily"
- "As a user, I want to manage payment methods securely"
- "As an admin, I want to track all billing and usage metrics"

## Prompt for Lovable

Create a complete billing system for Blog-Poster with Stripe integration, subscription management, usage tracking, and billing analytics. This system should be user-friendly, transparent, and handle all aspects of SaaS billing.

### Billing Routes Structure

```typescript
// Billing routes in App.tsx
<Route path="/billing" element={<Billing />} />
<Route path="/billing/subscription" element={<Subscription />} />
<Route path="/billing/upgrade" element={<UpgradePlan />} />
<Route path="/billing/usage" element={<Usage />} />
<Route path="/billing/invoices" element={<Invoices />} />
<Route path="/billing/payment" element={<PaymentMethods />} />
<Route path="/billing/history" element={<PaymentHistory />} />
```

### 1. Billing Overview (/billing)
```typescript
// src/pages/billing/Billing.tsx
<BillingOverview>
  Header:
    - "Billing & Usage"
    - "Manage your subscription and track usage"
  
  Current Plan Card:
    - Plan name with badge (FREE/STARTER/PROFESSIONAL/ENTERPRISE)
    - Price display: "$29/month" or "Free"
    - Billing cycle: "Monthly" / "Yearly" / "One-time"
    - Next billing date or "Free plan"
    - Auto-renewal status toggle
    - CTA buttons:
      - "Upgrade Plan" (if not on highest plan)
      - "Change Plan" 
      - "Cancel Subscription" (if paid plan)
  
  Usage Summary Cards:
    
    Card 1: "Articles This Month"
    - Progress bar: 15/20 articles used (75%)
    - Status: "Good" / "Warning" / "Limit Reached"
    - Color coding: Green / Yellow / Red
    - "View Details →" link to usage page
    
    Card 2: "Team Members"
    - Current: "3/5 members used"
    - "Invite more team members"
    - "Manage team →" link
    
    Card 3: "API Costs"
    - This month: "$12.45"
    - Budget: "$50.00 limit"
    - "Your own API keys, no markup"
    - "View breakdown →" link
    
    Card 4: "Storage Used"
    - "2.3 GB / 10 GB"
    - "Images and documents"
    - Progress bar visual
  
  Quick Actions:
    - "Download Invoice" for current month
    - "Update Payment Method"
    - "View Usage Analytics"
    - "Contact Billing Support"
  
  Billing Alerts (if any):
    - Payment failed notification
    - Plan expiring soon
    - Usage approaching limits
    - Trial ending reminder
  
  Recent Activity:
    - Last 5 billing events
    - Payments, plan changes, usage milestones
    - Timestamps and amounts
</BillingOverview>
```

### 2. Subscription Management (/billing/subscription)
```typescript
// src/pages/billing/Subscription.tsx
<SubscriptionManagement>
  Header:
    - "Subscription Details"
    - "Manage your plan and billing preferences"
  
  Current Subscription Card:
    - Plan: "Professional Plan"
    - Status: "Active" / "Cancelled" / "Past Due" / "Trial"
    - Price: "$99.00/month"
    - Next billing: "March 15, 2024"
    - Auto-renewal: Toggle switch
    - Billing email: "billing@company.com"
    - Customer ID: "cus_1234567890"
  
  Plan Comparison Table:
    - Side-by-side comparison of all plans
    - Current plan highlighted
    - Feature checkmarks for each plan
    - "Select Plan" buttons for upgrades
    - "Current Plan" badge for active plan
    
    Features to compare:
    - Articles per month
    - Team members
    - API integrations
    - WordPress sites
    - White-label options
    - Priority support
    - Custom agents
    - Analytics & reporting
  
  Billing Cycle Options:
    - Monthly vs Yearly toggle
    - Savings badge: "Save 20% with yearly billing"
    - Prorated adjustment explanation
    - Immediate vs next billing cycle application
  
  Plan Change Preview:
    - "Switching to Professional Plan"
    - Prorated amount: "+$45.67 today"
    - Next billing: "$99.00 on March 15"
    - Effective date: "Immediately"
    - Confirmation required
  
  Subscription Actions:
    - "Change Plan" button
    - "Pause Subscription" (if available)
    - "Cancel Subscription" with retention offer
    - "Reactivate" (if cancelled)
  
  Billing Preferences:
    - Billing email address
    - Invoice delivery method
    - Currency preference (if multi-currency)
    - Tax information (if applicable)
  
  Cancellation Section:
    - "Cancel Subscription" expandable section
    - Retention offers: "Save 50% for 3 months"
    - Feedback form: "Why are you leaving?"
    - Data retention policy explanation
    - Confirmation with password/email verification
</SubscriptionManagement>
```

### 3. Plan Upgrade (/billing/upgrade)
```typescript
// src/pages/billing/UpgradePlan.tsx
<PlanUpgrade>
  Header:
    - "Choose Your Plan"
    - "Upgrade to unlock more features and higher limits"
  
  Current Plan Indicator:
    - "You're currently on the FREE plan"
    - Usage status: "15/20 articles used this month"
  
  Pricing Cards (4 plans):
    
    FREE Plan:
    - Price: "$0/month"
    - "Current Plan" badge
    - Features: "2 articles/month", "1 WordPress site", "Email support"
    - Limitations highlighted
    - CTA: "Current Plan" (disabled)
    
    STARTER Plan:
    - Price: "$29/month" ($25/month yearly)
    - "Most Popular" badge
    - Features: "20 articles/month", "3 WordPress sites", "5 team members", "Priority support"
    - CTA: "Upgrade to Starter"
    - Trial offer: "14-day free trial"
    
    PROFESSIONAL Plan:
    - Price: "$99/month" ($85/month yearly)
    - "Best Value" badge
    - Features: "100 articles/month", "Unlimited sites", "Unlimited team", "White-label", "API access"
    - CTA: "Upgrade to Professional"
    - Trial offer: "14-day free trial"
    
    ENTERPRISE Plan:
    - Price: "Custom"
    - "Contact Sales" badge
    - Features: "Unlimited everything", "Custom deployment", "Dedicated support", "SLA"
    - CTA: "Contact Sales"
    - Note: "Custom pricing based on needs"
  
  Feature Comparison Matrix:
    - Detailed feature comparison table
    - Checkmarks, X marks, and limited indicators
    - Expandable rows for complex features
    - Hover tooltips for explanations
  
  Billing Options:
    - Monthly vs Yearly toggle
    - Yearly savings highlighted: "Save $348/year"
    - Payment method selection
    - Billing address form
  
  Upgrade Benefits:
    - "What you get immediately:"
    - "✅ Higher article limits"
    - "✅ Advanced features unlocked"
    - "✅ Priority support queue"
    - "✅ Team collaboration tools"
  
  Trial Information:
    - "Start your 14-day free trial"
    - "No commitment, cancel anytime"
    - "Full access to all features"
    - "Your free articles don't count against trial"
  
  Payment Security:
    - Stripe security badges
    - "SSL encrypted" indicator
    - "No long-term contracts"
    - "Cancel anytime" guarantee
  
  Upgrade Process:
    - Payment method selection/addition
    - Billing information form
    - Confirmation with plan details
    - Success page with next steps
</PlanUpgrade>
```

### 4. Usage Tracking (/billing/usage)
```typescript
// src/pages/billing/Usage.tsx
<UsageTracking>
  Header:
    - "Usage Analytics"
    - "Monitor your article generation and API costs"
  
  Current Period Overview:
    - Billing period: "March 1 - March 31, 2024"
    - Days remaining: "12 days left in cycle"
    - Reset date: "Resets on March 31"
  
  Usage Metrics Cards:
    
    Card 1: "Articles Generated"
    - Current: 67/100
    - Progress bar with color coding
    - Trend: "+15 this week"
    - Status: "On track" / "High usage" / "Limit reached"
    
    Card 2: "API Costs"
    - Total: "$23.45 this month"
    - Breakdown:
      - Anthropic Claude: "$18.20"
      - Jina AI Reader: "$3.15"
      - OpenAI (backup): "$2.10"
    - Trend: "12% below last month"
    
    Card 3: "Team Activity"
    - Active members: "5/8 team members"
    - Top contributor: "Sarah (23 articles)"
    - Collaboration score: "85%"
    
    Card 4: "Success Rate"
    - Pipeline success: "94%"
    - Average generation time: "2.3 minutes"
    - Quality score: "92/100"
  
  Usage Charts:
    
    Chart 1: "Daily Article Generation"
    - 30-day line chart
    - Articles per day trend
    - Weekday vs weekend patterns
    - Plan limit baseline
    
    Chart 2: "API Cost Breakdown"
    - Pie chart of cost distribution
    - Service-by-service breakdown
    - Cost per article calculation
    - Monthly trend comparison
    
    Chart 3: "Team Contribution"
    - Bar chart by team member
    - Articles generated per person
    - Cost attribution
    - Activity timeline
  
  Detailed Usage Table:
    - Date, User, Article Title, AI Cost, Status
    - Filterable by date range, user, status
    - Sortable columns
    - Export to CSV option
    - Pagination for large datasets
  
  Usage Alerts & Recommendations:
    - "You're using 67% of your monthly limit"
    - "Consider upgrading to Professional plan"
    - "Your API costs are 23% below budget"
    - "Team is most productive on Tuesdays"
  
  Cost Optimization Tips:
    - "💡 Optimization Suggestions"
    - "Use batch processing to reduce API calls"
    - "Your average cost per article: $0.35"
    - "Industry benchmark: $0.42"
    - "You're saving 16% vs benchmark"
  
  Export Options:
    - "Download Usage Report"
    - PDF summary for current month
    - CSV data export
    - Email reports scheduling
</UsageTracking>
```

### 5. Invoice Management (/billing/invoices)
```typescript
// src/pages/billing/Invoices.tsx
<InvoiceManagement>
  Header:
    - "Invoices & Receipts"
    - "Download and manage your billing documents"
  
  Invoice Summary:
    - Total invoices: "24 invoices"
    - Total paid: "$2,340.00"
    - Outstanding: "$0.00"
    - Next invoice: "March 31, 2024"
  
  Invoice Filters:
    - Date range picker
    - Status filter: "All", "Paid", "Pending", "Overdue"
    - Amount range slider
    - Plan type filter
  
  Invoices Table:
    Columns:
    - Invoice # (INV-2024-003)
    - Date (March 1, 2024)
    - Plan (Professional)
    - Amount ($99.00)
    - Status (Paid/Pending/Overdue with color coding)
    - Actions (Download PDF, Email, View Details)
    
    Sorting:
    - Sortable by date, amount, status
    - Default: Most recent first
    - Pagination for large lists
  
  Invoice Details Modal:
    - Full invoice preview
    - Billing address
    - Line items breakdown
    - Tax calculations
    - Payment method used
    - Download/Print options
    - Send copy via email
  
  Payment Status:
    - Automatic payment success indicators
    - Failed payment alerts with retry options
    - Payment method used
    - Transaction IDs for reference
  
  Bulk Actions:
    - Select multiple invoices
    - Bulk download as ZIP
    - Email multiple invoices
    - Export to accounting software
  
  Upcoming Charges:
    - Next billing preview
    - Prorated charges if plan changed
    - Tax estimates
    - Auto-payment schedule
  
  Invoice Settings:
    - Billing email address
    - Company information for invoices
    - Tax ID number
    - Invoice delivery preferences
    - Automatic payment preferences
</InvoiceManagement>
```

### 6. Payment Methods (/billing/payment)
```typescript
// src/pages/billing/PaymentMethods.tsx
<PaymentMethods>
  Header:
    - "Payment Methods"
    - "Manage your payment information securely"
  
  Primary Payment Method:
    - Card display: "**** **** **** 4242"
    - Type: "Visa"
    - Expires: "12/2027"
    - "Primary" badge
    - Actions: "Edit", "Remove", "Set as Primary"
  
  Additional Payment Methods:
    - List of backup payment methods
    - Same card display format
    - "Backup" indicators
    - Drag-and-drop reordering
    - Add/edit/remove actions
  
  Add Payment Method:
    - "Add New Payment Method" button
    - Stripe Elements integration
    - Credit card form with real-time validation
    - Security badges and SSL indicators
    - 3D Secure support
    - Multiple card type support
  
  Payment Method Types:
    - Credit/Debit cards (Visa, MC, Amex, etc.)
    - Bank accounts (ACH) for US customers
    - Digital wallets (Apple Pay, Google Pay)
    - PayPal integration (if available)
  
  Auto-Payment Settings:
    - Enable/disable automatic payments
    - Retry failed payments: "3 attempts over 7 days"
    - Backup payment method fallback
    - Email notifications for payment events
  
  Security Features:
    - "Your payment info is encrypted and secure"
    - "We never store full card numbers"
    - "Powered by Stripe" security badge
    - PCI compliance indicators
  
  Payment Notifications:
    - Successful payment confirmations
    - Failed payment alerts
    - Card expiration reminders
    - Receipt delivery preferences
  
  Billing Address:
    - Address form for tax calculations
    - Country/region selection
    - Tax ID field (if applicable)
    - Company information
    - Invoice recipient details
  
  Payment History Link:
    - "View all payment history →"
    - Recent transactions preview
    - Payment method usage statistics
</PaymentMethods>
```

### 7. Payment History (/billing/history)
```typescript
// src/pages/billing/PaymentHistory.tsx
<PaymentHistory>
  Header:
    - "Payment History"
    - "Complete history of all transactions"
  
  Summary Stats:
    - Total payments: "$2,340.00"
    - Average monthly: "$97.50"
    - Successful payments: "24/24 (100%)"
    - Member since: "January 2023"
  
  Transaction Filters:
    - Date range picker (last 30 days, 3 months, year, custom)
    - Payment status: All, Successful, Failed, Refunded
    - Amount range slider
    - Payment method filter
    - Transaction type: Subscription, Upgrade, Refund
  
  Transactions Table:
    Columns:
    - Date & Time
    - Description ("Professional Plan - March 2024")
    - Amount ($99.00)
    - Payment Method (**** 4242)
    - Status (Success/Failed/Refunded with icons)
    - Receipt (Download link)
    
    Enhanced Details:
    - Transaction ID
    - Stripe charge ID
    - Invoice number link
    - Refund status and reason
    - Dispute information if applicable
  
  Transaction Details Modal:
    - Full transaction breakdown
    - Payment method details
    - Billing address at time of payment
    - Tax calculations
    - Plan details and changes
    - Support ticket links if issues
  
  Failed Payments Section:
    - Separate section for failed attempts
    - Failure reasons explained
    - Retry options available
    - Support contact information
    - Resolution status
  
  Refunds & Credits:
    - Prorated refunds display
    - Account credits applied
    - Refund processing status
    - Original transaction references
  
  Export Options:
    - Download as PDF report
    - CSV export for accounting
    - Email specific transactions
    - Date range selection for exports
  
  Payment Analytics:
    - Monthly payment trends chart
    - Payment method usage over time
    - Average transaction values
    - Cost optimization insights
</PaymentHistory>
```

### Shared Billing Components

#### Stripe Integration
```typescript
// src/components/billing/StripeProvider.tsx
import { loadStripe } from '@stripe/stripe-js'
import { Elements } from '@stripe/react-stripe-js'

// Stripe Elements for payment forms
// Secure card input components
// 3D Secure authentication support
// Real-time validation and formatting
```

#### Plan Comparison Component
```typescript
// src/components/billing/PlanComparison.tsx
<PlanComparison>
  - Side-by-side plan features
  - Interactive feature tooltips
  - Upgrade/downgrade buttons
  - Savings calculations
  - Feature availability matrix
</PlanComparison>
```

#### Usage Widgets
```typescript
// src/components/billing/UsageWidget.tsx
<UsageWidget>
  - Progress bars with color coding
  - Real-time usage updates
  - Trend indicators
  - Warning thresholds
  - Quick action buttons
</UsageWidget>
```

#### Invoice Component
```typescript
// src/components/billing/InvoicePreview.tsx
<InvoicePreview>
  - Professional invoice layout
  - Company branding
  - Detailed line items
  - Tax calculations
  - Payment terms
  - Download/print functionality
</InvoicePreview>
```

### Billing Store Management
```typescript
// src/stores/billingStore.ts
interface BillingState {
  subscription: SubscriptionData
  usage: UsageData
  invoices: InvoiceData[]
  paymentMethods: PaymentMethodData[]
  transactions: TransactionData[]
  billingAddress: AddressData
  preferences: BillingPreferences
}

// Real-time usage tracking
// Automatic plan limit enforcement
// Payment failure handling
// Subscription lifecycle management
```

### Integration Requirements

#### Stripe Webhooks
```typescript
// Handle Stripe webhook events
- payment_intent.succeeded
- invoice.payment_failed
- customer.subscription.updated
- customer.subscription.deleted
- payment_method.attached
```

#### Usage Tracking
```typescript
// Real-time usage monitoring
- Article generation counting
- API cost tracking
- Team member activity
- Storage usage monitoring
- Feature usage analytics
```

#### Plan Enforcement
```typescript
// Automatic limit enforcement
- Article generation limits
- Team member limits
- Feature availability control
- API rate limiting
- Storage quotas
```

### Success Criteria
✅ **Transparent Billing**: Clear pricing and usage display
✅ **Secure Payments**: PCI-compliant Stripe integration
✅ **Self-Service**: Users can manage everything themselves
✅ **Accurate Tracking**: Real-time usage and cost monitoring
✅ **Professional Invoicing**: Clean, branded invoice generation
✅ **Flexible Plans**: Easy upgrades, downgrades, and cancellations
✅ **Payment Recovery**: Automatic retry and failure handling
✅ **Compliance Ready**: Tax handling and receipt generation
✅ **Analytics**: Detailed billing and usage insights
✅ **Mobile Responsive**: Perfect mobile billing experience

This comprehensive billing system provides everything needed for a professional SaaS platform, with transparent pricing, secure payments, and detailed usage tracking that builds trust with customers.
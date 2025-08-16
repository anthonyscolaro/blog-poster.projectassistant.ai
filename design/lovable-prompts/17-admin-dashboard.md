# Lovable Prompt: Admin Dashboard - Platform Management

> **Updated January 2025**: Enhanced with enterprise-grade security features including rate limiting, audit logging, emergency controls, and real-time performance monitoring.

## Business Context
Create a comprehensive platform admin dashboard for Blog-Poster that allows platform administrators to manage the entire SaaS operation. This includes user management, organization oversight, system monitoring, billing management, and platform analytics.

## Admin User Types
- **Platform Admin**: Full access to all platform operations and data
- **Support Admin**: Customer support functions and basic user management
- **Billing Admin**: Billing, subscriptions, and financial oversight
- **Technical Admin**: System monitoring, performance, and technical operations

## User Stories
- "As a platform admin, I want a comprehensive view of all platform activity and health"
- "As a support admin, I want to quickly help customers with their issues"
- "As a billing admin, I want to track revenue, subscriptions, and payment issues"
- "As a technical admin, I want to monitor system performance and resolve issues"

## Prompt for Lovable

Create a powerful admin dashboard for Blog-Poster platform administrators to manage users, organizations, billing, system health, and platform analytics. This should feel like a professional enterprise admin interface.

### Admin Routes Structure

```typescript
// Admin routes in App.tsx (protected by AdminRoute component)
<Route path="/admin" element={<AdminDashboard />} />
<Route path="/admin/users" element={<UserManagement />} />
<Route path="/admin/organizations" element={<OrganizationManagement />} />
<Route path="/admin/billing" element={<BillingManagement />} />
<Route path="/admin/content" element={<ContentModeration />} />
<Route path="/admin/system" element={<SystemSettings />} />
<Route path="/admin/logs" element={<SystemLogs />} />
<Route path="/admin/metrics" element={<PlatformMetrics />} />
<Route path="/admin/support" element={<SupportTickets />} />
```

### 1. Admin Dashboard Overview (/admin)
```typescript
// src/pages/admin/AdminDashboard.tsx
<AdminDashboard>
  Header:
    - "Platform Administration"
    - "System health and platform overview"
    - Admin user info with role badge
    - Quick access: "Support Queue", "System Status", "Emergency Actions"
  
  Key Metrics Cards:
    
    Card 1: "Platform Health"
    - Status: "All Systems Operational" (green) / "Minor Issues" (yellow) / "Critical Issues" (red)
    - Uptime: "99.97% (30 days)"
    - Active users: "1,247 online now"
    - System load: "42% average"
    - Quick action: "View System Status"
    
    Card 2: "User Growth"
    - Total users: "12,456 users"
    - New today: "+34 signups"
    - Active today: "2,843 active users"
    - Growth rate: "+12% this month"
    - Quick action: "View User Analytics"
    
    Card 3: "Revenue Overview"
    - MRR: "$28,350 Monthly Recurring Revenue"
    - Today's revenue: "+$1,240"
    - Churn rate: "3.2% monthly"
    - LTV: "$340 average lifetime value"
    - Quick action: "View Billing Dashboard"
    
    Card 4: "Content Activity"
    - Articles today: "847 articles generated"
    - API calls: "12.4K API calls"
    - Storage used: "2.3TB / 5TB"
    - Processing time: "2.1s average"
    - Quick action: "View Content Analytics"
  
  System Status Overview:
    - Services status grid with health indicators
    - "API Gateway": ✅ Healthy (response time: 120ms)
    - "Database": ✅ Healthy (connections: 45/100)
    - "AI Services": ⚠️ Degraded (Anthropic API slower)
    - "Storage": ✅ Healthy (89% available)
    - "Queue System": ✅ Healthy (12 jobs pending)
    - "Monitoring": ✅ Healthy (all alerts active)
  
  Recent Platform Activity:
    - Real-time activity feed of significant events
    - "New organization 'TechCorp' upgraded to Professional"
    - "Payment failed for user@domain.com - retry scheduled"
    - "High API usage detected from organization 'ContentAgency'"
    - "Support ticket #1247 escalated to technical team"
    - "Security alert: Multiple failed login attempts from IP 192.168.1.1"
    - Show last 20 activities with timestamps
  
  Alert Management:
    - Active system alerts
    - User-reported issues
    - Billing alerts (failed payments, subscription expiries)
    - Performance warnings
    - Security notifications
    - Alert severity levels and escalation paths
  
  Quick Actions Panel:
    - "Create Support Ticket"
    - "Send Platform Notification"
    - "Generate Platform Report"
    - "Emergency Maintenance Mode"
    - "Broadcast System Message"
    - "Export Platform Data"
  
  Platform Analytics Summary:
    - Chart: "Daily Active Users (30 days)"
    - Chart: "Revenue Trend (90 days)"
    - Chart: "API Usage Pattern (7 days)"
    - Chart: "Geographic User Distribution"
    - Interactive dashboards with drill-down capabilities
</AdminDashboard>
```

### 2. User Management (/admin/users)
```typescript
// src/pages/admin/UserManagement.tsx
<UserManagement>
  Header:
    - "User Management"
    - "Manage platform users and their access"
  
  User Statistics:
    - Total users: "12,456 registered users"
    - Active users: "8,123 active (30 days)"
    - New users: "+234 this week"
    - Inactive users: "2,156 inactive (90+ days)"
    - Suspended users: "12 suspended accounts"
  
  User Filters & Search:
    - Search by name, email, organization
    - Filter by status: "All", "Active", "Inactive", "Suspended", "Trial"
    - Filter by plan: "Free", "Starter", "Professional", "Enterprise"
    - Filter by role: "Owner", "Admin", "Editor", "Member", "Viewer"
    - Date filters: "Joined date", "Last active", "Trial expiry"
    - Advanced filters: "High usage", "Payment issues", "Support tickets"
  
  Users Table:
    Columns:
    - User info (avatar, name, email)
    - Organization name
    - Plan/Status badges
    - Role within organization
    - Last active timestamp
    - Articles generated
    - Account health score
    - Actions menu
    
    Sortable columns with pagination
    Bulk selection for mass actions
    Export capabilities (CSV, PDF)
  
  User Details Modal:
    - Complete user profile
    - Organization membership
    - Activity timeline
    - Billing history
    - Support ticket history
    - API usage patterns
    - Security information
    - Administrative notes
    
    Admin Actions:
    - "Impersonate User" (with audit trail)
    - "Suspend Account"
    - "Reset Password"
    - "Update Profile"
    - "Merge Accounts"
    - "Delete Account"
    - "Add Admin Note"
  
  Bulk User Actions:
    - Send email announcements
    - Apply plan changes
    - Suspend/unsuspend accounts
    - Export user data
    - Tag users for follow-up
    - Update user attributes
  
  User Analytics:
    - User cohort analysis
    - Activation funnel metrics
    - Feature adoption rates
    - Geographic distribution
    - Platform usage patterns
    - Customer satisfaction scores
  
  Onboarding Analytics:
    - Onboarding completion rates
    - Drop-off points analysis
    - Time to first value
    - Feature discovery patterns
    - Support ticket correlation
  
  Risk Management:
    - Fraud detection alerts
    - Suspicious activity monitoring
    - Payment risk assessment
    - Account security scoring
    - Abuse pattern detection
</UserManagement>
```

### 3. Organization Management (/admin/organizations)
```typescript
// src/pages/admin/OrganizationManagement.tsx
<OrganizationManagement>
  Header:
    - "Organization Management"
    - "Manage customer organizations and accounts"
  
  Organization Statistics:
    - Total organizations: "3,247 organizations"
    - Active organizations: "2,891 active"
    - Enterprise accounts: "124 enterprise customers"
    - Average team size: "4.2 members"
    - Total MRR: "$28,350 monthly recurring revenue"
  
  Organization Filters:
    - Search by name, domain, contact
    - Filter by plan tier
    - Filter by team size ranges
    - Filter by revenue brackets
    - Filter by health score
    - Filter by industry/vertical
    - Filter by geographic region
  
  Organizations Table:
    Columns:
    - Organization name and logo
    - Plan and billing status
    - Team size and growth
    - Monthly revenue contribution
    - Health score indicator
    - Primary contact
    - Last activity
    - Actions menu
    
    Health Score Indicators:
    - 🟢 Healthy: Active usage, payments current
    - 🟡 At Risk: Low engagement or payment issues
    - 🔴 Critical: Churning indicators or major issues
  
  Organization Details Modal:
    
    Overview Tab:
    - Organization profile and settings
    - Team member list with roles
    - Contact information
    - Billing address and tax info
    - Custom branding settings
    
    Usage Tab:
    - Article generation statistics
    - API usage patterns
    - Feature adoption metrics
    - Storage utilization
    - Performance metrics
    
    Billing Tab:
    - Current subscription details
    - Payment history
    - Invoice management
    - Revenue analytics
    - Credit and refund history
    
    Support Tab:
    - Support ticket history
    - Communication timeline
    - Escalation history
    - Satisfaction scores
    - Admin notes and flags
    
    Security Tab:
    - Access logs and security events
    - API key management
    - Two-factor authentication status
    - Compliance settings
    - Audit trail
  
  Organization Analytics:
    - Revenue by organization size
    - Plan distribution analysis
    - Geographic revenue mapping
    - Industry vertical breakdown
    - Customer lifetime value analysis
    - Expansion revenue tracking
  
  Account Health Monitoring:
    - Usage pattern analysis
    - Engagement scoring
    - Churn risk prediction
    - Support ticket trends
    - Payment health indicators
    - Feature adoption tracking
  
  Enterprise Features:
    - Custom contract management
    - SLA monitoring and reporting
    - Dedicated support assignment
    - Custom feature flags
    - White-label configuration
    - Integration management
</OrganizationManagement>
```

### 4. Billing Management (/admin/billing)
```typescript
// src/pages/admin/BillingManagement.tsx
<BillingManagement>
  Header:
    - "Billing Management"
    - "Platform revenue and subscription oversight"
  
  Revenue Dashboard:
    
    Key Metrics:
    - MRR: "$28,350" with trend indicator
    - ARR: "$340,200" with growth rate
    - ARPU: "$87.50" average revenue per user
    - LTV: "$340" lifetime value
    - Churn Rate: "3.2% monthly"
    - Growth Rate: "+12% MoM"
    
    Revenue Charts:
    - MRR trend over 12 months
    - Plan distribution pie chart
    - Geographic revenue mapping
    - Cohort revenue analysis
    - Churn and expansion tracking
  
  Subscription Overview:
    - Active subscriptions by plan
    - Trial conversions this month
    - Upcoming renewals (next 30 days)
    - Payment failures requiring attention
    - Subscription changes (upgrades/downgrades)
    - Cancellation requests and saves
  
  Payment Management:
    
    Failed Payments:
    - List of failed payment attempts
    - Customer notification status
    - Retry schedules and attempts
    - Manual retry options
    - Dunning management
    - Account suspension queue
    
    Refunds & Credits:
    - Pending refund requests
    - Prorated credit calculations
    - Dispute management
    - Chargeback tracking
    - Account credit balances
    - Goodwill credit allocation
  
  Plan Analytics:
    
    Plan Performance:
    - Conversion rates by plan
    - Upgrade/downgrade patterns
    - Plan retention rates
    - Feature usage by plan
    - Support burden by plan
    - Profitability analysis
    
    Pricing Optimization:
    - A/B testing results
    - Price elasticity analysis
    - Competitor pricing monitoring
    - Revenue impact modeling
    - Feature bundling analysis
  
  Financial Reporting:
    - Revenue recognition tracking
    - Tax calculation and reporting
    - Invoice generation and delivery
    - Payment reconciliation
    - Financial audit trails
    - Accounting system integration
  
  Billing Operations:
    - Bulk billing actions
    - Custom pricing approvals
    - Enterprise contract management
    - Payment method updates
    - Subscription modifications
    - Billing calendar management
  
  Stripe Integration Management:
    - Webhook status monitoring
    - API usage and limits
    - Payment method analytics
    - Currency and region settings
    - Fraud detection configuration
    - Compliance monitoring
</BillingManagement>
```

### 5. Content Moderation (/admin/content)
```typescript
// src/pages/admin/ContentModeration.tsx
<ContentModeration>
  Header:
    - "Content Moderation"
    - "Monitor and manage platform content"
  
  Content Statistics:
    - Total articles: "156,847 articles generated"
    - Today's articles: "2,341 articles"
    - Flagged content: "23 items requiring review"
    - High-quality content: "89% above quality threshold"
    - Compliance rate: "97% passing legal fact-check"
  
  Flagged Content Queue:
    - Content requiring admin review
    - Automated flag reasons (quality, compliance, abuse)
    - User-reported content
    - Priority levels and SLA tracking
    - Reviewer assignment and status
    - Approval/rejection workflows
  
  Content Quality Monitoring:
    
    Quality Metrics:
    - Average SEO scores by organization
    - Fact-checking pass rates
    - Content length distribution
    - Readability score analysis
    - Keyword optimization effectiveness
    
    Quality Alerts:
    - Organizations with declining quality
    - Suspicious content patterns
    - Compliance violations
    - Plagiarism detection alerts
    - Brand safety concerns
  
  Content Analytics:
    
    Usage Patterns:
    - Most generated content types
    - Popular keywords and topics
    - Industry-specific content trends
    - Seasonal content patterns
    - Geographic content preferences
    
    Performance Metrics:
    - Content engagement rates
    - SEO performance tracking
    - WordPress publishing success
    - Content lifecycle analysis
    - ROI metrics by content type
  
  Compliance Management:
    
    Legal Review:
    - ADA compliance checking
    - Legal fact verification
    - Citation accuracy
    - Industry regulation compliance
    - Copyright infringement detection
    
    Content Policies:
    - Platform content guidelines
    - Automated policy enforcement
    - Manual review workflows
    - Appeal processes
    - Policy violation tracking
  
  Content Administration:
    - Bulk content actions
    - Content migration tools
    - Backup and recovery
    - Content archival policies
    - Data retention management
    - Export capabilities
  
  AI Model Performance:
    - Content generation success rates
    - Model accuracy metrics
    - API usage efficiency
    - Cost per article trends
    - Quality improvement tracking
    - A/B testing of prompts
</ContentModeration>
```

### 6. System Settings (/admin/system)
```typescript
// src/pages/admin/SystemSettings.tsx
<SystemSettings>
  Header:
    - "System Settings"
    - "Configure platform-wide settings and policies"
  
  Platform Configuration:
    
    General Settings:
    - Platform name and branding
    - Default time zones and locales
    - System-wide feature flags
    - Maintenance mode controls
    - Emergency contact information
    - Legal entity information
    
    User Defaults:
    - Default plan assignments
    - Trial period configurations
    - Onboarding flow settings
    - Default notification preferences
    - Account verification requirements
    - Password policy enforcement
  
  API Configuration:
    
    Rate Limiting:
    - Global rate limits
    - Per-plan rate limits
    - Burst allowances
    - IP-based restrictions
    - API key management
    - Usage quotas
    
    Service Integrations:
    - Anthropic API settings
    - OpenAI API configuration
    - Jina AI service settings
    - WordPress connection limits
    - Third-party service limits
    - Failover configurations
  
  Security Settings:
    
    Authentication:
    - Two-factor authentication policies
    - Session timeout configurations
    - Password complexity requirements
    - Login attempt limitations
    - Account lockout policies
    - Social login settings
    
    Data Protection:
    - Data encryption settings
    - Backup retention policies
    - GDPR compliance configuration
    - Data export limitations
    - Privacy policy enforcement
    - Audit log retention
  
  Billing Configuration:
    
    Pricing Settings:
    - Plan pricing and features
    - Trial period lengths
    - Billing cycle options
    - Proration policies
    - Discount and coupon settings
    - Currency and tax settings
    
    Payment Processing:
    - Stripe configuration
    - Payment retry policies
    - Dunning management
    - Refund automation
    - Chargeback handling
    - Revenue recognition rules
  
  Notification Systems:
    
    Email Configuration:
    - SMTP server settings
    - Email template management
    - Delivery rate monitoring
    - Bounce handling
    - Unsubscribe management
    - Compliance tracking
    
    System Alerts:
    - Alert threshold configuration
    - Escalation procedures
    - Notification channels
    - Alert suppression rules
    - Maintenance notifications
    - Emergency procedures
  
  Performance Tuning:
    - Database optimization settings
    - Caching configuration
    - CDN settings
    - Load balancing rules
    - Resource allocation
    - Scaling policies
</SystemSettings>
```

### 7. System Logs (/admin/logs)
```typescript
// src/pages/admin/SystemLogs.tsx
<SystemLogs>
  Header:
    - "System Logs"
    - "Monitor system events and troubleshoot issues"
  
  Log Categories:
    
    Tab 1: "Application Logs"
    - User actions and application events
    - API requests and responses
    - Error tracking and debugging
    - Performance monitoring
    - Feature usage tracking
    
    Tab 2: "Security Logs"
    - Authentication events
    - Authorization failures
    - Suspicious activity detection
    - Data access auditing
    - Compliance violations
    
    Tab 3: "System Logs"
    - Server performance metrics
    - Database query logs
    - Service health checks
    - Infrastructure events
    - Deployment activities
    
    Tab 4: "Billing Logs"
    - Payment processing events
    - Subscription changes
    - Invoice generation
    - Failed payment attempts
    - Refund processing
  
  Log Filtering & Search:
    - Time range selection
    - Log level filtering (ERROR, WARN, INFO, DEBUG)
    - User/organization filtering
    - Event type selection
    - Text search with regex support
    - Advanced query builder
  
  Real-time Log Streaming:
    - Live log updates
    - Auto-refresh controls
    - Pause/resume streaming
    - Log volume indicators
    - Real-time alerts
    - Emergency log highlighting
  
  Log Analysis Tools:
    
    Error Analysis:
    - Error rate trends
    - Most common errors
    - Error impact assessment
    - Resolution tracking
    - Escalation management
    
    Performance Analysis:
    - Response time trends
    - Slow query identification
    - Resource utilization
    - Bottleneck detection
    - Capacity planning
    
    Security Analysis:
    - Failed login patterns
    - Suspicious IP addresses
    - Access pattern anomalies
    - Compliance violations
    - Threat detection
  
  Log Export & Retention:
    - Log export in multiple formats
    - Retention policy management
    - Archive and backup procedures
    - Legal hold capabilities
    - Compliance reporting
    - External SIEM integration
  
  Alerting & Monitoring:
    - Log-based alert rules
    - Threshold monitoring
    - Anomaly detection
    - Automated responses
    - Escalation procedures
    - Integration with monitoring tools
</SystemLogs>
```

### 8. Platform Metrics (/admin/metrics)
```typescript
// src/pages/admin/PlatformMetrics.tsx
<PlatformMetrics>
  Header:
    - "Platform Metrics"
    - "Comprehensive platform analytics and KPIs"
  
  Executive Dashboard:
    
    Business Metrics:
    - Monthly Recurring Revenue (MRR)
    - Customer Acquisition Cost (CAC)
    - Customer Lifetime Value (LTV)
    - Churn Rate and Retention
    - Net Promoter Score (NPS)
    - Product-Market Fit Indicators
    
    Growth Metrics:
    - User acquisition trends
    - Organic vs paid growth
    - Viral coefficient
    - Feature adoption rates
    - Market penetration
    - Competitive positioning
  
  User Analytics:
    
    Engagement Metrics:
    - Daily/Monthly Active Users
    - Session duration and frequency
    - Feature usage patterns
    - User journey analysis
    - Cohort behavior analysis
    - Activation funnel performance
    
    Retention Analysis:
    - User retention curves
    - Churn prediction modeling
    - Win-back campaign effectiveness
    - Segment-based retention
    - Product stickiness metrics
  
  Financial Analytics:
    
    Revenue Analysis:
    - Revenue by customer segment
    - Plan upgrade/downgrade patterns
    - Geographic revenue distribution
    - Seasonal revenue trends
    - Revenue forecasting
    - Unit economics analysis
    
    Cost Analysis:
    - Customer acquisition costs
    - Service delivery costs
    - Support cost per customer
    - Infrastructure cost trends
    - Profit margin analysis
    - ROI calculations
  
  Product Analytics:
    
    Feature Performance:
    - Feature adoption rates
    - Feature usage intensity
    - Feature-specific retention
    - A/B testing results
    - Product roadmap impact
    - User feedback correlation
    
    Technical Metrics:
    - API usage patterns
    - System performance trends
    - Error rates and resolution
    - Uptime and reliability
    - Scalability metrics
    - Infrastructure efficiency
  
  Market Analytics:
    
    Competitive Intelligence:
    - Market share analysis
    - Competitive feature comparison
    - Pricing analysis
    - Customer switching patterns
    - Industry trend correlation
    - Positioning effectiveness
    
    Customer Insights:
    - Customer satisfaction scores
    - Support ticket analysis
    - Feature request patterns
    - Use case distribution
    - Success story identification
    - Risk customer identification
  
  Custom Reporting:
    - Report builder interface
    - Scheduled report delivery
    - Custom KPI definitions
    - Data visualization options
    - Export capabilities
    - Dashboard sharing
</PlatformMetrics>
```

### 9. Support Tickets (/admin/support)
```typescript
// src/pages/admin/SupportTickets.tsx
<SupportTickets>
  Header:
    - "Support Management"
    - "Customer support and issue resolution"
  
  Support Queue Overview:
    - Open tickets: "47 tickets"
    - Response time SLA: "94% under 2 hours"
    - Resolution time: "18 hours average"
    - Customer satisfaction: "4.7/5.0 rating"
    - Escalated tickets: "3 critical issues"
  
  Ticket Filters & Views:
    - Priority levels: "Critical", "High", "Normal", "Low"
    - Status filters: "New", "Open", "Pending", "Resolved", "Closed"
    - Category filters: "Technical", "Billing", "Feature Request", "Bug Report"
    - Assignee filters: "Unassigned", "My Tickets", "Team Member"
    - SLA status: "Within SLA", "At Risk", "Breached"
  
  Ticket Management:
    
    Ticket List View:
    - Ticket ID and subject
    - Customer information
    - Priority and status indicators
    - Category and tags
    - Assigned agent
    - Last activity timestamp
    - SLA countdown timers
    
    Ticket Details:
    - Complete conversation thread
    - Customer context and history
    - Technical information
    - Internal notes and collaboration
    - Resolution tracking
    - Time logging
    - Customer satisfaction feedback
  
  Customer Context Panel:
    - Customer profile and organization
    - Account status and plan
    - Recent activity and usage
    - Previous support history
    - Billing and payment status
    - Technical configuration
    - Risk indicators and flags
  
  Support Analytics:
    
    Performance Metrics:
    - First response time trends
    - Resolution time analysis
    - Customer satisfaction scores
    - Agent performance metrics
    - Ticket volume patterns
    - Escalation rate tracking
    
    Issue Analysis:
    - Common issue categories
    - Root cause analysis
    - Product feedback insights
    - Feature request patterns
    - Bug report trends
    - Customer pain points
  
  Knowledge Management:
    - Knowledge base articles
    - Solution templates
    - FAQ management
    - Video tutorials
    - Documentation updates
    - Best practice sharing
  
  Support Operations:
    - Workload distribution
    - Skill-based routing
    - Escalation procedures
    - Quality assurance
    - Training requirements
    - Performance reviews
</SupportTickets>
```

### Shared Admin Components

#### Admin Layout
```typescript
// src/components/layout/AdminLayout.tsx
<AdminLayout>
  - Admin-specific navigation
  - Permission-based menu items
  - System status indicators
  - Quick action shortcuts
  - Role-based customization
</AdminLayout>
```

#### Metrics Dashboard
```typescript
// src/components/admin/MetricsDashboard.tsx
<MetricsDashboard>
  - KPI card components
  - Interactive charts and graphs
  - Real-time data updates
  - Drill-down capabilities
  - Export functionality
</MetricsDashboard>
```

#### Data Tables
```typescript
// src/components/admin/AdminDataTable.tsx
<AdminDataTable>
  - Advanced filtering and search
  - Bulk actions support
  - Export capabilities
  - Column customization
  - Pagination and sorting
</AdminDataTable>
```

#### Alert System
```typescript
// src/components/admin/AlertManager.tsx
<AlertManager>
  - Real-time alert notifications
  - Alert prioritization
  - Acknowledgment tracking
  - Escalation procedures
  - Alert history
</AlertManager>
```

### Admin Store Management
```typescript
// src/stores/adminStore.ts
interface AdminState {
  systemHealth: SystemHealthData
  platformMetrics: PlatformMetricsData
  userManagement: UserManagementData
  billingOverview: BillingOverviewData
  supportQueue: SupportQueueData
  contentModeration: ContentModerationData
}

// Real-time system monitoring
// Admin action audit trails
// Permission enforcement
// Data aggregation and caching
```

### Security & Audit
```typescript
// Comprehensive admin audit trail
- All admin actions logged
- IP address and session tracking
- Data access monitoring
- Permission change tracking
- System modification logs
- Compliance reporting

// Admin Activity Logging
interface AdminAuditLog {
  admin_id: string
  action: string
  target_type: 'user' | 'organization' | 'system'
  target_id: string
  details: Record<string, unknown>
  ip_address: string
  user_agent: string
  timestamp: string
  severity: 'info' | 'warning' | 'critical'
}

// Example audit log implementation
const logAdminAction = async (action: Partial<AdminAuditLog>) => {
  await supabase.from('admin_audit_logs').insert({
    ...action,
    admin_id: currentAdmin.id,
    ip_address: request.ip,
    timestamp: new Date().toISOString()
  })
}
```

### Rate Limiting & Abuse Prevention
```typescript
// Protect admin endpoints from abuse
const adminRateLimit = {
  impersonate: '5 per hour per admin',
  bulkOperations: '10 per hour',
  dataExport: '20 per day',
  systemConfig: '30 per hour',
  userModification: '100 per hour'
}

// Rate limiting implementation
interface RateLimitConfig {
  endpoint: string
  limit: number
  window: 'minute' | 'hour' | 'day'
  byAdmin: boolean
}

// Example rate limit check
const checkRateLimit = async (adminId: string, action: string): Promise<boolean> => {
  const key = `rate_limit:${adminId}:${action}`
  const current = await redis.incr(key)
  if (current === 1) {
    await redis.expire(key, getRateLimitWindow(action))
  }
  return current <= getRateLimitThreshold(action)
}
```

### Emergency Controls
```typescript
// Emergency admin capabilities for crisis management
interface EmergencyControls {
  maintenanceMode: boolean      // Disable all user access
  readOnlyMode: boolean         // Prevent all write operations
  disablePayments: boolean      // Stop payment processing
  pauseAgents: boolean          // Stop AI agent processing
  disableRegistrations: boolean // Stop new user signups
  throttleAPI: boolean          // Reduce API rate limits
  emergencyMessage: string | null // Display to all users
}

// Emergency control panel component
const EmergencyControlPanel = () => {
  const [controls, setControls] = useState<EmergencyControls>()
  
  const activateEmergency = async (control: keyof EmergencyControls) => {
    // Require additional authentication
    const confirmed = await confirmWithMFA()
    if (!confirmed) return
    
    // Log critical action
    await logAdminAction({
      action: `EMERGENCY_${control.toUpperCase()}_ACTIVATED`,
      severity: 'critical',
      target_type: 'system'
    })
    
    // Apply emergency control
    await supabase.from('system_config')
      .update({ [control]: true })
      .eq('id', 'emergency_controls')
  }
}
```

### Performance Monitoring
```typescript
// Real-time performance metrics dashboard
interface PerformanceMetrics {
  api: {
    latency_p50: number
    latency_p95: number
    latency_p99: number
    requests_per_second: number
    error_rate: number
  }
  database: {
    active_connections: number
    slow_queries: QueryLog[]
    replication_lag: number
    cache_hit_rate: number
  }
  infrastructure: {
    cpu_usage: number
    memory_usage: number
    disk_io: number
    network_throughput: number
  }
  application: {
    heap_size: number
    gc_pause_time: number
    event_loop_lag: number
    worker_pool_size: number
  }
}

// Performance monitoring component
const PerformanceMonitor = () => {
  const [metrics, setMetrics] = useState<PerformanceMetrics>()
  const [alerts, setAlerts] = useState<PerformanceAlert[]>()
  
  // Real-time metric updates via WebSocket
  useEffect(() => {
    const ws = new WebSocket('wss://api.blog-poster.com/admin/metrics')
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      setMetrics(data.metrics)
      
      // Check for performance alerts
      if (data.metrics.api.latency_p99 > 1000) {
        setAlerts(prev => [...prev, {
          type: 'API_LATENCY_HIGH',
          severity: 'warning',
          message: 'API latency exceeding 1 second at p99'
        }])
      }
    }
    return () => ws.close()
  }, [])
  
  return (
    <div className="performance-dashboard">
      <MetricChart data={metrics?.api} title="API Performance" />
      <MetricChart data={metrics?.database} title="Database Health" />
      <MetricChart data={metrics?.infrastructure} title="Infrastructure" />
      <AlertsList alerts={alerts} />
    </div>
  )
}
```

### Database Tables Required

```sql
-- Admin audit logs table
CREATE TABLE admin_audit_logs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  admin_id UUID REFERENCES auth.users(id) NOT NULL,
  action VARCHAR(255) NOT NULL,
  target_type VARCHAR(50) NOT NULL,
  target_id VARCHAR(255),
  details JSONB,
  ip_address INET,
  user_agent TEXT,
  severity VARCHAR(20) DEFAULT 'info',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create index for efficient querying
CREATE INDEX idx_admin_audit_logs_admin_id ON admin_audit_logs(admin_id);
CREATE INDEX idx_admin_audit_logs_created_at ON admin_audit_logs(created_at DESC);
CREATE INDEX idx_admin_audit_logs_target ON admin_audit_logs(target_type, target_id);

-- System configuration table for emergency controls
CREATE TABLE system_config (
  id VARCHAR(50) PRIMARY KEY,
  config JSONB NOT NULL,
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  updated_by UUID REFERENCES auth.users(id)
);

-- Insert default emergency controls
INSERT INTO system_config (id, config) VALUES (
  'emergency_controls',
  '{
    "maintenanceMode": false,
    "readOnlyMode": false,
    "disablePayments": false,
    "pauseAgents": false,
    "disableRegistrations": false,
    "throttleAPI": false,
    "emergencyMessage": null
  }'::jsonb
);

-- Admin roles table
CREATE TABLE admin_roles (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id) UNIQUE NOT NULL,
  role VARCHAR(50) NOT NULL,
  permissions JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  created_by UUID REFERENCES auth.users(id)
);

-- Rate limiting table
CREATE TABLE rate_limits (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  admin_id UUID REFERENCES auth.users(id) NOT NULL,
  action VARCHAR(100) NOT NULL,
  count INTEGER DEFAULT 0,
  window_start TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(admin_id, action, window_start)
);

-- Platform metrics snapshots for historical analysis
CREATE TABLE platform_metrics (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  metric_type VARCHAR(50) NOT NULL,
  metric_data JSONB NOT NULL,
  recorded_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create RLS policies for admin tables
ALTER TABLE admin_audit_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE system_config ENABLE ROW LEVEL SECURITY;
ALTER TABLE admin_roles ENABLE ROW LEVEL SECURITY;

-- Only platform admins can read audit logs
CREATE POLICY "Platform admins can read audit logs" ON admin_audit_logs
  FOR SELECT USING (
    EXISTS (
      SELECT 1 FROM admin_roles
      WHERE user_id = auth.uid()
      AND role IN ('platform_admin', 'technical_admin')
    )
  );

-- Only platform admins can modify system config
CREATE POLICY "Platform admins can modify system config" ON system_config
  FOR ALL USING (
    EXISTS (
      SELECT 1 FROM admin_roles
      WHERE user_id = auth.uid()
      AND role = 'platform_admin'
    )
  );
```

### Success Criteria
✅ **Comprehensive Oversight**: Complete platform visibility and control
✅ **Real-time Monitoring**: Live system health and performance tracking
✅ **Efficient Operations**: Streamlined admin workflows and bulk actions
✅ **Data-Driven Decisions**: Rich analytics and reporting capabilities
✅ **Security Focused**: Robust audit trails and access controls with rate limiting
✅ **Emergency Ready**: Quick crisis management with emergency controls
✅ **Performance Tracking**: Real-time metrics with p50/p95/p99 latency monitoring
✅ **Audit Compliant**: Complete admin action logging with IP tracking
✅ **Scalable Design**: Handles growth from startup to enterprise scale
✅ **Mobile Responsive**: Full admin capabilities on mobile devices
✅ **Integration Ready**: Connects with external monitoring and support tools
✅ **Compliance Ready**: Meets enterprise security and audit requirements
✅ **User Friendly**: Intuitive interface for complex administrative tasks

This admin dashboard provides enterprise-grade platform management capabilities with advanced security features, enabling administrators to efficiently operate and scale the Blog-Poster SaaS platform while maintaining security, compliance, and excellent customer experience.
# Lovable Prompt: Team Management - Collaboration Features

## Business Context
Create a comprehensive team management system for Blog-Poster that enables organizations to collaborate effectively on content creation. This includes member management, role-based permissions, activity tracking, and team productivity analytics.

## Team Roles & Permissions
- **Owner**: Full access to everything including billing and organization settings
- **Admin**: Manage team, content, and settings (no billing access)  
- **Editor**: Create and edit all content, manage workflows
- **Member**: Create own content, basic collaboration features
- **Viewer**: Read-only access to content and analytics

## User Stories
- "As an owner, I want to invite team members and assign appropriate roles"
- "As an admin, I want to see team productivity and manage permissions"
- "As a team member, I want to collaborate on content creation efficiently"
- "As a manager, I want to track team activity and content performance"

## Prompt for Lovable

Create a complete team management system for Blog-Poster that enables seamless collaboration, role-based access control, and team productivity tracking. This system should feel like a modern team collaboration platform.

### Team Management Routes Structure

```typescript
// Team routes in App.tsx
<Route path="/team" element={<Team />} />
<Route path="/team/members" element={<TeamMembers />} />
<Route path="/team/invite" element={<InviteTeam />} />
<Route path="/team/roles" element={<TeamRoles />} />
<Route path="/team/activity" element={<TeamActivity />} />
<Route path="/team/settings" element={<TeamSettings />} />
```

### 1. Team Overview (/team)
```typescript
// src/pages/team/Team.tsx
<TeamOverview>
  Header:
    - "Team Collaboration"
    - "Manage your content creation team"
  
  Team Stats Cards:
    
    Card 1: "Team Members"
    - Total: "8 active members"
    - Recently added: "+2 this month"
    - Breakdown by role: "1 Owner, 2 Admins, 3 Editors, 2 Members"
    - CTA: "Invite Members"
    
    Card 2: "Team Activity"
    - Articles this month: "47 articles"
    - Active contributors: "6/8 members"
    - Top contributor: "Sarah Chen (12 articles)"
    - Activity trend: "+23% vs last month"
    
    Card 3: "Collaboration Score"
    - Score: "85/100"
    - Metrics: "Response time, contribution balance, quality"
    - Status: "Excellent collaboration"
    - "View details →"
    
    Card 4: "Team Costs"
    - API costs: "$156.78 this month"
    - Cost per article: "$3.34 average"
    - Budget utilization: "62% of $250 budget"
    - Cost trend: "-12% vs last month"
  
  Recent Team Activity:
    - Timeline of recent actions
    - "Sarah created 'SEO Best Practices 2024'"
    - "Mike invited john@company.com"
    - "Lisa published 'WordPress Security Guide'"
    - "Team reached 50 articles milestone"
    - Show last 10 activities with timestamps
  
  Active Team Members:
    - Avatar grid of active members
    - Online status indicators
    - Hover cards with role and last activity
    - "Currently working on..." status
    - Quick message/collaborate buttons
  
  Team Performance Chart:
    - 30-day article production trend
    - Individual contribution breakdown
    - Quality metrics over time
    - Team velocity indicators
  
  Quick Actions:
    - "Invite Team Members"
    - "Assign Content Tasks"
    - "Review Team Settings"
    - "Export Team Report"
    - "Schedule Team Meeting"
  
  Team Milestones:
    - "🎉 50 Articles Published This Quarter"
    - "⭐ 95% Average SEO Score"
    - "🚀 Team Doubled in Size"
    - "💰 Stayed Under Budget 3 Months"
</TeamOverview>
```

### 2. Team Members Management (/team/members)
```typescript
// src/pages/team/TeamMembers.tsx
<TeamMembersManagement>
  Header:
    - "Team Members"
    - "Manage roles, permissions, and member access"
  
  Member Actions Toolbar:
    - Search/filter members
    - Role filter dropdown
    - Status filter: "All", "Active", "Invited", "Inactive"
    - Sort options: "Name", "Role", "Last Active", "Articles Created"
    - "Invite Members" button
    - "Export Member List"
  
  Members Grid/List View:
    
    For each member display:
    
    Member Card:
    - Profile avatar with online status
    - Full name and email
    - Role badge with color coding
    - Join date: "Member since March 2023"
    - Last active: "2 hours ago" / "Yesterday" / "3 days ago"
    - Activity stats: "12 articles, 95% quality score"
    
    Quick Stats:
    - Articles created this month
    - Average SEO score
    - Collaboration rating
    - Cost attribution
    
    Actions Menu:
    - "Change Role" dropdown
    - "Send Message" 
    - "View Profile"
    - "View Articles"
    - "Remove from Team" (if permissions allow)
    - "Resend Invitation" (for pending invites)
  
  Pending Invitations Section:
    - Separate section for pending invites
    - Email, role, invited by, date sent
    - "Resend" and "Cancel" options
    - Invitation expiry status
    - Bulk actions for multiple invites
  
  Member Details Modal:
    - Full member profile view
    - Activity timeline
    - Articles created list
    - Performance metrics
    - Cost breakdown
    - Team interactions
    - Permission management
    - Contact information
  
  Role Management:
    - Bulk role changes
    - Role transition workflows
    - Permission inheritance explanation
    - Role change audit log
    - Approval requirements for sensitive roles
  
  Member Filters & Search:
    - Real-time search by name/email
    - Filter by role, activity level, join date
    - Advanced filters: "No articles yet", "High performers", "Needs attention"
    - Saved filter presets
  
  Team Insights:
    - Member engagement scores
    - Contribution distribution chart
    - Onboarding completion status
    - Training/certification tracking
</TeamMembersManagement>
```

### 3. Team Invitations (/team/invite)
```typescript
// src/pages/team/InviteTeam.tsx
<TeamInvitations>
  Header:
    - "Invite Team Members"
    - "Grow your content creation team"
  
  Invitation Methods:
    
    Tab 1: "Email Invitations"
    - Email addresses input (comma-separated or one per line)
    - Role selection for all invites
    - Personal message customization
    - Invitation expiry settings
    - "Send Invitations" button
    
    Tab 2: "Invite Link"
    - Generate shareable invite link
    - Link expiry settings (24h, 7 days, 30 days, never)
    - Usage limit (1 use, 5 uses, unlimited)
    - Role pre-selection
    - Copy link button
    - QR code generation
    
    Tab 3: "Bulk Import"
    - CSV upload with name, email, role columns
    - Template download
    - Preview before sending
    - Batch processing status
  
  Role Selection & Explanation:
    - Visual role cards with permissions
    - "What can this role do?" expandable sections
    - Permission matrix comparison
    - Default role recommendations
    - Custom role creation (if available)
  
  Invitation Customization:
    - Organization branding on emails
    - Custom welcome message
    - Onboarding flow selection
    - Team introduction materials
    - Getting started resources
  
  Advanced Options:
    - Require admin approval for joins
    - Domain restrictions (only @company.com)
    - Auto-assignment to specific projects
    - Default notification preferences
    - Mandatory training requirements
  
  Invitation Preview:
    - Live preview of invitation email
    - Mobile and desktop views
    - Customization options
    - Subject line editing
    - Sender information
  
  Pending Invitations Management:
    - List of all pending invites
    - Status tracking: "Sent", "Viewed", "Bounced"
    - Resend options with tracking
    - Bulk actions: resend, cancel, modify
    - Invitation analytics
  
  Team Growth Analytics:
    - Invitation success rates
    - Time to acceptance metrics
    - Most effective invitation methods
    - Team growth projections
    - Onboarding completion rates
  
  Security Features:
    - Email verification requirements
    - Two-factor authentication options
    - IP restrictions (for enterprise)
    - Background check integrations
    - Compliance tracking
</TeamInvitations>
```

### 4. Role Management (/team/roles)
```typescript
// src/pages/team/TeamRoles.tsx
<RoleManagement>
  Header:
    - "Roles & Permissions"
    - "Define what team members can do"
  
  Role Overview Cards:
    
    Owner Role:
    - "Organization Owner"
    - Members: "1 member (you)"
    - Key permissions: "Full access to everything"
    - Cannot be changed or removed
    - Billing and legal responsibilities
    
    Admin Role:
    - "Administrators" 
    - Members: "2 members"
    - Key permissions: "Team management, all content"
    - "Manage permissions" button
    - Activity overview
    
    Editor Role:
    - "Content Editors"
    - Members: "3 members"
    - Key permissions: "Create/edit content, workflows"
    - "Manage permissions" button
    - Productivity metrics
    
    Member Role:
    - "Team Members"
    - Members: "2 members" 
    - Key permissions: "Create own content"
    - "Manage permissions" button
    - Contribution stats
    
    Viewer Role:
    - "Content Viewers"
    - Members: "0 members"
    - Key permissions: "Read-only access"
    - "Manage permissions" button
    - Usage analytics
  
  Detailed Permissions Matrix:
    
    Permissions by category:
    
    Content Management:
    - Create articles: Owner ✓, Admin ✓, Editor ✓, Member ✓, Viewer ✗
    - Edit any article: Owner ✓, Admin ✓, Editor ✓, Member (own), Viewer ✗
    - Delete articles: Owner ✓, Admin ✓, Editor ✓, Member (own), Viewer ✗
    - Publish articles: Owner ✓, Admin ✓, Editor ✓, Member (with approval), Viewer ✗
    
    Team Management:
    - Invite members: Owner ✓, Admin ✓, Editor ✗, Member ✗, Viewer ✗
    - Change roles: Owner ✓, Admin (limited), Editor ✗, Member ✗, Viewer ✗
    - Remove members: Owner ✓, Admin (limited), Editor ✗, Member ✗, Viewer ✗
    
    Organization Settings:
    - Billing & subscription: Owner ✓, Admin ✗, Editor ✗, Member ✗, Viewer ✗
    - API keys management: Owner ✓, Admin ✓, Editor ✗, Member ✗, Viewer ✗
    - WordPress connections: Owner ✓, Admin ✓, Editor ✓, Member ✗, Viewer ✗
    
    Analytics & Reporting:
    - View team analytics: Owner ✓, Admin ✓, Editor ✓, Member (limited), Viewer (limited)
    - Export data: Owner ✓, Admin ✓, Editor ✓, Member ✗, Viewer ✗
    - Cost tracking: Owner ✓, Admin ✓, Editor (view), Member ✗, Viewer ✗
  
  Custom Roles (Enterprise):
    - "Create Custom Role" button
    - Role name and description
    - Granular permission selection
    - Role templates library
    - Permission inheritance
    - Approval workflows
  
  Role Change Workflows:
    - Approval requirements for promotions
    - Automatic role transitions
    - Probationary periods
    - Role change notifications
    - Audit trail maintenance
  
  Permission Explanations:
    - Hover tooltips for each permission
    - "Why does this matter?" explanations
    - Security implications
    - Best practice recommendations
    - Compliance considerations
  
  Role Analytics:
    - Permission usage statistics
    - Role effectiveness metrics
    - Security incident tracking
    - Access pattern analysis
    - Compliance reporting
</RoleManagement>
```

### 5. Team Activity (/team/activity)
```typescript
// src/pages/team/TeamActivity.tsx
<TeamActivity>
  Header:
    - "Team Activity"
    - "Track collaboration and productivity"
  
  Activity Filters:
    - Date range picker (today, week, month, quarter, custom)
    - Team member filter (all, specific members)
    - Activity type: "All", "Articles", "Comments", "Reviews", "Admin"
    - Action filter: "Created", "Updated", "Published", "Deleted"
    - Search by content or keywords
  
  Activity Feed:
    
    Activity Item Structure:
    - User avatar and name
    - Action description with context
    - Timestamp (relative and absolute)
    - Content preview/link
    - Impact metrics (if applicable)
    - Collaboration indicators
    
    Example Activities:
    - "Sarah Chen created 'WordPress Security Best Practices'"
      - "2 hours ago • 1,847 words • SEO score: 94"
      - Quick actions: View, Edit, Comment
    
    - "Mike Rodriguez published 'E-commerce SEO Guide'"
      - "Yesterday • Generated $12.50 API cost • Status: Live"
      - Performance preview: "43 views, 12 clicks"
    
    - "Lisa Park commented on 'Content Marketing Trends'"
      - "3 days ago • Suggested SEO improvements"
      - Comment preview with reply options
    
    - "Team milestone: 50 articles published this quarter"
      - "1 week ago • +67% growth vs last quarter"
      - Celebration animation and sharing options
  
  Team Productivity Dashboard:
    
    Chart 1: "Daily Activity Heatmap"
    - Calendar view of team activity
    - Color intensity based on activity level
    - Hover details for specific days
    - Pattern recognition for peak times
    
    Chart 2: "Member Contribution"
    - Bar chart of articles per member
    - Quality scores overlay
    - Trend indicators (up/down arrows)
    - Target vs actual performance
    
    Chart 3: "Collaboration Network"
    - Visual map of member interactions
    - Comment threads and reviews
    - Knowledge sharing patterns
    - Mentor-mentee relationships
  
  Performance Metrics:
    
    Team KPIs:
    - Articles published: "47 this month (+23%)"
    - Average SEO score: "92/100 (+3 points)"
    - Collaboration score: "85% (Excellent)"
    - Response time: "2.3 hours average"
    
    Individual Highlights:
    - Top performer: "Sarah Chen - 12 articles"
    - Quality leader: "Mike Rodriguez - 97 avg score"
    - Best collaborator: "Lisa Park - 85 interactions"
    - Most improved: "John Smith - +15% quality"
  
  Activity Analytics:
    - Peak activity hours identification
    - Most productive days analysis
    - Collaboration patterns discovery
    - Content type preferences
    - Geographic activity distribution (if remote team)
  
  Activity Notifications:
    - Real-time activity updates
    - Mention notifications
    - Milestone celebrations
    - Deadline reminders
    - Performance alerts
  
  Export & Reporting:
    - Activity report generation
    - Custom date range exports
    - Team performance summaries
    - Individual activity reports
    - Compliance audit trails
</TeamActivity>
```

### 6. Team Settings (/team/settings)
```typescript
// src/pages/team/TeamSettings.tsx
<TeamSettings>
  Header:
    - "Team Settings"
    - "Configure team collaboration preferences"
  
  General Team Settings:
    
    Organization Information:
    - Organization name
    - Team description/mission
    - Time zone settings
    - Default working hours
    - Holiday calendar
    - Contact information
    
    Team Preferences:
    - Default content language
    - Content approval workflows
    - Quality thresholds
    - Collaboration guidelines
    - Communication preferences
  
  Workflow Configuration:
    
    Content Approval Process:
    - "Require approval for publishing": Toggle
    - Approval roles: "Admin and Editor roles can approve"
    - Auto-approval rules: "Articles with 90+ SEO score"
    - Approval timeouts: "72 hours default"
    - Escalation procedures
    
    Quality Standards:
    - Minimum SEO score: "85/100"
    - Word count requirements: "1,500+ words"
    - Readability standards: "Grade 8 reading level"
    - Fact-checking requirements: "Legal review for compliance"
    - Brand voice guidelines
    
    Collaboration Rules:
    - Comment requirements: "Peer review for all articles"
    - Review assignments: "Auto-assign by expertise"
    - Feedback timeframes: "48 hour response time"
    - Conflict resolution process
  
  Notification Settings:
    
    Team Notifications:
    - New member joined
    - Articles published
    - Milestones achieved
    - Performance alerts
    - System updates
    
    Individual Preferences:
    - Email frequency: "Real-time", "Daily digest", "Weekly summary"
    - Slack/Discord integration
    - Mobile push notifications
    - Browser notifications
    - Do not disturb schedules
  
  Integration Settings:
    
    Communication Tools:
    - Slack workspace connection
    - Discord server integration
    - Microsoft Teams setup
    - Email distribution lists
    - Video conferencing preferences
    
    Project Management:
    - Trello board sync
    - Asana project integration
    - Monday.com workflows
    - Notion workspace connection
    - Custom webhook endpoints
  
  Security & Access:
    
    Access Controls:
    - Two-factor authentication requirement
    - Session timeout settings
    - IP address restrictions
    - Device management
    - API access controls
    
    Data Protection:
    - Data retention policies
    - Export/backup procedures
    - GDPR compliance settings
    - Privacy preferences
    - Audit log retention
  
  Team Analytics Settings:
    
    Tracking Preferences:
    - Activity monitoring level
    - Performance metrics collection
    - Privacy-sensitive data handling
    - Analytics sharing permissions
    - Report generation frequency
    
    Custom Metrics:
    - Define team KPIs
    - Goal setting and tracking
    - Benchmark comparisons
    - Alert thresholds
    - Success celebrations
  
  Advanced Settings:
    
    API Configuration:
    - Team API key management
    - Usage quotas per member
    - Cost allocation rules
    - Backup API providers
    - Rate limiting settings
    
    Customization:
    - Team branding/colors
    - Custom field definitions
    - Workflow templates
    - Automated actions
    - Integration triggers
</TeamSettings>
```

### Shared Team Components

#### Team Member Card
```typescript
// src/components/team/TeamMemberCard.tsx
<TeamMemberCard>
  - Avatar with online status
  - Name, role, and badge
  - Activity indicators
  - Quick action buttons
  - Performance metrics
  - Hover state with details
</TeamMemberCard>
```

#### Role Badge Component
```typescript
// src/components/team/RoleBadge.tsx
<RoleBadge>
  - Color-coded role indicators
  - Permission level visualization
  - Hover tooltips with details
  - Role change animations
  - Hierarchy indicators
</RoleBadge>
```

#### Activity Timeline
```typescript
// src/components/team/ActivityTimeline.tsx
<ActivityTimeline>
  - Chronological activity feed
  - Grouped by time periods
  - User avatars and actions
  - Content previews
  - Interactive elements
</ActivityTimeline>
```

#### Team Analytics Charts
```typescript
// src/components/team/TeamCharts.tsx
<TeamCharts>
  - Productivity trend charts
  - Collaboration network graphs
  - Performance comparison bars
  - Activity heatmaps
  - Goal progress indicators
</TeamCharts>
```

### Team Store Management
```typescript
// src/stores/teamStore.ts
interface TeamState {
  members: TeamMemberData[]
  invitations: InvitationData[]
  roles: RoleData[]
  activities: ActivityData[]
  settings: TeamSettingsData
  analytics: TeamAnalyticsData
}

// Real-time team activity updates
// Role-based permission enforcement
// Activity tracking and logging
// Team performance calculations
```

### Real-time Features
```typescript
// WebSocket integration for live updates
- Member online/offline status
- Real-time activity feed
- Live collaboration indicators
- Instant notifications
- Concurrent editing awareness
```

### Permission Enforcement
```typescript
// Component-level permission checks
- Route-based access control
- Feature-level restrictions
- Data visibility controls
- Action authorization
- Audit trail generation
```

### Success Criteria
✅ **Intuitive Collaboration**: Easy team member management
✅ **Clear Permissions**: Transparent role-based access control
✅ **Activity Transparency**: Comprehensive activity tracking
✅ **Performance Insights**: Team productivity analytics
✅ **Flexible Roles**: Customizable permission systems
✅ **Real-time Updates**: Live collaboration features
✅ **Secure Access**: Robust security and audit trails
✅ **Scalable Structure**: Supports teams from 2 to 200+ members
✅ **Mobile Ready**: Full mobile team management experience
✅ **Integration Friendly**: Connects with popular team tools

This team management system provides everything needed for effective collaboration on content creation, with the flexibility to scale from small teams to large organizations while maintaining security and transparency.
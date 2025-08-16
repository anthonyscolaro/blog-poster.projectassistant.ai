import { useState, useEffect } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Link, useNavigate } from 'react-router-dom'
import { supabase } from '@/services/supabase'
import { useAuth } from '@/contexts/AuthContext'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { 
  Users, 
  TrendingUp, 
  DollarSign, 
  Activity,
  Plus,
  MessageCircle,
  Clock,
  CheckCircle,
  Star,
  Target,
  Zap
} from 'lucide-react'
import { TeamMemberCard } from '@/components/team/TeamMemberCard'
import { ActivityTimeline } from '@/components/team/ActivityTimeline'
import { TeamCharts } from '@/components/team/TeamCharts'

export default function Team() {
  const { organization } = useAuth()
  const navigate = useNavigate()

  // Query team members
  const { data: teamMembers } = useQuery({
    queryKey: ['team-members', organization?.id],
    queryFn: async () => {
      const { data, error } = await supabase
        .from('profiles')
        .select('*')
        .eq('organization_id', organization!.id)
        .order('created_at', { ascending: false })

      if (error) throw error
      return data
    },
    enabled: !!organization?.id
  })

  // Query team stats
  const { data: teamStats } = useQuery({
    queryKey: ['team-stats', organization?.id],
    queryFn: async () => {
      const [articlesResult, costResult] = await Promise.all([
        supabase
          .from('articles')
          .select('id, status, seo_score, generation_cost, user_id, created_at')
          .eq('organization_id', organization!.id)
          .gte('created_at', new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString()),
        
        supabase
          .from('cost_tracking')
          .select('amount')
          .eq('organization_id', organization!.id)
          .gte('created_at', new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString())
      ])

      const articles = articlesResult.data || []
      const costs = costResult.data || []

      const publishedArticles = articles.filter(a => a.status === 'published')
      const totalCost = costs.reduce((sum, c) => sum + (c.amount || 0), 0)
      const avgSeoScore = articles.length 
        ? Math.round(articles.reduce((sum, a) => sum + (a.seo_score || 0), 0) / articles.length)
        : 0

      // Calculate contributor stats
      const contributorStats = articles.reduce((acc, article) => {
        acc[article.user_id] = (acc[article.user_id] || 0) + 1
        return acc
      }, {} as Record<string, number>)

      const topContributor = Object.entries(contributorStats)
        .sort(([,a], [,b]) => b - a)[0]

      return {
        totalArticles: articles.length,
        publishedArticles: publishedArticles.length,
        avgSeoScore,
        totalCost,
        costPerArticle: articles.length ? totalCost / articles.length : 0,
        activeContributors: Object.keys(contributorStats).length,
        topContributorId: topContributor?.[0],
        topContributorCount: topContributor?.[1] || 0
      }
    },
    enabled: !!organization?.id
  })

  // Query recent activity
  const { data: recentActivity } = useQuery({
    queryKey: ['team-activity', organization?.id],
    queryFn: async () => {
      const { data, error } = await supabase
        .from('audit_logs')
        .select('*')
        .eq('organization_id', organization!.id)
        .order('created_at', { ascending: false })
        .limit(10)

      if (error) throw error
      return data || []
    },
    enabled: !!organization?.id
  })

  const getCollaborationScore = () => {
    if (!teamStats || !teamMembers) return 0
    
    // Simple collaboration score based on activity distribution
    const memberCount = teamMembers.length
    const activeContributors = teamStats.activeContributors
    
    if (memberCount === 0) return 0
    
    const activityDistribution = (activeContributors / memberCount) * 100
    const qualityScore = teamStats.avgSeoScore
    
    return Math.round((activityDistribution * 0.6 + qualityScore * 0.4))
  }

  const collaborationScore = getCollaborationScore()

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-foreground mb-2">
            Team Collaboration
          </h1>
          <p className="text-muted-foreground">
            Manage your content creation team and track productivity
          </p>
        </div>

        <div className="flex items-center gap-3">
          <Button 
            variant="outline"
            onClick={() => navigate('/team/activity')}
          >
            <Activity className="h-4 w-4 mr-2" />
            View Activity
          </Button>
          <Button
            onClick={() => navigate('/team/invite')}
            className="bg-gradient-to-r from-purple-600 to-blue-600 text-white"
          >
            <Plus className="h-4 w-4 mr-2" />
            Invite Members
          </Button>
        </div>
      </div>

      {/* Team Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {/* Team Members */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Team Members</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{teamMembers?.length || 0}</div>
            <p className="text-xs text-muted-foreground">
              +2 this month
            </p>
            <div className="mt-2 text-xs text-muted-foreground">
              {teamMembers && (
                <>
                  {teamMembers.filter(m => m.role === 'owner').length} Owner, {' '}
                  {teamMembers.filter(m => m.role === 'admin').length} Admin, {' '}
                  {teamMembers.filter(m => m.role === 'editor').length} Editor, {' '}
                  {teamMembers.filter(m => m.role === 'member').length} Member
                </>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Team Activity */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Team Activity</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{teamStats?.totalArticles || 0}</div>
            <p className="text-xs text-muted-foreground">
              articles this month
            </p>
            <div className="mt-2 text-xs text-muted-foreground">
              {teamStats?.activeContributors || 0}/{teamMembers?.length || 0} active contributors
            </div>
          </CardContent>
        </Card>

        {/* Collaboration Score */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Collaboration Score</CardTitle>
            <Star className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{collaborationScore}/100</div>
            <p className="text-xs text-muted-foreground">
              {collaborationScore >= 80 ? 'Excellent' : collaborationScore >= 60 ? 'Good' : 'Needs attention'}
            </p>
            <div className="mt-2 text-xs text-muted-foreground">
              SEO Avg: {teamStats?.avgSeoScore || 0}/100
            </div>
          </CardContent>
        </Card>

        {/* Team Costs */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Team Costs</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">${teamStats?.totalCost.toFixed(2) || '0.00'}</div>
            <p className="text-xs text-muted-foreground">
              this month
            </p>
            <div className="mt-2 text-xs text-muted-foreground">
              ${teamStats?.costPerArticle.toFixed(2) || '0.00'} per article
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Recent Team Activity */}
        <div className="lg:col-span-2">
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle>Recent Team Activity</CardTitle>
                <Link to="/team/activity">
                  <Button variant="outline" size="sm">
                    View All
                  </Button>
                </Link>
              </div>
            </CardHeader>
            <CardContent>
              <ActivityTimeline activities={recentActivity || []} limit={5} />
            </CardContent>
          </Card>
        </div>

        {/* Active Team Members */}
        <div>
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle>Active Members</CardTitle>
                <Link to="/team/members">
                  <Button variant="outline" size="sm">
                    Manage
                  </Button>
                </Link>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              {teamMembers?.slice(0, 5).map((member) => (
                <div key={member.id} className="flex items-center gap-3">
                  <Avatar className="h-8 w-8">
                    <AvatarImage src={member.avatar_url} />
                    <AvatarFallback>
                      {member.full_name?.split(' ').map(n => n[0]).join('') || 'U'}
                    </AvatarFallback>
                  </Avatar>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium truncate">
                      {member.full_name || member.email}
                    </p>
                    <p className="text-xs text-muted-foreground">
                      {member.role}
                    </p>
                  </div>
                  <div className="flex items-center gap-1">
                    <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                    <span className="text-xs text-muted-foreground">Online</span>
                  </div>
                </div>
              ))}
              
              {teamMembers && teamMembers.length > 5 && (
                <div className="text-center pt-2">
                  <Link to="/team/members">
                    <Button variant="ghost" size="sm">
                      +{teamMembers.length - 5} more members
                    </Button>
                  </Link>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Quick Actions */}
          <Card className="mt-6">
            <CardHeader>
              <CardTitle>Quick Actions</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <Button 
                variant="outline" 
                className="w-full justify-start"
                onClick={() => navigate('/team/invite')}
              >
                <Plus className="h-4 w-4 mr-2" />
                Invite Team Members
              </Button>
              <Button 
                variant="outline" 
                className="w-full justify-start"
                onClick={() => navigate('/team/roles')}
              >
                <Users className="h-4 w-4 mr-2" />
                Manage Roles
              </Button>
              <Button 
                variant="outline" 
                className="w-full justify-start"
                onClick={() => navigate('/team/settings')}
              >
                <Zap className="h-4 w-4 mr-2" />
                Team Settings
              </Button>
            </CardContent>
          </Card>

          {/* Team Milestones */}
          <Card className="mt-6">
            <CardHeader>
              <CardTitle>Team Milestones</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="flex items-center gap-2 text-sm">
                <span className="text-lg">🎉</span>
                <span>{teamStats?.publishedArticles || 0} Articles Published</span>
              </div>
              <div className="flex items-center gap-2 text-sm">
                <span className="text-lg">⭐</span>
                <span>{teamStats?.avgSeoScore || 0}% Average SEO Score</span>
              </div>
              <div className="flex items-center gap-2 text-sm">
                <span className="text-lg">🚀</span>
                <span>Team of {teamMembers?.length || 0} Members</span>
              </div>
              <div className="flex items-center gap-2 text-sm">
                <span className="text-lg">💰</span>
                <span>Budget: ${teamStats?.totalCost.toFixed(2) || '0.00'} this month</span>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
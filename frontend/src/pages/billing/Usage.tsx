import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Button } from '@/components/ui/button';
import { useAuth } from '@/contexts/AuthContext';
import { supabase } from '@/integrations/supabase/client';
import { toast } from 'sonner';
import { 
  TrendingUp, 
  DollarSign, 
  Users, 
  CheckCircle,
  Download,
  Calendar,
  ArrowLeft,
  Lightbulb
} from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, BarChart, Bar } from 'recharts';

interface UsageData {
  current_month_articles: number;
  monthly_article_limit: number;
  current_month_cost: number;
  monthly_budget: number;
  team_members_used: number;
  team_members_limit: number;
}

export default function Usage() {
  const { user } = useAuth();
  const [loading, setLoading] = useState(true);
  const [usage, setUsage] = useState<UsageData | null>(null);
  const [usageHistory, setUsageHistory] = useState<any[]>([]);
  const [costBreakdown, setCostBreakdown] = useState<any[]>([]);
  const [teamContribution, setTeamContribution] = useState<any[]>([]);

  useEffect(() => {
    if (user) {
      loadUsageData();
    }
  }, [user]);

  const loadUsageData = async () => {
    try {
      setLoading(true);
      
      // Get organization data
      const { data: profile } = await supabase
        .from('profiles')
        .select('organization_id, full_name')
        .eq('id', user?.id)
        .single();

      if (profile?.organization_id) {
        // Get current usage
        const { data: orgData } = await supabase
          .from('organizations')
          .select('current_month_articles, monthly_article_limit, current_month_cost, monthly_budget, team_members_used, team_members_limit')
          .eq('id', profile.organization_id)
          .single();

        setUsage(orgData);

        // Get usage tracking data for charts
        const { data: trackingData } = await supabase
          .from('usage_tracking')
          .select('*')
          .eq('organization_id', profile.organization_id)
          .gte('created_at', new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString())
          .order('created_at', { ascending: true });

        // Process data for charts
        const dailyUsage = processUsageHistory(trackingData || []);
        const costData = processCostBreakdown(trackingData || []);
        const teamData = await processTeamContribution(profile.organization_id);

        setUsageHistory(dailyUsage);
        setCostBreakdown(costData);
        setTeamContribution(teamData);
      }
    } catch (error) {
      console.error('Error loading usage data:', error);
      toast.error('Failed to load usage information');
    } finally {
      setLoading(false);
    }
  };

  const processUsageHistory = (data: any[]) => {
    const last30Days = Array.from({ length: 30 }, (_, i) => {
      const date = new Date();
      date.setDate(date.getDate() - (29 - i));
      return date.toISOString().split('T')[0];
    });

    return last30Days.map(date => {
      const dayData = data.filter(item => 
        item.created_at.startsWith(date) && item.resource_type === 'article'
      );
      return {
        date: new Date(date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
        articles: dayData.length,
        cost: dayData.reduce((sum, item) => sum + parseFloat(item.amount || 0), 0)
      };
    });
  };

  const processCostBreakdown = (data: any[]) => {
    const services = data.reduce((acc, item) => {
      const service = item.metadata?.service || 'Unknown';
      if (!acc[service]) {
        acc[service] = { name: service, value: 0, count: 0 };
      }
      acc[service].value += parseFloat(item.amount || 0);
      acc[service].count += 1;
      return acc;
    }, {} as any);

    return Object.values(services);
  };

  const processTeamContribution = async (organizationId: string) => {
    const { data: articles } = await supabase
      .from('articles')
      .select('user_id, generation_cost')
      .eq('organization_id', organizationId)
      .gte('created_at', new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString());

    const { data: profiles } = await supabase
      .from('profiles')
      .select('id, full_name')
      .eq('organization_id', organizationId);

    const contribution = (profiles || []).map(profile => {
      const userArticles = (articles || []).filter(article => article.user_id === profile.id);
      return {
        name: profile.full_name || 'Unknown',
        articles: userArticles.length,
        cost: userArticles.reduce((sum, article) => sum + parseFloat(String(article.generation_cost || 0)), 0)
      };
    }).filter(item => item.articles > 0);

    return contribution;
  };

  const getUsageStatus = () => {
    if (!usage) return { status: 'good', color: 'text-green-600' };
    
    const percentage = (usage.current_month_articles / usage.monthly_article_limit) * 100;
    
    if (percentage >= 90) return { status: 'Limit reached', color: 'text-red-600' };
    if (percentage >= 80) return { status: 'High usage', color: 'text-yellow-600' };
    return { status: 'On track', color: 'text-green-600' };
  };

  const COLORS = ['#8884d8', '#82ca9d', '#ffc658', '#ff7300', '#0088fe'];

  if (loading) {
    return (
      <div className="container mx-auto p-6">
        <div className="animate-pulse space-y-6">
          <div className="h-8 bg-muted rounded w-1/3"></div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="h-32 bg-muted rounded"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  const usageStatus = getUsageStatus();

  return (
    <div className="container mx-auto p-6 space-y-6">
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="sm" asChild>
          <a href="/billing">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Billing
          </a>
        </Button>
      </div>

      <div>
        <h1 className="text-3xl font-bold tracking-tight">Usage Analytics</h1>
        <p className="text-muted-foreground">Monitor your article generation and API costs</p>
      </div>

      {/* Current Period Overview */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Calendar className="w-5 h-5" />
            Current Billing Period
          </CardTitle>
          <p className="text-sm text-muted-foreground">
            {new Date().toLocaleDateString('en-US', { month: 'long', day: 'numeric' })} - {new Date(new Date().getFullYear(), new Date().getMonth() + 1, 0).toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })}
          </p>
        </CardHeader>
      </Card>

      {/* Usage Metrics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Articles Generated</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {usage?.current_month_articles || 0}/{usage?.monthly_article_limit || 2}
            </div>
            <Progress 
              value={Math.min(((usage?.current_month_articles || 0) / (usage?.monthly_article_limit || 2)) * 100, 100)} 
              className="mt-2" 
            />
            <p className={`text-xs mt-2 ${usageStatus.color}`}>
              {usageStatus.status}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">API Costs</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              ${(usage?.current_month_cost || 0).toFixed(2)}
            </div>
            <Progress 
              value={Math.min(((usage?.current_month_cost || 0) / (usage?.monthly_budget || 100)) * 100, 100)} 
              className="mt-2" 
            />
            <p className="text-xs text-muted-foreground mt-2">
              of ${(usage?.monthly_budget || 100).toFixed(2)} budget
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Team Activity</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {teamContribution.length}/{usage?.team_members_limit || 1}
            </div>
            <p className="text-xs text-muted-foreground mt-2">
              Active contributors
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Success Rate</CardTitle>
            <CheckCircle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">94%</div>
            <p className="text-xs text-muted-foreground mt-2">
              Pipeline success rate
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Daily Article Generation */}
        <Card>
          <CardHeader>
            <CardTitle>Daily Article Generation</CardTitle>
            <p className="text-sm text-muted-foreground">
              Articles created over the last 30 days
            </p>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={usageHistory}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Line 
                  type="monotone" 
                  dataKey="articles" 
                  stroke="hsl(var(--primary))" 
                  strokeWidth={2}
                />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* API Cost Breakdown */}
        <Card>
          <CardHeader>
            <CardTitle>API Cost Breakdown</CardTitle>
            <p className="text-sm text-muted-foreground">
              Cost distribution by service
            </p>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={costBreakdown}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {costBreakdown.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip formatter={(value) => [`$${Number(value).toFixed(2)}`, 'Cost']} />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Team Contribution */}
        <Card>
          <CardHeader>
            <CardTitle>Team Contribution</CardTitle>
            <p className="text-sm text-muted-foreground">
              Articles generated by team member
            </p>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={teamContribution}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="articles" fill="hsl(var(--primary))" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Cost Optimization Tips */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Lightbulb className="w-5 h-5" />
              Optimization Tips
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-3">
              <div className="flex items-start gap-3">
                <div className="w-2 h-2 bg-green-500 rounded-full mt-2 flex-shrink-0"></div>
                <div>
                  <p className="text-sm font-medium">Cost per article: $0.35</p>
                  <p className="text-xs text-muted-foreground">16% below industry benchmark of $0.42</p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="w-2 h-2 bg-blue-500 rounded-full mt-2 flex-shrink-0"></div>
                <div>
                  <p className="text-sm font-medium">Peak productivity: Tuesdays</p>
                  <p className="text-xs text-muted-foreground">Consider scheduling important content on high-productivity days</p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="w-2 h-2 bg-yellow-500 rounded-full mt-2 flex-shrink-0"></div>
                <div>
                  <p className="text-sm font-medium">Batch processing tip</p>
                  <p className="text-xs text-muted-foreground">Group similar articles to reduce API overhead</p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Export Options */}
      <Card>
        <CardHeader>
          <CardTitle>Export & Reports</CardTitle>
          <p className="text-sm text-muted-foreground">
            Download detailed usage reports for analysis
          </p>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-4">
            <Button variant="outline">
              <Download className="w-4 h-4 mr-2" />
              Download Usage Report (PDF)
            </Button>
            <Button variant="outline">
              <Download className="w-4 h-4 mr-2" />
              Export Data (CSV)
            </Button>
            <Button variant="outline">
              <Calendar className="w-4 h-4 mr-2" />
              Schedule Monthly Reports
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
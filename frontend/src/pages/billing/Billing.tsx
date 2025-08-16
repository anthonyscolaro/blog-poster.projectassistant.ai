import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { useAuth } from '@/contexts/AuthContext';
import { supabase } from '@/integrations/supabase/client';
import { toast } from 'sonner';
import { 
  CreditCard, 
  Users, 
  DollarSign, 
  HardDrive, 
  TrendingUp,
  AlertTriangle,
  Download,
  Settings
} from 'lucide-react';

interface SubscriptionData {
  subscribed: boolean;
  subscription_tier: string;
  subscription_status: string;
  subscription_end: string | null;
}

interface UsageData {
  current_month_articles: number;
  monthly_article_limit: number;
  current_month_cost: number;
  monthly_budget: number;
  team_members_used: number;
  team_members_limit: number;
}

export default function Billing() {
  const { user } = useAuth();
  const [loading, setLoading] = useState(true);
  const [subscription, setSubscription] = useState<SubscriptionData | null>(null);
  const [usage, setUsage] = useState<UsageData | null>(null);
  const [recentActivity, setRecentActivity] = useState<any[]>([]);

  useEffect(() => {
    // Check for success/cancel parameters from Stripe
    const urlParams = new URLSearchParams(window.location.search);
    const success = urlParams.get('success');
    const canceled = urlParams.get('canceled');
    
    if (success === 'true') {
      toast.success('Subscription activated! Welcome to your new plan.');
      // Refresh subscription data
      loadBillingData();
      // Clean up URL
      window.history.replaceState({}, '', '/billing');
    } else if (canceled === 'true') {
      toast.info('Checkout canceled. You can upgrade anytime.');
      window.history.replaceState({}, '', '/billing/upgrade');
    }
    
    if (user) {
      loadBillingData();
    }
  }, [user]);

  const loadBillingData = async () => {
    try {
      setLoading(true);
      
      // Check subscription status
      const { data: subData, error: subError } = await supabase.functions.invoke('check-subscription');
      if (subError) throw subError;
      setSubscription(subData);

      // Get usage data from organization
      const { data: profile } = await supabase
        .from('profiles')
        .select('organization_id')
        .eq('id', user?.id)
        .single();

      if (profile?.organization_id) {
        const { data: orgData } = await supabase
          .from('organizations')
          .select('current_month_articles, monthly_article_limit, current_month_cost, monthly_budget, team_members_used, team_members_limit')
          .eq('id', profile.organization_id)
          .single();

        setUsage(orgData);

        // Get recent activity
        const { data: activityData } = await supabase
          .from('audit_logs')
          .select('*')
          .eq('organization_id', profile.organization_id)
          .order('created_at', { ascending: false })
          .limit(5);

        setRecentActivity(activityData || []);
      }
    } catch (error) {
      console.error('Error loading billing data:', error);
      toast.error('Failed to load billing information');
    } finally {
      setLoading(false);
    }
  };

  const openCustomerPortal = async () => {
    try {
      const { data, error } = await supabase.functions.invoke('customer-portal');
      if (error) throw error;
      
      window.open(data.url, '_blank');
    } catch (error) {
      console.error('Error opening customer portal:', error);
      toast.error('Failed to open billing portal');
    }
  };

  const getArticleUsagePercentage = () => {
    if (!usage) return 0;
    return Math.min((usage.current_month_articles / usage.monthly_article_limit) * 100, 100);
  };

  const getBudgetUsagePercentage = () => {
    if (!usage) return 0;
    return Math.min((usage.current_month_cost / usage.monthly_budget) * 100, 100);
  };

  const getPlanDisplayName = (tier: string) => {
    switch (tier) {
      case 'free': return 'Free';
      case 'starter': return 'Starter';
      case 'professional': return 'Professional';
      case 'enterprise': return 'Enterprise';
      default: return 'Free';
    }
  };

  const getPlanBadgeVariant = (tier: string) => {
    switch (tier) {
      case 'free': return 'secondary';
      case 'starter': return 'default';
      case 'professional': return 'default';
      case 'enterprise': return 'default';
      default: return 'secondary';
    }
  };

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

  return (
    <div className="container mx-auto p-6 space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Billing & Usage</h1>
        <p className="text-muted-foreground">Manage your subscription and track usage</p>
      </div>

      {/* Current Plan Card */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center gap-2">
                Current Plan
                <Badge variant={getPlanBadgeVariant(subscription?.subscription_tier || 'free')}>
                  {getPlanDisplayName(subscription?.subscription_tier || 'free')}
                </Badge>
              </CardTitle>
              <p className="text-sm text-muted-foreground mt-1">
                {subscription?.subscription_tier === 'free' 
                  ? 'Free plan with basic features'
                  : subscription?.subscription_end 
                    ? `Next billing: ${new Date(subscription.subscription_end).toLocaleDateString()}`
                    : 'Subscription active'
                }
              </p>
            </div>
            <div className="flex gap-2">
              {subscription?.subscribed ? (
                <Button onClick={openCustomerPortal} variant="outline">
                  <Settings className="w-4 h-4 mr-2" />
                  Manage
                </Button>
              ) : (
                <Button asChild>
                  <a href="/billing/upgrade">Upgrade Plan</a>
                </Button>
              )}
            </div>
          </div>
        </CardHeader>
      </Card>

      {/* Usage Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Articles This Month</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {usage?.current_month_articles || 0}/{usage?.monthly_article_limit || 2}
            </div>
            <Progress value={getArticleUsagePercentage()} className="mt-2" />
            <p className="text-xs text-muted-foreground mt-2">
              {getArticleUsagePercentage() > 80 ? (
                <span className="text-yellow-600 flex items-center gap-1">
                  <AlertTriangle className="w-3 h-3" />
                  Approaching limit
                </span>
              ) : (
                "Good usage"
              )}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Team Members</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {usage?.team_members_used || 1}/{usage?.team_members_limit || 1}
            </div>
            <p className="text-xs text-muted-foreground mt-2">
              Active team members
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
            <Progress value={getBudgetUsagePercentage()} className="mt-2" />
            <p className="text-xs text-muted-foreground mt-2">
              of ${(usage?.monthly_budget || 100).toFixed(2)} budget
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Storage Used</CardTitle>
            <HardDrive className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">2.3 GB</div>
            <Progress value={23} className="mt-2" />
            <p className="text-xs text-muted-foreground mt-2">
              of 10 GB available
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Quick Actions */}
      <div className="flex flex-wrap gap-4">
        <Button variant="outline" asChild>
          <a href="/billing/invoices">
            <Download className="w-4 h-4 mr-2" />
            Download Invoice
          </a>
        </Button>
        <Button variant="outline" asChild>
          <a href="/billing/payment">
            <CreditCard className="w-4 h-4 mr-2" />
            Payment Methods
          </a>
        </Button>
        <Button variant="outline" asChild>
          <a href="/billing/usage">
            <TrendingUp className="w-4 h-4 mr-2" />
            View Usage Analytics
          </a>
        </Button>
      </div>

      {/* Recent Activity */}
      <Card>
        <CardHeader>
          <CardTitle>Recent Activity</CardTitle>
          <p className="text-sm text-muted-foreground">
            Latest billing and usage events
          </p>
        </CardHeader>
        <CardContent>
          {recentActivity.length > 0 ? (
            <div className="space-y-3">
              {recentActivity.map((activity, index) => (
                <div key={index} className="flex items-center justify-between py-2 border-b last:border-0">
                  <div>
                    <p className="text-sm font-medium">{activity.action}</p>
                    <p className="text-xs text-muted-foreground">
                      {new Date(activity.created_at).toLocaleDateString()}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-sm text-muted-foreground">No recent activity</p>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
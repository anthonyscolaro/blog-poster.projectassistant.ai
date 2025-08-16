import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Switch } from '@/components/ui/switch';
import { Label } from '@/components/ui/label';
import { supabase } from '@/integrations/supabase/client';
import { toast } from 'sonner';
import { 
  Check, 
  X, 
  Star, 
  Zap, 
  Crown,
  Shield,
  ArrowLeft
} from 'lucide-react';

const plans = [
  {
    id: 'free',
    name: 'Free',
    price: { monthly: 0, yearly: 0 },
    description: 'Perfect for getting started',
    features: [
      '2 articles per month',
      '1 WordPress site',
      'Basic AI agents',
      'Email support',
      'Standard templates'
    ],
    limitations: [
      'No team collaboration',
      'No custom branding',
      'Limited analytics'
    ],
    current: true,
    popular: false,
    cta: 'Current Plan'
  },
  {
    id: 'starter',
    name: 'Starter',
    price: { monthly: 29, yearly: 252 },
    description: 'Great for small teams and businesses',
    features: [
      '20 articles per month',
      '3 WordPress sites',
      '5 team members',
      'Advanced AI agents',
      'Priority support',
      'Team collaboration',
      'Basic analytics',
      'Custom templates'
    ],
    limitations: [
      'No white-label options',
      'Limited API access'
    ],
    current: false,
    popular: true,
    cta: 'Start 14-day Free Trial'
  },
  {
    id: 'professional',
    name: 'Professional',
    price: { monthly: 99, yearly: 852 },
    description: 'Best for growing businesses',
    features: [
      '100 articles per month',
      'Unlimited WordPress sites',
      'Unlimited team members',
      'Premium AI agents',
      'Priority support',
      'Advanced analytics',
      'White-label options',
      'API access',
      'Custom integrations',
      'Advanced SEO tools'
    ],
    limitations: [],
    current: false,
    popular: false,
    cta: 'Start 14-day Free Trial'
  },
  {
    id: 'enterprise',
    name: 'Enterprise',
    price: { monthly: 'Custom', yearly: 'Custom' },
    description: 'For large organizations with custom needs',
    features: [
      'Unlimited articles',
      'Unlimited everything',
      'Custom deployment',
      'Dedicated support',
      'SLA guarantee',
      'Custom AI training',
      'Advanced security',
      'Custom integrations',
      'Onboarding assistance'
    ],
    limitations: [],
    current: false,
    popular: false,
    cta: 'Contact Sales'
  }
];

export default function UpgradePlan() {
  const [billingCycle, setBillingCycle] = useState<'monthly' | 'yearly'>('monthly');
  const [loading, setLoading] = useState<string | null>(null);

  const handleUpgrade = async (planId: string) => {
    if (planId === 'free' || planId === 'enterprise') return;
    
    try {
      setLoading(planId);
      
      const { data, error } = await supabase.functions.invoke('create-checkout', {
        body: {
          planName: planId,
          billingCycle: billingCycle
        }
      });
      
      if (error) throw error;
      
      // Open Stripe checkout in a new tab
      window.open(data.url, '_blank');
    } catch (error) {
      console.error('Error creating checkout:', error);
      toast.error('Failed to start checkout process');
    } finally {
      setLoading(null);
    }
  };

  const calculateSavings = (monthlyPrice: number) => {
    const yearlyTotal = monthlyPrice * 12;
    const actualYearlyPrice = plans.find(p => p.price.monthly === monthlyPrice)?.price.yearly || 0;
    if (typeof actualYearlyPrice === 'number') {
      return yearlyTotal - actualYearlyPrice;
    }
    return 0;
  };

  const getIcon = (planId: string) => {
    switch (planId) {
      case 'starter': return <Zap className="w-6 h-6" />;
      case 'professional': return <Crown className="w-6 h-6" />;
      case 'enterprise': return <Shield className="w-6 h-6" />;
      default: return <Star className="w-6 h-6" />;
    }
  };

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

      <div className="text-center space-y-4">
        <h1 className="text-4xl font-bold tracking-tight">Choose Your Plan</h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          Upgrade to unlock more features and higher limits for your content creation
        </p>
      </div>

      {/* Billing Cycle Toggle */}
      <div className="flex items-center justify-center space-x-4">
        <Label htmlFor="billing-cycle" className={billingCycle === 'monthly' ? 'font-semibold' : ''}>
          Monthly
        </Label>
        <Switch
          id="billing-cycle"
          checked={billingCycle === 'yearly'}
          onCheckedChange={(checked) => setBillingCycle(checked ? 'yearly' : 'monthly')}
        />
        <Label htmlFor="billing-cycle" className={billingCycle === 'yearly' ? 'font-semibold' : ''}>
          Yearly
        </Label>
        {billingCycle === 'yearly' && (
          <Badge variant="secondary" className="ml-2">
            Save up to $348/year
          </Badge>
        )}
      </div>

      {/* Pricing Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {plans.map((plan) => (
          <Card 
            key={plan.id} 
            className={`relative ${plan.popular ? 'ring-2 ring-primary shadow-lg' : ''} ${plan.current ? 'ring-2 ring-muted' : ''}`}
          >
            {plan.popular && (
              <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                <Badge className="bg-primary text-primary-foreground">
                  Most Popular
                </Badge>
              </div>
            )}
            
            {plan.current && (
              <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                <Badge variant="secondary">
                  Current Plan
                </Badge>
              </div>
            )}

            <CardHeader className="text-center">
              <div className="flex justify-center mb-2">
                {getIcon(plan.id)}
              </div>
              <CardTitle className="text-2xl">{plan.name}</CardTitle>
              <div className="space-y-2">
                <div className="text-3xl font-bold">
                  {typeof plan.price[billingCycle] === 'number' 
                    ? (plan.price[billingCycle] === 0 ? 'Free' : `$${plan.price[billingCycle]}`)
                    : plan.price[billingCycle]
                  }
                  {typeof plan.price[billingCycle] === 'number' && plan.price[billingCycle] > 0 && (
                    <span className="text-base font-normal text-muted-foreground">
                      /{billingCycle === 'yearly' ? 'year' : 'month'}
                    </span>
                  )}
                </div>
                {billingCycle === 'yearly' && typeof plan.price.monthly === 'number' && plan.price.monthly > 0 && (
                  <div className="text-sm text-green-600">
                    Save ${calculateSavings(plan.price.monthly)}/year
                  </div>
                )}
              </div>
              <p className="text-sm text-muted-foreground">{plan.description}</p>
            </CardHeader>

            <CardContent className="space-y-4">
              <div className="space-y-2">
                {plan.features.map((feature, index) => (
                  <div key={index} className="flex items-center gap-2 text-sm">
                    <Check className="w-4 h-4 text-green-500 flex-shrink-0" />
                    <span>{feature}</span>
                  </div>
                ))}
                {plan.limitations.map((limitation, index) => (
                  <div key={index} className="flex items-center gap-2 text-sm text-muted-foreground">
                    <X className="w-4 h-4 text-red-500 flex-shrink-0" />
                    <span>{limitation}</span>
                  </div>
                ))}
              </div>

              <Button 
                className="w-full" 
                variant={plan.current ? "secondary" : plan.popular ? "default" : "outline"}
                disabled={plan.current || loading === plan.id}
                onClick={() => handleUpgrade(plan.id)}
              >
                {loading === plan.id ? 'Processing...' : plan.cta}
              </Button>

              {!plan.current && plan.id !== 'enterprise' && (
                <p className="text-xs text-center text-muted-foreground">
                  14-day free trial • No commitment • Cancel anytime
                </p>
              )}
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Feature Comparison */}
      <Card>
        <CardHeader>
          <CardTitle>Feature Comparison</CardTitle>
          <p className="text-muted-foreground">
            Compare features across all plans to find the perfect fit
          </p>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b">
                  <th className="text-left py-2">Feature</th>
                  <th className="text-center py-2">Free</th>
                  <th className="text-center py-2">Starter</th>
                  <th className="text-center py-2">Professional</th>
                  <th className="text-center py-2">Enterprise</th>
                </tr>
              </thead>
              <tbody className="space-y-2">
                <tr className="border-b">
                  <td className="py-2">Articles per month</td>
                  <td className="text-center">2</td>
                  <td className="text-center">20</td>
                  <td className="text-center">100</td>
                  <td className="text-center">Unlimited</td>
                </tr>
                <tr className="border-b">
                  <td className="py-2">Team members</td>
                  <td className="text-center">1</td>
                  <td className="text-center">5</td>
                  <td className="text-center">Unlimited</td>
                  <td className="text-center">Unlimited</td>
                </tr>
                <tr className="border-b">
                  <td className="py-2">WordPress sites</td>
                  <td className="text-center">1</td>
                  <td className="text-center">3</td>
                  <td className="text-center">Unlimited</td>
                  <td className="text-center">Unlimited</td>
                </tr>
                <tr className="border-b">
                  <td className="py-2">API access</td>
                  <td className="text-center"><X className="w-4 h-4 text-red-500 mx-auto" /></td>
                  <td className="text-center">Limited</td>
                  <td className="text-center"><Check className="w-4 h-4 text-green-500 mx-auto" /></td>
                  <td className="text-center"><Check className="w-4 h-4 text-green-500 mx-auto" /></td>
                </tr>
                <tr className="border-b">
                  <td className="py-2">White-label options</td>
                  <td className="text-center"><X className="w-4 h-4 text-red-500 mx-auto" /></td>
                  <td className="text-center"><X className="w-4 h-4 text-red-500 mx-auto" /></td>
                  <td className="text-center"><Check className="w-4 h-4 text-green-500 mx-auto" /></td>
                  <td className="text-center"><Check className="w-4 h-4 text-green-500 mx-auto" /></td>
                </tr>
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>

      {/* Security & Guarantee */}
      <div className="text-center space-y-4 pt-8">
        <div className="flex justify-center items-center gap-4 text-sm text-muted-foreground">
          <div className="flex items-center gap-2">
            <Shield className="w-4 h-4" />
            SSL Encrypted
          </div>
          <div className="flex items-center gap-2">
            <Check className="w-4 h-4" />
            14-day Money Back
          </div>
          <div className="flex items-center gap-2">
            <X className="w-4 h-4" />
            No Long-term Contracts
          </div>
        </div>
        <p className="text-xs text-muted-foreground max-w-md mx-auto">
          All payments are processed securely through Stripe. You can cancel or change your plan at any time.
        </p>
      </div>
    </div>
  );
}
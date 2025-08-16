# Critical Stripe Security Fixes

## Context
The billing system is working but needs critical security improvements before launch. These are minimal changes that significantly improve security.

## Priority: CRITICAL - Must Complete Before Launch

## Task 1: Add Plan Validation to Checkout

### File: `supabase/functions/create-checkout/index.ts`

Find the section after line 43 where you get the request data:
```typescript
const { priceId, planName, billingCycle = 'monthly' } = await req.json();
```

Add validation immediately after:
```typescript
// Security: Validate allowed plans and billing cycles
const ALLOWED_PLANS = ['starter', 'professional'];
const ALLOWED_CYCLES = ['monthly', 'yearly'];

if (!ALLOWED_PLANS.includes(planName)) {
  logStep("ERROR: Invalid plan name attempted", { planName });
  throw new Error('Invalid plan selected');
}

if (!ALLOWED_CYCLES.includes(billingCycle)) {
  logStep("ERROR: Invalid billing cycle attempted", { billingCycle });
  throw new Error('Invalid billing cycle selected');
}

logStep("Plan validation passed", { planName, billingCycle });
```

## Task 2: Create Stripe Webhook Handler

### Create New File: `supabase/functions/stripe-webhook/index.ts`

```typescript
import { serve } from "https://deno.land/std@0.190.0/http/server.ts";
import Stripe from "https://esm.sh/stripe@14.21.0";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2.45.0";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type, stripe-signature",
};

const logStep = (step: string, details?: any) => {
  const detailsStr = details ? ` - ${JSON.stringify(details)}` : '';
  console.log(`[STRIPE-WEBHOOK] ${step}${detailsStr}`);
};

serve(async (req) => {
  // Handle CORS
  if (req.method === "OPTIONS") {
    return new Response(null, { headers: corsHeaders });
  }

  // Only accept POST requests
  if (req.method !== "POST") {
    return new Response("Method not allowed", { status: 405 });
  }

  const supabaseClient = createClient(
    Deno.env.get("SUPABASE_URL") ?? "",
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") ?? "",
    { auth: { persistSession: false } }
  );

  try {
    // Verify webhook signature
    const signature = req.headers.get("stripe-signature");
    const webhookSecret = Deno.env.get("STRIPE_WEBHOOK_SECRET");
    
    if (!signature || !webhookSecret) {
      logStep("ERROR: Missing signature or webhook secret");
      throw new Error("Webhook configuration error");
    }

    const stripeKey = Deno.env.get("STRIPE_SECRET_KEY");
    if (!stripeKey) throw new Error("STRIPE_SECRET_KEY is not set");

    const stripe = new Stripe(stripeKey, { apiVersion: "2023-10-16" });
    
    // Construct and verify the event
    const body = await req.text();
    const event = stripe.webhooks.constructEvent(body, signature, webhookSecret);
    
    logStep("Webhook event received", { type: event.type, id: event.id });

    // Handle different event types
    switch (event.type) {
      case 'customer.subscription.created':
      case 'customer.subscription.updated': {
        const subscription = event.data.object as Stripe.Subscription;
        const customerId = subscription.customer as string;
        
        // Determine subscription tier from amount
        const priceAmount = subscription.items.data[0]?.price.unit_amount || 0;
        let tier = 'free';
        
        if (priceAmount >= 8500) {
          tier = 'professional';
        } else if (priceAmount >= 2500) {
          tier = 'starter';
        }

        // Update organization subscription
        const { error: updateError } = await supabaseClient
          .from('organizations')
          .update({
            subscription_tier: tier,
            subscription_status: subscription.status,
            subscription_id: subscription.id,
            stripe_customer_id: customerId,
            subscription_end: new Date(subscription.current_period_end * 1000).toISOString(),
            monthly_article_limit: tier === 'professional' ? 100 : tier === 'starter' ? 20 : 2,
            updated_at: new Date().toISOString()
          })
          .eq('stripe_customer_id', customerId);

        if (updateError) {
          logStep("ERROR updating organization", { error: updateError });
          throw updateError;
        }

        // Also update subscribers table
        const customerEmail = subscription.customer_email || 
          (await stripe.customers.retrieve(customerId) as Stripe.Customer).email;

        if (customerEmail) {
          await supabaseClient
            .from('subscribers')
            .upsert({
              email: customerEmail,
              stripe_customer_id: customerId,
              subscribed: subscription.status === 'active',
              subscription_tier: tier,
              subscription_status: subscription.status,
              subscription_end: new Date(subscription.current_period_end * 1000).toISOString(),
              updated_at: new Date().toISOString()
            }, { onConflict: 'email' });
        }

        logStep("Subscription updated successfully", { 
          customerId, 
          tier, 
          status: subscription.status 
        });
        break;
      }
      
      case 'customer.subscription.deleted': {
        const subscription = event.data.object as Stripe.Subscription;
        const customerId = subscription.customer as string;
        
        // Downgrade to free tier
        const { error: updateError } = await supabaseClient
          .from('organizations')
          .update({
            subscription_tier: 'free',
            subscription_status: 'canceled',
            subscription_id: null,
            monthly_article_limit: 2,
            updated_at: new Date().toISOString()
          })
          .eq('stripe_customer_id', customerId);

        if (updateError) {
          logStep("ERROR downgrading organization", { error: updateError });
          throw updateError;
        }

        // Update subscribers table
        const customerEmail = subscription.customer_email ||
          (await stripe.customers.retrieve(customerId) as Stripe.Customer).email;

        if (customerEmail) {
          await supabaseClient
            .from('subscribers')
            .update({
              subscribed: false,
              subscription_tier: 'free',
              subscription_status: 'canceled',
              subscription_end: null,
              updated_at: new Date().toISOString()
            })
            .eq('email', customerEmail);
        }

        logStep("Subscription canceled successfully", { customerId });
        break;
      }
      
      case 'invoice.payment_failed': {
        const invoice = event.data.object as Stripe.Invoice;
        const customerId = invoice.customer as string;
        
        // Update subscription status to past_due
        await supabaseClient
          .from('organizations')
          .update({
            subscription_status: 'past_due',
            updated_at: new Date().toISOString()
          })
          .eq('stripe_customer_id', customerId);

        logStep("Payment failed, marked as past_due", { customerId });
        
        // In production, you'd send an email notification here
        // Example: await sendPaymentFailedEmail(invoice);
        break;
      }

      case 'invoice.payment_succeeded': {
        const invoice = event.data.object as Stripe.Invoice;
        const customerId = invoice.customer as string;
        
        // Update subscription status back to active if it was past_due
        await supabaseClient
          .from('organizations')
          .update({
            subscription_status: 'active',
            updated_at: new Date().toISOString()
          })
          .eq('stripe_customer_id', customerId)
          .eq('subscription_status', 'past_due');

        logStep("Payment succeeded, reactivated if needed", { customerId });
        break;
      }
      
      default:
        logStep("Unhandled event type", { type: event.type });
    }

    return new Response(JSON.stringify({ received: true }), {
      headers: { ...corsHeaders, "Content-Type": "application/json" },
      status: 200,
    });

  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : String(error);
    logStep("ERROR in webhook handler", { message: errorMessage });
    
    // Return 400 to indicate webhook processing failed
    // Stripe will retry the webhook
    return new Response(JSON.stringify({ error: errorMessage }), {
      headers: { ...corsHeaders, "Content-Type": "application/json" },
      status: 400,
    });
  }
});
```

## Task 3: Update Billing Page to Show Real-time Status

### File: `src/pages/billing/Billing.tsx`

The billing page should already be checking subscription status correctly via the `check-subscription` function. However, ensure it refreshes after returning from Stripe checkout:

Add URL parameter checking in the useEffect:
```typescript
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
```

## Task 4: Configure Webhook in Stripe Dashboard

After deploying the webhook function, you need to configure it in Stripe:

1. The webhook endpoint URL will be:
   ```
   https://epftkydwdqerdlhvqili.supabase.co/functions/v1/stripe-webhook
   ```

2. Select these events to listen for:
   - `customer.subscription.created`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
   - `invoice.payment_failed`
   - `invoice.payment_succeeded`

3. After creating the endpoint, copy the "Signing secret" that starts with `whsec_`

4. Add this secret to your Supabase Edge Functions environment variables:
   - Go to your Supabase Dashboard
   - Navigate to Edge Functions
   - Add secret: `STRIPE_WEBHOOK_SECRET` = `whsec_...` (your signing secret)

## Testing Instructions

### Local Testing with Stripe CLI:
```bash
# Install Stripe CLI if not already installed
brew install stripe/stripe-cli/stripe

# Login to Stripe
stripe login

# Forward webhooks to your local Supabase
stripe listen --forward-to http://localhost:54321/functions/v1/stripe-webhook

# In another terminal, trigger test events
stripe trigger customer.subscription.created
stripe trigger customer.subscription.deleted
stripe trigger invoice.payment_failed
```

### Production Testing:
1. Complete a test checkout with a Stripe test card (4242 4242 4242 4242)
2. Check that the organization's subscription_tier updates to 'starter' or 'professional'
3. Cancel the subscription in Stripe Dashboard
4. Verify the organization downgrades to 'free' tier
5. Check Stripe webhook logs for any errors

## Success Criteria

- [ ] Plan validation prevents invalid plan names
- [ ] Webhook handler processes subscription events
- [ ] Database updates correctly on subscription changes
- [ ] Failed payments mark subscriptions as 'past_due'
- [ ] Canceled subscriptions downgrade to free tier
- [ ] No security vulnerabilities in request handling

## Important Notes

1. **Webhook Secret**: This is different from your API keys. It's specifically for verifying webhooks.
2. **Idempotency**: Stripe may send the same webhook multiple times. Our handler should handle duplicates gracefully.
3. **Error Handling**: Return 400 status on errors so Stripe will retry the webhook.
4. **Testing**: Always test with Stripe CLI locally before deploying.

This implementation provides the minimum viable security for your Stripe integration while keeping things simple and maintainable.
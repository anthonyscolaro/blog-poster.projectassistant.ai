# Stripe Security Fixes - Action Items

> **Priority**: Critical - Must complete before launch
> **Timeline**: 1-2 days of work
> **Status**: Not Started

## 🔴 P0: Critical Security Fixes (Do Now)

### 1. Add Plan Name Validation ⚠️
**File**: `frontend/supabase/functions/create-checkout/index.ts`
**Time**: 30 minutes

```typescript
// Add after line 43
const ALLOWED_PLANS = ['starter', 'professional'];
const ALLOWED_CYCLES = ['monthly', 'yearly'];

if (!ALLOWED_PLANS.includes(planName)) {
  throw new Error('Invalid plan selected');
}
if (!ALLOWED_CYCLES.includes(billingCycle)) {
  throw new Error('Invalid billing cycle');
}
```

### 2. Create Stripe Webhook Handler 🔄
**File**: `frontend/supabase/functions/stripe-webhook/index.ts`
**Time**: 2-3 hours

Create new Edge Function to handle these critical events:
- `customer.subscription.created`
- `customer.subscription.updated`
- `customer.subscription.deleted`
- `invoice.payment_failed`

```typescript
import { serve } from "https://deno.land/std@0.190.0/http/server.ts";
import Stripe from "https://esm.sh/stripe@14.21.0";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2.45.0";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
};

serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response(null, { headers: corsHeaders });
  }

  const signature = req.headers.get("stripe-signature");
  const webhookSecret = Deno.env.get("STRIPE_WEBHOOK_SECRET");
  
  if (!signature || !webhookSecret) {
    return new Response("Missing signature or secret", { status: 400 });
  }

  const stripe = new Stripe(Deno.env.get("STRIPE_SECRET_KEY") ?? "", {
    apiVersion: "2023-10-16",
  });

  const supabase = createClient(
    Deno.env.get("SUPABASE_URL") ?? "",
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") ?? "",
  );

  try {
    const body = await req.text();
    const event = stripe.webhooks.constructEvent(body, signature, webhookSecret);
    
    switch (event.type) {
      case 'customer.subscription.created':
      case 'customer.subscription.updated': {
        const subscription = event.data.object as Stripe.Subscription;
        // Update organization subscription status
        await supabase
          .from('organizations')
          .update({
            subscription_status: subscription.status,
            subscription_id: subscription.id,
            subscription_end: new Date(subscription.current_period_end * 1000).toISOString()
          })
          .eq('stripe_customer_id', subscription.customer);
        break;
      }
      
      case 'customer.subscription.deleted': {
        const subscription = event.data.object as Stripe.Subscription;
        // Downgrade to free tier
        await supabase
          .from('organizations')
          .update({
            subscription_tier: 'free',
            subscription_status: 'canceled',
            monthly_article_limit: 2
          })
          .eq('stripe_customer_id', subscription.customer);
        break;
      }
      
      case 'invoice.payment_failed': {
        const invoice = event.data.object as Stripe.Invoice;
        // Could send email notification here
        console.log('Payment failed for customer:', invoice.customer);
        break;
      }
    }
    
    return new Response(JSON.stringify({ received: true }), {
      headers: { ...corsHeaders, "Content-Type": "application/json" },
      status: 200
    });
  } catch (err) {
    console.error('Webhook error:', err);
    return new Response(`Webhook Error: ${err.message}`, { status: 400 });
  }
});
```

### 3. Configure Webhook in Stripe Dashboard 🔧
**Time**: 15 minutes

1. Go to https://dashboard.stripe.com/webhooks
2. Click "Add endpoint"
3. Enter URL: `https://epftkydwdqerdlhvqili.supabase.co/functions/v1/stripe-webhook`
4. Select events:
   - `customer.subscription.created`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
   - `invoice.payment_failed`
5. Copy the signing secret
6. Add to Supabase Edge Functions secrets: `STRIPE_WEBHOOK_SECRET`

## 🟡 P1: Important Improvements (Next Week)

### 4. Switch to Stripe Price IDs
**Why Wait**: Current hardcoded pricing works for MVP
**When to Do**: After first 10 customers

Instead of hardcoding prices, create products in Stripe Dashboard:
1. Create "Blog-Poster Starter" product
2. Create "Blog-Poster Professional" product
3. Add monthly and yearly prices for each
4. Use Price IDs in checkout:

```typescript
// Instead of price_data, use:
line_items: [{
  price: 'price_1AbCdEfGhIjKlMnOp', // From Stripe Dashboard
  quantity: 1,
}]
```

### 5. Add Trial Period
**Why Wait**: Reduces initial conversion but might increase later
**When to Do**: If conversion rate < 5%

```typescript
subscription_data: {
  trial_period_days: 14,
  trial_settings: {
    end_behavior: {
      missing_payment_method: 'cancel'
    }
  }
}
```

## 🟢 P2: Nice to Have (After PMF)

### 6. Frontend Loading States
- Add spinner during checkout creation
- Show "Processing..." during API calls
- Handle timeout scenarios

### 7. Invoice Downloads
- Use Stripe's hosted invoice pages
- Or generate PDFs with React PDF

### 8. Payment Method Management
- Use Stripe's Customer Portal (already implemented)
- Customers can update cards there

### 9. Usage Analytics Dashboard
- Chart.js or Recharts for visualizations
- Show usage trends over time

### 10. Grace Period for Failed Payments
- Configure in Stripe Dashboard
- Smart Retries already enabled by default

## Implementation Checklist

### Before Launch (This Week)
- [ ] Add plan validation to create-checkout
- [ ] Create stripe-webhook Edge Function
- [ ] Configure webhook in Stripe Dashboard
- [ ] Test webhook with Stripe CLI
- [ ] Deploy Edge Functions

### Testing Steps
1. **Test locally with Stripe CLI**:
   ```bash
   stripe listen --forward-to http://localhost:54321/functions/v1/stripe-webhook
   stripe trigger customer.subscription.created
   ```

2. **Verify database updates**:
   - Check organizations table after webhook
   - Verify subscription_tier changes
   - Confirm limits are updated

3. **Test failure scenarios**:
   - Invalid plan names
   - Missing webhook signature
   - Database update failures

## Quick Wins (Do Today)

The plan validation is a 5-minute fix that significantly improves security:

```typescript
// In create-checkout/index.ts, after line 43:
if (!['starter', 'professional'].includes(planName)) {
  throw new Error('Invalid plan selected');
}
```

This prevents users from manipulating the request to create arbitrary prices.

## Decision: Hardcoded Prices vs Price IDs

**Keep Hardcoded for Now Because:**
- Faster to iterate on pricing
- No Stripe Dashboard dependency
- Can change prices without updating Stripe
- Good enough for MVP

**Switch to Price IDs When:**
- You have 50+ customers
- Pricing is stable
- You need multiple currencies
- You want Stripe to handle taxation

## The Bottom Line

**Must Do Now (Security):**
1. ✅ Plan validation (5 minutes)
2. ✅ Webhook handler (2 hours)
3. ✅ Configure webhook (15 minutes)

**Everything else can wait.** The current implementation is secure enough for launch with these three fixes.

---

*Created: January 2025*
*Complete By: Before public launch*
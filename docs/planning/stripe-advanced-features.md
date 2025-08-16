# Stripe Advanced Features Guide

> **Status**: Partial Implementation (Basic checkout complete)
> **Current State**: Checkout and basic subscription management implemented
> **Next Steps**: Add webhook handler for subscription sync

## Current Implementation Status

### ✅ Completed
- Basic checkout flow (`create-checkout`)
- Subscription status checking (`check-subscription`)
- Customer portal access (`customer-portal`)
- Stripe keys properly configured in Edge Functions

### ⚠️ Critical - Needed Soon
- **Stripe Webhook Handler** (for subscription sync)
- **Plan name validation** (security fix)

### 📋 Future Features (Not needed for MVP)
- Usage-based billing
- Overage charges
- Proration handling
- Tax automation
- Advanced invoice customization

## Priority 1: Webhook Handler (Needed Now)

### Essential Webhook Events
```typescript
// supabase/functions/stripe-webhook/index.ts
const ESSENTIAL_EVENTS = [
  'customer.subscription.created',
  'customer.subscription.updated', 
  'customer.subscription.deleted',
  'invoice.payment_failed'
];
```

### Implementation Guide
```typescript
import { serve } from "https://deno.land/std@0.190.0/http/server.ts";
import Stripe from "https://esm.sh/stripe@14.21.0";

serve(async (req) => {
  const signature = req.headers.get("stripe-signature");
  const webhookSecret = Deno.env.get("STRIPE_WEBHOOK_SECRET");
  
  try {
    const event = stripe.webhooks.constructEvent(
      await req.text(),
      signature,
      webhookSecret
    );
    
    switch (event.type) {
      case 'customer.subscription.created':
      case 'customer.subscription.updated':
        await updateSubscriptionStatus(event.data.object);
        break;
        
      case 'customer.subscription.deleted':
        await cancelSubscription(event.data.object);
        break;
        
      case 'invoice.payment_failed':
        await handleFailedPayment(event.data.object);
        break;
    }
    
    return new Response(JSON.stringify({ received: true }), { status: 200 });
  } catch (err) {
    return new Response(`Webhook Error: ${err.message}`, { status: 400 });
  }
});
```

### Setting Up Webhook Endpoint
1. **Local Development**: Use Stripe CLI
   ```bash
   stripe listen --forward-to localhost:54321/functions/v1/stripe-webhook
   ```

2. **Production**: Configure in Stripe Dashboard
   - Endpoint: `https://[project].supabase.co/functions/v1/stripe-webhook`
   - Events: Select the 4 essential events above

## Priority 2: Security Fixes

### Plan Validation
```typescript
// Add to create-checkout/index.ts
const ALLOWED_PLANS = ['starter', 'professional'];
const ALLOWED_CYCLES = ['monthly', 'yearly'];

if (!ALLOWED_PLANS.includes(planName)) {
  throw new Error('Invalid plan selected');
}
if (!ALLOWED_CYCLES.includes(billingCycle)) {
  throw new Error('Invalid billing cycle');
}
```

### Rate Limiting
```typescript
// Simple rate limit using Supabase
const { count } = await supabase
  .from('checkout_attempts')
  .select('count(*)')
  .eq('user_id', user.id)
  .gte('created_at', new Date(Date.now() - 3600000).toISOString());

if (count > 5) {
  throw new Error('Too many checkout attempts. Please try again later.');
}
```

## Future Features (Post-Launch)

### Usage-Based Billing
**When to Implement**: After 50+ customers
**Complexity**: High
**Implementation Time**: 2-3 weeks

```typescript
// Track usage
await stripe.subscriptionItems.createUsageRecord(
  subscriptionItemId,
  {
    quantity: articlesGenerated,
    timestamp: Math.floor(Date.now() / 1000),
    action: 'increment'
  }
);

// Configure in Stripe Dashboard:
// - Create metered price
// - Set aggregation mode (sum, max, last)
// - Configure billing thresholds
```

### Overage Charges
**When to Implement**: When customers hit limits regularly
**Complexity**: Medium
**Alternative**: Just use hard limits initially

```typescript
// Option 1: Automatic overage billing
if (articlesUsed > plan.limit) {
  const overage = articlesUsed - plan.limit;
  await stripe.invoiceItems.create({
    customer: customerId,
    amount: overage * 200, // $2 per extra article
    currency: 'usd',
    description: `${overage} additional articles`
  });
}

// Option 2: Block at limit (simpler)
if (articlesUsed >= plan.limit) {
  throw new Error('Monthly article limit reached. Please upgrade.');
}
```

### Subscription Proration
**When to Implement**: When offering instant upgrades/downgrades
**Complexity**: Medium
**Stripe Handles**: Most of this automatically

```typescript
// Immediate upgrade with proration
await stripe.subscriptions.update(subscriptionId, {
  items: [{
    id: subscriptionItemId,
    price: newPriceId
  }],
  proration_behavior: 'create_prorations' // or 'none', 'always_invoice'
});
```

### Tax Automation (Stripe Tax)
**When to Implement**: $10k+ MRR or international customers
**Cost**: 0.5% of transaction volume
**Complexity**: Low (Stripe handles it)

```typescript
// Enable in checkout session
const session = await stripe.checkout.sessions.create({
  // ... other config
  automatic_tax: {
    enabled: true
  },
  customer_update: {
    address: 'auto',
    name: 'auto'
  }
});
```

### Advanced Invoice Customization
**When to Implement**: Enterprise customers only
**Complexity**: Medium

```typescript
// Custom invoice fields
await stripe.invoices.update(invoiceId, {
  custom_fields: [
    { name: 'PO Number', value: poNumber },
    { name: 'Department', value: department }
  ],
  footer: 'Thank you for your business!',
  metadata: {
    organization_id: orgId,
    billing_contact: contactEmail
  }
});

// Custom invoice numbering
await stripe.invoices.update(invoiceId, {
  number: `INV-${orgCode}-${sequenceNumber}`
});
```

### Payment Retry Logic
**When to Implement**: When you have failed payments
**Complexity**: Low (Stripe handles most)

```typescript
// Configure in Stripe Dashboard:
// Settings → Billing → Revenue recovery
// - Smart Retries: ON
// - Retry schedule: 3, 7, 14 days
// - Failed payment email: ON

// Or configure via API:
await stripe.subscriptions.update(subscriptionId, {
  collection_method: 'charge_automatically',
  payment_settings: {
    payment_method_options: {
      card: {
        request_three_d_secure: 'automatic'
      }
    },
    save_default_payment_method: 'on_subscription'
  }
});
```

### Discounts and Coupons
**When to Implement**: For marketing campaigns
**Complexity**: Low

```typescript
// Create coupon
const coupon = await stripe.coupons.create({
  percent_off: 20,
  duration: 'repeating',
  duration_in_months: 3,
  id: 'LAUNCH20'
});

// Apply to checkout
const session = await stripe.checkout.sessions.create({
  // ... other config
  discounts: [{
    coupon: 'LAUNCH20'
  }]
});
```

### Free Trials
**When to Implement**: To reduce friction
**Complexity**: Low

```typescript
const session = await stripe.checkout.sessions.create({
  // ... other config
  subscription_data: {
    trial_period_days: 14,
    trial_settings: {
      end_behavior: {
        missing_payment_method: 'cancel' // or 'create_invoice', 'pause'
      }
    }
  }
});
```

## Testing Stripe Features

### Test Cards
```
Success: 4242 4242 4242 4242
Decline: 4000 0000 0000 0002
3D Secure: 4000 0027 6000 3184
Insufficient funds: 4000 0000 0000 9995
```

### Test Webhooks Locally
```bash
# Install Stripe CLI
brew install stripe/stripe-cli/stripe

# Login
stripe login

# Forward webhooks to local
stripe listen --forward-to localhost:54321/functions/v1/stripe-webhook

# Trigger test events
stripe trigger customer.subscription.created
```

### Test Scenarios
1. **New Subscription**: Complete checkout → Verify database update
2. **Cancellation**: Cancel in portal → Verify status change
3. **Failed Payment**: Use decline card → Verify notification
4. **Upgrade/Downgrade**: Change plan → Verify proration

## Common Pitfalls

### 1. Not Handling Webhooks
**Problem**: Database out of sync with Stripe
**Solution**: Always implement webhooks, even basic ones

### 2. Storing Sensitive Data
**Problem**: Storing card numbers or full card details
**Solution**: Only store Stripe customer/payment method IDs

### 3. Not Handling Edge Cases
**Problem**: Failed payments, expired cards, disputes
**Solution**: Implement proper error handling and notifications

### 4. Complex Pricing Too Early
**Problem**: Usage-based billing before product-market fit
**Solution**: Start with simple tier-based pricing

### 5. Not Testing Payment Failures
**Problem**: App breaks when payment fails
**Solution**: Test with decline cards, handle gracefully

## Cost Considerations

### Stripe Fees
- **Standard**: 2.9% + $0.30 per transaction
- **Volume discounts**: Available at $80k+ monthly
- **International**: +1% for international cards
- **Currency conversion**: +1% for conversion
- **Stripe Tax**: +0.5% of transaction

### Hidden Costs
- **Disputes**: $15 per dispute (even if you win)
- **Failed payments**: Still charged the $0.30
- **Refunds**: Keep the fixed fee ($0.30)
- **3D Secure**: Free but may reduce conversion

## Implementation Checklist

### Immediate (Before Launch)
- [ ] Add webhook handler for 4 essential events
- [ ] Validate plan names in checkout
- [ ] Test subscription flow end-to-end
- [ ] Add error handling for failed payments

### Short-term (First 10 customers)
- [ ] Add subscription management UI
- [ ] Email notifications for billing events
- [ ] Basic usage tracking display
- [ ] Grace period for failed payments

### Medium-term (50+ customers)
- [ ] Customer portal customization
- [ ] Advanced analytics dashboard
- [ ] Coupon system for marketing
- [ ] Annual plan options

### Long-term (100+ customers)
- [ ] Usage-based billing option
- [ ] Stripe Tax integration
- [ ] Multi-currency support
- [ ] Enterprise invoice customization

## Quick Reference

### Environment Variables
```bash
# Production (Supabase Edge Functions)
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Frontend (.env.local)
VITE_STRIPE_PUBLISHABLE_KEY=pk_live_...
```

### Useful Stripe Dashboard Links
- [API Keys](https://dashboard.stripe.com/apikeys)
- [Webhooks](https://dashboard.stripe.com/webhooks)
- [Products](https://dashboard.stripe.com/products)
- [Customers](https://dashboard.stripe.com/customers)
- [Billing Portal](https://dashboard.stripe.com/settings/billing/portal)

### Support Resources
- [Stripe Docs](https://stripe.com/docs)
- [Stripe Discord](https://discord.gg/stripe)
- [Integration Examples](https://github.com/stripe-samples)

---

*Last Updated: January 2025*
*Next Review: After implementing webhook handler*
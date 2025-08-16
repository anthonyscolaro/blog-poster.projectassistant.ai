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
            stripe_subscription_id: subscription.id,
            stripe_customer_id: customerId,
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
            stripe_subscription_id: null,
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
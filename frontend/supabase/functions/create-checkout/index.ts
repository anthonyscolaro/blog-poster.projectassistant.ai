import { serve } from "https://deno.land/std@0.190.0/http/server.ts";
import Stripe from "https://esm.sh/stripe@14.21.0";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2.45.0";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
};

const logStep = (step: string, details?: any) => {
  const detailsStr = details ? ` - ${JSON.stringify(details)}` : '';
  console.log(`[CREATE-CHECKOUT] ${step}${detailsStr}`);
};

serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response(null, { headers: corsHeaders });
  }

  const supabaseClient = createClient(
    Deno.env.get("SUPABASE_URL") ?? "",
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") ?? "",
    { auth: { persistSession: false } }
  );

  try {
    logStep("Function started");

    const stripeKey = Deno.env.get("STRIPE_SECRET_KEY");
    if (!stripeKey) throw new Error("STRIPE_SECRET_KEY is not set");
    logStep("Stripe key verified");

    const authHeader = req.headers.get("Authorization");
    if (!authHeader) throw new Error("No authorization header provided");
    
    const token = authHeader.replace("Bearer ", "");
    const { data: userData, error: userError } = await supabaseClient.auth.getUser(token);
    if (userError) throw new Error(`Authentication error: ${userError.message}`);
    const user = userData.user;
    if (!user?.email) throw new Error("User not authenticated or email not available");
    logStep("User authenticated", { userId: user.id, email: user.email });

    const { priceId, planName, billingCycle = 'monthly' } = await req.json();
    logStep("Request data", { priceId, planName, billingCycle });

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

    const stripe = new Stripe(stripeKey, { apiVersion: "2023-10-16" });
    
    // Check if customer exists
    const customers = await stripe.customers.list({ email: user.email, limit: 1 });
    let customerId;
    if (customers.data.length > 0) {
      customerId = customers.data[0].id;
      logStep("Existing customer found", { customerId });
    } else {
      const customer = await stripe.customers.create({
        email: user.email,
        metadata: { user_id: user.id }
      });
      customerId = customer.id;
      logStep("New customer created", { customerId });
    }

    // Plan pricing based on tier and billing cycle
    const planPricing = {
      starter: { monthly: 2900, yearly: 25200 }, // $29/mo, $252/year (save $96)
      professional: { monthly: 9900, yearly: 85200 }, // $99/mo, $852/year (save $336)
    };

    const amount = planPricing[planName as keyof typeof planPricing]?.[billingCycle as 'monthly' | 'yearly'];
    if (!amount) throw new Error("Invalid plan or billing cycle");

    const session = await stripe.checkout.sessions.create({
      customer: customerId,
      line_items: [
        {
          price_data: {
            currency: "usd",
            product_data: { 
              name: `${planName.charAt(0).toUpperCase() + planName.slice(1)} Plan`,
              description: `Blog-Poster ${planName} subscription`
            },
            unit_amount: amount,
            recurring: { interval: billingCycle === 'yearly' ? 'year' : 'month' },
          },
          quantity: 1,
        },
      ],
      mode: "subscription",
      success_url: `${req.headers.get("origin")}/billing?success=true&session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${req.headers.get("origin")}/billing/upgrade?canceled=true`,
      metadata: {
        user_id: user.id,
        plan_name: planName,
        billing_cycle: billingCycle
      }
    });

    logStep("Checkout session created", { sessionId: session.id, url: session.url });

    return new Response(JSON.stringify({ url: session.url }), {
      headers: { ...corsHeaders, "Content-Type": "application/json" },
      status: 200,
    });
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : String(error);
    logStep("ERROR in create-checkout", { message: errorMessage });
    return new Response(JSON.stringify({ error: errorMessage }), {
      headers: { ...corsHeaders, "Content-Type": "application/json" },
      status: 500,
    });
  }
});
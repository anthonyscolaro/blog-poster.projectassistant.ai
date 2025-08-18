#!/bin/bash

# Setup Vercel environment variables for different environments
# Usage: ./setup-vercel-environments.sh [dev|staging|production|all]

set -e

# Set Vercel project context
export VERCEL_ORG_ID=team_pY2LWWSGeL99RTSLDlOanduL
export VERCEL_PROJECT_ID=prj_yk0NZ29vK0ts3otzWU4oHT7szzNG

# Supabase credentials (same for all environments for now)
SUPABASE_URL="https://pynlhikthsmduttvihuw.supabase.co"
SUPABASE_ANON_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB5bmxoaWt0aHNtZHV0dHZpaHV3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTUzODIwMTYsImV4cCI6MjA3MDk1ODAxNn0.BDGAvf1jeX9iiQF7RaouCyzds6NS58guKB4l39AX_uQ"

setup_dev() {
    echo "Setting up Development environment variables..."
    
    # Remove existing vars
    vercel env rm VITE_SUPABASE_URL development 2>/dev/null || true
    vercel env rm VITE_SUPABASE_ANON_KEY development 2>/dev/null || true
    vercel env rm VITE_API_URL development 2>/dev/null || true
    vercel env rm VITE_WS_URL development 2>/dev/null || true
    vercel env rm VITE_APP_NAME development 2>/dev/null || true
    vercel env rm VITE_APP_URL development 2>/dev/null || true
    
    # Add new vars
    echo "$SUPABASE_URL" | vercel env add VITE_SUPABASE_URL development
    echo "$SUPABASE_ANON_KEY" | vercel env add VITE_SUPABASE_ANON_KEY development
    echo "https://blog-poster-api-qps2l.ondigitalocean.app" | vercel env add VITE_API_URL development
    echo "wss://blog-poster-api-qps2l.ondigitalocean.app" | vercel env add VITE_WS_URL development
    echo "Blog-Poster (Dev)" | vercel env add VITE_APP_NAME development
    echo "https://dev.blog-poster.projectassistant.ai" | vercel env add VITE_APP_URL development
    
    echo "Development environment variables configured!"
}

setup_staging() {
    echo "Setting up Staging environment variables..."
    
    # Remove existing vars
    vercel env rm VITE_SUPABASE_URL preview 2>/dev/null || true
    vercel env rm VITE_SUPABASE_ANON_KEY preview 2>/dev/null || true
    vercel env rm VITE_API_URL preview 2>/dev/null || true
    vercel env rm VITE_WS_URL preview 2>/dev/null || true
    vercel env rm VITE_APP_NAME preview 2>/dev/null || true
    vercel env rm VITE_APP_URL preview 2>/dev/null || true
    
    # Add new vars (preview = staging in Vercel)
    echo "$SUPABASE_URL" | vercel env add VITE_SUPABASE_URL preview
    echo "$SUPABASE_ANON_KEY" | vercel env add VITE_SUPABASE_ANON_KEY preview
    echo "https://blog-poster-api-qps2l.ondigitalocean.app" | vercel env add VITE_API_URL preview
    echo "wss://blog-poster-api-qps2l.ondigitalocean.app" | vercel env add VITE_WS_URL preview
    echo "Blog-Poster (Staging)" | vercel env add VITE_APP_NAME preview
    echo "https://staging.blog-poster.projectassistant.ai" | vercel env add VITE_APP_URL preview
    
    echo "Staging/Preview environment variables configured!"
}

setup_production() {
    echo "Setting up Production environment variables..."
    
    # Production vars already set via setup-vercel-env.sh
    # This ensures they're current
    
    # Remove existing vars
    vercel env rm VITE_SUPABASE_URL production 2>/dev/null || true
    vercel env rm VITE_SUPABASE_ANON_KEY production 2>/dev/null || true
    vercel env rm VITE_API_URL production 2>/dev/null || true
    vercel env rm VITE_WS_URL production 2>/dev/null || true
    vercel env rm VITE_APP_NAME production 2>/dev/null || true
    vercel env rm VITE_APP_URL production 2>/dev/null || true
    
    # Add new vars
    echo "$SUPABASE_URL" | vercel env add VITE_SUPABASE_URL production
    echo "$SUPABASE_ANON_KEY" | vercel env add VITE_SUPABASE_ANON_KEY production
    echo "https://blog-poster-api-qps2l.ondigitalocean.app" | vercel env add VITE_API_URL production
    echo "wss://blog-poster-api-qps2l.ondigitalocean.app" | vercel env add VITE_WS_URL production
    echo "Blog-Poster" | vercel env add VITE_APP_NAME production
    echo "https://blog-poster.projectassistant.ai" | vercel env add VITE_APP_URL production
    
    echo "Production environment variables configured!"
}

list_all() {
    echo -e "\n=== Development Environment Variables ==="
    vercel env ls development
    
    echo -e "\n=== Staging/Preview Environment Variables ==="
    vercel env ls preview
    
    echo -e "\n=== Production Environment Variables ==="
    vercel env ls production
}

# Main execution
case "${1:-all}" in
    dev)
        setup_dev
        ;;
    staging)
        setup_staging
        ;;
    production)
        setup_production
        ;;
    all)
        setup_dev
        setup_staging
        setup_production
        list_all
        ;;
    list)
        list_all
        ;;
    *)
        echo "Usage: $0 [dev|staging|production|all|list]"
        exit 1
        ;;
esac

echo -e "\n✅ Environment setup complete!"
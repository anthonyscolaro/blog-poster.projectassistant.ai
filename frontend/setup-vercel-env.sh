#!/bin/bash

# Set Vercel project context
export VERCEL_ORG_ID=team_pY2LWWSGeL99RTSLDlOanduL
export VERCEL_PROJECT_ID=prj_yk0NZ29vK0ts3otzWU4oHT7szzNG

# Add production environment variables
echo "Adding production environment variables to Vercel..."

# Supabase Configuration
echo "https://pynlhikthsmduttvihuw.supabase.co" | vercel env add VITE_SUPABASE_URL production
echo "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB5bmxoaWt0aHNtZHV0dHZpaHV3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTUzODIwMTYsImV4cCI6MjA3MDk1ODAxNn0.BDGAvf1jeX9iiQF7RaouCyzds6NS58guKB4l39AX_uQ" | vercel env add VITE_SUPABASE_ANON_KEY production

# FastAPI Backend
echo "https://blog-poster-api-qps2l.ondigitalocean.app" | vercel env add VITE_API_URL production
echo "wss://blog-poster-api-qps2l.ondigitalocean.app" | vercel env add VITE_WS_URL production

# App Configuration
echo "Blog-Poster" | vercel env add VITE_APP_NAME production
echo "https://blog-poster.projectassistant.ai" | vercel env add VITE_APP_URL production

echo "Environment variables added successfully!"

# List all environment variables
echo -e "\nCurrent production environment variables:"
vercel env ls production
#!/bin/bash

# Setup and start Supabase local development
set -e

echo "🚀 Setting up Supabase for local development..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop first."
    exit 1
fi

# Create network if it doesn't exist
if ! docker network ls | grep -q blog-poster-network; then
    echo "📦 Creating Docker network..."
    docker network create blog-poster-network
fi

# Load environment variables
if [ -f .env.supabase ]; then
    echo "📝 Loading Supabase environment variables..."
    export $(cat .env.supabase | grep -v '^#' | xargs)
fi

# Stop any existing Supabase containers
echo "🧹 Cleaning up existing Supabase containers..."
docker compose -f docker-compose.supabase.yml down 2>/dev/null || true

# Start Supabase services
echo "🐳 Starting Supabase services..."
docker compose -f docker-compose.supabase.yml up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check if services are running
echo "✅ Checking service status..."
docker compose -f docker-compose.supabase.yml ps

echo ""
echo "🎉 Supabase is ready!"
echo ""
echo "📍 Access points:"
echo "  - Supabase Studio: http://localhost:3100"
echo "  - API Gateway: http://localhost:8000"
echo "  - Auth Service: http://localhost:9999"
echo "  - PostgreSQL: localhost:5434"
echo ""
echo "🔑 Default credentials:"
echo "  - Database: postgres / your-super-secret-password"
echo "  - Anon Key: Check .env.supabase"
echo ""
echo "📚 Next steps:"
echo "  1. Visit http://localhost:3100 to access Supabase Studio"
echo "  2. Create your user tables and enable RLS"
echo "  3. Configure authentication providers"
echo ""
echo "💡 To stop Supabase:"
echo "  docker compose -f docker-compose.supabase.yml down"
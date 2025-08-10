#!/bin/bash

# Blog Automation System Setup Script
# This script prepares the environment for the blog automation system

set -e

echo "🚀 Setting up Blog Automation System..."

# Check if .env.local exists
if [ ! -f .env.local ]; then
    echo "📝 Creating .env.local from .env.local.example..."
    cp .env.local.example .env.local
    echo "⚠️  Please update .env.local with your API keys!"
    echo "   Required keys:"
    echo "   - ANTHROPIC_API_KEY or OPENAI_API_KEY"
    echo "   - JINA_API_KEY"
    echo "   - BRIGHT_DATA_API_KEY (optional)"
    echo "   - WordPress credentials"
    exit 1
fi

# Check for required API keys
check_env_var() {
    if [ -z "${!1}" ]; then
        echo "❌ Missing required environment variable: $1"
        return 1
    fi
    return 0
}

# Load environment variables
export $(cat .env.local | grep -v '^#' | xargs)

# Check critical variables
MISSING_VARS=0
check_env_var "JINA_API_KEY" || MISSING_VARS=$((MISSING_VARS + 1))

if [ -z "$ANTHROPIC_API_KEY" ] && [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ Missing AI API key: Need either ANTHROPIC_API_KEY or OPENAI_API_KEY"
    MISSING_VARS=$((MISSING_VARS + 1))
fi

if [ $MISSING_VARS -gt 0 ]; then
    echo "⚠️  Please update .env.local with the missing API keys"
    exit 1
fi

# Create required directories
echo "📁 Creating required directories..."
mkdir -p data/competitors
mkdir -p data/articles
mkdir -p data/logs
mkdir -p data/media

# Check if system prompt file exists
if [ ! -f sonnet-3.5-prompt.txt ]; then
    echo "⚠️  Warning: sonnet-3.5-prompt.txt not found"
    echo "   The article generation agent will use the default prompt"
fi

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! docker info &> /dev/null; then
    echo "❌ Docker is not running. Please start Docker."
    exit 1
fi

# Build and start services
echo "🐳 Starting Docker services..."
# Use docker compose v2 syntax
docker compose down 2>/dev/null || true
docker compose up -d --build

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 5

# Check service health
check_service() {
    local service=$1
    local port=$2
    local endpoint=${3:-"/"}
    
    if curl -s -o /dev/null -w "%{http_code}" "http://localhost:$port$endpoint" | grep -q "200\|404"; then
        echo "✅ $service is running on port $port"
        return 0
    else
        echo "❌ $service is not responding on port $port"
        return 1
    fi
}

# Check each service
SERVICES_OK=0
check_service "API" 8088 "/health" || SERVICES_OK=$((SERVICES_OK + 1))
check_service "Qdrant" 6333 "/collections" || SERVICES_OK=$((SERVICES_OK + 1))
check_service "Redis" 6384 || true  # Redis doesn't have HTTP endpoint

if [ $SERVICES_OK -gt 0 ]; then
    echo "⚠️  Some services are not ready. Check docker-compose logs:"
    echo "   docker compose logs"
else
    echo "✅ All services are running!"
fi

# Display service URLs
echo ""
echo "📍 Service URLs:"
echo "   API:     http://localhost:8088"
echo "   Qdrant:  http://localhost:6333/dashboard"
echo "   Redis:   redis://localhost:6384"
echo ""
echo "📚 API Documentation: http://localhost:8088/docs"
echo ""
echo "🔧 Useful commands:"
echo "   View logs:        docker compose logs -f"
echo "   Stop services:    docker compose down"
echo "   Restart services: docker compose restart"
echo "   Test agent:       curl -X POST http://localhost:8088/agent/run -H 'Content-Type: application/json' -d '{\"agent_name\":\"topic_analysis\",\"input\":{}}'"
echo ""
echo "✨ Setup complete! The blog automation system is ready to use."
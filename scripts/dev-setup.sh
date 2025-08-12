#!/bin/bash

# Development Setup Script for Blog Poster
# This script sets up the complete development environment

set -e

echo "🚀 Setting up Blog Poster development environment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}📋 $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker Desktop first."
    exit 1
fi

print_status "Docker is running"

# Create network if it doesn't exist
if ! docker network ls | grep -q blog-poster-network; then
    print_info "Creating Docker network..."
    docker network create blog-poster-network
    print_status "Docker network created"
else
    print_info "Docker network already exists"
fi

# Start main services (Qdrant, Redis, PostgreSQL)
print_info "Starting main services (PostgreSQL, Qdrant, Redis)..."
docker compose up -d

# Wait for services to be ready
print_info "Waiting for services to be ready..."
sleep 10

# Check service health
print_info "Checking service health..."
if curl -s http://localhost:6333 > /dev/null; then
    print_status "Qdrant is healthy"
else
    print_warning "Qdrant may not be ready yet"
fi

if docker exec blog-vectors pg_isready -U postgres > /dev/null 2>&1; then
    print_status "PostgreSQL is healthy"
else
    print_warning "PostgreSQL may not be ready yet"
fi

# Set up environment variables
if [ ! -f .env.local ]; then
    print_info "Creating .env.local from example..."
    cp .env.local.example .env.local
    print_warning "Please update .env.local with your API keys"
else
    print_info ".env.local already exists"
fi

# Install Python dependencies
print_info "Installing Python dependencies..."
pip install -r requirements.txt

# Set up database
print_info "Setting up database..."
export $(cat .env.local | grep -v '^#' | xargs)
python -c "
from src.database import init_database
try:
    init_database()
    print('✅ Database initialized successfully')
except Exception as e:
    print(f'❌ Database initialization failed: {e}')
"

print_status "Development environment setup complete!"

echo ""
print_info "🎉 Setup Summary:"
echo "  - PostgreSQL (main database): http://localhost:5433"
echo "  - Qdrant (vector database): http://localhost:6333"
echo "  - Redis (caching/queuing): http://localhost:6384"
echo ""
print_info "🚀 Next steps:"
echo "  1. Update API keys in .env.local"
echo "  2. Run: make dev"
echo "  3. Visit: http://localhost:8088"
echo ""
print_info "📚 Available commands:"
echo "  make dev       - Start development server"
echo "  make test      - Run tests"
echo "  make stop      - Stop all services"
echo "  make logs      - View application logs"
echo "  make clean     - Clean up containers and volumes"
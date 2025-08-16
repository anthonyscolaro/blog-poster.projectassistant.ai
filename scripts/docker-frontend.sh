#!/bin/bash

# Frontend Docker Management Script
# Usage: ./scripts/docker-frontend.sh [command]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

cd "$PROJECT_ROOT"

# Function to print colored output
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker first."
        exit 1
    fi
}

# Function to check if backend is running
check_backend() {
    if ! docker compose ps | grep -q "blog-api.*running"; then
        print_warning "Backend API is not running. Starting backend services..."
        docker compose up -d
        sleep 5
    fi
}

# Main command handling
case "$1" in
    start|up)
        print_status "Starting frontend in Docker (development mode)..."
        check_docker
        check_backend
        
        # Start frontend with both compose files
        docker compose -f docker-compose.yml -f docker-compose.frontend.yml up -d frontend
        
        print_status "Frontend is starting on http://localhost:5173"
        print_status "Waiting for frontend to be ready..."
        
        # Wait for frontend to be healthy
        for i in {1..30}; do
            if curl -s http://localhost:5173 > /dev/null 2>&1; then
                print_status "Frontend is ready! Access at http://localhost:5173"
                break
            fi
            echo -n "."
            sleep 2
        done
        ;;
        
    stop|down)
        print_status "Stopping frontend container..."
        docker compose -f docker-compose.frontend.yml stop frontend
        print_status "Frontend stopped"
        ;;
        
    restart)
        print_status "Restarting frontend..."
        $0 stop
        sleep 2
        $0 start
        ;;
        
    logs)
        print_status "Showing frontend logs..."
        docker compose -f docker-compose.frontend.yml logs -f frontend
        ;;
        
    shell|sh)
        print_status "Opening shell in frontend container..."
        docker compose -f docker-compose.frontend.yml exec frontend sh
        ;;
        
    build)
        print_status "Building frontend Docker image..."
        docker compose -f docker-compose.frontend.yml build frontend
        print_status "Build complete"
        ;;
        
    rebuild)
        print_status "Rebuilding frontend (no cache)..."
        docker compose -f docker-compose.frontend.yml build --no-cache frontend
        print_status "Rebuild complete"
        ;;
        
    install)
        print_status "Installing npm packages in container..."
        docker compose -f docker-compose.frontend.yml run --rm frontend npm install
        print_status "Installation complete"
        ;;
        
    typecheck)
        print_status "Running TypeScript type checking..."
        docker compose -f docker-compose.frontend.yml run --rm frontend npx tsc --noEmit
        ;;
        
    lint)
        print_status "Running ESLint..."
        docker compose -f docker-compose.frontend.yml run --rm frontend npm run lint
        ;;
        
    test)
        print_status "Running tests..."
        docker compose -f docker-compose.frontend.yml run --rm frontend npm test
        ;;
        
    build-prod)
        print_status "Building production frontend..."
        docker build -t blog-frontend:production --target production ./frontend
        print_status "Production build complete"
        ;;
        
    status)
        print_status "Frontend container status:"
        docker compose -f docker-compose.frontend.yml ps frontend
        ;;
        
    clean)
        print_warning "Cleaning up frontend containers and volumes..."
        docker compose -f docker-compose.frontend.yml down -v
        print_status "Cleanup complete"
        ;;
        
    *)
        echo "Frontend Docker Management Script"
        echo ""
        echo "Usage: $0 {command}"
        echo ""
        echo "Commands:"
        echo "  start|up      - Start frontend in development mode"
        echo "  stop|down     - Stop frontend container"
        echo "  restart       - Restart frontend"
        echo "  logs          - Show frontend logs (follow mode)"
        echo "  shell|sh      - Open shell in frontend container"
        echo "  build         - Build frontend Docker image"
        echo "  rebuild       - Rebuild frontend image (no cache)"
        echo "  install       - Install npm packages"
        echo "  typecheck     - Run TypeScript type checking"
        echo "  lint          - Run ESLint"
        echo "  test          - Run tests"
        echo "  build-prod    - Build production image"
        echo "  status        - Show container status"
        echo "  clean         - Remove containers and volumes"
        echo ""
        echo "Examples:"
        echo "  $0 start      # Start frontend in Docker"
        echo "  $0 logs       # View frontend logs"
        echo "  $0 typecheck  # Check TypeScript types"
        exit 1
        ;;
esac
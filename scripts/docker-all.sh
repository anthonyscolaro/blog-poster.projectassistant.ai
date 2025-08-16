#!/bin/bash

# Complete Stack Docker Management Script
# Manages both backend and frontend services
# Usage: ./scripts/docker-all.sh [command]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

print_info() {
    echo -e "${BLUE}[i]${NC} $1"
}

# Main command handling
case "$1" in
    start|up)
        print_status "Starting complete Blog-Poster stack..."
        
        # Start backend services
        print_info "Starting backend services..."
        docker compose up -d
        
        # Wait for backend to be ready
        print_info "Waiting for backend to be ready..."
        sleep 10
        
        # Start frontend
        print_info "Starting frontend service..."
        docker compose -f docker-compose.yml -f docker-compose.frontend.yml up -d frontend
        
        # Show status
        print_status "All services started!"
        echo ""
        print_info "Access points:"
        echo "  • Frontend:        http://localhost:5173"
        echo "  • API:            http://localhost:8088"
        echo "  • Supabase Studio: http://localhost:3100"
        echo "  • Supabase API:    http://localhost:8000"
        ;;
        
    stop|down)
        print_status "Stopping all services..."
        docker compose -f docker-compose.yml -f docker-compose.frontend.yml down
        print_status "All services stopped"
        ;;
        
    restart)
        print_status "Restarting all services..."
        $0 stop
        sleep 3
        $0 start
        ;;
        
    status|ps)
        print_status "Service Status:"
        echo ""
        docker compose -f docker-compose.yml -f docker-compose.frontend.yml ps
        ;;
        
    logs)
        service="${2:-}"
        if [ -z "$service" ]; then
            print_info "Showing logs for all services (Ctrl+C to exit)..."
            docker compose -f docker-compose.yml -f docker-compose.frontend.yml logs -f
        else
            print_info "Showing logs for $service (Ctrl+C to exit)..."
            docker compose -f docker-compose.yml -f docker-compose.frontend.yml logs -f "$service"
        fi
        ;;
        
    frontend)
        shift
        ./scripts/docker-frontend.sh "$@"
        ;;
        
    typecheck)
        print_status "Running TypeScript strict mode check..."
        docker compose -f docker-compose.frontend.yml run --rm frontend npx tsc --noEmit
        ;;
        
    typecheck-strict)
        print_status "Checking TypeScript with strict mode enabled..."
        docker compose -f docker-compose.frontend.yml run --rm frontend sh -c "npx tsc --noEmit --strict 2>&1 | tee typescript-errors.txt"
        print_info "Errors saved to frontend/typescript-errors.txt"
        ;;
        
    clean)
        print_warning "This will remove all containers, volumes, and data!"
        read -p "Are you sure? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            docker compose -f docker-compose.yml -f docker-compose.frontend.yml down -v
            print_status "All containers and volumes removed"
        else
            print_info "Cancelled"
        fi
        ;;
        
    rebuild)
        print_status "Rebuilding all services..."
        docker compose -f docker-compose.yml -f docker-compose.frontend.yml build --no-cache
        print_status "Rebuild complete"
        ;;
        
    *)
        echo "Blog-Poster Complete Stack Management"
        echo ""
        echo "Usage: $0 {command} [options]"
        echo ""
        echo "Commands:"
        echo "  start|up          - Start all services (backend + frontend)"
        echo "  stop|down         - Stop all services"
        echo "  restart           - Restart all services"
        echo "  status|ps         - Show status of all services"
        echo "  logs [service]    - Show logs (all or specific service)"
        echo "  frontend [cmd]    - Run frontend-specific commands"
        echo "  typecheck         - Run TypeScript type checking"
        echo "  typecheck-strict  - Check with strict mode (for migration)"
        echo "  clean             - Remove all containers and volumes"
        echo "  rebuild           - Rebuild all images"
        echo ""
        echo "Examples:"
        echo "  $0 start                # Start everything"
        echo "  $0 logs frontend        # View frontend logs"
        echo "  $0 frontend shell       # Open frontend shell"
        echo "  $0 typecheck-strict     # Check TypeScript strict mode"
        exit 1
        ;;
esac
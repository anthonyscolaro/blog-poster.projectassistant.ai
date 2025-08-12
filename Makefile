.PHONY: help format lint test test-unit test-integration test-docker test-all clean install install-dev up down restart logs shell setup dev dev-bg status urls

help:
	@echo "🔧 Blog Poster Development Commands"
	@echo ""
	@echo "🚀 Setup & Development:"
	@echo "  make setup          - Complete development environment setup"
	@echo "  make dev            - Start development server"
	@echo "  make dev-bg         - Start development server in background"
	@echo "  make install        - Install production dependencies"
	@echo "  make install-dev    - Install development dependencies"
	@echo ""
	@echo "🧪 Testing & Quality:"
	@echo "  make test           - Run comprehensive test suite"
	@echo "  make test-unit      - Run unit tests only"
	@echo "  make test-integration - Run integration tests"
	@echo "  make test-docker    - Run Docker integration tests"
	@echo "  make test-all       - Run all tests including Docker and style"
	@echo "  make format         - Format code with black and isort"
	@echo "  make lint           - Run linting with flake8 and mypy"
	@echo ""
	@echo "🐳 Docker Services:"
	@echo "  make up             - Start Docker containers"
	@echo "  make down           - Stop Docker containers"
	@echo "  make restart        - Restart Docker containers"
	@echo "  make status         - Show service status"
	@echo "  make logs           - Show API logs"
	@echo "  make shell          - Open database shell"
	@echo ""
	@echo "🧹 Cleanup & Utils:"
	@echo "  make clean          - Remove cache files"
	@echo "  make urls           - Show development URLs"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt
	pre-commit install

format:
	black .
	isort .

lint:
	flake8 . --max-line-length=100 --extend-ignore=E203
	mypy . --config-file pyproject.toml

test:
	python run_tests.py

test-unit:
	pytest tests/ -v --tb=short --cov=. --cov-report=term-missing -k "not (docker or integration or real_)"

test-integration:
	pytest tests/test_api_endpoints.py -v --tb=short -k "not (docker or real_)"

test-docker:
	python run_tests.py --include-docker

test-all:
	python run_tests.py --include-docker --include-style

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true

up:
	docker compose up -d

down:
	docker compose down

restart:
	docker compose restart api

logs:
	docker compose logs -f api

shell:
	docker exec -it blog-vectors psql -U postgres -d blog_poster

# New development commands
setup:
	@echo "🚀 Setting up development environment..."
	chmod +x scripts/dev-setup.sh
	./scripts/dev-setup.sh

dev:
	@echo "🔥 Starting development server..."
	@if [ ! -f .env.local ]; then echo "❌ .env.local not found. Run 'make setup' first."; exit 1; fi
	export $$(cat .env.local | grep -v '^#' | xargs) && python app.py

dev-bg:
	@echo "🔥 Starting development server in background..."
	@if [ ! -f .env.local ]; then echo "❌ .env.local not found. Run 'make setup' first."; exit 1; fi
	export $$(cat .env.local | grep -v '^#' | xargs) && nohup python app.py > app.log 2>&1 &
	@echo "✅ Server started at http://localhost:8088"
	@echo "📋 View logs with: make logs"

status:
	@echo "📊 Service Status:"
	@docker compose ps
	@echo ""
	@echo "🔍 Health Checks:"
	@echo -n "PostgreSQL: "
	@if docker exec blog-vectors pg_isready -U postgres >/dev/null 2>&1; then echo "✅ Healthy"; else echo "❌ Unhealthy"; fi
	@echo -n "Qdrant: "
	@if curl -s http://localhost:6333 >/dev/null; then echo "✅ Healthy"; else echo "❌ Unhealthy"; fi
	@echo -n "Redis: "
	@if docker exec blog-redis redis-cli ping >/dev/null 2>&1; then echo "✅ Healthy"; else echo "❌ Unhealthy"; fi

urls:
	@echo "🌐 Development URLs:"
	@echo "  Application:  http://localhost:8088 (redirects to login or dashboard)"
	@echo "  Login:        http://localhost:8088/auth/login"
	@echo "  Register:     http://localhost:8088/auth/register"
	@echo "  Dashboard:    http://localhost:8088/dashboard (requires login)"
	@echo ""
	@echo "🔧 Service URLs:"
	@echo "  PostgreSQL:   localhost:5433"
	@echo "  Qdrant:       http://localhost:6333"
	@echo "  Qdrant UI:    http://localhost:6333/dashboard"
	@echo "  Redis:        localhost:6384"
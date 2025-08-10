.PHONY: help format lint test clean install install-dev up down restart logs shell

help:
	@echo "Available commands:"
	@echo "  make install      - Install production dependencies"
	@echo "  make install-dev  - Install development dependencies"
	@echo "  make format       - Format code with black and isort"
	@echo "  make lint         - Run linting with flake8 and mypy"
	@echo "  make test         - Run tests with pytest"
	@echo "  make clean        - Remove cache files"
	@echo "  make up           - Start Docker containers"
	@echo "  make down         - Stop Docker containers"
	@echo "  make restart      - Restart Docker containers"
	@echo "  make logs         - Show API logs"
	@echo "  make shell        - Open shell in API container"

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
	pytest tests/ -v --cov=. --cov-report=term-missing

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
	docker exec -it blog-api /bin/bash
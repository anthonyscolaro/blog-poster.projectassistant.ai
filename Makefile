.PHONY: help format lint test test-unit test-integration test-docker test-all clean install install-dev up down restart logs shell

help:
	@echo "Available commands:"
	@echo "  make install        - Install production dependencies"
	@echo "  make install-dev    - Install development dependencies"
	@echo "  make format         - Format code with black and isort"
	@echo "  make lint           - Run linting with flake8 and mypy"
	@echo "  make test           - Run comprehensive test suite"
	@echo "  make test-unit      - Run unit tests only"
	@echo "  make test-integration - Run integration tests"
	@echo "  make test-docker    - Run Docker integration tests"
	@echo "  make test-all       - Run all tests including Docker and style"
	@echo "  make clean          - Remove cache files"
	@echo "  make up             - Start Docker containers"
	@echo "  make down           - Stop Docker containers"
	@echo "  make restart        - Restart Docker containers"
	@echo "  make logs           - Show API logs"
	@echo "  make shell          - Open shell in API container"

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
	docker exec -it blog-api /bin/bash
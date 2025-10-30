.PHONY: help install run test lint format clean docker-up docker-down

# Variables
PORT := 8000

help: ## Display available commands
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	@echo "Installing dependencies..."
	pip install -r requirements.txt

run: ## Run the API locally
	@echo "Starting API at http://localhost:$(PORT)"
	uvicorn app.main:app --reload --port $(PORT)

test: ## Run tests with coverage
	@echo "Running tests..."
	pytest

lint: ## Check code with Ruff
	@echo "Checking code with Ruff..."
	ruff check .

format: ## Format code with Ruff
	@echo "Formatting code with Ruff..."
	ruff check --fix .
	ruff format .

clean: ## Clean generated files
	@echo "Cleaning..."
	rm -rf __pycache__ .pytest_cache .coverage htmlcov .ruff_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

docker-up: ## Build and run with Docker Compose
	@echo "Starting Docker containers..."
	docker-compose up --build -d

docker-down: ## Stop Docker Compose
	@echo "Stopping Docker containers..."
	docker-compose down

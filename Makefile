# FinOps Platform Makefile
# =========================

.PHONY: help install dev-up dev-down test lint format build clean docs

# Default target
.DEFAULT_GOAL := help

# Variables
PYTHON := python3
PIP := pip
DOCKER_COMPOSE := docker-compose
PYTEST := pytest
BLACK := black
RUFF := ruff
MYPY := mypy

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

##@ General

help: ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\n${BLUE}FinOps Platform${NC}\n\nUsage:\n  make ${GREEN}<target>${NC}\n"} /^[a-zA-Z_0-9-]+:.*?##/ { printf "  ${GREEN}%-20s${NC} %s\n", $$1, $$2 } /^##@/ { printf "\n${YELLOW}%s${NC}\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Development

install: ## Install all dependencies
	@echo "${BLUE}Installing dependencies...${NC}"
	$(PIP) install -r requirements.txt
	$(PIP) install -r requirements-dev.txt
	$(PIP) install -e ./portal/cli
	@echo "${GREEN}✓ Dependencies installed${NC}"

install-dev: ## Install development dependencies with pre-commit hooks
	@echo "${BLUE}Installing development dependencies...${NC}"
	$(PIP) install -r requirements-dev.txt
	pre-commit install
	@echo "${GREEN}✓ Development environment ready${NC}"

dev-up: ## Start local development environment
	@echo "${BLUE}Starting development environment...${NC}"
	$(DOCKER_COMPOSE) -f docker-compose.dev.yml up -d
	@echo "${GREEN}✓ Development environment started${NC}"
	@echo "  - Portal: http://localhost:3000"
	@echo "  - API: http://localhost:8080"
	@echo "  - Grafana: http://localhost:3001"

dev-down: ## Stop local development environment
	@echo "${BLUE}Stopping development environment...${NC}"
	$(DOCKER_COMPOSE) -f docker-compose.dev.yml down
	@echo "${GREEN}✓ Development environment stopped${NC}"

dev-logs: ## View development environment logs
	$(DOCKER_COMPOSE) -f docker-compose.dev.yml logs -f

dev-restart: dev-down dev-up ## Restart development environment

##@ Testing

test: ## Run all tests
	@echo "${BLUE}Running tests...${NC}"
	$(PYTEST) tests/ -v
	@echo "${GREEN}✓ Tests passed${NC}"

test-unit: ## Run unit tests only
	@echo "${BLUE}Running unit tests...${NC}"
	$(PYTEST) tests/unit/ -v

test-integration: ## Run integration tests only
	@echo "${BLUE}Running integration tests...${NC}"
	$(PYTEST) tests/integration/ -v

test-coverage: ## Run tests with coverage report
	@echo "${BLUE}Running tests with coverage...${NC}"
	$(PYTEST) tests/ --cov=finops --cov-report=html --cov-report=term-missing
	@echo "${GREEN}✓ Coverage report generated at htmlcov/index.html${NC}"

test-watch: ## Run tests in watch mode
	$(PYTEST) tests/ -v --watch

##@ Code Quality

lint: ## Run all linters
	@echo "${BLUE}Running linters...${NC}"
	$(RUFF) check .
	$(MYPY) portal/cli/finops
	@echo "${GREEN}✓ Linting passed${NC}"

lint-fix: ## Run linters and fix issues
	@echo "${BLUE}Fixing lint issues...${NC}"
	$(RUFF) check . --fix
	@echo "${GREEN}✓ Lint issues fixed${NC}"

format: ## Format code with black
	@echo "${BLUE}Formatting code...${NC}"
	$(BLACK) .
	@echo "${GREEN}✓ Code formatted${NC}"

format-check: ## Check code formatting without changes
	@echo "${BLUE}Checking code format...${NC}"
	$(BLACK) --check .

type-check: ## Run type checking
	@echo "${BLUE}Running type checks...${NC}"
	$(MYPY) portal/cli/finops --ignore-missing-imports

security-scan: ## Run security scanning
	@echo "${BLUE}Running security scan...${NC}"
	bandit -r portal/cli/finops -ll
	safety check
	@echo "${GREEN}✓ Security scan passed${NC}"

##@ Build

build: ## Build all containers
	@echo "${BLUE}Building containers...${NC}"
	$(DOCKER_COMPOSE) build
	@echo "${GREEN}✓ Build complete${NC}"

build-cli: ## Build CLI package
	@echo "${BLUE}Building CLI package...${NC}"
	cd portal/cli && $(PYTHON) -m build
	@echo "${GREEN}✓ CLI package built${NC}"

build-docs: ## Build documentation
	@echo "${BLUE}Building documentation...${NC}"
	mkdocs build
	@echo "${GREEN}✓ Documentation built at site/${NC}"

##@ Infrastructure

tf-init: ## Initialize Terraform
	@echo "${BLUE}Initializing Terraform...${NC}"
	cd templates/infrastructure/terraform && terraform init

tf-plan: ## Run Terraform plan
	@echo "${BLUE}Running Terraform plan...${NC}"
	cd templates/infrastructure/terraform && terraform plan

tf-validate: ## Validate Terraform configurations
	@echo "${BLUE}Validating Terraform...${NC}"
	cd templates/infrastructure/terraform && terraform validate
	@echo "${GREEN}✓ Terraform configuration valid${NC}"

k8s-validate: ## Validate Kubernetes manifests
	@echo "${BLUE}Validating Kubernetes manifests...${NC}"
	kubectl apply --dry-run=client -f templates/infrastructure/kubernetes/
	@echo "${GREEN}✓ Kubernetes manifests valid${NC}"

##@ Documentation

docs-serve: ## Serve documentation locally
	@echo "${BLUE}Starting documentation server...${NC}"
	mkdocs serve

docs-build: ## Build documentation site
	@echo "${BLUE}Building documentation...${NC}"
	mkdocs build

##@ Cleanup

clean: ## Clean build artifacts
	@echo "${BLUE}Cleaning build artifacts...${NC}"
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "${GREEN}✓ Cleaned${NC}"

clean-docker: ## Clean Docker resources
	@echo "${BLUE}Cleaning Docker resources...${NC}"
	$(DOCKER_COMPOSE) down -v --rmi local
	docker system prune -f
	@echo "${GREEN}✓ Docker resources cleaned${NC}"

clean-all: clean clean-docker ## Clean everything

##@ Release

version: ## Show current version
	@cat VERSION

bump-patch: ## Bump patch version
	@echo "${BLUE}Bumping patch version...${NC}"
	bump2version patch

bump-minor: ## Bump minor version
	@echo "${BLUE}Bumping minor version...${NC}"
	bump2version minor

bump-major: ## Bump major version
	@echo "${BLUE}Bumping major version...${NC}"
	bump2version major

##@ CI/CD

ci: lint test ## Run CI checks (lint + test)

ci-full: lint test-coverage security-scan ## Run full CI checks

pre-commit: ## Run pre-commit hooks
	pre-commit run --all-files

##@ Quick Commands

check: format lint test ## Format, lint, and test
all: install check build ## Full build pipeline

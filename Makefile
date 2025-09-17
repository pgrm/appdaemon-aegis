.SHELLFLAGS := -eu -o pipefail -c
SHELL := /bin/bash
.PHONY: help setup setup-ci lint lint-check format format-check test ci all clean ensure-poetry

all: setup format lint test

ensure-poetry:
	@echo "Ensuring poetry is installed..."
	@command -v poetry >/dev/null 2>&1 || { echo "Poetry not found. Install via: pipx install poetry"; exit 127; }

clean:
	@echo "Cleaning caches and build artifacts..."
	@rm -rf .ruff_cache .pytest_cache .mypy_cache dist build .coverage coverage.xml htmlcov

help:
	@echo "Commands:"
	@echo "  setup   		: Set up the development environment."
	@echo "  clean   		: Clean caches and build artifacts."
	@echo "  format  		: Format the code."
	@echo "  format-check	: Verify formatting (no changes)."
	@echo "  lint    		: Run linter checks and auto-fix issues when possible."
	@echo "  lint-check 	: Run linter checks."
	@echo "  test    		: Run tests."
	@echo "  ci      		: Setup the CI environment and run all checks."

setup: ensure-poetry
	@echo "Setting up the development environment..."
	@poetry env use python3.12
	@poetry install --with dev
	@poetry run lefthook install

setup-ci: ensure-poetry
	@echo "Setting up the CI environment..."
	@poetry install --with dev --sync --no-interaction --no-ansi

format:
	@echo "Formatting the code..."
	@poetry run ruff format .

format-check:
	@echo "Checking formatting..."
	@poetry run ruff format . --check --diff

lint:
	@echo "Auto-Fixing linter checks..."
	@poetry run ruff check . --fix

lint-check:
	@echo "Running linter checks..."
	@poetry run ruff check .

test:
	@echo "Running tests..."
	@poetry run pytest --cov=src/appdaemon_aegis --cov-branch --cov-report=xml --cov-fail-under=99

ci: setup-ci format-check lint-check test

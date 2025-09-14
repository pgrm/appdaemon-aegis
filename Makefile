.SHELLFLAGS := -eu -o pipefail -c
SHELL := /bin/bash
.PHONY: help setup lint lint-check format format-check test ci all clean

all: setup format lint test

clean:
	@echo "Cleaning caches and build artifacts..."
	@rm -rf .ruff_cache .pytest_cache .mypy_cache dist build .coverage

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

setup:
	@echo "Setting up the development environment..."
	@poetry install --with dev
	@poetry run lefthook install

setup-ci:
	@echo "Setting up the ci environment..."
	@poetry install --with dev

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
	@poetry run pytest

ci: setup-ci format-check lint-check test

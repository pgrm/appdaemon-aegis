.PHONY: help setup lint lint-check format format-check test ci

help:
	@echo "Commands:"
	@echo "  setup   		: Set up the development environment."
	@echo "  format  		: Format the code."
	@echo "  format-check	: Verify formatting (no changes)."
	@echo "  lint    		: Run linter checks and auto-fix issues when possible."
	@echo "  lint-check 	: Run linter checks."
	@echo "  test    		: Run tests."
	@echo "  ci      		: Run all CI checks."

setup:
	@echo "Setting up the development environment..."
	@poetry install --with dev
	@poetry run lefthook install

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

ci: format-check lint-check test

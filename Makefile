.PHONY: help setup lint format test ci

help:
	@echo "Commands:"
	@echo "  setup   : Set up the development environment."
	@echo "  lint    : Run linter checks."
	@echo "  format  : Format the code."
	@echo "  test    : Run tests."
	@echo "  ci      : Run all CI checks."

setup:
	@echo "Setting up the development environment..."
	@poetry install
	@poetry run lefthook install

lint:
	@echo "Running linter checks..."
	@poetry run ruff check .

format:
	@echo "Formatting the code..."
	@poetry run ruff format .

test:
	@echo "Running tests..."
	@poetry run pytest

ci: lint test

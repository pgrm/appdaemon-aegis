# Gemini Project Guide: AppDaemon Aegis

This document is a guide for, Gemini and other AI bots, to be the best possible assistant for this project.

**Note:** This document should be kept up-to-date with our conversations as the project evolves and potentially the goals or priorities change. If those changes either aren't obvious based on the rest of the source code, or if the old information in this document contradicts the new changes in the repository, please update this file.

## Project Goal

The primary goal of this project is to develop and maintain **AppDaemon Aegis**, a Python framework that enhances AppDaemon. The focus is on providing strong typing, powerful testing utilities, and higher-level abstractions to make creating smart home automations easier, more reliable, and more productive for end-users.

Key objectives:

- **Type Safety:** Introduce strong typing to the AppDaemon API to catch common errors before runtime.
- **Testability:** Provide a suite of testing helpers to make automations robust and easy to test in isolation.
- **Maintainability:** Reduce boilerplate code by offering higher-level abstractions, allowing developers to focus on automation logic.
- **Confidence:** Build a high-quality, well-tested library that developers can rely on for their own automations.

### Supported platforms and scope

- Supported Python: e.g., 3.11+ (update as appropriate)
- Supported AppDaemon: e.g., >= 4.x (update as appropriate)
- Non‑goals: direct device integrations, Home Assistant configuration management, or deployment tooling.
 
## Tech Stack and Tools

- **AppDaemon:** The target framework that this library enhances.
- **Python:** The language for writing the framework and its tests.
- **Poetry:** For dependency management and packaging.
- **pytest:** The testing framework.
- **Ruff:** For linting and code formatting.
- **mypy:** For static type checking.
- **Makefile:** For running common development tasks.
- **Lefthook:** For Git hooks to ensure code quality before commits.
- **GitHub Actions:** For continuous integration.

## Usage

AppDaemon Aegis is intended to be used as a library installed via `pip`. Users will typically add `appdaemon-aegis` to their `requirements.txt` file within their AppDaemon configuration directory. Their own AppDaemon applications will then inherit from `appdaemon_aegis.AegisApp`.

The library itself is not deployed, but rather published to a package repository like PyPI.

## Development Workflow

All development tasks should be run inside the project's virtual environment, which can be activated with `poetry shell`. The project uses a `Makefile` to streamline common tasks.

- The main framework code is located in the `src/appdaemon_aegis/` directory.
- Tests are located in the `tests/` directory.

Common tasks:

- `make setup`: Sets up the development environment, installing dependencies and git hooks.
- `make format`: Formats all code using Ruff.
- `make lint`: Lints all code using Ruff, fixing issues where possible.
- `make test`: Runs the pytest test suite. CI currently enforces ≥99% coverage via pytest-cov.
- `make ci`: Runs all CI checks, including formatting, linting, and testing.

## Conventions

- **Testing:** All new features must include unit tests. Target ≥99% overall coverage (CI-enforced), with critical modules at 100%. Document any justified exclusions.
- **Linting and Formatting:** All Python code must be formatted with `ruff format` and pass the linter checks defined in `pyproject.toml`. This is enforced by Lefthook pre-commit hooks.
- **Commits and Branches:** Commit messages should be clear and descriptive. All work must be done in a dedicated feature branch, never directly on the `main` branch.
- **Pull Requests:** When a feature branch is ready, it should be pushed to the remote repository and a pull request opened on GitHub. The CI pipeline must pass before a PR can be merged.
- **Make targets:** `make all` is developer-focused and may auto-fix (format/lint). `make ci` runs check-only equivalents for reproducible CI results.

## How you can help

- **Developing the Aegis Framework:** Help me write new features and abstractions for the `AegisApp` base class to solve common AppDaemon pain points.
- **Writing Tests:** For any new code we add, help me write comprehensive unit tests using `pytest`.
- **Improving Documentation:** Help me write clear and concise docstrings and update the `README.md` to make the framework easy for others to use.
- **Refactoring:** Suggest and perform refactorings to improve the testability, performance, and maintainability of the framework code.
- **Automating Tasks:** Help me automate repetitive tasks by adding new commands to the `Makefile` or improving the GitHub Actions CI pipeline.
- **Keeping this file up-to-date:** As we work together, please update this file to reflect the latest state of the project and our goals.

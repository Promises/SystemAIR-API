# Contributing to SystemAIR-API

First off, thank you for considering contributing to SystemAIR-API! We appreciate your time and effort, and every contribution helps make this project better for everyone.

This document provides guidelines and instructions for contributing to the project. Please read it before making any contributions.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Environment Setup](#development-environment-setup)
- [Code Style](#code-style)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Release Process](#release-process)

## Code of Conduct

This project and everyone participating in it is governed by a Code of Conduct that establishes expected behavior for our community. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## How Can I Contribute?

### Reporting Bugs

This section guides you through submitting a bug report. Following these guidelines helps maintainers understand your report and reproduce the issue.

- **Use the GitHub issue tracker**
- **Check if the bug has already been reported**
- **Use the bug report template**
- **Provide detailed steps to reproduce**
- **Describe the behavior you observed and what you expected to see**
- **Include relevant details about your environment** (OS, Python version, package versions, etc.)

### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion, including completely new features and minor improvements to existing functionality.

- **Use the GitHub issue tracker**
- **Check if the enhancement has already been suggested**
- **Use the feature request template**
- **Provide a clear description of the enhancement**
- **Explain why this enhancement would be useful**

### Code Contributions

#### Pull Requests

- **Submit pull requests from a new branch, not master/main**
- **Follow the [pull request template](/.github/PULL_REQUEST_TEMPLATE.md)**
- **Make sure all tests pass**
- **Add new tests for new functionality**
- **Update documentation for new features**

## Development Environment Setup

Here's how to set up your development environment to work on SystemAIR-API:

1. **Fork the repository** (click the Fork button at the top right of the repository page)

2. **Clone your fork**:
   ```bash
   git clone https://github.com/your-username/SystemAIR-API.git
   cd SystemAIR-API
   ```

3. **Set up upstream remote**:
   ```bash
   git remote add upstream https://github.com/Promises/SystemAIR-API.git
   ```

4. **Create a virtual environment and install dependencies**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   
   # Install the package in development mode
   pip install -e ".[dev]"
   # Or install dependencies separately
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

5. **Set up pre-commit hooks**:
   ```bash
   pre-commit install
   ```

## Code Style

This project follows these code style guidelines:

- **Black** for code formatting with a line length of 88 characters
- **isort** for import sorting (configured to be compatible with Black)
- **mypy** for static type checking
- **flake8** for linting

Pre-commit hooks are set up to run these tools automatically before each commit.

## Testing

All code contributions should include appropriate tests:

- **Write tests for all new functionality**
- **Ensure existing tests pass for bug fixes**
- **Run the test suite before submitting a PR**:
  ```bash
  pytest
  ```

- **Check test coverage**:
  ```bash
  pytest --cov=systemair_api --cov-report=term --cov-report=html
  ```

## Pull Request Process

1. **Update your fork with the latest changes from upstream**:
   ```bash
   git fetch upstream
   git checkout main
   git merge upstream/main
   git push origin main
   ```

2. **Create a new branch for your feature or bugfix**:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bugfix-name
   ```

3. **Make your changes and commit them with clear, descriptive messages**

4. **Push your branch to GitHub**:
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Submit a pull request** through the GitHub website

6. **Update your PR if requested** after code review

## Release Process

The project maintainers follow this process for releases:

1. Update version number in appropriate files (setup.py, __init__.py, etc.)
2. Update CHANGELOG.md with notable changes
3. Create a new GitHub release with a tag matching the version number
4. Publish to PyPI

## Questions?

If you have any questions or need help with the contribution process, please open an issue or contact the project maintainers.
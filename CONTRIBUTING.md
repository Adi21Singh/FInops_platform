# Contributing to FinOps Platform

First off, thank you for considering contributing to FinOps Platform! It's people like you that make this platform a great tool for the developer community.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to platform-team@example.com.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible using our bug report template.

**Great Bug Reports** include:
- A clear and descriptive title
- Steps to reproduce the behavior
- Expected behavior
- Actual behavior
- Screenshots (if applicable)
- Environment details (OS, versions, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- Use a clear and descriptive title
- Provide a detailed description of the proposed functionality
- Explain why this enhancement would be useful
- List any alternatives you've considered

### Pull Requests

1. **Fork** the repository and create your branch from `main`
2. **Follow** the coding standards and style guides
3. **Test** your changes thoroughly
4. **Document** any new functionality
5. **Submit** a pull request with a clear description

## Development Setup

### Prerequisites

```bash
# Required tools
- Docker >= 24.0
- Python >= 3.11
- Node.js >= 20
- kubectl >= 1.28
- Terraform >= 1.5
- Go >= 1.21 (for certain components)
```

### Local Environment Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/finops-platform.git
cd finops-platform

# Create a virtual environment (for Python components)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run the test suite
make test
```

### Running Locally

```bash
# Start local development environment
make dev-up

# Run the CLI in development mode
cd portal/cli
pip install -e .
finops --help

# Run tests
make test

# Run linting
make lint
```

## Coding Standards

### Python

- Follow [PEP 8](https://pep8.org/) style guide
- Use type hints for all function signatures
- Write docstrings for all public functions/classes
- Maximum line length: 100 characters

```python
def process_service(
    service_name: str,
    config: ServiceConfig,
    dry_run: bool = False
) -> ServiceResult:
    """
    Process a service deployment request.

    Args:
        service_name: Name of the service to process
        config: Service configuration object
        dry_run: If True, simulate the deployment

    Returns:
        ServiceResult containing deployment status

    Raises:
        ServiceError: If the service cannot be processed
    """
    pass
```

### JavaScript/TypeScript

- Follow the [Airbnb Style Guide](https://github.com/airbnb/javascript)
- Use TypeScript for all new code
- Use async/await over promises where possible

### Terraform

- Follow [HashiCorp's Style Conventions](https://developer.hashicorp.com/terraform/language/syntax/style)
- Include descriptions for all variables
- Use consistent naming: `snake_case`
- Group related resources together

### YAML/Kubernetes

- Use 2-space indentation
- Include comments for non-obvious configurations
- Follow Kubernetes naming conventions

## Commit Messages

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

```bash
feat(templates): add Node.js microservice template

- Add Express.js base template
- Include health check endpoints
- Add Dockerfile and docker-compose

Closes #123
```

```bash
fix(pipeline): resolve caching issue in build stage

The build cache was not properly invalidated when
dependencies changed. This fix adds a hash of the
lock file to the cache key.

Fixes #456
```

## Branch Naming

Use descriptive branch names:

```
feature/add-python-template
bugfix/fix-pipeline-timeout
docs/update-architecture
chore/upgrade-dependencies
```

## Testing

### Writing Tests

- Write unit tests for all new functionality
- Include integration tests for critical paths
- Maintain test coverage above 80%

```python
# Example test structure
class TestServiceManager:
    def test_create_service_success(self):
        """Test successful service creation."""
        pass

    def test_create_service_invalid_name(self):
        """Test service creation with invalid name."""
        pass

    def test_create_service_duplicate(self):
        """Test service creation when name already exists."""
        pass
```

### Running Tests

```bash
# Run all tests
make test

# Run specific test file
pytest tests/test_service_manager.py

# Run with coverage
pytest --cov=finops --cov-report=html

# Run integration tests
make test-integration
```

## Documentation

### Code Documentation

- All public APIs must have docstrings
- Complex logic should have inline comments
- Update README.md for user-facing changes

### Architecture Decision Records (ADRs)

For significant changes, create an ADR in `docs/adr/`:

```markdown
# ADR-XXX: Title

## Status
Proposed | Accepted | Deprecated | Superseded

## Context
Why is this decision needed?

## Decision
What is the decision?

## Consequences
What are the implications?
```

## Review Process

1. All PRs require at least one approval
2. CI must pass before merging
3. Breaking changes need team discussion
4. Documentation updates are required for new features

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Eligible for contributor badges

## Questions?

- Open a [Discussion](https://github.com/yourusername/finops-platform/discussions)
- Join our Slack channel: #finops-platform
- Email: platform-team@example.com

Thank you for contributing! 🎉

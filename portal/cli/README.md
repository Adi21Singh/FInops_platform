# FinOps CLI

Command-line interface for the FinOps Internal Developer Platform.

## Installation

```bash
# From the repository root
pip install -e ./portal/cli

# Verify installation
finops --version
```

## Usage

```bash
# Initialize platform
finops init

# Check setup
finops doctor

# Create a new service
finops create service my-api --template python-microservice

# Start local development
finops dev up

# Deploy to an environment
finops deploy --env dev

# View services
finops services list

# Get help
finops --help
finops create --help
```

## Commands

| Command | Description |
|---------|-------------|
| `finops init` | Initialize the platform |
| `finops doctor` | Check platform health |
| `finops create service` | Create a new service |
| `finops create resource` | Create infrastructure resource |
| `finops dev up/down` | Manage local environment |
| `finops deploy` | Deploy services |
| `finops services list` | List all services |
| `finops services describe` | Show service details |
| `finops services logs` | View service logs |

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black .
ruff check .
```

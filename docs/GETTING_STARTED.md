# Getting Started with FinOps Platform

This guide will help you get started with the FinOps Platform, from installation to deploying your first service.

## Prerequisites

Before you begin, ensure you have the following installed:

| Tool | Version | Installation |
|------|---------|--------------|
| Docker | >= 24.0 | [Install Docker](https://docs.docker.com/get-docker/) |
| Python | >= 3.11 | [Install Python](https://www.python.org/downloads/) |
| kubectl | >= 1.28 | [Install kubectl](https://kubernetes.io/docs/tasks/tools/) |
| Helm | >= 3.12 | [Install Helm](https://helm.sh/docs/intro/install/) |
| Terraform | >= 1.5 | [Install Terraform](https://developer.hashicorp.com/terraform/downloads) |

### Verify Prerequisites

```bash
# Check all required tools
docker --version
python --version
kubectl version --client
helm version
terraform --version
```

## Quick Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/finops-platform.git
cd finops-platform
```

### 2. Install the Platform CLI

```bash
# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the CLI
pip install -e ./portal/cli

# Verify installation
finops --version
```

### 3. Initialize the Platform

```bash
# Run the initialization wizard
finops init

# This will:
# - Check prerequisites
# - Configure default settings
# - Set up local development environment
```

### 4. Verify Installation

```bash
# Run health checks
finops doctor

# Expected output:
# ✅ Docker: Running
# ✅ Kubernetes: Connected
# ✅ Registry: Accessible
# ✅ Platform API: Healthy
```

## Your First Service

Let's create and deploy a simple Python microservice.

### Step 1: Scaffold the Service

```bash
# Create a new service from template
finops create service my-first-api \
  --template python-microservice \
  --description "My first API service"

# Navigate to the service directory
cd my-first-api
```

### Step 2: Explore the Generated Structure

```
my-first-api/
├── src/
│   ├── __init__.py
│   ├── main.py          # FastAPI application
│   ├── config.py        # Configuration management
│   ├── routes/          # API routes
│   └── models/          # Data models
├── tests/
│   ├── unit/
│   └── integration/
├── Dockerfile           # Container image definition
├── docker-compose.yml   # Local development setup
├── pyproject.toml       # Python dependencies
├── .github/
│   └── workflows/       # CI/CD pipelines
├── k8s/                 # Kubernetes manifests
│   ├── base/
│   └── overlays/
└── README.md
```

### Step 3: Run Locally

```bash
# Start local development environment
finops dev up

# Or use docker-compose directly
docker-compose up -d

# Test the service
curl http://localhost:8000/health
# {"status": "healthy"}

curl http://localhost:8000/api/v1/hello
# {"message": "Hello from my-first-api!"}
```

### Step 4: Run Tests

```bash
# Run unit tests
finops test unit

# Run all tests with coverage
finops test --coverage

# Lint the code
finops lint
```

### Step 5: Deploy to Development Environment

```bash
# Deploy to dev environment
finops deploy --env dev

# Check deployment status
finops status my-first-api --env dev

# View logs
finops logs my-first-api --env dev --follow
```

## Platform CLI Commands

### Service Management

```bash
# List available templates
finops templates list

# Create a new service
finops create service <name> --template <template>

# List your services
finops services list

# Get service details
finops services describe <name>

# Delete a service
finops services delete <name>
```

### Development

```bash
# Start local environment
finops dev up

# Stop local environment
finops dev down

# View local logs
finops dev logs

# Run tests
finops test [unit|integration|all]

# Lint code
finops lint [--fix]
```

### Deployment

```bash
# Deploy to environment
finops deploy --env <dev|staging|prod>

# Check deployment status
finops status <service> --env <env>

# View deployment history
finops history <service>

# Rollback deployment
finops rollback <service> --env <env> [--revision <n>]
```

### Observability

```bash
# View logs
finops logs <service> --env <env> [--follow]

# Open Grafana dashboard
finops dashboard <service>

# View metrics
finops metrics <service> --env <env>

# View traces
finops traces <service> --env <env>
```

### Platform Health

```bash
# Run diagnostics
finops doctor

# View platform status
finops platform status

# View resource quotas
finops quota
```

## Configuration

### Platform Configuration

The platform configuration is stored in `~/.finops/config.yaml`:

```yaml
# ~/.finops/config.yaml
default_environment: dev
organization: your-org

registries:
  default: ghcr.io/your-org

environments:
  dev:
    cluster: dev-cluster
    namespace_prefix: dev-
  staging:
    cluster: staging-cluster
    namespace_prefix: staging-
  prod:
    cluster: prod-cluster
    namespace_prefix: prod-

notifications:
  slack_channel: "#platform-notifications"
```

### Service Configuration

Each service has a `finops.yaml` configuration:

```yaml
# finops.yaml
apiVersion: finops.io/v1
kind: Service
metadata:
  name: my-first-api
  team: backend
  owner: john.doe@example.com
spec:
  template: python-microservice
  runtime:
    replicas: 2
    resources:
      cpu: 100m
      memory: 256Mi
  observability:
    metrics: true
    tracing: true
    logging:
      level: info
  dependencies:
    - name: postgresql
      version: "15"
    - name: redis
      version: "7"
```

## Next Steps

1. **Explore Templates**: Check out available [service templates](../templates/README.md)
2. **Set Up CI/CD**: Configure [pipeline templates](../pipelines/README.md)
3. **Add Monitoring**: Set up [observability](../observability/README.md) for your services
4. **Read Architecture**: Understand the [platform architecture](architecture/ARCHITECTURE.md)

## Getting Help

- **Documentation**: Browse the [docs](./README.md) directory
- **Issues**: Open an issue on [GitHub](https://github.com/yourusername/finops-platform/issues)
- **Discussions**: Join our [GitHub Discussions](https://github.com/yourusername/finops-platform/discussions)
- **Slack**: Join `#finops-platform` channel

## Troubleshooting

### Common Issues

**Issue: `finops: command not found`**
```bash
# Ensure the CLI is installed and PATH is configured
pip install -e ./portal/cli
# Or add to PATH
export PATH="$PATH:$HOME/.local/bin"
```

**Issue: Cannot connect to Kubernetes cluster**
```bash
# Check kubectl configuration
kubectl config current-context
kubectl cluster-info

# Verify credentials
finops doctor
```

**Issue: Docker build fails**
```bash
# Ensure Docker is running
docker info

# Check Docker resources
docker system df
docker system prune  # Clean up if needed
```

For more troubleshooting, see the [FAQ](./FAQ.md).

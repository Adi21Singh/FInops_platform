# ADR-001: Adopt GitOps-Based Deployment Model

## Status
Accepted

## Date
2025-02-01

## Context
The FinOps Platform needs a consistent, auditable, and reliable deployment
mechanism for all services. Development teams currently use various deployment
approaches including manual kubectl commands, custom scripts, and different
CI/CD tools, leading to inconsistency and difficulty in auditing changes.

Key requirements:
- Auditability for financial compliance (SOC 2, SOX)
- Reproducible deployments across environments
- Easy rollback capabilities
- Clear ownership and change tracking
- Reduced operational burden on platform team

## Decision
We will adopt a GitOps-based deployment model using ArgoCD as the primary
deployment orchestrator. All application and infrastructure changes will be
defined declaratively in Git repositories and automatically synchronized to
the target environments.

### Implementation Approach
1. **Application Repository**: Contains application code and Dockerfile
2. **GitOps Repository**: Contains Kubernetes manifests for all environments
3. **ArgoCD**: Watches GitOps repos and syncs to Kubernetes clusters

### Deployment Flow
```
Code Push → CI Pipeline → Build Image → Update GitOps Repo → ArgoCD Sync → Kubernetes
```

## Rationale

### Alternatives Considered

#### 1. Push-Based CI/CD (e.g., GitHub Actions deploying directly)
**Pros:**
- Simpler initial setup
- Familiar to most developers

**Cons:**
- Requires cluster credentials in CI system
- No continuous reconciliation
- Harder to audit state drift

#### 2. Helm-Based Deployments via CI
**Pros:**
- Powerful templating
- Large community

**Cons:**
- State not stored in Git
- Manual rollbacks
- No drift detection

#### 3. GitOps with ArgoCD (Chosen)
**Pros:**
- Git is the single source of truth
- Automatic drift detection and remediation
- Complete audit trail
- Easy rollbacks (git revert)
- Declarative and version-controlled

**Cons:**
- Additional learning curve
- Another component to manage
- Requires separate GitOps repository

### Why ArgoCD?
- Mature and CNCF-graduated project
- Strong multi-cluster support
- Excellent UI for visualization
- Supports Helm, Kustomize, and plain YAML
- Active community and enterprise support available

## Consequences

### Positive
- Complete audit trail of all deployments satisfying compliance requirements
- Developers can see deployment status through ArgoCD UI
- Easy rollback by reverting Git commits
- Consistent deployment process across all teams
- Reduced blast radius through declarative configurations

### Negative
- Learning curve for teams new to GitOps
- Need to maintain separate GitOps repositories
- Initial setup complexity for ArgoCD
- Image update workflow requires automation (we'll use ArgoCD Image Updater)

### Risks

| Risk | Mitigation |
|------|------------|
| ArgoCD becomes single point of failure | Deploy ArgoCD in HA mode with multiple replicas |
| Git repository unavailability | Use enterprise GitHub with SLA, mirror repos |
| Drift between desired and actual state | ArgoCD auto-sync with alerts on drift |
| Secret management in Git | Use sealed-secrets or external-secrets-operator |

## References
- [GitOps Principles](https://opengitops.dev/)
- [ArgoCD Documentation](https://argo-cd.readthedocs.io/)
- [CNCF GitOps Working Group](https://github.com/cncf/tag-app-delivery/tree/main/gitops-wg)
- ADR-002: Secret Management Strategy (forthcoming)

# ConsumeSafe GitHub Copilot Custom Instructions

## Project Overview
ConsumeSafe is a Python FastAPI application that checks products against a boycott list and suggests Tunisian alternatives. The project includes Docker containerization, Kubernetes deployment, and comprehensive CI/CD with GitHub Actions.

## Tech Stack
- **Backend**: Python 3.11 + FastAPI
- **Testing**: pytest
- **CI/CD**: GitHub Actions
- **Container**: Docker (multi-stage build)
- **Orchestration**: Kubernetes
- **Security**: Bandit, Trivy, TruffleHog

## Key Files & Responsibilities
- `src/main.py` - FastAPI application entry point
- `src/boycott_checker.py` - Boycott checking logic
- `src/product_analyzer.py` - Product analysis and alternatives
- `tests/test_main.py` - Unit tests
- `Dockerfile` - Container build configuration
- `.github/workflows/` - CI/CD pipeline
- `k8s/deployment.yaml` - Kubernetes deployment

## Coding Standards
- PEP 8 compliance (enforced by flake8)
- Code formatting with black
- Type hints for all functions
- Comprehensive docstrings
- Unit test coverage >80%
- Security scanning with bandit

## Development Workflow
1. Create feature branch from `develop`
2. Implement feature with tests
3. Run `pytest tests/ -v` locally
4. Push to GitHub (triggers CI/CD)
5. Pass all checks and code review
6. Merge to `develop` via PR
7. Deploy to dev/prod via CI/CD

## Security Requirements
- No hardcoded secrets
- All secrets in GitHub Secrets or K8s Secrets
- Non-root container execution
- Read-only root filesystem
- Network policies enabled
- RBAC implemented

## Common Tasks
- Adding new endpoint: Update `src/main.py` + tests
- Updating boycott list: Modify `data/boycott_list.json`
- Adding Tunisian products: Modify `data/tunisian_products.json`
- Debugging: Check pod logs with `kubectl logs -n consumesafe <pod>`
- Deploying: Push to main (auto-deploys via CI/CD)

## Helpful Commands
```bash
pytest tests/ -v                    # Run tests
docker-compose up --build           # Local Docker
kubectl apply -f k8s/deployment.yaml  # Deploy K8s
kubectl logs -n consumesafe <pod>   # Check logs
curl http://localhost:8000/health   # Health check
```

## Notes for AI Assistant
- Always maintain security-first approach
- Use absolute paths in file operations
- Validate all user inputs
- Log important operations
- Document changes clearly
- Test before committing
- Follow existing patterns

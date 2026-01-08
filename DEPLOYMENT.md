# ConsumeSafe - Deployment Instructions

## Prerequisites
- Git installed and configured
- GitHub account with repository access
- Docker installed (for local testing)
- kubectl installed (for K8s)
- Python 3.11+

## Step 1: Initial Setup

```bash
# Navigate to project
cd ConsumeSafe

# Initialize git
git init
git add .
git commit -m "Initial ConsumeSafe project setup"

# Add remote
git remote add origin <your-github-repo-url>
git branch -M main
git push -u origin main
```

## Step 2: Configure GitHub Secrets

Add these secrets to GitHub Settings > Secrets:

```
KUBECONFIG_DEV      - Your dev cluster kubeconfig (base64 encoded)
KUBECONFIG_PROD     - Your prod cluster kubeconfig (base64 encoded)
```

To encode kubeconfig:
```bash
cat ~/.kube/config | base64
```

## Step 3: Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# Run application
python -m uvicorn src.main:app --reload

# Test with Docker
docker-compose up --build
curl http://localhost:8000/health
```

## Step 4: Docker Registry Setup

Update `ci-cd.yml` with your registry:

```yaml
REGISTRY: docker.io  # or ghcr.io, ecr.aws, etc.
IMAGE_NAME: your-username/consumesafe
```

## Step 5: Kubernetes Cluster Setup

```bash
# Create namespace
kubectl create namespace consumesafe

# Label namespace for network policies
kubectl label namespace consumesafe name=consumesafe

# Create ConfigMap for data
kubectl create configmap consumesafe-data \
  --from-file=data/ \
  -n consumesafe

# Apply security policies
kubectl apply -f k8s/deployment.yaml
```

## Step 6: Ingress Configuration

Update `k8s/ingress.yaml` with your domain:

```yaml
- host: your-domain.com
  http:
    paths:
    - path: /
```

## Step 7: SSL/TLS Setup (Optional)

For HTTPS, install cert-manager:

```bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml

# Create ClusterIssuer for Let's Encrypt
cat <<EOF | kubectl apply -f -
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: your-email@example.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx
EOF
```

## Step 8: Deploy to Dev

```bash
# Push to develop branch
git checkout -b develop
git push -u origin develop

# Verify CI/CD pipeline runs
# Check GitHub Actions tab
```

## Step 9: Deploy to Production

```bash
# After testing in dev
git checkout main
git merge develop
git push origin main

# CI/CD automatically deploys to production
# Requires approval in GitHub Environment settings
```

## Monitoring Deployments

```bash
# Check pod status
kubectl get pods -n consumesafe -w

# View logs
kubectl logs -f -n consumesafe deployment/consumesafe-api

# Port forward
kubectl port-forward -n consumesafe svc/consumesafe-api 8000:80

# Test endpoint
curl http://localhost:8000/health
```

## Troubleshooting

### Image Pull Errors
```bash
# Create docker secret
kubectl create secret docker-registry ghcr-secret \
  --docker-server=ghcr.io \
  --docker-username=<username> \
  --docker-password=<token> \
  -n consumesafe

# Update deployment to use imagePullSecrets
```

### Pod CrashLoopBackOff
```bash
kubectl describe pod -n consumesafe <pod-name>
kubectl logs -n consumesafe <pod-name> --previous
```

### Network Policy Issues
```bash
# Check network policies
kubectl get networkpolicy -n consumesafe

# Temporarily disable for testing
kubectl delete networkpolicy -n consumesafe --all
```

### Storage Issues
```bash
# Check persistent volumes
kubectl get pv
kubectl get pvc -n consumesafe

# Check node disk space
kubectl describe nodes
```

## Rollback

```bash
# View rollout history
kubectl rollout history deployment/consumesafe-api -n consumesafe

# Rollback to previous version
kubectl rollout undo deployment/consumesafe-api -n consumesafe

# Rollback to specific revision
kubectl rollout undo deployment/consumesafe-api -n consumesafe --to-revision=2
```

## Cleanup

```bash
# Delete deployment
kubectl delete namespace consumesafe

# Delete Docker image
docker rmi consumesafe:latest
```

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [GitHub Actions](https://docs.github.com/en/actions)

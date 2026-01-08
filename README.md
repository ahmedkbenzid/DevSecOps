# ConsumeSafe - Boycott Product Checker Application

## Overview
ConsumeSafe is a comprehensive application that checks products against a boycott list and suggests Tunisian alternative products. It features a Python FastAPI backend, Docker containerization, Kubernetes deployment, and complete security hardening.

## Features
- ✅ **Boycott Product Checker**: Check if a product is on a boycott list
- ✅ **Highlight Mechanism**: Visual highlighting for boycotted products
- ✅ **Alternative Suggestions**: Suggests local Tunisian products
- ✅ **REST API**: FastAPI-based web service
- ✅ **Docker Support**: Container-ready application
- ✅ **Kubernetes Ready**: Complete K8s deployment manifests
- ✅ **CI/CD Pipeline**: GitHub Actions automation
- ✅ **Security Hardening**: Multiple security layers
- ✅ **Unit Tests**: Comprehensive test suite

## Quick Start

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- Kubernetes cluster (for K8s deployment)
- Git

### Local Development

```bash
# Clone the repository
git clone <repository-url>
cd ConsumeSafe

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# Run application (Option 1: Use startup script)
./start.sh       # Linux/Mac
start.bat        # Windows

# Run application (Option 2: Manual)
# Set PYTHONPATH first
export PYTHONPATH=$PWD/src  # Linux/Mac
set PYTHONPATH=%CD%\src     # Windows

python -m uvicorn src.main:app --host 127.0.0.1 --port 8000

# Run with Docker
docker-compose up --build
```

## API Endpoints

### Health Check
```bash
GET /health
```

### Check Product
```bash
POST /check
Content-Type: application/json

{
  "product_name": "coffee",
  "brand": "Nescafé",
  "category": "Beverages"
}
```

Response:
```json
{
  "product_name": "coffee",
  "boycott_status": {
    "is_boycotted": true,
    "reason": "Alleged violations of Palestinian rights",
    "highlight": true,
    "confidence": 1.0
  },
  "alternatives": [
    {
      "name": "Sidi Bou Saïd Coffee",
      "brand": "Café Tunisien",
      "category": "Beverages",
      "origin": "Tunisia",
      "description": "Traditional Tunisian coffee blend",
      "rating": 4.7
    }
  ]
}
```

### Get Boycott List
```bash
GET /boycott-list
```

### Get Tunisian Products
```bash
GET /tunisian-products
GET /tunisian-products?category=Beverages
```

### Get Product Categories
```bash
GET /categories
```

Response:
```json
{
  "count": 6,
  "categories": [
    "Beverages",
    "Cooking",
    "Dairy",
    "Food",
    "Spices"
  ]
}
```

## Docker Deployment

```bash
# Build image
docker build -t consumesafe:latest .

# Run container
docker run -p 8000:8000 consumesafe:latest

# Using Docker Compose
docker-compose up -d
```

## Kubernetes Deployment

```bash
# Create namespace
kubectl create namespace consumesafe

# Deploy application
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/ingress.yaml
kubectl apply -f k8s/cronjob.yaml

# Check deployment
kubectl get pods -n consumesafe
kubectl get svc -n consumesafe

# Port forward for testing
kubectl port-forward -n consumesafe svc/consumesafe-api 8000:80
```

## Security Features

### Container Security
- ✅ Non-root user (appuser, UID 1000)
- ✅ Read-only root filesystem
- ✅ Dropped capabilities (CAP_ALL)
- ✅ Health checks configured
- ✅ Multi-stage Docker build

### Kubernetes Security
- ✅ Pod Security Context (runAsNonRoot, fsGroup)
- ✅ Network Policies
- ✅ RBAC (Role-Based Access Control)
- ✅ Resource Limits and Requests
- ✅ Liveness and Readiness Probes
- ✅ Pod Disruption Budget
- ✅ Horizontal Pod Autoscaler (HPA)

### CI/CD Security
- ✅ Code Quality Checks (flake8, black)
- ✅ Security Scanning (bandit, trivy)
- ✅ Dependency Checks (safety)
- ✅ Container Image Scanning (Trivy, Grype)
- ✅ Secrets Detection (TruffleHog)
- ✅ SAST Analysis (Pylint)
- ✅ Environment-based deployments

## Project Structure

```
ConsumeSafe/
├── src/
│   ├── main.py                 # FastAPI application
│   ├── boycott_checker.py      # Boycott checking logic
│   └── product_analyzer.py     # Product analysis logic
├── tests/
│   └── test_main.py            # Unit tests
├── data/
│   ├── boycott_list.json       # Boycott data
│   └── tunisian_products.json  # Tunisian products data
├── k8s/
│   ├── deployment.yaml         # K8s deployment
│   ├── ingress.yaml            # Ingress configuration
│   └── cronjob.yaml            # Data sync cron job
├── .github/
│   └── workflows/
│       ├── ci-cd.yml           # CI/CD pipeline
│       └── security-scan.yml   # Security scanning
├── Dockerfile                  # Container build file
├── docker-compose.yml          # Docker compose file
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## CI/CD Pipeline

The GitHub Actions pipeline includes:

1. **Quality Checks**: Flake8, Black, Bandit
2. **Unit Tests**: Pytest with coverage
3. **Docker Build**: Multi-stage build and push to registry
4. **Container Scanning**: Trivy vulnerability scanning
5. **Deployment**: Automatic deployment to Dev/Prod

### Pipeline Triggers
- Push to `main` and `develop` branches
- Pull requests to `main` and `develop`
- Scheduled security scans (daily at 2 AM)
- Manual workflow dispatch

## Configuration

### Environment Variables
```bash
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=info
BOYCOTT_DATA_PATH=/app/data/boycott_list.json
PRODUCTS_DATA_PATH=/app/data/tunisian_products.json
```

### Kubernetes ConfigMap
Edit `k8s/deployment.yaml` to update configuration values.

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test
pytest tests/test_main.py::TestBoycottChecker -v
```

## Monitoring

### Health Check
```bash
curl http://localhost:8000/health
```

### Metrics (Kubernetes)
The application exposes Prometheus metrics at `/metrics` (if enabled).

## Database/Data Updates

Data files are located in the `data/` directory:
- `boycott_list.json`: Boycott products and brands
- `tunisian_products.json`: Tunisian product alternatives

Updates to these files will be reflected after container restart.

## Troubleshooting

### Container won't start
```bash
# Check logs
docker logs <container-id>

# Check port availability
netstat -an | grep 8000
```

### Kubernetes pod issues
```bash
# Check pod logs
kubectl logs -n consumesafe <pod-name>

# Describe pod for events
kubectl describe pod -n consumesafe <pod-name>

# Check resource limits
kubectl top pods -n consumesafe
```

## Contributing

1. Create a feature branch
2. Make your changes
3. Run tests and security checks
4. Submit a pull request

## License

[Add your license here]

## Support

For issues and questions, please create a GitHub issue.

## Contact

For more information about ConsumeSafe, visit: [Your contact information]

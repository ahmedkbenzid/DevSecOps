# ConsumeSafe - Quick Reference Guide

## 🎯 Essential Commands

### Development
```bash
# Activate virtual environment (Linux/Mac)
python -m venv venv && source venv/bin/activate

# Activate virtual environment (Windows PowerShell)
python -m venv venv; venv\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# Start development server
python -m uvicorn src.main:app --reload

# Format code
black src tests

# Lint code
flake8 src tests

# Security scan
bandit -r src
```

### Docker
```bash
# Build image
docker build -t consumesafe:latest .

# Run container
docker run -p 8000:8000 consumesafe:latest

# Docker Compose
docker-compose up --build
docker-compose down

# View logs
docker logs <container-id>
```

### Kubernetes
```bash
# Create namespace
kubectl create namespace consumesafe

# Deploy
kubectl apply -f k8s/deployment.yaml

# Check status
kubectl get pods -n consumesafe
kubectl get svc -n consumesafe

# View logs
kubectl logs -n consumesafe <pod-name>

# Port forward
kubectl port-forward -n consumesafe svc/consumesafe-api 8000:80

# Scale
kubectl scale deployment consumesafe-api --replicas=5 -n consumesafe

# Rollback
kubectl rollout undo deployment/consumesafe-api -n consumesafe
```

### Git
```bash
# Initialize
git init
git add .
git commit -m "Initial setup"
git remote add origin <url>
git push -u origin main

# Create branch
git checkout -b develop
git push -u origin develop

# Merge
git checkout main
git merge develop
git push origin main
```

---

## 📡 API Endpoints

### Health Check
```
GET /health
```

### Check Product for Boycott
```
POST /check
{
  "product_name": "coffee",
  "brand": "Nescafé",
  "category": "Beverages"
}
```

### Get All Boycott Items
```
GET /boycott-list
```

### Get Tunisian Products
```
GET /tunisian-products
GET /tunisian-products?category=Beverages
```

### Get Product Categories
```
GET /categories
```

---

## 📚 File Navigation

| File/Folder | Purpose |
|------------|---------|
| `src/main.py` | FastAPI app entry point |
| `src/boycott_checker.py` | Boycott checking logic |
| `src/product_analyzer.py` | Product recommendations |
| `tests/` | Unit tests |
| `k8s/` | Kubernetes manifests |
| `.github/workflows/` | CI/CD pipelines |
| `data/` | Boycott & product data |
| `Dockerfile` | Container build |
| `docker-compose.yml` | Local Docker setup |
| `README.md` | Main documentation |
| `SECURITY.md` | Security details |

---

## 🔑 Configuration

### Environment Variables
```bash
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=info
BOYCOTT_DATA_PATH=/app/data/boycott_list.json
PRODUCTS_DATA_PATH=/app/data/tunisian_products.json
```

### K8s Namespace
```
consumesafe
```

### Default Replicas
```
3 (2-10 with HPA)
```

---

## 🧪 Testing Checklist

```bash
# 1. Unit tests
pytest tests/ -v

# 2. API test
curl http://localhost:8000/health

# 3. Docker test
docker-compose up --build
curl http://localhost:8000/health

# 4. K8s test
kubectl apply -f k8s/deployment.yaml
kubectl get pods -n consumesafe
```

---

## 🚨 Troubleshooting

### Python not found
```bash
# Install Python 3.11+
# https://www.python.org/downloads/
```

### Port 8000 in use
```bash
# Windows
netstat -ano | findstr 8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :8000
kill -9 <PID>
```

### Docker build fails
```bash
# Clean up
docker system prune -a

# Rebuild
docker build --no-cache -t consumesafe:latest .
```

### K8s pod won't start
```bash
# Check logs
kubectl logs -n consumesafe <pod-name>

# Describe pod
kubectl describe pod -n consumesafe <pod-name>

# Check resources
kubectl top pods -n consumesafe
```

---

## 📞 Support Commands

```bash
# Python version
python --version

# Check Python path
which python  # Linux/Mac
where python  # Windows

# List installed packages
pip list

# Check requirements file
cat requirements.txt

# View Docker images
docker images

# View running containers
docker ps

# View K8s resources
kubectl get all -n consumesafe

# Get K8s cluster info
kubectl cluster-info
```

---

## 🎯 Common Tasks

### Add new API endpoint
1. Add to `src/main.py`
2. Add tests in `tests/test_main.py`
3. Run: `pytest tests/ -v`
4. Push to trigger CI/CD

### Update boycott list
1. Edit `data/boycott_list.json`
2. Restart container
3. Test: `curl http://localhost:8000/boycott-list`

### Update Tunisian products
1. Edit `data/tunisian_products.json`
2. Restart container
3. Test: `curl http://localhost:8000/tunisian-products`

### Deploy new version
1. Make code changes
2. Run tests: `pytest tests/ -v`
3. Commit: `git commit -m "Feature: ..."`
4. Push: `git push origin develop`
5. CI/CD automatically deploys to dev
6. PR to main for production deployment

### Scale application
```bash
# Manual scale
kubectl scale deployment consumesafe-api --replicas=5 -n consumesafe

# Check HPA
kubectl get hpa -n consumesafe

# View HPA status
kubectl describe hpa consumesafe-hpa -n consumesafe
```

---

## 🔐 Security Reminders

- ✅ Never commit secrets
- ✅ Use GitHub Secrets for credentials
- ✅ Use K8s Secrets for runtime secrets
- ✅ Keep dependencies updated
- ✅ Run security scans regularly
- ✅ Review CI/CD logs
- ✅ Monitor pod logs
- ✅ Check resource usage

---

## 📖 Documentation Files

| File | Content |
|------|---------|
| `README.md` | Overview & quick start |
| `SECURITY.md` | Security hardening guide |
| `DEPLOYMENT.md` | Deployment & troubleshooting |
| `PROJECT_CHECKLIST.md` | Feature checklist |
| `PROJECT_SUMMARY.md` | Detailed summary |
| `READY_FOR_DEPLOYMENT.md` | Deployment readiness |
| This file | Quick reference |

---

## ✨ Project at a Glance

- **Status**: ✅ Production Ready
- **Language**: Python 3.11
- **Framework**: FastAPI
- **Container**: Docker
- **Orchestration**: Kubernetes
- **CI/CD**: GitHub Actions
- **Tests**: pytest
- **Security**: Hardened at every layer
- **Files**: 25+
- **Lines of Code**: 1000+

**Everything is ready to go! 🚀**

---

**Last Updated**: January 7, 2026  
**Version**: 1.0.0  
**Status**: READY FOR PRODUCTION ✨

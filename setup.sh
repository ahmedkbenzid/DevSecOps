#!/bin/bash
# ConsumeSafe - Quick Setup Script
# This script helps you get started with ConsumeSafe quickly

set -e

echo "================================"
echo "ConsumeSafe - Quick Setup"
echo "================================"
echo ""

# Check Python version
echo "✓ Checking Python version..."
python --version || { echo "Python 3.11+ required"; exit 1; }
echo ""

# Create virtual environment
echo "✓ Creating virtual environment..."
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
echo ""

# Install dependencies
echo "✓ Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo ""

# Run tests
echo "✓ Running tests..."
pytest tests/ -v --tb=short
echo ""

# Show project structure
echo "✓ Project Structure:"
echo "  src/           - Application source code"
echo "  tests/         - Unit tests"
echo "  data/          - Data files (boycott list, products)"
echo "  k8s/           - Kubernetes manifests"
echo "  .github/       - GitHub workflows (CI/CD)"
echo ""

# Show next steps
echo "================================"
echo "Next Steps:"
echo "================================"
echo ""
echo "1. Start development server:"
echo "   python -m uvicorn src.main:app --reload"
echo ""
echo "2. Access API at:"
echo "   http://localhost:8000"
echo ""
echo "3. View API docs at:"
echo "   http://localhost:8000/docs"
echo ""
echo "4. Run Docker:"
echo "   docker-compose up --build"
echo ""
echo "5. Deploy to Kubernetes:"
echo "   kubectl apply -f k8s/deployment.yaml"
echo ""
echo "================================"
echo "Setup Complete! ✨"
echo "================================"

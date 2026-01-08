@echo off
REM ConsumeSafe - Quick Setup Script for Windows
REM This script helps you get started with ConsumeSafe quickly

echo.
echo ================================
echo ConsumeSafe - Quick Setup
echo ================================
echo.

REM Check Python version
echo ✓ Checking Python version...
python --version || (
    echo Python 3.11+ required
    exit /b 1
)
echo.

REM Create virtual environment
echo ✓ Creating virtual environment...
python -m venv venv
call venv\Scripts\activate.bat
echo.

REM Install dependencies
echo ✓ Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
echo.

REM Run tests
echo ✓ Running tests...
pytest tests/ -v --tb=short
echo.

REM Show project structure
echo ✓ Project Structure:
echo   src\           - Application source code
echo   tests\         - Unit tests
echo   data\          - Data files (boycott list, products)
echo   k8s\           - Kubernetes manifests
echo   .github\       - GitHub workflows (CI/CD)
echo.

REM Show next steps
echo ================================
echo Next Steps:
echo ================================
echo.
echo 1. Start development server:
echo    python -m uvicorn src.main:app --reload
echo.
echo 2. Access API at:
echo    http://localhost:8000
echo.
echo 3. View API docs at:
echo    http://localhost:8000/docs
echo.
echo 4. Run Docker:
echo    docker-compose up --build
echo.
echo 5. Deploy to Kubernetes:
echo    kubectl apply -f k8s/deployment.yaml
echo.
echo ================================
echo Setup Complete! (SHIFT+)
echo ================================

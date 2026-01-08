@echo off
REM ConsumeSafe - Start Application (Windows)

echo Starting ConsumeSafe API...
echo.

cd /d "%~dp0"

REM Activate virtual environment
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo Virtual environment not found. Run setup.bat first.
    pause
    exit /b 1
)

REM Set Python path
set PYTHONPATH=%CD%\src

REM Start application
echo.
echo Server starting at http://localhost:8000
echo Press Ctrl+C to stop
echo.

python -m uvicorn src.main:app --host 127.0.0.1 --port 8000

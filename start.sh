#!/bin/bash
# ConsumeSafe - Start Application (Linux/Mac)

echo "Starting ConsumeSafe API..."
echo ""

cd "$(dirname "$0")"

# Activate virtual environment
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    echo "Virtual environment not found. Run setup.sh first."
    exit 1
fi

# Set Python path
export PYTHONPATH="$PWD/src"

# Start application
echo ""
echo "Server starting at http://localhost:8000"
echo "Press Ctrl+C to stop"
echo ""

python -m uvicorn src.main:app --host 127.0.0.1 --port 8000

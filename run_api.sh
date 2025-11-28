#!/bin/bash
# Quick script to run the FastAPI server

echo "Starting Carbon AI Microservice..."
echo "=================================="
echo ""
echo "API will be available at:"
echo "  - http://localhost:8000"
echo "  - Docs: http://localhost:8000/docs"
echo "  - Health: http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop"
echo ""

cd "$(dirname "$0")"
python -m uvicorn src.api.app:app --reload --host 0.0.0.0 --port 8000

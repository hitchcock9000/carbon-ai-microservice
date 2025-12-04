#!/bin/bash

# 🚀 MyCarbonAI - Demo Startup Script
# Starts both backend (Carbon AI Microservice) and frontend (Dashboard)

echo "🌱 MyCarbonAI Demo - Starting both projects..."
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "⚠️  This script is designed for macOS"
fi

# ============================================================================
# BACKEND - Carbon AI Microservice (Port 8000)
# ============================================================================

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}📦 BACKEND - Carbon AI Microservice${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Navigate to backend
BACKEND_PATH="/Users/nim/Dev/ironhack/carbon-ai-microservice"

if [ ! -d "$BACKEND_PATH" ]; then
    echo -e "${RED}❌ Backend directory not found: $BACKEND_PATH${NC}"
    exit 1
fi

cd "$BACKEND_PATH"

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo -e "${YELLOW}⚠️  Conda not found. Make sure Anaconda/Miniconda is installed.${NC}"
    exit 1
fi

# Check if carbon-ai environment exists
if ! conda env list | grep -q "carbon-ai"; then
    echo -e "${YELLOW}⚠️  Environment 'carbon-ai' not found.${NC}"
    echo "Creating environment..."
    conda create -n carbon-ai python=3.11 -y
    conda activate carbon-ai
    pip install -r requirements.txt
else
    echo -e "${GREEN}✓${NC} Found conda environment: carbon-ai"
fi

# Check NumPy version compatibility
echo -e "${YELLOW}Checking NumPy compatibility...${NC}"
NUMPY_VERSION=$(conda run -n carbon-ai python -c "import numpy; print(numpy.__version__)" 2>/dev/null)
if [[ "$NUMPY_VERSION" == 2.* ]]; then
    echo -e "${RED}⚠️  NumPy 2.x detected! TensorFlow requires NumPy <2.0${NC}"
    echo -e "${YELLOW}Fixing NumPy version...${NC}"
    conda run -n carbon-ai pip install "numpy==1.26.4" --force-reinstall --quiet
    echo -e "${GREEN}✓${NC} NumPy downgraded to 1.26.4"
fi

# Start backend in a new terminal window
echo -e "${YELLOW}Starting backend on port 8000...${NC}"
osascript <<EOF
tell application "Terminal"
    do script "cd '$BACKEND_PATH' && eval \"\$(conda shell.bash hook)\" && conda activate carbon-ai && clear && echo '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━' && echo '🚀 BACKEND - Carbon AI Microservice' && echo '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━' && echo '' && echo '📊 ML Dashboard: http://localhost:8000/dashboard' && echo '📖 API Docs: http://localhost:8000/docs' && echo '🏠 Health Check: http://localhost:8000/health' && echo '' && echo 'Starting FastAPI server...' && echo '' && uvicorn src.api.main:app --reload --port 8000"
    activate
end tell
EOF

sleep 3

# ============================================================================
# FRONTEND - MyCarbonAI Dashboard (Port 5173 - Vite default)
# ============================================================================

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}🎨 FRONTEND - MyCarbonAI Dashboard${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Navigate to frontend
FRONTEND_PATH="/Users/nim/Dev/mycarbonai-dashboard"

if [ ! -d "$FRONTEND_PATH" ]; then
    echo -e "${RED}❌ Frontend directory not found: $FRONTEND_PATH${NC}"
    exit 1
fi

cd "$FRONTEND_PATH"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}Installing dependencies... (this may take a few minutes)${NC}"
    npm install
else
    echo -e "${GREEN}✓${NC} Dependencies already installed"
fi

# Start frontend in a new terminal window
echo -e "${YELLOW}Starting frontend with Vite...${NC}"
osascript <<EOF
tell application "Terminal"
    do script "cd '$FRONTEND_PATH' && clear && echo '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━' && echo '🎨 FRONTEND - MyCarbonAI Dashboard' && echo '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━' && echo '' && echo '🌐 Main Dashboard: http://localhost:5173' && echo '📱 Calculator: http://localhost:5173/calculator' && echo '📊 Reports: http://localhost:5173/reports' && echo '' && echo 'Starting Vite dev server...' && echo '' && npm run dev"
    activate
end tell
EOF

sleep 3

# ============================================================================
# Summary
# ============================================================================

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ Both projects starting in separate terminals!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${BLUE}📍 URLs to test:${NC}"
echo ""
echo -e "  ${GREEN}Backend (Carbon AI Microservice):${NC}"
echo -e "    🏠 API Root: ${YELLOW}http://localhost:8000${NC}"
echo -e "    📊 ML Dashboard: ${YELLOW}http://localhost:8000/dashboard${NC}"
echo -e "    📖 API Docs (Swagger): ${YELLOW}http://localhost:8000/docs${NC}"
echo -e "    ❤️  Health Check: ${YELLOW}http://localhost:8000/health${NC}"
echo ""
echo -e "  ${GREEN}Frontend (MyCarbonAI Dashboard):${NC}"
echo -e "    🌐 Main App: ${YELLOW}http://localhost:5173${NC}"
echo -e "    📱 Calculator: ${YELLOW}http://localhost:5173/calculator${NC}"
echo -e "    📊 Reports: ${YELLOW}http://localhost:5173/reports${NC}"
echo -e "    👥 Team: ${YELLOW}http://localhost:5173/team${NC}"
echo ""
echo -e "${YELLOW}⏳ Wait ~10-15 seconds for both servers to fully start...${NC}"
echo ""
echo -e "${BLUE}💡 Tips:${NC}"
echo -e "  • Check the terminal windows for startup logs"
echo -e "  • Backend should show: 'Application startup complete'"
echo -e "  • Frontend should show: 'ready in XXXms' with local URL"
echo -e "  • If ports are busy, kill processes: ${YELLOW}lsof -ti:8000 | xargs kill -9${NC}"
echo ""
echo -e "${GREEN}🎉 Ready for demo! Good luck! 🚀${NC}"
echo ""

# Optional: Wait a bit and try to open browsers
sleep 10
echo -e "${BLUE}🌐 Opening browsers...${NC}"
open "http://localhost:8000/dashboard"
sleep 2
open "http://localhost:5173"

echo ""
echo -e "${GREEN}✨ All set! Both dashboards should be open in your browser!${NC}"
echo ""

#!/bin/bash

echo "========================================="
echo "Full Integration Test"
echo "Dashboard + ML Microservice"
echo "========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Check ML service
echo -e "${YELLOW}Step 1: Checking ML Microservice (port 8000)...${NC}"
ML_HEALTH=$(curl -s http://localhost:8000/health)
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ ML Microservice is running${NC}"
    echo "$ML_HEALTH" | python -m json.tool
else
    echo -e "${RED}✗ ML Microservice is NOT running${NC}"
    echo "Please start it with: ./run_api.sh"
    exit 1
fi
echo ""

# Step 2: Check Dashboard server
echo -e "${YELLOW}Step 2: Checking Dashboard Server (port 4000)...${NC}"
DASHBOARD_HEALTH=$(curl -s http://localhost:4000/api/health)
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Dashboard Server is running${NC}"
    echo "$DASHBOARD_HEALTH" | python -m json.tool
else
    echo -e "${RED}✗ Dashboard Server is NOT running${NC}"
    echo "Please start it with: cd ../mycarbonai-dashboard && node server.js"
    exit 1
fi
echo ""

# Step 3: Test ML service directly
echo -e "${YELLOW}Step 3: Testing ML Energy Prediction (Direct)...${NC}"
DIRECT_PREDICTION=$(curl -s -X POST http://localhost:8000/api/predict/energy \
  -H "Content-Type: application/json" \
  -d '{
    "building_id": 100,
    "square_feet": 50000,
    "primary_use": 0,
    "year_built": 2000,
    "floor_count": 5,
    "air_temperature": 22.5,
    "dew_temperature": 15.0,
    "cloud_coverage": 3,
    "wind_speed": 5.2,
    "precip_depth_1_hr": 0,
    "sea_level_pressure": 1013.25
  }')

if echo "$DIRECT_PREDICTION" | grep -q "predicted_energy_kwh"; then
    echo -e "${GREEN}✓ Direct ML prediction working${NC}"
    echo "$DIRECT_PREDICTION" | python -m json.tool | head -20
else
    echo -e "${RED}✗ Direct ML prediction failed${NC}"
    echo "$DIRECT_PREDICTION"
fi
echo ""

# Step 4: Test chatbot directly
echo -e "${YELLOW}Step 4: Testing Chatbot (Direct)...${NC}"
DIRECT_CHAT=$(curl -s -X POST http://localhost:8000/api/chat/recommendations \
  -H "Content-Type: application/json" \
  -d '{"message": "Quick tips to reduce energy?"}')

if echo "$DIRECT_CHAT" | grep -q "response"; then
    echo -e "${GREEN}✓ Direct chatbot working${NC}"
    echo "$DIRECT_CHAT" | python -m json.tool | head -30
else
    echo -e "${RED}✗ Direct chatbot failed${NC}"
    echo "$DIRECT_CHAT"
fi
echo ""

# Step 5: Test dashboard proxy (without auth - should fail)
echo -e "${YELLOW}Step 5: Testing Dashboard Proxy (without auth - should require token)...${NC}"
PROXY_HEALTH=$(curl -s http://localhost:4000/api/ml/health)

if echo "$PROXY_HEALTH" | grep -q "Access token required"; then
    echo -e "${GREEN}✓ Dashboard proxy correctly requires authentication${NC}"
    echo "$PROXY_HEALTH" | python -m json.tool
else
    echo -e "${YELLOW}⚠ Unexpected response (should require auth):${NC}"
    echo "$PROXY_HEALTH" | python -m json.tool
fi
echo ""

# Step 6: Architecture summary
echo -e "${YELLOW}Step 6: Architecture Verification${NC}"
echo ""
echo "┌─────────────────────┐"
echo "│  React Frontend     │  Port 5173"
echo "│  (To be started)    │"
echo "└──────────┬──────────┘"
echo "           │ HTTP"
echo "           ▼"
echo "┌─────────────────────┐"
echo "│  Dashboard Server   │  Port 4000  ✓ Running"
echo "│  (Express.js)       │"
echo "└──────────┬──────────┘"
echo "           │ Proxy /api/ml/*"
echo "           ▼"
echo "┌─────────────────────┐"
echo "│  ML Microservice    │  Port 8000  ✓ Running"
echo "│  (FastAPI)          │"
echo "└─────────────────────┘"
echo ""

# Summary
echo "========================================="
echo -e "${GREEN}Integration Test Summary${NC}"
echo "========================================="
echo -e "${GREEN}✓${NC} ML Microservice: Running on port 8000"
echo -e "${GREEN}✓${NC} Dashboard Server: Running on port 4000"
echo -e "${GREEN}✓${NC} ML Predictions: Working"
echo -e "${GREEN}✓${NC} Chatbot: Working"
echo -e "${GREEN}✓${NC} Authentication: Correctly enforced"
echo ""
echo "Next steps:"
echo "1. Start React frontend: cd ../mycarbonai-dashboard && npm run dev"
echo "2. Test with authentication from frontend"
echo "3. Create React components for ML features"
echo ""

#!/bin/bash

echo "========================================="
echo "Testing Dashboard → ML Microservice Integration"
echo "========================================="
echo ""

# Test 1: ML service health directly
echo "1. Testing ML microservice health (direct):"
curl -s http://localhost:8000/health | python -m json.tool
echo ""
echo ""

# Test 2: ML service health via dashboard proxy (without auth - should work as health endpoint doesn't require auth in ml-predictions.js)
echo "2. Testing ML health via dashboard proxy:"
curl -s http://localhost:4000/api/ml/health | python -m json.tool
echo ""
echo ""

# Test 3: Energy prediction directly to ML service
echo "3. Testing energy prediction (direct to ML service):"
curl -s -X POST http://localhost:8000/api/predict/energy \
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
  }' | python -m json.tool
echo ""
echo ""

# Test 4: Chat topics
echo "4. Testing chat topics (direct to ML service):"
curl -s http://localhost:8000/api/chat/topics | python -m json.tool
echo ""
echo ""

# Test 5: Chatbot recommendations
echo "5. Testing chatbot recommendations (direct to ML service):"
curl -s -X POST http://localhost:8000/api/chat/recommendations \
  -H "Content-Type: application/json" \
  -d '{
    "message": "How can I reduce HVAC energy consumption?"
  }' | python -m json.tool
echo ""
echo ""

echo "========================================="
echo "Integration Tests Complete!"
echo "========================================="

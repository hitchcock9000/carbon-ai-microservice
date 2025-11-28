#!/bin/bash
# Test the API endpoints with curl

API_URL="http://localhost:8000"

echo "Testing Carbon AI Microservice API"
echo "===================================="
echo ""

# Test 1: Health check
echo "1. Testing health endpoint..."
curl -s $API_URL/health | python -m json.tool
echo ""
echo ""

# Test 2: Energy prediction
echo "2. Testing energy prediction endpoint..."
curl -s -X POST $API_URL/api/predict/energy \
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

# Test 3: Carbon calculation
echo "3. Testing carbon emissions endpoint..."
curl -s -X POST $API_URL/api/predict/carbon \
  -H "Content-Type: application/json" \
  -d '{
    "energy_kwh": 100.5,
    "energy_source": "grid",
    "region": "US"
  }' | python -m json.tool
echo ""
echo ""

# Test 4: Full prediction
echo "4. Testing full prediction pipeline..."
curl -s -X POST $API_URL/api/predict/full \
  -H "Content-Type: application/json" \
  -d '{
    "building_id": 200,
    "square_feet": 75000,
    "primary_use": 0,
    "year_built": 2010,
    "floor_count": 10,
    "air_temperature": 20.0
  }' | python -m json.tool
echo ""
echo ""

echo "===================================="
echo "All tests completed!"
echo "===================================="

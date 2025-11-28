"""
Simple API Test Script
Test the FastAPI endpoints locally
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from api.services.ml_service import MLService

def test_ml_service():
    """Test ML service initialization and prediction"""
    print("Testing ML Service...")
    print("-" * 50)

    # Initialize service
    ml_service = MLService()

    # Check if model loaded
    print(f"Model loaded: {ml_service.model_loaded}")
    print(f"R² Score: {ml_service.r2_score}")

    if not ml_service.model_loaded:
        print("ERROR: Model not loaded!")
        return False

    # Test data
    test_data = {
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
    }

    print("\nTest Input:")
    for key, value in test_data.items():
        print(f"  {key}: {value}")

    # Make prediction
    try:
        energy_kwh, metadata = ml_service.predict_energy(test_data)
        print(f"\nPredicted Energy: {energy_kwh:.2f} kWh")

        # Test carbon calculation
        carbon_kg, emission_factor = ml_service.calculate_carbon_emissions(
            energy_kwh=energy_kwh,
            energy_source="grid",
            region="US"
        )
        print(f"Carbon Emissions: {carbon_kg:.3f} kg CO2e")
        print(f"Emission Factor: {emission_factor} kg CO2e/kWh")

        print("\n" + "="*50)
        print("All tests passed!")
        print("="*50)
        return True

    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_ml_service()
    sys.exit(0 if success else 1)

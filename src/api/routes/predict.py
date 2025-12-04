"""
Prediction Routes - Energy and Carbon Predictions
"""

from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
import logging

from ..models import (
    EnergyPredictionRequest,
    EnergyPredictionResponse,
    CarbonPredictionRequest,
    CarbonPredictionResponse,
    ErrorResponse
)
from ..services.ml_service import get_ml_service, MLService

# Setup logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/predict", tags=["Predictions"])


@router.post(
    "/energy",
    response_model=EnergyPredictionResponse,
    summary="Predict Energy Consumption",
    description="Predict building energy consumption using XGBoost ML model"
)
async def predict_energy(
    request: EnergyPredictionRequest,
    ml_service: MLService = Depends(get_ml_service)
):
    """
    Predict energy consumption for a building based on features

    - **building_id**: Building identifier
    - **square_feet**: Building area
    - **air_temperature**: Current temperature
    - **timestamp**: Optional timestamp for temporal features
    - Returns predicted energy in kWh
    """
    try:
        logger.info(f"Energy prediction request for building {request.building_id}")

        # Convert request to dict
        data = request.model_dump()

        # Make prediction
        predicted_energy, metadata = ml_service.predict_energy(data)

        # Create response
        response = EnergyPredictionResponse(
            predicted_energy_kwh=round(predicted_energy, 2),
            confidence_score=ml_service.r2_score,
            model_used="XGBoost",
            timestamp=datetime.utcnow().isoformat(),
            metadata=metadata
        )

        logger.info(f"Prediction successful: {predicted_energy:.2f} kWh")
        return response

    except RuntimeError as e:
        logger.error(f"Model error: {e}")
        raise HTTPException(status_code=503, detail="ML model not available")
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@router.post(
    "/carbon",
    response_model=CarbonPredictionResponse,
    summary="Calculate Carbon Emissions",
    description="Calculate carbon emissions from energy consumption"
)
async def predict_carbon(
    request: CarbonPredictionRequest,
    ml_service: MLService = Depends(get_ml_service)
):
    """
    Calculate carbon emissions from energy consumption

    - **energy_kwh**: Energy consumption in kWh
    - **energy_source**: Type of energy source (grid, solar, wind, etc.)
    - **region**: Geographic region for emission factors
    - Returns carbon emissions in kg CO2e
    """
    try:
        logger.info(f"Carbon emission calculation for {request.energy_kwh} kWh")

        # Calculate emissions
        carbon_kg, emission_factor = ml_service.calculate_carbon_emissions(
            energy_kwh=request.energy_kwh,
            energy_source=request.energy_source,
            region=request.region
        )

        # Create response
        response = CarbonPredictionResponse(
            carbon_emissions_kg=round(carbon_kg, 3),
            energy_kwh=request.energy_kwh,
            emission_factor=emission_factor,
            energy_source=request.energy_source,
            region=request.region,
            timestamp=datetime.utcnow().isoformat()
        )

        logger.info(f"Carbon calculation successful: {carbon_kg:.3f} kg CO2e")
        return response

    except Exception as e:
        logger.error(f"Carbon calculation error: {e}")
        raise HTTPException(status_code=500, detail=f"Calculation failed: {str(e)}")


@router.post(
    "/full",
    summary="Full Prediction Pipeline",
    description="Predict energy consumption and calculate carbon emissions in one call"
)
async def predict_full(
    request: EnergyPredictionRequest,
    ml_service: MLService = Depends(get_ml_service)
):
    """
    Complete prediction pipeline: Energy prediction + Carbon calculation

    This endpoint combines both predictions for convenience.
    """
    try:
        logger.info(f"Full prediction pipeline for building {request.building_id}")

        # Predict energy
        data = request.model_dump()
        predicted_energy, metadata = ml_service.predict_energy(data)

        # Calculate carbon
        carbon_kg, emission_factor = ml_service.calculate_carbon_emissions(
            energy_kwh=predicted_energy,
            energy_source="grid",  # Default to grid
            region="US"
        )

        # Combined response
        response = {
            "energy_prediction": {
                "predicted_energy_kwh": round(predicted_energy, 2),
                "confidence_score": ml_service.r2_score,
                "model_used": "XGBoost"
            },
            "carbon_emissions": {
                "carbon_emissions_kg": round(carbon_kg, 3),
                "emission_factor": emission_factor,
                "energy_source": "grid",
                "region": "US"
            },
            "timestamp": datetime.utcnow().isoformat(),
            "metadata": metadata
        }

        logger.info(f"Full prediction successful: {predicted_energy:.2f} kWh, {carbon_kg:.3f} kg CO2e")
        return response

    except Exception as e:
        logger.error(f"Full prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

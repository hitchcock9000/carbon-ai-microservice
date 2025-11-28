"""
ML Service - Energy and Carbon Prediction
Loads XGBoost model and provides prediction functionality
"""

import pickle
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, Tuple
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Model paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
MODELS_DIR = BASE_DIR / "models"
MODEL_PATH = MODELS_DIR / "best_model_xgboost.pkl"


class MLService:
    """Service for ML predictions"""

    def __init__(self):
        self.model = None
        self.model_loaded = False
        self.r2_score = 0.7486  # From training
        self.load_model()

    def load_model(self):
        """Load the trained XGBoost model"""
        try:
            if MODEL_PATH.exists():
                with open(MODEL_PATH, 'rb') as f:
                    self.model = pickle.load(f)
                self.model_loaded = True
                logger.info(f"Model loaded successfully from {MODEL_PATH}")
            else:
                logger.error(f"Model file not found at {MODEL_PATH}")
                self.model_loaded = False
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            self.model_loaded = False

    def prepare_features(self, data: Dict) -> pd.DataFrame:
        """
        Prepare features for prediction

        Args:
            data: Dictionary with input features

        Returns:
            DataFrame with engineered features
        """
        # Extract timestamp features if provided
        timestamp = data.get('timestamp')
        if timestamp:
            try:
                dt = pd.to_datetime(timestamp)
                hour = dt.hour
                day = dt.day
                weekday = dt.weekday()
                month = dt.month
                is_weekend = 1 if weekday >= 5 else 0
            except:
                # Default values if timestamp parsing fails
                now = datetime.utcnow()
                hour = now.hour
                day = now.day
                weekday = now.weekday()
                month = now.month
                is_weekend = 1 if weekday >= 5 else 0
        else:
            now = datetime.utcnow()
            hour = now.hour
            day = now.day
            weekday = now.weekday()
            month = now.month
            is_weekend = 1 if weekday >= 5 else 0

        # Building features
        square_feet = data.get('square_feet', 50000)
        year_built = data.get('year_built', 2000)
        floor_count = data.get('floor_count', 5)
        primary_use = data.get('primary_use', 0)

        # Weather features
        air_temp = data.get('air_temperature', 20.0)
        dew_temp = data.get('dew_temperature', 15.0)
        cloud_coverage = data.get('cloud_coverage', 3.0)
        wind_speed = data.get('wind_speed', 5.0)
        precip = data.get('precip_depth_1_hr', 0.0)
        pressure = data.get('sea_level_pressure', 1013.0)

        # Engineered features
        building_age = 2024 - year_built
        log_square_feet = np.log1p(square_feet)
        sqft_per_floor = square_feet / max(floor_count, 1)

        # Degree hours (simplified - using current temperature)
        cooling_degree_hours = max(0, air_temp - 18)
        heating_degree_hours = max(0, 18 - air_temp)

        # Create feature dictionary matching training data
        features = {
            'square_feet': square_feet,
            'year_built': year_built,
            'floor_count': floor_count,
            'air_temperature': air_temp,
            'cloud_coverage': cloud_coverage,
            'dew_temperature': dew_temp,
            'precip_depth_1_hr': precip,
            'sea_level_pressure': pressure,
            'wind_speed': wind_speed,
            'hour': hour,
            'day': day,
            'weekday': weekday,
            'month': month,
            'primary_use': primary_use,
            'is_weekend': is_weekend,
            'log_square_feet': log_square_feet,
            'building_age': building_age,
            'sqft_per_floor': sqft_per_floor,
            'cooling_degree_hours': cooling_degree_hours,
            'heating_degree_hours': heating_degree_hours
        }

        # Note: lag features and aggregates would require historical data
        # For single predictions, we'll use defaults or omit them
        # The model should still work reasonably well without these

        return pd.DataFrame([features])

    def predict_energy(self, data: Dict) -> Tuple[float, Dict]:
        """
        Predict energy consumption

        Args:
            data: Input features dictionary

        Returns:
            Tuple of (predicted_energy_kwh, metadata)
        """
        if not self.model_loaded:
            raise RuntimeError("Model not loaded. Cannot make predictions.")

        # Prepare features
        features_df = self.prepare_features(data)

        # Make prediction (model predicts log-transformed values)
        log_prediction = self.model.predict(features_df)[0]

        # Transform back to original scale
        energy_kwh = np.expm1(log_prediction)  # Inverse of log1p

        # Ensure non-negative
        energy_kwh = max(0, energy_kwh)

        # Metadata
        metadata = {
            "features_used": list(features_df.columns),
            "input_data": data,
            "model_version": "xgboost_v1",
            "r2_score": self.r2_score
        }

        return energy_kwh, metadata

    def calculate_carbon_emissions(
        self,
        energy_kwh: float,
        energy_source: str = "grid",
        region: str = "US"
    ) -> Tuple[float, float]:
        """
        Calculate carbon emissions from energy consumption

        Args:
            energy_kwh: Energy consumption in kWh
            energy_source: Type of energy source
            region: Geographic region

        Returns:
            Tuple of (carbon_kg, emission_factor)
        """
        # Emission factors (kg CO2e per kWh)
        # Source: EPA and international standards
        emission_factors = {
            "grid": {
                "US": 0.385,      # US average grid
                "EU": 0.295,      # European average
                "UK": 0.233,      # UK grid
                "default": 0.385
            },
            "coal": {
                "default": 0.95   # Coal power
            },
            "natural_gas": {
                "default": 0.41   # Natural gas
            },
            "renewable": {
                "default": 0.02   # Solar/Wind average
            },
            "solar": {
                "default": 0.015  # Solar PV
            },
            "wind": {
                "default": 0.011  # Wind
            },
            "nuclear": {
                "default": 0.012  # Nuclear
            }
        }

        # Get emission factor
        source_factors = emission_factors.get(energy_source.lower(), emission_factors["grid"])
        emission_factor = source_factors.get(region, source_factors.get("default", 0.385))

        # Calculate emissions
        carbon_kg = energy_kwh * emission_factor

        return carbon_kg, emission_factor


# Singleton instance
_ml_service = None

def get_ml_service() -> MLService:
    """Get or create ML service singleton"""
    global _ml_service
    if _ml_service is None:
        _ml_service = MLService()
    return _ml_service

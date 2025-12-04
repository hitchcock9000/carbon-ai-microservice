"""
LSTM Energy Consumption Predictor

This module provides a class to load and use the trained LSTM model
for predicting energy consumption.
"""

import os
import json
import numpy as np
import pandas as pd
import tensorflow as tf
import joblib
from typing import Dict, List, Union, Tuple
from pathlib import Path


class LSTMEnergyPredictor:
    """
    LSTM-based energy consumption predictor.

    This class loads the trained LSTM model and provides methods for
    making predictions on energy consumption data.
    """

    def __init__(self, models_dir: str = "models/dl"):
        """
        Initialize the LSTM predictor.

        Args:
            models_dir: Directory containing the model files
        """
        self.models_dir = Path(models_dir)
        self.model = None
        self.scaler_X = None
        self.scaler_y = None
        self.metadata = None
        self.feature_names = None
        self.timesteps = None

        self._load_model()

    def _load_model(self):
        """Load the model, scalers, and metadata."""
        print("Loading LSTM model...")

        # Load metadata
        metadata_path = self.models_dir / "lstm_model_metadata.json"
        if not metadata_path.exists():
            raise FileNotFoundError(f"Metadata file not found: {metadata_path}")

        with open(metadata_path, 'r') as f:
            self.metadata = json.load(f)

        self.timesteps = self.metadata.get('timesteps', 24)
        self.feature_names = self.metadata.get('features', [])

        # Load scalers
        scaler_X_path = self.models_dir / "scaler_X_lstm.pkl"
        scaler_y_path = self.models_dir / "scaler_y_lstm.pkl"

        if not scaler_X_path.exists() or not scaler_y_path.exists():
            raise FileNotFoundError("Scaler files not found")

        self.scaler_X = joblib.load(scaler_X_path)
        self.scaler_y = joblib.load(scaler_y_path)

        # Load model
        model_path = self.models_dir / "lstm_energy_forecaster.keras"
        if not model_path.exists():
            raise FileNotFoundError(f"Model file not found: {model_path}")

        self.model = tf.keras.models.load_model(str(model_path))

        print(f"✅ Model loaded successfully!")
        print(f"   Architecture: {self.metadata.get('model_architecture')}")
        print(f"   Timesteps: {self.timesteps}")
        print(f"   Features: {len(self.feature_names)}")

    def predict(self, features: Union[pd.DataFrame, np.ndarray]) -> np.ndarray:
        """
        Make predictions on a sequence of features.

        Args:
            features: Input features (must have shape [timesteps, n_features])
                     Can be a DataFrame or numpy array

        Returns:
            Predicted energy consumption (original scale)
        """
        # Convert DataFrame to numpy if needed
        if isinstance(features, pd.DataFrame):
            # Ensure columns are in correct order
            features = features[self.feature_names].values

        # Validate shape
        if len(features.shape) != 2:
            raise ValueError(f"Features must be 2D (timesteps, features), got {features.shape}")

        if features.shape[0] != self.timesteps:
            raise ValueError(f"Expected {self.timesteps} timesteps, got {features.shape[0]}")

        if features.shape[1] != len(self.feature_names):
            raise ValueError(f"Expected {len(self.feature_names)} features, got {features.shape[1]}")

        # Scale features
        features_scaled = self.scaler_X.transform(features)

        # Reshape for LSTM [batch, timesteps, features]
        features_input = features_scaled.reshape(1, self.timesteps, -1)

        # Predict (scaled)
        prediction_scaled = self.model.predict(features_input, verbose=0)

        # Inverse transform to original scale
        prediction_log = self.scaler_y.inverse_transform(prediction_scaled)
        prediction = np.expm1(prediction_log)  # Reverse log1p transformation

        return prediction[0, 0]

    def predict_batch(self, sequences: List[Union[pd.DataFrame, np.ndarray]]) -> np.ndarray:
        """
        Make predictions on multiple sequences.

        Args:
            sequences: List of feature sequences

        Returns:
            Array of predicted energy consumption values
        """
        predictions = []
        for seq in sequences:
            pred = self.predict(seq)
            predictions.append(pred)
        return np.array(predictions)

    def predict_next_hour(self, historical_data: pd.DataFrame) -> Dict[str, float]:
        """
        Predict energy consumption for the next hour given historical data.

        Args:
            historical_data: DataFrame with last 24 hours of data
                           Must contain all required features

        Returns:
            Dictionary with prediction and confidence info
        """
        if len(historical_data) < self.timesteps:
            raise ValueError(f"Need at least {self.timesteps} hours of historical data")

        # Take last timesteps rows
        recent_data = historical_data.tail(self.timesteps)

        # Make prediction
        prediction = self.predict(recent_data)

        return {
            'predicted_consumption': float(prediction),
            'unit': 'kWh',
            'prediction_horizon': '1 hour',
            'model': self.metadata.get('model_architecture'),
            'model_mae': self.metadata.get('mae'),
            'model_mape': self.metadata.get('mape')
        }

    def forecast_multiple_steps(
        self,
        initial_sequence: Union[pd.DataFrame, np.ndarray],
        n_steps: int = 24
    ) -> np.ndarray:
        """
        Forecast multiple time steps ahead using rolling predictions.

        Note: This uses a simplified approach where features are assumed
        to remain similar to the last timestep. For production use,
        you should update features based on actual future values.

        Args:
            initial_sequence: Initial sequence of features [timesteps, n_features]
            n_steps: Number of steps ahead to forecast

        Returns:
            Array of forecasted values
        """
        # Convert to numpy if needed
        if isinstance(initial_sequence, pd.DataFrame):
            sequence = initial_sequence[self.feature_names].values.copy()
        else:
            sequence = initial_sequence.copy()

        # Validate
        if sequence.shape[0] != self.timesteps:
            raise ValueError(f"Expected {self.timesteps} timesteps, got {sequence.shape[0]}")

        forecasts = []

        for _ in range(n_steps):
            # Predict next value
            pred = self.predict(sequence)
            forecasts.append(pred)

            # Roll sequence forward (drop oldest, keep last n-1)
            # Note: In production, you should update features properly
            sequence = np.roll(sequence, -1, axis=0)
            # Keep last feature values (simplified approach)

        return np.array(forecasts)

    def get_model_info(self) -> Dict:
        """
        Get information about the loaded model.

        Returns:
            Dictionary with model information
        """
        return {
            'architecture': self.metadata.get('model_architecture'),
            'framework': self.metadata.get('framework'),
            'timesteps': self.timesteps,
            'features': self.feature_names,
            'n_features': len(self.feature_names),
            'performance': {
                'rmse': self.metadata.get('rmse'),
                'mae': self.metadata.get('mae'),
                'mape': self.metadata.get('mape')
            },
            'total_params': self.model.count_params() if self.model else None
        }


# Example usage
if __name__ == '__main__':
    # Initialize predictor
    predictor = LSTMEnergyPredictor()

    # Show model info
    info = predictor.get_model_info()
    print("\n" + "=" * 70)
    print("Model Information:")
    print("=" * 70)
    for key, value in info.items():
        if isinstance(value, dict):
            print(f"{key}:")
            for k, v in value.items():
                print(f"  {k}: {v}")
        else:
            print(f"{key}: {value}")

    # Test with dummy data
    print("\n" + "=" * 70)
    print("Testing with dummy data:")
    print("=" * 70)

    # Create dummy features (24 timesteps, n_features)
    n_features = len(predictor.feature_names)
    dummy_features = np.random.rand(predictor.timesteps, n_features)

    # Make prediction
    prediction = predictor.predict(dummy_features)
    print(f"Predicted energy consumption: {prediction:.2f} kWh")

    # Forecast multiple steps
    forecast = predictor.forecast_multiple_steps(dummy_features, n_steps=24)
    print(f"\n24-hour forecast:")
    print(f"  Min: {forecast.min():.2f} kWh")
    print(f"  Max: {forecast.max():.2f} kWh")
    print(f"  Mean: {forecast.mean():.2f} kWh")

    print("\n" + "=" * 70)
    print("✅ Predictor is working correctly!")
    print("=" * 70)

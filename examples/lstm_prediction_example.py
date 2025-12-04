"""
Example: Using the LSTM Energy Predictor

This script demonstrates how to use the LSTM model for energy predictions.
"""

import sys
import os
import pandas as pd
import numpy as np

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.models.lstm_predictor import LSTMEnergyPredictor


def example_1_single_prediction():
    """Example 1: Make a single prediction with dummy data"""
    print("=" * 70)
    print("Example 1: Single Prediction")
    print("=" * 70)

    # Initialize predictor
    predictor = LSTMEnergyPredictor(models_dir="models/dl")

    # Get feature names
    feature_names = predictor.feature_names
    print(f"\nRequired features ({len(feature_names)}):")
    for i, name in enumerate(feature_names, 1):
        print(f"  {i}. {name}")

    # Create dummy features for last 24 hours
    dummy_data = {
        'hour': list(range(24)),
        'day': [15] * 24,
        'weekday': [2] * 24,  # Wednesday
        'month': [12] * 24,
        'is_weekend': [0] * 24,
        'log_square_feet': [9.5] * 24,
        'building_age': [10] * 24,
        'floor_count': [5] * 24,
        'air_temperature': [20 + np.sin(np.arange(24) * np.pi / 12) * 5 for _ in range(1)][0],
        'meter_reading_per_sqft': [0.5] * 24,
        'cooling_degree_hours': [5] * 24,
        'heating_degree_hours': [2] * 24,
        'meter_reading_lag1': [100 + np.random.randn() * 10 for _ in range(24)],
        'hourly_avg_per_building': [95] * 24,
        'weekend_avg_per_building': [80] * 24
    }

    df = pd.DataFrame(dummy_data)

    # Make prediction
    prediction = predictor.predict(df)

    print(f"\n✅ Predicted energy consumption: {prediction:.2f} kWh")
    print(f"   (for the next hour)")


def example_2_forecast_24_hours():
    """Example 2: Forecast next 24 hours"""
    print("\n" + "=" * 70)
    print("Example 2: 24-Hour Forecast")
    print("=" * 70)

    predictor = LSTMEnergyPredictor(models_dir="models/dl")

    # Create dummy historical data
    feature_names = predictor.feature_names
    dummy_data = {name: np.random.rand(24) for name in feature_names}
    df = pd.DataFrame(dummy_data)

    # Forecast next 24 hours
    forecast = predictor.forecast_multiple_steps(df, n_steps=24)

    print(f"\n24-Hour Forecast:")
    print(f"  Min:    {forecast.min():.2f} kWh")
    print(f"  Max:    {forecast.max():.2f} kWh")
    print(f"  Mean:   {forecast.mean():.2f} kWh")
    print(f"  Median: {np.median(forecast):.2f} kWh")

    # Show hourly breakdown
    print(f"\nHourly breakdown:")
    for i, value in enumerate(forecast[:8], 1):  # Show first 8 hours
        print(f"  Hour {i}: {value:.2f} kWh")
    print(f"  ...")


def example_3_model_info():
    """Example 3: Get model information"""
    print("\n" + "=" * 70)
    print("Example 3: Model Information")
    print("=" * 70)

    predictor = LSTMEnergyPredictor(models_dir="models/dl")

    info = predictor.get_model_info()

    print(f"\n📊 Model Details:")
    print(f"  Architecture: {info['architecture']}")
    print(f"  Framework: {info['framework']}")
    print(f"  Timesteps: {info['timesteps']}")
    print(f"  Features: {info['n_features']}")
    print(f"  Parameters: {info['total_params']:,}")

    print(f"\n📈 Performance Metrics:")
    print(f"  RMSE: {info['performance']['rmse']:.2f}")
    print(f"  MAE:  {info['performance']['mae']:.2f}")
    print(f"  MAPE: {info['performance']['mape']:.2f}%")

    print(f"\n📝 Required Features:")
    for i, feature in enumerate(info['features'], 1):
        print(f"  {i}. {feature}")


def example_4_batch_predictions():
    """Example 4: Make predictions on multiple sequences"""
    print("\n" + "=" * 70)
    print("Example 4: Batch Predictions")
    print("=" * 70)

    predictor = LSTMEnergyPredictor(models_dir="models/dl")

    # Create 5 different sequences
    n_sequences = 5
    sequences = []

    for i in range(n_sequences):
        dummy_data = {name: np.random.rand(24) for name in predictor.feature_names}
        df = pd.DataFrame(dummy_data)
        sequences.append(df)

    # Make batch predictions
    predictions = predictor.predict_batch(sequences)

    print(f"\nPredicted {n_sequences} sequences:")
    for i, pred in enumerate(predictions, 1):
        print(f"  Sequence {i}: {pred:.2f} kWh")

    print(f"\nBatch statistics:")
    print(f"  Min:  {predictions.min():.2f} kWh")
    print(f"  Max:  {predictions.max():.2f} kWh")
    print(f"  Mean: {predictions.mean():.2f} kWh")


def example_5_realistic_scenario():
    """Example 5: Realistic scenario with actual building data"""
    print("\n" + "=" * 70)
    print("Example 5: Realistic Building Scenario")
    print("=" * 70)

    predictor = LSTMEnergyPredictor(models_dir="models/dl")

    # Simulate realistic building data for past 24 hours
    hours = list(range(24))

    # Simulate temperature variation (warmer during day)
    temperatures = [15 + 10 * np.sin((h - 6) * np.pi / 12) for h in hours]

    # Simulate energy usage pattern (higher during working hours)
    base_usage = 100
    hourly_pattern = [
        base_usage * (0.6 + 0.4 * np.sin((h - 6) * np.pi / 12))
        for h in hours
    ]

    building_data = {
        'hour': hours,
        'day': [15] * 24,
        'weekday': [2] * 24,  # Wednesday
        'month': [12] * 24,
        'is_weekend': [0] * 24,
        'log_square_feet': [10.5] * 24,  # ~36,000 sq ft building
        'building_age': [15] * 24,
        'floor_count': [8] * 24,
        'air_temperature': temperatures,
        'meter_reading_per_sqft': [0.003] * 24,
        'cooling_degree_hours': [max(0, t - 18) for t in temperatures],
        'heating_degree_hours': [max(0, 18 - t) for t in temperatures],
        'meter_reading_lag1': hourly_pattern,
        'hourly_avg_per_building': [90] * 24,
        'weekend_avg_per_building': [70] * 24
    }

    df = pd.DataFrame(building_data)

    # Get prediction for next hour
    result = predictor.predict_next_hour(df)

    print(f"\n🏢 Building Information:")
    print(f"  Size: ~36,000 sq ft")
    print(f"  Floors: 8")
    print(f"  Age: 15 years")

    print(f"\n🌡️  Current Conditions:")
    print(f"  Temperature: {temperatures[-1]:.1f}°C")
    print(f"  Hour: {hours[-1]}:00")
    print(f"  Day: Wednesday")

    print(f"\n⚡ Prediction for Next Hour:")
    print(f"  Consumption: {result['predicted_consumption']:.2f} kWh")
    print(f"  Horizon: {result['prediction_horizon']}")

    print(f"\n📊 Model Performance:")
    print(f"  MAE:  {result['model_mae']:.2f}")
    print(f"  MAPE: {result['model_mape']:.2f}%")


def main():
    """Run all examples"""
    print("\n" + "🔋" * 35)
    print("LSTM Energy Consumption Predictor - Examples")
    print("🔋" * 35)

    try:
        example_1_single_prediction()
        example_2_forecast_24_hours()
        example_3_model_info()
        example_4_batch_predictions()
        example_5_realistic_scenario()

        print("\n" + "=" * 70)
        print("✅ All examples completed successfully!")
        print("=" * 70)

    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you have:")
        print("  1. Trained the model in Google Colab")
        print("  2. Downloaded the model files")
        print("  3. Placed them in models/dl/ directory")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()

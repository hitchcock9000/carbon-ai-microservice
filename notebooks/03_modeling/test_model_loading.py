#!/usr/bin/env python3
"""
Test loading the trained LSTM model and scalers.

This script verifies that the model files downloaded from Colab
can be loaded correctly in the local environment.
"""

import os
import sys
import json
import numpy as np
import tensorflow as tf
import joblib

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

# Paths
MODELS_DIR = '../../models/dl'
MODEL_PATH = os.path.join(MODELS_DIR, 'lstm_energy_forecaster.keras')
SCALER_X_PATH = os.path.join(MODELS_DIR, 'scaler_X_lstm.pkl')
SCALER_Y_PATH = os.path.join(MODELS_DIR, 'scaler_y_lstm.pkl')
METADATA_PATH = os.path.join(MODELS_DIR, 'lstm_model_metadata.json')


def main():
    print("=" * 70)
    print("🧪 Testing LSTM Model Loading")
    print("=" * 70)

    # Check files exist
    print("\n1️⃣ Checking files...")
    files_to_check = {
        'Model': MODEL_PATH,
        'Scaler X': SCALER_X_PATH,
        'Scaler Y': SCALER_Y_PATH,
        'Metadata': METADATA_PATH
    }

    all_exist = True
    for name, path in files_to_check.items():
        full_path = os.path.join(os.path.dirname(__file__), path)
        exists = os.path.exists(full_path)
        status = "✅" if exists else "❌"
        size = f"({os.path.getsize(full_path) / 1024:.1f} KB)" if exists else ""
        print(f"   {status} {name}: {size}")
        if not exists:
            all_exist = False

    if not all_exist:
        print("\n❌ Some files are missing!")
        print("   Make sure you copied all files from Colab to models/dl/")
        return False

    # Load metadata
    print("\n2️⃣ Loading metadata...")
    try:
        with open(os.path.join(os.path.dirname(__file__), METADATA_PATH), 'r') as f:
            metadata = json.load(f)

        print(f"   ✅ Metadata loaded successfully")
        print(f"      Timesteps: {metadata.get('timesteps')}")
        print(f"      Features: {len(metadata.get('features', []))}")
        print(f"      Architecture: {metadata.get('model_architecture')}")
        print(f"      RMSE: {metadata.get('rmse', 0):.2f}")
        print(f"      MAE: {metadata.get('mae', 0):.2f}")
        print(f"      MAPE: {metadata.get('mape', 0):.2f}%")
    except Exception as e:
        print(f"   ❌ Error loading metadata: {e}")
        return False

    # Load scalers
    print("\n3️⃣ Loading scalers...")
    try:
        scaler_X = joblib.load(os.path.join(os.path.dirname(__file__), SCALER_X_PATH))
        scaler_y = joblib.load(os.path.join(os.path.dirname(__file__), SCALER_Y_PATH))

        print(f"   ✅ Scalers loaded successfully")
        print(f"      Scaler X shape: {scaler_X.n_features_in_} features")
        print(f"      Scaler Y shape: {scaler_y.n_features_in_} feature(s)")
    except Exception as e:
        print(f"   ❌ Error loading scalers: {e}")
        return False

    # Load model
    print("\n4️⃣ Loading LSTM model...")
    try:
        model = tf.keras.models.load_model(
            os.path.join(os.path.dirname(__file__), MODEL_PATH)
        )

        print(f"   ✅ Model loaded successfully")
        print(f"      Model name: {model.name}")
        print(f"      Total params: {model.count_params():,}")
        print(f"      Input shape: {model.input_shape}")
        print(f"      Output shape: {model.output_shape}")
    except Exception as e:
        print(f"   ❌ Error loading model: {e}")
        return False

    # Test prediction with dummy data
    print("\n5️⃣ Testing prediction with dummy data...")
    try:
        timesteps = metadata.get('timesteps', 24)
        n_features = len(metadata.get('features', []))

        # Create dummy input
        dummy_input = np.random.rand(1, timesteps, n_features).astype(np.float32)

        # Make prediction
        prediction = model.predict(dummy_input, verbose=0)

        print(f"   ✅ Prediction successful")
        print(f"      Input shape: {dummy_input.shape}")
        print(f"      Output shape: {prediction.shape}")
        print(f"      Predicted value (scaled): {prediction[0, 0]:.4f}")

        # Inverse transform
        prediction_unscaled = scaler_y.inverse_transform(prediction)
        prediction_original = np.expm1(prediction_unscaled)

        print(f"      Predicted value (original): {prediction_original[0, 0]:.2f}")
    except Exception as e:
        print(f"   ❌ Error during prediction: {e}")
        import traceback
        traceback.print_exc()
        return False

    # Summary
    print("\n" + "=" * 70)
    print("✅ ALL TESTS PASSED!")
    print("=" * 70)
    print("\n📊 Model Summary:")
    print(f"   Architecture: {metadata.get('model_architecture')}")
    print(f"   Total parameters: {model.count_params():,}")
    print(f"   Input: ({timesteps} timesteps, {n_features} features)")
    print(f"   Output: Energy consumption prediction")
    print(f"\n📈 Performance:")
    print(f"   RMSE: {metadata.get('rmse', 0):.2f}")
    print(f"   MAE: {metadata.get('mae', 0):.2f}")
    print(f"   MAPE: {metadata.get('mape', 0):.2f}%")
    print("\n🚀 Model is ready to use!")
    print("=" * 70)

    return True


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

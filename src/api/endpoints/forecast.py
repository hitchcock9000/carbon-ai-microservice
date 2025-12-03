"""
FastAPI endpoint para previsão de consumo energético usando LSTM.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List
import tensorflow as tf
import joblib
import numpy as np
import json
import os

router = APIRouter()

# Variáveis globais para modelo e scalers (carregados uma vez no startup)
model = None
scaler_X = None
scaler_y = None
metadata = None

def load_model():
    """Carrega o modelo, scalers e metadados."""
    global model, scaler_X, scaler_y, metadata
    
    try:
        model = tf.keras.models.load_model('models/dl/lstm_energy_forecaster.keras')
        scaler_X = joblib.load('models/dl/scaler_X_lstm.pkl')
        scaler_y = joblib.load('models/dl/scaler_y_lstm.pkl')
        
        with open('models/dl/lstm_model_metadata.json', 'r') as f:
            metadata = json.load(f)
        
        print("✓ Modelo LSTM carregado com sucesso")
        print(f"  - Arquitetura: {metadata.get('model_architecture')}")
        print(f"  - RMSE: {metadata.get('rmse'):.2f}")
        print(f"  - MAE: {metadata.get('mae'):.2f}")
        
    except Exception as e:
        print(f"❌ Erro ao carregar modelo LSTM: {e}")
        raise

# Carregar modelo no startup
if os.path.exists('models/dl/lstm_energy_forecaster.keras'):
    load_model()

class ForecastRequest(BaseModel):
    """
    Request para previsão de consumo energético.
    
    Espera uma sequência de observações passadas (timesteps x features).
    """
    sequence: List[List[float]] = Field(
        ...,
        description="Sequência de timesteps com features. Shape: (timesteps, n_features)",
        example=[
            [12.0, 1.0, 3.0, 12.0, 0.0, 10.5, 25.0, 5.0, 20.5, 0.05, 5.2, 0.0, 150.0, 145.0, 140.0]
            # ... mais 23 timesteps
        ]
    )

class ForecastResponse(BaseModel):
    """Response com a previsão de consumo energético."""
    prediction: float = Field(..., description="Previsão de consumo energético (escala original)")
    prediction_log: float = Field(..., description="Previsão em escala logarítmica")
    model_info: dict = Field(..., description="Informações sobre o modelo usado")

@router.post("/forecast", response_model=ForecastResponse)
async def forecast_energy(request: ForecastRequest):
    """
    Previsão de consumo energético usando LSTM.
    
    **Entrada:**
    - `sequence`: Lista de listas com as últimas observações
      - Shape esperado: (24 timesteps, 15 features)
      - Features (em ordem):
        1. hour (0-23)
        2. day (1-31)
        3. weekday (0-6)
        4. month (1-12)
        5. is_weekend (0 ou 1)
        6. log_square_feet
        7. building_age
        8. floor_count
        9. air_temperature
        10. meter_reading_per_sqft
        11. cooling_degree_hours
        12. heating_degree_hours
        13. meter_reading_lag1
        14. hourly_avg_per_building
        15. weekend_avg_per_building
    
    **Saída:**
    - `prediction`: Previsão de consumo energético (kWh ou unidade original)
    - `prediction_log`: Previsão em escala logarítmica
    - `model_info`: Informações sobre o modelo (arquitetura, métricas)
    """
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Modelo LSTM não está carregado. Verifique os arquivos em models/dl/"
        )
    
    try:
        # Converter para numpy array
        sequence = np.array(request.sequence)
        
        # Validar dimensões
        expected_shape = (metadata['timesteps'], metadata['n_features'])
        if sequence.shape != expected_shape:
            raise HTTPException(
                status_code=400,
                detail=f"Shape inválido. Esperado {expected_shape}, recebido {sequence.shape}"
            )
        
        # Escalar entrada
        sequence_flat = sequence.reshape(-1, metadata['n_features'])
        sequence_scaled = scaler_X.transform(sequence_flat)
        sequence_scaled = sequence_scaled.reshape(1, metadata['timesteps'], metadata['n_features'])
        
        # Predição
        pred_scaled = model.predict(sequence_scaled, verbose=0)[0][0]
        
        # Inverter escala
        pred_log = scaler_y.inverse_transform([[pred_scaled]])[0][0]
        pred_original = np.expm1(pred_log)
        
        return ForecastResponse(
            prediction=float(pred_original),
            prediction_log=float(pred_log),
            model_info={
                "architecture": metadata.get('model_architecture'),
                "rmse": metadata.get('rmse'),
                "mae": metadata.get('mae'),
                "mape": metadata.get('mape'),
                "framework": metadata.get('framework')
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar previsão: {str(e)}"
        )

@router.get("/forecast/info")
async def get_model_info():
    """
    Retorna informações sobre o modelo LSTM.
    """
    if model is None or metadata is None:
        raise HTTPException(
            status_code=503,
            detail="Modelo LSTM não está carregado"
        )
    
    return {
        "model_loaded": True,
        "architecture": metadata.get('model_architecture'),
        "timesteps": metadata.get('timesteps'),
        "n_features": metadata.get('n_features'),
        "features": metadata.get('features'),
        "metrics": {
            "rmse": metadata.get('rmse'),
            "mae": metadata.get('mae'),
            "mape": metadata.get('mape')
        },
        "training_info": {
            "framework": metadata.get('framework'),
            "trained_on": metadata.get('trained_on'),
            "date": metadata.get('date'),
            "training_samples": metadata.get('training_samples'),
            "validation_samples": metadata.get('validation_samples'),
            "test_samples": metadata.get('test_samples')
        }
    }

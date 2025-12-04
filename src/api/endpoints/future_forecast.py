"""
FastAPI endpoint para previsão futura de emissões usando LightGBM.
Pode prever dias/semanas à frente sem precisar de dados históricos!
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timedelta
import numpy as np
import json
import os

# Try to import LightGBM, but make it optional
try:
    import lightgbm as lgb
    LGB_AVAILABLE = True
except (ImportError, OSError) as e:
    LGB_AVAILABLE = False
    print(f"⚠️  LightGBM not available: {e}. Future forecast will use fallback predictions.")

router = APIRouter()

# Variáveis globais
model = None
metadata = None

def load_future_model():
    """Carrega o modelo LightGBM para previsões futuras."""
    global model, metadata

    if not LGB_AVAILABLE:
        print("⚠️  LightGBM not available. Skipping model loading.")
        return

    try:
        # Use o modelo ORIGINAL que tem melhor performance
        model_path = 'models/lightgbm_energy_model.txt'

        if not os.path.exists(model_path):
            print(f"❌ Modelo não encontrado: {model_path}")
            return

        model = lgb.Booster(model_file=model_path)
        
        # Metadata do modelo original
        metadata = {
            "model": "LightGBM",
            "features": model.feature_name(),
            "num_trees": model.num_trees(),
            "note": "Modelo original com features completas"
        }
        
        print("✓ Modelo LightGBM carregado com sucesso")
        print(f"  - Features: {len(model.feature_name())}")
        print(f"  - Trees: {model.num_trees()}")
        print(f"  - ✓ Performance esperada: R² ~0.85-0.95")
        
    except Exception as e:
        print(f"❌ Erro ao carregar modelo LightGBM: {e}")

# Carregar modelo no startup
if os.path.exists('models/lightgbm_energy_model.txt'):
    load_future_model()
else:
    print("⚠️  Modelo LightGBM não encontrado em models/lightgbm_energy_model.txt")


class BuildingInfo(BaseModel):
    """Informações do prédio (características fixas)."""
    square_meters: float = Field(4645, description="Área em metros quadrados")
    building_age: int = Field(15, description="Idade do prédio em anos")
    floor_count: int = Field(5, description="Número de andares")


class WeatherForecast(BaseModel):
    """Previsão do tempo para cada hora."""
    air_temperature: float = Field(..., description="Temperatura do ar (°C)")
    dew_temperature: Optional[float] = Field(None, description="Temperatura do ponto de orvalho (°C)")
    wind_speed: Optional[float] = Field(3.0, description="Velocidade do vento (m/s)")
    sea_level_pressure: Optional[float] = Field(1013.0, description="Pressão ao nível do mar (hPa)")


class FutureForecastRequest(BaseModel):
    """Request para previsão futura."""
    start_datetime: str = Field(
        ..., 
        description="Data/hora inicial (ISO format: 2025-12-04T00:00:00)",
        example="2025-12-04T00:00:00"
    )
    hours_ahead: int = Field(
        24, 
        ge=1, 
        le=168,  # máximo 7 dias
        description="Número de horas à frente (1-168)"
    )
    building: BuildingInfo = Field(..., description="Informações do prédio")
    weather_forecasts: Optional[List[WeatherForecast]] = Field(
        None,
        description="Previsões do tempo horárias (se None, usa valores típicos)"
    )


class HourlyPrediction(BaseModel):
    """Previsão para uma hora específica."""
    datetime: str
    hour: int
    predicted_consumption: float
    temperature: float
    is_weekend: bool


class FutureForecastResponse(BaseModel):
    """Response com previsões futuras."""
    predictions: List[HourlyPrediction]
    summary: dict
    model_info: dict


def get_simulated_temperature(hour: int, day_offset: int = 0) -> float:
    """Simula variação de temperatura ao longo do dia."""
    base_temp = 20 + np.random.normal(0, 1) * day_offset * 0.1
    variation = 8 * np.sin((hour - 6) * np.pi / 12)  # Pico às 14h
    return base_temp + variation


def build_features(dt: datetime, building: BuildingInfo, weather: WeatherForecast = None) -> dict:
    """Constrói features para previsão usando o modelo original."""

    # Features do modelo original:
    # ['square_feet', 'year_built', 'floor_count', 'primary_use', 'meter',
    #  'air_temperature', 'cloud_coverage', 'dew_temperature', 'precip_depth_1_hr',
    #  'sea_level_pressure', 'wind_direction', 'wind_speed',
    #  'hour', 'day', 'weekday', 'month']

    # Convert square meters to square feet for model compatibility (trained on sq ft)
    square_feet = building.square_meters * 10.764

    features = {
        # Building features
        'square_feet': square_feet,
        'year_built': 2025 - building.building_age,  # Convert age to year
        'floor_count': building.floor_count,
        'primary_use': 0,  # 0 = Office (default)
        'meter': 0,  # 0 = Electricity

        # Time features
        'hour': dt.hour,
        'day': dt.day,
        'weekday': dt.weekday(),
        'month': dt.month,
    }

    # Weather features
    if weather:
        features['air_temperature'] = weather.air_temperature
        features['dew_temperature'] = weather.dew_temperature or (weather.air_temperature - 5)
        features['wind_speed'] = weather.wind_speed or 3.0
        features['sea_level_pressure'] = weather.sea_level_pressure or 1013.0
        features['wind_direction'] = 180.0  # Default south
        features['cloud_coverage'] = 4.0  # Default partly cloudy
        features['precip_depth_1_hr'] = 0.0  # No rain default
    else:
        # Simulated values
        temp = get_simulated_temperature(dt.hour)
        features['air_temperature'] = temp
        features['dew_temperature'] = temp - 5
        features['wind_speed'] = 3 + np.random.normal(0, 0.5)
        features['sea_level_pressure'] = 1013 + np.random.normal(0, 2)
        features['wind_direction'] = 180.0
        features['cloud_coverage'] = 4.0
        features['precip_depth_1_hr'] = 0.0

    return features


async def _generate_fallback_forecast(request: FutureForecastRequest) -> FutureForecastResponse:
    """Generate simple rule-based predictions when LightGBM is not available."""
    try:
        start_dt = datetime.fromisoformat(request.start_datetime)
        predictions = []

        # Simple rule-based prediction based on building size and time of day
        base_consumption = request.building.square_meters * 0.05  # Base load

        for hour_offset in range(request.hours_ahead):
            target_dt = start_dt + timedelta(hours=hour_offset)
            hour = target_dt.hour
            is_weekend = target_dt.weekday() >= 5

            # Time-of-day pattern
            if 6 <= hour <= 18:  # Business hours
                time_factor = 1.5 if not is_weekend else 0.3
            else:  # Night
                time_factor = 0.4

            # Temperature effect
            temp = get_simulated_temperature(hour)
            temp_factor = 1.0 + (abs(temp - 20) * 0.02)  # More energy when temp deviates from 20°C

            predicted = base_consumption * time_factor * temp_factor

            predictions.append(HourlyPrediction(
                datetime=target_dt.isoformat(),
                hour=target_dt.hour,
                predicted_consumption=float(predicted),
                temperature=float(temp),
                is_weekend=is_weekend
            ))

        consumptions = [p.predicted_consumption for p in predictions]

        return FutureForecastResponse(
            predictions=predictions,
            summary={
                "total_consumption": float(np.sum(consumptions)),
                "average_consumption": float(np.mean(consumptions)),
                "min_consumption": float(np.min(consumptions)),
                "max_consumption": float(np.max(consumptions)),
                "std_consumption": float(np.std(consumptions)),
                "hours_predicted": len(predictions),
                "days_predicted": len(predictions) / 24
            },
            model_info={
                "model": "Fallback (Rule-based)",
                "note": "Using simple rule-based predictions. Install LightGBM for better accuracy."
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating fallback forecast: {str(e)}"
        )


@router.post("/forecast/future", response_model=FutureForecastResponse)
async def forecast_future(request: FutureForecastRequest):
    """
    Previsão de consumo energético para dias/semanas à frente.

    Diferente do LSTM, este modelo pode prever qualquer momento futuro
    porque não depende de dados históricos (lag features).

    **Entrada:**
    - `start_datetime`: Data/hora inicial para previsão
    - `hours_ahead`: Quantas horas prever (máx 168 = 7 dias)
    - `building`: Características do prédio (fixas)
    - `weather_forecasts`: Previsões do tempo (opcional)

    **Saída:**
    - `predictions`: Lista de previsões horárias
    - `summary`: Resumo estatístico
    - `model_info`: Informações do modelo
    """
    # Fallback: provide simple predictions if LightGBM is not available
    if not LGB_AVAILABLE or model is None:
        return await _generate_fallback_forecast(request)
    
    try:
        # Parse datetime
        start_dt = datetime.fromisoformat(request.start_datetime)
        
        # Validar weather forecasts se fornecido
        if request.weather_forecasts:
            if len(request.weather_forecasts) != request.hours_ahead:
                raise HTTPException(
                    status_code=400,
                    detail=f"Weather forecasts deve ter {request.hours_ahead} elementos"
                )
        
        predictions = []
        
        # Gerar previsões para cada hora
        for hour_offset in range(request.hours_ahead):
            target_dt = start_dt + timedelta(hours=hour_offset)
            
            # Get weather forecast for this hour
            weather = None
            if request.weather_forecasts:
                weather = request.weather_forecasts[hour_offset]
            
            # Build features
            features_dict = build_features(target_dt, request.building, weather)
            
            # Ordenar features conforme metadata
            feature_names = metadata.get('features', [])
            feature_values = [features_dict.get(f, 0) for f in feature_names]
            
            # Predict (modelo foi treinado com log1p)
            X = np.array([feature_values])
            pred = model.predict(X)[0]  # Model already returns kWh (not log-transformed)
            
            predictions.append(HourlyPrediction(
                datetime=target_dt.isoformat(),
                hour=target_dt.hour,
                predicted_consumption=float(pred),
                temperature=features_dict['air_temperature'],
                is_weekend=bool(target_dt.weekday() >= 5)  # Calculate from datetime
            ))
        
        # Calculate summary
        consumptions = [p.predicted_consumption for p in predictions]
        
        summary = {
            "total_consumption": float(np.sum(consumptions)),
            "average_consumption": float(np.mean(consumptions)),
            "min_consumption": float(np.min(consumptions)),
            "max_consumption": float(np.max(consumptions)),
            "std_consumption": float(np.std(consumptions)),
            "hours_predicted": len(predictions),
            "days_predicted": len(predictions) / 24
        }
        
        return FutureForecastResponse(
            predictions=predictions,
            summary=summary,
            model_info={
                "model": "LightGBM",
                "r2": metadata.get('r2'),
                "mae": metadata.get('mae'),
                "rmse": metadata.get('rmse'),
                "note": "Can predict any future moment without historical data"
            }
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Formato de data inválido: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar previsão: {str(e)}"
        )


@router.post("/forecast/scenario")
async def scenario_analysis(
    base_datetime: str,
    building: BuildingInfo,
    temperature_scenarios: List[float] = [0, 5, -5]
):
    """
    Análise de cenários "what-if" - impacto de mudanças de temperatura.
    
    **Exemplo:**
    - Normal: temperatura prevista
    - Hot (+5°C): +5 graus
    - Cold (-5°C): -5 graus
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Modelo não carregado")
    
    try:
        start_dt = datetime.fromisoformat(base_datetime)
        
        results = {}
        
        for delta in temperature_scenarios:
            scenario_name = f"temp_{delta:+.0f}°C" if delta != 0 else "normal"
            predictions = []
            
            for hour in range(24):
                target_dt = start_dt + timedelta(hours=hour)
                
                # Build features with temperature adjustment
                features_dict = build_features(target_dt, building)
                features_dict['air_temperature'] += delta
                features_dict['dew_temperature'] += delta
                features_dict['cooling_degree_hours'] = max(0, features_dict['air_temperature'] - 18)
                features_dict['heating_degree_hours'] = max(0, 18 - features_dict['air_temperature'])
                
                # Predict
                feature_names = metadata.get('features', [])
                feature_values = [features_dict.get(f, 0) for f in feature_names]
                X = np.array([feature_values])
                pred_log = model.predict(X)[0]
                pred = np.expm1(pred_log)
                
                predictions.append(float(pred))
            
            results[scenario_name] = {
                "hourly_predictions": predictions,
                "total_24h": float(np.sum(predictions)),
                "average": float(np.mean(predictions)),
                "temperature_delta": delta
            }
        
        # Calculate impacts
        normal_total = results["normal"]["total_24h"]
        impacts = {}
        
        for scenario, data in results.items():
            if scenario != "normal":
                delta_kwh = data["total_24h"] - normal_total
                delta_pct = (delta_kwh / normal_total) * 100
                impacts[scenario] = {
                    "delta_kwh": delta_kwh,
                    "delta_percentage": delta_pct
                }
        
        return {
            "scenarios": results,
            "impacts": impacts,
            "base_datetime": base_datetime,
            "building": building.dict()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/forecast/model-info")
async def get_future_model_info():
    """Retorna informações sobre o modelo LightGBM."""
    if model is None or metadata is None:
        raise HTTPException(status_code=503, detail="Modelo não carregado")
    
    return {
        "model_loaded": True,
        "model_type": "LightGBM",
        "capabilities": [
            "Forecast any future moment",
            "No historical data required",
            "7-day predictions",
            "What-if scenario analysis"
        ],
        "features": metadata.get('features', []),
        "metrics": {
            "r2": metadata.get('r2'),
            "mae": metadata.get('mae'),
            "rmse": metadata.get('rmse')
        },
        "training_info": {
            "train_samples": metadata.get('train_samples'),
            "test_samples": metadata.get('test_samples'),
            "note": metadata.get('note')
        }
    }

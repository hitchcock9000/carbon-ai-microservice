"""
Pydantic Models - Request/Response schemas
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict
from datetime import datetime


# Prediction Request Models
class EnergyPredictionRequest(BaseModel):
    """Request model for energy consumption prediction"""
    building_id: int = Field(..., description="Building identifier")
    square_feet: float = Field(..., gt=0, description="Building area in square feet")
    primary_use: int = Field(..., ge=0, description="Primary use category (encoded)")
    year_built: Optional[float] = Field(None, description="Year building was constructed")
    floor_count: Optional[float] = Field(None, ge=0, description="Number of floors")
    air_temperature: float = Field(..., description="Air temperature in Celsius")
    dew_temperature: Optional[float] = Field(None, description="Dew point temperature")
    cloud_coverage: Optional[float] = Field(None, ge=0, le=10, description="Cloud coverage (0-10)")
    wind_speed: Optional[float] = Field(None, ge=0, description="Wind speed")
    precip_depth_1_hr: Optional[float] = Field(None, ge=0, description="Precipitation depth")
    sea_level_pressure: Optional[float] = Field(None, description="Sea level pressure")
    timestamp: Optional[str] = Field(None, description="ISO timestamp for prediction")

    class Config:
        json_schema_extra = {
            "example": {
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
                "sea_level_pressure": 1013.25,
                "timestamp": "2024-01-15T14:00:00Z"
            }
        }


class CarbonPredictionRequest(BaseModel):
    """Request model for carbon emissions prediction"""
    energy_kwh: float = Field(..., gt=0, description="Energy consumption in kWh")
    energy_source: Optional[str] = Field("grid", description="Energy source type")
    region: Optional[str] = Field("US", description="Geographic region")

    class Config:
        json_schema_extra = {
            "example": {
                "energy_kwh": 1500.5,
                "energy_source": "grid",
                "region": "US"
            }
        }


# Prediction Response Models
class EnergyPredictionResponse(BaseModel):
    """Response model for energy prediction"""
    predicted_energy_kwh: float = Field(..., description="Predicted energy consumption in kWh")
    confidence_score: float = Field(..., ge=0, le=1, description="Model confidence (R² score)")
    model_used: str = Field(..., description="ML model used for prediction")
    timestamp: str = Field(..., description="Prediction timestamp")
    metadata: Optional[Dict] = Field(None, description="Additional prediction metadata")


class CarbonPredictionResponse(BaseModel):
    """Response model for carbon emissions prediction"""
    carbon_emissions_kg: float = Field(..., description="Carbon emissions in kg CO2e")
    energy_kwh: float = Field(..., description="Energy consumption used")
    emission_factor: float = Field(..., description="Emission factor applied (kg CO2e/kWh)")
    energy_source: str = Field(..., description="Energy source")
    region: str = Field(..., description="Geographic region")
    timestamp: str = Field(..., description="Prediction timestamp")


# Chat Request/Response Models
class ChatRequest(BaseModel):
    """Request model for RAG chatbot"""
    message: str = Field(..., min_length=1, max_length=2000, description="User message")
    context: Optional[Dict] = Field(None, description="Additional context (emissions data, building info)")
    conversation_id: Optional[str] = Field(None, description="Conversation ID for continuity")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "How can I reduce energy consumption in my office building?",
                "context": {
                    "building_type": "office",
                    "current_emissions": 5000
                }
            }
        }


class ChatResponse(BaseModel):
    """Response model for RAG chatbot"""
    response: str = Field(..., description="AI-generated response")
    sources: Optional[List[str]] = Field(None, description="Knowledge base sources used")
    recommendations: Optional[List[str]] = Field(None, description="Actionable recommendations")
    conversation_id: str = Field(..., description="Conversation ID")
    timestamp: str = Field(..., description="Response timestamp")


# Insights Models
class InsightsRequest(BaseModel):
    """Request model for AI insights"""
    emissions_data: List[Dict] = Field(..., description="Historical emissions data")
    building_info: Optional[Dict] = Field(None, description="Building information")

    class Config:
        json_schema_extra = {
            "example": {
                "emissions_data": [
                    {"date": "2024-01", "amount": 1500, "category": "energy"},
                    {"date": "2024-02", "amount": 1600, "category": "energy"}
                ],
                "building_info": {
                    "square_feet": 50000,
                    "type": "office"
                }
            }
        }


class InsightsResponse(BaseModel):
    """Response model for AI insights"""
    insights: Dict = Field(..., description="Detailed insights analysis")
    predictions: Dict = Field(..., description="Future predictions")
    recommendations: List[str] = Field(..., description="AI-generated recommendations")
    confidence: float = Field(..., ge=0, le=1, description="Overall confidence score")
    timestamp: str = Field(..., description="Analysis timestamp")


# Error Response Model
class ErrorResponse(BaseModel):
    """Standard error response"""
    error: str = Field(..., description="Error type")
    detail: str = Field(..., description="Error details")
    timestamp: str = Field(..., description="Error timestamp")

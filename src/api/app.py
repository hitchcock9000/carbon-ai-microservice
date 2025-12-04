"""
FastAPI Application - Carbon AI Microservice
Main application entry point for ML predictions and GenAI features
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from datetime import datetime
import os
from dotenv import load_dotenv

# Import routers
from .routes import predict_router, chat_router
from .static_files import router as static_router

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Carbon AI Microservice",
    description="ML-powered energy prediction and carbon emissions analysis with GenAI recommendations",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(static_router)  # Frontend dashboard
app.include_router(predict_router)
app.include_router(chat_router)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint to verify service status"""
    return {
        "status": "healthy",
        "service": "Carbon AI Microservice",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Carbon AI Microservice API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "prediction": "/api/predict",
            "chat": "/api/chat",
            "insights": "/api/insights"
        }
    }

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Handle all uncaught exceptions"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if os.getenv("DEBUG") == "true" else "An error occurred"
        }
    )

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )

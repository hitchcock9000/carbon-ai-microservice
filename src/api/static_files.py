"""
Static file serving configuration for FastAPI
"""
from fastapi import APIRouter
from fastapi.responses import FileResponse
from pathlib import Path

router = APIRouter()

# Path to static files
STATIC_DIR = Path(__file__).parent.parent.parent / "static"
RESULTS_DIR = Path(__file__).parent.parent.parent / "results"


@router.get("/", tags=["Frontend"])
async def serve_dashboard():
    """Serve the main dashboard"""
    dashboard_path = STATIC_DIR / "dashboard.html"
    if dashboard_path.exists():
        return FileResponse(dashboard_path)
    return {"error": "Dashboard not found"}


@router.get("/dashboard", tags=["Frontend"])
async def serve_dashboard_alt():
    """Alternative route for dashboard"""
    return await serve_dashboard()


@router.get("/results/{filename}", tags=["Results"])
async def serve_results(filename: str):
    """Serve result files (JSON, images, etc.)"""
    result_path = RESULTS_DIR / filename
    if result_path.exists():
        return FileResponse(result_path)
    return {"error": f"Result file {filename} not found"}


@router.get("/health", tags=["Health"])
async def health_check():
    """API health check endpoint"""
    return {
        "status": "online",
        "service": "Carbon AI Microservice",
        "version": "1.0.0"
    }

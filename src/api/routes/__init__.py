"""
API Routes Package
"""

from .predict import router as predict_router
from .chat import router as chat_router

__all__ = ['predict_router', 'chat_router']

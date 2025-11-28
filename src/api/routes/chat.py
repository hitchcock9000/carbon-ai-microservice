"""
Chat Routes - RAG Chatbot Endpoints
"""

from fastapi import APIRouter, HTTPException, Depends
import logging

from ..models import ChatRequest, ChatResponse
from ..services.rag_service import get_rag_service, RAGService

# Setup logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/chat", tags=["Chat"])


@router.post(
    "/recommendations",
    response_model=ChatResponse,
    summary="Get AI Recommendations",
    description="Chat with AI assistant for energy efficiency recommendations"
)
async def chat_recommendations(
    request: ChatRequest,
    rag_service: RAGService = Depends(get_rag_service)
):
    """
    Get AI-powered energy efficiency recommendations

    - **message**: User question or request
    - **context**: Optional context (emissions data, building info)
    - **conversation_id**: Optional ID for conversation continuity
    - Returns AI response with recommendations and sources
    """
    try:
        logger.info(f"Chat request: {request.message[:50]}...")

        # Generate response using RAG
        response_data = rag_service.generate_response(
            query=request.message,
            context=request.context,
            conversation_id=request.conversation_id
        )

        # Create response
        response = ChatResponse(
            response=response_data["response"],
            sources=response_data.get("sources"),
            recommendations=response_data.get("recommendations"),
            conversation_id=response_data["conversation_id"],
            timestamp=response_data["timestamp"]
        )

        logger.info(f"Chat response generated successfully")
        return response

    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")


@router.get(
    "/topics",
    summary="Get Available Topics",
    description="List all available energy efficiency topics in the knowledge base"
)
async def get_topics():
    """
    Get list of all available topics in the knowledge base

    Useful for suggesting conversation starters to users
    """
    from ...genai.knowledge_base import get_all_topics

    try:
        topics = get_all_topics()
        return {
            "topics": topics,
            "count": len(topics),
            "categories": [
                "hvac", "lighting", "envelope", "renewables",
                "monitoring", "equipment", "behavioral",
                "water_heating", "data_center", "quick_wins"
            ]
        }
    except Exception as e:
        logger.error(f"Error getting topics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

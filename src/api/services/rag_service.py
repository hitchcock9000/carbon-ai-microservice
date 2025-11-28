"""
RAG Service - -powered chatbot with energy efficiency knowledge
"""

import os
from typing import List, Dict, Optional
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import knowledge base
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))
from genai.knowledge_base import ENERGY_EFFICIENCY_KNOWLEDGE, search_knowledge

class RAGService:
    """RAG-based chatbot service using """

    def __init__(self):
        self.api_key = os.getenv("")
        self.client = None
        self.conversation_history = {}  # Store by conversation_id
        self.initialize_client()

    def initialize_client(self):
        """Initialize  client"""
        try:
            if self.api_key:
                from  import 
                self.client = (api_key=self.api_key)
                logger.info(" client initialized successfully")
            else:
                logger.warning(" not found. RAG service will use fallback mode.")
        except ImportError:
            logger.warning(" package not installed. Install with: pip install ")
        except Exception as e:
            logger.error(f"Error initializing  client: {e}")

    def retrieve_relevant_knowledge(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        Retrieve relevant knowledge base entries

        Args:
            query: User query
            top_k: Number of top results to return

        Returns:
            List of relevant knowledge entries
        """
        # Simple keyword-based retrieval
        # In production, use vector similarity with embeddings
        results = search_knowledge(query)

        # Return top_k results
        return results[:top_k]

    def format_context(self, knowledge_entries: List[Dict]) -> str:
        """Format knowledge entries as context for """
        if not knowledge_entries:
            return "No specific knowledge base entries found for this query."

        context_parts = ["Here is relevant information from the energy efficiency knowledge base:\n"]

        for i, entry in enumerate(knowledge_entries, 1):
            context_parts.append(f"\n{i}. {entry['topic']}")
            context_parts.append(f"Category: {entry['category']}")
            context_parts.append(f"Priority: {entry['priority']}")
            context_parts.append(f"Content: {entry['content']}\n")

        return "\n".join(context_parts)

    def generate_response_fallback(
        self,
        query: str,
        context: str,
        conversation_history: List[Dict]
    ) -> str:
        """
        Fallback response when  API is not available

        Args:
            query: User query
            context: Retrieved context
            conversation_history: Previous messages

        Returns:
            Fallback response
        """
        # Simple rule-based response
        query_lower = query.lower()

        if "hvac" in query_lower or "temperature" in query_lower or "heating" in query_lower or "cooling" in query_lower:
            return """
            Based on the knowledge base, here are HVAC optimization recommendations:

            1. Adjust temperature setpoints to 22-24°C in summer, 20-22°C in winter
            2. Implement scheduling to reduce HVAC during non-occupied hours (20-30% savings)
            3. Ensure regular maintenance with monthly filter cleaning
            4. Consider variable speed drives for 25-40% energy reduction

            Expected savings: 15-30% energy reduction with 1-3 year payback.

            Would you like more specific recommendations for your building type?
            """

        elif "lighting" in query_lower or "led" in query_lower or "lights" in query_lower:
            return """
            Lighting efficiency recommendations:

            1. Convert to LED lighting for 60-80% energy savings
            2. Install occupancy sensors for 20-30% additional savings
            3. Implement daylight harvesting where possible
            4. Use task lighting to reduce ambient lighting needs

            Expected savings: 30-50% lighting energy reduction with 2-5 year payback.

            Interested in specific product recommendations or ROI calculations?
            """

        elif "solar" in query_lower or "renewable" in query_lower or "pv" in query_lower:
            return """
            Renewable energy options for your building:

            1. Solar PV: Can offset 30-70% of electricity with 7-15 year payback
            2. Solar thermal: Excellent for buildings with high hot water demand
            3. Geothermal: 50-70% heating/cooling savings with 10-20 year payback

            Carbon reduction potential: 30-100% depending on system size.

            Would you like a preliminary feasibility assessment for your building?
            """

        elif "quick" in query_lower or "immediate" in query_lower or "low cost" in query_lower:
            return """
            Quick wins with minimal investment (under $500):

            1. Adjust thermostat setpoints by 1-2°C
            2. Turn off lights in unoccupied areas
            3. Close blinds to reduce solar heat gain
            4. Clean HVAC filters regularly
            5. Enable computer sleep mode and disable screensavers
            6. Schedule HVAC to match occupancy

            Expected savings: 5-10% immediate energy reduction
            Payback: Less than 3 months

            These actions can be implemented immediately while planning larger investments.
            """

        else:
            # Generic response with context
            return f"""
            Based on the energy efficiency knowledge base, I can provide recommendations on:

            - HVAC optimization (40-50% of building energy)
            - Lighting efficiency (15-25% of energy use)
            - Building envelope improvements
            - Renewable energy integration
            - Energy monitoring and management
            - Equipment and plug load optimization
            - Behavioral and operational improvements

            What aspect would you like to explore? I can provide specific, actionable recommendations
            with expected savings and payback periods.

            Relevant context: {context[:500]}...
            """

    def generate_response(
        self,
        query: str,
        context: Optional[Dict] = None,
        conversation_id: Optional[str] = None
    ) -> Dict:
        """
        Generate response using RAG + 

        Args:
            query: User question
            context: Additional context (emissions data, building info)
            conversation_id: ID for conversation continuity

        Returns:
            Response dict with answer, sources, recommendations
        """
        try:
            # Retrieve relevant knowledge
            knowledge_entries = self.retrieve_relevant_knowledge(query)
            formatted_context = self.format_context(knowledge_entries)

            # Get conversation history
            if conversation_id:
                history = self.conversation_history.get(conversation_id, [])
            else:
                conversation_id = f"conv_{datetime.utcnow().timestamp()}"
                history = []

            # If  API is available, use it
            if self.client:
                # Build system message
                system_message = f"""You are an expert energy efficiency consultant specializing in building carbon emissions reduction.

                Your role:
                - Provide actionable, specific recommendations based on the knowledge base
                - Include expected savings percentages and payback periods
                - Prioritize quick wins and high-impact strategies
                - Be concise but comprehensive

                Knowledge base context:
                {formatted_context}

                Additional context: {context if context else 'None provided'}

                Focus on practical, cost-effective solutions."""

                # Build messages
                messages = history + [{"role": "user", "content": query}]

                # Call 
                response = self.client.messages.create(
                    model="-3-5-sonnet-20241022",
                    max_tokens=1024,
                    system=system_message,
                    messages=messages
                )

                answer = response.content[0].text

                # Update conversation history
                history.append({"role": "user", "content": query})
                history.append({"role": "assistant", "content": answer})
                self.conversation_history[conversation_id] = history[-10:]  # Keep last 10 messages

            else:
                # Fallback response
                answer = self.generate_response_fallback(query, formatted_context, history)

            # Extract sources
            sources = [entry["topic"] for entry in knowledge_entries]

            # Extract actionable recommendations
            recommendations = self.extract_recommendations(answer)

            return {
                "response": answer,
                "sources": sources,
                "recommendations": recommendations,
                "conversation_id": conversation_id,
                "timestamp": datetime.utcnow().isoformat()
            }

        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return {
                "response": f"I apologize, but I encountered an error processing your request. Please try again or rephrase your question. Error: {str(e)}",
                "sources": [],
                "recommendations": [],
                "conversation_id": conversation_id or "error",
                "timestamp": datetime.utcnow().isoformat()
            }

    def extract_recommendations(self, text: str) -> List[str]:
        """Extract actionable recommendations from response"""
        recommendations = []
        lines = text.split('\n')

        for line in lines:
            # Look for numbered lists or bullet points
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
                # Clean up formatting
                rec = line.lstrip('0123456789.-•) ').strip()
                if len(rec) > 10:  # Filter out very short items
                    recommendations.append(rec)

        return recommendations[:5]  # Return top 5


# Singleton instance
_rag_service = None

def get_rag_service() -> RAGService:
    """Get or create RAG service singleton"""
    global _rag_service
    if _rag_service is None:
        _rag_service = RAGService()
    return _rag_service

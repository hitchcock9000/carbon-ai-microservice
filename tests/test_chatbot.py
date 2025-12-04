"""
Test RAG Chatbot
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from api.services.rag_service import RAGService

def test_chatbot():
    """Test RAG chatbot with sample queries"""
    print("Testing RAG Chatbot Service")
    print("=" * 50)
    print()

    # Initialize service
    rag_service = RAGService()

    # Test queries
    test_queries = [
        "How can I reduce HVAC energy consumption?",
        "What are quick wins for energy savings?",
        "Should I invest in solar panels?",
        "How can I improve lighting efficiency?"
    ]

    for i, query in enumerate(test_queries, 1):
        print(f"Test {i}: {query}")
        print("-" * 50)

        response = rag_service.generate_response(query)

        print(f"Response: {response['response'][:300]}...")
        print(f"\nSources: {response['sources']}")
        print(f"Recommendations: {len(response['recommendations'])} found")
        if response['recommendations']:
            print("  -", response['recommendations'][0])
        print()
        print("=" * 50)
        print()

    print("All chatbot tests completed!")

if __name__ == "__main__":
    test_chatbot()

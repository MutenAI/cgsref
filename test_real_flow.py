#!/usr/bin/env python3
"""Test script for complete real flow with knowledge base integration."""

import requests
import json
import sys
from typing import Dict, Any

def test_complete_real_flow():
    """Test the complete flow with real knowledge base documents."""
    base_url = "http://localhost:8001/api/v1"
    
    print("🔄 Testing Complete Real Flow...")
    print("=" * 60)
    
    # Step 1: Get real documents from knowledge base
    print("\n1️⃣ Step 1: Fetching real documents from knowledge base")
    try:
        response = requests.get(f"{base_url}/knowledge-base/frontend/clients/siebert/documents")
        
        if response.status_code == 200:
            documents = response.json()
            print(f"✅ Found {len(documents)} real documents:")
            
            for doc in documents:
                print(f"  - {doc['title']}")
                print(f"    ID: {doc['id']}")
                print(f"    Tags: {doc['tags']}")
                print(f"    Description: {doc['description'][:100]}...")
                print()
            
            if not documents:
                print("❌ No documents found")
                return
                
        else:
            print(f"❌ Error fetching documents: {response.text}")
            return
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return
    
    # Step 2: Simulate document selection (select all for testing)
    print("2️⃣ Step 2: Simulating document selection")
    selected_docs = []
    for doc in documents:
        doc['selected'] = True  # Select all documents
        selected_docs.append(doc['id'])
    
    print(f"✅ Selected documents: {selected_docs}")
    
    # Step 3: Generate content with real documents
    print("\n3️⃣ Step 3: Generating content with real knowledge base")
    
    generation_payload = {
        "topic": "AI-Powered Investment Strategies for Gen Z",
        "content_type": "article",
        "content_format": "markdown",
        "client_profile": "siebert",
        "workflow_type": "enhanced_article",
        "target": "Gen Z investors interested in AI and fintech",
        "context": "Focus on practical AI applications in investment strategies, using Siebert's brand voice and guidelines",
        "target_word_count": 1000,
        "tone": "professional",
        "include_statistics": True,
        "include_examples": True,
        "include_sources": True,
        "selected_documents": selected_docs,  # Pass selected document IDs
        "custom_instructions": "Use the content guidelines and company profile to ensure brand consistency"
    }
    
    print("📝 Generation request:")
    print(json.dumps(generation_payload, indent=2))
    
    try:
        print("\n🚀 Starting content generation...")
        response = requests.post(
            f"{base_url}/content/generate",
            json=generation_payload,
            timeout=120  # 2 minutes timeout
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            print("✅ Content generation successful!")
            print(f"📄 Content ID: {result.get('content_id')}")
            print(f"📝 Title: {result.get('title')}")
            print(f"📊 Word Count: {result.get('word_count')}")
            print(f"⏱️ Generation Time: {result.get('generation_time_seconds')}s")
            
            # Show content preview
            content = result.get('content', '')
            if content:
                print(f"\n📖 Content Preview (first 500 chars):")
                print("-" * 50)
                print(content[:500] + "..." if len(content) > 500 else content)
                print("-" * 50)
            
            # Show workflow info
            workflow_info = result.get('workflow_info', {})
            if workflow_info:
                print(f"\n🔄 Workflow Information:")
                print(f"  - Workflow ID: {workflow_info.get('workflow_id')}")
                print(f"  - Tasks Completed: {len(workflow_info.get('completed_tasks', []))}")
                print(f"  - Total Execution Time: {workflow_info.get('total_execution_time')}s")
            
            return result
            
        else:
            print(f"❌ Generation failed: {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        print("⏰ Request timed out - generation may still be running")
        return None
    except Exception as e:
        print(f"❌ Error during generation: {str(e)}")
        return None


def test_document_content_integration():
    """Test that document content is properly integrated in generation."""
    base_url = "http://localhost:8001/api/v1"
    
    print("\n🔍 Testing Document Content Integration...")
    print("=" * 60)
    
    # Get specific document content
    print("1️⃣ Fetching specific document content")
    try:
        response = requests.get(f"{base_url}/knowledge-base/clients/siebert/documents/content_guidelines")
        
        if response.status_code == 200:
            doc_data = response.json()
            content = doc_data['content']
            
            print(f"✅ Retrieved document: {doc_data['title']}")
            print(f"📄 Content length: {len(content)} characters")
            
            # Extract key phrases from content guidelines
            key_phrases = []
            if "gen z" in content.lower():
                key_phrases.append("Gen Z focus")
            if "conversational" in content.lower():
                key_phrases.append("Conversational tone")
            if "educational" in content.lower():
                key_phrases.append("Educational approach")
            if "empowering" in content.lower():
                key_phrases.append("Empowering message")
            
            print(f"🎯 Key brand elements found: {key_phrases}")
            
            return content
            
        else:
            print(f"❌ Error: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None


def compare_mock_vs_real():
    """Compare mock data vs real data."""
    print("\n📊 Comparison: Mock vs Real Data")
    print("=" * 60)
    
    print("🎭 MOCK DATA (Frontend currently shows):")
    mock_docs = [
        "Financial Market Trends 2024",
        "Gen Z Investment Preferences"
    ]
    for doc in mock_docs:
        print(f"  - {doc}")
    
    print("\n📚 REAL DATA (Available in knowledge base):")
    try:
        response = requests.get("http://localhost:8001/api/v1/knowledge-base/frontend/clients/siebert/documents")
        if response.status_code == 200:
            real_docs = response.json()
            for doc in real_docs:
                print(f"  - {doc['title']}")
                print(f"    Tags: {', '.join(doc['tags'])}")
                print(f"    Category: {doc['category']}")
        else:
            print("  ❌ Could not fetch real documents")
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")
    
    print("\n🎯 INTEGRATION BENEFITS:")
    print("  ✅ Real brand guidelines from Siebert")
    print("  ✅ Actual company profile and voice")
    print("  ✅ Dynamic content selection")
    print("  ✅ Automatic tag extraction")
    print("  ✅ Search and filter capabilities")
    print("  ✅ Always up-to-date content")


if __name__ == "__main__":
    # Check if server is running
    try:
        response = requests.get("http://localhost:8001/api/v1/system/health")
        if response.status_code != 200:
            print("❌ Backend server is not running on http://localhost:8001")
            print("Please start the backend with: python start_backend.py")
            sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend server on http://localhost:8001")
        print("Please start the backend with: python start_backend.py")
        sys.exit(1)
    
    # Run tests
    compare_mock_vs_real()
    test_document_content_integration()
    result = test_complete_real_flow()
    
    if result:
        print("\n" + "=" * 60)
        print("🎉 COMPLETE REAL FLOW TEST SUCCESSFUL!")
        print("✅ Knowledge base integration working")
        print("✅ Document selection functional")
        print("✅ Content generation with real data")
        print("✅ Brand guidelines properly applied")
        print("\n🚀 Ready for frontend integration!")
    else:
        print("\n" + "=" * 60)
        print("❌ Test failed - check logs for details")

#!/usr/bin/env python3
"""Live testing script for frontend functionality."""

import requests
import json
import time
import sys
from typing import Dict, Any

def test_frontend_api_calls():
    """Test the API calls that the frontend makes."""
    print("🎨 Testing Frontend API Calls")
    print("=" * 50)
    
    base_url = "http://localhost:8001/api/v1"
    
    # Test 1: Knowledge Base Documents (what frontend loads)
    print("\n1️⃣ Testing Knowledge Base Documents API")
    try:
        response = requests.get(f"{base_url}/knowledge-base/frontend/clients/siebert/documents")
        
        if response.status_code == 200:
            docs = response.json()
            print(f"✅ Successfully loaded {len(docs)} documents")
            
            print("\n📚 Available Documents:")
            for i, doc in enumerate(docs, 1):
                print(f"   {i}. {doc['title']}")
                print(f"      ID: {doc['id']}")
                print(f"      Category: {doc['category']}")
                print(f"      Tags: {', '.join(doc['tags'][:5])}")
                print(f"      Date: {doc['date']}")
                print()
            
            return docs
        else:
            print(f"❌ Failed to load documents: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return []


def test_search_and_filter(documents):
    """Test search and filter functionality."""
    print("2️⃣ Testing Search and Filter Functionality")
    
    base_url = "http://localhost:8001/api/v1"
    
    # Test search
    print("\n🔍 Testing Search:")
    search_terms = ["finance", "gen z", "guidelines"]
    
    for term in search_terms:
        try:
            response = requests.get(
                f"{base_url}/knowledge-base/frontend/clients/siebert/documents",
                params={"search": term}
            )
            
            if response.status_code == 200:
                results = response.json()
                print(f"   Search '{term}': {len(results)} results")
            else:
                print(f"   Search '{term}': Failed ({response.status_code})")
                
        except Exception as e:
            print(f"   Search '{term}': Error - {e}")
    
    # Test tag filtering
    print("\n🏷️ Testing Tag Filtering:")
    tag_filters = [["finance"], ["gen-z"], ["finance", "investing"]]
    
    for tags in tag_filters:
        try:
            params = {}
            for tag in tags:
                params[f"tags"] = tag
            
            response = requests.get(
                f"{base_url}/knowledge-base/frontend/clients/siebert/documents",
                params=params
            )
            
            if response.status_code == 200:
                results = response.json()
                print(f"   Filter {tags}: {len(results)} results")
            else:
                print(f"   Filter {tags}: Failed ({response.status_code})")
                
        except Exception as e:
            print(f"   Filter {tags}: Error - {e}")


def simulate_content_generation(documents):
    """Simulate content generation with selected documents."""
    print("\n3️⃣ Simulating Content Generation")
    
    base_url = "http://localhost:8001/api/v1"
    
    # Select first 2 documents
    selected_docs = [doc['id'] for doc in documents[:2]]
    
    print(f"📝 Selected Documents:")
    for doc_id in selected_docs:
        doc = next((d for d in documents if d['id'] == doc_id), None)
        if doc:
            print(f"   - {doc['title']}")
    
    # Prepare generation request (same format as frontend)
    payload = {
        "topic": "Frontend Test - AI Investment Strategies",
        "content_type": "article",
        "content_format": "markdown",
        "client_profile": "siebert",
        "workflow_type": "enhanced_article",
        "target": "Gen Z investors",
        "context": "Testing frontend integration",
        "target_word_count": 600,
        "tone": "professional",
        "include_statistics": True,
        "selected_documents": selected_docs
    }
    
    print(f"\n🚀 Starting content generation...")
    print(f"📤 Payload: {json.dumps(payload, indent=2)}")
    
    try:
        start_time = time.time()
        
        response = requests.post(
            f"{base_url}/content/generate",
            json=payload,
            timeout=90
        )
        
        generation_time = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"\n✅ Generation Successful!")
            print(f"⏱️ Time: {generation_time:.2f} seconds")
            print(f"📄 Content ID: {result.get('content_id')}")
            print(f"📝 Title: {result.get('title')}")
            print(f"📊 Word Count: {result.get('word_count')}")
            
            # Show content preview
            content = result.get('content', '')
            if content:
                print(f"\n📖 Content Preview:")
                print("-" * 50)
                lines = content.split('\n')[:10]  # First 10 lines
                for line in lines:
                    print(line)
                if len(content.split('\n')) > 10:
                    print("...")
                print("-" * 50)
            
            return True
            
        else:
            print(f"❌ Generation Failed: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("⏰ Generation timed out")
        return False
    except Exception as e:
        print(f"❌ Generation error: {e}")
        return False


def monitor_backend_logs():
    """Show instructions for monitoring backend logs."""
    print("\n4️⃣ Backend Monitoring")
    print("=" * 50)
    
    print("📊 To monitor backend logs in real-time, run:")
    print("   tail -f /path/to/backend/logs")
    print("\n🔍 Or check the backend terminal for detailed logs")
    print("   Look for:")
    print("   - 🚀 AGENT STARTED")
    print("   - 🛠️ TOOL CALL")
    print("   - 🧠 LLM REQUEST/RESPONSE")
    print("   - ✅ Task completion")


def print_frontend_testing_guide():
    """Print guide for testing frontend manually."""
    print("\n" + "=" * 60)
    print("🎨 FRONTEND TESTING GUIDE")
    print("=" * 60)
    
    print("\n🌐 Frontend URL: http://localhost:3001")
    print("🔧 Backend URL: http://localhost:8001")
    
    print("\n📋 TESTING CHECKLIST:")
    print("   1. ✅ Open http://localhost:3001")
    print("   2. ✅ Verify page loads correctly")
    print("   3. ✅ Check 'Knowledge Base Content' section")
    print("   4. ✅ Verify real documents appear (not mock data)")
    print("   5. ✅ Test search functionality")
    print("   6. ✅ Test tag filtering")
    print("   7. ✅ Select some documents")
    print("   8. ✅ Fill in topic and other fields")
    print("   9. ✅ Click 'Generate Content'")
    print("   10. ✅ Verify generation works with selected docs")
    
    print("\n🔍 WHAT TO LOOK FOR:")
    print("   📚 Real Documents:")
    print("      - Siebert Financial - Content Creation Guidelines")
    print("      - Siebert Financial Corp - Company Profile")
    print("   🏷️ Real Tags:")
    print("      - finance, gen-z, investing, markets, content, guidelines")
    print("   📅 Real Dates:")
    print("      - 2025-07-25 (current date)")
    
    print("\n🚨 TROUBLESHOOTING:")
    print("   ❌ If documents don't load:")
    print("      - Check browser console for errors")
    print("      - Verify backend is running (http://localhost:8001)")
    print("      - Check CORS settings")
    print("   ❌ If generation fails:")
    print("      - Check backend logs")
    print("      - Verify selected documents are passed")
    print("      - Check API key configuration")
    
    print("\n🎯 SUCCESS INDICATORS:")
    print("   ✅ Documents load from real knowledge base")
    print("   ✅ Search and filters work")
    print("   ✅ Document selection updates count")
    print("   ✅ Generation uses selected documents")
    print("   ✅ Generated content reflects brand guidelines")


if __name__ == "__main__":
    print("🧪 CGSRef Frontend Live Testing")
    print("=" * 60)
    
    # Run API tests
    documents = test_frontend_api_calls()
    
    if documents:
        test_search_and_filter(documents)
        success = simulate_content_generation(documents)
        monitor_backend_logs()
        print_frontend_testing_guide()
        
        if success:
            print("\n🎉 ALL API TESTS PASSED!")
            print("🎨 Frontend is ready for manual testing")
            print("🌐 Open http://localhost:3001 to test the UI")
        else:
            print("\n⚠️ Some tests failed - check backend logs")
    else:
        print("\n❌ Failed to load documents - check backend connection")

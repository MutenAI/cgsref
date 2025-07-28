#!/usr/bin/env python3
"""Test script for knowledge base endpoints."""

import requests
import json
import sys
from typing import Dict, Any

def test_knowledge_base_endpoints():
    """Test all knowledge base endpoints."""
    base_url = "http://localhost:8001/api/v1"
    
    print("🧪 Testing Knowledge Base Endpoints...")
    print("=" * 50)
    
    # Test 1: Get available clients
    print("\n1️⃣ Testing: GET /knowledge-base/clients")
    try:
        response = requests.get(f"{base_url}/knowledge-base/clients")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            clients = response.json()
            print(f"✅ Available clients: {clients}")
            
            if not clients:
                print("⚠️ No clients found in knowledge base")
                return
                
            # Use first client for further tests
            test_client = clients[0] if clients else "siebert"
            
        else:
            print(f"❌ Error: {response.text}")
            return
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return
    
    # Test 2: Get client documents
    print(f"\n2️⃣ Testing: GET /knowledge-base/clients/{test_client}/documents")
    try:
        response = requests.get(f"{base_url}/knowledge-base/clients/{test_client}/documents")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Client: {data['client_name']}")
            print(f"✅ Total documents: {data['total_documents']}")
            
            if data['documents']:
                print("\n📚 Documents found:")
                for i, doc in enumerate(data['documents'][:3], 1):  # Show first 3
                    print(f"  {i}. {doc['title']}")
                    print(f"     ID: {doc['id']}")
                    print(f"     Tags: {doc['tags']}")
                    print(f"     Size: {doc['size_bytes']} bytes")
                    print(f"     Modified: {doc['last_modified']}")
                    print(f"     Preview: {doc['content_preview'][:100]}...")
                    print()
                
                # Use first document for content test
                test_doc_id = data['documents'][0]['id']
                
            else:
                print("⚠️ No documents found for client")
                return
                
        else:
            print(f"❌ Error: {response.text}")
            return
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return
    
    # Test 3: Get document content
    print(f"\n3️⃣ Testing: GET /knowledge-base/clients/{test_client}/documents/{test_doc_id}")
    try:
        response = requests.get(f"{base_url}/knowledge-base/clients/{test_client}/documents/{test_doc_id}")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Document: {data['title']}")
            print(f"✅ Content length: {len(data['content'])} characters")
            print(f"✅ Metadata: {data['metadata']}")
            print(f"\n📄 Content preview:")
            print(data['content'][:500] + "..." if len(data['content']) > 500 else data['content'])
            
        else:
            print(f"❌ Error: {response.text}")
            return
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return
    
    # Test 4: Search documents
    print(f"\n4️⃣ Testing: Search documents with query 'finance'")
    try:
        response = requests.get(
            f"{base_url}/knowledge-base/clients/{test_client}/documents",
            params={"search": "finance"}
        )
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Search results: {data['total_documents']} documents")
            
            if data['documents']:
                for doc in data['documents']:
                    print(f"  - {doc['title']} (tags: {doc['tags']})")
            else:
                print("  No documents found matching 'finance'")
                
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 5: Filter by tags
    print(f"\n5️⃣ Testing: Filter documents by tags ['finance', 'investing']")
    try:
        response = requests.get(
            f"{base_url}/knowledge-base/clients/{test_client}/documents",
            params={"tags": ["finance", "investing"]}
        )
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Filtered results: {data['total_documents']} documents")
            
            if data['documents']:
                for doc in data['documents']:
                    print(f"  - {doc['title']} (tags: {doc['tags']})")
            else:
                print("  No documents found with specified tags")
                
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🎉 Knowledge Base API testing completed!")


def test_frontend_integration():
    """Test the data format expected by frontend."""
    base_url = "http://localhost:8001/api/v1"
    
    print("\n🎨 Testing Frontend Integration Format...")
    print("=" * 50)
    
    try:
        # Get documents in frontend format
        response = requests.get(f"{base_url}/knowledge-base/clients/siebert/documents")
        
        if response.status_code == 200:
            data = response.json()
            
            # Transform to frontend format
            frontend_docs = []
            for doc in data['documents']:
                frontend_doc = {
                    "id": doc['id'],
                    "title": doc['title'],
                    "description": doc['description'],
                    "date": doc['last_modified'][:10],  # YYYY-MM-DD format
                    "category": doc['tags'][0] if doc['tags'] else "general",
                    "tags": doc['tags'],
                    "selected": False
                }
                frontend_docs.append(frontend_doc)
            
            print("✅ Frontend-compatible format:")
            print(json.dumps(frontend_docs, indent=2))
            
            # Show comparison with current mock data
            print("\n📊 Comparison with mock data:")
            print("Mock documents shown in frontend:")
            print("- Financial Market Trends 2024")
            print("- Gen Z Investment Preferences")
            print()
            print("Real documents available:")
            for doc in frontend_docs:
                print(f"- {doc['title']}")
            
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")


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
    test_knowledge_base_endpoints()
    test_frontend_integration()

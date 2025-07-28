#!/usr/bin/env python3

import requests
import json
import sys

def test_api():
    url = 'http://localhost:8001/api/v1/content/generate'
    
    # Test data
    data = {
        "topic": "AI in Finance for Gen Z Investors",
        "content_type": "article",
        "content_format": "markdown",
        "client_profile": "siebert",
        "workflow_type": "enhanced_article",
        "target": "Gen Z investors interested in AI and fintech",
        "context": "Focus on practical applications and investment opportunities",
        "target_word_count": 800
    }
    
    try:
        print("Testing API endpoint...")
        print(f"URL: {url}")
        print(f"Data: {json.dumps(data, indent=2)}")
        
        response = requests.post(url, json=data, timeout=30)
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ Success!")
            result = response.json()
            print(f"Content ID: {result.get('content_id')}")
            print(f"Title: {result.get('title')}")
            print(f"Word Count: {result.get('word_count')}")
        else:
            print("❌ Error!")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Backend not running on localhost:8001")
    except requests.exceptions.Timeout:
        print("❌ Timeout: Request took too long")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")

if __name__ == "__main__":
    test_api()

"""
Test API endpoint to debug the JSON error
"""
from app import app
import json

# Test the API endpoint directly
with app.test_client() as client:
    print("🔍 Testing /api/fast-predictions endpoint")
    response = client.get('/api/fast-predictions')
    print(f"Status Code: {response.status_code}")
    print(f"Content-Type: {response.content_type}")
    
    # Show first 500 characters of response
    response_text = response.data.decode('utf-8')
    print(f"Response preview:\n{response_text[:500]}")
    
    # Check if response is valid JSON
    try:
        data = response.get_json()
        print("✅ Valid JSON response")
        if data and 'predictions' in data:
            print(f"📊 Found {len(data['predictions'])} predictions")
        elif data and 'error' in data:
            print(f"❌ API returned error: {data['error']}")
    except Exception as e:
        print(f"❌ JSON parsing error: {e}")
        print("This suggests the API is returning HTML instead of JSON")

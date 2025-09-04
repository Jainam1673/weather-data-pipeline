#!/usr/bin/env python3
"""
Test script for the Open-Meteo API integration
"""

import requests
import json
import time

API_BASE = "http://localhost:8000"

def test_endpoint(endpoint, description):
    """Test an API endpoint"""
    print(f"\n🧪 Testing: {description}")
    print(f"📍 Endpoint: {endpoint}")
    print("-" * 50)
    
    try:
        response = requests.get(f"{API_BASE}{endpoint}", timeout=10)
        print(f"✅ Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"📊 Response Data:")
            print(json.dumps(data, indent=2))
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_generate_data():
    """Test data generation with Open-Meteo API only"""
    print(f"\n🚀 Testing: Data Generation with Open-Meteo API")
    print("-" * 50)
    
    try:
        payload = {
            "num_points": 24,
            "latitude": 51.5074,
            "longitude": -0.1278
        }
        
        response = requests.post(f"{API_BASE}/generate-data", json=payload, timeout=10)
        print(f"✅ Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"📊 Response:")
            print(json.dumps(data, indent=2))
            
            # Wait a bit for processing
            print("\n⏳ Waiting 5 seconds for data processing...")
            time.sleep(5)
            
            # Check if data was stored
            weather_data = requests.get(f"{API_BASE}/weather-data?limit=10")
            if weather_data.status_code == 200:
                stored_data = weather_data.json()
                print(f"📈 Stored data points: {len(stored_data.get('data', []))}")
            
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    print("🌤️ Open-Meteo API Integration Test")
    print("=" * 60)
    
    # Test basic endpoints
    test_endpoint("/", "Root endpoint")
    test_endpoint("/health", "Health check")
    test_endpoint("/locations/popular", "Popular locations")
    
    # Test Open-Meteo specific endpoints
    test_endpoint("/openmeteo/current/51.5074/-0.1278", "Current weather for London")
    test_endpoint("/openmeteo/forecast/51.5074/-0.1278?days=1", "Weather forecast for London")
    
    # Test data generation
    test_generate_data()
    
    print("\n🎉 Test complete!")

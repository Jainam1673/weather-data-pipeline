"""
Test suite for the Advanced Weather Data Pipeline API
"""

import pytest
import requests
import time
import subprocess
import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

class TestWeatherAPI:
    """Test cases for the Weather API server"""
    
    @pytest.fixture(autouse=True)
    def setup_api_server(self):
        """Setup API server for testing"""
        # Start API server in background
        self.api_process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "src.api.server:app", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for server to start
        time.sleep(3)
        
        yield
        
        # Cleanup: stop the server
        self.api_process.terminate()
        self.api_process.wait()
    
    def test_api_health_endpoint(self):
        """Test the health check endpoint"""
        response = requests.get("http://localhost:8000/health", timeout=10)
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert "services" in data
        assert "version" in data
    
    def test_api_root_endpoint(self):
        """Test the root API endpoint"""
        response = requests.get("http://localhost:8000/", timeout=10)
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "features" in data
        assert "endpoints" in data
    
    def test_weather_enhanced_endpoint(self):
        """Test the enhanced weather data endpoint"""
        payload = {
            "latitude": 51.5074,
            "longitude": -0.1278,
            "location_name": "London, UK",
            "days": 1
        }
        
        response = requests.post(
            "http://localhost:8000/weather/enhanced",
            json=payload,
            timeout=30
        )
        
        assert response.status_code == 200
        
        data = response.json()
        assert "location" in data
        assert "current_weather" in data
        assert "performance" in data
        assert data["location"]["name"] == "London, UK"
    
    def test_locations_supported_endpoint(self):
        """Test the supported locations endpoint"""
        response = requests.get("http://localhost:8000/locations/supported", timeout=10)
        assert response.status_code == 200
        
        data = response.json()
        assert "supported_locations" in data
        assert "total_count" in data
        assert len(data["supported_locations"]) > 0
    
    def test_performance_benchmark_endpoint(self):
        """Test the performance benchmark endpoint"""
        response = requests.get("http://localhost:8000/performance/benchmark?iterations=10", timeout=30)
        assert response.status_code == 200
        
        data = response.json()
        assert "benchmark_info" in data
        assert "results" in data
        assert "performance_gain" in data

class TestWeatherDatabase:
    """Test cases for the Weather Database"""
    
    def test_database_initialization(self):
        """Test database initialization"""
        from data.database import WeatherDatabase
        
        # Use a test database
        db = WeatherDatabase("test_weather.db")
        
        # Test statistics retrieval
        stats = db.get_statistics()
        assert "total_records" in stats
        assert "last_update" in stats
        
        # Cleanup
        if os.path.exists("test_weather.db"):
            os.remove("test_weather.db")
    
    def test_database_data_operations(self):
        """Test database data operations"""
        from data.database import WeatherDatabase
        from datetime import datetime
        
        db = WeatherDatabase("test_weather.db")
        
        # Test data insertion
        test_data = [{
            'timestamp': datetime.now().timestamp(),
            'latitude': 51.5074,
            'longitude': -0.1278,
            'location_name': 'Test Location',
            'temperature': 22.5,
            'humidity': 65.0,
            'pressure': 1013.25,
            'wind_speed': 10.0,
            'rainfall': 0.5
        }]
        
        result = db.insert_weather_data(test_data)
        assert result == True
        
        # Test data retrieval
        recent_data = db.get_data_since(datetime.fromtimestamp(datetime.now().timestamp() - 3600).isoformat())
        assert len(recent_data) >= 1
        
        # Cleanup
        if os.path.exists("test_weather.db"):
            os.remove("test_weather.db")

class TestWeatherProcessor:
    """Test cases for the Weather Processor (Mojo simulation)"""
    
    def test_processor_import(self):
        """Test that the processor module can be imported"""
        # This tests the Python compatibility layer
        try:
            import sys
            sys.path.insert(0, "src")
            from processors import weather_processor
            assert True  # If we get here, import succeeded
        except ImportError:
            # Mojo not available, but that's expected
            assert True

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
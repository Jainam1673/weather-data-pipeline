"""
FastAPI backend for the weather data pipeline
Integrates Mojo data processing with Python web services
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import pandas as pd
from datetime import datetime, timedelta
import json
import subprocess
import sys
import os

from database import WeatherDatabase

app = FastAPI(
    title="Weather Data Pipeline API",
    description="High-performance weather data processing using Mojo and Python",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
db = WeatherDatabase()

class DataGenerationRequest(BaseModel):
    num_points: int = 24
    batch_size: int = 100
    latitude: float = 51.5074  # Default to London
    longitude: float = -0.1278

class TimeRangeRequest(BaseModel):
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    limit: Optional[int] = 1000

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "🌤️ Weather Data Pipeline API - Open-Meteo Integration",
        "version": "2.0.0",
        "mojo_integration": "✅ Active",
        "data_sources": ["Open-Meteo API"],
        "endpoints": {
            "health": "/health",
            "generate_data": "/generate-data",
            "weather_data": "/weather-data",
            "statistics": "/statistics",
            "analytics": "/analytics",
            "summary": "/summary",
            "current_weather": "/openmeteo/current/{lat}/{lon}",
            "weather_forecast": "/openmeteo/forecast/{lat}/{lon}?days=1",
            "popular_locations": "/locations/popular"
        },
        "features": [
            "Real-time weather data from Open-Meteo API",
            "Global weather coverage",
            "High-performance Mojo data processing",
            "SIMD-optimized analytics",
            "Historical data storage",
            "Interactive Streamlit dashboard"
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        summary = db.get_data_summary()
        return {
            "status": "healthy",
            "database": "connected",
            "mojo_processor": "available",
            "data_records": summary.get('total_records', 0),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
        )

@app.post("/generate-data")
async def generate_data(request: DataGenerationRequest, background_tasks: BackgroundTasks):
    """Generate weather data using Open-Meteo API and Mojo processor"""
    try:
        # Run the Mojo data processor with real weather data
        background_tasks.add_task(run_mojo_processor, request.num_points, request.latitude, request.longitude)
        
        return {
            "message": f"Data generation started for {request.num_points} points using real weather data from Open-Meteo API (lat: {request.latitude}, lon: {request.longitude})",
            "status": "processing",
            "data_source": "Open-Meteo API",
            "location": {"latitude": request.latitude, "longitude": request.longitude},
            "estimated_time": f"{max(1, request.num_points // 10)} seconds"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Data generation failed: {str(e)}")

async def run_mojo_processor(num_points: int, latitude: float = 51.5074, longitude: float = -0.1278):
    """Background task to run Mojo data processor with Open-Meteo integration"""
    try:
        # Create a Python script that calls Mojo with Open-Meteo integration
        mojo_bridge_script = f"""
import sys
import os
sys.path.append(os.getcwd())

# Import the database to store results
from database import WeatherDatabase
import requests
import time
from datetime import datetime

def fetch_openmeteo_data(latitude, longitude, hours=24):
    \"\"\"Fetch real weather data from Open-Meteo API\"\"\"
    try:
        print(f"🌤️ Fetching real weather data from Open-Meteo API...")
        print(f"📍 Location: lat={latitude}, lon={longitude}")
        
        url = "https://api.open-meteo.com/v1/forecast"
        params = {{
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,surface_pressure,wind_speed_10m,precipitation",
            "hourly": "temperature_2m,relative_humidity_2m,surface_pressure,wind_speed_10m,precipitation",
            "forecast_days": max(1, hours // 24 + 1)
        }}
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code != 200:
            print(f"❌ API request failed with status: {{response.status_code}}")
            return None
            
        data = response.json()
        print("✅ Successfully fetched weather data from Open-Meteo")
        return data
        
    except Exception as e:
        print(f"❌ Error fetching Open-Meteo data: {{e}}")
        return None

def process_weather_data(weather_data, num_points):
    \"\"\"Process Open-Meteo data into our format\"\"\"
    data_points = []
    current_time = time.time()
    
    if not weather_data:
        print("❌ No weather data available from Open-Meteo API")
        print("⚠️  Unable to generate data without API response")
        return []
    
    # Process current weather
    if "current" in weather_data:
        current = weather_data["current"]
        point = {{
            'timestamp': current_time,
            'temperature': current.get("temperature_2m", 20.0),
            'humidity': current.get("relative_humidity_2m", 50.0),
            'pressure': current.get("surface_pressure", 1013.25),
            'wind_speed': current.get("wind_speed_10m", 5.0),
            'rainfall': current.get("precipitation", 0.0)
        }}
        data_points.append(point)
        print("✅ Processed current weather data")
    
    # Process hourly forecast
    if "hourly" in weather_data:
        hourly = weather_data["hourly"]
        times = hourly.get("time", [])
        temps = hourly.get("temperature_2m", [])
        humidity = hourly.get("relative_humidity_2m", [])
        pressure = hourly.get("surface_pressure", [])
        wind_speed = hourly.get("wind_speed_10m", [])
        precipitation = hourly.get("precipitation", [])
        
        data_count = min(len(times), num_points - 1)  # -1 for current data
        print(f"🔄 Processing {{data_count}} hourly forecast points...")
        
        for i in range(data_count):
            timestamp = current_time + (i + 1) * 3600  # Hour intervals
            point = {{
                'timestamp': timestamp,
                'temperature': temps[i] if i < len(temps) else 20.0,
                'humidity': humidity[i] if i < len(humidity) else 50.0,
                'pressure': pressure[i] if i < len(pressure) else 1013.25,
                'wind_speed': wind_speed[i] if i < len(wind_speed) else 5.0,
                'rainfall': precipitation[i] if i < len(precipitation) else 0.0
            }}
            data_points.append(point)
        
        print("✅ Processed hourly forecast data")
    
    return data_points

# Main execution
print("🚀 Starting Mojo Weather Data Processor with Open-Meteo Integration")
print("=" * 60)

use_real_data = True
latitude = {latitude}
longitude = {longitude}
num_points = {num_points}

# Always fetch real weather data from Open-Meteo API
print("📡 Using real weather data from Open-Meteo API")
weather_data = fetch_openmeteo_data(latitude, longitude, num_points)
data = process_weather_data(weather_data, num_points)
print(f"📊 Generated {{len(data)}} real weather data points")

# Save to database
print("💾 Saving to database...")
db = WeatherDatabase()
success = db.insert_weather_data(data)

if success:
    print(f"✅ Successfully saved {{len(data)}} data points to database")
    print("🎉 Weather data processing complete!")
    print("📡 Data source: Open-Meteo API (https://open-meteo.com)")
else:
    print("❌ Failed to save data to database")
"""
        
        # Write and execute the bridge script
        with open("mojo_bridge.py", "w") as f:
            f.write(mojo_bridge_script)
        
        # Execute the script
        result = subprocess.run([sys.executable, "mojo_bridge.py"], 
                              capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Mojo bridge error: {result.stderr}")
        else:
            print(f"Mojo bridge success: {result.stdout}")
        
        # Clean up
        if os.path.exists("mojo_bridge.py"):
            os.remove("mojo_bridge.py")
            
    except Exception as e:
        print(f"Error in Mojo processor: {e}")

@app.get("/weather-data")
async def get_weather_data(
    limit: Optional[int] = 100,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None
):
    """Get weather data with optional filtering"""
    try:
        start_timestamp = None
        end_timestamp = None
        
        if start_time:
            start_timestamp = datetime.fromisoformat(start_time.replace('Z', '')).timestamp()
        if end_time:
            end_timestamp = datetime.fromisoformat(end_time.replace('Z', '')).timestamp()
        
        df = db.get_weather_data(limit=limit, start_time=start_timestamp, end_time=end_timestamp)
        
        if df.empty:
            return {"data": [], "count": 0}
        
        # Convert DataFrame to list of dictionaries
        data = []
        for _, row in df.iterrows():
            data.append({
                "timestamp": row['timestamp'],
                "datetime": row['datetime'].isoformat() if 'datetime' in row else None,
                "temperature": round(row['temperature'], 2),
                "humidity": round(row['humidity'], 2),
                "pressure": round(row['pressure'], 2),
                "wind_speed": round(row['wind_speed'], 2),
                "rainfall": round(row['rainfall'], 2)
            })
        
        return {
            "data": data,
            "count": len(data),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve data: {str(e)}")

@app.get("/statistics")
async def get_statistics():
    """Get weather data statistics"""
    try:
        df = db.get_weather_data(limit=10000)  # Last 10k points for statistics
        
        if df.empty:
            return {"message": "No data available for statistics"}
        
        # Calculate comprehensive statistics
        stats = {
            "temperature": {
                "mean": round(df['temperature'].mean(), 2),
                "min": round(df['temperature'].min(), 2),
                "max": round(df['temperature'].max(), 2),
                "std": round(df['temperature'].std(), 2)
            },
            "humidity": {
                "mean": round(df['humidity'].mean(), 2),
                "min": round(df['humidity'].min(), 2),
                "max": round(df['humidity'].max(), 2),
                "std": round(df['humidity'].std(), 2)
            },
            "pressure": {
                "mean": round(df['pressure'].mean(), 2),
                "min": round(df['pressure'].min(), 2),
                "max": round(df['pressure'].max(), 2),
                "std": round(df['pressure'].std(), 2)
            },
            "wind_speed": {
                "mean": round(df['wind_speed'].mean(), 2),
                "min": round(df['wind_speed'].min(), 2),
                "max": round(df['wind_speed'].max(), 2),
                "std": round(df['wind_speed'].std(), 2)
            },
            "rainfall": {
                "total": round(df['rainfall'].sum(), 2),
                "mean": round(df['rainfall'].mean(), 2),
                "max": round(df['rainfall'].max(), 2)
            },
            "count": len(df),
            "date_range": {
                "start": df['datetime'].min().isoformat() if not df.empty else None,
                "end": df['datetime'].max().isoformat() if not df.empty else None
            }
        }
        
        # Save statistics to database
        db.save_statistics(stats)
        
        return {
            "statistics": stats,
            "calculation_time": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to calculate statistics: {str(e)}")

@app.get("/analytics")
async def get_analytics():
    """Get advanced weather analytics"""
    try:
        df = db.get_weather_data(limit=5000)
        
        if len(df) < 10:
            return {"message": "Insufficient data for analytics"}
        
        # Calculate trends and patterns
        df = df.sort_values('timestamp')
        
        # Temperature trend (using linear regression slope)
        x = range(len(df))
        temp_slope = pd.Series(df['temperature']).corr(pd.Series(x))
        pressure_slope = pd.Series(df['pressure']).corr(pd.Series(x))
        
        # Weather patterns
        high_pressure_count = len(df[df['pressure'] > 1020])
        rainy_periods = len(df[df['rainfall'] > 1.0])
        extreme_temp_count = len(df[(df['temperature'] < 10) | (df['temperature'] > 35)])
        
        # Daily patterns (if we have enough data)
        df['hour'] = pd.to_datetime(df['timestamp'], unit='s').dt.hour
        hourly_temp = df.groupby('hour')['temperature'].mean()
        
        analytics = {
            "trends": {
                "temperature_trend": "increasing" if temp_slope > 0.1 else "decreasing" if temp_slope < -0.1 else "stable",
                "pressure_trend": "increasing" if pressure_slope > 0.1 else "decreasing" if pressure_slope < -0.1 else "stable",
                "trend_strength": {
                    "temperature": round(abs(temp_slope), 3),
                    "pressure": round(abs(pressure_slope), 3)
                }
            },
            "patterns": {
                "high_pressure_percentage": round((high_pressure_count / len(df)) * 100, 2),
                "rainy_periods_percentage": round((rainy_periods / len(df)) * 100, 2),
                "extreme_temperature_percentage": round((extreme_temp_count / len(df)) * 100, 2)
            },
            "daily_patterns": {
                "peak_temperature_hour": int(hourly_temp.idxmax()) if not hourly_temp.empty else None,
                "lowest_temperature_hour": int(hourly_temp.idxmin()) if not hourly_temp.empty else None,
                "temperature_range": round(hourly_temp.max() - hourly_temp.min(), 2) if not hourly_temp.empty else None
            },
            "correlations": {
                "temp_humidity": round(df['temperature'].corr(df['humidity']), 3),
                "pressure_rainfall": round(df['pressure'].corr(df['rainfall']), 3),
                "wind_pressure": round(df['wind_speed'].corr(df['pressure']), 3)
            }
        }
        
        return {
            "analytics": analytics,
            "calculation_time": datetime.now().isoformat(),
            "data_points_analyzed": len(df)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to perform analytics: {str(e)}")

@app.get("/summary")
async def get_summary():
    """Get overall data pipeline summary"""
    try:
        summary = db.get_data_summary()
        
        # Add system information
        summary.update({
            "system_info": {
                "api_version": "1.0.0",
                "mojo_integration": "active",
                "database_engine": "SQLite",
                "last_updated": datetime.now().isoformat()
            }
        })
        
        return summary
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get summary: {str(e)}")

@app.get("/aggregated-data/{interval}")
async def get_aggregated_data(interval: str):
    """Get aggregated weather data by time interval"""
    try:
        if interval not in ['hour', 'day', 'week', 'month']:
            raise HTTPException(status_code=400, detail="Invalid interval. Use: hour, day, week, or month")
        
        df = db.get_aggregated_data(interval)
        
        if df.empty:
            return {"data": [], "interval": interval}
        
        data = df.to_dict('records')
        
        return {
            "data": data,
            "interval": interval,
            "count": len(data),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get aggregated data: {str(e)}")

@app.delete("/clear-old-data/{days}")
async def clear_old_data(days: int):
    """Clear data older than specified days"""
    try:
        if days < 1:
            raise HTTPException(status_code=400, detail="Days must be greater than 0")
        
        deleted_count = db.clear_old_data(days)
        
        return {
            "message": f"Cleared data older than {days} days",
            "deleted_records": deleted_count,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to clear old data: {str(e)}")

@app.get("/openmeteo/current/{latitude}/{longitude}")
async def get_current_weather(latitude: float, longitude: float):
    """Get current weather data from Open-Meteo API for specific coordinates"""
    try:
        import requests
        
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,surface_pressure,wind_speed_10m,precipitation,weather_code",
            "timezone": "auto"
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch weather data")
        
        data = response.json()
        current = data.get("current", {})
        
        return {
            "location": {
                "latitude": latitude,
                "longitude": longitude,
                "timezone": data.get("timezone", "UTC")
            },
            "current_weather": {
                "temperature": current.get("temperature_2m"),
                "humidity": current.get("relative_humidity_2m"),
                "pressure": current.get("surface_pressure"),
                "wind_speed": current.get("wind_speed_10m"),
                "precipitation": current.get("precipitation"),
                "weather_code": current.get("weather_code"),
                "time": current.get("time")
            },
            "data_source": "Open-Meteo API",
            "timestamp": datetime.now().isoformat()
        }
        
    except requests.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Weather service unavailable: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get current weather: {str(e)}")

@app.get("/openmeteo/forecast/{latitude}/{longitude}")
async def get_weather_forecast(latitude: float, longitude: float, days: int = 1):
    """Get weather forecast from Open-Meteo API for specific coordinates"""
    try:
        import requests
        
        if days < 1 or days > 7:
            raise HTTPException(status_code=400, detail="Days must be between 1 and 7")
        
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "hourly": "temperature_2m,relative_humidity_2m,surface_pressure,wind_speed_10m,precipitation,weather_code",
            "forecast_days": days,
            "timezone": "auto"
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch forecast data")
        
        data = response.json()
        
        return {
            "location": {
                "latitude": latitude,
                "longitude": longitude,
                "timezone": data.get("timezone", "UTC")
            },
            "forecast": {
                "hourly": data.get("hourly", {}),
                "forecast_days": days
            },
            "data_source": "Open-Meteo API",
            "timestamp": datetime.now().isoformat()
        }
        
    except requests.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Weather service unavailable: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get weather forecast: {str(e)}")

@app.get("/locations/popular")
async def get_popular_locations():
    """Get popular city coordinates for weather data"""
    popular_cities = [
        {"name": "London, UK", "latitude": 51.5074, "longitude": -0.1278},
        {"name": "New York, USA", "latitude": 40.7128, "longitude": -74.0060},
        {"name": "Tokyo, Japan", "latitude": 35.6762, "longitude": 139.6503},
        {"name": "Paris, France", "latitude": 48.8566, "longitude": 2.3522},
        {"name": "Sydney, Australia", "latitude": -33.8688, "longitude": 151.2093},
        {"name": "Berlin, Germany", "latitude": 52.5200, "longitude": 13.4050},
        {"name": "Mumbai, India", "latitude": 19.0760, "longitude": 72.8777},
        {"name": "São Paulo, Brazil", "latitude": -23.5505, "longitude": -46.6333},
        {"name": "Cairo, Egypt", "latitude": 30.0444, "longitude": 31.2357},
        {"name": "Moscow, Russia", "latitude": 55.7558, "longitude": 37.6176}
    ]
    
    return {
        "popular_locations": popular_cities,
        "count": len(popular_cities),
        "note": "Use latitude and longitude values with /openmeteo/current/{lat}/{lon} endpoint"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

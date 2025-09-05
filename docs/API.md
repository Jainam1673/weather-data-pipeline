# API Documentation - Advanced Weather Data Pipeline v2.0
==========================================================

## Overview

The Weather API provides comprehensive weather data processing with machine learning capabilities, powered by Mojo for high-performance computations.

## Base URL

- Development: `http://localhost:8000`
- Production: `https://your-domain.com/api`

## Authentication

Currently, the API is open for demonstration purposes. In production, implement proper API key authentication.

## Endpoints

### Health Check

**GET** `/health`

Returns system health and version information.

```json
{
  "status": "healthy",
  "version": "2.0.0",
  "timestamp": "2024-01-01T00:00:00Z",
  "components": {
    "database": "✅ Connected",
    "mojo": "✅ Available",
    "memory_usage": "45%"
  }
}
```

### Weather Data

**GET** `/weather/{location}`

Fetch enhanced weather data with Mojo processing.

**Parameters:**
- `location` (path): City name or coordinates (lat,lon)

**Response:**
```json
{
  "location": "New York",
  "coordinates": [40.7128, -74.0060],
  "current": {
    "temperature": 22.5,
    "humidity": 65,
    "pressure": 1013.25,
    "wind_speed": 10.5,
    "wind_direction": 180,
    "uv_index": 5
  },
  "processed_metrics": {
    "heat_index": 24.2,
    "comfort_level": "comfortable",
    "air_quality_index": 85
  },
  "processing_engine": "Mojo v25.6+",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### Machine Learning Predictions

**GET** `/weather/predict/{location}`

Generate weather predictions using ML capabilities.

**Parameters:**
- `location` (path): City name
- `days` (query, optional): Prediction days (1-7, default: 3)

**Response:**
```json
{
  "location": "London",
  "predictions": [
    {
      "date": "2024-01-02",
      "temperature_range": [15, 22],
      "precipitation_probability": 0.3,
      "conditions": "partly_cloudy"
    }
  ],
  "confidence": 0.87,
  "model": "Enhanced Neural Network",
  "engine": "Mojo SIMD"
}
```

### Pattern Analysis

**GET** `/weather/patterns/{location}`

Analyze weather patterns and trends.

**Parameters:**
- `location` (path): City name
- `period` (query): Analysis period (week/month/year)

### Performance Benchmark

**GET** `/benchmark`

Run performance benchmark comparing Mojo vs Python processing.

## Error Handling

The API uses standard HTTP status codes:

- `200`: Success
- `400`: Bad Request
- `404`: Location not found
- `500`: Internal Server Error

Error responses include:
```json
{
  "error": "Location not found",
  "code": "LOCATION_NOT_FOUND",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## Rate Limiting

- Development: No limits
- Production: 1000 requests/hour per IP

## SDK Examples

### Python

```python
import requests

# Get weather data
response = requests.get("http://localhost:8000/weather/London")
weather = response.json()

# Get predictions
predictions = requests.get("http://localhost:8000/weather/predict/London?days=5")
forecast = predictions.json()
```

### cURL

```bash
# Basic weather data
curl "http://localhost:8000/weather/London"

# Weather predictions
curl "http://localhost:8000/weather/predict/London?days=3"

# Health check
curl "http://localhost:8000/health"
```

## WebSocket Support (Future)

Real-time weather updates will be available via WebSocket connections:

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/weather/London');
ws.onmessage = (event) => {
    const weatherUpdate = JSON.parse(event.data);
    console.log('Real-time update:', weatherUpdate);
};
```

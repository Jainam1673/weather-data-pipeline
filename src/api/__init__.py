"""
API Module - FastAPI Weather Server v2.0
========================================

High-performance weather API with machine learning capabilities,
comprehensive weather data processing, and real-time analytics.

Features:
- Real-time weather data processing
- Machine learning predictions
- Pattern analysis and forecasting
- Performance benchmarking
- Global weather coverage via Open-Meteo API
"""

from .server import app, fetch_enhanced_weather, get_current_weather, get_weather_forecast

__all__ = ["app", "fetch_enhanced_weather", "get_current_weather", "get_weather_forecast"]

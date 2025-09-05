"""
Data Module - Database Operations and Management
===============================================

Comprehensive data storage, retrieval, and management system for
weather data with advanced statistics and caching capabilities.

Features:
- Enhanced SQLite database operations
- Weather data storage and retrieval
- Statistics computation and caching
- Data aggregation and analysis
- Multi-table structure for complex queries
"""

from .database import WeatherDatabase

__all__ = ["WeatherDatabase"]

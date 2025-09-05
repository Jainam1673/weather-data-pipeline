"""
Enhanced Database module for weather data storage with advanced features
Supports the enhanced weather pipeline with Mojo integration
"""

import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WeatherDatabase:
    def __init__(self, db_path="weather_data.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with enhanced schema"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Enhanced weather data table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS weather_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL NOT NULL,
                    datetime TEXT NOT NULL,
                    latitude REAL NOT NULL,
                    longitude REAL NOT NULL,
                    location_name TEXT,
                    temperature REAL NOT NULL,
                    humidity REAL NOT NULL,
                    pressure REAL NOT NULL,
                    wind_speed REAL DEFAULT 0,
                    wind_direction REAL DEFAULT 0,
                    rainfall REAL DEFAULT 0,
                    cloudiness REAL DEFAULT 0,
                    visibility REAL DEFAULT 0,
                    uv_index REAL DEFAULT 0,
                    feels_like REAL DEFAULT 0,
                    dew_point REAL DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Statistics table for caching
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS weather_statistics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    calculation_date TEXT NOT NULL,
                    stats_json TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # System metrics table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS system_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    metric_name TEXT NOT NULL,
                    metric_value TEXT NOT NULL,
                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
            conn.close()
            logger.info("✅ Database initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Database initialization failed: {e}")
            raise

    def insert_weather_data(self, data_points):
        """Insert weather data points into database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for point in data_points:
                cursor.execute("""
                    INSERT INTO weather_data 
                    (timestamp, datetime, latitude, longitude, location_name, 
                     temperature, humidity, pressure, wind_speed, wind_direction, 
                     rainfall, cloudiness, visibility, uv_index, feels_like, dew_point)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    point.get('timestamp', 0),
                    datetime.fromtimestamp(point.get('timestamp', 0)).isoformat(),
                    point.get('latitude', 0),
                    point.get('longitude', 0),
                    point.get('location_name', 'Unknown'),
                    point.get('temperature', 0),
                    point.get('humidity', 0),
                    point.get('pressure', 0),
                    point.get('wind_speed', 0),
                    point.get('wind_direction', 0),
                    point.get('rainfall', 0),
                    point.get('cloudiness', 0),
                    point.get('visibility', 0),
                    point.get('uv_index', 0),
                    point.get('feels_like', 0),
                    point.get('dew_point', 0)
                ))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            logger.error(f"Error inserting weather data: {e}")
            return False

    def store_weather_data(self, latitude, longitude, weather_data):
        """Store enhanced weather data from API"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Store current weather if available
            current = weather_data.get("current_weather", {})
            if current:
                timestamp = datetime.now().timestamp()
                cursor.execute("""
                    INSERT INTO weather_data 
                    (timestamp, datetime, latitude, longitude, location_name,
                     temperature, humidity, pressure, wind_speed, rainfall)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    timestamp,
                    datetime.now().isoformat(),
                    latitude,
                    longitude,
                    weather_data.get("location", {}).get("name", "Unknown"),
                    current.get("temperature_2m", 0),
                    current.get("relative_humidity_2m", 0),
                    current.get("surface_pressure", 0),
                    current.get("wind_speed_10m", 0),
                    current.get("precipitation", 0)
                ))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            logger.error(f"Error storing weather data: {e}")
            return False

    def get_weather_data(self, limit=100, start_time=None, end_time=None):
        """Get weather data with optional filtering"""
        try:
            conn = sqlite3.connect(self.db_path)
            
            query = "SELECT * FROM weather_data"
            params = []
            
            if start_time or end_time:
                query += " WHERE"
                conditions = []
                
                if start_time:
                    conditions.append(" timestamp >= ?")
                    params.append(start_time)
                
                if end_time:
                    conditions.append(" timestamp <= ?")
                    params.append(end_time)
                
                query += " AND".join(conditions)
            
            query += " ORDER BY timestamp DESC LIMIT ?"
            params.append(limit)
            
            df = pd.read_sql_query(query, conn, params=params)
            conn.close()
            
            return df
            
        except Exception as e:
            logger.error(f"Error retrieving weather data: {e}")
            return pd.DataFrame()

    def get_statistics(self):
        """Get comprehensive database statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Total records
            cursor.execute("SELECT COUNT(*) FROM weather_data")
            total_records = cursor.fetchone()[0]
            
            # Latest record
            cursor.execute("SELECT MAX(datetime) FROM weather_data")
            latest_record = cursor.fetchone()[0]
            
            # Date range
            cursor.execute("SELECT MIN(datetime), MAX(datetime) FROM weather_data")
            date_range = cursor.fetchone()
            
            # Basic statistics
            if total_records > 0:
                df = pd.read_sql_query("""
                    SELECT temperature, humidity, pressure, wind_speed, rainfall 
                    FROM weather_data 
                    ORDER BY timestamp DESC 
                    LIMIT 1000
                """, conn)
                
                stats = {
                    "total_records": total_records,
                    "last_update": latest_record or "Never",
                    "date_range": {
                        "start": date_range[0] if date_range[0] else "N/A",
                        "end": date_range[1] if date_range[1] else "N/A"
                    },
                    "temperature": {
                        "avg": round(df['temperature'].mean(), 2) if not df.empty else 0,
                        "min": round(df['temperature'].min(), 2) if not df.empty else 0,
                        "max": round(df['temperature'].max(), 2) if not df.empty else 0
                    },
                    "humidity": {
                        "avg": round(df['humidity'].mean(), 2) if not df.empty else 0,
                        "min": round(df['humidity'].min(), 2) if not df.empty else 0,
                        "max": round(df['humidity'].max(), 2) if not df.empty else 0
                    },
                    "pressure": {
                        "avg": round(df['pressure'].mean(), 2) if not df.empty else 0,
                        "min": round(df['pressure'].min(), 2) if not df.empty else 0,
                        "max": round(df['pressure'].max(), 2) if not df.empty else 0
                    }
                }
            else:
                stats = {
                    "total_records": 0,
                    "last_update": "Never",
                    "date_range": {"start": "N/A", "end": "N/A"},
                    "temperature": {"avg": 0, "min": 0, "max": 0},
                    "humidity": {"avg": 0, "min": 0, "max": 0},
                    "pressure": {"avg": 0, "min": 0, "max": 0}
                }
            
            conn.close()
            return stats
            
        except Exception as e:
            logger.error(f"Error getting statistics: {e}")
            return {
                "total_records": 0,
                "last_update": "Error",
                "error": str(e)
            }

    def get_data_since(self, since_time):
        """Get data since a specific time"""
        try:
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql_query("""
                SELECT * FROM weather_data 
                WHERE datetime >= ? 
                ORDER BY timestamp DESC
            """, conn, params=[since_time])
            conn.close()
            
            return df.to_dict('records')
            
        except Exception as e:
            logger.error(f"Error getting recent data: {e}")
            return []

    def get_data_range(self, start_time, end_time):
        """Get data within a time range"""
        try:
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql_query("""
                SELECT * FROM weather_data 
                WHERE datetime BETWEEN ? AND ? 
                ORDER BY timestamp DESC
            """, conn, params=[start_time, end_time])
            conn.close()
            
            return df.to_dict('records')
            
        except Exception as e:
            logger.error(f"Error getting data range: {e}")
            return []

    def save_statistics(self, stats):
        """Save calculated statistics to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO weather_statistics (calculation_date, stats_json)
                VALUES (?, ?)
            """, (datetime.now().isoformat(), json.dumps(stats)))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            logger.error(f"Error saving statistics: {e}")
            return False

    def cleanup_old_data(self, cutoff_date):
        """Clean up old data before cutoff date"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                DELETE FROM weather_data 
                WHERE datetime < ?
            """, [cutoff_date])
            
            deleted_count = cursor.rowcount
            conn.commit()
            conn.close()
            
            return deleted_count
            
        except Exception as e:
            logger.error(f"Error cleaning up old data: {e}")
            return 0

    def get_data_summary(self):
        """Get a summary of all data in the database"""
        try:
            stats = self.get_statistics()
            return {
                "summary": "Weather data summary",
                "total_records": stats.get("total_records", 0),
                "last_update": stats.get("last_update", "Never"),
                "date_range": stats.get("date_range", {}),
                "statistics": stats
            }
            
        except Exception as e:
            logger.error(f"Error getting data summary: {e}")
            return {
                "summary": "Error retrieving summary",
                "error": str(e)
            }

    def store_batch_data(self, latitude, longitude, num_points):
        """Store batch weather data (legacy compatibility)"""
        try:
            # Generate sample data for testing
            import time
            data_points = []
            current_time = time.time()
            
            for i in range(num_points):
                point = {
                    'timestamp': current_time + (i * 3600),  # Hour intervals
                    'latitude': latitude,
                    'longitude': longitude,
                    'location_name': f"Location_{latitude}_{longitude}",
                    'temperature': 20.0 + (i % 15),
                    'humidity': 50.0 + (i % 40),
                    'pressure': 1013.25 + (i % 30),
                    'wind_speed': (i % 20),
                    'rainfall': (i % 5) * 0.5
                }
                data_points.append(point)
            
            return self.insert_weather_data(data_points)
            
        except Exception as e:
            logger.error(f"Error storing batch data: {e}")
            return False

    def get_aggregated_data(self, interval):
        """Get aggregated data by time interval"""
        try:
            conn = sqlite3.connect(self.db_path)
            
            if interval == 'hour':
                query = """
                    SELECT strftime('%Y-%m-%d %H:00:00', datetime) as time_group,
                           AVG(temperature) as avg_temperature,
                           AVG(humidity) as avg_humidity,
                           AVG(pressure) as avg_pressure,
                           COUNT(*) as count
                    FROM weather_data 
                    GROUP BY time_group 
                    ORDER BY time_group DESC 
                    LIMIT 24
                """
            elif interval == 'day':
                query = """
                    SELECT strftime('%Y-%m-%d', datetime) as time_group,
                           AVG(temperature) as avg_temperature,
                           AVG(humidity) as avg_humidity,
                           AVG(pressure) as avg_pressure,
                           COUNT(*) as count
                    FROM weather_data 
                    GROUP BY time_group 
                    ORDER BY time_group DESC 
                    LIMIT 30
                """
            else:
                query = """
                    SELECT datetime, temperature, humidity, pressure
                    FROM weather_data 
                    ORDER BY timestamp DESC 
                    LIMIT 100
                """
            
            df = pd.read_sql_query(query, conn)
            conn.close()
            
            return df
            
        except Exception as e:
            logger.error(f"Error getting aggregated data: {e}")
            return pd.DataFrame()

    def clear_old_data(self, days):
        """Clear data older than specified days"""
        try:
            cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
            return self.cleanup_old_data(cutoff_date)
            
        except Exception as e:
            logger.error(f"Error clearing old data: {e}")
            return 0

if __name__ == "__main__":
    # Test the database
    print("🧪 Testing Enhanced Weather Database...")
    
    db = WeatherDatabase()
    
    # Test statistics
    print("📊 Getting statistics...")
    stats = db.get_statistics()
    print(f"Total records: {stats.get('total_records', 0)}")
    
    # Test data insertion
    print("💾 Testing data insertion...")
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
    print(f"✅ Data insertion: {'Success' if result else 'Failed'}")
    
    # Test data retrieval
    print("📋 Testing data retrieval...")
    recent_data = db.get_data_since((datetime.now() - timedelta(hours=1)).isoformat())
    print(f"Recent records: {len(recent_data)}")
    
    print("✅ Database test completed!")

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
import pandas as pd

class WeatherDatabase:
    """SQLite database handler for weather data"""
    
    def __init__(self, db_path: str = "weather_data.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create weather data table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS weather_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL NOT NULL,
                    temperature REAL NOT NULL,
                    humidity REAL NOT NULL,
                    pressure REAL NOT NULL,
                    wind_speed REAL NOT NULL,
                    rainfall REAL NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create statistics table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS weather_statistics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    calculation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    stats_json TEXT NOT NULL,
                    analytics_json TEXT
                )
            """)
            
            # Create indexes for better performance
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_timestamp 
                ON weather_data(timestamp)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_created_at 
                ON weather_data(created_at)
            """)
            
            conn.commit()
    
    def insert_weather_data(self, data_points: List[Dict[str, Any]]) -> bool:
        """Insert weather data points into the database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                for point in data_points:
                    cursor.execute("""
                        INSERT INTO weather_data 
                        (timestamp, temperature, humidity, pressure, wind_speed, rainfall)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        point['timestamp'],
                        point['temperature'],
                        point['humidity'],
                        point['pressure'],
                        point['wind_speed'],
                        point['rainfall']
                    ))
                
                conn.commit()
                return True
        except Exception as e:
            print(f"Error inserting data: {e}")
            return False
    
    def get_weather_data(self, limit: Optional[int] = None, 
                        start_time: Optional[float] = None,
                        end_time: Optional[float] = None) -> pd.DataFrame:
        """Retrieve weather data from database"""
        query = """
            SELECT timestamp, temperature, humidity, pressure, wind_speed, rainfall, created_at
            FROM weather_data
        """
        params = []
        conditions = []
        
        if start_time is not None:
            conditions.append("timestamp >= ?")
            params.append(start_time)
        
        if end_time is not None:
            conditions.append("timestamp <= ?")
            params.append(end_time)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY timestamp DESC"
        
        if limit:
            query += f" LIMIT {limit}"
        
        with sqlite3.connect(self.db_path) as conn:
            df = pd.read_sql_query(query, conn, params=params)
            if not df.empty:
                df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')
            return df
    
    def get_latest_statistics(self) -> Optional[Dict[str, Any]]:
        """Get the most recent statistics calculation"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT stats_json, analytics_json, calculation_time
                FROM weather_statistics
                ORDER BY calculation_time DESC
                LIMIT 1
            """)
            result = cursor.fetchone()
            
            if result:
                stats = json.loads(result[0])
                analytics = json.loads(result[1]) if result[1] else None
                return {
                    'statistics': stats,
                    'analytics': analytics,
                    'calculation_time': result[2]
                }
        return None
    
    def save_statistics(self, stats: Dict[str, Any], analytics: Dict[str, Any] = None) -> bool:
        """Save calculated statistics to database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO weather_statistics (stats_json, analytics_json)
                    VALUES (?, ?)
                """, (
                    json.dumps(stats),
                    json.dumps(analytics) if analytics else None
                ))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error saving statistics: {e}")
            return False
    
    def get_data_summary(self) -> Dict[str, Any]:
        """Get a summary of the data in the database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Total record count
            cursor.execute("SELECT COUNT(*) FROM weather_data")
            total_records = cursor.fetchone()[0]
            
            # Date range
            cursor.execute("""
                SELECT MIN(timestamp), MAX(timestamp)
                FROM weather_data
            """)
            date_range = cursor.fetchone()
            
            # Latest record
            cursor.execute("""
                SELECT timestamp, temperature, humidity, pressure
                FROM weather_data
                ORDER BY timestamp DESC
                LIMIT 1
            """)
            latest_record = cursor.fetchone()
            
            summary = {
                'total_records': total_records,
                'date_range': {
                    'start': datetime.fromtimestamp(date_range[0]).isoformat() if date_range[0] else None,
                    'end': datetime.fromtimestamp(date_range[1]).isoformat() if date_range[1] else None
                },
                'latest_record': {
                    'timestamp': datetime.fromtimestamp(latest_record[0]).isoformat() if latest_record else None,
                    'temperature': latest_record[1] if latest_record else None,
                    'humidity': latest_record[2] if latest_record else None,
                    'pressure': latest_record[3] if latest_record else None
                } if latest_record else None
            }
            
            return summary
    
    def get_aggregated_data(self, interval: str = 'hour') -> pd.DataFrame:
        """Get aggregated weather data by time interval"""
        interval_mapping = {
            'hour': "strftime('%Y-%m-%d %H', datetime(timestamp, 'unixepoch'))",
            'day': "strftime('%Y-%m-%d', datetime(timestamp, 'unixepoch'))",
            'week': "strftime('%Y-%W', datetime(timestamp, 'unixepoch'))",
            'month': "strftime('%Y-%m', datetime(timestamp, 'unixepoch'))"
        }
        
        if interval not in interval_mapping:
            interval = 'hour'
        
        query = f"""
            SELECT 
                {interval_mapping[interval]} as time_period,
                AVG(temperature) as avg_temperature,
                MIN(temperature) as min_temperature,
                MAX(temperature) as max_temperature,
                AVG(humidity) as avg_humidity,
                AVG(pressure) as avg_pressure,
                AVG(wind_speed) as avg_wind_speed,
                SUM(rainfall) as total_rainfall,
                COUNT(*) as data_points
            FROM weather_data
            GROUP BY time_period
            ORDER BY time_period DESC
            LIMIT 100
        """
        
        with sqlite3.connect(self.db_path) as conn:
            return pd.read_sql_query(query, conn)
    
    def clear_old_data(self, days_to_keep: int = 30) -> int:
        """Clear data older than specified days"""
        cutoff_timestamp = datetime.now().timestamp() - (days_to_keep * 24 * 3600)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM weather_data 
                WHERE timestamp < ?
            """, (cutoff_timestamp,))
            deleted_count = cursor.rowcount
            conn.commit()
            
        return deleted_count

if __name__ == "__main__":
    # Test the database functionality
    db = WeatherDatabase()
    
    # Test data insertion
    test_data = [
        {
            'timestamp': datetime.now().timestamp(),
            'temperature': 25.5,
            'humidity': 65.0,
            'pressure': 1013.25,
            'wind_speed': 12.5,
            'rainfall': 0.0
        }
    ]
    
    success = db.insert_weather_data(test_data)
    print(f"Data insertion: {'Success' if success else 'Failed'}")
    
    # Test data retrieval
    df = db.get_weather_data(limit=5)
    print(f"Retrieved {len(df)} records")
    
    # Test summary
    summary = db.get_data_summary()
    print(f"Database summary: {summary}")

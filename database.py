"""
Database layer for the weather data pipeline
Handles SQLite operations for storing and retrieving weather data
"""

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

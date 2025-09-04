"""
Streamlit UI for the Weather Data Pipeline
Interactive dashboard for visualizing weather data processed by Mojo
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import json
from datetime import datetime, timedelta
import time

# Configure Streamlit page
st.set_page_config(
    page_title="🔥 Mojo Weather Data Pipeline",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_BASE_URL = "http://localhost:8000"

# Helper functions
@st.cache_data(ttl=30)  # Cache for 30 seconds
def fetch_api_data(endpoint):
    """Fetch data from API with error handling"""
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}", timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return None

def format_number(num):
    """Format numbers for display"""
    if num is None:
        return "N/A"
    if num >= 1000000:
        return f"{num/1000000:.1f}M"
    elif num >= 1000:
        return f"{num/1000:.1f}K"
    else:
        return str(round(num, 2))

# Main app
def main():
    # Header
    st.title("🌤️ Mojo Weather Data Pipeline")
    st.markdown("### Real-Time Weather Analytics with Open-Meteo API & Mojo Processing")
    
    # Show data source info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🔥 Mojo", "High-Performance", help="SIMD-optimized data processing")
    with col2:
        st.metric("📡 Open-Meteo", "Real Weather Data", help="Global weather API coverage")
    with col3:
        st.metric("⚡ Performance", "10k+ req/day", help="Free tier API limit")
    
    # Sidebar
    with st.sidebar:
        st.header("🛠️ Pipeline Controls")
        
        # Data Source Selection
        st.subheader("📡 Data Source")
        st.info("🌤️ **Open-Meteo API (Real Weather Data Only)**")
        st.caption("This application now exclusively uses real weather data from the Open-Meteo API")
        
        use_real_data = True
        
        # Location settings for real data
        st.markdown("**📍 Location Settings**")
        
        # Popular locations
        popular_locations = fetch_api_data("/locations/popular")
        if popular_locations:
            location_names = [loc["name"] for loc in popular_locations["popular_locations"]]
            selected_city = st.selectbox("Select City", ["Custom"] + location_names)
            
            if selected_city != "Custom":
                selected_location = next(loc for loc in popular_locations["popular_locations"] if loc["name"] == selected_city)
                latitude = selected_location["latitude"]
                longitude = selected_location["longitude"]
                st.info(f"📍 {selected_city}: {latitude:.4f}, {longitude:.4f}")
            else:
                col1, col2 = st.columns(2)
                with col1:
                    latitude = st.number_input("Latitude", value=51.5074, format="%.4f")
                with col2:
                    longitude = st.number_input("Longitude", value=-0.1278, format="%.4f")
        else:
            # Fallback if API fails
            col1, col2 = st.columns(2)
            with col1:
                latitude = st.number_input("Latitude", value=51.5074, format="%.4f")
            with col2:
                longitude = st.number_input("Longitude", value=-0.1278, format="%.4f")
        
        # Data Generation
        st.subheader("🔄 Data Generation")
        num_points = st.number_input("Hours of Data", min_value=1, max_value=168, value=24, step=1, help="Number of hours of weather data to fetch from Open-Meteo API")
        
        if st.button("🚀 Generate Data", type="primary"):
            with st.spinner("Generating data with Open-Meteo API..."):
                try:
                    payload = {
                        "num_points": num_points,
                        "use_real_data": True,
                        "latitude": latitude,
                        "longitude": longitude
                    }
                    
                    response = requests.post(
                        f"{API_BASE_URL}/generate-data",
                        json=payload
                    )
                    if response.status_code == 200:
                        result = response.json()
                        st.success(f"✅ Generated {num_points} points from Open-Meteo API!")
                        st.info(f"📍 Location: {latitude:.4f}, {longitude:.4f}")
                        st.balloons()
                        # Refresh the page data
                        st.rerun()
                    else:
                        st.error("Failed to generate data")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        st.divider()
        
        st.divider()
        
        # Refresh controls
        st.subheader("🔄 Data Refresh")
        auto_refresh = st.checkbox("Auto-refresh (30s)", value=False)
        
        if st.button("🔄 Refresh Now"):
            st.rerun()
        
        st.divider()
        
        # API Health
        st.subheader("🏥 System Health")
        health_data = fetch_api_data("/health")
        if health_data:
            if health_data.get("status") == "healthy":
                st.success("✅ System Healthy")
                st.metric("Data Records", format_number(health_data.get("data_records", 0)))
                if health_data.get("mojo_processor") == "available":
                    st.success("🔥 Mojo Processor Active")
            else:
                st.error("❌ System Issues")
        else:
            st.warning("⚠️ API Unavailable")
    
    # Auto-refresh logic
    if auto_refresh:
        time.sleep(30)
        st.rerun()
    
        # Store location settings in session state for main dashboard access
        st.session_state['latitude'] = latitude
        st.session_state['longitude'] = longitude
        st.session_state['use_real_data'] = True
        if 'selected_city' in locals() and selected_city != "Custom":
            st.session_state['location_name'] = selected_city
        else:
            st.session_state['location_name'] = f"Custom ({latitude:.4f}, {longitude:.4f})"    # Main content area
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Real-time Dashboard", 
        "📈 Analytics", 
        "📋 Data Explorer", 
        "📈 Statistics", 
        "⚙️ System Info"
    ])
    
    # Tab 1: Real-time Dashboard
    with tab1:
        st.header("🌤️ Live Weather Intelligence Center")
        
        # Get current location data for actionable content
        current_lat = st.session_state.get('latitude', 51.5074)
        current_lon = st.session_state.get('longitude', -0.1278)
        location_name = st.session_state.get('location_name', f"Location ({current_lat:.2f}, {current_lon:.2f})")
        
        # Weather Alert System
        st.subheader("⚠️ Weather Alerts & Actionable Insights")
        
        current_weather = fetch_api_data(f"/openmeteo/current/{current_lat}/{current_lon}")
        if current_weather and "current_weather" in current_weather:
            weather = current_weather["current_weather"]
            
            # Generate actionable alerts based on weather conditions
            alert_col1, alert_col2, alert_col3 = st.columns(3)
            
            temp = weather.get('temperature', 20)
            humidity = weather.get('humidity', 50)
            wind_speed = weather.get('wind_speed', 0)
            pressure = weather.get('surface_pressure', weather.get('pressure', 1013))
            precipitation = weather.get('precipitation', 0)
            
            with alert_col1:
                # Temperature alerts
                if temp > 30:
                    st.error("🥵 **HIGH HEAT ALERT**")
                    st.write("• Stay hydrated")
                    st.write("• Avoid outdoor activities 12-4pm")
                    st.write("• Use sunscreen SPF 30+")
                elif temp < 5:
                    st.warning("🥶 **COLD WEATHER ALERT**")
                    st.write("• Dress in layers")
                    st.write("• Protect exposed skin")
                    st.write("• Check on elderly neighbors")
                else:
                    st.success("🌡️ **COMFORTABLE TEMPERATURE**")
                    st.write("• Perfect for outdoor activities")
                    st.write("• Light clothing recommended")
            
            with alert_col2:
                # Wind & Pressure alerts
                if wind_speed > 15:
                    st.error("💨 **HIGH WIND WARNING**")
                    st.write("• Secure loose objects")
                    st.write("• Avoid high-profile vehicles")
                    st.write("• Driving caution advised")
                elif pressure < 1000:
                    st.warning("📉 **LOW PRESSURE SYSTEM**")
                    st.write("• Storm approaching")
                    st.write("• Indoor activities recommended")
                    st.write("• Monitor weather updates")
                else:
                    st.success("🌤️ **STABLE CONDITIONS**")
                    st.write("• Great for outdoor plans")
                    st.write("• Stable weather expected")
            
            with alert_col3:
                # Rain & Humidity alerts
                if precipitation > 5:
                    st.error("🌧️ **HEAVY RAIN ALERT**")
                    st.write("• Carry umbrella/raincoat")
                    st.write("• Allow extra travel time")
                    st.write("• Avoid flood-prone areas")
                elif humidity > 80:
                    st.warning("💧 **HIGH HUMIDITY**")
                    st.write("• Feels warmer than actual temp")
                    st.write("• Stay in air conditioning")
                    st.write("• Drink extra water")
                else:
                    st.success("☀️ **CLEAR CONDITIONS**")
                    st.write("• Perfect for outdoor activities")
                    st.write("• Great visibility")
        
        st.divider()
        
        # Current Weather Dashboard with Actions
        st.subheader(f"🌍 Current Conditions - {location_name}")
        
        # Quick action buttons
        action_col1, action_col2, action_col3, action_col4 = st.columns(4)
        
        with action_col1:
            if st.button("🔄 Refresh Data", type="primary"):
                st.rerun()
        
        with action_col2:
            if st.button("📊 24h Forecast"):
                st.info("💡 Use sidebar to generate 24-hour forecast data")
                
        with action_col3:
            if st.button("🗺️ Change Location"):
                st.info("💡 Use sidebar to select a different city")
                
        with action_col4:
            if st.button("📈 View Trends"):
                st.info("💡 Check the Analytics tab for detailed trends")
        
        if current_weather and "current_weather" in current_weather:
            weather = current_weather["current_weather"]
            
            # Enhanced metrics with color coding and recommendations
            metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
            
            with metric_col1:
                temp = weather.get('temperature', 'N/A')
                temp_color = "normal"
                if isinstance(temp, (int, float)):
                    if temp > 30:
                        temp_color = "inverse"
                    elif temp < 5:
                        temp_color = "off"
                
                st.metric(
                    "🌡️ Temperature",
                    f"{temp}°C" if temp != 'N/A' else 'N/A',
                    help="Current temperature with heat index consideration"
                )
                
                # Temperature comfort level
                if isinstance(temp, (int, float)):
                    if 18 <= temp <= 24:
                        st.success("Perfect comfort zone")
                    elif 25 <= temp <= 29:
                        st.warning("Getting warm")
                    elif temp >= 30:
                        st.error("Too hot")
                    elif 10 <= temp <= 17:
                        st.info("Cool but pleasant")
                    else:
                        st.error("Too cold")
            
            with metric_col2:
                humidity = weather.get('humidity', 'N/A')
                st.metric(
                    "💧 Humidity",
                    f"{humidity}%" if humidity != 'N/A' else 'N/A',
                    help="Relative humidity affects comfort level"
                )
                
                # Humidity comfort level
                if isinstance(humidity, (int, float)):
                    if 40 <= humidity <= 60:
                        st.success("Optimal humidity")
                    elif 61 <= humidity <= 75:
                        st.warning("Getting humid")
                    elif humidity > 75:
                        st.error("Very humid")
                    else:
                        st.info("Dry air")
            
            with metric_col3:
                wind = weather.get('wind_speed', 'N/A')
                st.metric(
                    "💨 Wind Speed",
                    f"{wind} m/s" if wind != 'N/A' else 'N/A',
                    help="Wind speed affects outdoor activities"
                )
                
                # Wind speed assessment
                if isinstance(wind, (int, float)):
                    if wind <= 5:
                        st.success("Light breeze")
                    elif 6 <= wind <= 12:
                        st.warning("Moderate wind")
                    elif 13 <= wind <= 20:
                        st.error("Strong wind")
                    else:
                        st.error("Very strong wind")
            
            with metric_col4:
                pressure = weather.get('surface_pressure', weather.get('pressure', 'N/A'))
                st.metric(
                    "📊 Pressure",
                    f"{pressure} hPa" if pressure != 'N/A' else 'N/A',
                    help="Atmospheric pressure indicates weather stability"
                )
                
                # Pressure trend
                if isinstance(pressure, (int, float)):
                    if pressure > 1020:
                        st.success("High pressure - stable")
                    elif 1010 <= pressure <= 1020:
                        st.info("Normal pressure")
                    else:
                        st.warning("Low pressure - unsettled")
        
        st.divider()
        
        # Actionable Recommendations Section
        st.subheader("🎯 Smart Recommendations")
        
        rec_col1, rec_col2 = st.columns(2)
        
        with rec_col1:
            st.markdown("### 👕 What to Wear")
            if current_weather and "current_weather" in current_weather:
                weather = current_weather["current_weather"]
                temp = weather.get('temperature', 20)
                wind = weather.get('wind_speed', 0)
                precipitation = weather.get('precipitation', 0)
                
                clothing_advice = []
                
                if temp >= 25:
                    clothing_advice.append("🩳 Light, breathable clothing")
                    clothing_advice.append("🧢 Hat for sun protection")
                    clothing_advice.append("🕶️ Sunglasses")
                elif 15 <= temp < 25:
                    clothing_advice.append("👕 Light long sleeves or t-shirt")
                    clothing_advice.append("👖 Light pants or jeans")
                elif 5 <= temp < 15:
                    clothing_advice.append("🧥 Jacket or sweater")
                    clothing_advice.append("👖 Long pants")
                    clothing_advice.append("🧦 Warm socks")
                else:
                    clothing_advice.append("🧥 Heavy coat")
                    clothing_advice.append("🧤 Gloves")
                    clothing_advice.append("🧣 Scarf")
                    clothing_advice.append("👢 Warm boots")
                
                if wind > 10:
                    clothing_advice.append("🧥 Wind-resistant outer layer")
                
                if precipitation > 0:
                    clothing_advice.append("☔ Umbrella or raincoat")
                    clothing_advice.append("👢 Waterproof shoes")
                
                for advice in clothing_advice:
                    st.write(f"• {advice}")
        
        with rec_col2:
            st.markdown("### 🏃‍♂️ Activity Suggestions")
            if current_weather and "current_weather" in current_weather:
                weather = current_weather["current_weather"]
                temp = weather.get('temperature', 20)
                wind = weather.get('wind_speed', 0)
                precipitation = weather.get('precipitation', 0)
                
                activities = []
                
                if precipitation > 5:
                    activities.extend([
                        "🏠 Indoor activities recommended",
                        "📚 Perfect for reading",
                        "🎬 Movie day",
                        "🍳 Cooking or baking"
                    ])
                elif 18 <= temp <= 28 and wind <= 10:
                    activities.extend([
                        "🚶‍♂️ Perfect for walking",
                        "🚴‍♂️ Great for cycling",
                        "🏃‍♂️ Good for jogging",
                        "🧺 Ideal for picnics"
                    ])
                elif temp > 30:
                    activities.extend([
                        "🏊‍♂️ Swimming recommended",
                        "🌳 Seek shaded areas",
                        "❄️ Air-conditioned activities",
                        "🌅 Early morning exercise"
                    ])
                elif temp < 10:
                    activities.extend([
                        "☕ Warm indoor activities",
                        "🏠 Cozy home activities",
                        "🛍️ Indoor shopping",
                        "🎭 Museums or theaters"
                    ])
                else:
                    activities.extend([
                        "🚶‍♂️ Nice for light activities",
                        "📷 Good for photography",
                        "🛍️ Shopping weather",
                        "☕ Café visits"
                    ])
                
                for activity in activities:
                    st.write(f"• {activity}")
        
        st.divider()
        
        # Historical Data Trends with Actionable Insights
        # Historical Data Trends with Actionable Insights
        st.subheader("📈 Weather Trends & Predictions")
        
        # Fetch latest data
        weather_data = fetch_api_data("/weather-data?limit=1000")
        
        if weather_data and weather_data.get("data"):
            df = pd.DataFrame(weather_data["data"])
            df['datetime'] = pd.to_datetime(df['datetime'])
            df = df.sort_values('datetime')
            
            # Trend Analysis Section
            trend_col1, trend_col2 = st.columns(2)
            
            with trend_col1:
                st.markdown("### 📊 Recent Trends (24h)")
                
                if len(df) >= 2:
                    latest = df.iloc[-1]
                    prev = df.iloc[-2]
                    
                    # Temperature trend
                    temp_change = latest['temperature'] - prev['temperature']
                    temp_trend = "↗️ Rising" if temp_change > 0.5 else "↘️ Falling" if temp_change < -0.5 else "➡️ Stable"
                    st.metric("🌡️ Temperature Trend", temp_trend, f"{temp_change:+.1f}°C")
                    
                    # Pressure trend
                    pressure_change = latest['pressure'] - prev['pressure']
                    pressure_trend = "↗️ Rising" if pressure_change > 2 else "↘️ Falling" if pressure_change < -2 else "➡️ Stable"
                    st.metric("📊 Pressure Trend", pressure_trend, f"{pressure_change:+.1f} hPa")
                    
                    # Weather prediction based on trends
                    if pressure_change < -5:
                        st.warning("⛈️ **Weather may deteriorate** - Falling pressure indicates incoming storms")
                    elif pressure_change > 5:
                        st.success("☀️ **Weather improving** - Rising pressure indicates clearing conditions")
                    else:
                        st.info("🌤️ **Stable weather** - Pressure stable, conditions likely to continue")
            
            with trend_col2:
                st.markdown("### 🎯 Optimization Insights")
                
                if len(df) >= 24:  # If we have at least 24 hours of data
                    # Find best times for activities
                    daily_df = df.tail(24)
                    
                    # Best time for outdoor activities (comfortable temp + low wind + no rain)
                    daily_df['comfort_score'] = (
                        (daily_df['temperature'].between(18, 25)).astype(int) * 3 +
                        (daily_df['wind_speed'] < 10).astype(int) * 2 +
                        (daily_df['rainfall'] == 0).astype(int) * 2
                    )
                    
                    best_hour = daily_df.loc[daily_df['comfort_score'].idxmax()]
                    best_time = best_hour['datetime'].strftime('%H:%M')
                    
                    st.success(f"🏃‍♂️ **Best activity time:** {best_time}")
                    st.write(f"• Temperature: {best_hour['temperature']:.1f}°C")
                    st.write(f"• Wind: {best_hour['wind_speed']:.1f} km/h")
                    st.write(f"• Rain: {best_hour['rainfall']:.1f} mm")
                    
                    # Energy efficiency recommendations
                    avg_temp = daily_df['temperature'].mean()
                    if avg_temp > 25:
                        st.info("❄️ **AC Tip:** Peak cooling needed. Use programmable thermostat.")
                    elif avg_temp < 15:
                        st.info("🔥 **Heating Tip:** Extra heating needed. Close unused rooms.")
                    else:
                        st.success("💡 **Energy Efficient:** Natural temperature - minimal HVAC needed.")
                
                else:
                    st.info("📊 Generate more data to see optimization insights")
            
            # Enhanced Visualization
            st.subheader("📈 Interactive Weather Analysis")
            
            # Time range selector
            time_range = st.selectbox(
                "Select time range for analysis:",
                ["Last 24 hours", "Last 3 days", "Last week", "All data"],
                index=0
            )
            
            # Filter data based on selection
            now = df['datetime'].max()
            if time_range == "Last 24 hours":
                filtered_df = df[df['datetime'] >= now - pd.Timedelta(hours=24)]
            elif time_range == "Last 3 days":
                filtered_df = df[df['datetime'] >= now - pd.Timedelta(days=3)]
            elif time_range == "Last week":
                filtered_df = df[df['datetime'] >= now - pd.Timedelta(days=7)]
            else:
                filtered_df = df
            
            if len(filtered_df) > 0:
                # Multi-tab visualization
                chart_tab1, chart_tab2, chart_tab3 = st.tabs(["🌡️ Temperature & Comfort", "🌧️ Precipitation & Wind", "📊 Pressure & Trends"])
                
                with chart_tab1:
                    # Temperature with comfort zones
                    fig_temp = go.Figure()
                    
                    # Add temperature line
                    fig_temp.add_trace(go.Scatter(
                        x=filtered_df['datetime'],
                        y=filtered_df['temperature'],
                        mode='lines+markers',
                        name='Temperature',
                        line=dict(color='red', width=3),
                        marker=dict(size=6)
                    ))
                    
                    # Add comfort zones
                    fig_temp.add_hrect(y0=18, y1=24, fillcolor="green", opacity=0.1, annotation_text="Comfort Zone")
                    fig_temp.add_hrect(y0=25, y1=30, fillcolor="yellow", opacity=0.1, annotation_text="Warm")
                    fig_temp.add_hrect(y0=30, y1=40, fillcolor="red", opacity=0.1, annotation_text="Hot")
                    
                    fig_temp.update_layout(
                        title="Temperature with Comfort Zones",
                        xaxis_title="Time",
                        yaxis_title="Temperature (°C)",
                        height=400
                    )
                    st.plotly_chart(fig_temp, use_container_width=True)
                    
                    # Humidity chart
                    fig_humidity = px.line(
                        filtered_df, x='datetime', y='humidity',
                        title='Humidity Levels Over Time',
                        labels={'humidity': 'Humidity (%)', 'datetime': 'Time'}
                    )
                    fig_humidity.add_hrect(y0=40, y1=60, fillcolor="green", opacity=0.1, annotation_text="Optimal")
                    st.plotly_chart(fig_humidity, use_container_width=True)
                
                with chart_tab2:
                    # Precipitation chart
                    fig_rain = px.bar(
                        filtered_df, x='datetime', y='rainfall',
                        title='Precipitation Over Time',
                        labels={'rainfall': 'Rainfall (mm)', 'datetime': 'Time'}
                    )
                    st.plotly_chart(fig_rain, use_container_width=True)
                    
                    # Wind speed with activity recommendations
                    fig_wind = go.Figure()
                    fig_wind.add_trace(go.Scatter(
                        x=filtered_df['datetime'],
                        y=filtered_df['wind_speed'],
                        mode='lines+markers',
                        name='Wind Speed',
                        line=dict(color='orange', width=3)
                    ))
                    
                    # Wind speed zones
                    fig_wind.add_hrect(y0=0, y1=5, fillcolor="green", opacity=0.1, annotation_text="Light Breeze")
                    fig_wind.add_hrect(y0=6, y1=12, fillcolor="yellow", opacity=0.1, annotation_text="Moderate")
                    fig_wind.add_hrect(y0=13, y1=25, fillcolor="red", opacity=0.1, annotation_text="Strong Wind")
                    
                    fig_wind.update_layout(
                        title="Wind Speed with Activity Zones",
                        xaxis_title="Time",
                        yaxis_title="Wind Speed (m/s)",
                        height=400
                    )
                    st.plotly_chart(fig_wind, use_container_width=True)
                
                with chart_tab3:
                    # Pressure trend with weather prediction
                    fig_pressure = go.Figure()
                    fig_pressure.add_trace(go.Scatter(
                        x=filtered_df['datetime'],
                        y=filtered_df['pressure'],
                        mode='lines+markers',
                        name='Pressure',
                        line=dict(color='purple', width=3)
                    ))
                    
                    # Add trend line
                    if len(filtered_df) > 2:
                        # Simple linear trend calculation
                        x_vals = range(len(filtered_df))
                        y_vals = filtered_df['pressure'].values
                        
                        # Calculate slope using simple linear regression
                        n = len(x_vals)
                        sum_x = sum(x_vals)
                        sum_y = sum(y_vals)
                        sum_xy = sum(x * y for x, y in zip(x_vals, y_vals))
                        sum_x2 = sum(x * x for x in x_vals)
                        
                        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
                        intercept = (sum_y - slope * sum_x) / n
                        
                        trend_line = [slope * x + intercept for x in x_vals]
                        fig_pressure.add_trace(go.Scatter(
                            x=filtered_df['datetime'],
                            y=trend_line,
                            mode='lines',
                            name='Trend',
                            line=dict(color='red', width=2, dash='dash')
                        ))
                        
                        # Weather prediction based on pressure trend
                        if slope > 0.1:
                            trend_text = "⬆️ Rising pressure - Weather improving"
                        elif slope < -0.1:
                            trend_text = "⬇️ Falling pressure - Weather may deteriorate"
                        else:
                            trend_text = "➡️ Stable pressure - Current conditions continue"
                        
                        st.info(f"**Pressure Trend Analysis:** {trend_text}")
                    
                    fig_pressure.update_layout(
                        title="Atmospheric Pressure Trend",
                        xaxis_title="Time",
                        yaxis_title="Pressure (hPa)",
                        height=400
                    )
                    st.plotly_chart(fig_pressure, use_container_width=True)
            
            # Data Summary with Actionable Statistics
            st.subheader("📊 Data Insights Summary")
            
            summary_col1, summary_col2, summary_col3 = st.columns(3)
            
            with summary_col1:
                st.markdown("### 🌡️ Temperature Analysis")
                temp_stats = filtered_df['temperature'].describe()
                st.metric("Average", f"{temp_stats['mean']:.1f}°C")
                st.metric("Range", f"{temp_stats['max'] - temp_stats['min']:.1f}°C")
                
                # Comfort analysis
                comfortable_hours = len(filtered_df[filtered_df['temperature'].between(18, 25)])
                total_hours = len(filtered_df)
                comfort_percentage = (comfortable_hours / total_hours) * 100 if total_hours > 0 else 0
                st.metric("Comfort Time", f"{comfort_percentage:.0f}%")
            
            with summary_col2:
                st.markdown("### 🌧️ Precipitation Analysis")
                rain_stats = filtered_df['rainfall'].describe()
                total_rainfall = filtered_df['rainfall'].sum()
                st.metric("Total Rainfall", f"{total_rainfall:.1f} mm")
                
                rainy_hours = len(filtered_df[filtered_df['rainfall'] > 0])
                rain_percentage = (rainy_hours / total_hours) * 100 if total_hours > 0 else 0
                st.metric("Rainy Time", f"{rain_percentage:.0f}%")
                
                if rain_stats['max'] > 5:
                    st.warning("Heavy rain periods detected")
                elif total_rainfall == 0:
                    st.success("Dry period")
                else:
                    st.info("Light precipitation")
            
            with summary_col3:
                st.markdown("### 💨 Wind Analysis")
                wind_stats = filtered_df['wind_speed'].describe()
                st.metric("Average Wind", f"{wind_stats['mean']:.1f} m/s")
                st.metric("Max Gust", f"{wind_stats['max']:.1f} m/s")
                
                calm_hours = len(filtered_df[filtered_df['wind_speed'] < 5])
                calm_percentage = (calm_hours / total_hours) * 100 if total_hours > 0 else 0
                st.metric("Calm Conditions", f"{calm_percentage:.0f}%")
        
        else:
            st.warning("📭 No historical data available.")
            st.info("💡 **Action Required:** Use the sidebar to generate weather data first!")
            
            # Show what they can do
            st.markdown("""
            ### 🚀 Get Started:
            1. **Select a location** in the sidebar
            2. **Generate weather data** (24+ hours recommended)
            3. **Return here** for detailed insights and recommendations
            
            ### 📈 What you'll get:
            • **Smart weather alerts** based on current conditions
            • **Activity recommendations** for optimal timing
            • **Energy efficiency tips** for your location
            • **Trend analysis** to predict weather changes
            • **Interactive charts** with comfort zones
            """)
            
            if st.button("🔄 Check for Data Again", type="primary"):
                st.rerun()
    
    # Tab 2: Analytics
    with tab2:
        st.header("🎯 Smart Weather Analytics & Planning")
        
        # Get weather data for analysis
        weather_data = fetch_api_data("/weather-data?limit=1000")
        analytics_data = fetch_api_data("/analytics")
        
        if weather_data and weather_data.get("data"):
            df = pd.DataFrame(weather_data["data"])
            df['datetime'] = pd.to_datetime(df['datetime'])
            df = df.sort_values('datetime')
            
            # Business Intelligence Dashboard
            st.subheader("📊 Business Intelligence Overview")
            
            # Key Performance Indicators
            kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
            
            with kpi_col1:
                comfort_hours = len(df[df['temperature'].between(18, 25) & (df['wind_speed'] < 10) & (df['rainfall'] == 0)])
                total_hours = len(df)
                comfort_score = (comfort_hours / total_hours) * 100 if total_hours > 0 else 0
                st.metric("🎯 Comfort Score", f"{comfort_score:.0f}%", help="Percentage of time with ideal conditions")
                
                if comfort_score >= 70:
                    st.success("Excellent outdoor conditions")
                elif comfort_score >= 50:
                    st.warning("Moderate outdoor conditions")
                else:
                    st.error("Poor outdoor conditions")
            
            with kpi_col2:
                energy_efficiency = 100 - abs(df['temperature'].mean() - 20) * 5  # Optimal temp is 20°C
                energy_efficiency = max(0, min(100, energy_efficiency))
                st.metric("⚡ Energy Efficiency", f"{energy_efficiency:.0f}%", help="Energy efficiency based on temperature")
                
                if energy_efficiency >= 80:
                    st.success("Low energy costs")
                elif energy_efficiency >= 60:
                    st.warning("Moderate energy costs")
                else:
                    st.error("High energy costs")
            
            with kpi_col3:
                storm_risk = len(df[(df['pressure'] < 1000) | (df['wind_speed'] > 15)]) / total_hours * 100
                st.metric("🌪️ Storm Risk", f"{storm_risk:.0f}%", help="Percentage of time with storm indicators")
                
                if storm_risk < 10:
                    st.success("Low storm risk")
                elif storm_risk < 25:
                    st.warning("Moderate storm risk")
                else:
                    st.error("High storm risk")
            
            with kpi_col4:
                activity_index = len(df[df['temperature'].between(15, 28) & (df['rainfall'] == 0)]) / total_hours * 100
                st.metric("🏃‍♂️ Activity Index", f"{activity_index:.0f}%", help="Percentage of time suitable for activities")
                
                if activity_index >= 70:
                    st.success("Great for activities")
                elif activity_index >= 50:
                    st.warning("Limited activity windows")
                else:
                    st.error("Poor activity conditions")
            
            st.divider()
            
            # Actionable Insights Section
            st.subheader("💡 Actionable Insights & Recommendations")
            
            insight_tab1, insight_tab2, insight_tab3, insight_tab4 = st.tabs([
                "🏢 Business Planning", "🏃‍♂️ Activity Optimization", "💰 Cost Management", "⚠️ Risk Assessment"
            ])
            
            with insight_tab1:
                st.markdown("### 🏢 Business & Event Planning Insights")
                
                # Best days for outdoor events
                if len(df) >= 24:
                    df['day'] = df['datetime'].dt.date
                    daily_scores = df.groupby('day').apply(
                        lambda x: len(x[x['temperature'].between(18, 25) & (x['rainfall'] == 0) & (x['wind_speed'] < 10)]) / len(x) * 100
                    ).reset_index(name='score')
                    
                    best_day = daily_scores.loc[daily_scores['score'].idxmax()]
                    worst_day = daily_scores.loc[daily_scores['score'].idxmin()]
                    
                    rec_col1, rec_col2 = st.columns(2)
                    
                    with rec_col1:
                        st.success(f"📅 **Best Event Day:** {best_day['day']}")
                        st.write(f"• Comfort Score: {best_day['score']:.0f}%")
                        st.write("• **Recommended for:**")
                        st.write("  - Outdoor events & conferences")
                        st.write("  - Team building activities")
                        st.write("  - Product launches")
                        st.write("  - Customer events")
                    
                    with rec_col2:
                        st.error(f"📅 **Avoid Events On:** {worst_day['day']}")
                        st.write(f"• Comfort Score: {worst_day['score']:.0f}%")
                        st.write("• **Better for:**")
                        st.write("  - Indoor workshops")
                        st.write("  - Virtual meetings")
                        st.write("  - Office-based activities")
                        st.write("  - Planning sessions")
                
                # Seasonal business recommendations
                avg_temp = df['temperature'].mean()
                avg_rain = df['rainfall'].mean()
                
                st.markdown("### 🎯 Business Opportunity Analysis")
                
                opportunities = []
                if avg_temp > 25:
                    opportunities.extend([
                        "🏖️ **High demand for:** Cooling services, ice cream, beverages",
                        "❄️ **HVAC services:** Peak demand for air conditioning",
                        "🏊‍♂️ **Recreation:** Swimming pools, water sports equipment",
                        "🧴 **Health products:** Sunscreen, hydration products"
                    ])
                elif avg_temp < 10:
                    opportunities.extend([
                        "☕ **High demand for:** Hot beverages, warming foods",
                        "🔥 **Heating services:** Furnace maintenance, insulation",
                        "🧥 **Clothing:** Winter wear, indoor entertainment",
                        "🏠 **Home services:** Weatherproofing, indoor activities"
                    ])
                else:
                    opportunities.extend([
                        "🚶‍♂️ **Outdoor services:** Tourism, outdoor dining",
                        "🌱 **Seasonal activities:** Gardening, outdoor sports",
                        "🎯 **Events:** Optimal conditions for gatherings",
                        "🚗 **Transportation:** Good conditions for deliveries"
                    ])
                
                if avg_rain > 2:
                    opportunities.append("☔ **Rain-related:** Umbrella sales, indoor entertainment")
                
                for opp in opportunities:
                    st.write(f"• {opp}")
            
            with insight_tab2:
                st.markdown("### 🏃‍♂️ Personal & Fitness Optimization")
                
                if len(df) >= 24:
                    # Hour-by-hour analysis
                    df['hour'] = df['datetime'].dt.hour
                    hourly_comfort = df.groupby('hour').apply(
                        lambda x: len(x[x['temperature'].between(18, 25) & (x['rainfall'] == 0) & (x['wind_speed'] < 8)]) / len(x) * 100
                    )
                    
                    best_hours = hourly_comfort.nlargest(3)
                    worst_hours = hourly_comfort.nsmallest(3)
                    
                    opt_col1, opt_col2 = st.columns(2)
                    
                    with opt_col1:
                        st.success("🌟 **Optimal Activity Windows**")
                        for hour, score in best_hours.items():
                            st.write(f"• **{hour:02d}:00-{(hour+1):02d}:00** - {score:.0f}% comfort")
                        
                        st.markdown("**Perfect for:**")
                        st.write("🏃‍♂️ Running & jogging")
                        st.write("🚴‍♂️ Cycling & outdoor sports")
                        st.write("🧘‍♀️ Yoga & meditation")
                        st.write("🚶‍♂️ Walking & hiking")
                    
                    with opt_col2:
                        st.warning("⚠️ **Avoid These Hours**")
                        for hour, score in worst_hours.items():
                            st.write(f"• **{hour:02d}:00-{(hour+1):02d}:00** - {score:.0f}% comfort")
                        
                        st.markdown("**Better for:**")
                        st.write("🏠 Indoor workouts")
                        st.write("🏊‍♂️ Swimming (if available)")
                        st.write("📚 Planning & preparation")
                        st.write("☕ Rest & recovery")
                
                # Workout intensity recommendations
                st.markdown("### 💪 Workout Intensity Guide")
                
                current_temp = df.iloc[-1]['temperature'] if len(df) > 0 else 20
                current_humidity = df.iloc[-1]['humidity'] if len(df) > 0 else 50
                
                heat_index = current_temp + (current_humidity - 40) * 0.1
                
                if heat_index < 20:
                    intensity_rec = "🔥 **High Intensity** - Cold weather allows for intense workouts"
                    intensity_color = "success"
                elif heat_index < 25:
                    intensity_rec = "⚖️ **Moderate to High** - Ideal conditions for most activities"
                    intensity_color = "success"
                elif heat_index < 30:
                    intensity_rec = "⚖️ **Moderate** - Reduce intensity, stay hydrated"
                    intensity_color = "warning"
                else:
                    intensity_rec = "🔽 **Low Intensity** - Focus on hydration and cooling"
                    intensity_color = "error"
                
                getattr(st, intensity_color)(intensity_rec)
            
            with insight_tab3:
                st.markdown("### 💰 Energy & Cost Management")
                
                # Energy consumption predictions
                heating_days = len(df[df['temperature'] < 15])
                cooling_days = len(df[df['temperature'] > 25])
                neutral_days = total_hours - heating_days - cooling_days
                
                cost_col1, cost_col2 = st.columns(2)
                
                with cost_col1:
                    st.markdown("#### 🔥 Heating Analysis")
                    heating_percentage = (heating_days / total_hours) * 100
                    st.metric("Heating Required", f"{heating_percentage:.0f}% of time")
                    
                    if heating_percentage > 50:
                        st.error("High heating costs expected")
                        st.write("💡 **Cost-saving tips:**")
                        st.write("• Use programmable thermostats")
                        st.write("• Seal windows and doors")
                        st.write("• Layer clothing indoors")
                        st.write("• Use space heaters for occupied rooms")
                    elif heating_percentage > 25:
                        st.warning("Moderate heating costs")
                        st.write("💡 **Optimization tips:**")
                        st.write("• Set thermostat to 18-20°C")
                        st.write("• Close unused rooms")
                        st.write("• Use ceiling fans to circulate air")
                    else:
                        st.success("Low heating requirements")
                
                with cost_col2:
                    st.markdown("#### ❄️ Cooling Analysis")
                    cooling_percentage = (cooling_days / total_hours) * 100
                    st.metric("Cooling Required", f"{cooling_percentage:.0f}% of time")
                    
                    if cooling_percentage > 50:
                        st.error("High cooling costs expected")
                        st.write("💡 **Cost-saving tips:**")
                        st.write("• Use AC during peak rate hours only")
                        st.write("• Install window films")
                        st.write("• Use fans to feel 2-3°C cooler")
                        st.write("• Close blinds during day")
                    elif cooling_percentage > 25:
                        st.warning("Moderate cooling costs")
                        st.write("💡 **Optimization tips:**")
                        st.write("• Set AC to 24-26°C")
                        st.write("• Use natural ventilation at night")
                        st.write("• Maintain AC units regularly")
                    else:
                        st.success("Low cooling requirements")
                
                # Monthly cost estimates
                st.markdown("#### 📊 Estimated Monthly Impact")
                
                if heating_percentage > cooling_percentage:
                    primary_cost = "heating"
                    primary_percentage = heating_percentage
                    primary_savings = [
                        "Lower thermostat by 1°C → Save 10-15%",
                        "Use smart thermostats → Save 10-20%",
                        "Improve insulation → Save 15-30%"
                    ]
                else:
                    primary_cost = "cooling"
                    primary_percentage = cooling_percentage
                    primary_savings = [
                        "Raise thermostat by 1°C → Save 10-15%",
                        "Use programmable AC → Save 10-20%",
                        "Improve insulation → Save 15-30%"
                    ]
                
                st.info(f"🎯 **Primary cost driver:** {primary_cost.title()} ({primary_percentage:.0f}% of time)")
                st.write("💰 **Potential savings:**")
                for saving in primary_savings:
                    st.write(f"• {saving}")
            
            with insight_tab4:
                st.markdown("### ⚠️ Risk Assessment & Preparedness")
                
                # Weather risk analysis
                risk_analysis = {
                    "extreme_heat": len(df[df['temperature'] > 35]) / total_hours * 100,
                    "extreme_cold": len(df[df['temperature'] < 0]) / total_hours * 100,
                    "high_wind": len(df[df['wind_speed'] > 20]) / total_hours * 100,
                    "heavy_rain": len(df[df['rainfall'] > 10]) / total_hours * 100,
                    "low_pressure": len(df[df['pressure'] < 990]) / total_hours * 100
                }
                
                risk_col1, risk_col2 = st.columns(2)
                
                with risk_col1:
                    st.markdown("#### 🌡️ Temperature Risks")
                    
                    if risk_analysis["extreme_heat"] > 10:
                        st.error(f"🔥 **High Heat Risk:** {risk_analysis['extreme_heat']:.1f}% of time")
                        st.write("🚨 **Actions required:**")
                        st.write("• Stock up on cooling supplies")
                        st.write("• Check AC systems")
                        st.write("• Plan for higher energy bills")
                        st.write("• Prepare heat emergency plan")
                    elif risk_analysis["extreme_heat"] > 0:
                        st.warning(f"🌡️ **Moderate Heat Risk:** {risk_analysis['extreme_heat']:.1f}% of time")
                        st.write("⚠️ **Precautions:**")
                        st.write("• Monitor elderly and pets")
                        st.write("• Stay hydrated")
                        st.write("• Avoid peak sun hours")
                    else:
                        st.success("✅ **Low Heat Risk**")
                    
                    if risk_analysis["extreme_cold"] > 10:
                        st.error(f"🥶 **High Cold Risk:** {risk_analysis['extreme_cold']:.1f}% of time")
                        st.write("🚨 **Actions required:**")
                        st.write("• Winterize pipes")
                        st.write("• Stock emergency supplies")
                        st.write("• Check heating systems")
                        st.write("• Prepare winter emergency kit")
                    elif risk_analysis["extreme_cold"] > 0:
                        st.warning(f"❄️ **Moderate Cold Risk:** {risk_analysis['extreme_cold']:.1f}% of time")
                        st.write("⚠️ **Precautions:**")
                        st.write("• Protect pipes from freezing")
                        st.write("• Have backup heating")
                        st.write("• Check car winterization")
                    else:
                        st.success("✅ **Low Cold Risk**")
                
                with risk_col2:
                    st.markdown("#### 🌪️ Storm Risks")
                    
                    total_storm_risk = risk_analysis["high_wind"] + risk_analysis["heavy_rain"] + risk_analysis["low_pressure"]
                    
                    if total_storm_risk > 20:
                        st.error(f"⛈️ **High Storm Risk:** {total_storm_risk:.1f}% combined indicators")
                        st.write("🚨 **Emergency preparedness:**")
                        st.write("• Emergency supply kit (3-7 days)")
                        st.write("• Battery-powered radio")
                        st.write("• Flashlights and batteries")
                        st.write("• First aid kit")
                        st.write("• Important documents secured")
                    elif total_storm_risk > 10:
                        st.warning(f"🌦️ **Moderate Storm Risk:** {total_storm_risk:.1f}% indicators")
                        st.write("⚠️ **Basic preparedness:**")
                        st.write("• Check emergency supplies")
                        st.write("• Secure outdoor items")
                        st.write("• Monitor weather alerts")
                        st.write("• Have backup communication")
                    else:
                        st.success("✅ **Low Storm Risk**")
                    
                    # Risk timeline
                    if len(df) > 24:
                        st.markdown("#### 📅 Risk Timeline")
                        
                        # Create risk score by day
                        df['risk_score'] = (
                            (df['temperature'] > 35).astype(int) * 3 +
                            (df['temperature'] < 0).astype(int) * 3 +
                            (df['wind_speed'] > 20).astype(int) * 2 +
                            (df['rainfall'] > 10).astype(int) * 2 +
                            (df['pressure'] < 990).astype(int) * 1
                        )
                        
                        daily_risk = df.groupby(df['datetime'].dt.date)['risk_score'].mean().reset_index()
                        daily_risk.columns = ['date', 'risk_score']
                        
                        highest_risk_day = daily_risk.loc[daily_risk['risk_score'].idxmax()]
                        
                        if highest_risk_day['risk_score'] > 2:
                            st.warning(f"📅 **Highest Risk Day:** {highest_risk_day['date']}")
                            st.write(f"Risk Score: {highest_risk_day['risk_score']:.1f}/10")
                        else:
                            st.success("📅 **All days show low risk scores**")
            
            st.divider()
            
            # Data-driven recommendations
            st.subheader("🎯 Personalized Action Plan")
            
            action_col1, action_col2 = st.columns(2)
            
            with action_col1:
                st.markdown("### 📋 This Week's Priorities")
                
                priorities = []
                
                # Priority based on conditions
                if risk_analysis["extreme_heat"] > 5:
                    priorities.append("🔥 **HIGH:** Prepare cooling strategies")
                if risk_analysis["extreme_cold"] > 5:
                    priorities.append("❄️ **HIGH:** Winterization checks")
                if risk_analysis["high_wind"] > 10:
                    priorities.append("💨 **MEDIUM:** Secure outdoor items")
                if risk_analysis["heavy_rain"] > 15:
                    priorities.append("🌧️ **MEDIUM:** Check drainage systems")
                
                if comfort_score < 50:
                    priorities.append("🏠 **LOW:** Focus on indoor activities")
                
                if energy_efficiency < 70:
                    priorities.append("⚡ **LOW:** Optimize energy usage")
                
                if not priorities:
                    priorities.append("✅ **Maintenance:** Regular system checks")
                    priorities.append("📊 **Planning:** Review upcoming forecasts")
                
                for priority in priorities:
                    st.write(f"• {priority}")
            
            with action_col2:
                st.markdown("### 📞 Emergency Contacts & Resources")
                
                st.write("**Weather Services:**")
                st.write("• Local Weather Service: Check local emergency management")
                st.write("• Storm Warnings: Monitor local alerts")
                
                st.write("**Utilities:**")
                st.write("• Power Company: Report outages")
                st.write("• Gas Company: Report leaks")
                st.write("• Water Department: Report issues")
                
                st.write("**Emergency Services:**")
                st.write("• Emergency: 911 (US) / 999 (UK) / 112 (EU)")
                st.write("• Non-Emergency: Check local numbers")
                
                if st.button("📱 Create Emergency Plan", key="emergency_plan"):
                    st.info("💡 Consider creating a family emergency plan with evacuation routes, meeting points, and emergency supplies.")
        
        else:
            st.warning("📊 Advanced analytics require historical data.")
            st.info("💡 **Generate weather data first** to unlock powerful business intelligence!")
            
            # Show what they'll get
            st.markdown("""
            ### 🎯 What You'll Get With Data:
            
            **🏢 Business Intelligence:**
            • Optimal event planning dates
            • Seasonal business opportunities
            • Customer behavior predictions
            
            **💪 Personal Optimization:**
            • Best workout times
            • Activity recommendations
            • Health and comfort insights
            
            **💰 Cost Management:**
            • Energy usage predictions
            • Heating/cooling optimization
            • Monthly cost estimates
            
            **⚠️ Risk Management:**
            • Weather risk assessment
            • Emergency preparedness
            • Safety recommendations
            """)
            
            if st.button("🚀 Generate Data for Analytics", type="primary", key="gen_analytics_data"):
                st.info("👈 Use the sidebar controls to generate weather data first!")
    
    # Tab 3: Data Explorer
    with tab3:
        st.header("📋 Data Explorer")
        
        # Data filters
        col1, col2, col3 = st.columns(3)
        with col1:
            limit = st.selectbox("Records to show", [100, 500, 1000, 5000], index=1)
        with col2:
            start_date = st.date_input("Start Date", value=datetime.now() - timedelta(days=7))
        with col3:
            end_date = st.date_input("End Date", value=datetime.now())
        
        # Fetch filtered data
        start_datetime = datetime.combine(start_date, datetime.min.time()).isoformat()
        end_datetime = datetime.combine(end_date, datetime.max.time()).isoformat()
        
        weather_data = fetch_api_data(f"/weather-data?limit={limit}&start_time={start_datetime}&end_time={end_datetime}")
        
        if weather_data and weather_data.get("data"):
            df = pd.DataFrame(weather_data["data"])
            df['datetime'] = pd.to_datetime(df['datetime'])
            
            st.subheader(f"📊 Data Summary ({len(df)} records)")
            
            # Display summary statistics
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Numerical Summary:**")
                st.dataframe(df[['temperature', 'humidity', 'pressure', 'wind_speed', 'rainfall']].describe())
            
            with col2:
                st.write("**Data Quality:**")
                quality_metrics = {
                    "Total Records": len(df),
                    "Missing Values": df.isnull().sum().sum(),
                    "Date Range": f"{df['datetime'].min().strftime('%Y-%m-%d')} to {df['datetime'].max().strftime('%Y-%m-%d')}",
                    "Data Completeness": f"{((len(df) - df.isnull().sum().sum()) / (len(df) * len(df.columns))) * 100:.1f}%"
                }
                for metric, value in quality_metrics.items():
                    st.write(f"**{metric}:** {value}")
            
            # Raw data table
            st.subheader("📄 Raw Data")
            st.dataframe(
                df.sort_values('datetime', ascending=False),
                use_container_width=True,
                height=400
            )
            
            # Download button
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"weather_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        else:
            st.warning("📭 No data available for the selected filters.")
    
    # Tab 4: Statistics
    with tab4:
        st.header("📈 Statistical Analysis")
        
        stats_data = fetch_api_data("/statistics")
        
        if stats_data and stats_data.get("statistics"):
            stats = stats_data["statistics"]
            
            # Create statistical visualizations
            metrics = ['temperature', 'humidity', 'pressure', 'wind_speed']
            
            for i, metric in enumerate(metrics):
                if metric in stats:
                    st.subheader(f"📊 {metric.replace('_', ' ').title()} Statistics")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    metric_stats = stats[metric]
                    
                    with col1:
                        st.metric("Mean", f"{metric_stats.get('mean', 'N/A')}")
                    with col2:
                        st.metric("Min", f"{metric_stats.get('min', 'N/A')}")
                    with col3:
                        st.metric("Max", f"{metric_stats.get('max', 'N/A')}")
                    with col4:
                        st.metric("Std Dev", f"{metric_stats.get('std', 'N/A')}")
                    
                    # Create distribution visualization
                    if "mean" in metric_stats and "std" in metric_stats:
                        import numpy as np
                        x = np.linspace(
                            metric_stats["mean"] - 3 * metric_stats["std"],
                            metric_stats["mean"] + 3 * metric_stats["std"],
                            100
                        )
                        y = (1 / (metric_stats["std"] * np.sqrt(2 * np.pi))) * np.exp(
                            -0.5 * ((x - metric_stats["mean"]) / metric_stats["std"]) ** 2
                        )
                        
                        fig = go.Figure()
                        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Normal Distribution'))
                        fig.add_vline(x=metric_stats["mean"], line_dash="dash", 
                                     annotation_text="Mean", line_color="red")
                        fig.update_layout(
                            title=f"{metric.replace('_', ' ').title()} Distribution",
                            xaxis_title=metric.replace('_', ' ').title(),
                            yaxis_title="Probability Density"
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                    if i < len(metrics) - 1:
                        st.divider()
            
            # Rainfall special case
            if "rainfall" in stats:
                st.subheader("🌧️ Rainfall Statistics")
                rainfall_stats = stats["rainfall"]
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Rainfall", f"{rainfall_stats.get('total', 'N/A')} mm")
                with col2:
                    st.metric("Average per Reading", f"{rainfall_stats.get('mean', 'N/A')} mm")
                with col3:
                    st.metric("Maximum", f"{rainfall_stats.get('max', 'N/A')} mm")
        else:
            st.warning("📊 Statistics not available. Generate some data first!")
    
    # Tab 5: System Info
    with tab5:
        st.header("⚙️ System Information")
        
        summary_data = fetch_api_data("/summary")
        
        if summary_data:
            # System metrics
            st.subheader("🖥️ Pipeline Status")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**System Components:**")
                st.write("🔥 Mojo Data Processor: ✅ Active")
                st.write("🐍 Python API Backend: ✅ Active")
                st.write("🗄️ SQLite Database: ✅ Connected")
                st.write("📊 Streamlit UI: ✅ Running")
            
            with col2:
                st.write("**Data Information:**")
                st.write(f"**Total Records:** {format_number(summary_data.get('total_records', 0))}")
                
                date_range = summary_data.get('date_range', {})
                if date_range.get('start'):
                    st.write(f"**Date Range:** {date_range['start']} to {date_range['end']}")
                
                latest = summary_data.get('latest_record', {})
                if latest.get('timestamp'):
                    st.write(f"**Latest Update:** {latest['timestamp']}")
            
            # Performance metrics
            st.subheader("⚡ Performance Metrics")
            
            if "system_info" in summary_data:
                system_info = summary_data["system_info"]
                
                metrics_col1, metrics_col2 = st.columns(2)
                
                with metrics_col1:
                    st.write("**API Information:**")
                    st.write(f"Version: {system_info.get('api_version', 'Unknown')}")
                    st.write(f"Database: {system_info.get('database_engine', 'Unknown')}")
                    st.write(f"Mojo Integration: {system_info.get('mojo_integration', 'Unknown')}")
                
                with metrics_col2:
                    st.write("**Last Updated:**")
                    st.write(system_info.get('last_updated', 'Unknown'))
            
            # API endpoints
            st.subheader("🔗 Available API Endpoints")
            
            endpoints = [
                ("GET", "/health", "System health check"),
                ("POST", "/generate-data", "Generate weather data from Open-Meteo API"),
                ("GET", "/weather-data", "Retrieve weather data"),
                ("GET", "/statistics", "Get statistical analysis"),
                ("GET", "/analytics", "Get advanced analytics"),
                ("GET", "/summary", "Get system summary")
            ]
            
            endpoint_df = pd.DataFrame(endpoints, columns=["Method", "Endpoint", "Description"])
            st.dataframe(endpoint_df, use_container_width=True)
            
        else:
            st.error("❌ Unable to fetch system information")
    
    # Footer
    st.divider()
    st.markdown("""
    ---
    **🔥 Mojo Weather Data Pipeline** | Built with Mojo, Python, FastAPI & Streamlit  
    High-performance data processing with modern web technologies
    """)

if __name__ == "__main__":
    main()

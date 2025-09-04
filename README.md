# 🌤️ Mojo Weather Data Pipeline - Open-Meteo Integration

[![CI/CD Pipeline](https://github.com/YOUR_USERNAME/mojo-weather-pipeline/workflows/CI/CD%20Pipeline/badge.svg)](https://github.com/YOUR_USERNAME/mojo-weather-pipeline/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Mojo](https://img.shields.io/badge/Mojo-25.6+-red.svg)](https://docs.modular.com/mojo/)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Pixi](https://img.shields.io/badge/Pixi-Package%20Manager-green.svg)](https://pixi.sh/)
[![Open-Meteo](https://img.shields.io/badge/Open--Meteo-API-lightblue.svg)](https://open-meteo.com/)

## ✅ **PRODUCTION READY - REAL WEATHER DATA**

**Status**: Complete pipeline with **real weather data** from Open-Meteo API + Mojo high-performance processing!

A comprehensive end-to-end data pipeline showcasing **Mojo's high-performance capabilities** integrated with **real-world weather data** from the Open-Meteo API. Features real-time weather processing, analytics, and interactive visualization.

## 🌟 Features

### 🌤️ **Real Weather Data Only**
- **Open-Meteo API Integration** - Exclusively uses real-time global weather data (10k requests/day free)
- **No API Key Required** - Start immediately without registration
- **Global Coverage** - Weather data for any location worldwide
- **Current + Forecast** - Real-time conditions + hourly forecasts
- **No Synthetic Data** - 100% real weather data from Open-Meteo API

### 🔥 **Mojo Integration**
- **High-performance data processing** using Mojo's SIMD capabilities
- **Zero-cost abstractions** with struct-based weather data types
- **Memory-safe operations** with Mojo's ownership system
- **Hardware portability** across different architectures
- **Real-time analytics** on live weather data

### 📊 **Data Pipeline Components**
- **Real Weather Data Fetching** - Exclusively live data from Open-Meteo API
- **Mojo Processing** - Real data processing with Mojo analytics for high-frequency insights
- **Interactive Dashboard** - Location-aware Streamlit UI with real weather
- **RESTful API** - FastAPI backend with Open-Meteo endpoints
- **Smart Caching** - Efficient data management and storage

### 📈 **Analytics Capabilities**
- Real weather data analysis (temperature, humidity, pressure, wind, rainfall)
- Location-based weather insights for 10+ major cities
- Live weather monitoring and alerting
- Weather pattern analysis and forecasting
- Statistical distributions on real meteorological data

## 🚀 Quick Start

### Prerequisites
- **Pixi** package manager ([Install here](https://pixi.sh/latest/))
- **Mojo** compiler (automatically managed by pixi environment)
- **Internet connection** (for Open-Meteo API)
- **Linux/macOS** (recommended)

### 1. Quick Setup (Recommended)
```bash
# Navigate to project directory
cd /home/jainam-jadav/Projects/life

# Run the automated setup script
./setup.sh
```

The setup script will:
- ✅ Install pixi (if not already installed)
- ✅ Set up the pixi environment with Mojo & Python
- ✅ Install all dependencies (requests, streamlit, fastapi, etc.)
- ✅ Configure Open-Meteo API integration
- ✅ Test Mojo availability
- ✅ Initialize the database
- ✅ Create necessary directories

### 1. Manual Setup (Alternative)
```bash
# Navigate to project directory
cd /home/jainam-jadav/Projects/life

# Install dependencies and setup pixi environment
pixi install

# Enter the pixi shell (optional for manual development)
pixi shell
```

### 2. Start the Pipeline
```bash
# Start the complete pipeline with Open-Meteo integration
./start_pipeline.sh
```

This will:
- ✅ Install all dependencies via pixi (including requests for API calls)
- ✅ Set up the isolated pixi environment
- ✅ Initialize the SQLite database
- ✅ Start the FastAPI backend with Open-Meteo endpoints (port 8000)
- ✅ Launch the Streamlit dashboard with location controls (port 8501)
- ✅ Run health checks
- ✅ Fetch initial real weather data from Open-Meteo API

### 3. Access the Application
- **🌤️ Dashboard**: http://localhost:8501 (Interactive weather data dashboard)
- **🔗 API Docs**: http://localhost:8000/docs (FastAPI interactive docs)
- **📡 Current Weather**: http://localhost:8000/openmeteo/current/51.5074/-0.1278
- **📊 Weather Forecast**: http://localhost:8000/openmeteo/forecast/51.5074/-0.1278
- **🏥 Health Check**: http://localhost:8000/health

### 4. Generate Real Weather Data
```bash
# Using the dashboard (recommended)
# 1. Open http://localhost:8501
# 2. Select "Open-Meteo API (Real Weather)" in sidebar
# 3. Choose location (London, Tokyo, NYC, etc.)
# 4. Click "🚀 Generate Data"

# Using API directly
curl -X POST "http://localhost:8000/generate-data" \
  -H "Content-Type: application/json" \
  -d '{
    "num_points": 24,
    "latitude": 51.5074,
    "longitude": -0.1278,
    "use_real_data": true
  }'
```

### 5. Development Commands
```bash
# Available pixi tasks (run from project directory)
pixi run health-check    # Check API and Open-Meteo connectivity
pixi run test-api        # Test API endpoints  
pixi run test-mojo       # Run Mojo processor
pixi run generate-data   # Generate sample data
pixi run clean-logs      # Clear log files
pixi shell              # Enter development shell

# Manual development in pixi shell
pixi shell
> mojo data_processor.mojo           # Test Mojo processor
> python database.py                # Initialize database
> uvicorn api:app --reload           # Start API server
> streamlit run streamlit_app.py     # Start dashboard
```

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   🔥 Mojo       │    │   🐍 Python      │    │   📊 Streamlit  │
│ Data Processor  │────│   FastAPI        │────│    Dashboard    │
│                 │    │   Backend        │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                     ┌──────────────────┐
                     │   🗄️ SQLite      │
                     │   Database       │
                     └──────────────────┘

## 🔧 Troubleshooting

### Common Issues

1. **API Not Starting**
   ```bash
   # Check if port 8000 is available
   lsof -i :8000
   # Kill existing process if needed
   kill -9 $(lsof -t -i:8000)
   ```

2. **Streamlit Connection Issues**
   ```bash
   # Verify API is running
   curl http://localhost:8000/health
   # Check port 8501 availability
   lsof -i :8501
   ```

3. **Open-Meteo API Issues**
   ```bash
   # Test Open-Meteo connectivity
   curl "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m"
   # Check API rate limits (10,000 requests/day)
   ```

4. **Mojo Compilation Errors**
   ```bash
   # Ensure Mojo is properly installed
   mojo --version
   # Check Mojo compiler compatibility
   pixi run test-mojo
   ```

5. **Database Issues**
   ```bash
   # Reset database if needed
   rm weather_data.db
   python database.py
   ```

### Environment Issues
```bash
# Clean and reinstall environment
pixi clean
rm -rf .pixi
pixi install

# Check all dependencies
pixi info
pixi list
```

## 📁 Project Structure

```
life/
├── 🔥 data_processor.mojo      # High-performance data processing with Open-Meteo integration
├── 🐍 api.py                   # FastAPI backend with weather endpoints
├── 📊 streamlit_app.py         # Interactive dashboard with location controls
├── 🗄️ database.py              # SQLite database management
├── 📦 pixi.toml               # Package manager configuration
├── 🔒 pixi.lock               # Dependency lock file
├── 📚 README.md               # This documentation
└── 🗄️ weather_data.db         # SQLite database (auto-generated)
```

### Key Components

- **data_processor.mojo**: Core Mojo module with Open-Meteo API integration
  - `fetch_openmeteo_data()`: Real weather data fetching
  - `DataPoint`: Enhanced struct with wind speed and rainfall
  - `calculate_statistics()`: Advanced weather analytics

- **api.py**: FastAPI backend server
  - `/openmeteo/current/{lat}/{lon}`: Current weather endpoint
  - `/openmeteo/forecast/{lat}/{lon}`: Forecast endpoint
  - `/locations/popular`: Popular cities with coordinates
  - `/generate-data`: Enhanced data generation with real weather

- **streamlit_app.py**: Interactive web dashboard
  - Location picker with popular cities
  - Real-time weather data display
  - Data source toggle (synthetic vs real)
  - Analytics and statistics visualization

## 🚀 Next Steps & Enhancements

### Immediate Improvements
1. **Enhanced Error Handling**: Add retry logic for API failures
2. **Caching Layer**: Implement Redis for API response caching
3. **Data Validation**: Add comprehensive input validation
4. **Logging**: Enhance logging with structured JSON format

### Advanced Features
1. **Weather Alerts**: Real-time weather warnings and notifications
2. **Historical Data**: Integration with weather history APIs
3. **Machine Learning**: Weather prediction models using Mojo
4. **Multi-Location**: Compare weather across multiple cities
5. **Export Features**: CSV/JSON data export functionality

### Performance Optimizations
1. **Async Processing**: Implement async weather data fetching
2. **Background Jobs**: Scheduled weather data updates
3. **Database Optimization**: Implement proper indexing and partitioning
4. **API Rate Limiting**: Smart request throttling for Open-Meteo

### Production Readiness
1. **Docker Deployment**: Containerized application setup
2. **Environment Configuration**: Proper environment variable management
3. **Security**: API key management and request authentication
4. **Monitoring**: Health checks and performance metrics

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Clone your fork: `git clone <your-fork-url>`
3. Install dependencies: `pixi install`
4. Create a feature branch: `git checkout -b feature/amazing-feature`
5. Make changes and test: `pixi run test-api && pixi run test-mojo`
6. Commit changes: `git commit -m 'Add amazing feature'`
7. Push to branch: `git push origin feature/amazing-feature`
8. Open a Pull Request

### Code Style
- **Mojo**: Follow Mojo language conventions and best practices
- **Python**: Use Black formatter and follow PEP 8
- **Documentation**: Update README.md for any new features
- **Testing**: Add tests for new functionality

### Reporting Issues
- Use GitHub Issues for bug reports and feature requests
- Include system information and reproduction steps
- Attach relevant logs and error messages

## 📊 API Endpoints Reference

### Weather Data Endpoints
```http
GET  /health                           # API health check
POST /generate-data                    # Generate weather data
GET  /weather-data                     # Retrieve stored data
GET  /analytics                        # Weather analytics
GET  /statistics                       # Statistical summary

# Open-Meteo Integration
GET  /openmeteo/current/{lat}/{lon}    # Current weather
GET  /openmeteo/forecast/{lat}/{lon}   # Weather forecast
GET  /locations/popular                # Popular cities list
```

### Request/Response Examples
```json
// POST /generate-data
{
  "num_points": 24,
  "latitude": 51.5074,
  "longitude": -0.1278,
  "use_real_data": true
}

// Response
{
  "message": "✅ Successfully fetched weather data from Open-Meteo",
  "points_generated": 24,
  "data_source": "open_meteo_api",
  "location": "London, UK"
}
```

## 🏆 Project Highlights

### ✨ What Makes This Special
- **🔥 Mojo Integration**: High-performance weather processing with cutting-edge language
- **🌍 Real Weather Data**: Live data from Open-Meteo API (no API key required)
- **📊 Interactive Dashboard**: Beautiful Streamlit interface with location controls
- **⚡ Performance**: Fast data processing with Mojo + Python hybrid architecture
- **🔧 Modern Tooling**: Pixi package management for seamless development
- **📱 Responsive Design**: Works on desktop and mobile devices

### 📈 Technical Achievements
- Successfully integrated Mojo with Python ecosystem
- Implemented real-time weather data pipeline
- Created responsive web dashboard with location awareness
- Built scalable architecture with proper separation of concerns
- Achieved 10,000+ daily API requests capability with Open-Meteo

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **Open-Meteo**: Excellent free weather API service
- **Modular AI**: For the incredible Mojo programming language  
- **Pixi**: Modern package management for cross-platform development
- **Streamlit**: Beautiful and easy-to-use web framework
- **FastAPI**: High-performance web framework for building APIs
- **Plotly**: Interactive visualization capabilities

---

**🎯 Ready to explore weather data with the power of Mojo? Get started now!**

```bash
git clone <your-repo-url>
cd life
pixi install
pixi run start-all
```

Then visit http://localhost:8501 and start exploring real weather data! 🌤️

---

**🔥 Built with Mojo - The future of high-performance programming!**

For more information about Mojo, visit: https://docs.modular.com/mojo/
```

### Component Details

#### 🔥 Mojo Data Processor (`data_processor.mojo`)
- **High-performance weather data generation** using SIMD operations
- **Statistical calculations** with zero-cost abstractions
- **Memory-efficient data structures** using Mojo structs
- **Python interoperability** for seamless integration

#### 🐍 FastAPI Backend (`api.py`)
- **RESTful API endpoints** for data access and control
- **Background task processing** for data generation
- **Real-time analytics** computation
- **CORS-enabled** for web frontend integration

#### 📊 Streamlit Dashboard (`streamlit_app.py`)
- **Interactive real-time dashboard** with auto-refresh
- **Multi-tab interface** for different views
- **Plotly visualizations** for beautiful charts
- **Data export capabilities** (CSV download)

#### 🗄️ Database Layer (`database.py`)
- **SQLite integration** for data persistence
- **Efficient queries** with proper indexing
- **Data aggregation** functions
- **Cleanup utilities** for data management

## 📋 API Endpoints

### Core Endpoints
- `GET /` - API information and available endpoints
- `GET /health` - System health check and status
- `POST /generate-data` - Generate synthetic weather data
- `GET /weather-data` - Retrieve weather data with filtering
- `GET /statistics` - Calculate comprehensive statistics
- `GET /analytics` - Advanced analytics and patterns
- `GET /summary` - Overall system summary

### Data Management
- `GET /aggregated-data/{interval}` - Aggregated data by time intervals
- `DELETE /clear-old-data/{days}` - Remove old data records

## 🔧 Configuration

### Pixi Environment
The project uses **pixi** for dependency management and environment isolation:

```toml
# pixi.toml - Environment configuration
[workspace]
name = "life"
channels = ["https://conda.modular.com/max-nightly", "conda-forge"]
platforms = ["linux-64"]

[dependencies]
mojo = ">=25.6.0.dev2025090305,<26"
python = ">=3.11"
fastapi = "*"
uvicorn = "*"
streamlit = "*"
# ... other dependencies

[tasks]
# Development tasks
dev = "pixi shell"
test-mojo = "mojo data_processor.mojo"
start-api = "uvicorn api:app --host 0.0.0.0 --port 8000 --reload"
start-ui = "streamlit run streamlit_app.py --server.port 8501"
# ... other tasks
```

### Environment Variables
```bash
export API_BASE_URL="http://localhost:8000"  # API backend URL
export DB_PATH="weather_data.db"             # Database file path
export LOG_LEVEL="INFO"                      # Logging level
```

### Pixi Task Configuration
All tasks are defined in `pixi.toml` and run in the isolated environment:
- **Development**: `pixi shell` - Enter development shell
- **Testing**: `pixi run test-mojo` - Test Mojo processor
- **Services**: `pixi run start-api` - Start API server
- **Database**: `pixi run init-db` - Initialize database
- **Cleanup**: `pixi run clean-all` - Clean logs and data

## 📊 Data Schema

### Weather Data Point
```mojo
struct DataPoint:
    var timestamp: Float64     # Unix timestamp
    var temperature: Float64   # Temperature in Celsius
    var humidity: Float64      # Humidity percentage (0-100)
    var pressure: Float64      # Atmospheric pressure in hPa
    var wind_speed: Float64    # Wind speed in km/h
    var rainfall: Float64      # Rainfall in mm
```

### Database Tables
- **weather_data** - Raw weather measurements
- **weather_statistics** - Calculated statistics and analytics

## 🎯 Performance Features

### Mojo Optimizations
- **SIMD vectorization** for bulk data processing
- **Zero-copy data structures** for memory efficiency
- **Compile-time optimizations** through metaprogramming
- **Hardware-agnostic** code that runs efficiently on any platform

### System Optimizations
- **Database indexing** for fast queries
- **Efficient data aggregation** for real-time analytics
- **Caching strategies** in the frontend
- **Background processing** for non-blocking operations

## 🧪 Usage Examples

### Generate Weather Data
```bash
curl -X POST "http://localhost:8000/generate-data" \
     -H "Content-Type: application/json" \
     -d '{"num_points": 5000}'
```

### Get Recent Weather Data
```bash
curl "http://localhost:8000/weather-data?limit=100"
```

### Get Statistics
```bash
curl "http://localhost:8000/statistics"
```

### Get Analytics
```bash
curl "http://localhost:8000/analytics"
```

## 📈 Dashboard Features

### Real-time Dashboard Tab
- **Live weather metrics** with trend indicators
- **Time series charts** for all weather parameters
- **Current conditions** display
- **Auto-refresh capability** (30-second intervals)

### Analytics Tab
- **Trend analysis** for temperature and pressure
- **Weather pattern detection** (high pressure, rainy days, extremes)
- **Daily pattern analysis** (peak hours, temperature ranges)
- **Variable correlation analysis** with interactive charts

### Data Explorer Tab
- **Raw data browsing** with filtering capabilities
- **Date range selection** for historical analysis
- **Data quality metrics** and completeness indicators
- **CSV export functionality** for external analysis

### Statistics Tab
- **Comprehensive statistical analysis** for all variables
- **Distribution visualizations** with normal curve fitting
- **Min/max/mean/standard deviation** calculations
- **Visual statistical summaries**

### System Info Tab
- **Pipeline status monitoring** for all components
- **Performance metrics** and system information
- **API endpoint documentation** within the dashboard
- **Data summary** and update timestamps

## 🛠️ Development

### Project Structure
```
life/
├── 🔥 data_processor.mojo    # Mojo data processor
├── 🐍 api.py                # FastAPI backend
├── 📊 streamlit_app.py      # Streamlit dashboard
├── 🗄️ database.py           # Database layer
├── ⚙️ start_pipeline.sh     # Pipeline startup script
├── �️ setup.sh              # Quick setup script
├── �📦 pixi.toml             # Pixi environment configuration
├── 📋 pixi.lock             # Dependency lock file
├── 🔥 life.mojo             # Original Mojo hello world
├── 📖 README.md             # This documentation
└── 📁 logs/                 # Application logs (created at runtime)
    ├── api.log              # API server logs
    ├── streamlit.log        # Streamlit logs
    └── mojo_test.log        # Mojo processor logs
```

### Adding New Features
1. **Extend Mojo processor** for new data types or algorithms
2. **Add API endpoints** in `api.py` for new functionality
3. **Create dashboard tabs** in `streamlit_app.py` for visualization
4. **Update database schema** in `database.py` if needed

### Testing
```bash
# Test Mojo processor in pixi environment
pixi run test-mojo

# Test API endpoints
pixi run health-check
pixi run test-api

# Test database operations
pixi run init-db

# Manual testing in pixi shell
pixi shell
> mojo data_processor.mojo    # Direct Mojo execution
> python database.py         # Database operations
> curl http://localhost:8000/health  # API testing
```

### Working with Pixi Shell
```bash
# Enter the isolated development environment
pixi shell

# Inside pixi shell, all dependencies are available:
(life) $ mojo --version              # Mojo compiler
(life) $ python --version           # Python interpreter  
(life) $ pip list                    # Installed packages
(life) $ streamlit --version        # Streamlit
(life) $ uvicorn --version          # FastAPI server

# Exit pixi shell
(life) $ exit
```

## 🔍 Troubleshooting

### Common Issues

#### Pixi Environment Issues
```bash
# Recreate pixi environment
pixi clean
pixi install

# Check pixi environment status
pixi info
pixi list

# Verify Mojo in pixi environment
pixi run mojo --version
```

#### Mojo Not Found
```bash
# Ensure you're using pixi environment
pixi shell
> mojo --version

# Or run via pixi task
pixi run test-mojo
```

#### Port Conflicts
```bash
# Check running processes
lsof -i :8000  # API port
lsof -i :8501  # Streamlit port

# Kill processes if needed
pkill -f "uvicorn.*api:app"
pkill -f "streamlit.*streamlit_app.py"

# Or use pixi tasks to restart cleanly
./start_pipeline.sh
```

#### Database Issues
```bash
# Reset database using pixi task
pixi run reset-db

# Or manually
rm weather_data.db
pixi run init-db
```

### Logs
Check application logs in the `logs/` directory:
- `api.log` - Backend API logs
- `streamlit.log` - Frontend dashboard logs
- `mojo_test.log` - Mojo processor test output

## 🚀 Future Enhancements

### Planned Features
- **Real sensor integration** with IoT devices
- **Machine learning predictions** using Mojo's ML capabilities
- **Geographic weather mapping** with location-based data
- **Historical data comparison** and seasonal analysis
- **Alert system** for extreme weather conditions
- **Mobile-responsive dashboard** design

### Performance Improvements
- **GPU acceleration** using Mojo's GPU package
- **Distributed processing** for large datasets
- **Real-time streaming** data ingestion
- **Advanced caching** strategies

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Quick Contribution Steps
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup
```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/mojo-weather-pipeline.git
cd mojo-weather-pipeline

# Setup development environment
./setup.sh

# Run tests
./test_pipeline.sh
```

## 📋 Project Status

### Current Version: 1.0.0
- ✅ Real weather data integration (Open-Meteo API)
- ✅ Mojo high-performance processing
- ✅ Interactive Streamlit dashboard
- ✅ FastAPI backend with comprehensive endpoints
- ✅ Comprehensive analytics and business intelligence
- ✅ SQLite database with efficient storage
- ✅ Production-ready deployment scripts

### Roadmap
See our [GitHub Issues](https://github.com/YOUR_USERNAME/mojo-weather-pipeline/issues) for planned features and improvements.

## 🐛 Bug Reports & 💡 Feature Requests

- **Bug Reports**: [Create a bug report](https://github.com/YOUR_USERNAME/mojo-weather-pipeline/issues/new?template=bug_report.md)
- **Feature Requests**: [Request a feature](https://github.com/YOUR_USERNAME/mojo-weather-pipeline/issues/new?template=feature_request.md)
- **Performance Issues**: [Report performance problems](https://github.com/YOUR_USERNAME/mojo-weather-pipeline/issues/new?template=performance.md)

## � Security

If you discover any security vulnerabilities, please see our [Security Policy](SECURITY.md) for responsible disclosure guidelines.

## 📊 Project Statistics

![GitHub stars](https://img.shields.io/github/stars/YOUR_USERNAME/mojo-weather-pipeline?style=social)
![GitHub forks](https://img.shields.io/github/forks/YOUR_USERNAME/mojo-weather-pipeline?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/YOUR_USERNAME/mojo-weather-pipeline?style=social)

## �📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Modular AI** for the incredible Mojo programming language
- **Open-Meteo** for providing free, high-quality weather data
- **Streamlit** for the beautiful and easy-to-use web framework
- **FastAPI** for the high-performance web framework
- **Plotly** for interactive visualization capabilities
- **Pixi** for excellent package management
- All contributors who help improve this project

## 📞 Support & Community

- **Documentation**: Check our comprehensive [README](README.md) and [Contributing Guide](CONTRIBUTING.md)
- **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/mojo-weather-pipeline/issues)
- **Discussions**: [GitHub Discussions](https://github.com/YOUR_USERNAME/mojo-weather-pipeline/discussions)
- **Code of Conduct**: [Community Guidelines](CODE_OF_CONDUCT.md)

---

**Built with ❤️ using Mojo, Python, and real weather data** 🌤️🔥

---

**🔥 Built with Mojo - The future of high-performance programming!**

For more information about Mojo, visit: https://docs.modular.com/mojo/

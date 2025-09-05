# Installation Guide - Advanced Weather Data Pipeline v2.0
============================================================

## Prerequisites

### System Requirements

- **Operating System**: Linux, macOS, or Windows with WSL2
- **Memory**: Minimum 8GB RAM (16GB recommended)
- **Storage**: At least 5GB free space
- **Network**: Internet connection for weather data API

### Required Software

1. **Python 3.11+**
   ```bash
   python --version  # Should be 3.11 or higher
   ```

2. **Pixi Package Manager**
   ```bash
   curl -fsSL https://pixi.sh/install.sh | bash
   source ~/.bashrc  # or restart terminal
   ```

3. **Git**
   ```bash
   git --version
   ```

4. **Docker (Optional)**
   ```bash
   docker --version
   docker-compose --version
   ```

## Installation Methods

### Method 1: Pixi Environment (Recommended)

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd life
   ```

2. **Setup with Pixi**
   ```bash
   chmod +x scripts/setup.sh
   ./scripts/setup.sh
   ```

3. **Activate Environment**
   ```bash
   pixi shell
   ```

4. **Start the Pipeline**
   ```bash
   ./scripts/start_pipeline.sh
   ```

### Method 2: Python Virtual Environment

1. **Clone and Setup**
   ```bash
   git clone <repository-url>
   cd life
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Mojo (Optional)**
   Follow [Mojo installation guide](https://docs.modular.com/mojo/manual/get-started/)

4. **Run Services**
   ```bash
   # API Server
   python main.py api
   
   # Dashboard (in another terminal)
   python main.py dashboard
   ```

### Method 3: Docker Deployment

1. **Clone Repository**
   ```bash
   git clone <repository-url>
   cd life
   ```

2. **Development Mode**
   ```bash
   docker-compose up --build
   ```

3. **Production Mode**
   ```bash
   docker-compose -f docker-compose.yml -f docker-compose.prod.yml up --build
   ```

## Verification

### Check Installation

1. **API Server**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Dashboard**
   Open browser: http://localhost:8501

3. **Mojo Processor**
   ```bash
   pixi run test-mojo
   ```

### Expected Output

- API health check returns system status
- Dashboard loads with weather interface
- Mojo processor executes without errors

## Configuration

### Environment Variables

Create `.env` file in project root:

```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=false

# Weather API
WEATHER_API_KEY=your_api_key_here  # Optional for Open-Meteo

# Database
DATABASE_PATH=src/data/weather_data.db

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

### Pixi Configuration

The `config/pixi.toml` file contains:
- Python environment setup
- Mojo installation
- Dependency management
- Task definitions

## Troubleshooting

### Common Issues

1. **Pixi Installation Failed**
   ```bash
   # Manual installation
   curl -fsSL https://pixi.sh/install.sh | bash
   export PATH="$HOME/.pixi/bin:$PATH"
   ```

2. **Mojo Not Found**
   ```bash
   # Check Mojo in pixi environment
   pixi run mojo --version
   
   # If missing, reinstall pixi environment
   pixi install --locked
   ```

3. **Port Already in Use**
   ```bash
   # Kill existing processes
   pkill -f uvicorn
   pkill -f streamlit
   
   # Or use different ports
   python main.py api  # Uses port 8000
   streamlit run src/dashboard/app.py --server.port 8502
   ```

4. **Permission Denied on Scripts**
   ```bash
   chmod +x scripts/*.sh
   ```

### Performance Optimization

1. **Enable Mojo Acceleration**
   - Ensure Mojo is properly installed
   - Use pixi environment for optimal performance

2. **Database Optimization**
   - Regular VACUUM operations
   - Index optimization for frequent queries

3. **Memory Management**
   - Monitor memory usage via `/health` endpoint
   - Adjust worker processes in production

## Development Setup

### IDE Configuration

**VS Code Extensions:**
- Python
- Mojo (if available)
- Docker
- GitLens

**Settings:**
```json
{
    "python.defaultInterpreterPath": ".pixi/envs/default/bin/python",
    "python.terminal.activateEnvironment": false
}
```

### Pre-commit Hooks

```bash
pip install pre-commit
pre-commit install
```

## Next Steps

1. **Read Documentation**: Review `docs/API.md` for API usage
2. **Explore Dashboard**: Open http://localhost:8501
3. **Run Tests**: `python main.py test`
4. **Custom Configuration**: Modify `config/pixi.toml` as needed

## Support

- **Issues**: Create GitHub issue with error logs
- **Documentation**: Check `docs/` directory
- **Performance**: Monitor via dashboard metrics

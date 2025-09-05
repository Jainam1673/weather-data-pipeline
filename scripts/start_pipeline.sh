#!/bin/bash

# Weather Data Pipeline Startup Script
# Starts the complete end-to-end data pipeline using pixi shell

echo "🔥 Mojo Weather Data Pipeline Startup"
echo "======================================"

# Check if pixi is available
if ! command -v pixi &> /dev/null; then
    echo "❌ Pixi is not installed. Please install pixi first."
    echo "Visit: https://pixi.sh/latest/"
    exit 1
fi

# Check if we're in the correct directory
if [ ! -f "pixi.toml" ]; then
    echo "❌ pixi.toml not found. Please run this script from the project root directory."
    exit 1
fi

# Install dependencies and setup environment
echo "📦 Installing dependencies and setting up pixi environment..."
pixi install

# Check if Mojo is available in pixi environment
echo "🔥 Checking Mojo installation in pixi environment..."
if pixi run mojo --version > /dev/null 2>&1; then
    echo "✅ Mojo is available in pixi environment"
    pixi run mojo --version
else
    echo "❌ Mojo not available in pixi environment"
    echo "Please check your pixi.toml configuration"
    exit 1
fi

# Create necessary directories
echo "📁 Setting up directories..."
mkdir -p logs
mkdir -p data

# Initialize database using pixi environment
echo "🗄️ Initializing database..."
pixi run init-db

# Function to start API server in pixi environment
start_api() {
    echo "🚀 Starting API server in pixi environment..."
    pixi run start-api > logs/api.log 2>&1 &
    API_PID=$!
    echo "API server started with PID: $API_PID"
    sleep 3
}

# Function to start Streamlit app in pixi environment
start_streamlit() {
    echo "📊 Starting Streamlit dashboard in pixi environment..."
    pixi run start-ui > logs/streamlit.log 2>&1 &
    STREAMLIT_PID=$!
    echo "Streamlit started with PID: $STREAMLIT_PID"
    sleep 3
}

# Function to test Mojo processor in pixi environment
test_mojo() {
    echo "🔥 Testing Mojo data processor in pixi environment..."
    if [ -f "src/processors/weather_processor.mojo" ]; then
        pixi run test-mojo > logs/mojo_test.log 2>&1
        if [ $? -eq 0 ]; then
            echo "✅ Mojo processor test completed successfully"
        else
            echo "⚠️  Mojo processor test encountered issues (check logs/mojo_test.log)"
        fi
    else
        echo "⚠️  Mojo processor file not found"
    fi
}

# Function to check health using pixi environment
check_health() {
    echo "🏥 Checking system health..."
    
    # Wait for API to be ready
    for i in {1..30}; do
        if pixi run health-check > /dev/null 2>&1; then
            echo "✅ API server is healthy"
            break
        fi
        if [ $i -eq 30 ]; then
            echo "❌ API server health check failed"
            return 1
        fi
        sleep 1
    done
    
    # Check Streamlit
    for i in {1..30}; do
        if curl -s http://localhost:8501 > /dev/null 2>&1; then
            echo "✅ Streamlit is healthy"
            break
        fi
        if [ $i -eq 30 ]; then
            echo "❌ Streamlit health check failed"
            return 1
        fi
        sleep 1
    done
}

# Function to generate initial data using pixi environment
generate_initial_data() {
    echo "📊 Generating initial weather data..."
    sleep 5  # Wait for API to be fully ready
    
    if pixi run generate-data > /dev/null 2>&1; then
        echo "✅ Initial data generation request sent"
        echo "⏳ Data processing in background..."
    else
        echo "⚠️  Failed to send data generation request (check if API is running)"
    fi
}

# Function to cleanup processes
cleanup() {
    echo ""
    echo "🛑 Shutting down pipeline..."
    
    if [ ! -z "$API_PID" ]; then
        kill $API_PID 2>/dev/null
        echo "🔴 API server stopped"
    fi
    
    if [ ! -z "$STREAMLIT_PID" ]; then
        kill $STREAMLIT_PID 2>/dev/null
        echo "🔴 Streamlit stopped"
    fi
    
    # Kill any remaining processes started by pixi
    pkill -f "uvicorn.*api" 2>/dev/null
    pkill -f "streamlit.*app.py" 2>/dev/null
    
    echo "✅ Cleanup completed"
    echo ""
    echo "💡 To restart the pipeline, run: ./start_pipeline.sh"
    echo "💡 To enter pixi shell manually, run: pixi shell"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Main execution
echo ""
echo "🚀 Starting pipeline components..."

# Test Mojo processor first
test_mojo

# Start API server
start_api

# Start Streamlit
start_streamlit

# Check health
check_health

# Generate initial data
generate_initial_data

echo ""
echo "🎉 Pipeline startup completed!"
echo ""
echo "📊 Dashboard URL: http://localhost:8501"
echo "🔗 API Documentation: http://localhost:8000/docs"
echo "🏥 Health Check: http://localhost:8000/health"
echo ""
echo "💡 Available pixi tasks:"
echo "   • pixi run health-check    - Check API health"
echo "   • pixi run test-api        - Test API endpoints"
echo "   • pixi run test-mojo       - Run Mojo processor"
echo "   • pixi run generate-data   - Generate sample data"
echo "   • pixi run clean-logs      - Clear log files"
echo "   • pixi shell               - Enter development shell"
echo ""
echo "🔥 Features available:"
echo "   • High-performance data processing with Mojo"
echo "   • Real-time weather analytics"
echo "   • Interactive data visualization"
echo "   • RESTful API endpoints"
echo "   • Statistical analysis"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Keep script running and show logs
echo "📋 Live logs (press Ctrl+C to stop):"
echo "======================================"

# Monitor logs
tail -f logs/api.log logs/streamlit.log 2>/dev/null &
LOG_PID=$!

# Wait for interrupt
wait

# Cleanup
kill $LOG_PID 2>/dev/null
cleanup

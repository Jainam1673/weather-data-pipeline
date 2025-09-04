#!/bin/bash

# Quick setup script for the Mojo Weather Data Pipeline
# This script helps users get started with the pixi environment

echo "🔥 Mojo Weather Data Pipeline - Quick Setup"
echo "==========================================="

# Check if pixi is installed
if ! command -v pixi &> /dev/null; then
    echo "❌ Pixi is not installed."
    echo ""
    echo "📦 Installing pixi..."
    
    # Install pixi
    if command -v curl &> /dev/null; then
        curl -fsSL https://pixi.sh/install.sh | bash
        echo "✅ Pixi installed! Please restart your terminal or run:"
        echo "   source ~/.bashrc"
        echo ""
        echo "Then run this setup script again."
        exit 0
    else
        echo "❌ curl not found. Please install pixi manually:"
        echo "   Visit: https://pixi.sh/latest/"
        exit 1
    fi
fi

echo "✅ Pixi is available: $(pixi --version)"

# Check if we're in the right directory
if [ ! -f "pixi.toml" ]; then
    echo "❌ pixi.toml not found. Please run this script from the project root directory."
    exit 1
fi

echo ""
echo "📦 Setting up pixi environment..."

# Install dependencies
pixi install

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully!"
else
    echo "❌ Failed to install dependencies. Please check your internet connection."
    exit 1
fi

echo ""
echo "🔥 Testing Mojo availability..."

# Test Mojo
if pixi run mojo --version > /dev/null 2>&1; then
    echo "✅ Mojo is available in pixi environment:"
    pixi run mojo --version
else
    echo "❌ Mojo is not available. Please check the pixi.toml configuration."
    exit 1
fi

echo ""
echo "🗄️ Setting up database..."

# Create logs directory
mkdir -p logs

# Initialize database
pixi run init-db

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "🚀 Next steps:"
echo "   1. Start the complete pipeline:"
echo "      ./start_pipeline.sh"
echo ""
echo "   2. Or explore the pixi environment:"
echo "      pixi shell                    # Enter development shell"
echo "      pixi run test-mojo            # Test Mojo processor"
echo "      pixi run health-check         # Check API health"
echo ""
echo "   3. Available URLs (after starting):"
echo "      📊 Dashboard: http://localhost:8501"
echo "      🔗 API Docs:  http://localhost:8000/docs"
echo ""
echo "📚 See README.md for detailed documentation."
echo ""
echo "Happy coding with Mojo! 🔥"

#!/usr/bin/env python3
"""
Advanced Weather Data Pipeline v2.0 - Main Entry Point
======================================================

Professional weather data processing system with multiple execution modes:
- API Server: FastAPI backend with ML capabilities
- Dashboard: Streamlit interactive interface
- Data Processing: Mojo-powered high-performance processing
- Testing: Comprehensive test suite execution

Usage:
    python main.py api           # Start FastAPI server
    python main.py dashboard     # Start Streamlit dashboard
    python main.py process       # Run weather data processing
    python main.py test          # Run test suite
    python main.py --help        # Show this help message

Author: Weather Analytics Team
Version: 2.0.0
"""

import argparse
import sys
import subprocess
import os
from pathlib import Path

# Add src directory to Python path
PROJECT_ROOT = Path(__file__).parent
SRC_DIR = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))


def start_api_server():
    """Start the FastAPI server."""
    print("🚀 Starting Advanced Weather API Server v2.0...")
    os.chdir(PROJECT_ROOT)
    subprocess.run([
        "uvicorn", 
        "src.api.server:app", 
        "--host", "0.0.0.0", 
        "--port", "8000", 
        "--reload"
    ])


def start_dashboard():
    """Start the Streamlit dashboard."""
    print("📊 Starting Weather Analytics Dashboard...")
    os.chdir(PROJECT_ROOT)
    subprocess.run([
        "streamlit", 
        "run", 
        "src/dashboard/app.py",
        "--server.port", "8501"
    ])


def run_processing():
    """Run weather data processing with Mojo."""
    print("⚡ Running High-Performance Weather Processing...")
    os.chdir(PROJECT_ROOT)
    subprocess.run(["mojo", "src/processors/weather_processor.mojo"])


def run_tests():
    """Run the test suite."""
    print("🧪 Running Test Suite...")
    os.chdir(PROJECT_ROOT)
    subprocess.run(["python", "-m", "pytest", "tests/", "-v"])


def main():
    """Main entry point with command-line interface."""
    parser = argparse.ArgumentParser(
        description="Advanced Weather Data Pipeline v2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py api           Start the API server
  python main.py dashboard     Start the dashboard
  python main.py process       Run data processing
  python main.py test          Run tests
        """
    )
    
    parser.add_argument(
        "mode",
        choices=["api", "dashboard", "process", "test"],
        help="Execution mode"
    )
    
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    args = parser.parse_args()
    
    print(f"🌦️  Advanced Weather Data Pipeline v2.0")
    print(f"{'='*50}")
    
    if args.mode == "api":
        start_api_server()
    elif args.mode == "dashboard":
        start_dashboard()
    elif args.mode == "process":
        run_processing()
    elif args.mode == "test":
        run_tests()


if __name__ == "__main__":
    main()

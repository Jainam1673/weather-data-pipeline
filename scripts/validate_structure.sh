#!/bin/bash

# Professional Structure Validation Script
# =========================================

echo "🏗️  Advanced Weather Data Pipeline v2.0 - Structure Validation"
echo "=============================================================="

PROJECT_ROOT="/home/jainam-jadav/Projects/life"
cd "$PROJECT_ROOT"

# Color codes for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo ""
echo -e "${BLUE}📁 Checking Professional Directory Structure...${NC}"

# Check main directories
directories=(
    "src"
    "src/api"
    "src/dashboard" 
    "src/data"
    "src/processors"
    "tests"
    "docs"
    "config"
    "scripts"
    "logs"
)

for dir in "${directories[@]}"; do
    if [ -d "$dir" ]; then
        echo -e "${GREEN}✅ $dir/${NC}"
    else
        echo -e "${RED}❌ $dir/ - Missing${NC}"
    fi
done

echo ""
echo -e "${BLUE}📄 Checking Core Files...${NC}"

# Check main files
files=(
    "main.py:Main entry point"
    "requirements.txt:Python dependencies"
    "Dockerfile:Container definition"
    "docker-compose.yml:Multi-service deployment"
    "src/api/server.py:FastAPI server"
    "src/dashboard/app.py:Streamlit dashboard"
    "src/data/database.py:Database operations"
    "src/processors/weather_processor.mojo:Mojo processor"
    "tests/test_api_server.py:API tests"
    "docs/API.md:API documentation"
    "docs/INSTALL.md:Installation guide"
    "scripts/setup.sh:Setup script"
    "scripts/start_pipeline.sh:Pipeline starter"
    "config/pixi.toml:Pixi configuration"
)

for file_info in "${files[@]}"; do
    IFS=':' read -r file desc <<< "$file_info"
    if [ -f "$file" ]; then
        echo -e "${GREEN}✅ $file${NC} - $desc"
    else
        echo -e "${RED}❌ $file - Missing${NC} - $desc"
    fi
done

echo ""
echo -e "${BLUE}🔗 Checking Symbolic Links...${NC}"

# Check symbolic links
if [ -L "pixi.toml" ] && [ -f "pixi.toml" ]; then
    echo -e "${GREEN}✅ pixi.toml -> config/pixi.toml${NC}"
else
    echo -e "${YELLOW}⚠️  pixi.toml symlink${NC}"
fi

if [ -L "pixi.lock" ] && [ -f "pixi.lock" ]; then
    echo -e "${GREEN}✅ pixi.lock -> config/pixi.lock${NC}"
else
    echo -e "${YELLOW}⚠️  pixi.lock symlink${NC}"
fi

echo ""
echo -e "${BLUE}🧪 Testing Import Paths...${NC}"

# Test Python imports
python3 -c "
import sys
sys.path.insert(0, 'src')
try:
    from src.api import server
    print('✅ API module imports correctly')
except Exception as e:
    print(f'❌ API import failed: {e}')

try:
    from src.data import database
    print('✅ Data module imports correctly')
except Exception as e:
    print(f'❌ Data import failed: {e}')
" 2>/dev/null

echo ""
echo -e "${BLUE}🚀 Testing Main Entry Point...${NC}"

# Test main.py help
if python3 main.py --help > /dev/null 2>&1; then
    echo -e "${GREEN}✅ main.py entry point works${NC}"
else
    echo -e "${RED}❌ main.py entry point failed${NC}"
fi

echo ""
echo -e "${BLUE}📊 Project Statistics...${NC}"

# Count files by type
python_files=$(find src -name "*.py" | wc -l)
mojo_files=$(find src -name "*.mojo" | wc -l)
test_files=$(find tests -name "*.py" | wc -l)
doc_files=$(find docs -name "*.md" | wc -l)

echo "📄 Python files: $python_files"
echo "🔥 Mojo files: $mojo_files"
echo "🧪 Test files: $test_files"
echo "📚 Documentation files: $doc_files"

echo ""
echo -e "${GREEN}🎉 Professional structure validation complete!${NC}"
echo ""
echo -e "${BLUE}💡 Next steps:${NC}"
echo "   1. Run: python main.py api"
echo "   2. Run: python main.py dashboard"
echo "   3. Run: python main.py test"
echo "   4. Check: http://localhost:8000/health"

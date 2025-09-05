#!/bin/bash
# Advanced Weather Data Pipeline v2.0 - Docker Build Script
# ===========================================================
# Optimized build script with latest Docker best practices

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="weather-data-pipeline"
VERSION="2.0.0"
REGISTRY="ghcr.io/jainam1673"
PLATFORMS="linux/amd64,linux/arm64"

# Build arguments
BUILDX_BUILDER="weather-builder"
CACHE_FROM="${REGISTRY}/${PROJECT_NAME}:cache"
CACHE_TO="${REGISTRY}/${PROJECT_NAME}:cache"

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed or not in PATH"
        exit 1
    fi
    
    # Check Docker version
    DOCKER_VERSION=$(docker --version | cut -d' ' -f3 | cut -d',' -f1)
    print_status "Docker version: $DOCKER_VERSION"
    
    # Check if buildx is available
    if ! docker buildx version &> /dev/null; then
        print_error "Docker Buildx is required but not available"
        exit 1
    fi
    
    # Check if uv is available (optional, for local builds)
    if command -v uv &> /dev/null; then
        UV_VERSION=$(uv --version)
        print_status "uv version: $UV_VERSION"
    else
        print_warning "uv not found locally (will use container version)"
    fi
    
    print_success "Prerequisites check passed"
}

# Function to setup buildx builder
setup_buildx() {
    print_status "Setting up buildx builder..."
    
    # Remove existing builder if it exists
    docker buildx rm "$BUILDX_BUILDER" 2>/dev/null || true
    
    # Create new builder with advanced features
    docker buildx create \
        --name "$BUILDX_BUILDER" \
        --driver docker-container \
        --driver-opt network=host \
        --use
    
    # Bootstrap the builder
    docker buildx inspect --bootstrap
    
    print_success "Buildx builder '$BUILDX_BUILDER' ready"
}

# Function to generate pyproject.toml if it doesn't exist
ensure_pyproject() {
    if [ ! -f "pyproject.toml" ]; then
        print_status "Generating pyproject.toml for uv..."
        
        # This would normally be created by the Dockerfile
        # but we can generate it here for local builds
        cat > pyproject.toml << 'EOF'
[project]
name = "weather-data-pipeline"
version = "2.0.0"
description = "Advanced Weather Data Pipeline with ML capabilities"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.104.1",
    "uvicorn[standard]>=0.24.0",
    "streamlit>=1.28.1",
    "pandas>=2.1.3",
    "numpy>=1.24.3",
    "plotly>=5.17.0",
    "requests>=2.31.0",
    "httpx>=0.25.2",
    "scikit-learn>=1.3.2",
    "scipy>=1.11.4",
    "python-dotenv>=1.0.0",
    "pydantic>=2.5.0",
    "structlog>=23.2.0",
    "python-multipart>=0.0.6",
    "gunicorn>=21.2.0"
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.uv]
dev-dependencies = [
    "pytest>=7.4.3",
    "pytest-asyncio>=0.21.1"
]
EOF
        print_success "pyproject.toml generated"
    fi
}

# Function to build development image
build_dev() {
    print_status "Building development image..."
    
    docker buildx build \
        --builder "$BUILDX_BUILDER" \
        --platform "$PLATFORMS" \
        --target development \
        --tag "${REGISTRY}/${PROJECT_NAME}:dev" \
        --tag "${REGISTRY}/${PROJECT_NAME}:dev-${VERSION}" \
        --cache-from "type=registry,ref=${CACHE_FROM}" \
        --cache-to "type=registry,ref=${CACHE_TO},mode=max" \
        --metadata-file /tmp/metadata-dev.json \
        --push \
        .
    
    print_success "Development image built and pushed"
}

# Function to build production images
build_prod() {
    print_status "Building production images..."
    
    # Build main production image
    docker buildx build \
        --builder "$BUILDX_BUILDER" \
        --platform "$PLATFORMS" \
        --target production \
        --tag "${REGISTRY}/${PROJECT_NAME}:latest" \
        --tag "${REGISTRY}/${PROJECT_NAME}:${VERSION}" \
        --tag "${REGISTRY}/${PROJECT_NAME}:prod" \
        --cache-from "type=registry,ref=${CACHE_FROM}" \
        --cache-to "type=registry,ref=${CACHE_TO},mode=max" \
        --metadata-file /tmp/metadata-prod.json \
        --push \
        .
    
    # Build API-specific image
    docker buildx build \
        --builder "$BUILDX_BUILDER" \
        --platform "$PLATFORMS" \
        --target api-server \
        --tag "${REGISTRY}/${PROJECT_NAME}:api" \
        --tag "${REGISTRY}/${PROJECT_NAME}:api-${VERSION}" \
        --cache-from "type=registry,ref=${CACHE_FROM}" \
        --push \
        .
    
    # Build Dashboard-specific image
    docker buildx build \
        --builder "$BUILDX_BUILDER" \
        --platform "$PLATFORMS" \
        --target dashboard \
        --tag "${REGISTRY}/${PROJECT_NAME}:dashboard" \
        --tag "${REGISTRY}/${PROJECT_NAME}:dashboard-${VERSION}" \
        --cache-from "type=registry,ref=${CACHE_FROM}" \
        --push \
        .
    
    # Build distroless image for ultra-minimal deployment
    docker buildx build \
        --builder "$BUILDX_BUILDER" \
        --platform "$PLATFORMS" \
        --target distroless \
        --tag "${REGISTRY}/${PROJECT_NAME}:distroless" \
        --tag "${REGISTRY}/${PROJECT_NAME}:distroless-${VERSION}" \
        --cache-from "type=registry,ref=${CACHE_FROM}" \
        --push \
        .
    
    print_success "Production images built and pushed"
}

# Function to run security scan
security_scan() {
    print_status "Running security scan with Docker Scout..."
    
    if ! command -v docker scout &> /dev/null; then
        print_warning "Docker Scout not available, skipping security scan"
        return
    fi
    
    # Scan the production image
    docker scout cves "${REGISTRY}/${PROJECT_NAME}:${VERSION}" || true
    docker scout quickview "${REGISTRY}/${PROJECT_NAME}:${VERSION}" || true
    
    print_success "Security scan completed"
}

# Function to generate SBOM
generate_sbom() {
    print_status "Generating Software Bill of Materials (SBOM)..."
    
    if ! command -v syft &> /dev/null; then
        print_warning "Syft not available, skipping SBOM generation"
        return
    fi
    
    syft "${REGISTRY}/${PROJECT_NAME}:${VERSION}" -o spdx-json=sbom.json
    syft "${REGISTRY}/${PROJECT_NAME}:${VERSION}" -o table=sbom.txt
    
    print_success "SBOM generated: sbom.json, sbom.txt"
}

# Function to test the built images
test_images() {
    print_status "Testing built images..."
    
    # Test API image
    print_status "Testing API image..."
    docker run --rm -d --name test-api -p 8001:8000 "${REGISTRY}/${PROJECT_NAME}:api"
    sleep 10
    
    if curl -f http://localhost:8001/health; then
        print_success "API image test passed"
    else
        print_error "API image test failed"
    fi
    
    docker stop test-api
    
    # Test production image
    print_status "Testing production image..."
    docker run --rm --name test-prod "${REGISTRY}/${PROJECT_NAME}:${VERSION}" python -c "import src; print('Production image OK')"
    
    print_success "Image tests completed"
}

# Function to cleanup
cleanup() {
    print_status "Cleaning up..."
    
    # Remove builder
    docker buildx rm "$BUILDX_BUILDER" 2>/dev/null || true
    
    # Clean up test containers
    docker stop test-api 2>/dev/null || true
    docker rm test-api 2>/dev/null || true
    
    # Prune build cache (optional)
    if [ "${CLEANUP_CACHE:-false}" = "true" ]; then
        docker buildx prune -f
    fi
    
    print_success "Cleanup completed"
}

# Function to show usage
usage() {
    cat << EOF
Usage: $0 [OPTIONS] [COMMAND]

Commands:
    dev         Build development image only
    prod        Build production images only
    all         Build all images (default)
    test        Test built images
    scan        Run security scan
    sbom        Generate SBOM
    clean       Cleanup build artifacts

Options:
    -h, --help          Show this help message
    -v, --version       Set version tag (default: $VERSION)
    -r, --registry      Set registry (default: $REGISTRY)
    -p, --platforms     Set platforms (default: $PLATFORMS)
    --no-cache          Disable build cache
    --push              Push images to registry
    --cleanup-cache     Clean up build cache after build

Examples:
    $0 all                          # Build all images
    $0 prod --push                  # Build and push production images
    $0 dev -v 2.1.0                # Build dev image with custom version
    $0 scan                         # Run security scan only

EOF
}

# Main function
main() {
    local command="all"
    local push=false
    local no_cache=false
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                usage
                exit 0
                ;;
            -v|--version)
                VERSION="$2"
                shift 2
                ;;
            -r|--registry)
                REGISTRY="$2"
                shift 2
                ;;
            -p|--platforms)
                PLATFORMS="$2"
                shift 2
                ;;
            --no-cache)
                no_cache=true
                shift
                ;;
            --push)
                push=true
                shift
                ;;
            --cleanup-cache)
                CLEANUP_CACHE=true
                shift
                ;;
            dev|prod|all|test|scan|sbom|clean)
                command="$1"
                shift
                ;;
            *)
                print_error "Unknown option: $1"
                usage
                exit 1
                ;;
        esac
    done
    
    # Set up trap for cleanup
    trap cleanup EXIT
    
    print_status "Starting build process for $PROJECT_NAME v$VERSION"
    print_status "Registry: $REGISTRY"
    print_status "Platforms: $PLATFORMS"
    print_status "Command: $command"
    
    # Execute based on command
    case $command in
        dev)
            check_prerequisites
            setup_buildx
            ensure_pyproject
            build_dev
            ;;
        prod)
            check_prerequisites
            setup_buildx
            ensure_pyproject
            build_prod
            ;;
        all)
            check_prerequisites
            setup_buildx
            ensure_pyproject
            build_dev
            build_prod
            ;;
        test)
            test_images
            ;;
        scan)
            security_scan
            ;;
        sbom)
            generate_sbom
            ;;
        clean)
            cleanup
            ;;
        *)
            print_error "Invalid command: $command"
            usage
            exit 1
            ;;
    esac
    
    print_success "Build process completed successfully!"
}

# Run main function with all arguments
main "$@"

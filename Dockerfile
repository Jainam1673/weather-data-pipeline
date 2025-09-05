# syntax=docker/dockerfile:1
# Advanced Weather Data Pipeline v2.0 - Production-Ready Multi-stage Docker Build
# ================================================================================
# Implements latest Docker best practices:
# - Multi-stage builds for minimal image size
# - Non-root user security
# - uv for ultra-fast package management
# - Proper layer caching optimization
# - Security hardening
# - Health checks
# - Distroless final stage option

# ===================================
# Stage 1: Base Environment with uv
# ===================================
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim AS base

# Pin specific uv version for reproducibility
# COPY --from=ghcr.io/astral-sh/uv:0.8.15 /uv /uvx /usr/local/bin/

# Set non-interactive mode for apt
ENV DEBIAN_FRONTEND=noninteractive

# Configure uv environment variables
ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_CACHE_DIR=/opt/uv-cache/ \
    UV_SYSTEM_PYTHON=1

# Configure Python environment variables  
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

# Create application user with specific UID/GID for consistency
RUN groupadd -r -g 1001 weather && \
    useradd --no-log-init -r -g weather -u 1001 -d /app weather

# Install system dependencies in a single layer
# Clean up in same layer to reduce image size
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create cache directory and set permissions
RUN mkdir -p /opt/uv-cache /app/logs /app/data && \
    chown -R weather:weather /opt/uv-cache /app

# Set working directory
WORKDIR /app

# ===================================
# Stage 2: Dependencies Builder
# ===================================
FROM base AS deps-builder

# Create pyproject.toml for uv project management
COPY <<EOF /app/pyproject.toml
[project]
name = "weather-data-pipeline"
version = "2.0.0"
description = "Advanced Weather Data Pipeline with ML capabilities"
readme = "README.md"
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

[project.optional-dependencies]
dev = [
    "pytest>=7.4.3",
    "pytest-asyncio>=0.21.1",
    "jupyter>=1.0.0",
    "notebook>=7.0.6"
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

# Install dependencies using uv with cache mount for better performance
RUN --mount=type=cache,target=/opt/uv-cache,uid=1001,gid=1001 \
    uv sync --no-install-project --compile-bytecode

# ===================================
# Stage 3: Development Environment
# ===================================
FROM base AS development

# Copy virtual environment from deps-builder
COPY --from=deps-builder --chown=weather:weather /app/.venv /app/.venv

# Copy source code
COPY --chown=weather:weather . /app/

# Activate virtual environment for all subsequent commands
ENV PATH="/app/.venv/bin:$PATH"

# Switch to non-root user
USER weather

# Expose ports for API and Dashboard
EXPOSE 8000 8501

# Development command with hot reload
CMD ["uvicorn", "src.api.server:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# ===================================
# Stage 4: Production Builder
# ===================================
FROM deps-builder AS prod-builder

# Copy source code and install project in non-editable mode
COPY --chown=weather:weather . /app/

# Install project with uv (skip local package install for script-based project)
RUN --mount=type=cache,target=/opt/uv-cache,uid=1001,gid=1001 \
    uv sync --no-install-project --no-dev --compile-bytecode

# ===================================
# Stage 5: Production Runtime
# ===================================
FROM base AS production

# Copy virtual environment from prod-builder
COPY --from=prod-builder --chown=weather:weather /app/.venv /app/.venv

# Copy application code (source is already in .venv due to non-editable install)
COPY --chown=weather:weather src/ /app/src/
COPY --chown=weather:weather main.py /app/
COPY --chown=weather:weather README.md /app/

# Add metadata labels for better image management
LABEL org.opencontainers.image.title="Advanced Weather Data Pipeline"
LABEL org.opencontainers.image.description="Production-ready weather data processing pipeline with ML capabilities"
LABEL org.opencontainers.image.version="2.0.0"
LABEL org.opencontainers.image.vendor="Weather Data Pipeline Project"
LABEL org.opencontainers.image.authors="Jainam Jadav"
LABEL org.opencontainers.image.source="https://github.com/Jainam1673/weather-data-pipeline"
LABEL org.opencontainers.image.documentation="https://github.com/Jainam1673/weather-data-pipeline/blob/main/README.md"

# Activate virtual environment for all subsequent commands
ENV PATH="/app/.venv/bin:$PATH"

# Switch to non-root user
USER weather

# Create volume for persistent data
VOLUME ["/app/data", "/app/logs"]

# Health check with proper timeout and retry logic
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Default production command with optimized gunicorn settings
CMD ["gunicorn", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "4", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--worker-connections", "1000", \
     "--max-requests", "1000", \
     "--max-requests-jitter", "100", \
     "--preload", \
     "--timeout", "30", \
     "--keep-alive", "2", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "src.api.server:app"]

# ===================================
# Stage 6: API-only Production
# ===================================
FROM production AS api-server

# Override for API-only service
EXPOSE 8000

# Optimized API-only command
CMD ["python", "main.py", "api"]

# ===================================
# Stage 7: Dashboard-only Production
# ===================================
FROM production AS dashboard

# Override for dashboard-only service
EXPOSE 8501

# Configure Streamlit for production
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_ENABLE_CORS=false
ENV STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false

# Dashboard-only command
CMD ["python", "main.py", "dashboard"]

# ===================================
# Stage 8: Distroless Production (Ultra-minimal)
# ===================================
FROM gcr.io/distroless/python3-debian12:latest AS distroless

# Copy virtual environment and application
COPY --from=prod-builder --chown=1001:1001 /app/.venv /app/.venv
COPY --from=prod-builder --chown=1001:1001 /app/src /app/src
COPY --from=prod-builder --chown=1001:1001 /app/main.py /app/

# Set environment
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app"

# Switch to non-root user
USER 1001

# Minimal command for distroless
ENTRYPOINT ["python", "/app/main.py"]
CMD ["api"]

# Advanced Weather Data Pipeline v2.0 - Multi-stage Docker Build
# ==============================================================

# Stage 1: Base Python Environment
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Create working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Stage 2: Development Environment
FROM base as development

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose ports for API and Dashboard
EXPOSE 8000 8501

# Development command
CMD ["python", "main.py", "api"]

# Stage 3: Production Environment
FROM base as production

# Create non-root user
RUN useradd --create-home --shell /bin/bash weather

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY --chown=weather:weather src/ /app/src/
COPY --chown=weather:weather main.py /app/
COPY --chown=weather:weather README.md /app/

# Create directories
RUN mkdir -p /app/logs /app/data && \
    chown -R weather:weather /app

# Switch to non-root user
USER weather

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Production command
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "src.api.server:app"]

# Stage 4: API-only Production
FROM production as api-server
EXPOSE 8000
CMD ["python", "main.py", "api"]

# Stage 5: Dashboard-only Production  
FROM production as dashboard
EXPOSE 8501
CMD ["python", "main.py", "dashboard"]

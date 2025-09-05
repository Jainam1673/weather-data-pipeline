# Docker Deployment Guide - Advanced Weather Data Pipeline v2.0

## 🐳 Modern Docker Setup with Latest Best Practices

This deployment uses the latest Docker best practices including:

- **uv** for ultra-fast Python package management (10-100x faster than pip)
- **Multi-stage builds** for minimal production images
- **Security hardening** with non-root users and read-only containers
- **Layer caching optimization** for faster builds
- **Distroless images** for ultimate security and minimal attack surface
- **Health checks** and proper resource limits
- **Multi-platform builds** (AMD64 + ARM64)

## 🏗️ Build Targets

| Target | Purpose | Size | Security |
|--------|---------|------|----------|
| `base` | Common base with uv | ~200MB | Medium |
| `development` | Hot reload, debugging | ~500MB | Low |
| `production` | Full production runtime | ~300MB | High |
| `api-server` | API-only service | ~300MB | High |
| `dashboard` | Dashboard-only service | ~350MB | High |
| `distroless` | Ultra-minimal runtime | ~150MB | Maximum |

## 🚀 Quick Start

### Development
```bash
# Start development environment with hot reload
docker-compose up

# Access services:
# - API: http://localhost:8000
# - Dashboard: http://localhost:8501
# - Jupyter: http://localhost:8888 (token: weather-dev-token)
# - DB Browser: http://localhost:8080
```

### Production
```bash
# Start production environment
docker-compose -f docker-compose.yml up -d

# Or use the production configuration
docker-compose -f docker-compose.prod.yml up -d
```

## 🔧 Build Script

Use the advanced build script for optimized builds:

```bash
# Build all images
./build.sh all

# Build development only
./build.sh dev

# Build production with push
./build.sh prod --push

# Build with custom version
./build.sh all -v 2.1.0

# Run security scan
./build.sh scan

# Generate SBOM (Software Bill of Materials)
./build.sh sbom
```

## 📦 uv Package Manager Benefits

Our Docker setup uses **uv** instead of pip for:

- **10-100x faster** package installation
- **Better dependency resolution** with proper conflict detection  
- **Smaller images** with optimized virtual environments
- **Reproducible builds** with lockfile support
- **Cache efficiency** with advanced caching strategies

### uv vs pip Comparison

| Feature | uv | pip |
|---------|----|----|
| Speed | 10-100x faster | Baseline |
| Dependency resolution | Advanced | Basic |
| Lockfile support | Native | External tool needed |
| Cache efficiency | Excellent | Poor |
| Memory usage | Low | High |

## 🐋 Docker Compose Configurations

### Development (`docker-compose.override.yml`)
- Automatic hot reload
- Volume mounts for source code
- Debug mode enabled
- Jupyter and DB browser included
- Relaxed security for development

### Production (`docker-compose.prod.yml`)
- Resource limits and security hardening
- Health checks and monitoring
- Nginx load balancer
- Prometheus and Grafana for observability
- Proper secrets management

## 🔒 Security Features

### Container Security
- **Non-root user** (UID/GID 1001)
- **Read-only filesystem** for production
- **No new privileges** security option
- **Specific resource limits**
- **Minimal attack surface** with distroless option

### Image Security
- **Pinned base image versions** for reproducibility
- **No unnecessary packages** installed
- **Security scanning** with Docker Scout
- **SBOM generation** for supply chain security
- **Signature verification** support

## 🏗️ Advanced Build Features

### Multi-stage Optimization
```dockerfile
# Dependency caching layer
FROM base AS deps-builder
RUN uv sync --locked --no-install-project

# Production build layer  
FROM deps-builder AS prod-builder
RUN uv sync --locked --no-editable --compile-bytecode

# Minimal runtime layer
FROM base AS production
COPY --from=prod-builder /app/.venv /app/.venv
```

### Layer Caching
- Dependencies installed in separate layer
- Source code copied after dependencies
- Cache mounts for uv cache directory
- Build cache reused across builds

### Multi-platform Support
```bash
# Build for multiple architectures
docker buildx build --platform linux/amd64,linux/arm64 .
```

## 📊 Resource Management

### Development Limits
```yaml
resources:
  limits:
    cpus: '4.0'
    memory: 4G
  reservations:
    cpus: '0.1'
    memory: 128M
```

### Production Limits
```yaml
resources:
  limits:
    cpus: '1.0'
    memory: 1G
  reservations:
    cpus: '0.25'
    memory: 256M
```

## 🔍 Health Checks

All services include comprehensive health checks:

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 60s
```

## 📈 Monitoring and Observability

Production setup includes:

- **Prometheus** for metrics collection
- **Grafana** for visualization
- **Loki** for log aggregation
- **Nginx** for load balancing and SSL termination

## 🚢 Deployment Options

### Local Development
```bash
docker-compose up
```

### Staging/Production
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Kubernetes (with Helm)
```bash
helm install weather-pipeline ./helm/
```

### Docker Swarm
```bash
docker stack deploy -c docker-compose.prod.yml weather
```

## 🔧 Configuration

### Environment Variables
- `ENVIRONMENT`: `development` | `production`
- `DEBUG`: Enable debug mode
- `LOG_LEVEL`: Logging level
- `WORKERS`: Number of gunicorn workers
- `MAX_REQUESTS`: Max requests per worker

### Volume Mounts
- `/app/data`: Persistent data storage
- `/app/logs`: Application logs
- `/opt/uv-cache`: Package cache (development)

## 🐛 Troubleshooting

### Common Issues

1. **Build fails with uv error**
   ```bash
   # Clear cache and rebuild
   docker builder prune
   ./build.sh all --no-cache
   ```

2. **Permission denied errors**
   ```bash
   # Fix ownership
   sudo chown -R $USER:$USER data/ logs/
   ```

3. **Out of memory during build**
   ```bash
   # Increase Docker memory limit
   # Docker Desktop: Settings > Resources > Memory
   ```

### Debug Commands
```bash
# Check container logs
docker-compose logs weather-api

# Execute into running container
docker-compose exec weather-api bash

# Check health status
docker-compose ps

# Inspect image layers
docker history weather-data-pipeline:latest
```

## 📚 References

- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [uv Documentation](https://docs.astral.sh/uv/)
- [Multi-stage Builds](https://docs.docker.com/build/building/multi-stage/)
- [Distroless Images](https://github.com/GoogleContainerTools/distroless)
- [Docker Security](https://docs.docker.com/engine/security/)

---

## 🎯 Next Steps

1. Set up CI/CD pipeline for automated builds
2. Configure monitoring and alerting
3. Implement automated security scanning
4. Set up Kubernetes deployment
5. Configure backup and disaster recovery

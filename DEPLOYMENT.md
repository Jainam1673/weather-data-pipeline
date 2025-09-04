# 🚀 Deployment Guide

This guide covers various deployment options for the Mojo Weather Data Pipeline.

## 📋 Prerequisites

Before deploying, ensure you have:

- **Git** installed
- **Internet connection** for Open-Meteo API
- **Appropriate hardware** (see requirements below)

## 🖥️ System Requirements

### Minimum Requirements
- **OS**: Linux (Ubuntu 20.04+), macOS (12.0+)
- **CPU**: 2 cores, x86_64 or ARM64
- **RAM**: 4GB
- **Storage**: 2GB free space
- **Network**: Stable internet connection

### Recommended Requirements
- **OS**: Linux (Ubuntu 22.04+), macOS (14.0+)
- **CPU**: 4+ cores, x86_64 with AVX2 support
- **RAM**: 8GB+
- **Storage**: 5GB+ free space (SSD preferred)
- **Network**: High-speed internet connection

## 🏠 Local Development Deployment

### Quick Setup
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/mojo-weather-pipeline.git
cd mojo-weather-pipeline

# Run automated setup
./setup.sh

# Start the pipeline
./start_pipeline.sh
```

### Manual Setup
```bash
# Install Pixi (if not already installed)
curl -fsSL https://pixi.sh/install.sh | bash

# Install dependencies
pixi install

# Initialize database
pixi run python -c "from database import WeatherDatabase; WeatherDatabase()"

# Start services
pixi run python api.py &
pixi run streamlit run streamlit_app.py
```

### Access Points
- **Dashboard**: http://localhost:8501
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## ☁️ Cloud Deployment

### Docker Deployment (Recommended)

1. **Create Dockerfile**:
```dockerfile
FROM ubuntu:22.04

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install Pixi
RUN curl -fsSL https://pixi.sh/install.sh | bash
ENV PATH="/root/.pixi/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pixi install

# Expose ports
EXPOSE 8000 8501

# Start command
CMD ["./start_pipeline.sh"]
```

2. **Build and run**:
```bash
# Build image
docker build -t mojo-weather-pipeline .

# Run container
docker run -p 8000:8000 -p 8501:8501 mojo-weather-pipeline
```

### Docker Compose
```yaml
version: '3.8'

services:
  weather-pipeline:
    build: .
    ports:
      - "8000:8000"
      - "8501:8501"
    volumes:
      - weather_data:/app/data
      - weather_logs:/app/logs
    environment:
      - ENVIRONMENT=production
    restart: unless-stopped

volumes:
  weather_data:
  weather_logs:
```

### AWS EC2 Deployment

1. **Launch EC2 Instance**:
   - **AMI**: Ubuntu 22.04 LTS
   - **Instance Type**: t3.medium (minimum), t3.large (recommended)
   - **Security Group**: Allow ports 22, 8000, 8501

2. **Setup on EC2**:
```bash
# Connect to EC2
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Clone and setup
git clone https://github.com/YOUR_USERNAME/mojo-weather-pipeline.git
cd mojo-weather-pipeline
./setup.sh

# Start with systemd (optional)
sudo cp deployment/weather-pipeline.service /etc/systemd/system/
sudo systemctl enable weather-pipeline
sudo systemctl start weather-pipeline
```

3. **Access**: http://your-ec2-ip:8501

### Google Cloud Platform

1. **Create VM Instance**:
```bash
gcloud compute instances create weather-pipeline \
    --zone=us-central1-a \
    --machine-type=e2-medium \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=20GB
```

2. **Deploy application**:
```bash
# SSH to instance
gcloud compute ssh weather-pipeline

# Setup application
git clone https://github.com/YOUR_USERNAME/mojo-weather-pipeline.git
cd mojo-weather-pipeline
./setup.sh
./start_pipeline.sh
```

### Azure Container Instances

```bash
# Create resource group
az group create --name weather-pipeline-rg --location eastus

# Deploy container
az container create \
    --resource-group weather-pipeline-rg \
    --name weather-pipeline \
    --image your-dockerhub-username/mojo-weather-pipeline \
    --ports 8000 8501 \
    --dns-name-label weather-pipeline-unique \
    --cpu 2 \
    --memory 4
```

## 🔧 Production Configuration

### Environment Variables
```bash
# Optional configuration
export WEATHER_DB_PATH="/data/weather_data.db"
export API_HOST="0.0.0.0"
export API_PORT="8000"
export STREAMLIT_PORT="8501"
export LOG_LEVEL="INFO"
```

### Reverse Proxy (Nginx)
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### SSL/HTTPS (Certbot)
```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo certbot renew --dry-run
```

## 📊 Monitoring & Logging

### Health Checks
```bash
# API health
curl http://localhost:8000/health

# System metrics
curl http://localhost:8000/system/metrics
```

### Log Management
```bash
# View logs
tail -f logs/api.log
tail -f logs/streamlit.log

# Log rotation (logrotate)
sudo vim /etc/logrotate.d/weather-pipeline
```

### Performance Monitoring
```bash
# Monitor resource usage
htop
iotop
netstat -tlnp
```

## 🔒 Security Considerations

### Network Security
- **Firewall**: Only open necessary ports (22, 80, 443)
- **VPN**: Consider VPN access for admin functions
- **Load Balancer**: Use cloud load balancers for high availability

### Application Security
- **Regular Updates**: Keep dependencies updated
- **Input Validation**: All inputs are validated
- **Rate Limiting**: Implement API rate limiting
- **HTTPS**: Always use HTTPS in production

### Data Security
- **Backup**: Regular database backups
- **Encryption**: Encrypt data at rest if needed
- **Access Control**: Limit database access

## 🚀 Scaling Strategies

### Horizontal Scaling
```yaml
# Kubernetes deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: weather-pipeline
spec:
  replicas: 3
  selector:
    matchLabels:
      app: weather-pipeline
  template:
    metadata:
      labels:
        app: weather-pipeline
    spec:
      containers:
      - name: weather-pipeline
        image: your-registry/mojo-weather-pipeline:latest
        ports:
        - containerPort: 8000
        - containerPort: 8501
```

### Database Scaling
- **Read Replicas**: For read-heavy workloads
- **Sharding**: For large datasets
- **Caching**: Redis/Memcached for frequent queries

### Performance Optimization
- **CDN**: Use CDN for static assets
- **Caching**: Implement application-level caching
- **Database Optimization**: Index optimization
- **Mojo Optimization**: SIMD and vectorization

## 🔄 Backup & Recovery

### Database Backup
```bash
# Backup SQLite database
cp weather_data.db weather_data_backup_$(date +%Y%m%d).db

# Automated backup script
#!/bin/bash
BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
cp weather_data.db "$BACKUP_DIR/weather_data_$DATE.db"
find "$BACKUP_DIR" -name "weather_data_*.db" -mtime +7 -delete
```

### Configuration Backup
```bash
# Backup configuration files
tar -czf config_backup_$(date +%Y%m%d).tar.gz \
    pixi.toml \
    *.sh \
    *.py \
    README.md
```

## 📈 Performance Tuning

### Mojo Optimizations
- Enable all SIMD optimizations
- Use appropriate data types
- Optimize memory allocation

### Database Tuning
```sql
-- Create indexes for better performance
CREATE INDEX idx_weather_timestamp ON weather_data(timestamp);
CREATE INDEX idx_weather_temperature ON weather_data(temperature);
```

### API Optimization
- Enable async processing
- Implement connection pooling
- Use appropriate timeout values

## 🛠️ Troubleshooting

### Common Issues

1. **Port already in use**:
```bash
sudo lsof -i :8000
sudo lsof -i :8501
```

2. **Mojo not found**:
```bash
pixi run mojo --version
pixi install
```

3. **Database locked**:
```bash
fuser weather_data.db
# Kill processes using the database
```

4. **API connection errors**:
```bash
# Check Open-Meteo API status
curl "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m"
```

### Support Resources
- **GitHub Issues**: Report bugs and issues
- **Documentation**: Check README and guides
- **Community**: GitHub Discussions
- **Logs**: Check application logs

---

**For additional deployment support, please check our [GitHub Issues](https://github.com/YOUR_USERNAME/mojo-weather-pipeline/issues) or create a new issue.**

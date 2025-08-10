# Blog-Poster Deployment Guide

## 📋 Prerequisites

### System Requirements
- **OS**: Ubuntu 20.04+ / macOS 12+ / Windows WSL2
- **Docker**: 20.10+
- **Docker Compose**: 2.0+
- **Memory**: 4GB minimum, 8GB recommended
- **Storage**: 10GB minimum for containers and data
- **CPU**: 2 cores minimum, 4 cores recommended

### Required API Keys
- **Anthropic API Key** OR **OpenAI API Key** (for LLM generation)
- **Jina API Key** (for web scraping)
- **WordPress Credentials** (admin user with publishing rights)

---

## 🚀 Local Development Deployment

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/blog-poster.git
cd blog-poster
```

### Step 2: Configure Environment
```bash
# Copy example environment file
cp .env.example .env.local

# Edit with your credentials
nano .env.local
```

Required `.env.local` configuration:
```env
# AI Provider (at least one required)
ANTHROPIC_API_KEY=sk-ant-api03-...
# OR
OPENAI_API_KEY=sk-...

# Web Scraping
JINA_API_KEY=jina_...

# WordPress Configuration
WORDPRESS_URL=http://localhost:8084
WORDPRESS_ADMIN_USER=admin
WORDPRESS_ADMIN_PASSWORD=your-password

# Local Development Settings
WP_VERIFY_SSL=false
DEBUG=true
```

### Step 3: Start Services
```bash
# Start all services with build
docker compose up -d --build

# Watch logs
docker compose logs -f api

# Verify all services are running
docker compose ps
```

### Step 4: Verify Installation
```bash
# Check API health
curl http://localhost:8088/health

# Test WordPress connection
curl http://localhost:8088/wordpress/test

# Check Qdrant vector database
curl http://localhost:6333/collections
```

### Step 5: Run Test Pipeline
```python
# test_deployment.py
import requests

# Test article generation
response = requests.post(
    "http://localhost:8088/article/generate",
    json={
        "topic": "Test Article",
        "primary_keyword": "test"
    }
)
print("Article generation:", response.status_code)

# Test vector search
response = requests.post(
    "http://localhost:8088/vector/search",
    json={
        "query": "service dogs",
        "limit": 5
    }
)
print("Vector search:", response.status_code)
```

---

## 🌐 Production Deployment

### Option 1: Docker Compose (Single Server)

#### Step 1: Server Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

#### Step 2: Deploy Application
```bash
# Clone repository
git clone https://github.com/yourusername/blog-poster.git
cd blog-poster

# Create production environment file
cp .env.example .env.production
nano .env.production
```

Production `.env.production`:
```env
# Production Settings
NODE_ENV=production
DEBUG=false

# AI Provider
ANTHROPIC_API_KEY=sk-ant-api03-...

# Web Scraping
JINA_API_KEY=jina_...

# WordPress Production
WORDPRESS_URL=https://yoursite.com
WORDPRESS_ADMIN_USER=admin
WORDPRESS_ADMIN_PASSWORD=secure-password
WP_VERIFY_SSL=true

# Security
API_KEY=your-secure-api-key
ALLOWED_ORIGINS=https://yoursite.com

# Cost Management
MAX_COST_PER_ARTICLE=0.50
MAX_MONTHLY_COST=100.00

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=500
```

#### Step 3: Production Docker Compose
Create `docker-compose.prod.yml`:
```yaml
services:
  api:
    image: blog-poster-api:latest
    container_name: blog-api
    restart: always
    env_file:
      - .env.production
    environment:
      VECTOR_BACKEND: qdrant
      QDRANT_URL: http://qdrant:6333
    ports:
      - "127.0.0.1:8088:8088"  # Only expose to localhost
    depends_on:
      - qdrant
      - vectors
      - redis
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8088/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  qdrant:
    image: qdrant/qdrant:latest
    container_name: blog-qdrant
    restart: always
    ports:
      - "127.0.0.1:6333:6333"
    volumes:
      - qdrant_storage:/qdrant/storage
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  vectors:
    image: pgvector/pgvector:pg16
    container_name: blog-vectors
    restart: always
    environment:
      POSTGRES_DB: vectors
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    ports:
      - "127.0.0.1:5433:5432"
    volumes:
      - pg_data:/var/lib/postgresql/data
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  redis:
    image: redis:7-alpine
    container_name: blog-redis
    restart: always
    command: ["redis-server", "--appendonly", "yes", "--requirepass", "${REDIS_PASSWORD}"]
    ports:
      - "127.0.0.1:6384:6379"
    volumes:
      - redis_data:/data
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

volumes:
  qdrant_storage:
  pg_data:
  redis_data:
```

#### Step 4: Deploy with Docker Compose
```bash
# Build production image
docker build -t blog-poster-api:latest .

# Start production services
docker compose -f docker-compose.prod.yml up -d

# Check status
docker compose -f docker-compose.prod.yml ps

# View logs
docker compose -f docker-compose.prod.yml logs -f
```

#### Step 5: Setup Nginx Reverse Proxy
```nginx
# /etc/nginx/sites-available/blog-poster
server {
    listen 80;
    server_name api.yoursite.com;
    
    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.yoursite.com;
    
    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/api.yoursite.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.yoursite.com/privkey.pem;
    
    # Security Headers
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options DENY;
    add_header X-XSS-Protection "1; mode=block";
    
    # Rate Limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req zone=api burst=20 nodelay;
    
    location / {
        proxy_pass http://127.0.0.1:8088;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts for long-running requests
        proxy_connect_timeout 60s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/blog-poster /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Option 2: Kubernetes Deployment

#### Kubernetes Manifests
Create `k8s/deployment.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: blog-poster-api
spec:
  replicas: 2
  selector:
    matchLabels:
      app: blog-poster-api
  template:
    metadata:
      labels:
        app: blog-poster-api
    spec:
      containers:
      - name: api
        image: blog-poster-api:latest
        ports:
        - containerPort: 8088
        env:
        - name: VECTOR_BACKEND
          value: qdrant
        - name: QDRANT_URL
          value: http://qdrant-service:6333
        envFrom:
        - secretRef:
            name: blog-poster-secrets
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8088
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 8088
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: blog-poster-api-service
spec:
  selector:
    app: blog-poster-api
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8088
  type: LoadBalancer
```

#### Deploy to Kubernetes
```bash
# Create namespace
kubectl create namespace blog-poster

# Create secrets
kubectl create secret generic blog-poster-secrets \
  --from-env-file=.env.production \
  -n blog-poster

# Apply manifests
kubectl apply -f k8s/ -n blog-poster

# Check status
kubectl get pods -n blog-poster
kubectl get services -n blog-poster
```

### Option 3: Cloud Platform Deployment

#### AWS ECS Deployment
```bash
# Build and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $ECR_REGISTRY
docker build -t blog-poster-api .
docker tag blog-poster-api:latest $ECR_REGISTRY/blog-poster-api:latest
docker push $ECR_REGISTRY/blog-poster-api:latest

# Deploy with ECS CLI
ecs-cli compose --file docker-compose.prod.yml up --cluster blog-poster-cluster
```

#### Google Cloud Run
```bash
# Build and push to GCR
gcloud builds submit --tag gcr.io/$PROJECT_ID/blog-poster-api

# Deploy to Cloud Run
gcloud run deploy blog-poster-api \
  --image gcr.io/$PROJECT_ID/blog-poster-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="VECTOR_BACKEND=qdrant" \
  --set-secrets="ANTHROPIC_API_KEY=anthropic-key:latest"
```

#### Azure Container Instances
```bash
# Create resource group
az group create --name blog-poster-rg --location eastus

# Create container instance
az container create \
  --resource-group blog-poster-rg \
  --name blog-poster-api \
  --image blog-poster-api:latest \
  --dns-name-label blog-poster-api \
  --ports 8088 \
  --environment-variables VECTOR_BACKEND=qdrant \
  --secure-environment-variables ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY
```

---

## 🔒 Security Configuration

### SSL/TLS Setup
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Generate certificate
sudo certbot --nginx -d api.yoursite.com

# Auto-renewal
sudo systemctl enable certbot.timer
```

### Firewall Configuration
```bash
# UFW setup
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### API Authentication
Add to `.env.production`:
```env
# API Security
API_KEY_REQUIRED=true
API_KEYS=key1,key2,key3  # Comma-separated list
JWT_SECRET=your-jwt-secret
JWT_EXPIRY=3600  # seconds
```

### Rate Limiting
Configure in `app.py`:
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100 per minute", "1000 per hour"]
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
```

---

## 📊 Monitoring & Logging

### Prometheus Setup
```yaml
# docker-compose.monitoring.yml
services:
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    ports:
      - "9090:9090"
    
  grafana:
    image: grafana/grafana:latest
    volumes:
      - grafana_data:/var/lib/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
```

### Logging with ELK Stack
```yaml
# docker-compose.logging.yml
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
    environment:
      - discovery.type=single-node
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    volumes:
      - es_data:/usr/share/elasticsearch/data
    ports:
      - "9200:9200"
  
  kibana:
    image: docker.elastic.co/kibana/kibana:8.11.0
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    ports:
      - "5601:5601"
  
  filebeat:
    image: docker.elastic.co/beats/filebeat:8.11.0
    volumes:
      - ./filebeat.yml:/usr/share/filebeat/filebeat.yml
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
      - /var/run/docker.sock:/var/run/docker.sock:ro
```

### Health Checks
```bash
# Create health check script
cat > health_check.sh << 'EOF'
#!/bin/bash

# Check API
if ! curl -f http://localhost:8088/health > /dev/null 2>&1; then
  echo "API health check failed"
  exit 1
fi

# Check Qdrant
if ! curl -f http://localhost:6333/health > /dev/null 2>&1; then
  echo "Qdrant health check failed"
  exit 1
fi

# Check Redis
if ! redis-cli -p 6384 ping > /dev/null 2>&1; then
  echo "Redis health check failed"
  exit 1
fi

echo "All services healthy"
EOF

chmod +x health_check.sh

# Add to crontab
crontab -e
# Add: */5 * * * * /path/to/health_check.sh || systemctl restart docker
```

---

## 🔄 Backup & Recovery

### Automated Backups
```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backups/blog-poster/$(date +%Y%m%d)"
mkdir -p $BACKUP_DIR

# Backup Qdrant
docker exec blog-qdrant qdrant-backup create /qdrant/backup
docker cp blog-qdrant:/qdrant/backup $BACKUP_DIR/qdrant

# Backup PostgreSQL
docker exec blog-vectors pg_dump -U postgres vectors > $BACKUP_DIR/vectors.sql

# Backup Redis
docker exec blog-redis redis-cli --rdb /data/backup.rdb
docker cp blog-redis:/data/backup.rdb $BACKUP_DIR/redis.rdb

# Compress
tar -czf $BACKUP_DIR.tar.gz $BACKUP_DIR
rm -rf $BACKUP_DIR

# Upload to S3 (optional)
aws s3 cp $BACKUP_DIR.tar.gz s3://your-backup-bucket/blog-poster/

# Keep only last 7 days
find /backups/blog-poster -name "*.tar.gz" -mtime +7 -delete
```

### Recovery Process
```bash
#!/bin/bash
# restore.sh

BACKUP_FILE=$1
RESTORE_DIR="/tmp/restore"

# Extract backup
tar -xzf $BACKUP_FILE -C /tmp
BACKUP_DIR=$(tar -tzf $BACKUP_FILE | head -1 | cut -f1 -d"/")

# Restore Qdrant
docker cp $RESTORE_DIR/$BACKUP_DIR/qdrant blog-qdrant:/qdrant/restore
docker exec blog-qdrant qdrant-backup restore /qdrant/restore

# Restore PostgreSQL
docker exec -i blog-vectors psql -U postgres vectors < $RESTORE_DIR/$BACKUP_DIR/vectors.sql

# Restore Redis
docker cp $RESTORE_DIR/$BACKUP_DIR/redis.rdb blog-redis:/data/dump.rdb
docker restart blog-redis

echo "Restoration complete"
```

---

## 🚨 Troubleshooting

### Common Issues

#### 1. Container won't start
```bash
# Check logs
docker compose logs api

# Common fixes:
# - Check environment variables
# - Verify port availability: netstat -tulpn | grep 8088
# - Check disk space: df -h
```

#### 2. WordPress connection fails
```bash
# Test connection
curl -u admin:password https://yoursite.com/wp-json/wp/v2/posts

# Common fixes:
# - Verify WordPress REST API is enabled
# - Check authentication plugin installed
# - Verify SSL certificate if using HTTPS
```

#### 3. Vector search not working
```bash
# Check Qdrant status
curl http://localhost:6333/collections

# Rebuild collections
docker exec blog-api python scripts/rebuild_vectors.py
```

#### 4. High memory usage
```bash
# Check memory usage
docker stats

# Limit container memory
docker update --memory="1g" --memory-swap="2g" blog-api
```

### Debug Mode
Enable debug logging:
```env
# .env.local
DEBUG=true
LOG_LEVEL=DEBUG
```

Check logs:
```bash
docker compose logs -f --tail=100 api
```

---

## 📈 Performance Tuning

### API Optimization
```python
# Use connection pooling
from databases import Database

database = Database(
    DATABASE_URL,
    min_size=5,
    max_size=20,
    command_timeout=60
)
```

### Qdrant Optimization
```yaml
# qdrant_config.yaml
storage:
  performance:
    max_optimization_threads: 4
  optimizers:
    indexing_threshold: 10000
```

### Redis Optimization
```conf
# redis.conf
maxmemory 256mb
maxmemory-policy allkeys-lru
save 900 1
save 300 10
```

---

## 🎯 Production Checklist

### Pre-Deployment
- [ ] All environment variables configured
- [ ] API keys secured in secrets management
- [ ] SSL certificates installed
- [ ] Firewall rules configured
- [ ] Backup strategy implemented

### Post-Deployment
- [ ] Health checks passing
- [ ] Monitoring dashboards configured
- [ ] Log aggregation working
- [ ] Alerts configured
- [ ] Performance baseline established

### Maintenance
- [ ] Weekly backup verification
- [ ] Monthly security updates
- [ ] Quarterly performance review
- [ ] Annual disaster recovery test

---

## 📞 Support

### Getting Help
- GitHub Issues: [github.com/yourusername/blog-poster/issues](https://github.com/yourusername/blog-poster/issues)
- Documentation: [docs/](./docs/)
- Discord: [discord.gg/blog-poster](https://discord.gg/blog-poster)

### Logs Location
- API Logs: `/var/log/blog-poster/api.log`
- Docker Logs: `docker compose logs`
- System Logs: `/var/log/syslog`

### Emergency Rollback
```bash
# Quick rollback to previous version
docker compose down
git checkout tags/v1.0.0
docker compose up -d --build
```
# Infrastructure Setup for Self-Hosted Server

## Overview

Before deploying any applications to the self-hosted server, you need to set up the foundational infrastructure. This is a **one-time setup** per server.

## Prerequisites

- Docker and Docker Compose installed on self-hosted server
- DNS pointed to your server
- Ports 80 and 443 open

## Step 1: Infrastructure Setup (One-Time)

Deploy the reverse proxy infrastructure **before** adding any application stacks to Portainer:

```bash
# On your self-hosted server
docker compose -f docker-compose.nginx-proxy.yml up -d
```

This creates:
- **nginx-proxy**: Automatic reverse proxy for Docker containers
- **letsencrypt**: SSL certificate management
- **reverse-proxy-network**: External network for applications

## Step 2: Verify Infrastructure

```bash
# Check containers are running
docker ps --filter "name=nginx-proxy"
docker ps --filter "name=nginx-letsencrypt"

# Check network exists
docker network ls | grep reverse-proxy-network
```

## Step 3: Deploy Applications via Portainer

Once infrastructure is running, you can deploy application stacks through Portainer that will automatically connect to the reverse proxy network.

## Important Notes

1. **Deploy infrastructure FIRST** - Applications depend on the reverse-proxy-network
2. **One-time setup** - You typically never need to touch this again
3. **SSL automatic** - Let's Encrypt will automatically handle SSL certificates
4. **Domain routing** - Applications use labels to configure automatic routing

## Application Integration

Your application `docker-compose.yml` files should:

```yaml
networks:
  reverse-proxy-network:
    external: true
    name: reverse-proxy-network

services:
  app:
    labels:
      - "proxy.domain=your-app.yourdomain.com"
      - "proxy.port=3000"
    networks:
      - reverse-proxy-network
```

## Troubleshooting

```bash
# Check nginx-proxy logs
docker logs nginx-proxy

# Check letsencrypt logs  
docker logs nginx-letsencrypt

# Restart if needed
docker compose -f docker-compose.nginx-proxy.yml restart
```

This infrastructure setup enables automatic SSL and domain routing for all applications deployed to your self-hosted server.
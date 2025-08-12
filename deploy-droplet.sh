#!/bin/bash

# Blog Poster - Digital Ocean Droplet Deployment Script
# This script deploys the blog-poster to a Digital Ocean Droplet
# Prerequisites: 
# - doctl CLI installed and authenticated
# - SSH key added to Digital Ocean account

set -e

echo "🚀 Blog Poster - Digital Ocean Droplet Deployment"
echo "=================================================="
echo ""

# Configuration
DROPLET_NAME="blog-poster-staging"
REGION="nyc3"
SIZE="s-2vcpu-4gb"  # $24/month
IMAGE="docker-20-04"  # Ubuntu 20.04 with Docker pre-installed
SSH_KEY_NAME="blog-poster-key"
DOMAIN="blog-staging.servicedogus.com"  # Optional: your domain

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if doctl is installed
if ! command -v doctl &> /dev/null; then
    echo -e "${RED}❌ Error: doctl CLI is not installed${NC}"
    echo "Install it with: brew install doctl"
    exit 1
fi

# Verify authentication
echo "📋 Checking Digital Ocean authentication..."
if ! doctl account get &> /dev/null; then
    echo -e "${RED}❌ Error: Not authenticated with Digital Ocean${NC}"
    echo "Run: doctl auth init"
    exit 1
fi

ACCOUNT_EMAIL=$(doctl account get --format Email --no-header)
echo -e "${GREEN}✅ Authenticated as: $ACCOUNT_EMAIL${NC}"
echo ""

# Check for existing droplet
EXISTING_DROPLET=$(doctl compute droplet list --format Name,ID --no-header | grep "^${DROPLET_NAME}" | awk '{print $2}' || true)

if [ -n "$EXISTING_DROPLET" ]; then
    echo -e "${YELLOW}⚠️  Droplet '$DROPLET_NAME' already exists (ID: $EXISTING_DROPLET)${NC}"
    read -p "Do you want to redeploy to the existing droplet? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Deployment cancelled."
        exit 0
    fi
    DROPLET_ID=$EXISTING_DROPLET
    DROPLET_IP=$(doctl compute droplet get $DROPLET_ID --format PublicIPv4 --no-header)
else
    echo "🖥️  Creating new droplet..."
    
    # Get SSH key fingerprint
    SSH_KEY_FINGERPRINT=$(doctl compute ssh-key list --format Name,FingerPrint --no-header | grep "$SSH_KEY_NAME" | awk '{print $2}' || true)
    
    if [ -z "$SSH_KEY_FINGERPRINT" ]; then
        echo -e "${YELLOW}No SSH key found. Creating one...${NC}"
        ssh-keygen -t ed25519 -f ~/.ssh/blog-poster-key -N "" -C "blog-poster@staging"
        doctl compute ssh-key create $SSH_KEY_NAME --public-key-file ~/.ssh/blog-poster-key.pub
        SSH_KEY_FINGERPRINT=$(doctl compute ssh-key list --format Name,FingerPrint --no-header | grep "$SSH_KEY_NAME" | awk '{print $2}')
    fi
    
    # Create droplet
    DROPLET_ID=$(doctl compute droplet create $DROPLET_NAME \
        --region $REGION \
        --size $SIZE \
        --image $IMAGE \
        --ssh-keys $SSH_KEY_FINGERPRINT \
        --enable-monitoring \
        --enable-backups \
        --format ID \
        --no-header \
        --wait)
    
    echo -e "${GREEN}✅ Droplet created (ID: $DROPLET_ID)${NC}"
    
    # Get droplet IP
    DROPLET_IP=$(doctl compute droplet get $DROPLET_ID --format PublicIPv4 --no-header)
fi

echo "📍 Droplet IP: $DROPLET_IP"
echo ""

# Wait for SSH to be ready
echo "⏳ Waiting for SSH to be ready..."
for i in {1..30}; do
    if ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no root@$DROPLET_IP "echo 'SSH ready'" &>/dev/null; then
        echo -e "${GREEN}✅ SSH connection established${NC}"
        break
    fi
    echo -n "."
    sleep 5
done
echo ""

# Create deployment script
cat > deploy-remote.sh <<'REMOTE_SCRIPT'
#!/bin/bash
set -e

echo "🔧 Setting up blog-poster on droplet..."

# Update system
apt-get update
apt-get upgrade -y

# Install Docker Compose if not present
if ! command -v docker-compose &> /dev/null; then
    curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
fi

# Create app directory
mkdir -p /opt/blog-poster
cd /opt/blog-poster

# Clone or update repository
if [ -d ".git" ]; then
    git pull origin dev
else
    git clone -b dev https://github.com/anthonyscolaro/blog-poster.git .
fi

# Create staging environment file if it doesn't exist
if [ ! -f .env.staging ]; then
    cp .env.local.example .env.staging
    echo "⚠️  Please edit /opt/blog-poster/.env.staging with your API keys"
fi

# Build and start services
docker-compose -f docker-compose.staging.yml down
docker-compose -f docker-compose.staging.yml build
docker-compose -f docker-compose.staging.yml up -d

# Wait for services to be healthy
echo "⏳ Waiting for services to start..."
sleep 10

# Check health
if curl -f http://localhost/health; then
    echo "✅ Services are running!"
else
    echo "❌ Health check failed"
    docker-compose -f docker-compose.staging.yml logs api
fi

# Setup firewall
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
echo "y" | ufw enable

echo "🎉 Deployment complete!"
REMOTE_SCRIPT

# Copy and execute deployment script
echo "📤 Deploying to droplet..."
scp -o StrictHostKeyChecking=no deploy-remote.sh root@$DROPLET_IP:/tmp/
ssh -o StrictHostKeyChecking=no root@$DROPLET_IP "bash /tmp/deploy-remote.sh"

# Optional: Setup domain
if [ -n "$DOMAIN" ]; then
    echo ""
    echo "🌐 Setting up domain $DOMAIN..."
    
    # Check if domain record exists
    RECORD_ID=$(doctl compute domain records list $DOMAIN --format Name,ID --no-header | grep "^@" | awk '{print $2}' || true)
    
    if [ -n "$RECORD_ID" ]; then
        # Update existing record
        doctl compute domain records update $DOMAIN --record-id $RECORD_ID --record-data $DROPLET_IP
    else
        # Create new record
        doctl compute domain records create $DOMAIN --record-type A --record-name @ --record-data $DROPLET_IP
    fi
    
    echo -e "${GREEN}✅ Domain configured to point to $DROPLET_IP${NC}"
fi

echo ""
echo "================== Deployment Summary =================="
echo -e "${GREEN}✅ Deployment successful!${NC}"
echo ""
echo "📊 Droplet Details:"
echo "   Name: $DROPLET_NAME"
echo "   ID: $DROPLET_ID"
echo "   IP: $DROPLET_IP"
echo "   Size: $SIZE"
echo "   Region: $REGION"
echo ""
echo "🔗 Access URLs:"
echo "   HTTP: http://$DROPLET_IP"
if [ -n "$DOMAIN" ]; then
    echo "   Domain: https://$DOMAIN"
fi
echo "   Dashboard: http://$DROPLET_IP/dashboard"
echo "   Pipeline: http://$DROPLET_IP/pipeline"
echo "   Health: http://$DROPLET_IP/health"
echo ""
echo "📝 Next Steps:"
echo "1. SSH into droplet: ssh root@$DROPLET_IP"
echo "2. Edit environment variables: nano /opt/blog-poster/.env.staging"
echo "3. Restart services: cd /opt/blog-poster && docker-compose -f docker-compose.staging.yml restart"
echo "4. View logs: docker-compose -f docker-compose.staging.yml logs -f"
echo ""
echo "🔐 Security Reminder:"
echo "   - Set up SSL certificates with Let's Encrypt"
echo "   - Configure firewall rules"
echo "   - Set strong passwords for all services"
echo "   - Enable automatic backups"
echo "========================================================"

# Clean up
rm -f deploy-remote.sh
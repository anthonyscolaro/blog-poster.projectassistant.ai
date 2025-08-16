#!/bin/bash

# Digital Ocean App Platform Deployment Script
# Usage: ./deploy.sh [staging|production]

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default to staging if no environment specified
ENVIRONMENT=${1:-staging}

echo -e "${GREEN}🚀 Blog-Poster Deployment Script${NC}"
echo -e "${YELLOW}Environment: ${ENVIRONMENT}${NC}"
echo ""

# Check if doctl is installed
if ! command -v doctl &> /dev/null; then
    echo -e "${RED}❌ doctl CLI not found. Please install it first:${NC}"
    echo "brew install doctl"
    exit 1
fi

# Check if authenticated
if ! doctl account get &> /dev/null; then
    echo -e "${RED}❌ Not authenticated with Digital Ocean${NC}"
    echo "Run: doctl auth init"
    exit 1
fi

# Set app name based on environment
if [ "$ENVIRONMENT" = "production" ]; then
    APP_NAME="blog-poster-api"
    APP_SPEC="app.yaml"
    BRANCH="main"
elif [ "$ENVIRONMENT" = "staging" ]; then
    APP_NAME="blog-poster-staging"
    APP_SPEC="app.staging.yaml"
    BRANCH="staging"
else
    echo -e "${RED}❌ Invalid environment: ${ENVIRONMENT}${NC}"
    echo "Usage: ./deploy.sh [staging|production]"
    exit 1
fi

echo -e "${GREEN}📋 Pre-deployment checks...${NC}"

# Check if app spec exists
if [ ! -f "$APP_SPEC" ]; then
    echo -e "${YELLOW}⚠️  App spec not found: ${APP_SPEC}${NC}"
    if [ "$ENVIRONMENT" = "staging" ]; then
        echo "Creating staging spec from production spec..."
        cp app.yaml app.staging.yaml
        # Update staging spec
        sed -i '' 's/blog-poster-api/blog-poster-staging/g' app.staging.yaml
        sed -i '' 's/branch: main/branch: staging/g' app.staging.yaml
        sed -i '' 's/professional-xs/basic-xxs/g' app.staging.yaml
        sed -i '' 's/value: production/value: staging/g' app.staging.yaml
        echo -e "${GREEN}✅ Created staging spec${NC}"
    else
        exit 1
    fi
fi

# Check if the app exists
APP_ID=$(doctl apps list --format ID,Name --no-header | grep "$APP_NAME" | awk '{print $1}')

if [ -z "$APP_ID" ]; then
    echo -e "${YELLOW}📱 Creating new app: ${APP_NAME}${NC}"
    
    # Create the app
    APP_ID=$(doctl apps create --spec "$APP_SPEC" --format ID --no-header)
    
    if [ -z "$APP_ID" ]; then
        echo -e "${RED}❌ Failed to create app${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ App created with ID: ${APP_ID}${NC}"
else
    echo -e "${GREEN}✅ Found existing app: ${APP_NAME} (${APP_ID})${NC}"
    
    # Update the app spec
    echo -e "${YELLOW}📝 Updating app spec...${NC}"
    doctl apps spec update "$APP_ID" --spec "$APP_SPEC"
fi

# Set environment variables if .env.production exists
if [ -f ".env.${ENVIRONMENT}" ]; then
    echo -e "${YELLOW}🔐 Setting environment variables...${NC}"
    
    # Parse .env file and set variables
    while IFS='=' read -r key value; do
        # Skip comments and empty lines
        if [[ ! "$key" =~ ^# ]] && [ -n "$key" ]; then
            # Remove quotes from value
            value="${value%\"}"
            value="${value#\"}"
            
            # Check if it's a secret variable
            if [[ "$key" =~ (KEY|PASSWORD|SECRET|TOKEN|URL) ]]; then
                echo "  Setting secret: $key"
                doctl apps config set "$APP_ID" --key "$key" --value "$value" --type SECRET --scope RUN_TIME
            fi
        fi
    done < ".env.${ENVIRONMENT}"
    
    echo -e "${GREEN}✅ Environment variables set${NC}"
else
    echo -e "${YELLOW}⚠️  No .env.${ENVIRONMENT} file found${NC}"
fi

# Trigger deployment
echo -e "${YELLOW}🚀 Triggering deployment...${NC}"
DEPLOYMENT_ID=$(doctl apps create-deployment "$APP_ID" --format ID --no-header --wait)

if [ -z "$DEPLOYMENT_ID" ]; then
    echo -e "${RED}❌ Failed to create deployment${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Deployment started: ${DEPLOYMENT_ID}${NC}"

# Get app URL
echo -e "${YELLOW}📱 Getting app information...${NC}"
APP_URL=$(doctl apps get "$APP_ID" --format DefaultIngress --no-header)

if [ -n "$APP_URL" ]; then
    echo -e "${GREEN}✅ App URL: ${APP_URL}${NC}"
    
    # Wait for health check
    echo -e "${YELLOW}⏳ Waiting for health check...${NC}"
    sleep 30
    
    # Test the health endpoint
    if curl -s "${APP_URL}/health" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Health check passed!${NC}"
        echo ""
        echo -e "${GREEN}🎉 Deployment successful!${NC}"
        echo -e "API URL: ${GREEN}${APP_URL}${NC}"
        echo -e "API Docs: ${GREEN}${APP_URL}/api/docs${NC}"
    else
        echo -e "${YELLOW}⚠️  Health check not responding yet${NC}"
        echo "Check deployment status with: doctl apps get-deployment $APP_ID $DEPLOYMENT_ID"
    fi
else
    echo -e "${YELLOW}⚠️  No public URL assigned yet${NC}"
fi

echo ""
echo -e "${GREEN}📊 Useful commands:${NC}"
echo "  View logs:        doctl apps logs $APP_ID --follow"
echo "  View deployment:  doctl apps get-deployment $APP_ID $DEPLOYMENT_ID"
echo "  List deployments: doctl apps list-deployments $APP_ID"
echo "  App details:      doctl apps get $APP_ID"
#!/bin/bash

# Blog Poster - Digital Ocean Staging Deployment Script
# This script deploys the blog-poster app to Digital Ocean App Platform
# Prerequisites: doctl CLI installed and authenticated

set -e

echo "🚀 Blog Poster - Digital Ocean Staging Deployment"
echo "=================================================="
echo ""

# Configuration
APP_NAME="blog-poster-staging"
REGION="nyc"  # New York region
BRANCH="dev"  # Staging branch

# Check if doctl is installed
if ! command -v doctl &> /dev/null; then
    echo "❌ Error: doctl CLI is not installed"
    echo "Install it with: brew install doctl"
    exit 1
fi

# Verify authentication
echo "📋 Checking Digital Ocean authentication..."
if ! doctl account get &> /dev/null; then
    echo "❌ Error: Not authenticated with Digital Ocean"
    echo "Run: doctl auth init"
    exit 1
fi

ACCOUNT_EMAIL=$(doctl account get --format Email --no-header)
echo "✅ Authenticated as: $ACCOUNT_EMAIL"
echo ""

# Create app spec for staging deployment
cat > app-staging.yaml <<EOF
name: blog-poster-staging
region: nyc
services:
- name: api
  dockerfile_path: Dockerfile
  source_dir: /
  github:
    branch: $BRANCH
    deploy_on_push: true
    repo: anthonyscolaro/blog-poster
  http_port: 8088
  instance_count: 1
  instance_size_slug: basic-xxs
  health_check:
    http_path: /health
    initial_delay_seconds: 10
    period_seconds: 10
    timeout_seconds: 5
    success_threshold: 1
    failure_threshold: 3
  envs:
  - key: DATABASE_URL
    scope: RUN_AND_BUILD_TIME
    value: \${db.DATABASE_URL}
  - key: REDIS_URL
    scope: RUN_AND_BUILD_TIME
    value: \${redis.REDIS_URL}
  - key: ANTHROPIC_API_KEY
    scope: RUN_TIME
    type: SECRET
  - key: JINA_API_KEY
    scope: RUN_TIME
    type: SECRET
  - key: WORDPRESS_URL
    scope: RUN_TIME
    value: "https://servicedogus.com"
  - key: WP_USERNAME
    scope: RUN_TIME
    type: SECRET
  - key: WP_APP_PASSWORD
    scope: RUN_TIME
    type: SECRET
  - key: WP_VERIFY_SSL
    scope: RUN_TIME
    value: "true"
  - key: DEBUG
    scope: RUN_TIME
    value: "false"
  - key: LOG_LEVEL
    scope: RUN_TIME
    value: "INFO"

databases:
- name: db
  engine: PG
  production: false
  size: db-s-dev-database
  version: "16"

- name: redis
  engine: REDIS
  production: false
  size: db-s-dev-database
  version: "7"

jobs:
- name: db-migrate
  kind: PRE_DEPLOY
  source_dir: /
  github:
    branch: $BRANCH
    repo: anthonyscolaro/blog-poster
  run_command: python scripts/init_database.py
  envs:
  - key: DATABASE_URL
    scope: RUN_AND_BUILD_TIME
    value: \${db.DATABASE_URL}

# Static site for the UI
static_sites:
- name: dashboard
  source_dir: /
  github:
    branch: $BRANCH
    repo: anthonyscolaro/blog-poster
  index_document: dashboard.html
  error_document: error.html
  routes:
  - path: /
    preserve_path_prefix: true
EOF

echo "📦 Creating/updating Digital Ocean App..."
echo ""

# Check if app exists
if doctl apps list --format Name --no-header | grep -q "^${APP_NAME}$"; then
    echo "App exists. Updating configuration..."
    APP_ID=$(doctl apps list --format Name,ID --no-header | grep "^${APP_NAME}" | awk '{print $2}')
    doctl apps update $APP_ID --spec app-staging.yaml
else
    echo "Creating new app..."
    doctl apps create --spec app-staging.yaml
    APP_ID=$(doctl apps list --format Name,ID --no-header | grep "^${APP_NAME}" | awk '{print $2}')
fi

echo ""
echo "⏳ Waiting for deployment to start..."
sleep 5

# Get app URL
APP_URL=$(doctl apps get $APP_ID --format LiveURL --no-header)

echo ""
echo "📊 Deployment Status:"
echo "===================="
doctl apps get-deployment $APP_ID $(doctl apps list-deployments $APP_ID --format ID --no-header | head -1)

echo ""
echo "🔗 App Details:"
echo "=============="
echo "App ID: $APP_ID"
echo "App URL: $APP_URL"
echo "Dashboard: https://cloud.digitalocean.com/apps/$APP_ID"
echo ""

echo "📝 Next Steps:"
echo "============="
echo "1. Set environment secrets in Digital Ocean dashboard:"
echo "   - ANTHROPIC_API_KEY"
echo "   - JINA_API_KEY"
echo "   - WP_USERNAME"
echo "   - WP_APP_PASSWORD"
echo ""
echo "2. Monitor deployment progress:"
echo "   doctl apps list-deployments $APP_ID"
echo ""
echo "3. View logs:"
echo "   doctl apps logs $APP_ID"
echo ""
echo "4. Access your app at:"
echo "   $APP_URL"
echo ""

# Monitor deployment
echo "🔄 Monitoring deployment (press Ctrl+C to stop)..."
while true; do
    STATUS=$(doctl apps list-deployments $APP_ID --format Phase --no-header | head -1)
    echo -ne "\rDeployment status: $STATUS    "
    
    if [[ "$STATUS" == "ACTIVE" ]]; then
        echo ""
        echo "✅ Deployment successful!"
        break
    elif [[ "$STATUS" == "ERROR" ]] || [[ "$STATUS" == "CANCELED" ]]; then
        echo ""
        echo "❌ Deployment failed with status: $STATUS"
        echo "Check logs with: doctl apps logs $APP_ID"
        exit 1
    fi
    
    sleep 5
done

echo ""
echo "🎉 Staging deployment complete!"
echo "Access your app at: $APP_URL"
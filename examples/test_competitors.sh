#!/bin/bash

# Test script for competitor monitoring endpoints
# Usage: ./test_competitors.sh

BASE_URL="http://localhost:8088"

echo "🔍 Testing Competitor Monitoring Endpoints"
echo "=========================================="

# Check if API is running
echo -n "Checking API health... "
if curl -s "$BASE_URL/health" > /dev/null; then
    echo "✅ API is running"
else
    echo "❌ API is not running. Start it with: docker compose up"
    exit 1
fi

echo ""
echo "1️⃣ Scanning competitors..."
echo "----------------------------"
curl -X POST "$BASE_URL/competitors/scan?force=true" \
    -H "Content-Type: application/json" | jq '.'

echo ""
echo "2️⃣ Getting competitor insights..."
echo "-----------------------------------"
curl -s "$BASE_URL/competitors/insights" | jq '.'

echo ""
echo "3️⃣ Getting trending topics..."
echo "-------------------------------"
curl -s "$BASE_URL/competitors/trends" | jq '.trends[:3]'

echo ""
echo "4️⃣ Identifying content gaps..."
echo "--------------------------------"
curl -s "$BASE_URL/competitors/gaps" | jq '.gaps[:3]'

echo ""
echo "✅ Competitor monitoring test complete!"
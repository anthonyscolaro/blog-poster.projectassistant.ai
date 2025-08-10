#!/bin/bash

# Quick WordPress Publishing Test
# Update the PASSWORD variable with your actual WordPress password

USERNAME="anthony"
PASSWORD="YOUR_WORDPRESS_PASSWORD"  # <-- UPDATE THIS
API_URL="http://localhost:8088"
WP_URL="http://localhost:8084"

echo "🔧 WordPress Publishing Quick Test"
echo "=================================="
echo ""
echo "⚠️  Before running this test:"
echo "1. Update the PASSWORD variable in this script with your WordPress password"
echo "2. Update .env.local with the same password:"
echo "   WP_USERNAME=anthony"
echo "   WP_APP_PASSWORD=your-password-here"
echo ""
read -p "Have you updated the password? (y/n): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Please update the password first."
    exit 1
fi

echo ""
echo "Testing WordPress API directly..."
echo "---------------------------------"

# Test WordPress API
RESPONSE=$(curl -s -u "$USERNAME:$PASSWORD" \
  "$WP_URL/wp-json/wp/v2/posts" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Post - '"$(date +%Y-%m-%d\ %H:%M)"'",
    "content": "This is a test post created by the Blog Poster quick test.",
    "status": "draft"
  }')

# Check if post was created
if echo "$RESPONSE" | grep -q '"id"'; then
    POST_ID=$(echo "$RESPONSE" | grep -o '"id":[0-9]*' | cut -d: -f2)
    echo "✅ Post created successfully! ID: $POST_ID"
    echo "   View at: $WP_URL/wp-admin/post.php?post=$POST_ID&action=edit"
else
    echo "❌ Failed to create post"
    echo "   Response: $RESPONSE"
    exit 1
fi

echo ""
echo "Testing Blog Poster API..."
echo "--------------------------"

# Test via Blog Poster API
curl -s "$API_URL/wordpress/test" | python -m json.tool

echo ""
echo "=================================="
echo "✅ If the test passed, you can now:"
echo "1. Run: python examples/test_full_workflow.py"
echo "2. Or use: ./examples/full_workflow_test.sh"
echo ""
echo "Note: You still need valid AI API keys (Anthropic/OpenAI) for article generation"
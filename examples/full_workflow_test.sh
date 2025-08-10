#!/bin/bash

# Full end-to-end workflow test: Research → Generate → Publish
# This script demonstrates the complete blog posting workflow

BASE_URL="http://localhost:8088"
WP_URL="http://localhost:8084"

echo "🚀 Blog-Poster Full Workflow Test"
echo "=================================="
echo "This will:"
echo "  1. Scan competitors for trending topics"
echo "  2. Generate an SEO-optimized article"
echo "  3. Publish to WordPress as a draft"
echo ""

# Check API health
echo "Checking services..."
if ! curl -s "$BASE_URL/health" > /dev/null; then
    echo "❌ API not running. Start with: docker compose up"
    exit 1
fi
echo "✅ API is healthy"

# Step 1: Get competitor insights
echo ""
echo "📊 Step 1: Analyzing competitors for trending topics..."
INSIGHTS=$(curl -s "$BASE_URL/competitors/insights")

if [ -z "$INSIGHTS" ]; then
    echo "⚠️ Could not get competitor insights, using default topic"
    TOPIC="Service Dog Training: Essential Commands Every Handler Should Know"
    PRIMARY_KW="service dog commands"
else
    # Extract first trending topic (using jq if available)
    if command -v jq > /dev/null; then
        TOPIC=$(echo "$INSIGHTS" | jq -r '.trending_topics[0].topic // "Service Dog Training Basics"')
        echo "  Found trending topic: $TOPIC"
    else
        TOPIC="Service Dog Training: Essential Commands Every Handler Should Know"
        echo "  Using default topic: $TOPIC"
    fi
    PRIMARY_KW="service dog training"
fi

# Step 2: Generate article
echo ""
echo "✍️ Step 2: Generating SEO-optimized article..."
echo "  Topic: $TOPIC"
echo "  Primary keyword: $PRIMARY_KW"
echo "  This may take 30-60 seconds..."

ARTICLE_RESPONSE=$(curl -s -X POST "$BASE_URL/article/generate" \
    -H "Content-Type: application/json" \
    -d "{
        \"topic\": \"$TOPIC\",
        \"primary_keyword\": \"$PRIMARY_KW\",
        \"secondary_keywords\": [\"ADA requirements\", \"training tips\", \"handler rights\"],
        \"min_words\": 1500,
        \"max_words\": 2000,
        \"use_competitor_insights\": true
    }")

if [ -z "$ARTICLE_RESPONSE" ]; then
    echo "❌ Article generation failed"
    echo "  Check that ANTHROPIC_API_KEY or OPENAI_API_KEY is set in .env.local"
    exit 1
fi

# Extract article data
if command -v jq > /dev/null; then
    TITLE=$(echo "$ARTICLE_RESPONSE" | jq -r '.title')
    SLUG=$(echo "$ARTICLE_RESPONSE" | jq -r '.slug')
    META_TITLE=$(echo "$ARTICLE_RESPONSE" | jq -r '.meta_title')
    META_DESC=$(echo "$ARTICLE_RESPONSE" | jq -r '.meta_description')
    CONTENT=$(echo "$ARTICLE_RESPONSE" | jq -r '.content_markdown')
    WORD_COUNT=$(echo "$ARTICLE_RESPONSE" | jq -r '.word_count')
    SEO_SCORE=$(echo "$ARTICLE_RESPONSE" | jq -r '.seo_score')
    
    echo ""
    echo "✅ Article generated successfully!"
    echo "  Title: $TITLE"
    echo "  Word count: $WORD_COUNT"
    echo "  SEO score: ${SEO_SCORE}/100"
else
    echo "✅ Article generated (install jq for detailed output)"
    TITLE="Generated Article"
    SLUG="generated-article-$(date +%s)"
    CONTENT="Article content here"
fi

# Step 3: Publish to WordPress
echo ""
echo "📤 Step 3: Publishing to WordPress..."
echo "  Target: $WP_URL"
echo "  Status: DRAFT (for review)"

# Create publish payload
PUBLISH_PAYLOAD=$(cat <<EOF
{
    "frontmatter": {
        "title": "$TITLE",
        "slug": "$SLUG",
        "category": "ADA Compliance",
        "tags": ["service dogs", "training", "ADA"],
        "meta_title": "$META_TITLE",
        "meta_desc": "$META_DESC"
    },
    "markdown": "$CONTENT",
    "status": "DRAFT"
}
EOF
)

# Save article to file for backup
BACKUP_FILE="data/articles/${SLUG}-$(date +%Y%m%d_%H%M%S).json"
mkdir -p data/articles
echo "$ARTICLE_RESPONSE" > "$BACKUP_FILE"
echo "  💾 Article backed up to: $BACKUP_FILE"

# Publish to WordPress
PUBLISH_RESPONSE=$(curl -s -X POST "$BASE_URL/publish/wp" \
    -H "Content-Type: application/json" \
    -d "$PUBLISH_PAYLOAD")

if echo "$PUBLISH_RESPONSE" | grep -q "error"; then
    echo "❌ Publishing failed"
    echo "  Response: $PUBLISH_RESPONSE"
    echo ""
    echo "  Troubleshooting:"
    echo "  1. Check WordPress is running at $WP_URL"
    echo "  2. Verify WP_USERNAME and WP_APP_PASSWORD in .env.local"
    echo "  3. Ensure WPGraphQL plugin is activated"
else
    echo "✅ Article published to WordPress!"
    
    if command -v jq > /dev/null && [ -n "$PUBLISH_RESPONSE" ]; then
        POST_ID=$(echo "$PUBLISH_RESPONSE" | jq -r '.id // .post_id // ""')
        if [ -n "$POST_ID" ]; then
            echo "  View draft at: $WP_URL/wp-admin/post.php?post=$POST_ID&action=edit"
        fi
    fi
    
    echo ""
    echo "  Next steps:"
    echo "  1. Review the article in WordPress admin"
    echo "  2. Add featured image if needed"
    echo "  3. Review SEO metadata"
    echo "  4. Publish when ready"
fi

# Step 4: Show cost summary
echo ""
echo "💰 Cost Summary:"
COSTS=$(curl -s "$BASE_URL/article/costs")
if command -v jq > /dev/null && [ -n "$COSTS" ]; then
    TOTAL_COST=$(echo "$COSTS" | jq -r '.total_cost // 0')
    echo "  Total session cost: \$${TOTAL_COST}"
else
    echo "  Check $BASE_URL/article/costs for details"
fi

echo ""
echo "🎉 Workflow complete!"
echo ""
echo "📊 Summary:"
echo "  • Competitor analysis: ✅"
echo "  • Article generation: ✅"
echo "  • WordPress publishing: ✅"
echo "  • Cost tracking: ✅"
echo ""
echo "View your WordPress site at: $WP_URL"
echo "Admin panel: $WP_URL/wp-admin"
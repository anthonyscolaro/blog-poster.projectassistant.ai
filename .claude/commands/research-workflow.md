---
allowed-tools: Bash(curl:*), Bash(python:*), Task, Read, Write
description: Comprehensive research using hybrid Jina + LocalDocs approach
---

# Hybrid Research Workflow

Execute comprehensive research using both Jina scraping for detailed analysis and LocalDocs for organized, reusable collections.

## Research Strategy Selection

**For New/Unknown Technologies:**
- Use Jina scraping for comprehensive page-by-page analysis
- Create detailed research/ directory structure
- Generate llm.txt summaries for PRP context

**For Established Technologies:**
- Check existing LocalDocs collections first
- Add key documentation to LocalDocs for team reuse
- Export organized @file references for Claude integration

## Execution Workflow

### Phase 1: Assessment
1. **Check existing LocalDocs collections** for relevant documentation
   ```bash
   python /Users/anthonyscolaro/apps/localdocs/bin/localdocs list --tags $TECHNOLOGY
   ```

2. **If existing collections found**: Export and extend
   ```bash
   python /Users/anthonyscolaro/apps/localdocs/bin/localdocs export $TECHNOLOGY-docs --format claude
   ```

3. **If no existing collections**: Proceed with comprehensive research

### Phase 2: Jina Research (New Technologies)
1. **Create research directory structure**
   ```bash
   mkdir -p research/$TECHNOLOGY/page{1..8}
   ```

2. **Scrape key documentation pages**
   ```bash
   curl "https://r.jina.ai/https://docs.$TECHNOLOGY.com/guide" \
     -H "Authorization: Bearer $JINA_TOKEN" > research/$TECHNOLOGY/page1/guide.md
   
   curl "https://r.jina.ai/https://docs.$TECHNOLOGY.com/api" \
     -H "Authorization: Bearer $JINA_TOKEN" > research/$TECHNOLOGY/page2/api.md
   ```

3. **Quality validation**: If scrapes fail or return minimal content, retry until successful

4. **Create technology summary**
   ```bash
   # Compile findings into llm.txt for AI context
   cat research/$TECHNOLOGY/page*/*.md > research/$TECHNOLOGY/llm.txt
   ```

### Phase 3: LocalDocs Organization
1. **Add key URLs to LocalDocs**
   ```bash
   python /Users/anthonyscolaro/apps/localdocs/bin/localdocs add \
     https://docs.$TECHNOLOGY.com/api \
     https://docs.$TECHNOLOGY.com/authentication \
     https://docs.$TECHNOLOGY.com/deployment
   ```

2. **Organize with meaningful metadata**
   ```bash
   python /Users/anthonyscolaro/apps/localdocs/bin/localdocs set [hash] \
     -n "$TECHNOLOGY API" \
     -d "Core API endpoints and authentication" \
     -t "$TECHNOLOGY,api,reference"
   ```

3. **Export organized collections**
   ```bash
   python /Users/anthonyscolaro/apps/localdocs/bin/localdocs export $TECHNOLOGY-integration --format claude
   ```

### Phase 4: Multi-Agent Coordination
When multiple technologies need research:

1. **Launch parallel agents** for different technologies
2. **Coordinate LocalDocs organization** to avoid conflicts
3. **Create unified exports** for related technologies

## Quality Assurance

### Content Validation
- **Check scraped content size**: Files should be substantial (>1KB typically)
- **Verify content relevance**: Ensure scraped content matches expected documentation
- **Retry failed scrapes**: Don't accept minimal or failed content

### Organization Standards
- **Consistent tagging**: Use standardized tags across projects
- **Clear descriptions**: Metadata should be searchable and descriptive
- **Logical grouping**: Export collections that make sense for specific use cases

## Integration with Development

### Using Research Results
1. **Jina Research**: Reference `research/$TECHNOLOGY/llm.txt` for comprehensive context
2. **LocalDocs Collections**: Use @file references for specific API endpoints
3. **Combined Approach**: Deep context from Jina, quick reference from LocalDocs

### Team Collaboration
1. **Share LocalDocs collections** across team members
2. **Maintain research/ directories** for project-specific deep analysis
3. **Export collections** for cross-project reuse

## Error Handling

### Failed Scrapes
```bash
# Check if scrape succeeded
if [ -s "research/$TECHNOLOGY/page1/content.md" ]; then
    echo "Scrape successful"
else
    echo "Scrape failed, retrying..."
    # Retry logic
fi
```

### LocalDocs Issues
```bash
# Verify LocalDocs installation
python /Users/anthonyscolaro/apps/localdocs/bin/localdocs --help

# Check collection status
python /Users/anthonyscolaro/apps/localdocs/bin/localdocs list
```

## Output Structure

After successful execution, you should have:

```
research/
└── $TECHNOLOGY/
    ├── page1/guide.md
    ├── page2/api.md
    ├── page3/auth.md
    └── llm.txt

docs/
└── $TECHNOLOGY-integration/
    ├── claude-refs.md
    ├── [hash1].md
    ├── [hash2].md
    └── localdocs.config.json
```

## Usage Examples

```bash
# Research new API integration
/research-workflow "FastAPI authentication and deployment"

# Extend existing collection
/research-workflow "Add Supabase real-time features to existing database collection"

# Multi-technology research
/research-workflow "React frontend with FastAPI backend and PostgreSQL database"
```

This hybrid approach ensures comprehensive research depth while building reusable, organized documentation assets for team collaboration and future projects.
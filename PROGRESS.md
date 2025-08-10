# Blog Poster — Progress & Status

## What’s done
- Rules/docs aligned
  - Added `.cursorrules` and updated `CLAUDE.md` to use `~/shared-docs/` with key WP Headless refs
  - Added Shared Docs section to `README.md`
- PRP & tasks
  - Created `PRPs/blog-poster.prp.md` (goal, success criteria, tasks, validation loop)
  - Added in-progress checklist to `TASK.md`
- Publisher & auth
  - Publisher supports Bearer JWT or Basic (Application Passwords)
  - JWT login fallback via WPGraphQL if available
  - `WP_VERIFY_SSL` to allow local self-signed HTTPS
  - Ensured `ADA Compliance` category exists via WP-CLI
  - Generated WP Application Password and saved in `.env.local`
- Docker & env
  - `blog-poster/docker-compose.yml` loads `../.env.local`
  - Removed Redis host port mapping (avoids conflict with project Redis)
  - Relaxed qdrant health gating (depends_on: service_started)
  - Publisher prefers internal WP URL; fallback to external
  - API service exports `WORDPRESS_URL` from `WORDPRESS_LOCAL_URL` with host fallback
- Makefile
  - Added targets: `blog-poster-up`, `blog-poster-down`, `blog-poster-logs`, `blog-poster-rebuild`
- Examples
  - Added Base64 hero image curl example to `blog-poster/blog-poster.md`

## Environment
Use repository root `.env.local`:

```bash
# WordPress local
WORDPRESS_LOCAL_URL=https://host.docker.internal:8445
WORDPRESS_LOCAL_GRAPHQL_URL=https://host.docker.internal:8445/graphql
WORDPRESS_LOCAL_API_URL=https://host.docker.internal:8445/wp-json/wp/v2

# External browser access
WORDPRESS_EXTERNAL_URL=https://localhost:8445
WORDPRESS_EXTERNAL_GRAPHQL_URL=https://localhost:8445/graphql

# Auth (choose ONE method)
WP_AUTH_TOKEN=                 # if JWT available
# OR Application Passwords
WP_USERNAME=admin
WP_APP_PASSWORD=<generated>

# Local SSL
WP_VERIFY_SSL=false
```

## How to run
```bash
# Start WordPress
make wp-up

# Start blog-poster stack (API, qdrant, pgvector, redis)
make blog-poster-up

# Logs
make blog-poster-logs
```

## Smoke tests
```bash
# Health
curl -s http://localhost:8088/health

# Publish minimal post with inline Base64 hero image (DRAFT)
BASE64_IMG="iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGNgYAAAAAMAASsJTYQAAAAASUVORK5CYII="
jq -n --arg b64 "$BASE64_IMG" '{
  frontmatter: {
    title: "Base64 Media Upload Test",
    slug: "base64-media-upload-test",
    category: "ADA Compliance",
    tags: ["service dogs"],
    meta_title: "Base64 Upload Test",
    meta_desc: "Validates inline Base64 media upload via REST and GraphQL.",
    canonical: "https://servicedogus.org/base64-media-upload-test",
    schema_jsonld: {},
    internal_link_targets: [],
    citations: ["https://www.ada.gov/resources/service-animals-2010-requirements/"]
  },
  markdown: "# Base64 Upload Test\n\nThis post validates media uploads.",
  status: "DRAFT",
  hero_image_base64: $b64,
  hero_image_filename: "tiny.png"
}' | curl -s -X POST http://localhost:8088/publish/wp -H 'Content-Type: application/json' -d @-
```

## Planned posts for validation
- `ada-service-dog-requirements` — ADA overview, two questions, disclaimers, citations
- `service-dog-laws-by-state-2025` — state-by-state quick reference with ADA context
- `esa-vs-service-dog` — clear differences, rights, access, documentation

## Playwright E2E (after publish)
- Assert pages render with H1, meta, featured image via frontend routes
- Validate slugs exist and return 200
- Capture screenshots for visual confirmation

## Issues & mitigations
- Qdrant unhealthy gating API startup → relaxed depends_on to service_started
- Redis port collision with project Redis → removed host port mapping
- API→WP reachability from container (service DNS) → switched to `host.docker.internal` fallback exported to API

## Next steps
- Publish 3 posts via `/publish/wp`
- Verify in WP Admin and frontend
- Add Playwright tests to assert presence of H1/meta/featured image per slug
- Add minimal pytest for helper functions (follow-up)

# Frontend Docker Setup

This guide explains how to run the Blog-Poster frontend in Docker for consistent development and deployment.

## Quick Start

### Start Everything (Backend + Frontend)
```bash
./scripts/docker-all.sh start
```

This will start:
- Backend API on http://localhost:8088
- Frontend on http://localhost:5173
- Supabase Studio on http://localhost:3100
- All supporting services

### Frontend-Only Commands
```bash
# Start frontend only
./scripts/docker-frontend.sh start

# View frontend logs
./scripts/docker-frontend.sh logs

# Open shell in frontend container
./scripts/docker-frontend.sh shell

# Run TypeScript type checking
./scripts/docker-frontend.sh typecheck

# Restart frontend
./scripts/docker-frontend.sh restart
```

## TypeScript Strict Mode Migration

### Check Current TypeScript Errors
```bash
# Run type check with current settings
./scripts/docker-all.sh typecheck

# Check what errors would appear with strict mode
./scripts/docker-all.sh typecheck-strict
```

### Run TypeScript Fixes in Docker
```bash
# Open shell in frontend container
./scripts/docker-frontend.sh shell

# Inside container, run TypeScript compiler
npx tsc --noEmit

# Or save errors to file
npx tsc --noEmit > /app/typescript-errors.txt 2>&1
```

## Development Workflow

### 1. Initial Setup
```bash
# Clone repository
git clone <repo-url>
cd blog-poster

# Copy environment variables
cp .env.example .env.local
cp frontend/.env.example frontend/.env.local

# Start everything
./scripts/docker-all.sh start
```

### 2. Daily Development
```bash
# Start services
./scripts/docker-all.sh start

# Make changes in your editor
# Frontend hot-reloads automatically

# Check TypeScript
./scripts/docker-frontend.sh typecheck

# View logs if needed
./scripts/docker-frontend.sh logs
```

### 3. Debugging
```bash
# Open shell in frontend container
./scripts/docker-frontend.sh shell

# Inside container:
npm run build  # Test production build
npm run lint   # Run linter
npx tsc --noEmit  # Type check
```

## Architecture

### Development Mode
- Frontend runs with Vite dev server
- Hot Module Replacement (HMR) enabled
- Source code mounted as volume
- Node modules in anonymous volume (faster)

### Production Mode
- Multi-stage build
- Static files served by nginx
- Optimized bundle size
- Security headers configured

## File Structure
```
blog-poster/
├── frontend/
│   ├── Dockerfile              # Multi-stage Docker build
│   ├── nginx.conf             # Production nginx config
│   ├── .dockerignore          # Files to exclude
│   └── src/                   # Application code
├── docker-compose.yml         # Backend services
├── docker-compose.frontend.yml # Frontend service
└── scripts/
    ├── docker-frontend.sh     # Frontend management
    └── docker-all.sh          # Complete stack management
```

## Environment Variables

Frontend environment variables in Docker:
- Set in `docker-compose.frontend.yml`
- Or pass via `.env.local` file
- Must be prefixed with `VITE_` to be accessible

```yaml
environment:
  VITE_SUPABASE_URL: http://localhost:8000
  VITE_SUPABASE_ANON_KEY: your-key-here
  VITE_API_URL: http://localhost:8088
```

## Troubleshooting

### Port Already in Use
```bash
# Find what's using port 5173
lsof -i :5173

# Kill the process or change port in docker-compose.frontend.yml
```

### Node Modules Issues
```bash
# Rebuild without cache
./scripts/docker-frontend.sh rebuild

# Or clean everything
./scripts/docker-frontend.sh clean
./scripts/docker-frontend.sh build
```

### Hot Reload Not Working
- Ensure `CHOKIDAR_USEPOLLING: true` is set in docker-compose.frontend.yml
- Check that volumes are mounted correctly
- Restart the frontend container

### TypeScript Errors
```bash
# Check errors in container
./scripts/docker-frontend.sh shell
npx tsc --noEmit --pretty

# Fix incrementally
npx tsc --noEmit --listFiles | grep "error TS"
```

## Production Deployment

### Build Production Image
```bash
# Build optimized production image
docker build -t blog-frontend:production --target production ./frontend

# Run production container
docker run -p 80:80 blog-frontend:production
```

### Docker Compose Production
```yaml
# Uncomment production section in docker-compose.frontend.yml
# Then run:
docker compose -f docker-compose.frontend.yml up frontend-prod
```

## Benefits of Docker Frontend

1. **Consistency**: Same Node version for all developers
2. **Isolation**: No global npm package conflicts
3. **Reproducibility**: Guaranteed same build environment
4. **Easy Onboarding**: New developers just run one command
5. **CI/CD Ready**: Same Docker image for testing and deployment
6. **TypeScript Migration**: Consistent environment for fixing types

## Next Steps

1. Start services: `./scripts/docker-all.sh start`
2. Run TypeScript strict check: `./scripts/docker-all.sh typecheck-strict`
3. Fix TypeScript errors incrementally in Claude Code
4. Test changes in Docker environment
5. Deploy with confidence!
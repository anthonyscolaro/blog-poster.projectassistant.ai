# Port Allocation Strategy for Team Development

## Overview

This document defines the standard port allocation strategy for all projects in our development environment. The core principle is **service type separation** - Next.js applications stay in their own range (3xxx), monitoring tools stay in theirs (30xxx), preventing any possibility of overlap between different service types.

## Port Allocation Ranges

### Next.js Applications: 3000-3999
- **Purpose**: Frontend applications using Next.js
- **Assignment Strategy**: +2 offset from base port 3000
- **Range Logic**: Keeps all Next.js apps in the 3xxx range
- **Examples**:
  - Project 1: localhost:3002 (3000 + 2)
  - Project 2: localhost:3004 (3002 + 2) 
  - Project 3: localhost:3006 (3004 + 2)
  - Continue incrementing by +2 within 3xxx range

### API Services: 8000-8999
- **Purpose**: Backend APIs, FastAPI, Express, etc.
- **Assignment Strategy**: +2 offset from base port 8080
- **Range Logic**: Keeps all API services in the 8xxx range
- **Examples**:
  - Project 1 API: localhost:8082 (8080 + 2)
  - Project 2 API: localhost:8084 (8082 + 2)
  - Gateway services: 8000-8099 range

### Monitoring Tools: 30000-39999  
- **Purpose**: Grafana, Prometheus, monitoring dashboards
- **Assignment Strategy**: Use 30xxx range to completely separate from Next.js
- **Range Logic**: Prevents any overlap with 3xxx Next.js applications
- **Examples**:
  - Grafana: localhost:30002
  - Prometheus: localhost:30001  
  - Custom monitoring: localhost:30010+

### Admin Tools: 80-99
- **Purpose**: Database admin, system management
- **Assignment Strategy**: +2 offset from base port 80
- **Examples**:
  - PgAdmin: localhost:82 (80 + 2)
  - Custom admin: localhost:84

### Email/SMTP Services: 8025+ and 1025+
- **Purpose**: Email testing, SMTP services
- **Assignment Strategy**: +2 offset from standard ports
- **Examples**:
  - Mailpit Web UI: localhost:8027 (8025 + 2)
  - Mailpit SMTP: localhost:1027 (1025 + 2)

### Database Services: 54320+
- **Purpose**: PostgreSQL, Redis, databases
- **Assignment Strategy**: +2 offset from standard ports
- **Examples**:
  - PostgreSQL: localhost:54322 (54320 + 2)
  - Redis: localhost:6381 (6379 + 2)

## Implementation Guidelines

### For New Projects

1. **Choose next available ports in correct ranges**:
   ```bash
   # Check what's currently in use, then increment by +2
   Frontend: Next available in 3xxx range (3002, 3004, 3006...)
   API: Next available in 8xxx range (8082, 8084, 8086...)
   Monitoring: Next available in 30xxx range (30002, 30004, 30006...)
   ```

3. **Update your docker-compose files**:
   ```yaml
   frontend:
     ports:
       - "3002:3000"  # External:Internal
   
   api:
     ports:
       - "8082:8000"  # External:Internal
   
   grafana:
     ports:
       - "30002:3000"  # External:Internal
   ```

4. **Update environment variables**:
   ```bash
   NEXT_PUBLIC_APP_URL=http://localhost:3002
   NEXT_PUBLIC_API_URL=http://localhost:8082
   PLAYWRIGHT_BASE_URL=http://localhost:3002
   ```

### For Existing Projects

1. **Audit current port usage**: Check docker-compose files
2. **Update to follow strategy**: Modify ports to match allocation ranges  
3. **Update documentation**: Ensure README and memory files reflect changes
4. **Test thoroughly**: Verify no conflicts with other running projects

## Port Conflict Resolution

### Before Starting Development
```bash
# Check if ports are in use
netstat -an | grep :3002
netstat -an | grep :8082
netstat -an | grep :30002

# Or use lsof
lsof -i :3002
lsof -i :8082
```

### If Conflicts Occur
1. **Identify the conflicting process**: Use `lsof -i :PORT`
2. **Stop the conflicting service**: `kill -9 PID` if safe
3. **Use next available port**: Follow +2 increment pattern
4. **Update project documentation**: Record the port change

## Team Coordination

### Port Registry Integration
This strategy integrates with the team-wide port registry maintained in LocalDocs:
- **Registry Location**: `/Users/anthonyscolaro/apps/localdocs/data/port-registry.md`
- **Current Active Projects**: ColdKnock (+2), ProjectAssistant (+4), DevTools (+6)
- **Export for Sharing**: Use `localdocs export port-registry --format claude`

Before starting a new project:
1. Check the LocalDocs port registry for current assignments
2. Claim your next available offset (+8, +10, +12...)
3. Update the registry with your project details
4. Export and share updated registry with team

## Best Practices

1. **Always use the +2 offset pattern** for consistency
2. **Reserve monitoring ports early** to avoid conflicts
3. **Document ports in project README** and CLAUDE.md
4. **Test port allocation** before committing configuration
5. **Update templates** when changing port strategies

## Common Pitfalls

- ❌ **Don't hardcode localhost:3000** - use your assigned port  
- ❌ **Don't assume standard ports are free** - always check availability
- ❌ **Don't skip documentation** - team needs to know your port assignments
- ❌ **Don't change ports mid-project** without team coordination

## Integration with Enhanced Template

When using this template for new projects:

1. **Copy this strategy** into your project's memory/ directory
2. **Implement port assignments** in docker-compose files
3. **Update environment files** with correct URLs
4. **Test locally** before deploying to self-hosted server
5. **Document your port choices** in project README

---

This strategy ensures scalable, conflict-free development across our entire team and project portfolio.
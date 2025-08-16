# Migration Guide: WebSocket to Supabase Real-time

## Overview
The pipeline management system has been upgraded from custom WebSocket connections to Supabase real-time subscriptions. This provides better scalability, automatic reconnection, and leverages Supabase's infrastructure.

## Key Changes

### 1. Database Schema
The new version includes complete database tables with Row Level Security:
- `pipeline_executions` - Main execution tracking
- `pipeline_logs` - Detailed logging per agent
- `pipeline_configs` - Saved pipeline configurations
- RPC functions for status updates

### 2. Frontend Changes

#### Before (Custom WebSocket):
```typescript
// Old WebSocket connection
const { isConnected, lastMessage } = useWebSocket('/ws/pipeline', {
  onMessage: (data) => { /* handle message */ }
})
```

#### After (Supabase Real-time):
```typescript
// New Supabase subscription
const channel = supabase
  .channel(`pipeline:${organization.id}`)
  .on('postgres_changes', {
    event: '*',
    schema: 'public',
    table: 'pipeline_executions',
    filter: `organization_id=eq.${organization.id}`
  }, (payload) => { /* handle update */ })
  .subscribe()
```

### 3. Backend Changes

The WebSocket router now publishes to Supabase tables instead of just broadcasting:
- Updates are written to database tables
- Supabase handles real-time distribution
- Backward compatibility maintained for existing WebSocket clients

### 4. Benefits of Migration

- **Automatic Reconnection**: Supabase handles connection management
- **Data Persistence**: All updates stored in database
- **Row Level Security**: Automatic organization-based filtering
- **Better Scalability**: Leverages Supabase's infrastructure
- **Simpler Client Code**: No manual WebSocket management

## Migration Steps

### Step 1: Run Database Migrations
Execute the SQL script from `04-pipeline-management.md` to create tables and RLS policies.

### Step 2: Update Environment Variables
Add Supabase service key for backend operations:
```env
SUPABASE_SERVICE_KEY=your_service_key_here
```

### Step 3: Update Frontend Code
Replace WebSocket hooks with Supabase subscriptions as shown in the new `04-pipeline-management.md`.

### Step 4: Test Real-time Updates
1. Start a pipeline execution
2. Verify updates appear in real-time
3. Check database for persisted logs

## Rollback Plan

If you need to revert to the WebSocket version:
1. The old implementation is archived at `04-pipeline-management-websocket-version.md`
2. Backend WebSocket router maintains backward compatibility
3. Simply use the old frontend code to connect via WebSocket

## Support

For questions or issues with migration:
- Review the updated `04-pipeline-management.md` for complete implementation
- Check backend logs for Supabase publishing errors
- Verify RLS policies are correctly configured

## Timeline

- **Old Version**: Custom WebSocket implementation (archived)
- **New Version**: Supabase real-time (current)
- **Deprecation**: WebSocket endpoints will be removed in future releases
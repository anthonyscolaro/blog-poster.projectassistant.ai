# API Integration Improvements Based on LocalDocs Best Practices

## Current Implementation Review

After reviewing the frontend API integration against LocalDocs best practices, here's a comprehensive analysis with recommended improvements.

## ✅ What's Done Well

1. **Response Unwrapping**: Correctly handles wrapped API responses
2. **Native WebSocket**: Properly uses native WebSocket instead of Socket.IO
3. **Auth Headers**: Includes JWT token and organization context
4. **Mock Data Fallback**: Has development mode mock data
5. **Error Handling**: Basic error handling with try/catch
6. **Supabase Integration**: Uses Supabase client for auth

## 🔧 Improvements Needed

### 1. Environment Variable Management

**Issue**: Hardcoded Supabase URL and key in `client.ts`

**Fix Required**:
```typescript
// src/integrations/supabase/client.ts
const SUPABASE_URL = import.meta.env.VITE_SUPABASE_URL || "https://epftkydwdqerdlhvqili.supabase.co"
const SUPABASE_PUBLISHABLE_KEY = import.meta.env.VITE_SUPABASE_ANON_KEY || "eyJhbG..."

// Validate at startup
if (!SUPABASE_URL || !SUPABASE_PUBLISHABLE_KEY) {
  console.error('Missing required Supabase configuration')
}
```

**Create `.env.local`**:
```bash
VITE_SUPABASE_URL=https://epftkydwdqerdlhvqili.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbG...
VITE_API_URL=http://localhost:8088
VITE_WS_URL=ws://localhost:8088
```

### 2. Enhanced Error Handling with Retry Logic

**Current**: Basic error handling without retries

**Improvement**:
```typescript
// src/services/api.ts - Add exponential backoff
class ApiService {
  private async requestWithRetry<T>(
    endpoint: string,
    options: RequestInit = {},
    retries = 3
  ): Promise<T> {
    let lastError: Error | null = null
    
    for (let i = 0; i < retries; i++) {
      try {
        return await this.request<T>(endpoint, options)
      } catch (error) {
        lastError = error as Error
        
        // Don't retry on client errors (4xx)
        if (error.message?.includes('4')) {
          throw error
        }
        
        // Exponential backoff with jitter
        const delay = Math.min(1000 * Math.pow(2, i) + Math.random() * 1000, 10000)
        await new Promise(resolve => setTimeout(resolve, delay))
      }
    }
    
    throw lastError
  }
}
```

### 3. WebSocket Connection Health Monitoring

**Current**: Basic ping interval

**Improvement**:
```typescript
// src/services/websocket.ts - Add connection health monitoring
class WebSocketService {
  private connectionHealth = {
    lastPing: Date.now(),
    lastPong: Date.now(),
    latency: 0,
    isHealthy: true
  }
  
  private checkConnectionHealth() {
    const now = Date.now()
    const timeSinceLastPong = now - this.connectionHealth.lastPong
    
    if (timeSinceLastPong > 60000) { // 1 minute timeout
      this.connectionHealth.isHealthy = false
      this.reconnect()
    }
  }
  
  getConnectionHealth() {
    return this.connectionHealth
  }
}
```

### 4. Supabase Row Level Security Integration

**Missing**: Direct RLS usage for data queries

**Add**:
```typescript
// src/services/supabase-data.ts
import { supabase } from '@/integrations/supabase/client'

export class SupabaseDataService {
  // Use RLS for organization data isolation
  async getOrganizationData(orgId: string) {
    const { data, error } = await supabase
      .from('organizations')
      .select('*')
      .eq('id', orgId)
      .single()
    
    if (error) throw error
    return data
  }
  
  // Real-time subscriptions with RLS
  subscribeToChanges(table: string, callback: (payload: any) => void) {
    return supabase
      .channel(`${table}_changes`)
      .on('postgres_changes', { 
        event: '*', 
        schema: 'public', 
        table 
      }, callback)
      .subscribe()
  }
}
```

### 5. React Query Configuration Improvements

**Current**: Basic React Query setup

**Improvement**:
```typescript
// src/lib/query-client.ts
import { QueryClient } from '@tanstack/react-query'

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      gcTime: 1000 * 60 * 60, // 1 hour (was cacheTime)
      retry: (failureCount, error: any) => {
        // Don't retry on 4xx errors
        if (error?.status >= 400 && error?.status < 500) {
          return false
        }
        return failureCount < 3
      },
      refetchOnWindowFocus: false,
      refetchOnMount: true,
      refetchOnReconnect: 'always'
    },
    mutations: {
      retry: 1,
      onError: (error) => {
        console.error('Mutation error:', error)
        // Global error handling
      }
    }
  }
})
```

### 6. TypeScript Type Safety Improvements

**Issue**: Some `any` types in the implementation

**Fix**:
```typescript
// src/types/api.ts - Complete type definitions
export interface ApiError {
  message: string
  code?: string
  status?: number
  details?: Record<string, unknown>
}

// Replace all 'any' with specific types
export interface CostMetrics {
  totalCost: number
  breakdown: {
    llm: number
    storage: number
    api: number
  }
  period: 'daily' | 'monthly' | 'yearly'
}
```

### 7. Security Enhancements

**Add Content Security Policy headers**:
```typescript
// src/services/api.ts
private async getSecureHeaders(): Promise<Record<string, string>> {
  const headers = await getAuthHeaders()
  
  // Add security headers
  return {
    ...headers,
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'DENY',
    'X-XSS-Protection': '1; mode=block'
  }
}
```

### 8. Performance Optimizations

**Add request deduplication**:
```typescript
// src/services/api.ts
class ApiService {
  private pendingRequests = new Map<string, Promise<any>>()
  
  private async deduplicatedRequest<T>(
    key: string,
    requestFn: () => Promise<T>
  ): Promise<T> {
    if (this.pendingRequests.has(key)) {
      return this.pendingRequests.get(key)
    }
    
    const promise = requestFn().finally(() => {
      this.pendingRequests.delete(key)
    })
    
    this.pendingRequests.set(key, promise)
    return promise
  }
}
```

### 9. Error Boundary Implementation

**Add global error boundary**:
```typescript
// src/components/ErrorBoundary.tsx
import { Component, ErrorInfo, ReactNode } from 'react'

interface Props {
  children: ReactNode
  fallback?: ReactNode
}

interface State {
  hasError: boolean
  error?: Error
}

export class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false }
  
  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error }
  }
  
  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Uncaught error:', error, errorInfo)
    // Send to error tracking service
  }
  
  render() {
    if (this.state.hasError) {
      return this.props.fallback || <ErrorFallback error={this.state.error} />
    }
    
    return this.props.children
  }
}
```

### 10. Testing Implementation

**Add API integration tests**:
```typescript
// src/services/__tests__/api.test.ts
import { describe, it, expect, vi } from 'vitest'
import { apiService } from '../api'

describe('ApiService', () => {
  it('should unwrap successful responses', async () => {
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({
        success: true,
        data: { test: 'data' },
        message: 'Success'
      })
    })
    
    const result = await apiService.getHealth()
    expect(result).toEqual({ test: 'data' })
  })
  
  it('should handle wrapped errors', async () => {
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({
        success: false,
        error: 'Test error',
        message: 'Failed'
      })
    })
    
    await expect(apiService.getHealth()).rejects.toThrow('Test error')
  })
})
```

## Implementation Priority

### High Priority (Do First)
1. ✅ Environment variable management
2. ✅ Complete TypeScript type definitions
3. ✅ Enhanced error handling with retries
4. ✅ Security headers

### Medium Priority
5. ⏳ WebSocket health monitoring
6. ⏳ React Query configuration
7. ⏳ Error boundaries
8. ⏳ Request deduplication

### Low Priority (Nice to Have)
9. ⏹️ Testing implementation
10. ⏹️ Performance monitoring

## Configuration Files Needed

### 1. `.env.local` (Create this file)
```bash
# Supabase
VITE_SUPABASE_URL=https://epftkydwdqerdlhvqili.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# FastAPI Backend
VITE_API_URL=http://localhost:8088
VITE_WS_URL=ws://localhost:8088

# Stripe
VITE_STRIPE_PUBLISHABLE_KEY=pk_test_...

# App Config
VITE_APP_NAME=Blog-Poster
VITE_APP_URL=http://localhost:5173
```

### 2. `.env.example` (For team reference)
```bash
# Copy this to .env.local and fill in your values
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_supabase_key
VITE_API_URL=http://localhost:8088
VITE_WS_URL=ws://localhost:8088
VITE_STRIPE_PUBLISHABLE_KEY=your_stripe_key
VITE_APP_NAME=Blog-Poster
VITE_APP_URL=http://localhost:5173
```

## Summary

The current implementation is functional and follows many best practices, but needs improvements in:

1. **Environment Management**: Move from hardcoded values to env vars
2. **Error Handling**: Add retry logic and better error classification
3. **Type Safety**: Replace remaining `any` types
4. **Security**: Add proper headers and validation
5. **Performance**: Add request deduplication and caching

These improvements will make the frontend more robust, secure, and maintainable while following team best practices from LocalDocs.
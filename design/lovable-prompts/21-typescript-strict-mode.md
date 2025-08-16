# TypeScript Strict Mode & Type Safety Improvements

## Priority: CRITICAL - Must Complete First

## Overview
Enable TypeScript strict mode and fix all type safety issues to bring the codebase to enterprise standards. This will catch potential bugs and make the code more maintainable.

## Task 1: Enable Strict Mode in tsconfig.json

### Update: `tsconfig.json`
```json
{
  "files": [],
  "references": [
    { "path": "./tsconfig.app.json" },
    { "path": "./tsconfig.node.json" }
  ],
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    },
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitThis": true,
    "alwaysStrict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "skipLibCheck": true,
    "allowJs": false,
    "esModuleInterop": true,
    "resolveJsonModule": true
  }
}
```

## Task 2: Fix Common Type Issues

### Issue 1: Replace `any` types with proper interfaces

#### File: `src/pages/billing/Billing.tsx`
Replace:
```typescript
const [recentActivity, setRecentActivity] = useState<any[]>([]);
```

With:
```typescript
interface ActivityLog {
  id: string;
  action: string;
  created_at: string;
  user_id: string;
  organization_id: string;
  metadata?: Record<string, unknown>;
}

const [recentActivity, setRecentActivity] = useState<ActivityLog[]>([]);
```

#### File: `src/pages/team/Team.tsx`
Add proper types for all state and props:
```typescript
interface TeamStats {
  totalArticles: number;
  publishedArticles: number;
  avgSeoScore: number;
  totalCost: number;
  costPerArticle: number;
  activeContributors: number;
  topContributorId?: string;
  topContributorCount: number;
}

interface TeamMember {
  id: string;
  email: string;
  full_name: string | null;
  avatar_url: string | null;
  role: 'owner' | 'admin' | 'editor' | 'member' | 'viewer';
  created_at: string;
  last_activity_at: string | null;
  organization_id: string;
}
```

### Issue 2: Add return types to all functions

#### Pattern to follow:
```typescript
// Before:
const calculateScore = (data) => {
  return data.score * 100;
}

// After:
const calculateScore = (data: { score: number }): number => {
  return data.score * 100;
}
```

### Issue 3: Fix nullable types

#### Pattern to follow:
```typescript
// Before:
const userName = user.name; // user might be null

// After:
const userName = user?.name ?? 'Anonymous';
// OR
if (!user) {
  return <LoadingSpinner />;
}
const userName = user.name; // Now TypeScript knows user is not null
```

## Task 3: Create Type Definition Files

### Create: `src/types/database.ts`
```typescript
export interface Organization {
  id: string;
  name: string;
  created_at: string;
  updated_at: string;
  subscription_tier: 'free' | 'starter' | 'professional' | 'enterprise';
  subscription_status: 'active' | 'past_due' | 'canceled' | 'inactive';
  stripe_customer_id: string | null;
  stripe_subscription_id: string | null;
  monthly_article_limit: number;
  current_month_articles: number;
  current_month_cost: number;
  monthly_budget: number;
  team_members_used: number;
  team_members_limit: number;
}

export interface Profile {
  id: string;
  email: string;
  full_name: string | null;
  avatar_url: string | null;
  organization_id: string | null;
  role: UserRole;
  created_at: string;
  updated_at: string;
  last_activity_at: string | null;
}

export type UserRole = 'owner' | 'admin' | 'editor' | 'member' | 'viewer';

export interface Article {
  id: string;
  title: string;
  content: string;
  status: 'draft' | 'published' | 'scheduled';
  seo_score: number;
  word_count: number;
  created_at: string;
  updated_at: string;
  published_at: string | null;
  user_id: string;
  organization_id: string;
  generation_cost: number;
}

export interface Pipeline {
  id: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  agents_completed: string[];
  current_agent: string | null;
  error_message: string | null;
  started_at: string;
  completed_at: string | null;
  total_cost: number;
  article_id: string | null;
  user_id: string;
  organization_id: string;
}

export interface ApiKey {
  id: string;
  user_id: string;
  organization_id: string;
  provider: 'anthropic' | 'openai' | 'jina' | 'wordpress';
  encrypted_key: string;
  is_valid: boolean;
  last_validated: string | null;
  created_at: string;
  updated_at: string;
}
```

### Create: `src/types/supabase.ts`
```typescript
import { Database } from '@/integrations/supabase/types';

export type Tables<T extends keyof Database['public']['Tables']> = 
  Database['public']['Tables'][T]['Row'];

export type Enums<T extends keyof Database['public']['Enums']> = 
  Database['public']['Enums'][T];

// Helper types for common operations
export type InsertPayload<T extends keyof Database['public']['Tables']> = 
  Database['public']['Tables'][T]['Insert'];

export type UpdatePayload<T extends keyof Database['public']['Tables']> = 
  Database['public']['Tables'][T]['Update'];
```

## Task 4: Fix React Component Types

### Pattern for all components:
```typescript
import { FC, ReactNode } from 'react';

interface ComponentProps {
  children?: ReactNode;
  className?: string;
  onSomething?: (value: string) => void;
  data: SomeDataType;
}

export const Component: FC<ComponentProps> = ({ 
  children, 
  className, 
  onSomething, 
  data 
}) => {
  // Component implementation
};
```

## Task 5: Fix Hook Types

### Custom hooks pattern:
```typescript
// Before:
export const useAuth = () => {
  const [user, setUser] = useState(null);
  return { user };
}

// After:
interface AuthState {
  user: User | null;
  loading: boolean;
  error: Error | null;
}

interface AuthReturn extends AuthState {
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  updateProfile: (data: Partial<Profile>) => Promise<void>;
}

export const useAuth = (): AuthReturn => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);
  
  // Implementation
  
  return { 
    user, 
    loading, 
    error,
    login,
    logout,
    updateProfile
  };
}
```

## Task 6: Fix Query Types

### React Query pattern:
```typescript
import { useQuery, UseQueryResult } from '@tanstack/react-query';

// Define the return type
interface ArticlesData {
  articles: Article[];
  total: number;
}

// Use in query
const { data, error, isLoading }: UseQueryResult<ArticlesData, Error> = useQuery({
  queryKey: ['articles', organizationId],
  queryFn: async (): Promise<ArticlesData> => {
    const { data, error, count } = await supabase
      .from('articles')
      .select('*', { count: 'exact' })
      .eq('organization_id', organizationId);
    
    if (error) throw error;
    
    return {
      articles: data || [],
      total: count || 0
    };
  }
});
```

## Task 7: Fix Event Handler Types

### Pattern:
```typescript
import { ChangeEvent, FormEvent, MouseEvent } from 'react';

// Form submission
const handleSubmit = (e: FormEvent<HTMLFormElement>): void => {
  e.preventDefault();
  // Handle form
};

// Input change
const handleChange = (e: ChangeEvent<HTMLInputElement>): void => {
  setValue(e.target.value);
};

// Button click
const handleClick = (e: MouseEvent<HTMLButtonElement>): void => {
  e.stopPropagation();
  // Handle click
};
```

## Testing Your Changes

After enabling strict mode, you'll see errors. Fix them in this order:

1. **Type errors** - Add missing types
2. **Null checks** - Add proper null handling
3. **Implicit any** - Add explicit types
4. **Unused variables** - Remove or prefix with underscore
5. **Missing returns** - Add return statements

## Common Fixes

### Handling possible null/undefined:
```typescript
// Option 1: Optional chaining
const name = user?.profile?.name ?? 'Unknown';

// Option 2: Type guard
if (user && user.profile) {
  const name = user.profile.name;
}

// Option 3: Non-null assertion (use sparingly)
const name = user!.profile!.name; // Only if you're SURE it exists
```

### Handling union types:
```typescript
type Status = 'idle' | 'loading' | 'success' | 'error';

const getStatusColor = (status: Status): string => {
  switch (status) {
    case 'idle':
      return 'gray';
    case 'loading':
      return 'blue';
    case 'success':
      return 'green';
    case 'error':
      return 'red';
    default:
      // This ensures all cases are handled
      const exhaustive: never = status;
      return exhaustive;
  }
};
```

## Success Criteria

- [ ] TypeScript strict mode enabled
- [ ] Zero TypeScript errors
- [ ] No `any` types remaining
- [ ] All functions have return types
- [ ] All components properly typed
- [ ] All hooks properly typed
- [ ] All event handlers typed
- [ ] Type definition files created

## Benefits

1. **Catch bugs at compile time** instead of runtime
2. **Better IntelliSense** in VS Code
3. **Self-documenting code** through types
4. **Easier refactoring** with confidence
5. **Enterprise-grade code quality**

This will make your codebase more maintainable and impressive to enterprise clients who expect type-safe code.
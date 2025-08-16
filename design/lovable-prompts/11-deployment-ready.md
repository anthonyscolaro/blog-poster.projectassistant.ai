# Lovable Prompt: Production Deployment & Optimization

## Business Context:
Preparing the Blog-Poster dashboard for production deployment with performance optimizations, security hardening, environment configuration, and Digital Ocean deployment setup. Focus on production-grade build optimization, CDN integration, monitoring, and scalability.

## User Story:
"As a system administrator, I want the dashboard deployed to production with optimal performance, security best practices, environment-specific configurations, and comprehensive monitoring to ensure reliable operation."

## Technical Requirements:
- Production build optimization and code splitting
- Environment variable management for different stages
- Security headers and CSP configuration
- Performance monitoring and analytics
- CDN integration and asset optimization
- Digital Ocean deployment configuration
- CI/CD pipeline setup
- Health checks and monitoring

## Prompt for Lovable:

Configure the Blog-Poster dashboard for production deployment with comprehensive optimizations, security hardening, and Digital Ocean integration.

### Environment Configuration

```typescript
// src/config/environment.ts
interface Environment {
  API_BASE_URL: string
  WS_BASE_URL: string
  ENVIRONMENT: 'development' | 'staging' | 'production'
  VERSION: string
  SENTRY_DSN?: string
  ANALYTICS_ID?: string
  CDN_BASE_URL?: string
}

const getEnvironment = (): Environment => {
  const env = import.meta.env.MODE || 'development'
  
  const config: Record<string, Environment> = {
    development: {
      API_BASE_URL: 'http://localhost:8088',
      WS_BASE_URL: 'ws://localhost:8088',
      ENVIRONMENT: 'development',
      VERSION: import.meta.env.VITE_VERSION || 'dev',
    },
    staging: {
      API_BASE_URL: 'https://staging-api.servicedogus.com',
      WS_BASE_URL: 'wss://staging-api.servicedogus.com',
      ENVIRONMENT: 'staging',
      VERSION: import.meta.env.VITE_VERSION || '1.0.0',
      SENTRY_DSN: import.meta.env.VITE_SENTRY_DSN,
      ANALYTICS_ID: import.meta.env.VITE_ANALYTICS_ID,
    },
    production: {
      API_BASE_URL: 'https://api.servicedogus.com',
      WS_BASE_URL: 'wss://api.servicedogus.com',
      ENVIRONMENT: 'production',
      VERSION: import.meta.env.VITE_VERSION || '1.0.0',
      SENTRY_DSN: import.meta.env.VITE_SENTRY_DSN,
      ANALYTICS_ID: import.meta.env.VITE_ANALYTICS_ID,
      CDN_BASE_URL: 'https://cdn.servicedogus.com',
    },
  }

  return config[env] || config.development
}

export const environment = getEnvironment()
export default environment
```

### Production Vite Configuration

```typescript
// vite.config.ts (updated for production)
import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'
import { resolve } from 'path'
import { visualizer } from 'rollup-plugin-visualizer'

export default defineConfig(({ command, mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  
  return {
    plugins: [
      react({
        // Enable React Fast Refresh
        fastRefresh: true,
      }),
      // Bundle analyzer in production
      ...(mode === 'production' ? [
        visualizer({
          filename: 'dist/stats.html',
          open: true,
          gzipSize: true,
        }),
      ] : []),
    ],
    resolve: {
      alias: {
        '@': resolve(__dirname, './src'),
        '@components': resolve(__dirname, './src/components'),
        '@pages': resolve(__dirname, './src/pages'),
        '@services': resolve(__dirname, './src/services'),
        '@hooks': resolve(__dirname, './src/hooks'),
        '@types': resolve(__dirname, './src/types'),
        '@utils': resolve(__dirname, './src/utils'),
        '@config': resolve(__dirname, './src/config'),
      },
    },
    define: {
      __APP_VERSION__: JSON.stringify(env.npm_package_version),
      __BUILD_DATE__: JSON.stringify(new Date().toISOString()),
    },
    server: {
      port: 3000,
      host: true,
      proxy: {
        '/api': {
          target: env.VITE_API_URL || 'http://localhost:8088',
          changeOrigin: true,
          secure: false,
        },
        '/ws': {
          target: env.VITE_WS_URL || 'ws://localhost:8088',
          ws: true,
        },
      },
    },
    preview: {
      port: 3000,
      host: true,
    },
    build: {
      target: 'es2020',
      outDir: 'dist',
      assetsDir: 'assets',
      sourcemap: mode !== 'production',
      minify: 'terser',
      terserOptions: {
        compress: {
          drop_console: mode === 'production',
          drop_debugger: true,
        },
      },
      rollupOptions: {
        output: {
          manualChunks: {
            // Vendor chunks
            vendor: ['react', 'react-dom'],
            router: ['react-router-dom'],
            query: ['@tanstack/react-query'],
            ui: ['lucide-react'],
            charts: ['recharts'],
            utils: ['date-fns', 'clsx'],
            // Socket.io as separate chunk due to size
            socket: ['socket.io-client'],
          },
          chunkFileNames: 'assets/js/[name]-[hash].js',
          entryFileNames: 'assets/js/[name]-[hash].js',
          assetFileNames: ({ name }) => {
            if (/\.(gif|jpe?g|png|svg)$/.test(name ?? '')) {
              return 'assets/images/[name]-[hash][extname]'
            }
            if (/\.css$/.test(name ?? '')) {
              return 'assets/css/[name]-[hash][extname]'
            }
            return 'assets/[name]-[hash][extname]'
          },
        },
      },
      // Chunk size warnings
      chunkSizeWarningLimit: 1000,
    },
    optimizeDeps: {
      include: [
        'react',
        'react-dom',
        'react-router-dom',
        '@tanstack/react-query',
        'socket.io-client',
        'lucide-react',
        'date-fns',
        'clsx',
      ],
    },
  }
})
```

### Environment Files

```bash
# .env.local (development)
VITE_MODE=development
VITE_API_URL=http://localhost:8088
VITE_WS_URL=ws://localhost:8088
VITE_VERSION=dev

# .env.staging
VITE_MODE=staging
VITE_API_URL=https://staging-api.servicedogus.com
VITE_WS_URL=wss://staging-api.servicedogus.com
VITE_SENTRY_DSN=your_sentry_dsn_here
VITE_ANALYTICS_ID=your_analytics_id_here
VITE_VERSION=1.0.0-staging

# .env.production
VITE_MODE=production
VITE_API_URL=https://api.servicedogus.com
VITE_WS_URL=wss://api.servicedogus.com
VITE_SENTRY_DSN=your_production_sentry_dsn
VITE_ANALYTICS_ID=your_production_analytics_id
VITE_VERSION=1.0.0
```

### Performance Optimizations

```typescript
// src/components/LazyComponents.tsx
import { lazy, Suspense } from 'react'
import { LoadingSpinner } from '@/components/LoadingSpinner'

// Lazy load heavy components
export const Dashboard = lazy(() => import('@/pages/Dashboard'))
export const Pipeline = lazy(() => import('@/pages/Pipeline'))
export const Articles = lazy(() => import('@/pages/Articles'))
export const ArticleDetail = lazy(() => import('@/pages/ArticleDetail'))
export const Monitoring = lazy(() => import('@/pages/Monitoring'))
export const Settings = lazy(() => import('@/pages/Settings'))

// Higher-order component for lazy loading
export function withSuspense<T extends object>(Component: React.ComponentType<T>) {
  return (props: T) => (
    <Suspense fallback={
      <div className="flex items-center justify-center h-64">
        <LoadingSpinner size="lg" />
      </div>
    }>
      <Component {...props} />
    </Suspense>
  )
}

// Pre-wrapped components
export const LazyDashboard = withSuspense(Dashboard)
export const LazyPipeline = withSuspense(Pipeline)
export const LazyArticles = withSuspense(Articles)
export const LazyArticleDetail = withSuspense(ArticleDetail)
export const LazyMonitoring = withSuspense(Monitoring)
export const LazySettings = withSuspense(Settings)
```

```typescript
// src/hooks/usePreload.ts
import { useEffect } from 'react'

// Preload critical routes
export function usePreloadRoutes() {
  useEffect(() => {
    // Preload Dashboard after initial load
    const preloadDashboard = () => import('@/pages/Dashboard')
    
    // Preload after a short delay to not block initial render
    const timer = setTimeout(preloadDashboard, 1000)
    
    return () => clearTimeout(timer)
  }, [])
}

// Preload on hover for better UX
export function useHoverPreload(routePath: string) {
  const preload = () => {
    switch (routePath) {
      case '/dashboard':
        import('@/pages/Dashboard')
        break
      case '/pipeline':
        import('@/pages/Pipeline')
        break
      case '/articles':
        import('@/pages/Articles')
        break
      case '/monitoring':
        import('@/pages/Monitoring')
        break
      case '/settings':
        import('@/pages/Settings')
        break
    }
  }

  return { preload }
}
```

### Security Configuration

```typescript
// src/utils/security.ts
export const securityHeaders = {
  'Content-Security-Policy': [
    "default-src 'self'",
    "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.servicedogus.com",
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
    "font-src 'self' https://fonts.gstatic.com",
    "img-src 'self' data: https: blob:",
    "connect-src 'self' https://api.servicedogus.com wss://api.servicedogus.com https://sentry.io",
    "frame-ancestors 'none'",
    "base-uri 'self'",
    "form-action 'self'",
  ].join('; '),
  'X-Frame-Options': 'DENY',
  'X-Content-Type-Options': 'nosniff',
  'Referrer-Policy': 'strict-origin-when-cross-origin',
  'Permissions-Policy': 'camera=(), microphone=(), location=(), payment=()',
}

// Sanitize user input
export function sanitizeInput(input: string): string {
  return input
    .replace(/[<>]/g, '') // Remove potential HTML tags
    .trim()
    .slice(0, 1000) // Limit length
}

// Validate environment variables
export function validateEnvironment() {
  const required = ['VITE_API_URL', 'VITE_WS_URL']
  const missing = required.filter(key => !import.meta.env[key])
  
  if (missing.length > 0) {
    console.error('Missing required environment variables:', missing)
    throw new Error(`Missing environment variables: ${missing.join(', ')}`)
  }
}
```

### Monitoring and Analytics

```typescript
// src/services/monitoring.ts
import environment from '@/config/environment'

interface ErrorReport {
  message: string
  stack?: string
  url: string
  timestamp: number
  userAgent: string
  userId?: string
}

interface PerformanceMetric {
  name: string
  value: number
  timestamp: number
  metadata?: Record<string, any>
}

class MonitoringService {
  private isProduction = environment.ENVIRONMENT === 'production'

  // Error reporting
  reportError(error: Error, context?: Record<string, any>) {
    if (!this.isProduction) {
      console.error('Error:', error, context)
      return
    }

    const report: ErrorReport = {
      message: error.message,
      stack: error.stack,
      url: window.location.href,
      timestamp: Date.now(),
      userAgent: navigator.userAgent,
      ...context,
    }

    // Send to monitoring service (Sentry, LogRocket, etc.)
    if (environment.SENTRY_DSN) {
      this.sendToSentry(report)
    }
  }

  // Performance metrics
  reportPerformance(metric: PerformanceMetric) {
    if (!this.isProduction) {
      console.log('Performance metric:', metric)
      return
    }

    // Send to analytics service
    if (environment.ANALYTICS_ID) {
      this.sendToAnalytics(metric)
    }
  }

  // User interaction tracking
  trackEvent(event: string, properties?: Record<string, any>) {
    if (!this.isProduction) {
      console.log('Event tracked:', event, properties)
      return
    }

    if (environment.ANALYTICS_ID) {
      // Send to analytics platform
      this.sendToAnalytics({
        name: event,
        value: 1,
        timestamp: Date.now(),
        metadata: properties,
      })
    }
  }

  private sendToSentry(report: ErrorReport) {
    // Implement Sentry integration
    fetch(`https://sentry.io/api/projects/blog-poster/store/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Sentry-Auth': `Sentry sentry_key=${environment.SENTRY_DSN}`,
      },
      body: JSON.stringify(report),
    }).catch(console.error)
  }

  private sendToAnalytics(metric: PerformanceMetric) {
    // Implement analytics integration
    if (typeof gtag !== 'undefined') {
      gtag('event', metric.name, {
        value: metric.value,
        custom_parameter: metric.metadata,
      })
    }
  }

  // Health check endpoint
  async checkHealth() {
    try {
      const response = await fetch('/api/health')
      const health = await response.json()
      
      this.reportPerformance({
        name: 'api_health_check',
        value: response.status === 200 ? 1 : 0,
        timestamp: Date.now(),
        metadata: health,
      })
      
      return health
    } catch (error) {
      this.reportError(error as Error, { context: 'health_check' })
      throw error
    }
  }
}

export const monitoring = new MonitoringService()
export default monitoring
```

### Service Worker for Caching

```typescript
// public/sw.js
const CACHE_NAME = 'blog-poster-v1.0.0'
const urlsToCache = [
  '/',
  '/static/css/main.css',
  '/static/js/main.js',
  '/manifest.json',
]

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(urlsToCache))
  )
})

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((response) => {
        // Return cached version or fetch from network
        return response || fetch(event.request)
      })
  )
})

// src/utils/registerSW.ts
export function registerServiceWorker() {
  if ('serviceWorker' in navigator && import.meta.env.PROD) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('/sw.js')
        .then((registration) => {
          console.log('SW registered: ', registration)
        })
        .catch((registrationError) => {
          console.log('SW registration failed: ', registrationError)
        })
    })
  }
}
```

### Digital Ocean Deployment Configuration

```yaml
# .do/app.yaml
name: blog-poster-dashboard
services:
- name: web
  source_dir: /
  github:
    repo: your-org/blog-poster
    branch: main
    deploy_on_push: true
  run_command: npm run preview
  environment_slug: node-js
  instance_count: 1
  instance_size_slug: basic-xxs
  http_port: 3000
  routes:
  - path: /
  health_check:
    http_path: /health
    initial_delay_seconds: 10
    period_seconds: 10
    timeout_seconds: 5
    failure_threshold: 3
  envs:
  - key: NODE_ENV
    value: production
  - key: VITE_MODE
    value: production
  - key: VITE_API_URL
    value: https://api.servicedogus.com
  - key: VITE_WS_URL
    value: wss://api.servicedogus.com
  - key: VITE_SENTRY_DSN
    value: ${SENTRY_DSN}
    type: SECRET
  - key: VITE_ANALYTICS_ID
    value: ${ANALYTICS_ID}
    type: SECRET

# Build configuration
- name: build
  source_dir: /
  github:
    repo: your-org/blog-poster
    branch: main
  build_command: |
    npm ci --only=production
    npm run build
  instance_size_slug: basic-xxs
```

### Docker Configuration for Deployment

```dockerfile
# Dockerfile
FROM node:18-alpine as builder

WORKDIR /app

# Copy package files
COPY package*.json ./
COPY yarn.lock ./

# Install dependencies
RUN yarn install --frozen-lockfile

# Copy source code
COPY . .

# Build the application
RUN yarn build

# Production stage
FROM nginx:alpine

# Copy built assets
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Add health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost/health || exit 1

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

```nginx
# nginx.conf
events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;
    
    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/javascript
        application/xml+rss
        application/json;

    # Security headers
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; connect-src 'self' https: wss:;" always;

    server {
        listen 80;
        server_name _;
        root /usr/share/nginx/html;
        index index.html;

        # Handle client-side routing
        location / {
            try_files $uri $uri/ /index.html;
        }

        # Cache static assets
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }

        # Health check endpoint
        location /health {
            access_log off;
            return 200 "healthy\n";
            add_header Content-Type text/plain;
        }

        # Proxy API requests
        location /api/ {
            proxy_pass http://api.servicedogus.com/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # WebSocket proxy
        location /ws/ {
            proxy_pass http://api.servicedogus.com/ws/;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

### GitHub Actions CI/CD

```yaml
# .github/workflows/deploy.yml
name: Deploy to Digital Ocean

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
        cache: 'yarn'
    
    - name: Install dependencies
      run: yarn install --frozen-lockfile
    
    - name: Run linting
      run: yarn lint
    
    - name: Run tests
      run: yarn test
    
    - name: Build application
      run: yarn build
      env:
        VITE_MODE: production
        VITE_API_URL: ${{ secrets.API_URL }}
        VITE_WS_URL: ${{ secrets.WS_URL }}

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to Digital Ocean App Platform
      uses: digitalocean/app_action@v1.1.5
      with:
        app_name: blog-poster-dashboard
        token: ${{ secrets.DIGITALOCEAN_ACCESS_TOKEN }}
```

### Performance Monitoring Component

```typescript
// src/components/PerformanceMonitor.tsx
import { useEffect } from 'react'
import monitoring from '@/services/monitoring'

export function PerformanceMonitor() {
  useEffect(() => {
    // Monitor Core Web Vitals
    if ('web-vitals' in window) {
      import('web-vitals').then(({ getCLS, getFID, getFCP, getLCP, getTTFB }) => {
        getCLS(monitoring.reportPerformance)
        getFID(monitoring.reportPerformance)
        getFCP(monitoring.reportPerformance)
        getLCP(monitoring.reportPerformance)
        getTTFB(monitoring.reportPerformance)
      })
    }

    // Monitor navigation timing
    if ('performance' in window && 'getEntriesByType' in window.performance) {
      const navigationEntries = performance.getEntriesByType('navigation')
      if (navigationEntries.length > 0) {
        const entry = navigationEntries[0] as PerformanceNavigationTiming
        monitoring.reportPerformance({
          name: 'page_load_time',
          value: entry.loadEventEnd - entry.navigationStart,
          timestamp: Date.now(),
        })
      }
    }

    // Monitor resource loading
    const observer = new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        if (entry.entryType === 'resource') {
          const resourceEntry = entry as PerformanceResourceTiming
          monitoring.reportPerformance({
            name: 'resource_load_time',
            value: resourceEntry.responseEnd - resourceEntry.startTime,
            timestamp: Date.now(),
            metadata: {
              name: resourceEntry.name,
              type: resourceEntry.initiatorType,
            },
          })
        }
      }
    })

    observer.observe({ entryTypes: ['resource'] })

    return () => {
      observer.disconnect()
    }
  }, [])

  return null // This component doesn't render anything
}
```

**Success Criteria:**
- Production-optimized build with code splitting
- Environment-specific configuration management
- Security headers and CSP implementation
- Performance monitoring and error reporting
- Service worker for offline capabilities
- Digital Ocean deployment configuration
- CI/CD pipeline with automated testing
- Health checks and monitoring endpoints
- CDN integration and asset optimization
- Comprehensive logging and analytics

This configuration ensures the Blog-Poster dashboard is production-ready with enterprise-grade performance, security, and monitoring capabilities.
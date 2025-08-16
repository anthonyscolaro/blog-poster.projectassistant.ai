# Lovable Prompt: Project Base Setup (React + Vite)

## Business Context:
Setting up the Blog-Poster dashboard as a professional SEO content generation platform for ServiceDogUS. This React + Vite application will manage a 5-agent orchestration system that automates content creation while maintaining legal accuracy for service dog industry content.

## User Story:
"As a content manager, I want a modern, responsive dashboard that lets me monitor and control the entire content generation pipeline from competitor research to WordPress publishing."

## Technical Requirements:
- React 19+ with Vite 5+ build system
- TailwindCSS with custom purple gradient theme
- Dark/light mode toggle
- Responsive design (mobile-first)
- WebSocket support for real-time updates
- React 19 features: Server Components, improved Suspense, use() hook, Actions

## Prompt for Lovable:

🚨 CRITICAL REQUIREMENT: Use React + Vite ONLY
- This MUST be a React application with Vite build system (Lovable's default)
- Use standard React components and hooks
- Use React Router for navigation
- Ensure package.json includes "react": "^19.0.0" and "vite": "^5.0.0"

Create a React 19 + Vite project setup for the Blog-Poster SEO content generation dashboard. This is a professional content automation platform that orchestrates 5 AI agents to generate legally-compliant, SEO-optimized articles for the service dog industry.

**React 19 Features to Leverage:**
- **Server Components**: Enhanced performance with server-side rendering capabilities
- **Improved Suspense**: Better handling of async components and data fetching
- **use() Hook**: New hook for consuming promises and context values
- **Actions**: Form handling and mutations with automatic pending states
- **Enhanced Hydration**: Faster initial page loads and better SEO
- **Async Components**: Components that can await data before rendering

**Project Configuration:**

### Package.json Setup
```json
{
  "name": "blog-poster-dashboard",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0"
  },
  "dependencies": {
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "react-router-dom": "^6.26.0",
    "@tanstack/react-query": "^5.56.0",
    "@supabase/supabase-js": "^2.39.0",
    "zustand": "^4.5.0",
    "recharts": "^2.10.0",
    "lucide-react": "^0.303.0",
    "clsx": "^2.1.0",
    "date-fns": "^3.3.0",
    "socket.io-client": "^4.6.0",
    "@stripe/stripe-js": "^2.4.0",
    "@stripe/react-stripe-js": "^2.4.0",
    "react-hot-toast": "^2.4.1",
    "framer-motion": "^11.5.0",
    "react-hook-form": "^7.53.0",
    "@hookform/resolvers": "^3.3.2",
    "zod": "^3.22.4",
    "react-markdown": "^9.0.1",
    "react-syntax-highlighter": "^15.5.0",
    "react-countup": "^6.5.0",
    "react-intersection-observer": "^9.5.3"
  },
  "devDependencies": {
    "@types/react": "^19.0.0",
    "@types/react-dom": "^19.0.0",
    "@typescript-eslint/eslint-plugin": "^6.0.0",
    "@typescript-eslint/parser": "^6.0.0",
    "@vitejs/plugin-react": "^4.2.0",
    "autoprefixer": "^10.4.0",
    "eslint": "^8.56.0",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.0",
    "postcss": "^8.4.0",
    "tailwindcss": "^3.4.0",
    "typescript": "^5.3.0",
    "vite": "^5.0.0"
  }
}
```

### TailwindCSS Configuration with Custom Theme
```typescript
// tailwind.config.js
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f5f3ff',
          100: '#ede9fe',
          200: '#ddd6fe',
          300: '#c4b5fd',
          400: '#a78bfa',
          500: '#8b5cf6',
          600: '#7c3aed',
          700: '#6d28d9',
          800: '#5b21b6',
          900: '#4c1d95',
          950: '#2e1065',
        },
        dashboard: {
          bg: '#f8fafc',
          dark: '#0f172a',
          card: '#ffffff',
          'card-dark': '#1e293b',
        }
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'slide-in': 'slideIn 0.3s ease-out',
        'fade-in': 'fadeIn 0.5s ease-out',
      },
      keyframes: {
        slideIn: {
          '0%': { transform: 'translateX(-100%)' },
          '100%': { transform: 'translateX(0)' },
        },
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
      },
      backgroundImage: {
        'purple-gradient': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'success-gradient': 'linear-gradient(135deg, #667eea 0%, #48bb78 100%)',
      },
    },
  },
  plugins: [],
}
```

### Vite Configuration
```typescript
// vite.config.ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@components': path.resolve(__dirname, './src/components'),
      '@pages': path.resolve(__dirname, './src/pages'),
      '@services': path.resolve(__dirname, './src/services'),
      '@hooks': path.resolve(__dirname, './src/hooks'),
      '@types': path.resolve(__dirname, './src/types'),
      '@utils': path.resolve(__dirname, './src/utils'),
    },
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8088',
        changeOrigin: true,
      },
      '/ws': {
        target: 'ws://localhost:8088',
        ws: true,
      },
    },
  },
})
```

### TypeScript Configuration
```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"],
      "@components/*": ["./src/components/*"],
      "@pages/*": ["./src/pages/*"],
      "@services/*": ["./src/services/*"],
      "@hooks/*": ["./src/hooks/*"],
      "@types/*": ["./src/types/*"],
      "@utils/*": ["./src/utils/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

### Global Styles
```css
/* src/index.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
  }
}

@layer utilities {
  .animate-slide-in {
    animation: slideIn 0.3s ease-out;
  }

  .animate-fade-in {
    animation: fadeIn 0.5s ease-out;
  }

  .scrollbar-thin {
    scrollbar-width: thin;
    scrollbar-color: rgb(203 213 225) transparent;
  }

  .dark .scrollbar-thin {
    scrollbar-color: rgb(51 65 85) transparent;
  }
}

/* Custom scrollbar styles */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background-color: rgb(203 213 225);
  border-radius: 4px;
}

.dark ::-webkit-scrollbar-thumb {
  background-color: rgb(51 65 85);
}

/* Loading spinner */
.spinner {
  border: 2px solid rgba(139, 92, 246, 0.1);
  border-left-color: rgb(139, 92, 246);
  border-radius: 50%;
  width: 20px;
  height: 20px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
```

### Basic Folder Structure
Create the following directory structure in `src/`:

```
src/
├── components/
│   ├── layout/
│   │   ├── PublicLayout.tsx
│   │   ├── AppLayout.tsx
│   │   └── AdminLayout.tsx
│   ├── ProtectedRoute.tsx
│   └── AdminRoute.tsx
├── contexts/
│   ├── ThemeContext.tsx
│   └── AuthContext.tsx
├── pages/
│   ├── public/
│   ├── auth/
│   ├── onboarding/
│   ├── dashboard/
│   ├── pipeline/
│   ├── articles/
│   ├── team/
│   ├── billing/
│   ├── settings/
│   ├── analytics/
│   ├── monitoring/
│   └── admin/
├── hooks/
├── services/
├── types/
├── utils/
├── App.tsx
├── main.tsx
└── index.css
```

### Theme Context Provider
```typescript
// src/contexts/ThemeContext.tsx
import { createContext, useContext, useEffect, useState } from 'react'

interface ThemeContextType {
  theme: 'light' | 'dark'
  toggleTheme: () => void
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined)

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<'light' | 'dark'>(() => {
    const saved = localStorage.getItem('theme')
    return (saved as 'light' | 'dark') || 'light'
  })

  useEffect(() => {
    localStorage.setItem('theme', theme)
    document.documentElement.classList.toggle('dark', theme === 'dark')
  }, [theme])

  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light')
  }

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  )
}

export function useTheme() {
  const context = useContext(ThemeContext)
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider')
  }
  return context
}
```

### Next Steps:
After setting up this base configuration:

1. Refer to **01b-routing-setup.md** for complete router configuration and all page components
2. Test the development server with `npm run dev`
3. Verify all dependencies install correctly
4. Confirm dark/light mode toggle works
5. Ensure TypeScript compilation succeeds

This base setup provides the foundation for a professional React + Vite application with all necessary build tools, styling, and project structure configured correctly.
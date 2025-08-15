# Lovable Prompt: Project Setup Overview

## Business Context:
Setting up the Blog-Poster dashboard as a professional SEO content generation platform for ServiceDogUS. This React + Vite application will manage a 5-agent orchestration system that automates content creation while maintaining legal accuracy for service dog industry content.

## User Story:
"As a content manager, I want a modern, responsive dashboard that lets me monitor and control the entire content generation pipeline from competitor research to WordPress publishing."

## Setup Instructions:

**⚠️ IMPORTANT: This file has been split into focused, manageable parts for Lovable:**

### 📋 Step 1: Basic Project Setup
**Use file: `01a-project-base.md`**
- Package.json with all dependencies
- Vite & TypeScript configuration
- TailwindCSS with purple gradient theme
- Basic folder structure
- Theme context provider

### 📋 Step 2: Complete Routing & Pages
**Use file: `01b-routing-setup.md`**
- Complete App.tsx with router setup
- All layout components (PublicLayout, AppLayout, AdminLayout)
- Auth context provider
- Protected route components
- ALL page components (every single route)

## Implementation Order:

1. **First**: Use `01a-project-base.md` to set up the foundation
2. **Second**: Use `01b-routing-setup.md` to implement complete routing
3. **Test**: Verify all routes work without 404 errors

## Technical Requirements:
- React 19+ with Vite 5+ build system
- TailwindCSS with custom purple gradient theme
- Dark/light mode toggle
- Responsive design (mobile-first)
- WebSocket support for real-time updates
- Complete routing with NO 404 errors
- TypeScript throughout

## Final Instructions for Lovable:

**⚠️ IMPORTANT: Use the split files in this order:**

1. **Start with file: `01a-project-base.md`**
   - Contains all package dependencies, configurations, and base setup
   - Follow it exactly for the foundation

2. **Then use file: `01b-routing-setup.md`** 
   - Contains complete router setup and ALL page components
   - Every single page must be created to avoid 404 errors

## Success Criteria:
- Project builds without errors using `npm run dev`
- All routes work without 404 errors  
- Dark/light mode toggle works
- Purple gradient theme applied consistently
- Responsive sidebar navigation
- All placeholder pages display correctly
- TypeScript compilation succeeds

This modular approach ensures the project stays under Lovable's character limits while providing complete functionality.
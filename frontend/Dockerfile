# Multi-stage Dockerfile for Blog-Poster Frontend
# Stage 1: Development
FROM node:20-alpine AS development

# Set working directory
WORKDIR /app

# Install dependencies for better compatibility
RUN apk add --no-cache python3 make g++

# Copy package files
COPY package*.json ./

# Install dependencies (with legacy peer deps for React 19 compatibility)
RUN npm ci --legacy-peer-deps

# Copy application files
COPY . .

# Expose Vite dev server port
EXPOSE 5173

# Start development server with host binding for Docker
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

# Stage 2: Build
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies (with legacy peer deps for React 19 compatibility)
RUN npm ci --legacy-peer-deps

# Copy application files
COPY . .

# Build the application
RUN npm run build

# Stage 3: Production with nginx
FROM nginx:alpine AS production

# Copy custom nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy built application from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Expose HTTP port
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
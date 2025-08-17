#!/bin/bash
echo "Starting Blog Poster API..."
echo "Environment: ${ENVIRONMENT:-not set}"
echo "Database URL: ${DATABASE_URL:0:30}..." # Show first 30 chars only for security
echo "Python version: $(python3 --version)"
echo "Working directory: $(pwd)"
echo "Files in directory:"
ls -la

echo "Starting uvicorn..."
exec uvicorn app:app --host 0.0.0.0 --port 8088 --log-level info
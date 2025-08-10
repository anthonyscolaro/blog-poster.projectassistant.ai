FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create data directories
RUN mkdir -p /data/competitor-content/raw \
    /data/competitor-content/md \
    /data/competitor-content/metadata \
    /data/generated-articles/drafts \
    /data/generated-articles/published \
    /data/logs/monitoring \
    /data/logs/generation \
    /data/logs/publishing \
    /data/backups

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8088/docs || exit 1

# Run the application
CMD ["uvicorn", "fast_api_tool_shim_pydantic_schemas_for_article_generation_agent:app", "--host", "0.0.0.0", "--port", "8088"]
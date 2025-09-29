# Use official Python slim image
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends git curl && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/*

# Set working directory
WORKDIR /app

# Copy only requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy BentoML bento files and your source code
COPY bentofile.yaml .
COPY src/ ./src/
COPY k8s/ ./k8s/

# Expose the port your service will run on
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:3000/healthz || exit 1

# ENTRYPOINT: serve the BentoML service directly
# BentoML will build the Bento automatically at container startup
CMD ["bentoml", "serve", "src.service:LLMInference", "--host", "0.0.0.0", "--port", "3000"]

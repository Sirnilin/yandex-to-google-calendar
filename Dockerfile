FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directories for data persistence
RUN mkdir -p /app/data

# Set environment variables
ENV PYTHONPATH=/app
ENV GOOGLE_CREDENTIALS_FILE=/app/data/credentials.json
ENV GOOGLE_TOKEN_FILE=/app/data/token.json
ENV STATE_FILE=/app/data/sync_state.json

# Expose volume for data persistence
VOLUME ["/app/data"]

# Default command
CMD ["python", "main.py", "continuous"]
# Use Astral image to include uv
FROM ghcr.io/astral-sh/uv:python3.13-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies first
RUN apk update && apk add --no-cache \
    gcc

# Copy requirements
COPY pyproject.toml .
COPY uv.lock .

# Install Python dependencies
RUN uv sync --locked --no-dev

# Copy FastAPI application
COPY . .

# Expose port (default for FastAPI)
EXPOSE 8000

# Run the FastAPI application
CMD ["uv", "run", "--", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
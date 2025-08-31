# LangChain Sandbox MCP Server Docker Image
FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install Deno (required for LangChain Sandbox)
ENV DENO_INSTALL=/root/.deno
ENV PATH=$DENO_INSTALL/bin:$PATH
RUN curl -fsSL https://deno.land/install.sh | sh

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml ./
COPY src/ ./src/

# Install Python dependencies
RUN pip install --no-cache-dir uv && \
    uv pip install --system langchain-sandbox>=0.0.6 \
    fastmcp>=2.11.3 \
    pytz \
    pydantic \
    uvicorn \
    structlog

# Environment variables
ENV PYTHONPATH=/app
ENV IS_DOCKER=true

# Expose port
EXPOSE 8035

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8035/health || exit 1

# Start the server
CMD ["python", "-m", "src.mcp.servers.langchain_sandbox_server", \
     "--host", "0.0.0.0", \
     "--port", "8035", \
     "--debug"]
# Stage 1: Build the frontend assets
FROM node:22-alpine AS frontend-builder
WORKDIR /app

# Copy package files and configuration needed for npm ci
COPY a2a-inspector/frontend/package*.json ./
COPY a2a-inspector/frontend/tsconfig.json ./
COPY a2a-inspector/frontend/src ./src

# Install dependencies (this will run prepare script which needs tsconfig.json and src/)
RUN npm ci

# Copy remaining files
COPY a2a-inspector/frontend/ ./

# Rebuild native dependencies like esbuild for the container's architecture (Alpine)
# in case host node_modules were copied over.
RUN npm rebuild esbuild

RUN npm run build

# Stage 2: Build the final application with the backend
FROM python:3.12-slim
WORKDIR /app
RUN pip install uv
COPY a2a-inspector/pyproject.toml a2a-inspector/uv.lock ./
RUN uv sync --no-cache --frozen
RUN uv pip install validators
COPY a2a-inspector/backend/ ./backend/
RUN mkdir -p /app/frontend
COPY --from=frontend-builder /app/public /app/frontend/public


WORKDIR /app/backend

# Expose the port the backend server runs on
EXPOSE 8080

# The command to run the server. Because our WORKDIR is now /app/backend,
# we can simply refer to 'app:app' from the current directory.git 
CMD ["uv", "run", "--", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
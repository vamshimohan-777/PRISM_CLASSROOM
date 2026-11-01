# Multi-stage Dockerfile for PRISM CLASSROOM
# Packages both React Frontend and FastAPI Backend into a single unified container

# Stage 1: Build React Frontend
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: Python Backend + Static Asset Serving
FROM python:3.11-slim
WORKDIR /app

# Install Python dependencies
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r ./backend/requirements.txt

# Copy backend code and built frontend distribution
COPY backend/ ./backend/
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Initialize demo database
WORKDIR /app/backend
RUN python -m app.seed

# Expose default port
EXPOSE 8000
ENV PORT=8000

# Start unified FastAPI server (serves both /api and React frontend)
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]

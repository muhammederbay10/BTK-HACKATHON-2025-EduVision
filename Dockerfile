# ================= FRONTEND ====================
FROM node:18-alpine AS frontend

WORKDIR /app/Webapp

COPY Webapp/package*.json ./
RUN npm install

COPY Webapp/ ./
RUN npm run build

# ================= BACKEND ====================
FROM python:3.11-slim AS backend

WORKDIR /app

# Install system dependencies (libGL and more)
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
 && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./
COPY computer-vision_integration/ ./computer-vision_integration/
COPY EduVision_NLP/ ./EduVision_NLP/

# Copy Next.js build and frontend assets
#COPY --from=frontend /app/Webapp/.next ./frontend-next
COPY --from=frontend /app/Webapp/package.json ./frontend-package.json

# ENV vars (customize if needed)
ENV NODE_ENV=production
ENV PORT=8000
ENV PYTHONUNBUFFERED=1

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI with uvicorn (directly)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
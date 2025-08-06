# ================= BACKEND ====================
FROM python:3.11-slim AS backend

WORKDIR /app

# Install system dependencies (libGL and more)
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
 && rm -rf /var/lib/apt/lists/*

# Copy backend requirements
COPY backend/requirements.txt ./backend-requirements.txt
COPY computer-vision_integration/requirements.txt ./cv-requirements.txt
COPY EduVision_NLP/requirements.txt ./nlp-requirements.txt   

# Install Python dependencies
RUN pip install --no-cache-dir -r backend-requirements.txt
RUN pip install --no-cache-dir -r cv-requirements.txt
RUN pip install --no-cache-dir -r nlp-requirements.txt       

# Copy backend code
COPY backend/ ./backend/
COPY computer-vision_integration/ ./computer-vision_integration/
COPY EduVision_NLP/ ./EduVision_NLP/

# ENV vars
ENV NODE_ENV=production
ENV PORT=8000
ENV PYTHONUNBUFFERED=1

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI with uvicorn
CMD ["sh", "-c", "uvicorn backend.app:app --host 0.0.0.0 --port $PORT"]

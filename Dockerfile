FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    OMP_NUM_THREADS=1 \
    OPENBLAS_NUM_THREADS=1 \
    MKL_NUM_THREADS=1 \
    NUMEXPR_NUM_THREADS=1 \
    MALLOC_ARENA_MAX=2

RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . /app

# Render provides $PORT; EXPOSE optional
EXPOSE 10000

# Tiny Gunicorn setup; no Supervisor, no worker
CMD gunicorn "main:app" \
  --bind 0.0.0.0:${PORT:-10000} \
  --workers=1 --threads=2 \
  --worker-tmp-dir /dev/shm \
  --timeout 60 \
  --max-requests 200 --max-requests-jitter 50

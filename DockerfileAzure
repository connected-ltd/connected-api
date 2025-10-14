# Base image
FROM python:3.9

# Ensure Python prints straight to terminal and doesn't create .pyc files
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    DEBIAN_FRONTEND=noninteractive

# System deps (supervisor + OCR/graphics libs)
RUN apt-get update && apt-get install -y --no-install-recommends \
    supervisor \
    tesseract-ocr \
    libtesseract-dev \
    poppler-utils \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Create app dir
WORKDIR /app

# Copy only files needed to install deps first (better layer caching)
COPY .fs /app/.fs

# Install flask-setup and project deps via fs (no pip cache)
RUN pip install --no-cache-dir --upgrade flask-setup && \
    fs install && \
    rm -rf /root/.cache/pip

# Now copy the rest of the project
COPY . /app

# Copy entrypoint and make it executable
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Expose port 80 for CapRover
EXPOSE 80

# Healthcheck (optional but helpful)
# Adjust /health if you have a health route; otherwise comment this out
HEALTHCHECK --interval=30s --timeout=5s --retries=5 \
  CMD wget -qO- http://127.0.0.1:80/health || exit 1

# Start the container
CMD ["/app/entrypoint.sh"]

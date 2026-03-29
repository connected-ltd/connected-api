FROM python:3.9

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    OMP_NUM_THREADS=1 \
    OPENBLAS_NUM_THREADS=1 \
    MKL_NUM_THREADS=1 \
    NUMEXPR_NUM_THREADS=1 \
    MALLOC_ARENA_MAX=2 \
    DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential curl ca-certificates supervisor \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY .fs /app/.fs
RUN pip install --no-cache-dir --upgrade flask-setup \
 && fs install \
 && rm -rf /root/.cache/pip

COPY . /app

# Make entrypoint executable
RUN chmod +x /app/entrypoint.sh

EXPOSE 10000

# Use ENTRYPOINT so entrypoint.sh actually runs
ENTRYPOINT ["/app/entrypoint.sh"]
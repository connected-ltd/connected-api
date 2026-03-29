#!/bin/bash
set -e

echo "🚀 Booting app..."

if [ "${RUN_MIGRATIONS:-false}" = "true" ]; then
  echo "🔄 Running migrations..."
  flask db upgrade || echo "⚠️ Migration failed"
fi

# Start Celery in background (LOW RESOURCE MODE)
echo "👷 Starting Celery worker..."
celery -A app.celery.tasks.celery worker \
  --loglevel=info \
  --concurrency=1 \
  --pool=solo &

# Start Gunicorn (main process)
echo "🌐 Starting Gunicorn..."
exec gunicorn "main:app" \
  --bind 0.0.0.0:${PORT:-10000} \
  --workers=1 \
  --threads=2 \
  --timeout=60 \
  --preload

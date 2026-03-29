#!/bin/bash
set -euo pipefail

echo "🔧 Bootstrapping container..."

# Optional: show key envs exist (mask sensitive values)
# echo "ENV CHECK -> DATABASE_URI: ${DATABASE_URI:-<missing>}, FLASK_DEBUG: ${FLASK_DEBUG:-0}"

# Wait for DB if DATABASE_URI is set and looks like a network target
# Can be refined for DB driver (Postgres/MySQL)
wait_db() {
  if [[ -z "${DATABASE_URI:-}" ]]; then
    echo "ℹ️ DATABASE_URI not set, skipping DB wait."
    return 0
  fi

  # Extract host and port from DATABASE_URI
  # e.g. postgresql://user:pass@hostname:5432/dbname
  local host port retries=10 sleep_sec=2

  host=$(echo "$DATABASE_URI" | sed -E 's|.*@([^:/]+)[:/].*|\1|')
  port=$(echo "$DATABASE_URI" | sed -E 's|.*:([0-9]+)/.*|\1|')
  port=${port:-5432}  # default postgres port

  echo "⏳ Waiting for DB at $host:$port (up to $((retries*sleep_sec))s)..."
  for i in $(seq 1 "$retries"); do
    if curl -sf --connect-timeout 2 "telnet://$host:$port" >/dev/null 2>&1; then
      echo "✅ DB reachable."
      return 0
    fi
    echo "  attempt $i/$retries: not ready..."
    sleep "$sleep_sec"
  done

  echo "⚠️ DB did not respond in time. Continuing anyway."
}
# Run migrations with retry (does not crash the container if it fails)
run_migrations() {
  echo "🔄 Running database migrations (flask db upgrade)..."
  if flask db upgrade; then
    echo "✅ Migrations applied."
  else
    echo "⚠️ Migration step failed — check DB connectivity and Alembic setup."
  fi
}

wait_db
run_migrations

# Run manage.py
echo "🌱 Running manage.py..."
python /app/manage.py

echo "▶️ Starting Supervisor..."
# Use exec so signals are handled correctly
exec supervisord -c /app/supervisord.conf

#!/bin/bash
set -euo pipefail

echo "🔧 Bootstrapping container..."

# Optional: show key envs exist (mask sensitive values)
echo "ENV CHECK -> DATABASE_URI: ${DATABASE_URI:-<missing>}, FLASK_DEBUG: ${FLASK_DEBUG:-0}"

# Wait for DB if DATABASE_URI is set and looks like a network target
# Can be refined for DB driver (Postgres/MySQL)
wait_db() {
  local retries=20
  local sleep_sec=3
  local ok=0

  if [[ -z "${DATABASE_URI:-}" ]]; then
    echo "ℹ️ DATABASE_URI not set, skipping DB wait."
    return 0
  fi

  echo "⏳ Waiting for database to be reachable (up to $((retries*sleep_sec))s)..."
  for i in $(seq 1 "$retries"); do
    # Try a lightweight DB touch via Flask (adjust to your app init if needed)
    if flask db current >/dev/null 2>&1; then
      ok=1
      break
    fi
    echo "  attempt $i/$retries: DB not ready yet..."
    sleep "$sleep_sec"
  done

  if [[ "$ok" -ne 1 ]]; then
    echo "⚠️ DB did not become reachable in time. Continuing anyway."
  else
    echo "✅ DB reachable."
  fi
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

echo "▶️ Starting Supervisor..."
# Use exec so signals are handled correctly
exec supervisord -c /app/supervisord.conf

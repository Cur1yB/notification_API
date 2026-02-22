#!/usr/bin/env bash
set -euo pipefail

COMPOSE_FILE="${COMPOSE_FILE:-docker-compose.test.yml}"
SERVICE="${SERVICE:-postgres_test}"

export DATABASE_URL="${DATABASE_URL:-postgres://postgres:postgres@localhost:5433/notifications_test}"
export JWT_SECRET="${JWT_SECRET:-test-secret}"

docker compose -f "$COMPOSE_FILE" up -d

echo "Please stand by mathafaka..."
until docker compose -f "$COMPOSE_FILE" exec -T "$SERVICE" pg_isready -U postgres -d notifications_test >/dev/null 2>&1; do
  sleep 1
done

uv run pytest --cov -vv

docker compose -f "$COMPOSE_FILE" down -v

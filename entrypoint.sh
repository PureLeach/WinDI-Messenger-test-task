#!/bin/bash

set -e

echo "Applying database migrations..."
if alembic -c project/alembic.ini upgrade head; then
    echo "Migrations applied successfully."
else
    echo "Failed to apply migrations." >&2
    exit 1
fi

echo "Starting FastAPI application..."
exec python -m uvicorn project.main:app --host 0.0.0.0 --port 8000

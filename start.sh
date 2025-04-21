#!/bin/sh

# Wait for PostgreSQL to be ready
until pg_isready -h db -U postgres; do
  echo "Waiting for PostgreSQL to start..."
  sleep 2
done

# Run migrations
alembic upgrade head

# Start FastAPI
exec uvicorn main:app --host 0.0.0.0 --port 8000
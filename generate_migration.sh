#!/bin/bash

# Generate Python migration
alembic revision --autogenerate -m "$1"

# Get the generated revision ID
REVISION=$(ls migrations/versions | grep -E "^[a-f0-9]+_$1.py$" | cut -d'_' -f1)

# Generate SQL version
mkdir -p migrations/versions/sql
alembic upgrade ${REVISION} --sql > migrations/versions/sql/${REVISION}_$1.sql

echo "Generated:"
echo " - migrations/versions/${REVISION}_$1.py"
echo " - migrations/versions/sql/${REVISION}_$1.sql"
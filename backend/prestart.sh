#!/usr/bin/env sh

# Let the DB start
python /app/backend/backend_prestart.py

# Run migrations
alembic upgrade head

# Create initial data in DB
python /app/backend/initial_data.py

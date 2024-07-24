#!/bin/sh

# Wait for the database to be ready
echo "Waiting for database to start..."
while ! nc -z db 5432; do
  sleep 1
done

echo "Database started"

# Run database migrations
echo "Running database migrations..."
poetry run flask db init
poetry run flask db migrate
poetry run flask db upgrade

# Start your Flask application
echo "Starting Flask application..."
exec poetry run flask run --host=0.0.0.0 --reload
#!/bin/sh

# Wait for the database to be ready
echo "Waiting for database to start..."
while ! nc -z db 5432; do
  sleep 1
done

echo "Database started"

# Run database migrations
echo "Running database migrations..."
poetry run flask db init || true  # Ignore if already initialized
poetry run flask db migrate || true  # Ignore if no changes detected
if poetry run flask db upgrade; then
  echo "Database migrations completed successfully"
else
  echo "Database migrations failed"
  exit 1
fi

# Debug: Check the Python environment and installed packages
echo "Checking Python environment..."
poetry run python -c "import sys; print(sys.executable)"
poetry run python -m pip list

# Seed the database using the virtual environment's Python interpreter
echo "Seeding the database..."
/app/.venv/bin/python seed.py

# Start your Flask application
echo "Starting Flask application..."
exec poetry run flask run --host=0.0.0.0 --reload
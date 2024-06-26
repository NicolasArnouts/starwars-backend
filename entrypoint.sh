#!/bin/sh

# Wait for PostgreSQL to start
until pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER; do
  echo "Waiting for PostgreSQL..."
  sleep 2
done

# Run Django migrations
cd /app
python manage.py migrate

# Fetch characters from API
python manage.py fetch_characters  


# Start Django server
exec "$@"

#! /usr/bin/env /bin/sh

set -e

echo "Setting Up DB"

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Starting application..."
exec "$@"
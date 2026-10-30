#! /usr/bin/env /bin/sh

set -e

echo "Setting Up DB"

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Synching permissions"
python manage.py sync_group_policies

echo "Starting application..."
exec "$@"
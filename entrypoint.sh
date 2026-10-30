#! /usr/bin/env /bin/sh

set -e

echo "Setting Up DB"

python - <<'EOF'
import os
from pathlib import Path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

import django
django.setup()
from django.conf import settings

db = settings.DATABASES["default"]

if db["ENGINE"] == "django.db.backends.sqlite3":
    path = Path(db["NAME"])
    if str(path) != ":memory:" and not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch()
        print(f"Created SQLite database file: {path}")
EOF

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Starting application..."
exec "$@"
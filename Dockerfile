# syntax=docker/dockerfile:1-labs

FROM python:3.13-slim as common
LABEL authors="pcmagas"

WORKDIR /app

RUN useradd --create-home --shell /bin/bash --uid 1000 appuser && \
    mkdir -p /db_dir && \
    mkdir -p /static &&\
    chown -R appuser:appuser /app /db_dir &&\
    chmod 600 /db_dir &&\
    chmod 755 /static

VOLUME /db_dir


FROM common as dev
COPY --from=docker.io/astral/uv:latest /uv /uvx /bin/

FROM common as prod

COPY pyproject.toml uv.lock entrypoint.sh /app/
COPY src /app/src

RUN --mount=from=docker.io/astral/uv:latest,source=/uv,target=/bin/uv \
    --mount=type=cache,target=/root/.cache/uv \
    uv export --frozen --no-dev --no-emit-project --format requirements-txt --output-file dependencies.txt && \
    pip install --no-cache-dir -r dependencies.txt

WORKDIR /app/src

# Setting proper DB path
RUN sed -i 's|^DB_DIR = .*|DB_DIR = Path("/db_dir")|' core/settings.py &&\
    echo 'STATIC_ROOT = Path("/static")' >> core/settings.py &&\
    python manage.py collectstatic --noinput

VOLUME /static

EXPOSE 8000
ENTRYPOINT ["/bin/sh","/app/entrypoint.sh"]
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
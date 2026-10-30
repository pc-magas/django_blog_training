# syntax=docker/dockerfile:1-labs

FROM python:3.13-slim as common
LABEL authors="pcmagas"

ENV DB_HOST=postgresql \
    DB_PORT=5432 \
    DB_NAME=blog \
    DB_USER=blog \
    DB_PASSWORD=""

RUN useradd --create-home --shell /bin/bash --uid 1000 appuser &&\
    mkdir /app &&\
    mkdir -p /db_dir &&\
    mkdir -p /static &&\
    chown -R appuser:appuser /app /db_dir /static &&\
    chmod 666 /db_dir &&\
    chmod 755 /static

VOLUME /db_dir
VOLUME /static

FROM common as dev
COPY --from=docker.io/astral/uv:latest /uv /uvx /bin/

ENV VIRTUAL_ENV=/opt/venv \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

RUN mkdir -p /opt/venv &&\
    chown -R appuser:appuser /app /db_dir /opt/venv

USER appuser

FROM dev as build

ENV UV_PROJECT_ENVIRONMENT=/opt/venv

COPY --chown=appuser:appuser pyproject.toml uv.lock entrypoint.sh /app/
COPY --chown=appuser:appuser src /app/src

WORKDIR /app

RUN uv export --frozen --no-dev --no-emit-project --format requirements-txt --output-file dependencies.txt && \
    pip install --no-cache-dir -r dependencies.txt


WORKDIR /app/src

# Setting proper DB path
RUN ls -l core/settings.py &&\
    sed -i 's|^DB_DIR = .*|DB_DIR = Path("/db_dir")|' core/settings.py &&\
    echo 'STATIC_ROOT = Path("/static")' >> core/settings.py


FROM common as prod

COPY --from=build --chown=appuser:appuser /app /app
COPY --from=build --chown=appuser:appuser /static /static
COPY --from=build --chown=appuser:appuser /app/src/core/settings.py /app/src/core/settings.py

USER appuser

WORKDIR /app/src

RUN ls -l /app &&\
    pip install --no-cache-dir -r ../dependencies.txt &&\
    python manage.py collectstatic --noinput

EXPOSE 8000
ENTRYPOINT ["/bin/sh","/app/entrypoint.sh"]
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
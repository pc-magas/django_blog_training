FROM python:3.13-slim as common
LABEL authors="pcmagas"

WORKDIR /app

RUN useradd --create-home --shell /bin/bash --uid 1000 appuser && \
    mkdir -p /db_dir && \
    chown -R appuser:appuser /app /db_dir &&\
    chmod 600 /db_dir


FROM common as dev

USER root
RUN pip install --no-cache-dir uv
USER appuser

FROM common as prod

COPY . /app/

RUN --mount=from=docker.io/astral/uv:latest,source=/uv,target=/bin/uv \
    --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Setting proper DB path
RUN sed -i 's|^DB_DIR = .*|DB_DIR = Path("/db_dir")|' /app/core/settings.py

EXPOSE 8000
CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]
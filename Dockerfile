# syntax=docker/dockerfile:1-labs

FROM python:3.13-slim as common
LABEL authors="pcmagas"

WORKDIR /app

RUN useradd --create-home --shell /bin/bash --uid 1000 appuser && \
    mkdir -p /db_dir && \
    mkdir -p /static &&\
    chown -R appuser:appuser /app /db_dir &&\
    chmod 600 /db_dir &&\
    chmod 644 /static


FROM common as dev

USER root
RUN pip install --no-cache-dir uv
USER appuser


FROM common as prod

COPY --exclude=./static . /app/
COPY ./static/ /static/*

RUN --mount=from=docker.io/astral/uv:latest,source=/uv,target=/bin/uv \
    --mount=type=cache,target=/root/.cache/uv \
    uv export --frozen --no-dev --no-emit-project --format requirements-txt --output-file dependencies.txt && \
    pip install --no-cache-dir -r dependencies.txt

# Setting proper DB path
RUN sed -i 's|^DB_DIR = .*|DB_DIR = Path("/db_dir")|' /app/core/settings.py

VOLUME /static
VOLUME /db_dir

EXPOSE 8000
ENTRYPOINT ["/bin/sh","/app/entrypoint.sh"]
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
FROM python:3.13-slim as common
LABEL authors="pcmagas"

WORKDIR /app
RUN useradd --create-home --shell /bin/bash --uid 1000 appuser && \
    chown appuser:appuser /app

# Make this the default user for everything below and for `docker run`
USER appuser

FROM common

USER root
RUN pip install --no-cache-dir uv
USER appuser
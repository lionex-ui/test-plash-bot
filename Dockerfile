# Builder
FROM python:3.12-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=2.1.1
RUN pip install --no-cache-dir poetry==${POETRY_VERSION}

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Final
FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -r appuser \
    && mkdir -p /app \
    && chown appuser:appuser /app

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

COPY --chown=appuser:appuser ./main.py ./
COPY --chown=appuser:appuser ./src ./src
COPY --chown=appuser:appuser ./alembic.ini ./
COPY --chown=appuser:appuser ./migrations ./migrations
COPY --chown=appuser:appuser ./pyproject.toml ./
COPY --chown=appuser:appuser ./poetry.lock ./

COPY ./wait-for-it.sh ./
RUN chmod +x ./wait-for-it.sh

USER appuser
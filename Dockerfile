FROM python:3.14.0
LABEL authors="Anna"

ENV PYTHONUNBUFFERED 1
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY medical_app/ /app/
WORKDIR /app
RUN uv sync --frozen
CMD set -xe; \
    uv run python manage.py collectstatic --noinput; \
    uv run python manage.py migrate --noinput; \
    uv run python manage.py runserver 0.0.0.0:8000

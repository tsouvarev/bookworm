# syntax = docker/dockerfile:1.2

FROM python:3.12-slim as base
COPY --from=ghcr.io/astral-sh/uv /uv /bin/
WORKDIR /opt
COPY pyproject.toml uv.lock .

FROM base as dev
RUN uv sync --dev --frozen --no-cache
CMD ["uv", "run", "flask", "run", "--host=0.0.0.0", "--port=3000", "--debug"]

FROM base as release
RUN uv sync --frozen --no-cache
COPY . .
CMD ["uv", "run", "gunicorn", "bookworm:create_app()"]

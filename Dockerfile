FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim AS base
WORKDIR /opt
ADD pyproject.toml uv.lock /opt/

FROM base AS dev
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --dev --no-editable
CMD ["uv", "run", "--frozen", "flask", "run", "--host=0.0.0.0", "--port=3000", "--debug"]

FROM base AS release
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-editable
COPY . .
CMD ["uv", "run", "--frozen", "gunicorn", "--bind", "0.0.0.0:5000", "bookworm:create_app()"]

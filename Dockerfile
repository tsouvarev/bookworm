# syntax = docker/dockerfile:1.2

FROM python:3.12-slim as base
WORKDIR /opt
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/ pip install -r requirements.txt

FROM base as dev
COPY requirements.dev.txt .
RUN --mount=type=cache,target=/root/.cache/ pip install -r requirements.dev.txt
CMD ["flask", "--app bookworm:create_app", "run", "-h 0.0.0.0", "-p 3000"]

FROM base as release
COPY . .
CMD ["gunicorn", "bookworm:app"]

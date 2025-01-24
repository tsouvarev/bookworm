# syntax = docker/dockerfile:1.2

FROM python:3.12-slim as base
WORKDIR /opt
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/ pip install -r requirements.txt

FROM base as dev
COPY requirements.dev.txt .
RUN --mount=type=cache,target=/root/.cache/ pip install -r requirements.dev.txt
CMD ["flask", "run", "--host=0.0.0.0", "--port=3000", "--debug"]

FROM base as release
COPY . .
CMD ["gunicorn", "bookworm:create_app()"]

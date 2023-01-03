# syntax = docker/dockerfile:1.2

FROM python:3.8-slim as base
WORKDIR /opt
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/ pip install -r requirements.txt

FROM base as dev
COPY requirements.dev.txt .
RUN --mount=type=cache,target=/root/.cache/ pip install -r requirements.dev.txt
ENV FLASK_APP=bookworm.py
CMD flask run -h 0.0.0.0 -p 3000

FROM base as release
ARG SECRET_KEY
ARG MONGO_URI
ARG USER
ARG PASSWORD
COPY . .
RUN gunicorn bookworm:app

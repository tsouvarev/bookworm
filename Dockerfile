FROM python:3.8-slim as base
WORKDIR /opt
COPY requirements.txt .
RUN pip install -r requirements.txt

FROM base as dev
COPY requirements.dev.txt .
RUN pip install -r requirements.dev.txt
CMD flask run -h 0.0.0.0 -p 3000

FROM base as release
COPY . .
RUN gunicorn app:app

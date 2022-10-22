FROM python:3.8-slim-buster

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV CELERY_BROKER_URL redis://redis:6379
ENV HOSTNAME postgres

COPY ./ /app

COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt --no-cache-dir --default-timeout=1000


COPY ./docker/local/flask_start /flask_start

RUN chmod +x /flask_start

WORKDIR /app

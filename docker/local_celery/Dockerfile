FROM python:3.8-slim-buster

RUN apt-get -y update
RUN apt-get install -y ffmpeg


WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV CELERY_BROKER_URL redis://redis:6379/0
ENV HOSTNAME 34.171.227.62
ENV MEDIAFILE /consumer
COPY . /app

#COPY ./requirements.txt /requirements.txt

RUN pip install -r /app/requirements.txt --no-cache-dir --default-timeout=1000


COPY ./docker/local/flask_start /flask_start

#RUN chmod +x /flask_start

WORKDIR /app

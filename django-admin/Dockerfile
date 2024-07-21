FROM python:3.11-slim

RUN apt-get update \
    && pip install psycopg2-binary

WORKDIR /django-admin

COPY requirements.txt .

RUN pip install -r requirements.txt

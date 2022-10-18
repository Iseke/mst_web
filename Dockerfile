FROM python:3.9.13-slim-bullseye

ENV PYTHONUNBUFFERED=1

RUN apt-get update

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt --no-cache-dir && \
    rm -rf ~/.cache/pip && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get purge   --auto-remove && \
    apt-get clean

COPY . /app/
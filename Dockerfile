FROM python:3.9-slim

WORKDIR /app

ARG CONFIG_PATH

ENV PYTHONPATH "${PYTHONPATH}:/app"
ENV CONFIG_PATH ${CONFIG_PATH}

COPY requirements/requirements.txt .
COPY api api
COPY bl bl
COPY dl dl
COPY config.py .
COPY config/config.yaml .
COPY main.py .
EXPOSE 8080

RUN pip install -r requirements.txt
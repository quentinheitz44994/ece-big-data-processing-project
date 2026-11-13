# Lightweight Python image for the Kafka side of the project: topic creation
# (kafka-init) and the Wikimedia EventStreams producer. The source code and the
# configuration are bind-mounted by compose.yaml (/app/src, /app/conf).
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src \
    IMDB_PROJECT_CONFIG=/app/conf/settings.yaml

WORKDIR /app

COPY requirements-producer.txt /tmp/requirements-producer.txt
RUN pip install --no-cache-dir -r /tmp/requirements-producer.txt

CMD ["python", "-m", "imdb_project.streaming.producer"]

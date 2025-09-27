FROM python:3.12.3-slim

ENV PYTHONUNBUFFERED 1
WORKDIR /app

RUN apt-get update \
    && apt-get install -y build-essential libpq-dev \
    && apt-get clean

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY alembic.ini /app/
COPY db /app/db
COPY libs /app/libs
COPY src /app/src
COPY scripts /app/scripts

RUN chmod +x /app/scripts/entrypoint.sh

EXPOSE 8000
ENTRYPOINT ["/app/scripts/entrypoint.sh"]

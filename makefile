.PHONY: help build up down logs restart revision upgrade clean disable-postgres disable-mysql disable-mongo

include .env
export $(shell sed 's/=.*//' .env)

DOCKER_COMPOSE_FILE=docker/docker-compose.yml

help:
	@echo "Available commands:"
	@echo "  make build             - Build the Docker image"
	@echo "  make up                - Start FastAPI"
	@echo "  make down              - Stop and remove containers"
	@echo "  make logs              - View logs"
	@echo "  make restart           - Restart FastAPI"
	@echo "  make revision          - Create Alembic migration revision"
	@echo "  make upgrade           - Apply Alembic migrations"
	@echo "  make clean             - Remove volumes and stop everything"
	@echo "  make disable-postgres  - Stop and remove PostgreSQL container"
	@echo "  make disable-mysql     - Stop and remove MySQL container"
	@echo "  make disable-mongo     - Stop and remove Mongo container"

build:
	@echo "🔨 Building FastAPI Docker image..."
	docker compose -f $(DOCKER_COMPOSE_FILE) build --no-cache

up:
	@echo "🚀 Starting FastAPI with ${DB_TYPE}..."
	DB_TYPE=${DB_TYPE} docker compose -f $(DOCKER_COMPOSE_FILE) up -d --build

down:
	@echo "🛑 Stopping and removing all containers..."
	docker compose -f $(DOCKER_COMPOSE_FILE) down

logs:
	@echo "📜 Viewing logs..."
	docker compose -f $(DOCKER_COMPOSE_FILE) logs -f

restart: down up
	@echo "🔄 Restarted FastAPI service!"

revision:
	@read -p "Enter revision message: " msg; \
	docker compose -f $(DOCKER_COMPOSE_FILE) exec fastapi alembic revision --autogenerate -m "$$msg"

upgrade:
	@echo "📦 Upgrading database to latest revision..."
	docker compose -f $(DOCKER_COMPOSE_FILE) exec fastapi alembic upgrade head

clean: down
	@echo "🧹 Cleaning up volumes..."
	docker volume rm postgres_data mysql_data || true

disable-postgres:
	@echo "🛑 Disabling PostgreSQL..."
	docker compose -f $(DOCKER_COMPOSE_FILE) stop postgres
	docker compose -f $(DOCKER_COMPOSE_FILE) rm -f postgres

disable-mysql:
	@echo "🛑 Disabling MySQL..."
	docker compose -f $(DOCKER_COMPOSE_FILE) stop mysql
	docker compose -f $(DOCKER_COMPOSE_FILE) rm -f mysql

disable-mongo:
	@echo "🛑 Disabling Mongo..."
	docker compose -f $(DOCKER_COMPOSE_FILE) stop mongo
	docker compose -f $(DOCKER_COMPOSE_FILE) rm -f mongo

test:
	@echo "🧪 Running unit tests with pytest..."
	docker compose -f $(DOCKER_COMPOSE_FILE) exec fastapi pytest -v /app/src/tests

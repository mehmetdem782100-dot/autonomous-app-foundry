.PHONY: init up down restart logs migrate test

init:
	cp .env.example .env
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

restart:
	down up

logs:
	docker-compose logs -f api

makemigrations:
	alembic revision --autogenerate -m "$(m)"

migrate:
	alembic upgrade head

test:
	pytest tests/ -v\n
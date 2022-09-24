
build:
	docker container prune -f
	docker build . -f ./docker/Dockerfile -t citywideiowa0/finapp
	docker build -f ./frontend/Dockerfile ./frontend -t cityewideiowa0/finapp-frontend 

update:
	docker compose --env-file ./.env -f ./docker/docker-compose.yml run finapp

explore:
	docker compose --env-file ./.env -f ./docker/docker-compose.yml run finapp python3 ./src/exploration.py

start-db:
	docker compose -f ./docker/docker-compose.yml run -d --name mongo_db db

stop-db:
	docker container stop mongo_db

attach:
	docker compose --env-file ./.env -f ./docker/docker-compose.yml run -i finapp bash


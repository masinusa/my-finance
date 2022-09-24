
build:
	docker container prune -f
	docker build . -f ./docker/Dockerfile -t citywideiowa0/finapp

update:
	docker compose --env-file ./.env -f ./docker/docker-compose.yml run finapp

analyze:
	docker compose --env-file ./.env -f ./docker/docker-compose.yml run finapp python3 ./src/analyze.py


write:
	docker compose --env-file ./.env -f ./docker/docker-compose.yml run finapp python3 ./src/write.py

explore:
	docker compose --env-file ./.env -f ./docker/docker-compose.yml run finapp python3 ./src/explore.py

start-db:
	docker compose -f ./docker/docker-compose.yml run -d --name mongo_db db

stop-db:
	docker container stop mongo_db

attach:
	docker compose --env-file ./.env -f ./docker/docker-compose.yml run -i finapp bash


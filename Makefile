
SHELL := /bin/bash

up:
	@docker compose --profile prod up -d
	@echo "######## http://localhost ########"

down:
	@docker compose --profile prod --profile dev down

demo:
	@docker compose --profile dev up -d
	@echo "######## http://localhost ########"

run-int-tests:
	docker compose run --rm test py.test tests/integration/

run-unit-tests:
	docker compose run --rm test py.test tests/unit/

restart_container: 
	@read -p "Enter Service Name:" service &&\
	docker container kill &&service &&\
	docker compose start &&service

restart_system:
	make down
	make up

enter:
	@read -p "Enter Service Name:" service &&\
	docker compose run --rm $$service bash

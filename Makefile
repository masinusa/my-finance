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

restart:
	make down
	make up

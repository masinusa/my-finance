
prune:
	docker container prune -f

build_plaid: prune
	docker build -f dockerfiles/plaid_Dockerfile . -t citywideiowa0/finapp_plaid

build_gui: prune
	docker build -f dockerfiles/gui_Dockerfile . -t citywideiowa0/finapp_gui
	
up:
	@docker compose up -d
	@echo "######## http://localhost:8501 ########"

restart:
	make down
	make up

restart-plaid:
	docker compose

analyze:
	docker compose --env-file ./.env -f ./docker/docker-compose.yml run gui python3 ./src/analyze.py

write:
	docker compose --env-file ./.env -f ./docker/docker-compose.yml run gui python3 ./src/write.py

explore:
	docker compose --env-file ./.env -f ./docker/docker-compose.yml run gui python3 ./src/explore.py

start-db:
	docker compose -f ./docker/docker-compose.yml run --rm -d --name mongo_db db

stop-db:
	docker container stop mongo_db

down:
	docker compose down

flask:
	docker run -v '/mnt/c/Users/Michael Spicer/OneDrive/Documents/--- financial_cookbook ---':'/finapp' -p 5000:5000 test_flask
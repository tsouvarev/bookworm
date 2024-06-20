format:
	ruff format .
	ruff check . --fix-only
	black .

check:
	ruff .
	black --check .

install:
	pip install -r requirements.dev.txt

upgrade:
	pip-compile requirements.in -o requirements.txt -q --upgrade

compile:
	pip-compile requirements.in -o requirements.txt -q

run:
	docker compose up --build app

dev:
	flask --app bookworm:create_app run

test:
	docker compose run app pytest

generate:
	python -m app.generate

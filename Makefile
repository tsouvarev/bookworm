RUN = uv run

format:
	$(RUN) ruff format .
	$(RUN) ruff check . --fix-only --unsafe-fixes

check:
	$(RUN) ruff check .

install:
	uv sync

upgrade:
	uv lock --upgrade

run:
	docker-compose up --build app

dev:
	$(RUN) flask --app bookworm:create_app run --reload

test:
	docker-compose run --rm app pytest

generate:
	$(RUN) python -m app.generate

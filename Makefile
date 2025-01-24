RUN = uv run --with-requirements requirements.dev.txt

format:
	$(RUN) ruff format .
	$(RUN) ruff check . --fix-only
	$(RUN) black .

check:
	$(RUN) ruff check .
	$(RUN) black --check .

install:
	uv pip install -r requirements.dev.txt

upgrade:
	uv pip compile requirements.in -o requirements.txt -q --upgrade

compile:
	uv pip compile requirements.in -o requirements.txt -q

run:
	docker-compose up --build app

dev:
	$(RUN) flask --app bookworm:create_app run --reload

test:
	docker-compose run --rm app pytest

generate:
	$(RUN) python -m app.generate

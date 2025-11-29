set dotenv-load
RUN := 'uv run'

format:
	{{ RUN }} ruff format .
	{{ RUN }} ruff check . --fix-only --unsafe-fixes

check:
	{{ RUN }} ruff check .

install:
	uv sync

upgrade:
	uv lock --upgrade --exclude-newer `date --date '7 days ago' --iso-8601`

run:
	docker compose up --build app

dev:
	{{ RUN }} flask --app bookworm:create_app run --reload

test:
	docker compose run --build --rm app {{ RUN }} pytest

generate:
	{{ RUN }} python -m app.generate

deploy:
	docker build . --target release --tag cr.yandex/$YANDEX_REGISTRY_ID/bookworm
	docker push cr.yandex/$YANDEX_REGISTRY_ID/bookworm

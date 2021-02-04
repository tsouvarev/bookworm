format:
	black .
	isort .

check:
	isort --check-only --diff .
	black --check .
	flake8 --config flake8.ini

install:
	pip install -r requirements.dev.txt

upgrade:
	pip-compile requirements.in -o requirements.txt -q --upgrade

compile:
	pip-compile requirements.in -o requirements.txt -q

run:
	DOCKER_BUILDKIT=1 COMPOSE_DOCKER_CLI_BUILD=1 docker-compose up --build app

generate:
	python -m app.generate

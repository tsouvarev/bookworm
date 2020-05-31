format:
	black .
	isort --recursive .

install:
	pip install -r requirements.dev.txt

compile:
	pip-compile requirements.in -o requirements.txt -q

run:
	docker-compose run --build
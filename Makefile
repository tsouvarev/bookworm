format:
	black .
	isort --recursive .

install:
	pip install -r requirements.dev.txt

upgrade:
	pip-compile requirements.in -o requirements.txt -q --upgrade

compile:
	pip-compile requirements.in -o requirements.txt -q

run:
	docker-compose up --build

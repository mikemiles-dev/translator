VERSION=0.0.1
HOST?=0.0.0.0
REDIS_HOST?=redis://127.0.0.1:7001

export PYTHONPATH=$(PWD)
export REDIS_HOST
export TRANSLATE_API_VER=$(VERSION)
export FLASK_APP=src/translator.py

redis-dev:
	docker run --rm --name translate-redis -p 7001:6379 -d redis

redis-test-start:
	docker run --rm --name translate-redis-test -p 7002:6379 -d redis

redis-test-stop:
	docker stop translate-redis-test

build-dev:
	pip install -r requirements_dev.txt
	flake8

build:
	pip install -r requirements.txt

run-dev:
	export FLASK_ENV=development
	@echo Running Version ${VERSION}
	flask run --host=$(HOST)

run-prod:
	@echo Todo UWGI or something here

test:
	$(MAKE) redis-test-stop || true
	@echo Starting Redis test service
	export REDIS_HOST=redis://127.0.0.1:7002
	$(MAKE) redis-test-start
	pytest -v || true
	$(MAKE) redis-test-stop

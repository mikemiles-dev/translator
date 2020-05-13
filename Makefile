VERSION=0.0.1
HOST?=0.0.0.0

export FLASK_APP=src/translator.py

build:
	pip install -r requirements.txt

run: build
	@echo Running Version ${VERSION}
	flask run --host=$(HOST)

test:
	@echo Todo Add Unit Tests

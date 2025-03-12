SHELL=/bin/bash
VENV:=./.venv
BIN := $(VENV)/bin
PIP := $(BIN)/pip
PYTHON:=$(BIN)/python3
PYTEST:=$(BIN)/pytest
BLACK := $(BIN)/black
FLAKE8 := $(BIN)/flake8
DC:=docker-compose

.venv:
	python3 -m venv $@

install: requirements.txt .venv
	./.venv/bin/pip install -r $<

install-dev: requirements-dev.txt install
	./.venv/bin/pip install -r $<

build:
	$(DC) build app

compose-up:
	$(DC) up -d

compose-down:
	$(DC) down -v

redis-up:
	$(DC) up -d redis

redis-down:
	$(DC) down -v redis

compose-logs:
	$(DC) logs -f

format:
	$(BLACK) app

lint:
	$(FLAKE8) app

ws:
	$(PYTHON) utils/ws_test.py
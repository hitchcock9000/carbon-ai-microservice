PYTHON ?= python
PIP ?= pip
UVICORN_APP ?= src.api.main:app
HOST ?= 0.0.0.0
PORT ?= 8000

.PHONY: install run test lint format check

install:
	$(PIP) install -r requirements.txt

run:
	uvicorn $(UVICORN_APP) --reload --host $(HOST) --port $(PORT)

test:
	pytest -v

lint:
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics --exclude=venv,data,.venv
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics --exclude=venv,data,.venv

format:
	black .

check: lint test

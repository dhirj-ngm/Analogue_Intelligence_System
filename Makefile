PYTHON := .venv/bin/python
APP_PYTHON ?= python3
export PYTHONPATH := src
export HF_HOME := models/hf
.PHONY: setup test lint run validate app browser-test collection-check search-check search-check-m005
setup:
	python3 -m venv .venv
	$(PYTHON) -m pip install -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu
test:
	$(APP_PYTHON) -m unittest discover -s tests -v
	node --test tests/test_reader.mjs
lint:
	.venv/bin/ruff check src tests scripts
	.venv/bin/ruff format --check src tests scripts
validate:
	$(APP_PYTHON) -m ais.pilot validate
run:
	$(PYTHON) -m ais.pilot run
app:
	$(APP_PYTHON) -m ais.app
browser-test:
	node scripts/check_app_browser.mjs
collection-check:
	$(APP_PYTHON) -m ais.collection
	$(APP_PYTHON) scripts/check_collection.py
search-check:
	$(APP_PYTHON) scripts/evaluate_search.py
search-check-m005:
	$(APP_PYTHON) scripts/evaluate_search.py --module m005

PYTHON := .venv/bin/python
APP_PYTHON ?= python3
export PYTHONPATH := src
export HF_HOME := models/hf
.PHONY: setup test lint run validate app browser-test collection-check search-check search-check-m005 collection-check-m007 review-check review-browser audit-check
setup:
	python3 -m venv .venv
	$(PYTHON) -m pip install -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu
test:
	$(APP_PYTHON) -m unittest discover -s tests -v
	node --test tests/test_reader.mjs tests/test_review.mjs
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
collection-check-m007:
	$(APP_PYTHON) scripts/check_collection_m007.py
search-check:
	$(APP_PYTHON) scripts/evaluate_search.py
	$(APP_PYTHON) scripts/check_collection_m007.py
search-check-m005:
	$(APP_PYTHON) scripts/evaluate_search.py --module m005
review-check: audit-check
audit-check:
	$(APP_PYTHON) scripts/check_audit_m008.py
review-browser:
	node scripts/check_review_browser.mjs

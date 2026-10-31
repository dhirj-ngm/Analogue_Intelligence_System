PYTHON := .venv/bin/python
export PYTHONPATH := src
export HF_HOME := models/hf
.PHONY: setup test lint run validate
setup:
	python3 -m venv .venv
	$(PYTHON) -m pip install -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu
test:
	$(PYTHON) -m unittest discover -s tests -v
lint:
	.venv/bin/ruff check src tests scripts
	.venv/bin/ruff format --check src tests scripts
validate:
	$(PYTHON) -m ais.pilot validate
run:
	$(PYTHON) -m ais.pilot run

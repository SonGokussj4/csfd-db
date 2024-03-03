PYTHON=python3.11
VENV=.venv
PIP=$(VENV)/bin/pip
UVICORN=$(VENV)/bin/uvicorn


.PHONY: all help venv venv-dev clean run

help:
	@echo "make venv"
	@echo "    Create a virtual environment" and install the dependencies
	@echo "make help"
	@echo "    Show this help message"
	@echo "make clean"
	@echo "    Remove all the compiled files"

venv:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

venv-dev: venv
	$(PIP) install -r requirements_dev.txt

clean:
	find . -name '*.pyc' -delete
	find . -name '*.pyo' -delete
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '.mypy_cache' -exec rm -rf {} +

run:
	$(UVICORN) app.main:app --reload

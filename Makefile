# Makefile
VENV := .venv
PYTHON := python3.12
PY := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
PIP_COMPILE := $(VENV)/bin/pip-compile

.PHONY: init venv install-dev compile activate clean

init: venv install-dev compile activate install pre-commit
	@echo "init done."

venv:
	@test -d $(VENV) || $(PYTHON) -m venv $(VENV)

install-dev: venv
	$(PY) -m pip install --upgrade pip setuptools wheel
	$(PIP) install --upgrade pip-tools

compile: install-dev
	@if [ -f requirements.in ]; then \
		$(PIP_COMPILE) requirements.in --output-file=requirements.txt; \
	else \
		echo "No requirements.in found — skipping pip-compile."; \
	fi

activate:
	@. $(VENV)/bin/activate
	echo "Virtual environment activated."

pre-commit: install-dev
	$(PIP) install --upgrade pre-commit
	$(PY) -m pre_commit install
	@echo "pre-commit hooks installed."

install: install-dev
	@if [ -f requirements.txt ]; then \
		$(PIP) install -r requirements.txt; \
	else \
		echo "No requirements.txt found — skipping installation."; \
	fi

clean:
	@rm -rf $(VENV)
	@rm -f requirements.txt
	@rm -f requirements.lock
	@echo "Cleaned up virtual environment and generated files."

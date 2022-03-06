.DEFAULT_GOAL := run

# Variables
PY_RUN = data/flatten.py

PIPENV := pipenv
PYTHON := python3


# Setup the virtual env
setup:
	@$(PIPENV) install
.PHONY:setup

setup-dev:
	@$(PIPENV) install --dev
.PHONY:setup

# Run tests
test: setup-dev
	@$(PIPENV) run pytest
.PHONY:test

# Run the app
run: setup
	@$(PIPENV) run $(PYTHON) $(PY_RUN)
.PHONY:run

# Clean the app and remove the venv
clean:
	@rm -rf __pycache__
	@$(PIPENV) --rm
.PHONY:clean


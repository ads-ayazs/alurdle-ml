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

# Clean up
clean-app:
	@echo "Cleaning app..."
	@rm -rf __pycache__
.PHONY:clean-app

clean-env: guard-PIPENV_ACTIVE
	@echo "Cleaning pipenv..."
	@rm -rf __pycache__
	-@$(PIPENV) --rm
.PHONY:clean-env

clean-test:
	@echo "Cleaning pytest..."
	@rm -rf .pytest_cache
.PHONY:clean-test

clean: clean-test clean-app clean-env
.PHONY:clean

# Protect against running from inside pipenv shell
guard-PIPENV_ACTIVE:
	@ if [ "${PIPENV_ACTIVE}" != "" ]; then \
		echo "Exit pipenv shell before running make clean" && exit 1; \
	fi
.DEFAULT_GOAL := run

# Variables
PY_RUN = data/flatten.py

PIPENV := pipenv
PYTHON := python3


# Create and activate the venv
setup:
	@$(PIPENV) install
.PHONY:setup

# Run the app
run: setup
	@$(PIPENV) run $(PYTHON) $(PY_RUN)
.PHONY:run

# Clean the app and remove the venv
clean:
	@rm -rf __pycache__
	@$(PIPENV) --rm
.PHONY:clean


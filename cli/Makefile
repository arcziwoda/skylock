phony: install test test-coverage mkdocs pylint help

install:
	poetry install
	poetry run setup_config
	poetry run setup_downloads

test:
	poetry run pytest tests/

test-coverage:
	coverage run -m pytest
	coverage report --sort=cover

mkdocs:
	mkdocs serve --dev-addr localhost:8090

pylint:
	poetry run pylint skylock_cli tests

help:
	@echo "install: Install the project dependencies"
	@echo "test: Run the tests"
	@echo "test-coverage: Run the tests and show the coverage"
	@echo "mkdocs: Run the documentation server"
	@echo "pylint: Run the pylint"
	@echo "help: Show this help message"
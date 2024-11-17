phony: install test test-coverage mkdocs help

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


help:
	@echo "install: Install the project dependencies"
	@echo "test: Run the tests"
	@echo "test-coverage: Run the tests and show the coverage"
	@echo "mkdocs: Run the documentation server"
	@echo "help: Show this help message"
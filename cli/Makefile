install:
	poetry install
	poetry run setup_config

mkdocs:
	mkdocs serve --dev-addr 0.0.0.0:8090

coverage:
	coverage run -m pytest
	coverage report --sort=cover

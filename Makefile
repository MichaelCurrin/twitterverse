# Show summarized form of Makefile.
# Match targets or comments, empty lines and echo lines.
# egrep is needed to avoid error and $$ is needed to escape $ in make file.
help:
	@egrep '(^\S)|(^$$)|^\S+@echo' Makefile

# Install core dependencies
install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

# Install dev dependencies.
dev-install:
	pip install -r requirements-dev.txt


# Run flake8 linting.
lint:
	# Stop the build if there are Python syntax errors or undefined names.
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	# Exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide.
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

# Run PY2/3 lint check.
lint3:
	pylint --py3k app/*


# Run tests suitable for any environnment.
test: unit ig
unit:
	# Run unit tests
	python -m unittest discover -s app/tests/unit -t app -v
ig:
	# Run integration tests. Use test DB.
	python -m unittest discover -s app/tests/integration -t app -v

# Run tests only appropriate for local environment.
test-local:
	# Run manual unit tests. Using test DB.
	python -m unittest discover -s app/tests/manual/ -t app
	# Run manual search tests. Using main DB.
	cd app && tests/manual/search_api.sh

# Open SQL console for configured DB.
sql:
	tools/open_main_db.sh

# WARNING! Drops all data.
fresh-db:
	# Drop entire main DB and create base DB without populating it.
	# TODO: Add confirmation step and show configured path to DB.
	cd app && utils/db_manager.py --drop --create --summary

# Tail log file for application.
log:
	cd app && tail -f var/log/app.log

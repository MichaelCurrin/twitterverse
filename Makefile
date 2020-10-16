default: install install-dev

# Show summary of make commands.
h help:
	@echo "Include left-aligned, empty lines and echo lines."
	@egrep '(^\S)|(^$$)|\s+@echo' Makefile


install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt


lint:
	# Stop the build if there are Python syntax errors or undefined names.
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	# Exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide.
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics


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


# Tail log file for application.
log:
	cd app && tail -f var/log/app.log


.PHONY: docs
docs:
	docsify serve docs

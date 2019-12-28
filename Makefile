help:
	@egrep '^\w+' Makefile

install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt
dev-install:
	pip install -r requirements-dev.txt

lint:
	# Stop the build if there are Python syntax errors or undefined names.
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	# Exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide.
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
lint3:
	pylint --py3k app/*

unit:
	python -m unittest discover -s app/tests/unit -t app -v
integration:
	python -m unittest discover -s app/tests/integration -t app -v
test: unit integration

test-local:
	python -m unittest discover -s app/tests/manual/ -t app
	cd app && tests/manual/search_api.sh


# Open SQL console for configured DB.
sql:
	tools/open_main_db.sh

fresh-db:
	# WARNING! Use with caution.
	# Drop entire main DB and create base DB without populating it.
	# TODO: Add confirmation step and show configured path to DB.
	cd app && utils/db_manager.py --drop --create --summary

log:
	cd app && tail -f var/log/app.log

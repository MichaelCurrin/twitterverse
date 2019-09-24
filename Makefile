help:
	@egrep '^\w*:' Makefile

unit:
	python -m unittest discover -s app/tests/unit -t app

integration:
	python -m unittest discover -s app/tests/integration -t app

test: unit integration

lint:
	# Stop the build if there are Python syntax errors or undefined names
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics --exclude app/lib/wip/
	# Exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics --exclude app/lib/wip/

lint3:
	cd app && pylint --py3k *

install:
	# From workflow file.
	python -m pip install --upgrade pip
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

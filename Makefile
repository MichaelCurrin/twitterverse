help:
	@egrep '^\w+' Makefile

install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

dev-install:
	pip install -r requirements-dev.txt

lint:
	# Stop the build if there are Python syntax errors or undefined names
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics --exclude app/lib/wip/
	# Exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 \
		--statistics --exclude app/lib/wip/,app/tests/manual --ignore=E266,E402

lint3:
	cd app && pylint --py3k *

unit:
	python -m unittest discover -s app/tests/unit -t app

integration:
	python -m unittest discover -s app/tests/integration -t app

test: unit integration

test-local:
	python -m unittest discover -s app/tests/manual/ -t app

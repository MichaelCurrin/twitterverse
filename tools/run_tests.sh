#!/usr/bin/env bash
# Run test suite.
#
# Usage:
#   $ cd <PROJECT_PATH>
#   $ ./tools/run_tests.sh
#

. venv/bin/activate

cd app
python -m unittest discover tests

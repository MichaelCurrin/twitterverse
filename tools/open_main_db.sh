#!/usr/bin/env bash
# Open SQLite console for the configured DB file.

set -e

cd app
DB=$(utils/db_manager.py --path)
sqlite3 "$DB"

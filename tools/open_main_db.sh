#!/bin/bash -e
# Open SQLite console for the configured DB file.

cd app
DB=$(utils/db_manager.py --path)
sqlite3 "$DB"

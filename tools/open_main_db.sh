#!/bin/bash -e
# Open SQLite console in configured DB.

cd app
DB=$(utils/db_manager.py --path)
sqlite3 "$DB"

# SQLObject Tips

Tips for working with the database models, using lib.database module and SQLObject functionality.

## Reasoning behind column attributes

Some general notes on using and understanding SQLObject.

### Not null

SQLObject's column validation by default requires a value for a column
when creating it. Even if the value is set as `db.MyTable(myColumn=None)`
and even though there is no `NOT NULL` contraint when checking the table's schema. Therefore it is a good idea add `notNull=True` in the model, to add this as a contraint for when doing SQL queries directly. In the SQLObject code, `notNull` and `notNone` are aliases.

### Default

Setting `default=None` for the column allows the value to be omitted when inserting
a row using SQLObject. However, it does not add a default in the
schema, in SQLite at least.


## View column definitions

A table's column definitions are available on the table's sqlmeta class.

```python
from lib import database as db

# Returns a dictionary.
colDefs = db.Tweet.sqlmeta.columnDefinitions

for k, v in colDefs.items():
    print k, v
# => retweetCount <IntCol 7f56142b11d0 retweetCount>
# => etc.
```


## View the create table SQL

Print out the SQL statement used to create the table. Note that `.createTable` will _create_ the table in the db, while the method below will only _return_ SQL statements without executing.

```python
>>> # Get create table statement and a list of constraints statements.
>>> sql, contraints = db.Tweet.createTableSQL()
>>> print sql
CREATE TABLE tweet (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    guid INT NOT NULL UNIQUE,
    ...
);
>>> print constraints
[]
>>> # Optionally, exclude the join tables and index from the sql, since they are on by default.
>>> db.Tweet.createTableSQL(createJoinTables=False, createIndexes=False)
...
```

See SQLObject's `main.py` or `dbconnection.py` files for more detail.


Alternatively, view all create statements in sqlite itself, assuming the `lib/database.py` script has already been run with the `--create` flag.

```bash
$ sqlite3 var/db.sqlite
sqlite> .schema
```

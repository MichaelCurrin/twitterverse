
# Models

See the [models](../app/models/) directory.


## Table structure

TBC


## SQLObject notes

### Not null

SQLObject's column validation by default requires a value for a column
when creating it. Even if the value is set as `db.MyTable(myColumn=None)`
and even though there is no `NOT NULL` contraint when checking the table's schema. Therefore it is a good idea add `notNull=True` in the model, to add this as a contraint for when doing SQL queries directly. In the SQLObject code, `notNull` and `notNone` are aliases.

### Default

Setting `default=None` for the column allows the value to be omitted when inserting
a row using SQLObject. However, it does not add a default in the
schema, in SQLite at least.

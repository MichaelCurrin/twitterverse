# SQLObject Tips
> General tips for working with the database models.


Links:

- [lib/database.py](https://github.com/MichaelCurrin/twitterverse/blob/master/app/lib/database.py) module.
- [lib/models](https://github.com/MichaelCurrin/twitterverse/blob/master/app/models/) module.
- [SQLObject](http://sqlobject.org) - used as the ORM.

See also the [models](development/models.md) doc page.

## Queries with the ORM.

SQLObject doc links of selections:

- [Select Results](http://sqlobject.org/SelectResults.html) object
- [Selecting multiple objects](http://sqlobject.org/SQLObject.html#selecting-multiple-objects)
- [Select objects using relationships](http://sqlobject.org/SQLObject.html#selecting-objects-using-relationships)

SQLObject provides ways of selecting and filtering database records using Python. You can iterate over select results and each item will be an instance of a model class/table. e.g. `Tweet` class is used for the `tweet` table.


## Accessing models.

In the _app_ directory, open a Python console.

The models can be found in the [models](https://github.com/MichaelCurrin/twitterverse/blob/master/app/models/) module. These are made available on the database module.

Import the database module and access class.

```python
>>> from lib import database as db
>>> db.Tweet
models.tweets.Tweet
```

The location of the class in the modules structure is shown.


## Run queries with the ORM

Notes:

- In the examples below, `Profile` could be replaced with one of the other model names.
- Results are usually an iterator. This can be expensive to do all at once, so you could use `list` or iterate over.

```python
>>> results = db.Profile.select()
```

```python
>>> # Count the results. This is efficient and does not involve getting each record.
>>> results.count()
1234
```

Select results are returned as an iterator, which fetches lazily.

```python
>>> # This can be converted to a list, which can take a few seconds. Each
>>> # item in the list will be an instance of Profile class in this case.
>>> my_list = list(results)

>>> # Or, iterate over results. Each item will lazily fetched
>>> for x in results:
...     print(x)
```

Slice the results.

```python
>>> subset = results[0:5]

>>> # Get one result using of these options.
>>> results[0]
>>> results.getOne()
```

One or more filters can be applied to a select results instance, to apply filtering. This can be more efficient to do _before_ iterating.

```python
>>> results.filter(db.Profile.q.name == 'foo')
>>> results.filter(db.Profile.q.name.startswith('foo'))
```

Instead of using `.filter`, you can apply the condition directly to `.select`.
```
>>> from sqlobject import OR
>>> results = db.Tweet.select(
    OR(
        db.Tweet.q.favoriteCount > 5,
        db.Tweet.q.retweetCount > 5,
    )
)
```

For simple filtering on one more attributes, pass keyword parameters to `.selectBy`.

```python
>>> search = db.Tweet.selectBy(foo='bar', baz=123)
```


## Reasoning behind column attributes

Some general notes on using and understanding SQLObject.

### Not null

SQLObject's column validation by default requires a value for a column
when creating it. Even if the value is set as `db.MyTable(myColumn=None)`
and even though there is no `NOT NULL` constraint when checking the table's schema. Therefore it is a good idea add `notNull=True` in the model, to add this as a constraint for when doing SQL queries directly. In the SQLObject code, `notNull` and `notNone` are aliases.

### Default

Setting `default=None` for the column allows the value to be omitted when inserting
a row using SQLObject. However, it does not add a default in the
schema, in SQLite at least.


## View column definitions

A table's column definitions are available on the table's `sqlmeta` class.

```python
from lib import database as db

# Returns a dictionary.
colDefs = db.Tweet.sqlmeta.columnDefinitions

for k, v in colDefs.items():
    print(k, v)
# => retweetCount <IntCol 7f56142b11d0 retweetCount>
# => etc.
```


## View the create table SQL

Print out the SQL statement used to create the table. Note that `.createTable` will _create_ the table in the db, while the method below will only _return_ SQL statements without executing.

```python
>>> # Get create table statement and a list of constraints statements.
>>> sql, contraints = db.Tweet.createTableSQL()
>>> print(sql)
CREATE TABLE tweet (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    guid INT NOT NULL UNIQUE,
    ...
);
>>> print(constraints)
[]
>>> # Optionally, exclude the join tables and index from the sql, since they are on by default.
>>> db.Tweet.createTableSQL(createJoinTables=False, createIndexes=False)
...
```

See SQLObject's `main.py` or `dbconnection.py` files for more detail.


Alternatively, view all create statements in sqlite itself, assuming the `lib/database.py` script has already been run with the `--create` flag.

```bash
$ # From project root.
$ make sql
sqlite> .schema
...
```

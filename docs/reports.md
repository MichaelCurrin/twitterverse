# Reports

## Database overview

### Table names and record counts

```bash
$ utils/db_manager.py --summary
```

```
Getting table summary...
Table           | Rows
================|===============
Place           |   471
Supername       |     1
Continent       |     6
```

### Preview table rows

Get 10 rows from each of the tables and display them using the Python ORM representations.

```bash
$ python -m lib.db_query.schema.preview
```

```
Results preview

Place (471)
===
<Continent 2 supernameID=1 woeid=24865670 name='Africa' timestamp='datetime.datetime...)'>
<Continent 3 supernameID=1 woeid=24865671 name='Asia' timestamp='datetime.datetime...)'>
```

## Reports

Report on tweets and profiles or trends and places.

This project includes a [lib/db_query](https://github.com/MichaelCurrin/twitterverse/tree/master/app/lib/db_query) section which allows DB queries to be done with the ORM or SQL. See [SQLObject documentation](http://www.sqlobject.org/) for more info.

### ORM queries

Run a Python script directly. Note you must import a script as a module.

Example:

```bash
$ python -m lib.db_query.place.country_report --name
```

### SQL queries

Execute SQL statements and store output as CSV file.

Use the `-csv` flag to get comma-separated values of rows and use `-header` to include the header.

Examples:

-   ```bash
    $ cat lib/query/sql/tweets/allTweets.sql | sqlite3 -csv -header \
        var/db.sqlite > var/reporting/fileName.csv
    ```
-   ```
    $ sqlite3 -csv -header var/db.sqlite < lib/query/sql/tweets/allTweets.sql \
        > var/reporting/fileName.csv
    ```

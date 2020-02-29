# Reports
> How to get DB overview and run reports

## Database overview

### Table names and record counts

```bash
$ cd app/utils
```

```bash
$ ./db_manager.py --summary
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

## How to run reports

Run reports data stored in the DB.

Reports are mostly focused on tweets and profiles, or trends and places. Some print to the screen as text and some are CSV reports.

See queries to run in the [db_query](https://github.com/MichaelCurrin/twitterverse/tree/master/app/lib/db_query) directory.

```bash
$ cd app
$ ls lib/db_query
```

### ORM queries

Run Python scripts which use the ORM for reports.

Note that unlike the _utils_ directory of executables, _lib_ directory Python scripts must be imported `-m` flag as below.

Example:

```bash
$ python -m lib.db_query.place.country_report --name
```

See [SQLObject documentation](http://www.sqlobject.org/) for more info on how ORM queries work.

### SQL queries

Execute SQL statements and store output as CSV file.

Use the `-csv` flag to get comma-separated values of rows and use `-header` to include the header.

All the SQL queries are in this directory.

```bash
$ ls lib/db_query/sql
```

Choose a query and run it with SQLite.


#### Basic execute

SQLite queries can be sent using two approaches:

- `cat` command.
    ```sh
    $ cat <PATH_TO_QUERY> | sqlite3 <DB_PATH>
    ```
- Redirection.
    ```sh
    $ sqlite3 <DB_PATH> < <PATH_TO_QUERY>
    ```

The results will be printed and not stored.

Replace `<DB_PATH>` with `$(utils/db_manager.py --path)` to use the configured DB path.

To check it:

```sh
echo $(utils/db_manager.py --path)
```

#### Execute and store as CSV

To format as a CSV with a header, add flags. To save, redirect to file.

Example:

```bash
$ sqlite3 -csv -header $(utils/db_manager.py --path) \
    < lib/db_query/sql/tweets/allTweets.sql \
    > var/reporting/my_file.csv
```

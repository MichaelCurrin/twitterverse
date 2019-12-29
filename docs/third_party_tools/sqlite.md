# SQLite tips

See this [quickstart guide](https://www.techinfected.net/2018/01/how-to-install-sqlite3-in-ubuntu-linux-mint.html) to install and use SQLite if you are not familiar with it.

Note this doc assumes you are in the directory where database files are stored.

```bash
$ cd app/var/lib/
```

## Check version

Version `3.16.2` was used for the original development of this repo.

```bash
$ sqlite3 --version
```

## Queries

There are multiple ways to run a query in SQLite.

1. SQL as argument. `sqlite3 db.sqlite 'SELECT COUNT(*) FROM tweet'`
2. SQL as file. `sqlite3 db.sqlite < query.sql`
3. SQL as piped text. `echo 'SELECT COUNT(*) FROM tweet' | sqlite3 db.sqlite`
4. Open SQLite on the command line and type or paste queries. See [Working in SQLite](#working-in-sqlite) below.

## Output formats

How to get reports out of SQLite.

The default output does not include a header and uses `|` symbol to separate columns. See output approaches below.

### Column report in terminal

```bash
$ sqlite3 db.sqlite -header -column "SELECT * FROM Tweet LIMIT 10;"
```

### Export to CSV

Note that this output is not that readable on the terminal because all the white space is taken out, but it will open fine in a CSV editor.

```bash
$ sqlite3 db.sqlite -header -csv "SELECT * FROM Tweet LIMIT 10;" > data.csv
```

### Export to HTML

```bash
$ sqlite3 db.sqlite -header -html "SELECT * FROM Tweet LIMIT 10;" > data.html
```


## Working in SQLite

```
$ sqlite3
sqlite> .headers on
sqlite> .mode csv
sqlite> SELECT * FROM Tweet;
```


```bash
$ sqlite3 db.sqlite .tables
```

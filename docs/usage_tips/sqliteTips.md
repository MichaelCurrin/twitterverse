# SQLite tips

See this [quickstart guide](https://www.techinfected.net/2018/01/how-to-install-sqlite3-in-ubuntu-linux-mint.html) to install and use SQlite if you are not familar with it.

## Check version

Version `3.16.2` was used for the original development of this repo.

```bash
$ sqlite3 --version
```

## Export

Export to CSV

```bash
$ echo "SELECT * from Country LIMIT 10;" | sqlite3 db.sqlite -header -csv > data.csv
```

Export to HTML

```bash
$ echo "SELECT * from Country LIMIT 10;" | sqlite3 db.sqlite -header -html > data.html
```


## Working in SQLite

```
$ sqlite3
sqlite> .headers on
sqlite> .mode csv
sqlite> SELECT * FROM Country;
```


```bash
$ sqlite3 db.sqlite .tables
```


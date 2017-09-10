# SQLite tips

## Export

Export to CSV

`echo "SELECT * from Country LIMIT 10;" | sqlite3 db.sqlite -header -csv > data.csv`

Export to HTML

`echo "SELECT * from Country LIMIT 10;" | sqlite3 db.sqlite -header -html > data.html`


## Working in SQLite

```
$ sqlite3
sqlite> .headers on
sqlite> .mode csv
sqlite> SELECT * FROM Country;
```

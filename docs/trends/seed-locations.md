# Seed locations
> How to add location data to the database using fixtures.

## Populate

Populate the database with location data and links between those records.

The locations were originally fetched from Twitter and are assumed to stay the same. They are stored in the repo as [locations_data.json](https://github.com/MichaelCurrin/twitterverse/blob/master/app/var/sample/locations_data.json).

```bash
$ ./utils/db_manager.py --populate --summary
```

## Summary

Check the summary view to see how many records you have for _Country_, _Trend_, etc.

Below is an example view.


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
Country         |    62
Town            |   402
Trend           |     0
Profile         |     0
Tweet           |     0
Category        |     4
ProfileCategory |     0
Campaign        |     0
TweetCampaign   |     0
PlaceJob        |     0
```

Note this uses ORM names and not DB schema names. This view includes all the countries and towns which Twitter provides data for in its API, plus some _Place_, _Supername_ and _Continent_ are used to give them more structure to allow say filtering towns in a certain country or continent.

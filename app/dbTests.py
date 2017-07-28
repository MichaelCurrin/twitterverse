# -*- coding: utf-8 -*-
"""
Filter
    http://sqlobject.org/SelectResults.html#filter-expression
Builder expressions
    http://sqlobject.org/SQLBuilder.html
Like
    https://stackoverflow.com/questions/1003506/executing-sql-like-in-sqlobject

Date range
    https://groups.google.com/forum/#!topic/turbogears/_cwaU86NDfU
"""
import datetime

import sqlobject.sqlbuilder as builder

from lib import database as db, places, twitterAuth
from lib.config import AppConf

appConf = AppConf()

api = twitterAuth.getAPIConnection()


def searchCountry(searchStr='', startswith=False):
    """
    LIKE, startswith and endswith seem to be case insensitive at least when using SQLite as db.
    """
    if startswith:
        condition = db.Country.q.name.startswith(searchStr)
    else:
        condition = builder.LIKE(db.Country.q.name, '%{}%'.format(searchStr))

    res = db.Country.select().filter(condition)

    return res


def searchTowns(searchStr='', startswith=False):
    """
    LIKE, startswith and endswith seem to be case insensitive at least when using SQLite as db.
    """
    if startswith:
        condition = db.Town.q.name.startswith(searchStr)
    else:
        condition = builder.LIKE(db.Town.q.name, '%{}%'.format(searchStr))

    res = db.Town.select().filter(condition)

    return res


### Tempory tests ###

def _testSearchTowns(searchStr='ca'):
    print 'TOWNS SEARCH'
    print searchStr
    res = searchTowns(searchStr)
    print
    print str(res)
    print
    for town in res:
        print u'{:10d} - {}'.format(town.woeid, town.name)
    print
    print '-------'
    '''
    # Sample
    23424800 - Dominican Republic
     *      76456 - Santo Domingo

    23424942 - South Africa
     *    1580913 - Durban
     *    1582504 - Johannesburg
     *    1586614 - Port Elizabeth
     *    1586638 - Pretoria
     *    1591691 - Cape Town
    '''

def _testSearchCountry(searchStr='ica'):
    print 'COUNTRY SEARCH'
    print searchStr
    res = searchCountry(searchStr)
    print
    print str(res)
    print
    for country in res:
        print u'{} - {}'.format(country.woeid, country.name)
        for town in country.hasTowns:
            print u' * {:10d} - {}'.format(town.woeid, town.name)
        print
    '''
    # Sample
          8775 - Calgary
         15127 - Cardiff
         30079 - Newcastle
        110978 - Acapulco
        111579 - Aguascalientes
        118466 - Ecatepec de Morelos
        133475 - Mexicali
        134395 - Naucalpan de Juárez
        149769 - Toluca
        368149 - Cali
        395269 - Caracas
        395270 - Maracaibo
        395271 - Maracay
        455828 - Campinas
       1100968 - Canberra
       1167715 - Calocan
       1199002 - Cagayan de Oro
       1252351 - Can Tho
       1521894 - Cairo
       1591691 - Cape Town
       1939897 - Mecca
       2268284 - Muscat
       2379574 - Chicago
    '''


def _testTweepyTrends():
    """
    This is used for testing only and can be replaced by other functions which
    are in use.
    """
    global api
    # Read in configured city ID.
    cityWoeid = conf.getint('tests', 'cityWoeid')

    # Ignore 'created_at' and 'as_of' and just use 'trends'. There is a list of one item so we have to take first and only the item.

    cityTrends = api.trends_place(cityWoeid)[0]['trends']
    ##print api.trends_place(cityWoeid)[0]['created_at']
    ## 2017-07-14T22:03:14Z
    ## note this is GMT+0000

    print 'GET TRENDS FOR LOCATION FROM TWEEPY'
    for x in cityTrends:
        topic = x['name']
        volume = x['tweet_volume']
        t = db.Trend(topic=topic, volume=volume).setPlace(cityWoeid)
        print u'Created - Trend: {0} | {1} | {2}.'.format(cityWoeid, topic, volume)


def _testHighestWithDate():
    global api

    cityWoeid = conf.getint('tests', 'cityWoeid')

    print 'GET HIGHEST TRENDS FOR LOCATION, FOR DATE RANGE'
    # End date will start at midnight so have to add a day to include whole day. And we use < to exclude start of the day.
    endDate = datetime.date.today() + datetime.timedelta(days=1)
    startDate = endDate - datetime.timedelta(days=7)
    print startDate
    print endDate
    # use timezone aware column for timestamp?
    # timezone aware datetime?

    # use datetime.datetime for past 24 hours instead of today?

    if True:
        # Using Town causes an error on ambiguous sort id. And adding order by here doesn't work.
        city = db.Place.byWoeid(cityWoeid)
        assert city is not None, 'Expected city to be returned for {}.'.format(cityWoeid)
        cityID = city.id
    else:
        # Alternative.
        cityRes = db.Town.select(db.Town.q.woeid == cityWoeid)
        city = cityRes.getOne() if cityRes else None
        assert city is not None, 'Expected city to be returned for {}.'.format(cityWoeid)
        cityID = city.id

    res = db.Trend.select(
        builder.AND(db.Trend.q.placeID == cityID,
                    db.Trend.q.timestamp >= startDate,
                    db.Trend.q.timestamp < endDate,
                    )
        ).orderBy('volume desc').limit(5)

    print res
    for x in res:
        print x


def _testTwoCities(freshPull=True):
    """
    Lookup trends for two cities.

    Find topics which appear at least once, or are common or exclusive
    (one but not the other).

    Set freshPull to false if you know you have the data in the db and
    want to select it to work with it.
    """
    global api
    # Specify country because there can be towns with same name in different countries.
    country = 'South Africa'
    townNames = ['Cape Town', 'Johannesburg']

    # Orderby should be set explicitly here to avoid ambiguity error when place.id and country.id are used to compare, but order by is just on 'id'.
    # This could possibly be removed now that default order has been removed from model.
    countryObj = db.Country.selectBy(name=country).orderBy('place.id')
    countryID = countryObj.getOne().id

    townObjList = []
    for tName in townNames:
        townObj = db.Town.select(builder.AND(db.Town.q.name == tName,
                                             db.Town.q.countryID == countryID)
                                ).orderBy('place.id')
        townObjList.append(townObj.getOne())

    # Now we have the town objects we can look up trends against their IDs.

    if freshPull:
        print 'INSERT INTO DB'
        print 'ID Name WOEID'
        for x in townObjList:
            print x.id, x.name, x.woeid
            insertTrendsForWoeid(x.woeid)
            print
        print

    print 'DO STATS ON TOPICS'
    # Timestamp - select from start of today.

    # Retrieve the values we just added to the db. Normally the time gap would
    # be larger - cronjob to insert the records on schedule and at another
    # time in the day get records for that day or any date range.
    if False:
        woeidList = [x.woeid for x in townObjList]

        # Select Place objects (and ids) for Places we are looking for.
        subquery = db.Place.select(builder.IN(db.Place.q.woeid,
                                              woeidList))
        print subquery

        # Select trends matching any of the Places we are looking for.
        todayTrends = db.Trend.select(builder.AND(
            builder.IN(db.Trend.q.placeID, subquery),
            db.Trend.q.timestamp >= datetime.date.today()
            )
        )

        print todayTrends.count()

        for t in todayTrends:
            print t.topic
        print

    print 'DO STATS ON TOPICS - ALTERNATIVE'
    # Instead of using IN as above and putting all trends together and then having to look up what regularly queries to get what place matches the place ID, this approach keeps the trends separated by place using a list (this could be list of dictionaries so it wouldn't have to be matched with the first list).
    # Use for loop instead of a subquery.

    todayTrendsAlt = []
    for x in townObjList:
        trendGroup = []
        trendSelection = db.Trend.select(builder.AND(
            db.Trend.q.timestamp >= datetime.date.today(),
            db.Trend.q.placeID == x.id
            )
        )
        for t in trendSelection:
            trendGroup.append(t)
        todayTrendsAlt.append(trendGroup)

    for i, x in enumerate(todayTrendsAlt):
        print townObjList[i].name.upper()
        print len(x)
        for y in x:
            print y.topic
        print


    print 'SUMMARY STATS'

    from collections import Counter

    trendList = []
    c = Counter()

    for town in todayTrendsAlt:
        townTopics = [trend.topic for trend in town]
        trendList.append(townTopics)
        c.update(townTopics)

    trendSetList = [set(x) for x in trendList]

    print 'All trends'
    # Get items which appear at least once across towns.
    allTrends = set.union(*trendSetList)
    print allTrends
    print

    print 'Overlap'
    # Get items which show overlap between towns.
    overlap = set.intersection(*trendSetList)
    print overlap
    print


    print 'Exclusive'
    # Get what is current town and not the others.
    for i, x in enumerate(trendList):
        exclusive = set(x) - overlap
        print '*', townObjList[i].name
        print exclusive
    print


    print 'Counter'
    print '======='
    # Get counts of words across Places.

    # print ' Sorted default.'
    # # No useful order here.
    # for x in c.keys():
    #     # Use key and value.
    #     print u'{1:5d} | {0:20}'.format(x, c[x])
    # print

    print ' Sorted by most common'
    for x in c.most_common():
        # Unpack tuples.
        print u'{1:5d} | {0:20}'.format(*x)
    print

    print ' Sorted alphabetically'
    for x in sorted(c.keys()):
        # Use key and value.
        print u'{1:5d} | {0:20}'.format(x, c[x])
    print


def _test_distinct():
    ## This will apply distinct across all columns.
    ## db.Trend.select(distinct=True)

    # Unique place and topic combinations (regardless of time).
    select = builder.Select(
            [db.Trend.q.place, db.Trend.q.topic],
             distinct=True,
             )

    sql = db.conn.sqlrepr(select)

    for item in db.conn.queryAll(sql):
        print item


def _test_group():
    # http://sqlobject.org/SQLBuilder.html?highlight=group
    # Count of terms grouped by hashtag.
    select = builder.Select(
                ['hashtag', 'COUNT(topic)'],
                staticTables=['Trend'],
                groupBy='hashtag',
                )
    sql = db.conn.sqlrepr(select)

    for item in db.conn.queryAll(sql):
        print item


def _test_dateDistinct():
    # Occurences of topic on date without place, ignoring duplicates
    # on same day. In this case we don't need an aggregation rule so
    # distinct will work just as well as groupy by.
    select = builder.Select(
                ['DATE(timestamp) AS date', 'topic'],
                staticTables=['Trend'],
                distinct=True,
                orderBy='date DESC'
                )
    sql = db.conn.sqlrepr(select)
    print sql

    res = db.conn.queryAll(sql)

    print len(res)
    print
    for item in res:
        print item


def _test_dateGroup():
    """
    Variation of above.
    Remove duplicate date-topic-place combinations then count the places.
    """

    # NOTE: DISTINCT ON does not work in SQLite

    # Get date from datetime
    # Apply distinct to remove occurences of place pulled multiple times on one day.
    subquery = builder.Select(
                ['DATE(timestamp) AS date', 'topic', 'place_id'],
                staticTables=['trend'],
                distinct=True,
                )
    subsql = db.conn.sqlrepr(subquery)

    # Do a grouping and place count on the previous query.
    select = builder.Select([
                'date', 'topic', 'COUNT(place_id)'],
                staticTables=['({0})'.format(subsql)],
                groupBy='date, topic',
                orderBy='date ASC, COUNT(place_id) DESC, topic DESC',
                )

    sql = db.conn.sqlrepr(select)

    print sql

    res = db.conn.queryAll(sql)

    print len(res)
    print
    for item in res:
        print item


def _testAllPlacesCount():
    """
    Take all Places, get the trends and count places against the trends. All the places should be of the same time (all towns or all countries.)

    Broken down by day or for the period.

    @param woeidIDs: Leave empty to show all items. Otherwise filter by places in list.
    """

    #print placeFilter
    subquery = builder.Select(
                ['DATE(timestamp) AS date', 'topic', 'place_id'],
                staticTables=['trend'],
                distinct=True,
                )

    subsql = db.conn.sqlrepr(subquery)
    print subsql

    res = db.conn.queryAll(subsql)
    print len(res)

'''
def _testManyPlacesCount(woeidIDs=[]):
    """
    Take any number of given places, get the trends and count places against the trends. All the places should be of the same time (all towns or all countries.)

    Broken down by day or for the period.

    @param woeidIDs: Leave empty to show all items. Otherwise filter by places in list.
    """
    placeFilter = db.Place.select(
            builder.IN(db.Place.q.woeid, woeidIDs) if woeidIDs else True
            )
    print placeFilter

    # why is timestamp ambiguous?
    # how can I filter on or off? Maybe two queries since this is a test.
    #print placeFilter
    subquery = builder.Select(
                ['DATE(trend.timestamp) AS date', 'trend.topic', 'trend.place_id'],
                staticTables=['trend'],
                join='INNER JOIN place ON place.id = trend.place_id',
                distinct=True,
                where=placeFilter,
                #orderBy='timestamp'
                )
    #

    subsql = db.conn.sqlrepr(subquery)
    print subsql

    res = db.conn.queryAll(subsql)
    print len(res)
'''


def trendCountForPlaces(woeidIDs=[], daysAgo=1):
    """
    Take any number of given places, get the trends count for the places.
    """
    if not woeidIDs:
        countryName = conf.get('Cron', 'countryName')
        print 'Configured country: {}\n'.format(countryName)
        woeidIDs = places.countryAndTowns(countryName)

    placeList = db.Place.select(builder.IN(db.Place.q.woeid, woeidIDs))

    # Past N days.
    endDate = datetime.date.today() + datetime.timedelta(days=1)
    startDate = endDate - datetime.timedelta(days=daysAgo)

    dateRange = builder.AND(db.Trend.q.timestamp >= startDate,
                            db.Trend.q.timestamp < endDate)

    print 'This shows how many trend records have been stored for each place for the date range.'
    print 'Trends | Place'
    print '===================='
    for p in placeList:
        res = db.Trend.select(dateRange).filter(db.Trend.q.placeID == p.id)
        print '{0:6,d} | {1}'.format(res.count(), p.name)
    print


def _testPlaceVolume():
    """
    Get trends for say country or town and rank trends by volume.
    """
    pass


def _testManyPlacesVolume():
    """
    Get trends for many places either as countries, or towns in a country or towns across countries, and rank trends by volume within each.
    """
    pass

def getChildPlaces(woeid):
    """
    Receive a Place ID and return all it's direct child records available in the database.
    """
    pass



def getCountryAndCities(countryName='', countryWoeid=0):
    """
    Receive a country name or WOEID and return Country record as well as all Town records available in the database for that Country.
    """
    pass


if __name__ == '__main__':
    # _testSearchTowns()
    # _testSearchCountry()
    # _testHighestWithDate()
    #_testTwoCities(freshPull=False)
    #_testTwoCities(freshPull=True)
    #_test_dateGroup()

    #trendCountForPlaces(daysAgo=1)


    countryName = conf.get('Cron', 'countryName')
    woeidIDs = places.countryAndTowns(countryName)
    woeidIDs = (woeidIDs[0])
    _testAllPlacesCount()
    _testManyPlacesCount(woeidIDs)

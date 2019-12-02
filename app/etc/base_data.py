# -*- coding: utf-8 -*-
"""
Default data records and associations, used to setup the database.
"""


# Place data

# Mapping of continent names to WOEID values. The WOEIDs were looked up from
# Yahoo index since they did not appear in Twitter API.
continentBase = {
    24865670: u'Africa',
    24865671: u'Asia',
    24865675: u'Europe',
    24865672: u'North America',
    55949069: u'Oceana',
    24865673: u'South America',
}

# A manual mapping of continents to countries, based on country data available
# in the Twitter API.
continentMapping = {
    u'Africa': [
        u'Nigeria',
        u'Ecuador',
        u'Ghana',
        u'Algeria',
        u'Dominican Republic',
        u'Egypt',
        u'South Africa',
        u'Kenya'],
    u'Asia': [
        u'Qatar',
        u'Kuwait',
        u'Israel',
        u'Korea',
        u'Singapore',
        u'Thailand',
        u'Jordan',
        u'Oman',
        u'Bahrain',
        u'Philippines',
        u'Indonesia',
        u'Saudi Arabia',
        u'Turkey',
        u'Japan',
        u'Russia',
        u'Pakistan',
        u'United Arab Emirates',
        u'Lebanon',
        u'India',
        u'Malaysia',
        u'Vietnam'],
    u'Europe': [
        u'Italy',
        u'France',
        u'Ireland',
        u'Norway',
        u'Belarus',
        u'Belgium',
        u'Germany',
        u'Poland',
        u'Spain',
        u'Ukraine',
        u'Netherlands',
        u'Denmark',
        u'Sweden',
        u'Switzerland',
        u'Portugal',
        u'United Kingdom',
        u'Austria',
        u'Latvia',
        u'Greece'],
    u'North America': [
        u'Canada',
        u'Panama',
        u'Puerto Rico',
        u'Guatemala',
        u'United States'],
    u'Oceana': [
        u'Australia',
        u'New Zealand'],
    u'South America': [
        u'Brazil',
        u'Peru',
        u'Argentina',
        u'Venezuela',
        u'Chile',
        u'Mexico',
        u'Colombia'],
}

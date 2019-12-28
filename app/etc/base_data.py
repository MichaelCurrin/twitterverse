# -*- coding: utf-8 -*-
"""
Default data records and associations, used to setup the database.
"""


# Place data

# Mapping of continent names to WOEID values. The WOEIDs were looked up from
# Yahoo index since they did not appear in Twitter API.
continentBase = {
    24865670: 'Africa',
    24865671: 'Asia',
    24865675: 'Europe',
    24865672: 'North America',
    55949069: 'Oceana',
    24865673: 'South America',
}

# A manual mapping of continents to countries, based on country data available
# in the Twitter API.
continentMapping = {
    'Africa': [
        'Nigeria',
        'Ecuador',
        'Ghana',
        'Algeria',
        'Dominican Republic',
        'Egypt',
        'South Africa',
        'Kenya'],
    'Asia': [
        'Qatar',
        'Kuwait',
        'Israel',
        'Korea',
        'Singapore',
        'Thailand',
        'Jordan',
        'Oman',
        'Bahrain',
        'Philippines',
        'Indonesia',
        'Saudi Arabia',
        'Turkey',
        'Japan',
        'Russia',
        'Pakistan',
        'United Arab Emirates',
        'Lebanon',
        'India',
        'Malaysia',
        'Vietnam'],
    'Europe': [
        'Italy',
        'France',
        'Ireland',
        'Norway',
        'Belarus',
        'Belgium',
        'Germany',
        'Poland',
        'Spain',
        'Ukraine',
        'Netherlands',
        'Denmark',
        'Sweden',
        'Switzerland',
        'Portugal',
        'United Kingdom',
        'Austria',
        'Latvia',
        'Greece'],
    'North America': [
        'Canada',
        'Panama',
        'Puerto Rico',
        'Guatemala',
        'United States'],
    'Oceana': [
        'Australia',
        'New Zealand'],
    'South America': [
        'Brazil',
        'Peru',
        'Argentina',
        'Venezuela',
        'Chile',
        'Mexico',
        'Colombia'],
}

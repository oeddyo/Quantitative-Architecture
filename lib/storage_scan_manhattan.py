"""This script contains all the mysql fetching and saving functions so that this could be independent of main logics

"""

import mysql_connect
import datetime
import json

def save_venue_meta(venue):
    """Save meta data for a single venue into mysql (table venue_meta)
See table 'venue_meta' for details of fields
Keyword arguments
venue - Venue object """
    #print venue['venue'].keys()
    venue_dic = venue['venue']
    id = venue_dic['id']
    name = venue_dic.get('name',None)
    lat = venue_dic['location']['lat']
    lng = venue_dic['location']['lng']
    if len(venue_dic['categories'])>0:
        categoriesID = venue_dic['categories'][0].get('id', None)
        categoriesName = venue_dic['categories'][0].get('name', None)
    else:
        categoriesID = categoriesName = None
    postalCode = venue_dic['location'].get('postalCode',None)
    city = venue_dic['location'].get('city',None)
    state = venue_dic['location'].get('state',None)
    country = venue_dic['location'].get('country',None)
    if venue_dic['verified'] == True:
        verified = 1
    else:
        verified = 0
    checkinsCount = venue_dic['stats'].get('checkinsCount', None)
    usersCount = venue_dic['stats'].get('usersCount',None)
    tipCount = venue_dic['stats'].get('tipCount',None)
    likesCount = venue_dic['likes'].get('count',None)
    cursor = mysql_connect.connect_to_mysql()
    cursor.execute("REPLACE INTO manhattan_venues_meta (id, name, lat, lng, categoriesID, categoriesName, postalCode, city, state, country, verified, checkinsCount, usersCount, tipCount, likesCount) values (%s" + ",%s"*14 + ")", (id, name, lat, lng, categoriesID, categoriesName, postalCode, city, state, country, verified, checkinsCount, usersCount, tipCount, likesCount) )
    #cursor.execute(sql)


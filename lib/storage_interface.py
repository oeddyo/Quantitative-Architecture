"""This script contains all the mysql fetching and saving functions so that this could be independent of main logics

"""

import mysql_connect


def save_venue_meta(venue):
    """Save meta data for a single venue into mysql (table venue_meta)
See table 'venue_meta' for details of fields
Keyword arguments
venue - Venue object """
    print venue['venue'].keys()
    venue_dic = venue['venue']
    id = venue_dic['id']
    name = venue_dic.get('name',None)
    lat = venue_dic['location']['lat']
    lng = venue_dic['location']['lng']
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
    url = venue_dic.get('url', None)
    likesCount = venue_dic['likes'].get('count',None)
    rating = venue_dic.get('rating',None)
    ratingSignals = venue_dic.get('ratingSignals',None)
    photoCount = venue_dic['photos'].get('count',None)
    tmp_list = [id, name, lat, lng, postalCode, city, state, country, verified, checkinsCount, usersCount, tipCount, url, likesCount, rating, ratingSignals, photoCount]
    cursor = mysql_connect.connect_to_mysql()
    cursor.execute("REPLACE INTO venue_meta (id, name, lat, lng, postalCode, city, state, country, verified, checkinsCount, usersCount, tipCount, url, likesCount, rating, ratingSignals, photoCount) values ('%s'" + ",'%s'"*16 + ")", (id, name, lat, lng, postalCode, city, state, country, verified, checkinsCount, usersCount, tipCount, url, likesCount, rating, ratingSignals, photoCount) )
    #cursor.execute(sql)

def save_venue_photo_4sq(photo, venue_id):
    """Save photos from 4sq into table venue_photo_4sq
    See table 'venue_photo_4sq' for columns detail.
    Keyword arguments
    photo - photos from 4sq 
    venue_id - venue id for this venue. Used as a foreign key"""
    cursor = mysql_connect.connect_to_mysql()
    for pic in photo['photos']['items']:
        print pic
        print '\n\n'
        id = pic['id']
        createdAt = pic.get('createdAt',None)
        source_name = pic['source'].get('name', None)
        source_url = pic['source'].get('url', None)
        url = pic.get('url', None)
        user_id = pic['user'].get('id',None)
        user_firstName = pic['user'].get('firstName',None)
        user_lastName = pic['user'].get('lastName', None)
        user_photo = pic['user'].get('photo',None)
        user_gender = pic['user'].get('gender',None)
        user_homeCity = pic['user'].get('homeCity',None)
        user_tips = pic['user']['tips'].get('count',None)
        cursor.execute("REPLACE INTO venue_photo_4sq (venue_id, id, createdAt, source_name, source_url, url, user_id, user_firstName, user_lastName, user_photo, user_gender, user_homeCity, user_tips) values (%s" + ",%s"*12+")", (venue_id, id, createdAt, source_name, source_url, url ,user_id, user_firstName, user_lastName, user_photo, user_gender, user_homeCity, user_tips) )


def save_venue_tip(tips, venue_id):
    """Save tips from 4sq into table venue_tips.
    See table 'venue_tips' for columns detail.
    Keyword arguments
    tips - tips from 4sq given a venue id
    venue_id - venue id for this venue. This is used as a foreign key so that we could fetch venue details from venue_meta table"""
    cursor = mysql_connect.connect_to_mysql()
    for tip in tips['tips'].get('items', None):
        id = tip['id']
        createdAt = tip.get('createdAt',None)
        text = tip.get('text', None)
        likesCount = tip['likes'].get('count', None)
        user_id = tip['user'].get('id',None)
        user_firstName = tip['user'].get('firstName',None)
        user_lastName = tip['user'].get('lastName', None)
        user_photo = tip['user'].get('photo',None)
        user_gender = tip['user'].get('gender',None)
        user_homeCity = tip['user'].get('homeCity',None)
        user_tips = tip['user']['tips'].get('count',None)
        cursor.execute("REPLACE INTO venue_tips (venue_id, id, createdAt, text, likesCount, user_id, user_firstName, user_lastName, user_photo, user_gender, user_homeCity, user_tips) values (%s"+",%s"*11+")", (venue_id, id, createdAt, text, likesCount, user_id, user_firstName, user_lastName, user_photo, user_gender, user_homeCity, user_tips) )


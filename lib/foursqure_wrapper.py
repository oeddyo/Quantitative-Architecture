"""
    For a venue id, grab all it's meta data
"""
from instagram.client import InstagramAPI
import config
import foursquare
import time

def default_client():
    client = foursquare.Foursquare(config.foursquare_client_id, client_secret=config.foursquare_client_secret)
    return client

def download_meta_data(venue_id, client = default_client()):
    """Download meta data from foursquare API"""
    venue = client.venues(venue_id)
    return venue

def download_venue_photo(venue_id, client = default_client()):
    """Download photos for a venue using foursquare API"""
    count = 0
    for offset in range(0, 1000, 200):
        print 'now off set ',offset
        venue_photo = client.venues.photos(VENUE_ID = venue_id, params = {'limit':200, 'group':'venue', 'offset':offset})
        for p in  venue_photo['photos']['items']:
            print p
        
        if len(venue_photo['photos']['items'])==0:
            break;
        yield venue_photo

def download_venue_tips(venue_id, client = default_client()):
    venue_tips = []
    for offset in range(0,1000,100):
        venue_tip = client.venues.tips(VENUE_ID = venue_id, params = {'limit':100, 'offset':offset} )
        if venue_tip['tips'].get('items',None) == None or len(venue_tip['tips']['items'])==0:
            break
        yield venue_tip

if __name__=='__main__':
    print 'Testing:'
    print 'Test download meta data'
    #print download_meta_data('4b903af5f964a520b77d33e3')

    #gen  = download_venue_photo('4c209648eac020a1c8b24cc2')
    #for g in gen:
    #    print g 
    gen = download_venue_tips('4ab79e30f964a520397a20e3')
    for g in gen:
        print g
        print '\n\n\n'

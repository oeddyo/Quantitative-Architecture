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
    client = default_client()
    print client.venues(venue_id)
    pass
    try:
        venue = client.venues(venue_id)
    except Exception as e:
        return e
    return [venue]

def download_venue_photo(venue_id, client = default_client()):
    """Download photos for a venue using foursquare API"""
    venue_photos = []
    try:
        for offset in range(0, 1000, 200):
            venue_photo = self.client.venues.photos(VENUE_ID = venue_id, params = {'limit':200, 'group':'venue', 'offset':offset})
            venue_photo.append(venue_photo)
    except:
        pass
    return venue_photos

def download_venue_tips(venue_id, client = default_client()):
    venue_tips = []
    try:
        for offset in range(0,1000,100):
            venue_tip = self.client.venues.tips(VENUE_ID = venue_id, params = {'limit':100, 'offset':offset} )
            venue_tips.append(venue_tip)
    except:
        pass
    return venue_tips

if __name__=='__main__':
    print 'Testing:'
    print 'Test download meta data'
    print download_meta_data('4b903af5f964a520b77d33e3')
    


"""
    For a venue id, grab all it's meta data
"""
from instagram.client import InstagramAPI
import foursquare
import config
import time

def default_client():
    return foursquare.Foursquare(config.foursquare_client_id, client_secret=config.foursquare_client_secret)

def download_meta_data(client = default_client(), venue_id):
    """Download meta data from foursquare API"""
    try:
        venue = client.veneus(venue_id)
    except:
        return None
    return [venue]

def download_venue_photo(client = default_client(), venue_id):
    """Download photos for a venue using foursquare API"""
    venue_photos = []
    try:
        for offset in range(0, 1000, 200):
            venue_photo = self.client.venues.photos(VENUE_ID = venue_id, params = {'limit':200, 'group':'venue', 'offset':offset})
            venue_photo.append(venue_photo)
    except:
        pass
    return venue_photos

def download_venue_tips(client = default_client(), venue_id):
    venue_tips = []
    try:
    for offset in range(0,1000,100):
        venue_tip = self.client.venues.tips(VENUE_ID = venue_id, params = {'limit':100, 'offset':offset} )
        venue_tips.append(venue_tip)
    except:
        pass
    return venue_tips


if __name__ == '__main__':
    pass

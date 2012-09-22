"""
    For a venue id, grab all it's meta data
"""

from lib.storage_interface import save_venue_meta
from lib.storage_interface import save_venue_photo_4sq
from lib.storage_interface import save_venue_tip
from lib.mysql_connect import add_table_venue_meta
from lib.mysql_connect import add_table_venue_photo_4sq
from lib.mysql_connect import add_table_venue_tips

import foursquare
import config


class VenueMetaCrawler:
    def __init__(self):
        self.client = foursquare.Foursquare(config.client_id, client_secret=config.client_secret)
    def grab_meta_data(self, venue_id):
        venue = self.client.venues(venue_id)
        save_venue_meta(venue)
        #print venue

class VenuePhotoCrawler:
    def __init__(self):
        self.client = foursquare.Foursquare(config.client_id, client_secret=config.client_secret)
    def grab_photo(self, venue_id):
        #venue_photo = self.client.venues.photos( params = {'VENUE_ID':venue_id, 'group':'venue'})
        print venue_id
        print 'here'
        for offset in range(0, 613, 200):
            venue_photo = self.client.venues.photos(VENUE_ID = venue_id, params = {'limit':200, 'group':'venue', 'offset':offset})
            save_venue_photo_4sq(venue_photo, venue_id)

class VenueTipsCrawler:
    def __init__(self):
        self.client = foursquare.Foursquare(config.client_id, client_secret=config.client_secret)
    def grab_tip(self, venue_id):
        for offset in range(0,6000,500):
            venue_tip = self.client.venues.tips(VENUE_ID = venue_id, params = {'limit':500, 'offset':offset} )
            save_venue_tip(venue_tip, venue_id)


def main():
    add_table_venue_meta()
    add_table_venue_photo_4sq()
    add_table_venue_tips()
    venue_id = '4dcc0c0e1fc7eca44b1f1ed6'
    crawler = VenueMetaCrawler()
    crawler.grab_meta_data(venue_id)
    crawler = VenuePhotoCrawler()
    crawler.grab_photo(venue_id)
    
    crawler = VenueTipsCrawler()
    crawler.grab_tip(venue_id)

main()

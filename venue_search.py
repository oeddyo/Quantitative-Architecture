"""
    For a venue id, grab all it's meta data
"""
from instagram.client import InstagramAPI
import foursquare

from lib.storage_interface import save_venue_meta
from lib.storage_interface import save_venue_photo_4sq
from lib.storage_interface import save_venue_tip
from lib.storage_interface import save_photo_instagram

from lib.storage_interface import get_all_foursquare_ids
from lib.storage_interface import get_all_photo_fetched_venue_id_instagram

from lib.mysql_connect import add_table_venue_meta
from lib.mysql_connect import add_table_venue_photo_4sq
from lib.mysql_connect import add_table_venue_tips
from lib.mysql_connect import add_table_venue_photo_instagram

import config
import time

class VenueSearch:
    def __init__(self):
        self.client = foursquare.Foursquare(config.foursquare_client_id, client_secret=config.foursquare_client_secret)
    def do_search(self,params):
        search_results = self.client.venues.search(params)
        return search_results['venues']

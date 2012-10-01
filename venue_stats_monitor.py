from lib.storage_interface import get_all_foursquare_ids
from lib.storage_interface import save_venue_stats
from lib.mysql_connect import add_table_venue_stats

import foursquare
import config



def checkin_update():
    """Update all the checkin info for each foursquare venue in database"""
    add_table_venue_stats()
    venue_ids = get_all_foursquare_ids()
    client = foursquare.Foursquare(config.foursquare_client_id, client_secret=config.foursquare_client_secret)
    for venue_id in venue_ids:
        #try:
        print venue_id
        venue_meta = client.venues(venue_id)
        save_venue_stats(venue_meta, venue_id)
        #except:
        #    continue


checkin_update()

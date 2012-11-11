"""
    For a venue id, grab all it's meta data
"""
from instagram.client import InstagramAPI
import foursquare


from lib.storage_interface import get_all_foursquare_ids
from lib.storage_interface import get_all_photo_fetched_venue_id_instagram

from lib.mysql_connect import add_table_venue_meta
from lib.mysql_connect import add_table_venue_photo_4sq
from lib.mysql_connect import add_table_venue_tips
from lib.mysql_connect import add_table_venue_photo_instagram

import config
import time

def default_client():
    self.client = InstagramAPI(client_id = config.instagram_client_id, client_secret = config.instagram_client_secret)

def download_instagram_photos(client = default_client(), venue_id):
    

class VenuePhotoCrawlerInstagram:
    def __init__(self):
        def fetch_instagram_id(self, foursquare_id):
            print 'foursquare id is ',foursquare_id
        res = self.client.location_search(foursquare_v2_id=foursquare_id)
        return res[0].id
    def show_popular(self):
        popular_media = self.client.media_popular(20)
        for media in popular_media:
            print media.caption.text
    def grab_photos(self, foursquare_id, max_pages, min_timestamp):
        try:
            instagram_id = self.fetch_instagram_id(foursquare_id)
            gen = self.client.location_recent_media(count=200, location_id = instagram_id, as_generator=True, max_pages=max_pages, min_timestamp = min_timestamp)
            page_cnt = 0
        except:
            return 
        for page in gen:
            save_photo_instagram(page[0], foursquare_id, instagram_id)    
            print 'fetching page',page_cnt
            page_cnt+=1
            time.sleep(config.instagram_API_pause)

def instagram_test():
    add_table_venue_photo_instagram()
    crawler = VenuePhotoCrawlerInstagram()
    foursquare_ids = get_all_foursquare_ids()
    #fetched_ids = get_all_photo_fetched_venue_id_instagram()
    for foursquare_id in foursquare_ids.keys():
        """NOTICE THIS IS TO AVOID REPEATING FETCHING"""
        #if foursquare_id not in fetched_ids:
        print foursquare_id, foursquare_ids[foursquare_id]
        crawler.grab_photos(foursquare_id)
#instagram_test()

if __name__ == '__main__':
    main()
    instagram_test()

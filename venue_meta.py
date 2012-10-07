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

class VenueMetaCrawler:
    def __init__(self):
        self.client = foursquare.Foursquare(config.foursquare_client_id, client_secret=config.foursquare_client_secret)
    def grab_meta_data(self, venue_id):
        venue = self.client.venues(venue_id)
        save_venue_meta(venue)
        return venue

class VenuePhotoCrawlerFoursquare:
    def __init__(self):
        self.client = foursquare.Foursquare(config.foursquare_client_id, client_secret=config.foursquare_client_secret)
    def grab_photo(self, venue_id):
        for offset in range(0, 1000, 200):
            venue_photo = self.client.venues.photos(VENUE_ID = venue_id, params = {'limit':200, 'group':'venue', 'offset':offset})
            save_venue_photo_4sq(venue_photo, venue_id)

class VenueTipsCrawler:
    def __init__(self):
        self.client = foursquare.Foursquare(config.foursquare_client_id, client_secret=config.foursquare_client_secret)
    def grab_tip(self, venue_id):
        for offset in range(0,1000,100):
            print 'now offset is ',offset
            venue_tip = self.client.venues.tips(VENUE_ID = venue_id, params = {'limit':100, 'offset':offset} )
            save_venue_tip(venue_tip, venue_id)

class VenuePhotoCrawlerInstagram:
    def __init__(self):
        self.client = InstagramAPI(client_id = config.instagram_client_id, client_secret = config.instagram_client_secret)
    def fetch_instagram_id(self, foursquare_id):
        print 'foursquare id is ',foursquare_id
        res = self.client.location_search(foursquare_v2_id=foursquare_id)
        return res[0].id
    def show_popular(self):
        popular_media = self.client.media_popular(20)
        for media in popular_media:
            print media.caption.text
    def grab_photos(self, foursquare_id):
        try:
            instagram_id = self.fetch_instagram_id(foursquare_id)
            gen = self.client.location_recent_media(count=200, location_id = instagram_id, as_generator=True, max_pages=500)#, return_json=True)
            page_cnt = 0
        except:
            return 
        for page in gen:
            save_photo_instagram(page[0], foursquare_id, instagram_id)    
            print 'fetching page',page_cnt
            page_cnt+=1
            time.sleep(config.instagram_API_pause)

def main():
    add_table_venue_meta()
    add_table_venue_photo_4sq()
    add_table_venue_tips()

    client = foursquare.Foursquare(config.foursquare_client_id, client_secret=config.foursquare_client_secret)
    
    all_plazas = client.venues.search(params={'near':'New York City', 'limit':50, 'intent':'browse', 'radius':5000, 'categoryId':'4bf58dd8d48988d164941735'} )
    
    cnt = 0
    for v in all_plazas['venues']:
        time.sleep(10)
        venue_id = v['id']
        print 'progress: %d/%d -> %s'%(cnt, len(all_plazas), v['name'])
        crawler = VenueMetaCrawler()
        crawler.grab_meta_data(venue_id)
        crawler = VenuePhotoCrawlerFoursquare()
        crawler.grab_photo(venue_id)
        crawler = VenueTipsCrawler()
        crawler.grab_tip(venue_id)

#main()

def instagram_test():
    add_table_venue_photo_instagram()
    crawler = VenuePhotoCrawlerInstagram()
    foursquare_ids = get_all_foursquare_ids()
    fetched_ids = get_all_photo_fetched_venue_id_instagram()
    for foursquare_id in foursquare_ids.keys():
        if foursquare_id not in fetched_ids:
            print foursquare_id, foursquare_ids[foursquare_id]
            crawler.grab_photos(foursquare_id)
#instagram_test()

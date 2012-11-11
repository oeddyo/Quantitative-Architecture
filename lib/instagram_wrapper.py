"""
    For a venue id, grab all it's meta data
"""
from instagram.client import InstagramAPI
import config
import time

def default_client():
    client = InstagramAPI(client_id = config.instagram_client_id, client_secret = config.instagram_client_secret)
    return client
def download_instagram_photos( venue_id, start_timestamp, end_timestamp, client = default_client()):
    """
    Download instagram photo for a foursquare veneu. This venue dosn't necessarily exist on instagra. 
    Need to fire a search on instagram API to find the instagram id first, and then do download.
    Parameters:
    client - connect instagram api
    venue_id - foursquare v2 id
    start_date - start date. Default would be infinity
    end_date - end date. Default would be today
    """
    instagram_id = client.location_search(foursquare_v2_id = venue_id)
    instagram_id = instagram_id[0].id
    print 'instagram id ', instagram_id
    gen = client.location_recent_media(count = 200, location_id = instagram_id,  max_pages=500, min_timestamp=start_timestamp, max_timestamp=end_timestamp, as_generator = True)
    for page in gen:
        yield (page[0], venue_id, instagram_id)


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

if __name__ == '__main__':
    gen = download_instagram_photos(venue_id = '3fd66200f964a520d7f11ee3', start_timestamp = 1352153848, end_timestamp = 1352653871)

    for p in gen:
        print p

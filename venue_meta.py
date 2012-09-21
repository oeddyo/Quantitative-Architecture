"""
    For a venue id, grab all it's meta data
"""

import foursquare
import config

class VenueMetaCrawler:
    def __init__(self):
        self.client = foursquare.Foursquare(config.client_id, client_secret=config.client_secret)
    def grab_data(self, venue_id):
        venue = self.client.venues(venue_id)
        print venue

def main():
    crawler = VenueMetaCrawler()
    crawler.grab_data('40a55d80f964a52020f31ee3')

main()

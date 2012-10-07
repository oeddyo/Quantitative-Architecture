from venue_meta import VenueMetaCrawler
from venue_meta import VenuePhotoCrawlerFoursquare
from threading import Thread
from time import sleep
class Job():
    def __init__(self, venue_ids):
        if type(venue_ids) is not list:
            raise TypeError
        self.status = "Wating"
        self.venue_count = 0
        self.venue_ids = venue_ids
    
    def submit(self, downloading_locker):
        _meta_crawler = VenueMetaCrawler()
        _foursqaure_photo_crawler = VenuePhotoCrawlerFoursquare()
        for id in self.venue_ids:
            self.venue_count += 1
            self.status = 'Fetching meta data for venue id = '+str(id)
            #_meta_crawler.grab_meta_data(id)
            sleep(1)
            self.status = 'Fetching foursquare photo data for venue id = ' +str(id)
            #_foursqaure_photo_crawler.grab_photo(id)
            sleep(1)
        downloading_locker.clear() 
        return "job done"
     
    def report(self):
        return [self.status, self.venue_count]
        #print self.status

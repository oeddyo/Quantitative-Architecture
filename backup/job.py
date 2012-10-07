from venue_meta import VenueMetaCrawler
from venue_meta import VenuePhotoCrawlerFoursquare
import threading
class Job(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.status = "Begin"
        self.queue = queue
        pass
    
    def run(self):
        metaCrawler = VenueMetaCrawler()
        _counter = 0
        while True:
            id = self.queue.get()
            _v = metaCrawler.grab_meta_data(id)
            print 'checking ',_v['venue']['name']
            self.queue.task_done()
        """
        for id in venue_ids:
            print 'In downloading!!!', _counter
            _v = metaCrawler.grab_meta_data(id)
            self.status = 'Downloading '+str( _counter) + '-th venue meta'
            _counter += 1
        """

    def report(self):
        return self.status
        #print self.status

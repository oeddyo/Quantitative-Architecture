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
from threading import Thread
from job import Job

def test():
    add_table_venue_photo_4sq()
    client = foursquare.Foursquare(config.foursquare_client_id, client_secret=config.foursquare_client_secret)
    all_plazas = client.venues.search(params={'near':'New York City', 'limit':50, 'intent':'browse', 'radius':5000, 'categoryId':'4bf58dd8d48988d164941735'} )
    ids = []
    for v in all_plazas['venues']:
        ids.append(v['id'])
    for id in ids:
        job = Job()
        t = Thread(target=job.download, args=([id],))
        #t.setDaemon(True)
        t.start()
test()

def main():
    job = Job()
    client = foursquare.Foursquare(config.foursquare_client_id, client_secret=config.foursquare_client_secret)
    all_plazas = client.venues.search(params={'near':'New York City', 'limit':50, 'intent':'browse', 'radius':5000, 'categoryId':'4bf58dd8d48988d164941735'} )

    ids = []
    for v in all_plazas['venues']:
        ids.append(v['id'])
    
    t = Thread(target=job.download, args=(ids,))
    t.setDaemon(True)
    t.start()
    print 'The thread started'
    
    second = 0
    while(1):
        second += 1
        time.sleep(1)
        job.report()
#main()

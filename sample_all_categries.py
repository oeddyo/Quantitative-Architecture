from venue_meta import VenuePhotoCrawlerInstagram
from lib.mysql_connect import connect_to_mysql
import random
import logging
logging.basicConfig(filename='./sample.log', level=logging.DEBUG,
        format='[%(levelname)s] (%(threadName)-10s) %(message)s',
        )

def main():
    sql = "select * from manhattan_venues_meta where checkinsCount > 1000 and tipCount > 20"
    cursor = connect_to_mysql()
    cursor.execute(sql)
    all_venues = cursor.fetchall()

    ids = []
    for r in all_venues:
        ids.append( r['id'] )
    
    ids = set(ids)

    crawler = VenuePhotoCrawlerInstagram()
    
    cnt = 0 
    for id in ids:
        cnt += 1
        logging.debug('crawling %d'%(cnt))
        if random.random()<0.35:
            crawler.grab_photos(id, 10)
   
main()

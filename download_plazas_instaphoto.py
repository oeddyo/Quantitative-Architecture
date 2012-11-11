"""
Download all the plazas metas for all the ids in plazas
"""

from lib.instagram_wrapper import download_instagram_photos
from lib.mysql_connect import connect_to_mysql
from lib.storage_interface import save_photo_instagram
from lib.multithread import do_multithread_job
import time

def do_work(venue_id):
    photos_gen = download_instagram_photos(venue_id, 1, time.time()) 
    for p in photos_gen:
        (data, venue_id, instagram_id) = p
        save_photo_instagram(data, venue_id, instagram_id, 'plazas_instaphoto')

def main():
    sql = "select id from plazas_nyc"
    cursor = connect_to_mysql()
    cursor.execute(sql)
    
    ids = ['4aad5ee2f964a520f25f20e3']
    for r in cursor.fetchall():
        ids.append(r['id'])
    do_multithread_job(do_work, ids, 10, './log/download_instagram.log')

main()

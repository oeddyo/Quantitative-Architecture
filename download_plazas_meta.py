"""
Download all the plazas metas for all the ids in plazas
"""

from lib.foursqure_wrapper import download_meta_data
from lib.mysql_connect import connect_to_mysql
from lib.storage_interface import save_venue_meta
from lib.multithread import do_multithread_job

def do_work(venue_id):
    meta_data = download_meta_data(venue_id)
    save_venue_meta(meta_data, table = 'plazas_meta')

def main():
    sql = "select id from plazas"
    cursor = connect_to_mysql()
    cursor.execute(sql)
    
    ids = []
    count = 10
    for r in cursor.fetchall():
        ids.append(r['id'])
        count-=1;
        if(count<=0):break
    do_multithread_job(do_work, ids, 10, 'do_multi.log')
main()

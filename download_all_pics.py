from lib.mysql_connect import connect_to_mysql

from urllib import urlretrieve
import os
from lib.multithread import do_multithread_job


def do_work(venue_id):
    sql = "select standard_resolution as url, plazas_meta.name as name from plazas_instaphoto, plazas_meta where plazas_instaphoto.foursquare_venue_id = plazas_meta.id and plazas_instaphoto.foursquare_venue_id = '"+venue_id+"'"
    cursor =  connect_to_mysql()
    cursor.execute(sql)
    rows = cursor.fetchall()
    my_cnt = 0
    
    #for k in files_dic.keys():
    k = rows[0]['name']
    download_path = '/Users/eddiexie/work/plaza_insta_pics/'
    if not os.path.exists(download_path+k):
        os.mkdir(download_path+k)
    pic_count = 0
    for r in rows:
        _url = r['url'][r['url'].find('http'):].strip()
        try:
            pic_count+=1
            if(pic_count>=500):
                break
            print 'working on %s %s\t %d'%(k,_url, pic_count)
            out_path = download_path+k+'/'+str(pic_count)+'.jpg'
            urlretrieve(_url, out_path)
        except:
            continue

def main():
    sql = """select distinct(foursquare_venue_id) as id from plazas_instaphoto"""
    cursor = connect_to_mysql()
    cursor.execute(sql)
    ids = []
    for r in cursor.fetchall():
        ids.append(r['id'])
    do_multithread_job(do_work, ids, 20, './log/dump_pics.log')
main()
